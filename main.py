import logic
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from transformers import BlipProcessor, BlipForConditionalGeneration

app = FastAPI()

# model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
# processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base", use_fast = True)

@app.post("/caption/")
async def generate_caption(request: Request):
    # image_bytes = await request.body()
    # caption = logic.generate_caption(image_bytes, model, processor)
    # return caption
    return "Placeholder reply."

app.mount("/", StaticFiles(directory = "ui", html = True), name = "ui")
