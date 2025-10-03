import torch
from diffusers import DiffusionPipeline, StableDiffusionInpaintPipelineLegacy
from huggingface_hub import login
from PIL import Image
import os

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

login(token=os.environ.get("HF_TOKEN"))


def load_image_model() -> StableDiffusionInpaintPipelineLegacy:
    pipe = DiffusionPipeline.from_pretrained(
        "black-forest-labs/FLUX.1-dev",
        device=device,
    )
    return pipe


def generate_image(
    pipe: StableDiffusionInpaintPipelineLegacy, prompt: str
) -> Image.Image:
    # output = pipe(prompt, num_inference_steps=10).images[0]
    output = pipe(prompt).images[0]
    return output


# from diffusers import DiffusionPipeline

# pipe = DiffusionPipeline.from_pretrained("black-forest-labs/FLUX.1-dev")

# prompt = "Astronaut in a jungle, cold color palette, muted colors, detailed, 8k"
# image = pipe(prompt).images[0]
