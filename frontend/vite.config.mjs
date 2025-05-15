// vite.config.mjs
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import fs from "fs";
import path from "path";

function maybeHttps() {
  const keyPath = path.resolve("../certs/server.key");
  const certPath = path.resolve("../certs/server.crt");

  if (fs.existsSync(keyPath) && fs.existsSync(certPath)) {
    return {
      key: fs.readFileSync(keyPath),
      cert: fs.readFileSync(certPath),
    };
  }

  return false; // fallback to HTTP in CI
}

export default defineConfig({
  plugins: [react()],
  server: {
    https: maybeHttps(),
    host: "localhost",
    port: 5173,
  },
});
