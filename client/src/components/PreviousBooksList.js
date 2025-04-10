const { getBookHistory } = require('@/utils/bookHistory');
import { useState, useEffect } from 'react';

const PreviousBooksList = () => {
    const [previousBooks, setPreviousBooks] = useState([]);

    useEffect(() => {
        setPreviousBooks(getBookHistory());
    }, []);
    return (
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
        </div>)
}

export default PreviousBooksList