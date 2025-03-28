export default function BookViewer({ content }) {
    return (
      <div className="book-viewer">
        <h1>{content.title}</h1>
        <div className="book-content">
          {content.content.split('\n').map((paragraph, i) => (
            <p key={i}>{paragraph}</p>
          ))}
        </div>
      </div>
    );
  }