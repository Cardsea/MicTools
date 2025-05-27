import numpy as np
import sounddevice as sd
from PIL import Image
import time

SAMPLE_RATE = 44100  # Hz
DURATION = 5  # seconds
WIDTH = 936
HEIGHT = 469

print("🎙️ Recording will start in:")
for i in range(3, 0, -1):
    print(f"{i}...")
    time.sleep(1)

print("🎙️ Recording raw audio for 5 seconds (stereo)...")

# Record audio in stereo (2 channels)
audio = sd.rec(int(SAMPLE_RATE * DURATION), samplerate=SAMPLE_RATE, channels=2, dtype='float32')
sd.wait()

print("✅ Audio recorded, creating amplitude visualization...")

# Split into left and right channels and process
left_channel = np.abs(audio[:, 0]) * 50
right_channel = np.abs(audio[:, 1]) * 50

# Reshape channels to fill half the width each
samples_per_channel = HEIGHT * (WIDTH // 2)
left_chunk = left_channel[:samples_per_channel]
right_chunk = right_channel[:samples_per_channel]

# Pad if needed
if len(left_chunk) < samples_per_channel:
    left_chunk = np.pad(left_chunk, (0, samples_per_channel - len(left_chunk)))
if len(right_chunk) < samples_per_channel:
    right_chunk = np.pad(right_chunk, (0, samples_per_channel - len(right_chunk)))

# Reshape into 2D arrays
left_data = left_chunk.reshape((HEIGHT, WIDTH // 2))
right_data = right_chunk.reshape((HEIGHT, WIDTH // 2))

# Normalize each channel to 0-255
def normalize_channel(data):
    min_val = data.min()
    max_val = data.max()
    if max_val > min_val:
        return ((data - min_val) / (max_val - min_val) * 255).astype(np.uint8)
    return np.zeros_like(data, dtype=np.uint8)

left_image = normalize_channel(left_data)
right_image = normalize_channel(right_data)

# Combine channels side by side
image_data = np.concatenate((left_image, right_image), axis=1)

# Create and show image
img = Image.fromarray(image_data, mode='L')
img.save('amplitude converter/outputfiles/mic_amplitude_stereo.png')
img.show()

print(f"🖼️ Done! Created {WIDTH}x{HEIGHT} stereo image (Left | Right channels). Higher amplitude = brighter pixels.") 