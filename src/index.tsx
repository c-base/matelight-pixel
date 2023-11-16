import React from "react";
import { createRoot } from "react-dom/client";
import App from "./components/App";

const domNode = document.getElementById("root");
if (domNode != null) {
  const root = createRoot(domNode);
  root.render(<App />);
} else {
  console.error("Could not initialize App!");
}
