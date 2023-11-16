import { useState } from "react";
import "../../static/css/styles.css";

interface Pixel {
  r: Number;
  g: Number;
  b: Number;
}

function sendPixel(x: Number, y: Number, pixel: Pixel) {
  fetch(`/pixel/${x}/${y}/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(pixel),
  });
}

function hexToRgb(hex: string): Pixel {
  var result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
  return result
    ? {
        r: parseInt(result[1], 16),
        g: parseInt(result[2], 16),
        b: parseInt(result[3], 16),
      }
    : { r: 0, g: 0, b: 0 };
}

export default function App() {
  const [color, setColor] = useState<Pixel>({ r: 0, g: 0, b: 0 });

  return (
    <>
      <h1>Mate-Light Pixel Wall</h1>
      <div className="colorPicker">
        <span>Select color:</span>
        <input
          id="colorPicker"
          type="color"
          onChange={(e) => setColor(hexToRgb(e.target.value))}
        />
      </div>
      <div id="pixelTileContainer">
        {Array.from({ length: 16 }, (value, index) => index).map((y) =>
          Array.from({ length: 40 }, (value, index) => index).map((x) => (
            <div
              key={x + "," + y}
              onClick={() => sendPixel(x, y, color)}
              className="pixelTile"
            ></div>
          ))
        )}
      </div>
    </>
  );
}
