import numpy as np
import sounddevice as sd
from PIL import Image
import time
import math

SAMPLE_RATE = 44100  # Hz
DURATION = 5  # seconds

# Calculate optimal square size based on total samples
total_samples = SAMPLE_RATE * DURATION  # Total number of samples in 5 seconds
size = int(math.sqrt(total_samples))  # Square root to get a reasonable square dimension
size = size - (size % 2)  # Make it even for better visualization

print("🎙️ Recording will start in:")
for i in range(3, 0, -1):
    print(f"{i}...")
    time.sleep(1)

print("🎙️ Recording raw audio for 5 seconds (mono)...")

# Record audio in mono (1 channel)
audio = sd.rec(int(SAMPLE_RATE * DURATION), samplerate=SAMPLE_RATE, channels=1, dtype='float32')
sd.wait()

print("✅ Audio recorded, creating amplitude visualization...")

# Get absolute amplitudes and amplify them significantly
audio_flat = np.abs(audio.flatten()) * 50

# Make it square (size x size)
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
img.save('amplitude converter/outputfiles/mic_amplitude_mono.png')
img.show()

print(f"🖼️ Done! Created {size}x{size} mono image. Higher amplitude = brighter pixels.")