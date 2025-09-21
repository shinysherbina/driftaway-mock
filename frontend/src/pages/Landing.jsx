import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import backgroundImage from "../assets/background.png"; // Import the background image

const Landing = () => {
  const [destination, setDestination] = useState("");
  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault();
    if (destination.trim()) {
      navigate("/input", { state: { destination } });
    }
  };

  return (
    <div className="h-screen w-screen relative bg-[url('/assets/Plan.jpg')] bg-cover bg-center bg-no-repeat flex flex-col items-center justify-start">
      <div className="w-full h-full flex flex-col items-center justify-center align-center p-8 gap-8">
        <div className="flex flex-col gap-2  items-center justify-center align-center">
          <div className="flex flex-row gap-4">
            <h1
              style={{ fontFamily: "Poppins, sans-serif" }}
              className="text-[4rem] m-0"
            >
              DRIFT{" "}
            </h1>
            <h1 className="text-[6rem]">Away</h1>{" "}
          </div>
          <p
            className="text-white text-3xl"
            style={{
              color: "white",
              fontSize: "1.5rem",
              marginTop: 0,
              marginBottom: "2rem",
            }}
          >
            Plan your getaway with ease
          </p>
        </div>

        <div
          className="mt-24 w-[60%] text-center flex flex-row justify-evenly bg-[#107bbf] rounded-3xl"
          style={{ borderRadius: "2rem", padding: "0.25rem" }}
        >
          {/* Tagline */}
          <p
            className="text-lg text-white mb-8 font-semibold rounded-3xl"
            style={{ color: "white", borderRadius: "1rem" }}
          >
            So... where can we drift off today?
          </p>

          {/* Destination Input Form */}
          <form
            onSubmit={handleSubmit}
            className="flex flex-row gap-4 w-full items-center justify-center"
          >
            <input
              type="text"
              placeholder="Enter your dream destination..."
              className="flex-grow p-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 text-lg"
              style={{
                padding: "1rem",
                fontSize: "1rem",
                borderRadius: "1rem",
              }}
              value={destination}
              onChange={(e) => setDestination(e.target.value)}
              aria-label="Destination input"
            />
            <button
              type="submit"
              className="text-white py-3 rounded-xl hover:brightness-90 transition duration-300 ease-in-out text-lg font-bold"
              style={{
                backgroundColor: "#2bc8bd",
                color: "white",
                borderRadius: "1rem",
                border: "none",
                fontSize: "1.5rem",
                padding: "0.5rem 1.5rem",
              }}
            >
              Drift
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default Landing;
