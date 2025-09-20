import React from 'react';

const MapEmbed = ({ destination }) => {
  // Encode the destination to ensure it's URL-safe
  const encodedDestination = encodeURIComponent(destination);
  const mapSrc = `https://www.google.com/maps?q=${encodedDestination}&output=embed`;

  return (
    <div className="w-full h-full flex items-center justify-center">
      <iframe
        title={`Google Map of ${destination}`}
        src={mapSrc}
        width="100%"
        height="100%"
        style={{ border: 0, minHeight: '400px' }}
        allowFullScreen=""
        loading="lazy"
        referrerPolicy="no-referrer-when-downgrade"
        className="rounded-lg shadow-lg"
      ></iframe>
    </div>
  );
};

export default MapEmbed;
