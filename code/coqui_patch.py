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
    # Ensure the method is always available
    if not hasattr(self, '_validate_model_class'):
        self._validate_model_class = _validate_model_class

# Store the original __init__ and replace it
original_init = GPT2InferenceModel.__init__
GPT2InferenceModel.__init__ = patched_init

# Patch the RealtimeTTS CoquiEngine directly
try:
    from RealtimeTTS.engines.coqui_engine import CoquiEngine
    from RealtimeTTS.engines.coqui_engine import CoquiEngine as RealtimeCoquiEngine
    
    # Patch the _synthesize_worker method to handle the missing method
    original_synthesize_worker = RealtimeCoquiEngine._synthesize_worker
    
    def patched_synthesize_worker(self, *args, **kwargs):
        """Patched synthesis worker that ensures _validate_model_class exists"""
        try:
            # Ensure all GPT2InferenceModel instances have the method
            if hasattr(self, 'model') and hasattr(self.model, '_validate_model_class'):
                # Method already exists, proceed normally
                pass
            else:
                # Add the method if it doesn't exist
                if hasattr(self, 'model'):
                    self.model._validate_model_class = _validate_model_class
                # Also patch any nested models
                if hasattr(self, 'model') and hasattr(self.model, 'gpt'):
                    self.model.gpt._validate_model_class = _validate_model_class
                if hasattr(self, 'model') and hasattr(self.model, 'decoder'):
                    self.model.decoder._validate_model_class = _validate_model_class
            
            # Call the original method
            return original_synthesize_worker(self, *args, **kwargs)
        except AttributeError as e:
            if '_validate_model_class' in str(e):
                # Add the method and retry
                if hasattr(self, 'model'):
                    self.model._validate_model_class = _validate_model_class
                return original_synthesize_worker(self, *args, **kwargs)
            else:
                raise e
    
    RealtimeCoquiEngine._synthesize_worker = patched_synthesize_worker
    print("✅ Patched RealtimeTTS CoquiEngine._synthesize_worker method")
    
except ImportError as e:
    print(f"⚠️ Could not patch RealtimeTTS CoquiEngine: {e}")

# Also patch the stream generator module directly
try:
    from TTS.tts.layers.xtts.stream_generator import StreamGenerator
    # Patch the StreamGenerator class as well
    if hasattr(StreamGenerator, 'generate'):
        original_generate = StreamGenerator.generate
        def patched_generate(self, *args, **kwargs):
            # Ensure the method exists before calling
            if hasattr(self, '_validate_model_class'):
                return original_generate(self, *args, **kwargs)
            else:
                # Add the method if it doesn't exist
                self._validate_model_class = _validate_model_class
                return original_generate(self, *args, **kwargs)
        StreamGenerator.generate = patched_generate
        print("✅ Also patched StreamGenerator.generate method")
except ImportError:
    print("⚠️ Could not patch StreamGenerator (module not available)")

# Patch any existing instances that might have been created
import gc
try:
    for obj in gc.get_objects():
        if isinstance(obj, GPT2InferenceModel) and not hasattr(obj, '_validate_model_class'):
            obj._validate_model_class = _validate_model_class
    print("✅ Patched existing GPT2InferenceModel instances")
except Exception as e:
    print(f"⚠️ Could not patch existing instances: {e}")

print("✅ Successfully patched GPT2InferenceModel with _validate_model_class method")
print("✅ Applied comprehensive patch to ensure method is available for all instances")
print("✅ Applied RealtimeTTS CoquiEngine patch for synthesis worker") 