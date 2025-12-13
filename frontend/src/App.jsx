import { useState, useEffect, useRef } from "react";
import TypingLoader from "./components/typingloader";
import ThemeToggle from "./components/themetoggle";
import ReactMarkdown from "react-markdown";
import { PlusIcon, TrashIcon, ChevronDownIcon } from "@heroicons/react/24/outline";

export default function App() {
  const [conversations, setConversations] = useState([
    { id: 1, title: "New Chat", messages: [] },
  ]);
  const [activeConversationId, setActiveConversationId] = useState(1);
  const [query, setQuery] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [displayedText, setDisplayedText] = useState(""); // Track streamed text

  const inputRef = useRef(null);
  const messagesEndRef = useRef(null);

  const activeConversation = conversations.find(
    (c) => c.id === activeConversationId
  );

  // Auto-focus input
  useEffect(() => {
    inputRef.current?.focus();
  }, [activeConversationId]);

  // Auto-scroll to bottom
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [activeConversation?.messages, displayedText, isLoading]);

  // Stream text animation
  useEffect(() => {
    if (!isLoading && activeConversation?.messages.length > 0) {
      const lastMessage = activeConversation.messages[activeConversation.messages.length - 1];
      if (lastMessage.role === "assistant") {
        // Message is complete, reset displayedText
        setDisplayedText("");
      }
    }
  }, [activeConversation?.messages, isLoading]);

  async function askBackend() {
    if (!query.trim() || isLoading) return;

    const userQuery = query;
    setQuery("");
    setDisplayedText("");

    // Add user message
    setConversations((prev) =>
      prev.map((conv) => {
        if (conv.id === activeConversationId) {
          return {
            ...conv,
            messages: [
              ...conv.messages,
              { role: "user", content: userQuery, id: Date.now() },
            ],
          };
        }
        return conv;
      })
    );

    setIsLoading(true);

    try {
      const res = await fetch(
        `http://127.0.0.1:8000/chat-llm?query=${encodeURIComponent(userQuery)}`
      );

      const data = await res.json();
      const answer = data.answer || "No response found.";

      // Add assistant message immediately
      const messageId = Date.now() + 1;
      setConversations((prev) =>
        prev.map((conv) => {
          if (conv.id === activeConversationId) {
            const newMessages = [
              ...conv.messages,
              { role: "assistant", content: answer, id: messageId, isStreaming: true },
            ];

            // Update conversation title if it's the first message
            const updatedConv = {
              ...conv,
              messages: newMessages,
            };

            if (conv.messages.length === 1) {
              updatedConv.title =
                userQuery.substring(0, 30) +
                (userQuery.length > 30 ? "..." : "");
            }

            return updatedConv;
          }
          return conv;
        })
      );

      // Stream the text character by character
      let currentIndex = 0;
      const streamInterval = setInterval(() => {
        if (currentIndex < answer.length) {
          setDisplayedText(answer.substring(0, currentIndex + 1));
          currentIndex++;
        } else {
          clearInterval(streamInterval);
          // Mark message as complete
          setConversations((prev) =>
            prev.map((conv) => {
              if (conv.id === activeConversationId) {
                return {
                  ...conv,
                  messages: conv.messages.map((msg) =>
                    msg.id === messageId ? { ...msg, isStreaming: false } : msg
                  ),
                };
              }
              return conv;
            })
          );
          setIsLoading(false);
        }
      }, 10); // Adjust speed: lower = faster, higher = slower

      return () => clearInterval(streamInterval);
    } catch (err) {
      setConversations((prev) =>
        prev.map((conv) => {
          if (conv.id === activeConversationId) {
            return {
              ...conv,
              messages: [
                ...conv.messages,
                {
                  role: "assistant",
                  content: "⚠️ Error connecting to backend server",
                  id: Date.now() + 1,
                  isStreaming: false,
                },
              ],
            };
          }
          return conv;
        })
      );
      setIsLoading(false);
    }
  }

  function startNewChat() {
    const newId = Math.max(...conversations.map((c) => c.id), 0) + 1;
    setConversations((prev) => [
      ...prev,
      { id: newId, title: "New Chat", messages: [] },
    ]);
    setActiveConversationId(newId);
  }

  function deleteConversation(id) {
    const remaining = conversations.filter((c) => c.id !== id);
    if (remaining.length === 0) {
      startNewChat();
    } else {
      setConversations(remaining);
      if (activeConversationId === id) {
        setActiveConversationId(remaining[0].id);
      }
    }
  }

  function clearAllConversations() {
    setConversations([{ id: 1, title: "New Chat", messages: [] }]);
    setActiveConversationId(1);
  }

  return (
    <div className="h-screen w-screen flex bg-white dark:bg-gray-900 text-gray-900 dark:text-white transition-colors duration-300">
      {/* SIDEBAR */}
      <div
        className={`${
          sidebarOpen ? "w-64" : "w-0"
        } bg-gray-50 dark:bg-gray-800 border-r border-gray-200 dark:border-gray-700 flex flex-col transition-all duration-300 overflow-hidden`}
      >
        {/* New Chat Button */}
        <button
          onClick={startNewChat}
          className="m-3 p-3 rounded-lg bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 dark:hover:bg-gray-600 flex items-center justify-center gap-2 font-medium transition-colors"
        >
          <PlusIcon className="w-5 h-5" />
          New Chat
        </button>

        {/* Chat History */}
        <div className="flex-1 overflow-y-auto px-2">
          <p className="text-xs font-semibold text-gray-500 dark:text-gray-400 px-2 py-3 uppercase tracking-wide">
            Chat History
          </p>
          {conversations.map((conv) => (
            <div
              key={conv.id}
              onClick={() => setActiveConversationId(conv.id)}
              className={`p-3 rounded-lg mb-2 cursor-pointer transition-colors flex items-center justify-between group ${
                activeConversationId === conv.id
                  ? "bg-gray-200 dark:bg-gray-700"
                  : "hover:bg-gray-100 dark:hover:bg-gray-700"
              }`}
            >
              <span className="text-sm truncate flex-1">{conv.title}</span>
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  deleteConversation(conv.id);
                }}
                className="opacity-0 group-hover:opacity-100 p-1 hover:bg-gray-300 dark:hover:bg-gray-600 rounded transition-all"
              >
                <TrashIcon className="w-4 h-4 text-red-500" />
              </button>
            </div>
          ))}
        </div>

        {/* Clear All Button */}
        <button
          onClick={clearAllConversations}
          className="m-3 p-2 text-xs rounded-lg bg-red-100 dark:bg-red-900/30 hover:bg-red-200 dark:hover:bg-red-900/50 text-red-600 dark:text-red-400 transition-colors"
        >
          Clear all conversations
        </button>
      </div>

      {/* MAIN CHAT AREA */}
      <div className="flex-1 flex flex-col">
        {/* Header */}
        <div className="border-b border-gray-200 dark:border-gray-700 p-4 flex items-center justify-between bg-white dark:bg-gray-900">
          <button
            onClick={() => setSidebarOpen(!sidebarOpen)}
            className="p-2 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-lg transition-colors"
          >
            <ChevronDownIcon
              className={`w-6 h-6 transition-transform duration-300 ${
                sidebarOpen ? "rotate-90" : ""
              }`}
            />
          </button>
          <h1 className="text-xl font-bold flex-1 text-center">
            Resume Chatbot
          </h1>
          <div className="w-10 flex justify-end">
            <ThemeToggle />
          </div>
        </div>

        {/* Messages Area */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-white dark:bg-gray-900">
          {activeConversation?.messages.length === 0 && (
            <div className="h-full flex items-center justify-center">
              <div className="text-center">
                <h2 className="text-3xl font-bold mb-2">
                  Hi, I'm Shashank's Resume Assistant
                </h2>
                <p className="text-gray-500 dark:text-gray-400 mb-8 max-w-lg">
                  Ask me anything about Shashank's experience, skills, projects,
                  and achievements. Feel free to explore their background!
                </p>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3 max-w-2xl">
                  {[
                    "What experience do you have?",
                    "Tell me about your projects",
                    "What awards have you won?",
                    "What are your technical skills?",
                  ].map((example, i) => (
                    <button
                      key={i}
                      onClick={() => {
                        setQuery(example);
                        setTimeout(() => {
                          inputRef.current?.focus();
                        }, 0);
                      }}
                      className="p-4 rounded-lg border border-gray-300 dark:border-gray-600 hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors text-left text-sm font-medium"
                    >
                      {example}
                    </button>
                  ))}
                </div>
              </div>
            </div>
          )}

          {activeConversation?.messages.map((msg, idx) => {
            // Check if this is the last message and it's being streamed
            const isLastMessage =
              idx === activeConversation.messages.length - 1 && msg.role === "assistant";
            const textToDisplay = isLastMessage ? displayedText : msg.content;

            return (
              <div
                key={msg.id}
                className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}
              >
                <div
                  className={`max-w-2xl px-4 py-3 rounded-lg ${
                    msg.role === "user"
                      ? "bg-blue-500 text-white rounded-br-none"
                      : "bg-gray-100 dark:bg-gray-800 text-gray-900 dark:text-white rounded-bl-none"
                  }`}
                >
                  {msg.role === "user" ? (
                    <p className="whitespace-pre-wrap text-sm leading-relaxed">
                      {msg.content}
                    </p>
                  ) : (
                    <div className="text-sm leading-relaxed space-y-2">
                      <ReactMarkdown
                        allowedElements={['p', 'br', 'strong', 'em', 'h2', 'h3', 'ul', 'ol', 'li', 'a', 'code', 'pre']}
                        unwrapDisallowed={true}
                        components={{
                          p: ({ children }) => <p className="mb-2">{children}</p>,
                          strong: ({ children }) => <strong className="font-bold">{children}</strong>,
                          em: ({ children }) => <em className="italic">{children}</em>,
                          h2: ({ children }) => <h2 className="text-base font-bold mt-3 mb-2 text-blue-600 dark:text-blue-400">{children}</h2>,
                          h3: ({ children }) => <h3 className="text-sm font-bold mt-2 mb-1 text-gray-800 dark:text-gray-200">{children}</h3>,
                          ul: ({ children }) => <ul className="list-disc list-inside ml-2 space-y-1">{children}</ul>,
                          ol: ({ children }) => <ol className="list-decimal list-inside ml-2 space-y-1">{children}</ol>,
                          li: ({ children }) => <li className="text-sm">{children}</li>,
                          a: ({ children, href }) => (
                            <a 
                              href={href}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="text-blue-500 dark:text-blue-400 hover:underline break-all"
                            >
                              {children}
                            </a>
                          ),
                          code: ({ inline, children }) => 
                            inline ? (
                              <code className="bg-gray-300 dark:bg-gray-700 px-1.5 py-0.5 rounded text-xs font-mono">
                                {children}
                              </code>
                            ) : (
                              <pre className="bg-gray-300 dark:bg-gray-700 p-2 rounded my-2 text-xs overflow-x-auto">
                                <code className="font-mono">{children}</code>
                              </pre>
                            ),
                        }}
                      >
                        {textToDisplay}
                      </ReactMarkdown>
                      {isLastMessage && isLoading && <span className="inline-block w-2 h-5 bg-gray-900 dark:bg-white ml-1 animate-pulse"></span>}
                    </div>
                  )}
                </div>
              </div>
            );
          })}

          {isLoading && activeConversation?.messages.length === 0 && (
            <div className="flex justify-start">
              <div className="bg-gray-100 dark:bg-gray-800 px-4 py-3 rounded-lg rounded-bl-none">
                <TypingLoader />
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Input Area */}
        <div className="border-t border-gray-200 dark:border-gray-700 p-4 bg-white dark:bg-gray-900">
          <div className="flex gap-3">
            <input
              ref={inputRef}
              type="text"
              placeholder="Message Resume Assistant..."
              value={query}
              disabled={isLoading}
              onChange={(e) => setQuery(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter" && !e.shiftKey) {
                  e.preventDefault();
                  askBackend();
                }
              }}
              className="flex-1 px-4 py-3 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
            />
            <button
              onClick={askBackend}
              disabled={isLoading || !query.trim()}
              className="px-6 py-3 rounded-lg bg-blue-500 hover:bg-blue-600 disabled:bg-blue-300 disabled:cursor-not-allowed text-white font-medium transition-colors flex items-center justify-center"
            >
              Send
            </button>
          </div>
          <p className="text-xs text-gray-500 dark:text-gray-400 mt-2 text-center">
            Shift + Enter for new line
          </p>
        </div>
      </div>
    </div>
  );
}
