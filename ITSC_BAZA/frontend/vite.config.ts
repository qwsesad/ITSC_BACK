
// https://vitejs.dev/config/

import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// https://vitejs.dev/config/
export default defineConfig({
  build: { manifest: true },
  base: '/itc-presentation-build/',
  plugins: [reactS()],
});