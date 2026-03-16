import { useEffect, useRef } from "react";
import { fabric } from "fabric";

function App() {
  const canvasRef = useRef(null);
  const fabricRef = useRef(null);

  const setupBrush = (canvas) => {
    canvas.isDrawingMode = true;
    canvas.freeDrawingBrush.width = 5;
    canvas.freeDrawingBrush.color = "black";
  };

  useEffect(() => {
    const canvas = new fabric.Canvas(canvasRef.current);

    canvas.setWidth(600);
    canvas.setHeight(400);

    setupBrush(canvas);
    fabricRef.current = canvas;

    
    return () => {
      canvas.dispose();
    };
  }, []);

  // Clear tool
  const clearCanvas = () => {
    const canvas = fabricRef.current;
    if (!canvas) return;

    canvas.clear();
   
  };

  // Change color tool
  const changeColor = (e) => {
    const canvas = fabricRef.current;
    if (!canvas) return;
    canvas.freeDrawingBrush.color = e.target.value;
  };

  // Change brush size tool
  const changeBrush = (e) => {
    const canvas = fabricRef.current;
    if (!canvas) return;
    canvas.freeDrawingBrush.width = Number(e.target.value);
  };

  // Submit function
  const submitDoodle = () => {
  const canvas = fabricRef.current;

  if (!canvas) return;

  const image = canvas.toDataURL({
    format: "png",
    quality: 1
  });

  console.log(image);
};

  return (
    <div
      style={{
        minHeight: "100vh",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        gap: "20px",
      }}
    >
      <h1>Doodle IT</h1>

      <div
        style={{
          display: "flex",
          gap: "30px",
          alignItems: "flex-start",
        }}
      >
        {/* CANVAS */}
        <canvas
          ref={canvasRef}
          style={{
            border: "2px solid black",
          }}
        />

        {/* TOOLS PANEL */}
        <div
          style={{
            border: "2px solid black",
            padding: "20px",
            display: "flex",
            flexDirection: "column",
            gap: "15px",
            minWidth: "150px",
          }}
        >
          <h3>Tools</h3>

          <button onClick={clearCanvas}>Clear</button>

          <input type="color" onChange={changeColor} />

          <input type="range" min="1" max="30" onChange={changeBrush} />

          <button onClick={submitDoodle}>
            Submit
          </button>
          
        </div>
      </div>
    </div>
  );
}

export default App;