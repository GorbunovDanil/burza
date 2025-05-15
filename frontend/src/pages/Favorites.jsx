import React, { useEffect, useState } from "react";
import { api } from "../lib/api";

export function Favorites() {
  const [list, setList] = useState([]);
  const [input, setInput] = useState("");

  // Load on mount
  useEffect(() => {
    api
      .get("favorites/")
      .then((res) => setList(res.data))
      .catch((err) => console.error("Failed to fetch favorites", err));
  }, []);

  // Save current list back to the server
  const saveFavorites = () => {
    api
      .put("favorites/", { tickers: list })
      .then((res) => setList(res.data))
      .catch((err) => console.error("Failed to save favorites", err));
  };

  return (
    <div className="p-4 border rounded mb-4">
      <h2 className="text-lg font-semibold mb-2">Favorites</h2>

      {/* List */}
      <ul className="mb-3 space-y-1">
        {list.map((ticker, idx) => (
          <li key={idx} className="flex justify-between items-center">
            <span>{ticker}</span>
            <button
              className="text-red-500 hover:text-red-700"
              onClick={() => setList(prev => prev.filter(t => t !== ticker))}
            >
              ✕
            </button>
          </li>
        ))}
      </ul>

      {/* Add input */}
      <div className="flex space-x-2 mb-3">
        <input
          type="text"
          placeholder="Ticker"
          className="border p-1 flex-1 rounded"
          value={input}
          onChange={e => setInput(e.target.value.toUpperCase())}
          onKeyDown={e => {
            if (e.key === "Enter" && input) {
              setList(prev => Array.from(new Set([...prev, input])));
              setInput("");
            }
          }}
        />
        <button
          className="px-3 bg-blue-600 text-white rounded"
          onClick={() => {
            if (input) {
              setList(prev => Array.from(new Set([...prev, input])));
              setInput("");
            }
          }}
        >
          Add
        </button>
      </div>

      {/* Save button */}
      <button
        className="px-4 py-2 bg-green-600 text-white rounded"
        onClick={saveFavorites}
      >
        Save
      </button>
    </div>
  );
}
