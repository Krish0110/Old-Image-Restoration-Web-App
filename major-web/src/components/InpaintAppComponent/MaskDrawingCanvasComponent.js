import React, { useRef, useEffect, useState } from "react";
import { postImageApi } from '../../pages/InpaintApp/InpaintAppApi';
import Button from "../Button/Button";

const DrawingCanvas = ({ imageUrl, width, height, onClose, onInpainted }) => {
  const drawCanvasRef = useRef(null); // Transparent overlay canvas
  const maskCanvasRef = useRef(null); // Binary mask canvas
  const [drawing, setDrawing] = useState(false);
  const brushSize = 5;

  // Scale factor for display size
  const displayScale = 0.5;
  const displayWidth = width * displayScale;
  const displayHeight = height * displayScale;


  useEffect(() => {
    if (!width || !height) return;

    // Initialize mask canvas
    const maskCanvas = maskCanvasRef.current;
    const maskCtx = maskCanvas.getContext("2d");
    maskCanvas.width = width;
    maskCanvas.height = height;
    maskCtx.fillStyle = "black";
    maskCtx.fillRect(0, 0, width, height);

    // Also make sure drawCanvas matches dimensions
    const drawCanvas = drawCanvasRef.current;
    drawCanvas.width = width;
    drawCanvas.height = height;
  }, [width, height]);

  const getCoords = (e, canvas) => {
    const rect = canvas.getBoundingClientRect();
    const scaleX = canvas.width / rect.width;
    const scaleY = canvas.height / rect.height;
    return {
      x: (e.clientX - rect.left) * scaleX,
      y: (e.clientY - rect.top) * scaleY,
    };
  };

  const startDrawing = (e) => {
    setDrawing(true);
    draw(e); // Draw a dot immediately on mouse down
  };

  const endDrawing = () => {
    setDrawing(false);
  };

  const draw = (e) => {
    if (!drawing) return;

    const drawCanvas = drawCanvasRef.current;
    const maskCanvas = maskCanvasRef.current;

    const { x, y } = getCoords(e, drawCanvas);

    // Draw on visible canvas
    const drawCtx = drawCanvas.getContext("2d");
    drawCtx.fillStyle = "rgba(255,255,255,0.6)";
    drawCtx.beginPath();
    drawCtx.arc(x, y, brushSize, 0, 2 * Math.PI);
    drawCtx.fill();

    // Draw on binary mask canvas
    const maskCtx = maskCanvas.getContext("2d");
    maskCtx.fillStyle = "white";
    maskCtx.beginPath();
    maskCtx.arc(x, y, brushSize, 0, 2 * Math.PI);
    maskCtx.fill();
  };

  const handleInpaintImageButton = async () => {
    try {
      // Convert mask canvas to blob
      const maskCanvas = maskCanvasRef.current;
      const maskDataUrl = maskCanvas.toDataURL("image/png");
      const maskBlob = await (await fetch(maskDataUrl)).blob();
  
      // Convert input image to blob
      const inputBlob = await (await fetch(imageUrl)).blob();
  
      // Create form data
      const formData = new FormData();
      formData.append("input_image", inputBlob, "input_image.png");
      formData.append("mask_image", maskBlob, "mask.png");
  
      // Send to backend
      const response = await postImageApi("/api/inpaint-image/", formData);
      console.log("Inpainting response:", response);
  
      // Convert response to Data URL
      const inpaintedImageDataUrl = `data:image/png;base64,${response.inpainted_image}`;

      onInpainted(inpaintedImageDataUrl);
    } catch (error) {
      console.error("Inpainting failed:", error.message);
    }
  };
  
  if (!imageUrl) return <p>No image to draw on.</p>;

  return (
    <>
      <div style={{ display: "flex", gap: "40px", alignItems: "flex-start", justifyContent: "center" }}>
        {/* Left: Image + Drawing Overlay */}
        <div style={{ position: "relative", width: displayWidth, height: displayHeight }}>
          <img
            src={imageUrl}
            alt="To draw on"
            style={{
              width: displayWidth,
              height: displayHeight,
              position: "absolute", 
              zIndex: 1,
            }}
          />
          <canvas
            ref={drawCanvasRef}
            style={{
              width: displayWidth,
              height: displayHeight,
              position: "absolute",
              zIndex: 2,
              cursor: "crosshair",
            }}
            onMouseDown={startDrawing}
            onMouseUp={endDrawing}
            onMouseMove={draw}
            onMouseLeave={endDrawing}
          />
        </div>

        {/* Right: Binary Mask */}
        <div>
          <canvas
            ref={maskCanvasRef}
            width={width}
            height={height}
            style={{
              width: displayWidth,
              height: displayHeight,
              border: "2px solid black",
              background: "black",
              marginBottom: "30px",
              marginLeft: "80px",
            }}
          />
        </div>
      </div>
          <div style={{display: "flex", justifyContent: "center", gap: "40px" }}>
          <Button title={"Inpaint image"} onClick={handleInpaintImageButton} />
          <Button title={"Cancel"} onClick={onClose}/>
      </div>
    </>
  );
};

export default DrawingCanvas;
