#!/usr/bin/env python3
"""
Example script showing how to use the Indonesian TTS engine.
This demonstrates how to use different speakers and synthesize Indonesian text.
"""

import os
import sys
from pathlib import Path

# Add the code directory to the path
sys.path.insert(0, str(Path(__file__).parent / "code"))

from audio_module import IndonesianTTSEngine, ensure_indonesian_tts_models

def example_indonesian_tts():
    """Example usage of Indonesian TTS with different speakers."""
    print("🇮🇩 Indonesian TTS Example")
    print("=" * 50)
    
    # Ensure models are downloaded
    print("📥 Ensuring Indonesian TTS models are available...")
    ensure_indonesian_tts_models(models_root="./models", model_name="indonesian-tts")
    
    # Example texts in Indonesian
    texts = [
        "Halo, selamat pagi! Bagaimana kabar Anda hari ini?",
        "Terima kasih telah menggunakan sistem text-to-speech Indonesia.",
        "Sistem ini mendukung berbagai suara seperti Ardi, Gadis, dan Wibowo."
    ]
    
    # Available speakers
    speakers = ["ardi", "gadis", "wibowo"]
    
    for i, text in enumerate(texts, 1):
        print(f"\n📝 Example {i}: {text}")
        
        for speaker in speakers:
            print(f"🎤 Using speaker: {speaker}")
            
            try:
                # Initialize engine with specific speaker
                engine = IndonesianTTSEngine(
                    model_path="./models/indonesian-tts",
                    speaker=speaker
                )
                
                # Synthesize audio
                audio_data = engine.synthesize(text)
                
                # Save audio file
                output_file = f"example_{i}_{speaker}.wav"
                with open(output_file, "wb") as f:
                    f.write(audio_data)
                
                print(f"✅ Audio saved: {output_file} ({len(audio_data)} bytes)")
                
            except Exception as e:
                print(f"❌ Error with speaker {speaker}: {e}")
    
    print("\n🎉 Example completed!")
    print("📁 Check the generated .wav files to hear the different speakers.")

if __name__ == "__main__":
    example_indonesian_tts() 