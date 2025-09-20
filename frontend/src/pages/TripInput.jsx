import React, { useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import MapEmbed from '../components/MapEmbed'; // Import the new MapEmbed component

const TripInput = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const destination = location.state?.destination || 'Lonavala, India'; // Default for map if not passed
  const [chatMessage, setChatMessage] = useState('');

  const handleGenerateItinerary = () => {
    // In a real app, you'd send chat messages and destination to a backend
    // For now, just navigate to the TripPlan page
    navigate('/tripplan', { state: { destination, chatMessage } });
  };

  return (
    <div className="min-h-screen flex flex-col lg:flex-row bg-gray-100">
      {/* Left Panel: MCP Data (Placeholder) */}
      <div className="w-full lg:w-1/4 bg-white p-4 shadow-md flex flex-col">
        <h2 className="text-2xl font-bold mb-4 text-gray-800">Trip Details for {destination}</h2>
        <div className="flex flex-col gap-4 overflow-y-auto flex-grow">
          <div className="p-4 bg-blue-50 rounded-lg shadow-sm">
            <h3 className="font-semibold text-lg text-blue-700">Weather</h3>
            <p className="text-gray-600">Sunny, 28°C. Pack light clothes!</p>
          </div>
          <div className="p-4 bg-green-50 rounded-lg shadow-sm">
            <h3 className="font-semibold text-lg text-green-700">Hotel</h3>
            <p className="text-gray-600">Luxury resort with mountain views. Check-in 3 PM.</p>
          </div>
          <div className="p-4 bg-yellow-50 rounded-lg shadow-sm">
            <h3 className="font-semibold text-lg text-yellow-700">Food</h3>
            <p className="text-gray-600">Local cuisine tour. Don't miss the Vada Pav!</p>
          </div>
          <div className="p-4 bg-red-50 rounded-lg shadow-sm">
            <h3 className="font-semibold text-lg text-red-700">Activities</h3>
            <p className="text-gray-600">Trekking to Tiger's Point, exploring Karla Caves.</p>
          </div>
          <div className="p-4 bg-purple-50 rounded-lg shadow-sm">
            <h3 className="font-semibold text-lg text-purple-700">Transport</h3>
            <p className="text-gray-600">Local taxis and auto-rickshaws recommended.</p>
          </div>
          <div className="p-4 bg-indigo-50 rounded-lg shadow-sm">
            <h3 className="font-semibold text-lg text-indigo-700">Budget</h3>
            <p className="text-gray-600">Estimated daily spend: ₹3000-5000.</p>
          </div>
        </div>
      </div>

      {/* Middle Section: Google Map */}
      <div className="w-full lg:w-1/2 p-4 flex items-center justify-center">
        <MapEmbed destination={destination} />
      </div>

      {/* Right Panel: Chatbox Interface */}
      <div className="w-full lg:w-1/4 bg-white p-4 shadow-md flex flex-col">
        <h2 className="text-2xl font-bold mb-4 text-gray-800">Chat with Driftaway AI</h2>
        <div className="flex-grow border border-gray-300 rounded-lg p-4 mb-4 overflow-y-auto bg-gray-50">
          {/* Placeholder for chat messages */}
          <div className="mb-2 text-gray-700"><span className="font-semibold">AI:</span> Hello! How can I help you plan your trip to {destination}?</div>
          <div className="mb-2 text-right text-blue-700"><span className="font-semibold">You:</span> Tell me more about local attractions.</div>
        </div>
        <div className="flex gap-2">
          <input
            type="text"
            placeholder="Type your message..."
            className="flex-grow p-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            value={chatMessage}
            onChange={(e) => setChatMessage(e.target.value)}
            aria-label="Chat message input"
          />
          <button
            onClick={handleGenerateItinerary}
            className="bg-green-600 text-white py-3 px-6 rounded-md hover:bg-green-700 transition duration-300 ease-in-out font-bold"
          >
            Generate Itinerary
          </button>
        </div>
      </div>
    </div>
  );
};

export default TripInput;