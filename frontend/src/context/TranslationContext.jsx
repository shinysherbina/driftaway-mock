import React, { createContext, useState, useContext, useEffect } from 'react';

// Create the Translation Context
const TranslationContext = createContext();

// Translation Provider component
export const TranslationProvider = ({ children }) => {
  // Initialize language from localStorage or default to 'English'
  const [selectedLanguage, setSelectedLanguage] = useState(() => {
    return localStorage.getItem('selectedLanguage') || 'English';
  });

  // Effect to persist selected language to localStorage
  useEffect(() => {
    localStorage.setItem('selectedLanguage', selectedLanguage);
    // Placeholder for actual translation logic
    // In a real application, you would call a translation API here
    // For example: translatePageContent(selectedLanguage);
    console.log(`Translating page content to: ${selectedLanguage}`);
    // This is where you'd integrate with Gemini's multilingual capabilities
    // to dynamically translate the DOM content.
  }, [selectedLanguage]);

  const setLanguage = (language) => {
    setSelectedLanguage(language);
  };

  return (
    <TranslationContext.Provider value={{ selectedLanguage, setLanguage }}>
      {children}
    </TranslationContext.Provider>
  );
};

// Custom hook to use the translation context
export const useTranslation = () => {
  const context = useContext(TranslationContext);
  if (context === undefined) {
    throw new Error('useTranslation must be used within a TranslationProvider');
  }
  return context;
};
