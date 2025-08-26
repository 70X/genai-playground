# GenAI Playground

A **hands-on generative AI playground** for experimenting with **text, image, 3D models, audio, and video**. Built with **Python, FastAPI, and Streamlit**, it's designed for rapid experimentation and learning.

---

## 🚀 Features

- **Text → Text**: Transform prompts into AI-generated text.
- **Text → Audio**: Generate speech or audio from text.
- **Text → Image**: Create stunning images from descriptions.
- **Text → 3D Models**: Convert prompts into 3D meshes.
- **Image → Video**: Turn images into short, AI-generated videos.

---

## 🏗️ Project Structure

```sh
api/
├── audio/ # Audio generation logic
├── image/ # Image generation logic
├── mesh3d/ # 3D model generation logic
├── text/ # Text generation logic
├── video/ # Video generation logic
├── main.py # FastAPI entrypoint
client/
├── pages
│   │   ├── 1_🧐 Text → Text.py
│   │   ├── 2_🔉 Text → Audio.py
│   │   ├── 3_🖼️ Text → Image.py
│   │   ├── 4_👾 Text → 3D.py
│   │   └── 5_🎥 Image → Video.py
├── 🏠_Home.py # Streamlit main dashboard
Makefile # Build and run commands
setup.sh # Setup virtual environment and dependencies
requirements.txt
README.md
```

## ⚡ Getting Started

### Prerequisites

- Python 3.11+

### Installation

```sh
make build
```

### Run

Start API only:

```sh
make api
```

Start Client only:

```sh
make client
```

Run both API and Client (dev mode):

```sh
make dev
```

The dev command opens two Terminal windows automatically: one for the API and one for the Streamlit client.

## 🧩 How It Works

API: Handles generation logic for different media types using modular Python packages (audio, image, mesh3d, text, video).

Client: Streamlit dashboard for interactive experimentation.

Makefile: Simplifies environment setup, running API/client, and development workflow.
