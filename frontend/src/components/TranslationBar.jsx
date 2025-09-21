import React from 'react';
import { useTranslation } from '../context/TranslationContext';

const languages = [
  { code: 'en', name: 'English' },
  { code: 'hi', name: 'Hindi' },
  { code: 'ta', name: 'Tamil' },
  { code: 'te', name: 'Telugu' },
  { code: 'bn', name: 'Bengali' },
  { code: 'kn', name: 'Kannada' },
  { code: 'ml', name: 'Malayalam' },
  { code: 'mr', name: 'Marathi' },
  { code: 'gu', name: 'Gujarati' },
  { code: 'pa', name: 'Punjabi' },
  { code: 'ur', name: 'Urdu' },
];

const TranslationBar = () => {
  const { selectedLanguage, setLanguage } = useTranslation();

  const handleChange = (event) => {
    setLanguage(event.target.value);
  };

  return (
    <div className="w-full bg-gray-800 text-white p-2 flex justify-end items-center shadow-md fixed top-0 left-0 z-50">
      <label htmlFor="language-select" className="mr-2 text-sm">Translate:</label>
      <select
        id="language-select"
        value={selectedLanguage}
        onChange={handleChange}
        className="bg-gray-700 text-white text-sm rounded px-2 py-1 focus:outline-none focus:ring-2 focus:ring-blue-500"
      >
        {languages.map((lang) => (
          <option key={lang.code} value={lang.name}>
            {lang.name}
          </option>
        ))}
      </select>
    </div>
  );
};

export default TranslationBar;
