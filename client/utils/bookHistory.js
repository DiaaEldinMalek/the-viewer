export const addToBookHistory = (bookId) => {
    const stored = localStorage.getItem('previousBooks');
    const previousBooks = stored ? JSON.parse(stored) : [];
    const newBooks = [...new Set([bookId.trim(), ...previousBooks])].slice(0, 5);
    localStorage.setItem('previousBooks', JSON.stringify(newBooks));
    return newBooks;
  };
  
  export const getBookHistory = () => {
    const stored = localStorage.getItem('previousBooks');
    return stored ? JSON.parse(stored) : [];
  };