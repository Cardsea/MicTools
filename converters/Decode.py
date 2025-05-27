import numpy as np
import sounddevice as sd
from PIL import Image
import soundfile as sf

def image_to_stereo_sound(image_path='amplitude converter/outputfiles/mic_amplitude.png', output_path='amplitude converter/outputfiles/output.wav'):
    # Load and process the image
    print("📷 Loading image...")
    img = Image.open(image_path).convert('L')  # Convert to grayscale
    width, height = img.size
    
    # Convert image to numpy array
    image_data = np.array(img)
    
    # Split the image into left and right channels
    left_channel = image_data[:, :width//2]
    right_channel = image_data[:, width//2:]
    
    # Convert back to audio data
    left_audio = left_channel.flatten().astype(np.float32) / 255.0  # Normalize to 0-1
    right_audio = right_channel.flatten().astype(np.float32) / 255.0
    
    # Reverse the amplification from encoding
    left_audio = left_audio / 50
    right_audio = right_audio / 50
    
    # Combine channels into stereo
    stereo_audio = np.vstack((left_audio, right_audio)).T
    
    # Set audio parameters
    SAMPLE_RATE = 44100  # Hz
    
    # Save the audio file
    print("💾 Saving stereo audio file...")
    sf.write(output_path, stereo_audio, SAMPLE_RATE)
    
    # Play the audio
    print("🔊 Playing audio...")
    sd.play(stereo_audio, SAMPLE_RATE)
    sd.wait()
    
    print("✅ Done! Audio has been saved to", output_path)

def image_to_mono_sound(image_path='amplitude converter/outputfiles/mic_amplitude_mono.png', output_path='amplitude converter/outputfiles/output_mono.wav'):
    # Load and process the image
    print("📷 Loading mono image...")
    img = Image.open(image_path).convert('L')  # Convert to grayscale
    
    # Convert image to numpy array
    image_data = np.array(img)
    
    # Convert back to audio data
    audio_data = image_data.flatten().astype(np.float32) / 255.0  # Normalize to 0-1
    audio_data = audio_data / 50  # Reverse the amplification from encoding
    
    # Set audio parameters
    SAMPLE_RATE = 44100  # Hz
    
    # Save the audio file
    print("💾 Saving mono audio file...")
    sf.write(output_path, audio_data, SAMPLE_RATE)
    
    # Play the audio
    print("🔊 Playing mono audio...")
    sd.play(audio_data, SAMPLE_RATE)
    sd.wait()
    
    print("✅ Done! Mono audio has been saved to", output_path)

if __name__ == "__main__":
    image_to_stereo_sound()
    image_to_mono_sound() 