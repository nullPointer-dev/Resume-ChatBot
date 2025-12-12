# 📄 Resume Chatbot – AI-Powered Portfolio Assistant

An intelligent chatbot that answers interview-style and resume-based questions using your personal resume JSON.  
Built with **FastAPI**, **custom vector search**, and **Google Gemini 2.5 Flash**.

This project acts as an **interactive AI version of your resume**, capable of answering:

- “What ML experience do you have?”
- “Tell me about yourself”
- “Why should we hire you?”
- “What are your strengths?”

---

## 🚀 Features

### 🔍 Custom Vector Search (Lightweight RAG)
- No external database required  
- Token-based embeddings + cosine similarity  
- Auto-indexes resume at startup  

### 🤖 Gemini-Powered Answers
- Clean, first-person, interview-style responses  
- Uses **gemini-2.5-flash** (Generative Language API)

### 🧠 Interview Question Detection
When user asks:
- “Why should we hire you?”
- “Tell me about yourself”
- “What value do you bring?”

→ System automatically uses **full resume context**.

### ⚡ FastAPI Backend
- Modular  
- Predictable structure  
- Instantly deployable  

---

## 📁 Project Structure
```md
resume-chatbot-json/
│
├── backend/
│   ├── app.py
│   ├── vector_store.py
│   ├── flatten.py
│   ├── rewrite.py
│   ├── embed.py
│   ├── example_resume.json
│   └── .env
│
├── frontend/
│   ├── public/
│   │   └── favicon.ico
│   │
│   ├── src/
│   │   ├── assets/
│   │   │
│   │   ├── components/
│   │   │   ├── typingloader.jsx
│   │   │   └── themetoggle.jsx
│   │   │
│   │   ├── styles/
│   │   │   └── globals.css
│   │   │
│   │   ├── App.jsx
│   │   └── main.jsx
│   │
│   ├── index.html
│   ├── package.json
│   ├── package-lock.json
│   ├── postcss.config.js
│   ├── tailwind.config.js
│   └── vite.config.js
│
└── README.md
└── .gitignore
```

---

## 🛠 Tech Stack

- Python 3.10+
- FastAPI
- Google Gemini 2.5 Flash API
- Custom Embedding Engine
- Uvicorn

---

## 🧠 How It Works (RAG Pipeline)

The backend uses a lightweight Retrieval-Augmented Generation (RAG) system without any external vector database.

### **1. Resume JSON → Flattened Chunks**
Your structured resume is converted into readable text blocks:
- Basics  
- Skills  
- Experience  
- Projects  
- Education  

### **2. Custom Embedding Engine**
Each chunk is embedded using:
- Tokenization  
- Word frequency vectors  
- Cosine similarity scoring  

This avoids heavy libraries like FAISS and keeps the system lightweight.

### **3. Vector Search**
When a query comes in:
- The system retrieves the most relevant chunks  
- If similarity is low → it falls back to the **full resume**  
- If query is an interview-style question → it *always* uses full resume

### **4. Gemini 2.5 Flash Rewrites the Answer**
Gemini receives:
- The user query  
- The retrieved resume info  
- Strict rewriting rules (“first person", “professional”, and “resume only”)

This generates clean, polished interview-ready responses.

---

## 🚀 Future Enhancements

Here are the planned improvements for expanding the project:

### **Frontend Enhancements**
- Build a React UI with chat interface  
- Add animated typing effect  
- Add resume upload interface  

### **Backend Enhancements**
- Support multiple resumes (profiles)
- Add caching for responses  
- Add authentication for private resumes  

### **AI Features**
- Add scoring for interview answers  
- Add auto-improvement mode for resume optimization  
- Support follow-up questioning  

### **Deployment**
- One-click deployment to Render / Railway  
- Add Dockerfile for containerization  

---

## 📜 License

This project is licensed under the **MIT License**.

You are free to:
- Use  
- Modify  
- Distribute  
- Reproduce  

…as long as the original copyright notice is included.

---

## ⭐ Show Your Support

If you found this project helpful:

- ⭐ **Star the repository**
- 🔄 **Share it with others**
- 🐛 Open issues / feature requests  
- 💬 Leave feedback to help improve it  

Your support encourages more updates, new features, and continuous improvements.

---



