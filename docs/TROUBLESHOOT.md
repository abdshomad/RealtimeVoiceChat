# Troubleshooting Guide for RealtimeVoiceChat Docker Compose

This guide covers common issues and their solutions for the RealtimeVoiceChat Docker Compose setup.

## Common Issues and Solutions

### 1. Port Already in Use

**Symptoms:**
```
Error response from daemon: driver failed programming external connectivity on endpoint: Bind for 0.0.0.0:9002 failed: port is already allocated
```

**Root Cause:** Another service is using the configured port.

**Resolution:**
1. Check what's using the port:
   ```bash
   sudo netstat -tulpn | grep :9002
   ```
2. Change the PORT in your `.env` file:
   ```bash
   PORT=9003  # or any other available port
   ```
3. Restart the services:
   ```bash
   sudo docker compose restart
   ```

### 2. GPU Not Available in Container

**Symptoms:**
```
RuntimeError: CUDA out of memory
```
or
```
nvidia-smi: command not found
```

**Root Cause:** NVIDIA Container Toolkit not properly installed or configured.

**Resolution:**
1. Verify NVIDIA Container Toolkit installation:
   ```bash
   sudo docker run --rm --gpus all nvidia/cuda:12.1.1-base-ubuntu22.04 nvidia-smi
   ```
2. If the above fails, reinstall NVIDIA Container Toolkit:
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
3. Restart the services:
   ```bash
   sudo docker compose down
   sudo docker compose up -d
   ```

### 3. Code Changes Not Reflected

**Symptoms:** Changes to files in `./code/` directory are not appearing in the running application.

**Root Cause:** Volume mount not working properly or container not restarted.

**Resolution:**
1. Verify volume mounts are active:
   ```bash
   sudo docker compose exec app ls -la /app/code
   ```
2. Check if the volume mount is working:
   ```bash
   sudo docker compose exec app cat /app/code/server.py
   ```
3. If volume mount is not working, restart the app service:
   ```bash
   sudo docker compose restart app
   ```
4. Verify the docker-compose.yml has the correct volume mounts:
   ```yaml
   volumes:
     - ./code:/app/code
     - ./entrypoint.sh:/app/entrypoint/entrypoint.sh
   ```

### 4. Entrypoint Script Not Found

**Symptoms:**
```
Error: No such file or directory: /app/entrypoint/entrypoint.sh
```

**Root Cause:** Entrypoint script not properly mounted or missing.

**Resolution:**
1. Verify entrypoint.sh exists in the project root:
   ```bash
   ls -la entrypoint.sh
   ```
2. Check if the file is mounted correctly:
   ```bash
   sudo docker compose exec app ls -la /app/entrypoint/
   ```
3. Ensure the file has execute permissions:
   ```bash
   chmod +x entrypoint.sh
   ```
4. Restart the app service:
   ```bash
   sudo docker compose restart app
   ```

### 5. Model Download Failures

**Symptoms:**
```
Error downloading Silero VAD: Connection timeout
```
or
```
Faster Whisper download failed
```

**Root Cause:** Network connectivity issues or insufficient disk space.

**Resolution:**
1. Check internet connectivity:
   ```bash
   sudo docker compose exec app ping -c 3 google.com
   ```
2. Check available disk space:
   ```bash
   df -h
   ```
3. Clear Docker cache if needed:
   ```bash
   sudo docker system prune -a
   ```
4. Retry the build:
   ```bash
   sudo docker compose up --build -d
   ```

### 6. Ollama Model Not Found

**Symptoms:**
```
Error: model not found
```

**Root Cause:** Required Ollama model not pulled.

**Resolution:**
1. Pull the required model:
   ```bash
   sudo docker compose exec ollama ollama pull hf.co/bartowski/huihui-ai_Mistral-Small-24B-Instruct-2501-abliterated-GGUF:Q4_K_M
   ```
2. Verify the model is available:
   ```bash
   sudo docker compose exec ollama ollama list
   ```
3. Restart the app service:
   ```bash
   sudo docker compose restart app
   ```

### 7. Memory Issues

**Symptoms:**
```
CUDA out of memory
```
or
```
Killed process (out of memory)
```

**Root Cause:** Insufficient GPU or system memory.

**Resolution:**
1. Check GPU memory usage:
   ```bash
   nvidia-smi
   ```
2. Check system memory:
   ```bash
   free -h
   ```
3. Reduce model size or increase system resources
4. Restart services to free memory:
   ```bash
   sudo docker compose down
   sudo docker compose up -d
   ```

### 8. Permission Issues

**Symptoms:**
```
Permission denied
```
or
```
Cannot create directory '/app/code': Permission denied
```

**Root Cause:** File permission issues with mounted volumes.

**Resolution:**
1. Check file permissions:
   ```bash
   ls -la code/
   ls -la entrypoint.sh
   ```
2. Fix permissions if needed:
   ```bash
   chmod -R 755 code/
   chmod 755 entrypoint.sh
   ```
3. Restart the services:
   ```bash
   sudo docker compose restart
   ```

### 9. Build Failures

**Symptoms:**
```
Step X/XX : RUN pip install -r requirements.txt FAILED
```

**Root Cause:** Network issues, dependency conflicts, or insufficient resources.

**Resolution:**
1. Check internet connectivity
2. Clear Docker cache:
   ```bash
   sudo docker system prune -a
   ```
3. Try building with more verbose output:
   ```bash
   sudo docker compose build --no-cache --progress=plain
   ```
4. Check if all required files exist:
   ```bash
   ls -la requirements.txt
   ls -la code/
   ```

### 10. Service Health Checks

**Symptoms:** Services not starting properly or becoming unresponsive.

**Resolution:**
1. Check service status:
   ```bash
   sudo docker compose ps
   ```
2. View logs for specific services:
   ```bash
   sudo docker compose logs app
   sudo docker compose logs ollama
   ```
3. Restart problematic services:
   ```bash
   sudo docker compose restart app
   sudo docker compose restart ollama
   ```

## Debugging Commands

### View Real-time Logs
```bash
# All services
sudo docker compose logs -f

# Specific service
sudo docker compose logs -f app
sudo docker compose logs -f ollama
```

### Check Container Status
```bash
# List all containers
sudo docker compose ps

# Check resource usage
sudo docker stats
```

### Access Container Shell
```bash
# App container
sudo docker compose exec app bash

# Ollama container
sudo docker compose exec ollama sh
```

### Verify Volume Mounts
```bash
# Check mounted volumes
sudo docker compose exec app ls -la /app/
sudo docker compose exec app ls -la /app/code/
```

## Performance Optimization

### GPU Memory Management
1. Monitor GPU usage:
   ```bash
   watch -n 1 nvidia-smi
   ```
2. Use smaller models if memory is limited
3. Adjust batch sizes in the application

### System Resources
1. Monitor system resources:
   ```bash
   htop
   ```
2. Ensure sufficient RAM and disk space
3. Consider using SSD storage for better I/O performance

## Getting Help

If you encounter issues not covered in this guide:

1. Check the application logs for specific error messages
2. Verify your system meets the minimum requirements
3. Ensure all prerequisites are properly installed
4. Try the troubleshooting steps in order
5. Check the main project repository for additional documentation

## Version Compatibility

This troubleshooting guide is compatible with:
- Docker Compose v2+
- NVIDIA Container Toolkit
- Ubuntu 22.04+ (recommended)
- CUDA 12.1+ 