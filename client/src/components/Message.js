import { marked } from 'marked';

export default function Message({ sender, text }) {
  const html = marked(text);
  
  return (
    <div className={`message ${sender}`}>
      <div 
        className="message-content"
        dangerouslySetInnerHTML={{ __html: html }}
      />
    </div>
  );
}