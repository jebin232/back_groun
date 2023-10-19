from fastapi import FastAPI, File, UploadFile
from rembg import remove
from PIL import Image
import io

app = FastAPI()

@app.post("/remove_background/")
async def remove_background(image: UploadFile):
    # Check if the uploaded file is an image
    if not image.content_type.startswith("image/"):
        return {"error": "Invalid file type. Please upload an image."}

    # Read the image file
    image_bytes = await image.read()
    image_data = Image.open(io.BytesIO(image_bytes))

    # Remove the background
    output_image = remove(image_data)

    # Save the processed image to a temporary file
    output_buffer = io.BytesIO()
    output_image.save(output_buffer, format="PNG")
    output_buffer.seek(0)

    return {
        "message": "Background removed successfully.",
        "processed_image": output_buffer,
    }
