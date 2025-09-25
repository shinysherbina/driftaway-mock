import React, { useState, useEffect, useRef } from "react";

const TripChat = ({ destination }) => {
  const [chatHistory, setChatHistory] = useState([]);
  const [chatMessage, setChatMessage] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const chatHistoryRef = useRef(null);

  // Scroll to bottom on chat update
  useEffect(() => {
    if (chatHistoryRef.current) {
      chatHistoryRef.current.scrollTop = chatHistoryRef.current.scrollHeight;
    }
  }, [chatHistory]);

  // Send initial destination to backend on mount
  useEffect(() => {
    const sendInitialMessage = async () => {
      try {
await fetch("/chat", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            uid: "shiny123",
            destination,
            message: "init",
            session_history: [],
          }),
        });
      } catch (error) {
        console.error("Error sending initial destination:", error);
      }
    };

    sendInitialMessage();
  }, [destination]);

  const sendMessage = async () => {
    if (!chatMessage.trim()) return;
    setIsLoading(true);

    try {
      const response = await fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          uid: "shiny123",
          destination,
          message: chatMessage,
          session_history: chatHistory,
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setChatHistory(data.session_history || []);
      setChatMessage("");
    } catch (error) {
      console.error("Error sending message:", error);
      setChatHistory((prev) => [
        ...prev,
        {
          role: "assistant",
          content:
            "Error: Could not connect to the server or receive a valid response.",
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter" && !isLoading) {
      sendMessage();
    }
  };

  return (
    <div className="flex flex-col h-full bg-white rounded-lg shadow-md p-4">
      <h2 className="text-2xl font-bold mb-4 text-gray-800">
        Chat with Driftaway AI
      </h2>

      {/* Chat History */}
      <div
        ref={chatHistoryRef}
        className="flex-grow border border-gray-300 rounded-lg p-4 mb-4 overflow-y-auto bg-gray-50"
        style={{ minHeight: "200px", maxHeight: "400px" }}
      >
        {chatHistory.length === 0 && (
          <div className="text-gray-500 text-center">
            Great choice — {destination} is calling. Let’s drift away into its
            hidden gems. How many people are joining you, and when would you
            like to drift away?
          </div>
        )}
        {chatHistory.map((msg, index) => (
          <div
            key={index}
            className={`mb-2 ${
              msg.role === "user" ? "text-right" : "text-left"
            }`}
          >
            <span
              className={`inline-block p-2 rounded-lg ${
                msg.role === "user"
                  ? "bg-blue-500 text-white"
                  : "bg-gray-300 text-gray-800"
              }`}
            >
              {msg.content}
            </span>
          </div>
        ))}
        {isLoading && (
          <div className="text-center text-gray-500">
            <span className="animate-pulse">Typing...</span>
          </div>
        )}
      </div>

      {/* Input + Send */}
      <div className="flex gap-2">
        <input
          type="text"
          placeholder="Type your message..."
          className="flex-grow p-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          value={chatMessage}
          onChange={(e) => setChatMessage(e.target.value)}
          onKeyPress={handleKeyPress}
          disabled={isLoading}
          aria-label="Chat message input"
        />
        <button
          onClick={sendMessage}
          className="bg-blue-600 text-white py-3 px-6 rounded-md hover:bg-blue-700 transition duration-300 ease-in-out font-bold"
          disabled={isLoading}
        >
          Send
        </button>
      </div>
    </div>
  );
};

export default TripChat;
