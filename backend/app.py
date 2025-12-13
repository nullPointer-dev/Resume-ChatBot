from fastapi import FastAPI
from fastapi.responses import JSONResponse
import json
import os
import requests
from dotenv import load_dotenv
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from vector_store import vector_store
from flatten import load_resume_json, flatten_resume
from rewrite import to_first_person

# ---------------------------------------
# Load environment variables
# ---------------------------------------
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# ---------------------------------------
# FastAPI Lifespan – Auto Build Index
# ---------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Automatically loads the resume, flattens it, and builds
    the vector index before the server starts handling requests.
    """
    print("⚡ Building vector index on startup...")

    data = load_resume_json()
    chunks = flatten_resume(data)

    vector_store.documents = []
    for ch in chunks:
        vector_store.add(ch["text"], ch["metadata"])

    print(f"✅ Vector index built with {len(vector_store.documents)} chunks.")
    yield  # Server runs after this


app = FastAPI(title="Resume Chatbot Backend", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], #can restrict later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# ---------------------------------------
# Paths
# ---------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EXAMPLE_PATH = os.path.join(BASE_DIR, "example_resume.json")

# ---------------------------------------
# Interview Question Trigger List
# ---------------------------------------
INTERVIEW_QUESTIONS = [
    "why should we hire you",
    "tell me about yourself",
    "what are your strengths",
    "what are your weaknesses",
    "why do you want this job",
    "why do you want to work here",
    "what makes you a good fit",
    "what value do you bring",
]


# ---------------------------------------
# Root Endpoint
# ---------------------------------------
@app.get("/")
def root():
    return {"status": "ok", "message": "Resume Chatbot Backend running properly"}


# ---------------------------------------
# Return Raw Resume JSON
# ---------------------------------------
@app.get("/resume")
def get_resume():
    if not os.path.exists(EXAMPLE_PATH):
        return JSONResponse(
            status_code=404,
            content={"error": "example_resume.json not found"},
        )

    with open(EXAMPLE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


# ---------------------------------------
# Flatten Resume Content
# ---------------------------------------
@app.get("/flatten")
def flatten_resume_endpoint():
    data = load_resume_json()
    chunks = flatten_resume(data)
    return {"chunks": chunks, "count": len(chunks)}


# ---------------------------------------
# Rebuild Vector Index Manually (optional)
# ---------------------------------------
@app.get("/build_index")
def build_index():
    data = load_resume_json()
    chunks = flatten_resume(data)

    vector_store.documents = []
    for ch in chunks:
        vector_store.add(ch["text"], ch["metadata"])

    return {"status": "ok", "indexed_chunks": len(vector_store.documents)}


# ---------------------------------------
# Search Only (No LLM)
# ---------------------------------------
@app.get("/search")
def search(query: str):
    results = vector_store.search(query)
    return {
        "query": query,
        "results": [
            {
                "score": score,
                "text": doc["text"],
                "metadata": doc["metadata"],
            }
            for score, doc in results
        ],
    }


# ---------------------------------------
# Basic Chat Without LLM
# ---------------------------------------
@app.get("/chat")
def chat(query: str):
    results = vector_store.search(query)

    if not results or results[0][0] < 0.10:
        return {"answer": "I couldn't find information about that in my resume.", "sources": []}

    _, top_doc = results[0]
    answer_text = to_first_person(top_doc["text"])

    return {"query": query, "answer": answer_text, "sources": [top_doc["metadata"]]}


# ---------------------------------------
# Full Chat With Gemini LLM + RAG Logic
# ---------------------------------------
@app.get("/chat-llm")
def chat_llm(query: str):
    query_lower = query.lower()

    # Interview question → Use full resume
    if any(q in query_lower for q in INTERVIEW_QUESTIONS):
        full_resume = " ".join(doc["text"] for doc in vector_store.documents)
        return generate_llm_response(query, full_resume, sources=[])

    # RAG retrieval
    results = vector_store.search(query)

    # Fallback to full resume if retrieval is weak
    if not results or results[0][0] < 0.10:
        full_resume = " ".join(doc["text"] for doc in vector_store.documents)
        return generate_llm_response(query, full_resume, sources=[])

    _, top_doc = results[0]
    return generate_llm_response(query, top_doc.get("text", ""), sources=[top_doc.get("metadata", {})])


# ---------------------------------------
# Gemini API Helper
# ---------------------------------------
def generate_llm_response(query: str, resume_text: str, sources: list):
    """
    Sends the query + retrieved resume text to Gemini
    and returns a well-formatted, markdown-styled answer.
    """
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"

    prompt = f"""
You are Shashank's resume assistant. Your role is to provide well-formatted, professional responses about their background.

User Query: "{query}"
Resume Information: "{resume_text}"

INSTRUCTIONS:
1. Speak as Shashank using "I" and "my"
2. Use ONLY information from the provided resume
3. Format your response using markdown for better readability:
   - Use **bold** for important terms
   - Use bullet points (•) for lists of items
   - Use numbered lists (1., 2., etc.) for sequential information
   - Use ## for section headings when applicable
   - Include links in [text](url) format when URLs are provided
4. Keep responses concise but informative
5. Be professional and clear

Example format:
## My Experience

• **Role** at Company (dates): Description of work
• Key achievement with metrics
• Another significant accomplishment

## Skills
• Python, JavaScript, React
• Machine Learning, Deep Learning
• Team Leadership, Communication

If the response includes projects, certifications, or awards with links, format them as:
- **Project Name**: Brief description - [GitHub](url) | [Live Demo](url)
- **Certification**: Name - Issuer (Date) - [Credential](url)

Now generate your response:
"""

    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    params = {"key": GEMINI_API_KEY}

    try:
        response = requests.post(url, json=payload, params=params)
        data = response.json()

        print("RAW GEMINI RESPONSE:", data)

        answer = data["candidates"][0]["content"]["parts"][0]["text"]
        return {"query": query, "answer": answer, "sources": sources}

    except Exception as e:
        return {"query": query, "answer": f"Error: {e}", "sources": sources}
