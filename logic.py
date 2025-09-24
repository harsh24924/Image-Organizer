import io
from PIL import Image

def generate_caption(image_bytes, model, processor):
    raw_image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    inputs = processor(raw_image, return_tensors = "pt")
    output = model.generate(**inputs)
    caption = processor.decode(output[0], skip_special_tokens = True)
    return caption
