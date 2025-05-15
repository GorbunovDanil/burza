import React from "react";
import { Favorites } from "./pages/Favorites";
import { Dashboard } from "./pages/Dashboard";
import { LogConsole } from "./pages/LogConsole";

export default function App() {
  return (
    <div className="max-w-md mx-auto p-4">
      <Favorites />
      <Dashboard />
      <LogConsole />
    </div>
  );
}
