import { useEffect, useRef } from "react";
import { fabric } from "fabric";

function App() {

  const canvasRef = useRef(null);

  useEffect(() => {

    const canvas = new fabric.Canvas(canvasRef.current);

    canvas.isDrawingMode = true;
    canvas.freeDrawingBrush.width = 5;
    canvas.freeDrawingBrush.color = "black";

  }, []);

  return (
    <div style={{ padding: 40 }}>
      <h1>Doodle AI</h1>

      <canvas
        ref={canvasRef}
        width={600}
        height={400}
        style={{ border: "2px solid black" }}
      />

    </div>
  );
}

export default App;