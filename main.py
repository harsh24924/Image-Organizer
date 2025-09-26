import io
import requests
from PIL import Image
from fastapi import FastAPI
from logic import group_images, generate_captions
from schemas import Request, Response, Group, Image as ImageModel
from transformers import AutoImageProcessor, AutoModel, BlipProcessor, BlipForConditionalGeneration

app = FastAPI()

embedding_model = AutoModel.from_pretrained("facebook/dinov2-base")
embedding_processor = AutoImageProcessor.from_pretrained("facebook/dinov2-base", use_fast = True)

captioning_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
captioning_processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base", use_fast = True)

@app.post("/organize/", response_model = Response)
async def organize_images(request: Request):
    image_data = []

    for url in request.urls:
        response = requests.get(url)
        image = Image.open(io.BytesIO(response.content))
        image_data.append({"image": image, "url": url})

    grouped_images = group_images(image_data, embedding_model, embedding_processor)
    organized_images = generate_captions(grouped_images, captioning_model, captioning_processor)

    groups = []
    for cluster_id, images_in_cluster in organized_images.items():
        group_name = "Uncategorized" if cluster_id == -1 else f"Group {cluster_id}"
        group = Group(
            group_name = group_name,
            images = [ImageModel(**img_info) for img_info in images_in_cluster]
        )

        groups.append(group)
    
    return Response(groups = groups)
