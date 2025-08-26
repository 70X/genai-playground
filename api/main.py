from typing import AsyncIterator
from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from text.models import generate_text, load_text_model
from fastapi import status
from audio.schemas import VoicePresets
from fastapi.responses import StreamingResponse
from audio.models import generate_audio, load_audio_model
from audio.utils import audio_array_to_buffer
from fastapi import Response
from image.models import generate_image, load_image_model
from image.utils import img_to_bytes
from fastapi import File
from io import BytesIO
from PIL import Image
from video.models import generate_video, load_video_model
from video.utils import export_to_video_buffer
from mesh3d.models import generate_3d_geometry, load_3d_model
from mesh3d.utils import mesh_to_obj_buffer
import csv
import time
from datetime import datetime, timezone
from uuid import uuid4
from typing import Awaitable, Callable
from fastapi import Request

app = FastAPI()
models = {}


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    models["text2text"] = load_text_model()
    models["text2image"] = load_image_model()
    models["text2audio"] = load_audio_model()
    models["image2video"] = load_video_model()
    models["text2threed"] = load_3d_model()

    yield

    models.clear()


app = FastAPI(lifespan=lifespan)

csv_header = [
    "Request ID",
    "Datetime",
    "Endpoint Triggered",
    "Client IP Address",
    "Response Time",
    "Status Code",
    "Successful",
]


@app.middleware("http")
async def monitor_service(
    req: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    request_id = uuid4().hex
    request_datetime = datetime.now(timezone.utc).isoformat()
    start_time = time.perf_counter()
    response: Response = await call_next(req)
    response_time = round(time.perf_counter() - start_time, 4)
    response.headers["X-Response-Time"] = str(response_time)
    response.headers["X-API-Request-ID"] = request_id
    with open("usage.csv", "a", newline="") as file:
        writer = csv.writer(file)
        if file.tell() == 0:
            writer.writerow(csv_header)
        writer.writerow(
            [
                request_id,
                request_datetime,
                req.url,
                req.client.host,
                response_time,
                response.status_code,
                response.status_code < 400,
            ]
        )
    return response


@app.get("/generate/text")
def serve_language_model_controller(prompt: str) -> str:
    output = generate_text(models["text2text"], prompt)
    return output


@app.get(
    "/generate/audio",
    responses={status.HTTP_200_OK: {"content": {"audio/wav": {}}}},
    response_class=StreamingResponse,
)
def serve_text_to_audio_model_controller(
    prompt: str,
    preset: VoicePresets = "v2/en_speaker_9",
):
    processor, model = models["text2audio"]
    output, sample_rate = generate_audio(processor, model, prompt, preset)
    return StreamingResponse(
        audio_array_to_buffer(output, sample_rate), media_type="audio/wav"
    )


@app.get(
    "/generate/image",
    responses={status.HTTP_200_OK: {"content": {"image/png": {}}}},
    response_class=Response,
)
def serve_text_to_image_model_controller(prompt: str):
    output = generate_image(models["text2image"], prompt)
    return Response(content=img_to_bytes(output), media_type="image/png")


@app.post(
    "/generate/video",
    responses={status.HTTP_200_OK: {"content": {"video/mp4": {}}}},
    response_class=StreamingResponse,
)
def serve_image_to_video_model_controller(
    image: bytes = File(...), num_frames: int = 25
):
    image = Image.open(BytesIO(image))
    frames = generate_video(models["image2video"], image, num_frames)
    return StreamingResponse(export_to_video_buffer(frames), media_type="video/mp4")


@app.get(
    "/generate/3d",
    responses={status.HTTP_200_OK: {"content": {"model/obj": {}}}},
    response_class=StreamingResponse,
)
def serve_text_to_3d_model_controller(prompt: str, num_inference_steps: int = 25):
    mesh = generate_3d_geometry(models["text2threed"], prompt, num_inference_steps)
    response = StreamingResponse(mesh_to_obj_buffer(mesh), media_type="model/obj")
    response.headers["Content-Disposition"] = f"attachment; filename={prompt}.obj"
    return response
