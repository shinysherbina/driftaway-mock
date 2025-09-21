import React from "react";

const HotelRenderer = ({ data }) => {
  const hotels = data?.hotels || data?.data?.hotels;
  const summary = data?.summary || data?.data?.summary;

  if (!hotels) {
    return <p className="text-gray-500">No hotel data available.</p>;
  }

  return (
    <div className="flex flex-col gap-4">
      <p className="text-gray-600 font-medium">
        {summary || "Here are some hotel recommendations."}
      </p>
      {hotels.map((hotel, index) => (
        <div
          key={index}
          className="p-4 bg-green-50 rounded-lg shadow-sm flex flex-col lg:flex-row gap-4"
        >
          {hotel.imageUrl && (
            <img
              src={hotel.imageUrl}
              alt={hotel.name}
              className="w-full lg:w-40 h-32 object-cover rounded-md"
            />
          )}
          <div>
            <p className="font-semibold text-green-700 text-lg">{hotel.name}</p>
            <p className="text-gray-800">{hotel.price} per night</p>
            <p className="text-gray-600">{hotel.address}</p>
            <p className="text-gray-500 text-sm">
              Rating: ⭐ {hotel.rating} ({hotel.reviewCount} reviews)
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

export default HotelRenderer;
