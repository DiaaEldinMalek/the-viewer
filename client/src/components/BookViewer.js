export default function BookViewer({ book }) {
    return (
      <div className="book-viewer">
        <h1>{book.title}</h1>
        <div className="book-content">
          {book.content.split('\n').map((paragraph, i) => (
            <p key={i}>{paragraph}</p>
          ))}
        </div>
      </div>
    );
  }