import os
import requests
from io import BytesIO
from PIL import Image, ImageOps
from sklearn.preprocessing import normalize
from transformers import CLIPProcessor, CLIPModel
import torch

from pyserini.encode import DocumentEncoder, QueryEncoder

os.environ['OPENBLAS_NUM_THREADS'] = '1'




def load_pil_image(image, format='RGB'):
    if isinstance(image, str) or os.path.isfile(image):
        if image.startswith(("http://", "https://")):  # Image is a URL
            response = requests.get(str(image))
            response.raise_for_status()
            with Image.open(BytesIO(response.content)) as img:
                image = img.copy()
        else:  # Image is a file path
            with Image.open(image) as img:
                image = img.copy()
    elif not isinstance(image, Image.Image):
        raise ValueError("Image must be a PIL Image object, a file path, or a URL.")
    
    # Ensure the image is correctly oriented according to its EXIF data and convert format
    image = ImageOps.exif_transpose(image).convert(format)

    return image


class BaseClipEncoder:
    """Base class for encoding using a CLIP model."""
    def __init__(self, model_name, device='cuda:0', l2_norm=True):
        self.device = device
        self.model = CLIPModel.from_pretrained(model_name).to(device)
        self.processor = CLIPProcessor.from_pretrained(model_name)
        self.l2_norm = l2_norm

    def normalize_embeddings(self, embeddings):
        """Apply L2 normalization to embeddings if required."""
        return normalize(embeddings, axis=1, norm='l2') if self.l2_norm else embeddings


class ClipImageEncoder(BaseClipEncoder):
    """Encodes images using a CLIP model."""
    def encode(self, paths, **kwargs):
        processed_images = []

        if isinstance(paths, str):
            paths = [paths]
            
        for image in paths:
            try:
                img = load_pil_image(image)
                processed_images.append(img)
            except Exception as e:
                print(f"Error loading image {image}: {e}")

        inputs = self.processor(images=processed_images, return_tensors="pt").to(self.device)

        with torch.no_grad():
            image_features = self.model.get_image_features(**inputs)

        embeddings = image_features.detach().cpu().numpy()
        return self.normalize_embeddings(embeddings)


class ClipTextEncoder(BaseClipEncoder):
    """Encodes text using a CLIP model."""
    def __init__(self, model_name, device='cuda:0', l2_norm=False, prefix=None):
        super().__init__(model_name, device, l2_norm)
        self.prefix = prefix

    def encode(self, texts, max_length=77, **kwargs):

        if isinstance(texts, str):
            texts = [texts]
            
        if self.prefix:
            texts = [f"{self.prefix} {text}" for text in texts]

        inputs = self.processor(
            text=texts, 
            return_tensors="pt",
            padding='max_length',
            max_length=max_length,
            truncation='longest_first',
        ).to(self.device)

        with torch.no_grad():
            text_features = self.model.get_text_features(**inputs)

        embeddings = text_features.detach().cpu().numpy()
        return self.normalize_embeddings(embeddings)
    
    
class ClipDocumentEncoder(DocumentEncoder):
    """Encodes documents using a CLIP model, supporting both images and texts."""
    def __init__(self, model_name, device='cuda:0', l2_norm=False, prefix=None, multimodal=False):
        super().__init__()
        self.encoder = ClipImageEncoder(model_name, device, l2_norm) if multimodal else ClipTextEncoder(model_name, device, l2_norm, prefix)

    def encode(self, *args, **kwargs):
        return self.encoder.encode(*args, **kwargs)


class ClipEncoder(QueryEncoder):
    """Encodes queries using a CLIP model, supporting both images and texts."""
    def __init__(self, model_name, device='cuda:0', l2_norm=False, prefix=None, multimodal=False):
        super().__init__()
        self.encoder = ClipImageEncoder(model_name, device, l2_norm) if multimodal else ClipTextEncoder(model_name, device, l2_norm, prefix)

    def encode(self, *args, **kwargs):
        return self.encoder.encode(*args, **kwargs)
