export const addToBookHistory = (bookId, bookName) => {
    const stored = localStorage.getItem('previousBooks');
    const previousBooks = stored ? JSON.parse(stored) : [];
    const newBook = { id: bookId.trim(), name: bookName };
    const newBooks = [newBook, ...previousBooks.filter(book => book.id !== bookId)]
      .slice(0, 5);
    localStorage.setItem('previousBooks', JSON.stringify(newBooks));
    return newBooks;
  };
  
  export const getBookHistory = () => {
    const stored = localStorage.getItem('previousBooks');
    return stored ? JSON.parse(stored) : [];
  };