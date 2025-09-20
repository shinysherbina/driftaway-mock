import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const Landing = () => {
  const [destination, setDestination] = useState('');
  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault();
    if (destination.trim()) {
      navigate('/input', { state: { destination } });
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-br from-blue-400 to-purple-600 p-4">
      <div className="bg-white p-8 rounded-lg shadow-xl text-center max-w-md w-full">
        {/* Logo Placeholder */}
        <div className="mb-6">
          <img src="/logo.png" alt="Driftaway Logo" className="mx-auto h-24 w-24 object-contain" />
          {/* Or use placeholder text if no image is available */}
          {/* <h1 className="text-5xl font-bold text-gray-800">Driftaway</h1> */}
        </div>

        {/* Tagline */}
        <p className="text-xl text-gray-700 mb-8 font-semibold">So... where can we drift off today?</p>

        {/* Destination Input Form */}
        <form onSubmit={handleSubmit} className="flex flex-col gap-4">
          <input
            type="text"
            placeholder="Enter your dream destination..."
            className="w-full p-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 text-lg"
            value={destination}
            onChange={(e) => setDestination(e.target.value)}
            aria-label="Destination input"
          />
          <button
            type="submit"
            className="w-full bg-blue-600 text-white py-3 rounded-md hover:bg-blue-700 transition duration-300 ease-in-out text-lg font-bold"
          >
            Drift
          </button>
        </form>
      </div>
    </div>
  );
};

export default Landing;
