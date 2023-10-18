from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from rembg import remove
from PIL import Image
import io

app = FastAPI()

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://groun.onrender.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/remove_background/")
async def remove_background(file: UploadFile):
    # Check if a file was provided
    if not file:
        return {"error": "No file provided."}

    # Read the image file
    image_bytes = await file.read()

    # Perform background removal
    image = Image.open(io.BytesIO(image_bytes))
    output_image = remove(image)

    # Save the output image to a BytesIO object
    output_buffer = io.BytesIO()
    output_image.save(output_buffer, format="PNG")
    output_bytes = output_buffer.getvalue()

    # Return the resulting image
    return {"result_image": output_bytes}
