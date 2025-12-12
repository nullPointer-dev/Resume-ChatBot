import { useState, useEffect, useRef } from "react";
import TypingLoader from "./components/typingloader";
import ThemeToggle from "./components/themetoggle";

export default function App() {
  const [query, setQuery] = useState("");
  const [response, setResponse] = useState("");
  const [displayText, setDisplayText] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const inputRef = useRef(null);

  // Auto-focus input on load
  useEffect(() => {
    inputRef.current?.focus();
  }, []);

  // Typing animation
  useEffect(() => {
    setDisplayText("");
    if (!response) return;

    let i = 0;
    const interval = setInterval(() => {
      setDisplayText(response.substring(0, i));
      i++;
      if (i > response.length) clearInterval(interval);
    }, 15);

    return () => clearInterval(interval);
  }, [response]);

  async function askBackend() {
    if (!query.trim() || isLoading) return;

    setIsLoading(true);
    setResponse("");
    setDisplayText("");

    try {
      const res = await fetch(
        `http://127.0.0.1:8000/chat-llm?query=${encodeURIComponent(query)}`
      );

      const data = await res.json();
      setResponse(data.answer || "No response found.");
    } catch (err) {
      setResponse("⚠️ Error connecting to backend server");
    }

    setIsLoading(false);
  }

  return (
    <div
      className="
        min-h-screen flex items-center justify-center p-6 
        bg-gradient-to-br 
        from-purple-900 via-black to-purple-800 
        dark:from-gray-100 dark:via-gray-200 dark:to-white
        text-white dark:text-black
        transition-all duration-500
      "
    >
      {/* Theme Toggle Button */}
      <div className="absolute top-6 right-6 z-50">
        <ThemeToggle />
      </div>

      {/* MAIN CARD */}
      <div
        className="
          w-full max-w-3xl mx-auto p-10 mt-10 rounded-3xl
          bg-white/10 dark:bg-white/60
          backdrop-blur-2xl
          border border-white/20 dark:border-black/20
          shadow-[0_0_60px_rgba(200,100,255,0.4)]
          hover:shadow-[0_0_90px_rgba(200,100,255,0.7)]
          transition-all duration-300
        "
      >
        <h1 className="text-4xl font-extrabold text-center mb-8 tracking-wide">
          Resume Chatbot
        </h1>

        {/* INPUT BOX */}
        <div className="relative group">
          <input
            ref={inputRef}
            type="text"
            placeholder="Ask anything about Shashank..."
            value={query}
            disabled={isLoading}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter") askBackend();
            }}
            className="
              w-full px-5 py-4 rounded-2xl text-white dark:text-black text-lg
              bg-white/20 dark:bg-white/80
              border border-white/30 dark:border-black/20 
              backdrop-blur-xl shadow-lg placeholder-white/60 dark:placeholder-black/50
              disabled:opacity-50 disabled:cursor-not-allowed
              focus:outline-none focus:ring-2 focus:ring-purple-400
              transition-all duration-300
            "
          />

          {/* Glow */}
          <div
            className="
              absolute inset-0 rounded-2xl pointer-events-none
              opacity-0 group-focus-within:opacity-30
              bg-purple-400 blur-xl transition-all duration-300
            "
          ></div>
        </div>

        {/* BUTTON */}
        <button
          onClick={askBackend}
          disabled={isLoading}
          className="
            w-full py-4 mt-5 rounded-2xl text-lg font-semibold
            bg-gradient-to-r from-purple-500 to-purple-700
            dark:from-purple-400 dark:to-purple-600
            hover:from-purple-600 hover:to-purple-800
            disabled:opacity-50 disabled:cursor-not-allowed
            shadow-lg active:scale-95 transition-all duration-200
          "
        >
          {isLoading ? "Thinking..." : "Ask Chatbot"}
        </button>

        {/* RESPONSE OUTPUT */}
        {(isLoading || displayText) && (
          <div
            className="
              mt-8 p-6 rounded-2xl
              bg-black/40 dark:bg-black/10
              border border-white/20 dark:border-black/20
              shadow-lg backdrop-blur-xl
              animate-fadeIn
            "
          >
            {isLoading ? (
              <TypingLoader />
            ) : (
              <p className="whitespace-pre-line leading-relaxed text-lg">
                {displayText}
              </p>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
