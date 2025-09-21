
export const mockTrip = {
  destination: "Lonavala, India",
  itinerary: [
    {
      day: 1,
      theme: "Arrival and Relaxation",
      activities: [
        { time: "12:00 PM", description: "Check-in to your hotel and freshen up." },
        { time: "02:00 PM", description: "Lunch at a local restaurant." },
        { time: "04:00 PM", description: "Visit Lonavala Lake for a serene evening." },
        { time: "08:00 PM", description: "Dinner at the hotel." },
      ],
    },
    {
      day: 2,
      theme: "Adventure and Sightseeing",
      activities: [
        { time: "09:00 AM", description: "Trek to Tiger's Point for breathtaking views." },
        { time: "01:00 PM", description: "Lunch at a restaurant near Tiger's Point." },
        { time: "03:00 PM", description: "Explore the historic Karla Caves." },
        { time: "07:00 PM", description: "Dinner at a dhaba for authentic local food." },
      ],
    },
    {
        day: 3,
        theme: "Departure",
        activities: [
            { time: "10:00 AM", description: "Enjoy a final breakfast at the hotel." },
            { time: "11:00 AM", description: "Check-out and depart from Lonavala." }
        ]
    }
  ],
  weather: {
    temperature: "28°C",
    condition: "Sunny",
    advice: "Pack light clothes!",
  },
  hotel: {
    name: "Luxury resort with mountain views",
    checkIn: "3:00 PM",
  },
  food: {
    recommendation: "Local cuisine tour. Don't miss the Vada Pav!",
  },
  activities: {
    recommendation: "Trekking to Tiger's Point, exploring Karla Caves.",
  },
  transport: {
    recommendation: "Local taxis and auto-rickshaws recommended.",
  },
  budget: {
    dailySpend: "₹3000-5000",
  },
};
