import React from "react";

const TransportRenderer = ({ data }) => {
  if (!data || !data.options) {
    return <p className="text-gray-500">No transport data available.</p>;
  }

  return (
    <div className="flex flex-col gap-4">
      <p className="text-gray-600 font-medium">
        {data.summary || "Here are some transport options."}
      </p>
      {data.options.map((option, index) => (
        <div key={index} className="p-4 bg-purple-50 rounded-lg shadow-sm">
          <p className="font-semibold text-purple-700">{option.mode}</p>
          <p className="text-gray-800">
            Estimated Cost: {option.estimatedCost}
          </p>
          <p className="text-gray-600">{option.description}</p>
          <button
            type="submit"
            className="text-white py-3 rounded-xl hover:brightness-90 transition duration-300 ease-in-out text-lg font-bold"
            style={{
              backgroundColor: "#2bc8bd",
              color: "white",
              borderRadius: "1rem",
              border: "none",
              fontSize: "1rem",
              padding: "0.5rem 1.5rem",
            }}
          >
            Select
          </button>
        </div>
      ))}
    </div>
  );
};

export default TransportRenderer;
