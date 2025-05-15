import React, { useEffect, useState, useRef } from "react";

export function LogConsole() {
  const [lines, setLines] = useState([]);
  const bottomRef = useRef();

  useEffect(() => {
    const es = new EventSource("https://localhost:8000/api/logs/stream/");
    es.onmessage = (e) => {
      setLines((prev) => [...prev, e.data]);
    };
    es.onerror = () => {
      console.error("Log stream error");
      es.close();
    };
    return () => es.close();
  }, []);

  // Scroll to bottom on new line
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [lines]);

  return (
    <div className="p-4 bg-black text-green-300 font-mono h-48 overflow-auto rounded mb-4">
      {lines.map((line, idx) => (
        <div key={idx}>{line}</div>
      ))}
      <div ref={bottomRef} />
    </div>
  );
}
