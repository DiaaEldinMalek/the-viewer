'use client'; // Required for hooks

import { useState } from 'react';
import { useRouter } from 'next/navigation';

export default function Home() {
  const [bookId, setBookId] = useState('');
  const router = useRouter();

  const handleSearch = (e) => {
    e.preventDefault();
    if (bookId.trim()) {
      router.push(`/book/${bookId.trim()}`);
    }
  };

  return (
    <div className="home-container">
      <h1>Book Chat Application</h1>
      <form onSubmit={handleSearch} className="search-form">
        <input
          type="text"
          value={bookId}
          onChange={(e) => setBookId(e.target.value)}
          placeholder="Enter Book ID"
          required
        />
        <button type="submit">View Book</button>
      </form>
    </div>
  );
}