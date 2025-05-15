const { defineConfig } = require("vite");
const react = require("@vitejs/plugin-react");
const fs = require("fs");
const path = require("path");

function maybeHttps() {
  const keyPath = path.resolve(__dirname, "../certs/server.key");
  const certPath = path.resolve(__dirname, "../certs/server.crt");

  if (fs.existsSync(keyPath) && fs.existsSync(certPath)) {
    return {
      key: fs.readFileSync(keyPath),
      cert: fs.readFileSync(certPath),
    };
  }

  return false; // fallback to HTTP
}

module.exports = defineConfig({
  plugins: [react()],
  server: {
    https: maybeHttps(),
    host: "localhost",
    port: 5173,
  },
});
