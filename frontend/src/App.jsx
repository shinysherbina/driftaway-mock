import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Landing from './pages/Landing';
import TripInput from './pages/TripInput';
import TripPlan from './pages/TripPlan';

function App() {
  return (
    <Routes>
      <Route path="/" element={<Landing />} />
      <Route path="/input" element={<TripInput />} />
      <Route path="/tripplan" element={<TripPlan />} />
    </Routes>
  );
}

export default App;