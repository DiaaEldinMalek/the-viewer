'use client'; // Required for hooks

import {getBookHistory } from '../utils/bookHistory';
import SearchBar from '../src/components/SearchBar';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';

export default function Home() {
  const [bookId, setBookId] = useState('');
  const [isLoading, setIsLoading] = useState(true);
  const [previousBooks, setPreviousBooks] = useState([]);
  const [pingResponse, setPingResponse] = useState(null); // State to store ping response
  const router = useRouter();

  useEffect(() => {
    setIsLoading(false);
    setPreviousBooks(getBookHistory());
  }, []);

  const handleSearch = (e) => {
    e.preventDefault();
    if (bookId.trim() && !isLoading) {
      router.push(`/book/${bookId.trim()}`);
    }
  };

  const testServer = async () => {
    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_BACKEND_API_BASE_URL}/ping`,
        {
          method: 'GET',
          headers: {
            'ngrok-skip-browser-warning': 'true',
          }
        }
      );
      
      if (response.ok) {
        setPingResponse("✓");
      } else {
        setPingResponse('Server error');
      }
    } catch (error) {
      setPingResponse('Failed to connect to server');
    }
  };

  return (
    <div className="home-container">
      <div className="container">
        <main className="main">
          <SearchBar />
        </main>
      </div>
      <h1>{process.env.NEXT_PUBLIC_APP_NAME}</h1>
      <div className="main-content">
        <form onSubmit={handleSearch} className="search-form">
          <input
            type="number"
            value={bookId}
            onChange={(e) => setBookId(e.target.value)}
            placeholder="..or enter book ID"
            required
            disabled={isLoading}
          />
          <button type="submit">View Book</button>
        </form>
        
        <div className="previous-books">
          <h3>Previously Viewed Books</h3>
          {previousBooks.length > 0 ? (
            <ul>
              {previousBooks.map((book) => (
                <li key={book.id}>
                  <button onClick={() => router.push(`/book/${book.id}`)}>
                    {book.id}-{book.name}
                  </button>
                </li>
              ))}
            </ul>
          ) : (
            <p>No books viewed yet</p>
          )}
        </div>

        {/* Test Server Button */}
        <div className="test-server">
          
          <button onClick={testServer}>Ping </button>
          {<p>{pingResponse}</p>}
        </div>
      </div>
    </div>
  );
}