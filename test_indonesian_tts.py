#!/usr/bin/env python3
"""
Test script for Indonesian TTS integration.
This script tests the Indonesian TTS engine functionality.
"""

import os
import sys
import logging
from pathlib import Path

# Add the code directory to the path
sys.path.insert(0, str(Path(__file__).parent / "code"))

from audio_module import IndonesianTTSEngine, ensure_indonesian_tts_models

def test_indonesian_tts():
    """Test the Indonesian TTS engine."""
    print("🧪 Testing Indonesian TTS integration...")
    
    try:
        # Ensure models are downloaded
        print("📥 Downloading Indonesian TTS models...")
        ensure_indonesian_tts_models(models_root="./models", model_name="indonesian-tts")
        
        # Initialize the engine
        print("🔧 Initializing Indonesian TTS engine...")
        engine = IndonesianTTSEngine(
            model_path="./models/indonesian-tts",
            speaker="wibowo"
        )
        
        # Test text
        test_text = "Halo, ini adalah tes untuk mesin text-to-speech Indonesia."
        print(f"📝 Testing with text: {test_text}")
        
        # Synthesize audio
        print("🎵 Synthesizing audio...")
        audio_data = engine.synthesize(test_text)
        
        # Save test audio
        output_file = "test_indonesian_tts.wav"
        with open(output_file, "wb") as f:
            f.write(audio_data)
        
        print(f"✅ Test completed successfully! Audio saved to: {output_file}")
        print(f"📊 Audio data size: {len(audio_data)} bytes")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_indonesian_tts()
    sys.exit(0 if success else 1) 