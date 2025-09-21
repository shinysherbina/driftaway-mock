import React from "react";

const FoodRenderer = ({ data }) => {
  const cafes = data?.cafes || data?.data?.cafes;
  const summary = data?.summary || data?.data?.summary;

  if (!cafes) {
    return <p className="text-gray-500">No food data available.</p>;
  }

  return (
    <div className="flex flex-col gap-4">
      <p className="text-gray-600 font-medium">
        {summary || "Here are some food recommendations."}
      </p>
      {cafes.map((cafe, index) => (
        <div
          key={index}
          className="p-4 bg-yellow-50 rounded-lg shadow-sm flex flex-col lg:flex-row gap-4"
        >
          {cafe.imageUrl && (
            <img
              src={cafe.imageUrl}
              alt={cafe.name}
              className="w-full lg:w-40 h-32 object-cover rounded-md"
            />
          )}
          <div>
            <p className="font-semibold text-yellow-700 text-lg">{cafe.name}</p>
            <p className="text-gray-800">Cuisine: {cafe.cuisine}</p>
            <p className="text-gray-600">{cafe.address}</p>
            <p className="text-gray-500 text-sm">
              Rating: ⭐ {cafe.rating} ({cafe.reviewCount} reviews)
            </p>
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
        </div>
      ))}
    </div>
  );
};

export default FoodRenderer;
