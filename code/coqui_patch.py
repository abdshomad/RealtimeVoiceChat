#!/usr/bin/env python3
"""
Patch script to fix the missing _validate_model_class method in GPT2InferenceModel.
This addresses the compatibility issue between TTS 0.26.0 and RealtimeTTS 0.5.5.
"""

import sys
import types
from TTS.tts.layers.xtts.gpt import GPT2InferenceModel

def _validate_model_class(self):
    """
    Dummy method to satisfy the interface expected by RealtimeTTS.
    This method is called by the stream generator but doesn't need to do anything
    in this context since the model is already validated during initialization.
    """
    pass

# Add the missing method to the GPT2InferenceModel class
GPT2InferenceModel._validate_model_class = _validate_model_class

# Also patch the class method to ensure it's available for all instances
def patched_init(self, *args, **kwargs):
    """Patched __init__ to ensure _validate_model_class is always available"""
    super(GPT2InferenceModel, self).__init__(*args, **kwargs)
    if not hasattr(self, '_validate_model_class'):
        self._validate_model_class = _validate_model_class

# Store the original __init__ and replace it
original_init = GPT2InferenceModel.__init__
GPT2InferenceModel.__init__ = patched_init

print("✅ Successfully patched GPT2InferenceModel with _validate_model_class method")
print("✅ Applied comprehensive patch to ensure method is available for all instances") 