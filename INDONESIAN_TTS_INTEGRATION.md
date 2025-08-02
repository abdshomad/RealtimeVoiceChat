# Indonesian TTS Integration

This document describes the integration of Indonesian Text-to-Speech (TTS) functionality into the RealtimeVoiceChat application using the [Wikidepia Indonesian TTS](https://github.com/Wikidepia/indonesian-tts) model.

## Overview

The Indonesian TTS integration provides native Indonesian language support for text-to-speech synthesis, featuring multiple speakers and high-quality audio output. This integration is based on the Wikidepia Indonesian TTS model, which is trained specifically for Indonesian language synthesis.

## Features

- **Multiple Speakers**: Support for three different speakers (Ardi, Gadis, Wibowo)
- **Grapheme-to-Phoneme Conversion**: Uses `g2p-id` for accurate Indonesian pronunciation
- **High-Quality Audio**: 22kHz sample rate, 16-bit audio output
- **Easy Integration**: Seamless integration with existing TTS engine architecture
- **Automatic Model Download**: Models are automatically downloaded on first use

## Architecture

### Core Components

1. **IndonesianTTSEngine**: Main engine class that handles TTS synthesis
2. **IndonesianTTSEngineStream**: Streaming adapter for RealtimeTTS compatibility
3. **ensure_indonesian_tts_models()**: Helper function for model management

### Integration Points

- **AudioProcessor**: Modified to support Indonesian TTS engine
- **SpeechPipelineManager**: Updated to handle Indonesian TTS synthesis
- **Server Configuration**: Environment variable support for engine selection

## Usage

### Environment Configuration

Set the TTS engine in your environment:

```bash
# In .env file or environment variable
TTS_START_ENGINE=indonesian
```

### Available Speakers

- **Ardi**: Male speaker voice
- **Gadis**: Female speaker voice  
- **Wibowo**: Male speaker voice (default)

### Code Example

```python
from audio_module import IndonesianTTSEngine

# Initialize with specific speaker
engine = IndonesianTTSEngine(
    model_path="/app/code/models/indonesian-tts",
    speaker="wibowo"  # or "ardi", "gadis"
)

# Synthesize Indonesian text
audio_data = engine.synthesize("Halo, selamat pagi!")
```

## Model Information

### Source
- **Repository**: [Wikidepia/indonesian-tts](https://github.com/Wikidepia/indonesian-tts)
- **Model Version**: v1.2 (latest)
- **License**: Non-commercial use only

### Model Files
- `checkpoint.pth`: Trained model weights
- `config.json`: Model configuration

### Training Data
The model was trained on:
- 4 hours of Audiobook dataset
- 2000 samples of Azure TTS
- High-quality TTS data for Javanese & Sundanese

## Dependencies

### Required Packages
- `TTS`: Coqui TTS framework
- `g2p-id`: Indonesian grapheme-to-phoneme conversion

### Installation
```bash
pip install TTS g2p-id
```

## Testing

### Test Script
Run the test script to verify the integration:

```bash
python test_indonesian_tts.py
```

### Example Script
Run the example script to see different speakers:

```bash
python indonesian_tts_example.py
```

## Configuration

### Audio Settings
- **Sample Rate**: 22050 Hz
- **Channels**: Mono (1 channel)
- **Bit Depth**: 16-bit
- **Format**: WAV

### Performance Notes
- **GPU Support**: Set `gpu=True` in TTS initialization for GPU acceleration
- **Memory Usage**: Model requires approximately 500MB RAM
- **Initialization Time**: ~10-30 seconds on first load

## Troubleshooting

### Common Issues

1. **Model Download Failures**
   - Check internet connection
   - Verify Hugging Face Hub access
   - Check available disk space

2. **Audio Quality Issues**
   - Ensure proper text input (Indonesian language)
   - Check speaker selection
   - Verify audio output format

3. **Performance Issues**
   - Enable GPU acceleration if available
   - Check system memory usage
   - Consider using smaller audio chunks

### Debug Information

Enable debug logging to see detailed information:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Limitations

- **Non-Commercial Use**: The model is licensed for non-commercial use only
- **Indonesian Language**: Optimized for Indonesian language only
- **Speaker Limitations**: Limited to three predefined speakers
- **No Streaming**: Current implementation processes text in chunks rather than true streaming

## Future Enhancements

Potential improvements for future versions:
- Real-time streaming synthesis
- Additional speaker voices
- Custom voice training support
- Commercial licensing options
- Multi-language support

## License and Attribution

This integration uses the Indonesian TTS model from the [Wikidepia repository](https://github.com/Wikidepia/indonesian-tts), which is licensed for non-commercial use. Please respect the original model's licensing terms.

## Support

For issues related to the Indonesian TTS integration:
1. Check the troubleshooting section above
2. Review the test and example scripts
3. Verify environment configuration
4. Check system requirements and dependencies 