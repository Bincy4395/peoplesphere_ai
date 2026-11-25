import { useState, useEffect, useRef } from "react";
import { MessageCircle, X, FileText } from "lucide-react";
import api from "../api/api";

function ChatbotWidget() {
  const [isOpen, setIsOpen] = useState(false);
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  // Conversation ID
  const [conversationId, setConversationId] = useState(null);

  const messagesEndRef = useRef(null);
  const requestIdRef = useRef(0);

  // --------------------------------------------------
  // 1. Auto-scroll to latest message
  // --------------------------------------------------
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages, loading]);

  // --------------------------------------------------
  // 2. Send message to chatbot API
  // --------------------------------------------------
  async function handleSend() {
    if (!message.trim() || loading) return;

    const userMessage = message.trim();
    const currentRequestId = ++requestIdRef.current;

    setMessages((prev) => [
      ...prev,
      {
        role: "user",
        content: userMessage,
      },
    ]);

    setMessage("");
    setLoading(true);

    try {
      // --------------------------------------------------
      // 3. Prepare API request
      // --------------------------------------------------
      const requestData = {
        message: userMessage,
        employee_id: 1,
      };

      if (conversationId) {
        requestData.conversation_id = conversationId;
      }

      // --------------------------------------------------
      // 4. Send request to backend
      // --------------------------------------------------
      const response = await api.post("/chat/", requestData);

      if (requestIdRef.current !== currentRequestId) {
        return;
      }

      // --------------------------------------------------
      // 5. Save conversation ID
      // --------------------------------------------------
      setConversationId(response.data.conversation_id);

      // --------------------------------------------------
      // 6. Extract answer, sources and context status
      // --------------------------------------------------
      const answer = response.data.answer;

      const hasRelevantContext = response.data.has_relevant_context ?? false;

      const sources = hasRelevantContext ? response.data.sources || [] : [];

      // --------------------------------------------------
      // 7. Store assistant response
      // --------------------------------------------------
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: answer,
          sources: sources,
          has_relevant_context: hasRelevantContext,
        },
      ]);
    } catch (error) {
      if (requestIdRef.current !== currentRequestId) {
        return;
      }

      console.error("Chat API Error:", error);

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: "Unable to get a response. Please try again.",
        },
      ]);
    } finally {
      if (requestIdRef.current === currentRequestId) {
        setLoading(false);
      }
    }
  }

  // --------------------------------------------------
  // 8. Start a new conversation
  // --------------------------------------------------
  function handleCloseChat() {
    requestIdRef.current += 1;

    setIsOpen(false);
    setMessages([]);
    setMessage("");
    setConversationId(null);
    setLoading(false);
  }

  // --------------------------------------------------
  // 9. Render chatbot
  // --------------------------------------------------
  return (
    <div className="chatbot-widget">
      {isOpen ? (
        <div className="chatbot-window">
          {/* Chat Header */}
          <div className="chatbot-header">
            <div>
              <h3>PeopleSphere AI</h3>
              <span>Employee Assistant</span>
            </div>

            <button onClick={handleCloseChat}>
              <X size={24} />
            </button>
          </div>

          {/* Chat Body */}
          <div className="chatbot-body">
            {messages.map((msg, index) => (
              <div
                key={index}
                className={msg.role === "user" ? "user-message" : "bot-message"}
              >
                <div>{msg.content}</div>

                {/* Source Citations */}
                {msg.role === "assistant" &&
                  msg.has_relevant_context === true &&
                  msg.sources?.length > 0 && (
                    <div className="chatbot-sources">
                      <strong>Sources</strong>

                      <ul>
                        {[
                          ...new Set(
                            msg.sources
                              .map((source) => source.source)
                              .filter(Boolean),
                          ),
                        ].map((source, sourceIndex) => (
                          <li key={sourceIndex}>
                            <FileText size={14} />
                            <span>{source}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
              </div>
            ))}

            {loading && <div className="bot-message">Thinking...</div>}

            <div ref={messagesEndRef} />
          </div>

          {/* Chat Input */}
          <div className="chatbot-input">
            <input
              type="text"
              placeholder="Ask me anything..."
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter") {
                  handleSend();
                }
              }}
            />

            <button type="button" onClick={handleSend} disabled={loading}>
              ➤
            </button>
          </div>
        </div>
      ) : (
        <button className="chatbot-toggle" onClick={() => setIsOpen(true)}>
          <MessageCircle size={27} />
          <span>Chat with AI</span>
        </button>
      )}
    </div>
  );
}

export default ChatbotWidget;
