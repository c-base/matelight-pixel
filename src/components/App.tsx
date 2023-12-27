import { useState } from "react";
import "../../static/css/styles.css";
import headerImage from "../../static/img/header.png";
import headerImageSM from "../../static/img/header-sm.png";
import "../../static/fonts/Mona Sans/Mona-Sans.woff2";

const DEFAULT_COLOR = "#00FF00";

interface Pixel {
  r: Number;
  g: Number;
  b: Number;
}
interface Coordinates {
  x: Number;
  y: Number;
}

function sendPixel(coordinates: Coordinates, pixel: Pixel) {
  fetch(`/pixel/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ coordinates, pixel }),
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

function RgbToHex(rgb: Pixel): string {
  return (
    "#" +
    rgb.r.toString(16).padStart(2, "0") +
    rgb.g.toString(16).padStart(2, "0") +
    rgb.b.toString(16).padStart(2, "0")
  );
}

export default function App() {
  const [color, setColor] = useState<string>(DEFAULT_COLOR);
  const [frameBuffer, setFrameBuffer] = useState(
    Array.from({ length: 16 }, (value, index) => index).map((y) =>
      Array.from({ length: 40 }, (value, index) => index).map((x) => ({
        r: 0,
        g: 0,
        b: 0,
      }))
    )
  );
  setTimeout(() => {
    fetch("/framebuffer/")
      .then((buffer) => buffer.json())
      // .then((buffer) => { console.log(buffer); return buffer; })
      .then((buffer) => setFrameBuffer(buffer));
  }, 1000);

  return (
    <>
      <h1>Mate-Light Pixel Wall</h1>
      <img id={"header"} src={headerImage} />
      <img id={"header-sm"} src={headerImageSM} />
      <div className="colorPicker">
        <span>Select color:</span>
        <input
          id="colorPicker"
          type="color"
          onChange={(e) => setColor(e.target.value)}
          value={color}
        />
      {/**  <input
          type="button"
          value={"session"}
          onClick={() => fetch("/getToken/")}
        /> **/}
      </div>
      <div id="pixelTileContainerWrapper">
        <div id="pixelTileContainer">
          {Array.from({ length: 16 }, (value, index) => index).map((y) =>
            Array.from({ length: 40 }, (value, index) => index).map((x) => (
              <div
                key={x + "," + y}
                onClick={() => sendPixel({ x, y }, hexToRgb(color))}
                className="pixelTile"
                style={{ backgroundColor: RgbToHex(frameBuffer[y][x]) }}
              ></div>
            ))
          )}
        </div>
      </div>
    </>
  );
}
