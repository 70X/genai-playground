import torch
from diffusers import DiffusionPipeline
from huggingface_hub import login
from PIL import Image
import os

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def load_image_model() -> DiffusionPipeline:
    token = os.environ.get("HF_TOKEN")
    if not token:
        raise ValueError(
            "HF_TOKEN environment variable not set. Please provide a Hugging Face token."
        )
    login(token=token)
    model_id = os.environ.get("IMAGE_MODEL_ID", "black-forest-labs/FLUX.1-dev")
    pipe = DiffusionPipeline.from_pretrained(model_id, device=device)
    # model_id = os.environ.get("IMAGE_MODEL_ID", "black-forest-labs/FLUX.1-dev")
    # torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32
    # pipe = DiffusionPipeline.from_pretrained(
    #     model_id,
    #     torch_dtype=torch_dtype,
    # )
    # pipe = pipe.to(device)
    return pipe


def generate_image(
    pipe: DiffusionPipeline, prompt: str, num_inference_steps: int = 10
) -> Image.Image:
    # the more inference steps the better the final image is
    output = pipe(prompt, num_inference_steps=num_inference_steps).images[0]
    return output
