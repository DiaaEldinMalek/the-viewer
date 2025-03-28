'use client'; // Required for hooks

import { addToBookHistory, getBookHistory } from '../utils/bookHistory';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';

export default function Home() {
  const [bookId, setBookId] = useState('');
  const [isLoading, setIsLoading] = useState(true);
  const [previousBooks, setPreviousBooks] = useState([]);
  const router = useRouter();

  useEffect(() => {
    setIsLoading(false);
    // Load previous books from localStorage
    setPreviousBooks(getBookHistory());

    // const stored = localStorage.getItem('previousBooks');
    // if (stored) {
    //   setPreviousBooks(JSON.parse(stored));
    // }
  }, []);

  const handleSearch = (e) => {
    e.preventDefault();
    if (bookId.trim() && !isLoading) {
      // Add to history if not already present
      const newBooks = addToBookHistory(bookId.trim(), `Book #${bookId.trim()}`);
      // const newBooks = [...new Set([bookId.trim(), ...previousBooks])].slice(0, 5);
      setPreviousBooks(newBooks);
      // localStorage.setItem('previousBooks', JSON.stringify(newBooks));
      router.push(`/book/${bookId.trim()}`);
    }
  };

  return (
    <div className="home-container">
      <h1>Book Chat Application</h1>
      <div className="main-content">
        <form onSubmit={handleSearch} className="search-form">
          <input
            type="number"
            value={bookId}
            onChange={(e) => setBookId(e.target.value)}
            placeholder="Enter Book ID"
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
      </div>
    </div>
  );
}