import React from "react";
import { useLocation } from "react-router-dom";

const TripPlan = () => {
  const location = useLocation();
  const { itinerary, destination } = location.state || {};

  console.log("TripPlan - location.state:", location.state);
  console.log("TripPlan - itinerary:", itinerary);

  if (!itinerary) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-100">
        <div className="bg-white p-8 rounded-lg shadow-md text-center">
          <h1 className="text-3xl font-bold mb-4">No Itinerary Found</h1>
          <p className="text-lg text-gray-600">
            Please go back and generate an itinerary.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="h-screen w-screen relative bg-[url('/assets/Plan.jpg')] bg-cover bg-center bg-no-repeat flex flex-row items-center justify-start">
      <div
        className="flex flex-row h-2/3 m-8 w-5/6 overflow-y-auto"
        style={{
          backgroundColor: "whitesmoke",
          margin: "2rem",
          padding: "2rem",
          borderRadius: "2rem",
        }}
      >
        <div className="max-w-4xl mx-auto bg-white p-8 rounded-lg shadow-md">
          <h1 className="text-4xl font-bold mb-6 text-center text-gray-800">
            Your Trip to {destination}
          </h1>

          {/* Primary Transport */}
          <section className="mb-8">
            <h2 className="text-2xl font-semibold mb-4 text-gray-700">
              Primary Transport
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="bg-blue-50 p-4 rounded-lg shadow-sm">
                <h3 className="font-medium text-blue-700">
                  Outbound: {itinerary.primary_transport.outbound.type}
                </h3>
                <p>{itinerary.primary_transport.outbound.details}</p>
                <p>Price: ${itinerary.primary_transport.outbound.price}</p>
                <a
                  href={itinerary.primary_transport.outbound.booking_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-blue-500 hover:underline"
                >
                  Book Now
                </a>
              </div>
              <div className="bg-blue-50 p-4 rounded-lg shadow-sm">
                <h3 className="font-medium text-blue-700">
                  Inbound: {itinerary.primary_transport.inbound.type}
                </h3>
                <p>{itinerary.primary_transport.inbound.details}</p>
                <p>Price: ${itinerary.primary_transport.inbound.price}</p>
                <a
                  href={itinerary.primary_transport.inbound.booking_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-blue-500 hover:underline"
                >
                  Book Now
                </a>
              </div>
            </div>
          </section>

          {/* Local Transport */}
          <section className="mb-8">
            <h2 className="text-2xl font-semibold mb-4 text-gray-700">
              Local Transport
            </h2>
            <div className="bg-green-50 p-4 rounded-lg shadow-sm">
              <h3 className="font-medium text-green-700">
                Provider: {itinerary.local_transport.provider}
              </h3>
              <p>{itinerary.local_transport.details}</p>
              <p>Price: ${itinerary.local_transport.price}</p>
              <a
                href={itinerary.local_transport.booking_url}
                target="_blank"
                rel="noopener noreferrer"
                className="text-green-500 hover:underline"
              >
                Book Now
              </a>
            </div>
          </section>

          {/* Daily Activities */}
          <section className="mb-8">
            <h2 className="text-2xl font-semibold mb-4 text-gray-700">
              Daily Activities
            </h2>
            {itinerary.daily_activities.map((dayPlan, index) => (
              <div
                key={index}
                className="mb-6 bg-purple-50 p-4 rounded-lg shadow-sm"
              >
                <h3 className="text-xl font-medium text-purple-700 mb-3">
                  {dayPlan.day} - {dayPlan.date}
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {dayPlan.activities.map((activity, activityIndex) => (
                    <div
                      key={activityIndex}
                      className="bg-white p-3 rounded-lg shadow-sm flex items-center space-x-3"
                    >
                      {activity.imageUrl && (
                        <img
                          src={activity.imageUrl}
                          alt={activity.name}
                          className="w-16 h-16 object-cover rounded-md"
                        />
                      )}
                      <div>
                        <p className="font-semibold text-gray-800">
                          {activity.name} ({activity.time})
                        </p>
                        <p className="text-gray-600 text-sm">
                          {activity.description}
                        </p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </section>

          {/* Cafes to Try */}
          <section className="mb-8">
            <h2 className="text-2xl font-semibold mb-4 text-gray-700">
              Cafes to Try
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {itinerary.cafes_to_try.map((cafe, index) => (
                <div
                  key={index}
                  className="bg-yellow-50 p-4 rounded-lg shadow-sm"
                >
                  <h3 className="font-medium text-yellow-700">
                    {cafe.name} ({cafe.cuisine})
                  </h3>
                  <p>
                    Rating: {cafe.rating} | Location: {cafe.location}
                  </p>
                  <p className="text-sm italic">{cafe.reason}</p>
                  <a
                    href={cafe.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-yellow-600 hover:underline"
                  >
                    View Details
                  </a>
                </div>
              ))}
            </div>
          </section>

          {/* Weather Forecast */}
          <section className="mb-8">
            <h2 className="text-2xl font-semibold mb-4 text-gray-700">
              Weather Forecast
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {itinerary.weather_forecast.map((weather, index) => (
                <div
                  key={index}
                  className="bg-blue-50 p-4 rounded-lg shadow-sm text-center"
                >
                  <h3 className="font-medium text-blue-700">{weather.date}</h3>
                  <p className="text-lg">{weather.summary}</p>
                  <p className="text-xl font-bold">{weather.temperature}</p>
                </div>
              ))}
            </div>
          </section>
        </div>
      </div>
    </div>
  );
};

export default TripPlan;
