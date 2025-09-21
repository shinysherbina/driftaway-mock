import React from "react";

const ActivitiesRenderer = ({ data }) => {
  const itinerary = data?.data?.itinerary || data?.itinerary;
  const summary = data?.data?.summary || data?.summary;
  const location = data?.data?.location || data?.location;

  console.log("ActivitiesRenderer received data:", data);

  if (!itinerary) {
    return <p className="text-gray-500">No activity data available.</p>;
  }

  return (
    <div className="flex flex-col gap-4">
      <p className="text-gray-600 font-medium">
        {summary ||
          `Here's your adventure itinerary for ${
            location || "your destination"
          }.`}
      </p>

      {itinerary.map((dayPlan, index) => (
        <div key={index} className="mb-6">
          <p className="font-semibold text-blue-600 text-lg">
            {dayPlan.day} – {dayPlan.date}
          </p>

          {dayPlan.activities.map((activity) => (
            <div
              key={activity.id}
              className="ml-4 mt-2 p-4 bg-white rounded-lg shadow-sm border"
            >
              <div className="flex flex-col lg:flex-row gap-4">
                <img
                  src={activity.imageUrl}
                  alt={activity.name}
                  className="w-full lg:w-40 h-32 object-cover rounded-md"
                />
                <div className="flex flex-col justify-between">
                  <p className="text-gray-800 font-bold text-lg">
                    {activity.name}
                  </p>
                  <p className="text-gray-600 text-sm">
                    Location: {activity.location} | Type: {activity.type}
                  </p>
                  <p className="text-gray-500 text-sm italic">
                    {activity.reason}
                  </p>
                  <p className="text-gray-500 text-sm">
                    Rating: ⭐ {activity.rating} ({activity.reviewCount}{" "}
                    reviews)
                  </p>
                  <p className="text-gray-500 text-sm">
                    Tags: {activity.tags?.join(", ") || "None"}
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
            </div>
          ))}
        </div>
      ))}
    </div>
  );
};

export default ActivitiesRenderer;
