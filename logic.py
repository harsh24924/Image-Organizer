import torch
from sklearn.cluster import DBSCAN
from collections import defaultdict

def group_images(image_data, model, processor):
    images = [item["image"] for item in image_data]

    model.eval()
    inputs = processor(images = images, return_tensors = "pt")
    with torch.no_grad():
        outputs = model(**inputs)

    last_hidden_states = outputs.last_hidden_state
    image_vectors = last_hidden_states[:, 0, :]

    dbscan = DBSCAN(eps = 0.90, min_samples = 2, metric = "cosine")
    clusters = dbscan.fit_predict(image_vectors)

    grouped_images = defaultdict(list)
    for item_data, cluster_id in zip(image_data, clusters):
        grouped_images[int(cluster_id)].append(item_data)

    return dict(grouped_images)

def generate_captions(grouped_images, model, processor):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(device)
    model.eval()

    organized_images = defaultdict(list)

    with torch.no_grad():
        for cluster_id, items_in_cluster in grouped_images.items():

            for item in items_in_cluster:
                image = item["image"]
                url = item["url"]

                inputs = processor(image, return_tensors = "pt").to(device)
                outputs = model.generate(**inputs)
                caption = processor.decode(outputs[0], skip_special_tokens = True)

                organized_images[cluster_id].append({
                    "url": url,       
                    "caption": caption
                })

    return dict(organized_images)
