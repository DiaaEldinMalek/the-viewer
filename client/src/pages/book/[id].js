import { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import BookViewer from '../../components/BookViewer';
import ChatInterface from '../../components/ChatInterface';

export default function BookPage() {
  const [book, setBook] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const router = useRouter();
  const { id } = router.query;

  useEffect(() => {
    if (!id) return;

    const fetchBook = async () => {
      try {
        console.info(`Routing to ${process.env.NEXT_PUBLIC_BACKEND_API_BASE_URL}`)
        const response = await fetch(
            `${process.env.NEXT_PUBLIC_BACKEND_API_BASE_URL}/get_book_content/${id}`,
            {
              method: 'GET',
              headers: {
                'Content-Type': 'application/json',
                'ngrok-skip-browser-warning': 'true',
              }
            }
          );
        if (!response.ok) throw new Error('Book not found');
        const data = await response.json();
        setBook(data.data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchBook();
  }, [id]);

  if (loading) return <div className="loading">Loading...</div>;
  if (error) return <div className="error">Error: {error}</div>;
  if (!book) return <div>Book not found</div>;

  return (
    <div className="book-container">
      <div className="book-header">
        <button onClick={() => router.push('/')} className="back-button">
          ← Back to Search
        </button>
      </div>
      <BookViewer content={book} />
      <ChatInterface bookId={id} />
    </div>
  );
}