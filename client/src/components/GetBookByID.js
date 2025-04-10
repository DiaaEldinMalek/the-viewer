import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';

const GetBookByID = () => {
    const [isLoading, setIsLoading] = useState(true);
    const router = useRouter();
    const [bookId, setBookId] = useState('');
    useEffect(() => {
        setIsLoading(false);
    }, []);

    const handleSearch = (e) => {
        e.preventDefault();
        if (bookId.trim() && !isLoading) {
            router.push(`/book/${bookId.trim()}`);
        }
    };
    return (
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
        </div>
    )
}

export default GetBookByID