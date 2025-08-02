# Installation Guide for RealtimeVoiceChat with Docker Compose

This guide provides step-by-step instructions for setting up and running the RealtimeVoiceChat application using Docker Compose.

## Prerequisites

### System Requirements
- **Operating System**: Linux (recommended for GPU support)
- **Docker**: Docker Engine and Docker Compose v2+
- **GPU**: NVIDIA GPU with CUDA support (highly recommended for performance)
- **NVIDIA Container Toolkit**: Required for GPU access in Docker containers

### Install NVIDIA Container Toolkit (Linux)
```bash
# Add NVIDIA package repositories
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list

# Install nvidia-docker2
sudo apt-get update
sudo apt-get install -y nvidia-docker2

# Restart Docker daemon
sudo systemctl restart docker
```

## Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/KoljaB/RealtimeVoiceChat.git
cd RealtimeVoiceChat
```

### 2. Configure Environment Variables
Copy the example environment file and configure it:
```bash
cp env.example .env
```

Edit the `.env` file to customize your settings:
```bash
# Application Configuration
PORT=9002                    # Change this to your preferred port
LOG_LEVEL=INFO
MAX_AUDIO_QUEUE_SIZE=50

# Ollama Configuration
OLLAMA_BASE_URL=http://ollama:11434

# GPU Configuration
NVIDIA_VISIBLE_DEVICES=all
NVIDIA_DRIVER_CAPABILITIES=compute,utility

# Cache Directories
HF_HOME=/home/appuser/.cache/huggingface
TORCH_HOME=/home/appuser/.cache/torch
```

### 3. Build Docker Images
```bash
sudo docker compose build
```

**Note**: This step takes time as it downloads base images, installs Python/ML dependencies, and pre-downloads the default STT model.

### 4. Start the Services
```bash
sudo docker compose up -d
```

This starts both the application and Ollama services in the background.

### 5. Pull the Required Ollama Model
```bash
# Pull the default model
sudo docker compose exec ollama ollama pull hf.co/bartowski/huihui-ai_Mistral-Small-24B-Instruct-2501-abliterated-GGUF:Q4_K_M

# Verify the model is available
sudo docker compose exec ollama ollama list
```

### 6. Access the Application
Open your web browser and navigate to:
```
http://localhost:9002
```

**Note**: Replace `9002` with the port you configured in your `.env` file.

**✅ Success Indicators:**
- The application should load a web interface with microphone controls
- You should see "Start", "Stop", and "Reset" buttons
- The application will take some time on first startup to download models and compile CUDA kernels
- Check the logs with `sudo docker compose logs -f app` to monitor startup progress
- TTS engine can be configured via `TTS_START_ENGINE` in `.env` file (options: kokoro, coqui, orpheus)

## Management Commands

### View Logs
```bash
# Follow app logs
sudo docker compose logs -f app

# Follow Ollama logs
sudo docker compose logs -f ollama

# View all logs
sudo docker compose logs -f
```

### Stop Services
```bash
sudo docker compose down
```

### Restart Services
```bash
sudo docker compose restart
```

### Rebuild and Start (for Dockerfile changes)
```bash
sudo docker compose up --build -d
```

### Live Development Commands
```bash
# Start services (no rebuild needed for code changes)
sudo docker compose up -d

# View logs in real-time
sudo docker compose logs -f

# Restart services (for environment variable changes)
sudo docker compose restart

# Rebuild only when Dockerfile changes
sudo docker compose up --build -d
```

## Configuration

### Environment Variables
The application uses the following key environment variables:

- `PORT`: The port on which the application runs (default: 9002)
- `LOG_LEVEL`: Logging level (INFO, DEBUG, etc.)
- `MAX_AUDIO_QUEUE_SIZE`: Maximum size of the audio processing queue
- `OLLAMA_BASE_URL`: URL for the Ollama service
- `NVIDIA_VISIBLE_DEVICES`: GPU device configuration
- `HF_HOME`: HuggingFace cache directory
- `TORCH_HOME`: PyTorch cache directory

### Volume Mounts
The Docker Compose setup includes several volumes for persistent data:

- `ollama_data`: Persists Ollama models and data
- `huggingface_cache`: Caches HuggingFace models
- `torch_cache`: Caches PyTorch models

### GPU Support
The setup is configured for NVIDIA GPU support. Ensure you have:
1. NVIDIA drivers installed
2. NVIDIA Container Toolkit installed
3. CUDA-compatible GPU

## Troubleshooting

### Port Conflicts
If you encounter port conflicts, change the `PORT` variable in your `.env` file and restart the services.

### GPU Issues
1. Verify NVIDIA Container Toolkit is installed:
   ```bash
   sudo docker run --rm --gpus all nvidia/cuda:12.1.1-base-ubuntu22.04 nvidia-smi
   ```

2. Check GPU visibility in containers:
   ```bash
   sudo docker compose exec app nvidia-smi
   ```

### Model Download Issues
If models fail to download, check your internet connection and try:
```bash
sudo docker compose restart ollama
```

### Memory Issues
For large models, ensure you have sufficient RAM and GPU memory. Consider using smaller models or increasing system resources.

### Log Analysis
Check logs for specific error messages:
```bash
sudo docker compose logs app | grep ERROR
sudo docker compose logs ollama | grep ERROR
```

## Development Setup

The Docker Compose setup is configured for live development by default. The following files are mounted for live development:

```yaml
volumes:
  - ./code:/app/code                    # Application code
  - ./entrypoint.sh:/app/entrypoint/entrypoint.sh  # Entrypoint script
```

This allows you to make code changes without rebuilding the Docker image. Changes to the code or entrypoint script are immediately reflected in the running container.

### Live Development Workflow
1. Make changes to files in the `./code/` directory
2. Changes are automatically reflected in the running container
3. No need to rebuild Docker image for code changes
4. Use `docker-compose restart` only for environment variable changes
5. Use `docker-compose up --build` only for Dockerfile changes

## Security Notes

- The application runs on HTTP by default
- For production, consider enabling SSL/HTTPS
- Keep your `.env` file secure and don't commit it to version control
- Regularly update Docker images and dependencies

## Support

For issues and contributions, please refer to the main project repository and documentation. 