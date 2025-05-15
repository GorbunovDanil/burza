// frontend/src/lib/api.ts

import axios from "axios";

export const api = axios.create({
  baseURL: "https://localhost:8000/api/",
  // mkcert root CA is trusted in your browser, so no httpsAgent needed
});
