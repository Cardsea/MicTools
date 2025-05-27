import numpy as np
import sounddevice as sd
from PIL import Image

SAMPLE_RATE = 44100  # Hz
DURATION = 2  # seconds

print("🎙️ Recording raw audio...")

# Record audio
audio = sd.rec(int(SAMPLE_RATE * DURATION), samplerate=SAMPLE_RATE, channels=1, dtype='float32')
sd.wait()

print("✅ Audio recorded, creating amplitude visualization...")

# Get absolute amplitudes and amplify them significantly
audio_flat = np.abs(audio.flatten()) * 50

# Make it square (512x512)
size = 512
audio_chunk = audio_flat[:size*size]  # Take what we need
if len(audio_chunk) < size*size:
    # Pad with zeros if we don't have enough samples
    audio_chunk = np.pad(audio_chunk, (0, size*size - len(audio_chunk)))

# Normalize to 0-255 range for image
image_data = audio_chunk.reshape((size, size))
min_val = image_data.min()
max_val = image_data.max()
if max_val > min_val:
    image_data = ((image_data - min_val) / (max_val - min_val) * 255).astype(np.uint8)
else:
    # If there's no variation (silence), just return black
    image_data = np.zeros((size, size), dtype=np.uint8)

# Create and show image
img = Image.fromarray(image_data, mode='L')
img.save('mic_amplitude.png')
img.show()

print("🖼️ Done! Higher amplitude = brighter pixels. Simple as that.")