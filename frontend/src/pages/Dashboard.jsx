import React, { useState } from "react";
import { api } from "../lib/api";

export function Dashboard() {
  const [running, setRunning] = useState(false);

  const runNow = async () => {
    setRunning(true);
    try {
      await api.post("start/");
    } catch (err) {
      console.error("Failed to trigger pipeline", err);
      alert("Error starting pipeline");
    } finally {
      setRunning(false);
    }
  };

  return (
    <div className="p-4 border rounded mb-4">
      <h2 className="text-lg font-semibold mb-2">Dashboard</h2>
      <button
        onClick={runNow}
        disabled={running}
        className={`px-4 py-2 rounded ${
          running ? "bg-gray-500" : "bg-indigo-600 hover:bg-indigo-700"
        } text-white`}
      >
        {running ? "Running…" : "Spustit"}
      </button>
    </div>
  );
}
