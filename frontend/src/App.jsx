import { useEffect, useRef, useState } from "react";
import { fabric } from "fabric";



function App() {

  const [loading, setLoading] = useState(false);

  const [result, setResult] = useState(null);
  const [style,setStyle] = useState("realistic");
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
    canvas.backgroundColor = "white";
   
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
  const submitDoodle = async  () => {
  const canvas = fabricRef.current;

  if (!canvas) return;

  setLoading(true);

  const image = canvas.toDataURL({
    format: "png",
    quality: 1
  });

  const res = await fetch("http://127.0.0.1:8000/generate", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ 
      image, 
      style 
    })
  });

  const data = await res.json();

  setResult(data.preview);
  setLoading(false);
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

          <h4>Select Style</h4>
          <select
            value={style}
            onChange={(e) => setStyle(e.target.value)}
          >
            <option value="realistic">Realistic</option>
            <option value="cartoon">Cartoon</option>
            <option value="anime">Anime</option>
            <option value="3d">3D</option>
          </select>

          <button onClick={submitDoodle}>
            Submit
          </button>

          

        </div>        
      </div>
        {loading && <h2>Loading...</h2>}
      {/*RESULT */}
          {result && (
            <div style={{ marginTop: 30 }}>
              <h2>Result</h2>

              <img
                src={result}
                style={{
                  width: 400,
                  border: "2px solid black"
                }}
              />
            </div>
          )}
    </div>
  );
}

export default App;