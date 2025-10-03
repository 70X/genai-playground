import torch
from diffusers import DiffusionPipeline
from huggingface_hub import login
from PIL import Image
import os

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def load_image_model() -> DiffusionPipeline:
    login(token=os.environ.get("HF_TOKEN"))
    pipe = DiffusionPipeline.from_pretrained(
        "black-forest-labs/FLUX.1-dev",
        device=device,
    )
    return pipe


def generate_image(pipe: DiffusionPipeline, prompt: str) -> Image.Image:
    # the more inference steps the better the final image is. For testing purpose we reduce it to 10 here
    output = pipe(prompt, num_inference_steps=10).images[0]
    return output
