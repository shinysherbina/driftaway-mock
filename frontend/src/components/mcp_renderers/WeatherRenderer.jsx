import React from "react";

const WeatherRenderer = ({ data }) => {
  const forecast = data?.forecast || data?.data?.forecast;
  if (!forecast) {
    return <p className="text-gray-500">No weather data available.</p>;
  }

  return (
    <div className="flex flex-col gap-4">
      <p className="text-gray-600 font-medium">
        {data.summary || data?.data?.location || "Here's the weather forecast."}
      </p>
      {forecast.map((day, index) => (
        <div key={index} className="p-4 bg-blue-50 rounded-lg shadow-sm">
          <p className="font-semibold text-blue-600">{day.date}</p>
          <p className="text-gray-800">Temperature: {day.temperature}</p>
          <p className="text-gray-600">{day.condition}</p>
        </div>
      ))}
    </div>
  );
};

export default WeatherRenderer;
