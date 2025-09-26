import React, { useState, useEffect } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import MapEmbed from "../components/MapEmbed.jsx";
import TripChat from "../components/TripChat.jsx";
import {
  ActivitiesRenderer,
  BudgetRenderer,
  FoodRenderer,
  HotelRenderer,
  TransportRenderer,
  WeatherRenderer,
} from "../components/mcp_renderers";

const MCP_TABS = [
  "Weather",
  "Hotel",
  "Food",
  "Activities",
  "Transport",
  "Budget",
];

const TripInput = () => {
  const location = useLocation();
  const destination = location.state?.destination || "Lonavala, India";
  const [activeTab, setActiveTab] = useState(MCP_TABS[0]);
  const [mcpData, setMcpData] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchMcpData = async () => {
      setIsLoading(true);
      setError(null);
      setMcpData(null);

      try {
        const response = await fetch(
          `/api/${activeTab.toLowerCase()}`,
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({ uid: "shiny123", destination }),
          }
        );

        if (!response.ok) {
          throw new Error(`Failed to fetch ${activeTab} data`);
        }

        const data = await response.json();
        console.log(`Fetched ${activeTab} data:`, data);
        setMcpData(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setIsLoading(false);
      }
    };

    fetchMcpData();
  }, [activeTab, destination]);

  const handleGenerateItinerary = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await fetch(
        `/api/itinerary?uid=shiny123`,
        {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
        }
      );

      if (!response.ok) {
        throw new Error("Failed to generate itinerary");
      }

      const itineraryData = await response.json();
      console.log("Generated Itinerary:", itineraryData);
      navigate("/trip-plan", { state: { itinerary: itineraryData, destination } });
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  const renderMcpData = () => {
    if (isLoading) {
      return <p>Loading {activeTab} data...</p>;
    }

    if (error) {
      return <p className="text-red-500">Error: {error}</p>;
    }

    if (!mcpData) {
      return <p>No data available for {activeTab}.</p>;
    }

    switch (activeTab) {
      case "Weather":
        return <WeatherRenderer data={mcpData} />;
      case "Hotel":
        return <HotelRenderer data={mcpData} />;
      case "Food":
        return <FoodRenderer data={mcpData} />;
      case "Activities":
        return <ActivitiesRenderer data={mcpData} />;
      case "Transport":
        return <TransportRenderer data={mcpData} />;
      case "Budget":
        return <BudgetRenderer data={mcpData} />;
      default:
        return <p>Select a category to view details.</p>;
    }
  };

  return (
    <div className="h-screen w-screen relative bg-[url('/assets/Plan.jpg')] bg-cover bg-center bg-no-repeat flex flex-row items-center justify-start">
      <div
        className="flex flex-row h-2/3 m-8"
        style={{
          backgroundColor: "whitesmoke",
          margin: "2rem",
          padding: "2rem",
          borderRadius: "2rem",
        }}
      >
        <div className="w-full lg:w-1/4 bg-white p-4 shadow-md flex flex-col">
          <h2 className="text-2xl font-bold mb-4 text-gray-800">
            Trip Details for {destination}
          </h2>
          {/* Horizontally scrollable tabs */}
          <div className="sticky flex border-b mb-4">
            {MCP_TABS.map((tab) => (
              <button
                key={tab}
                className={`py-2 px-4 whitespace-nowrap ${
                  activeTab === tab
                    ? "border-b-2 border-blue-500 text-blue-600"
                    : "text-gray-500"
                }`}
                onClick={() => setActiveTab(tab)}
              >
                {tab}
              </button>
            ))}
          </div>
          {/* Vertically scrollable content area */}
          <div className="flex flex-col gap-4 overflow-y-auto flex-grow">
            <div className="p-4 bg-gray-50 rounded-lg shadow-sm">
              <h3 className="font-semibold text-lg text-gray-700">
                {activeTab}
              </h3>
              {renderMcpData()}
            </div>
          </div>
        </div>

        <div className="w-full lg:w-1/2 p-4 flex items-center justify-center">
          <MapEmbed destination={destination} />
        </div>

        <div className="w-full flex flex-col lg:w-1/4 p-4">
          <TripChat destination={destination} />
          <button
            type="button"
            onClick={handleGenerateItinerary}
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
            Generate Itinerary
          </button>
        </div>
      </div>
    </div>
  );
};

export default TripInput;
