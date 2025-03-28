import { useState, useEffect } from 'react';

const SearchBar = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [searchResults, setSearchResults] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  // Debounce function to limit API calls
  useEffect(() => {
    const timerId = setTimeout(() => {
      if (searchTerm.trim() !== '') {
        performSearch(searchTerm);
      } else {
        setSearchResults([]);
      }
    }, 300); // 300ms debounce delay

    return () => {
      clearTimeout(timerId);
    };
  }, [searchTerm]);

  const performSearch = async (query) => {
    setIsLoading(true);
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_API_BASE_URL}/search`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: query })
      });

      if (!response.ok) throw new Error('Search failed');
      const data = await response.json();
      setSearchResults(data.data);
    } catch (error) {
      console.error('Search error:', error);
      setSearchResults([]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="search-container">
      <input
        type="text"
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
        placeholder="Search in CSV..."
        className="search-input"
      />
      
      {isLoading && <div className="loading-indicator">Searching...</div>}
      
      {searchResults.length > 0 && (
        <div className="results-container">
          {searchResults.map((result) => (
            <div key={result.book_id} className="result-item">
              <p><b>{result.book_id}</b> {result.title}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default SearchBar;