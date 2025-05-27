import pyaudio
import numpy as np
import time

THRESHOLD = 500  # adjust to your mic level
DOT_DURATION = 0.13
DASH_DURATION = 0.4
LETTER_SPACE = 0.39
WORD_SPACE = 0.91

# Morse dictionary same as before
MORSE_CODE_DICT = {
    '.-': 'A', '-...': 'B', '-.-.': 'C',
    '-..': 'D', '.': 'E', '..-.': 'F',
    '--.': 'G', '....': 'H', '..': 'I',
    '.---': 'J', '-.-': 'K', '.-..': 'L',
    '--': 'M', '-.': 'N', '---': 'O',
    '.--.': 'P', '--.-': 'Q', '.-.': 'R',
    '...': 'S', '-': 'T', '..-': 'U',
    '...-': 'V', '.--': 'W', '-..-': 'X',
    '-.--': 'Y', '--..': 'Z', '-----': '0',
    '.----': '1', '..---': '2', '...--': '3',
    '....-': '4', '.....': '5', '-....': '6',
    '--...': '7', '---..': '8', '----.': '9'
}

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=44100,
                input=True,
                frames_per_buffer=1024)

def is_signal(data):
    amplitude = np.abs(np.frombuffer(data, dtype=np.int16)).mean()
    return amplitude > THRESHOLD

print("🐾 Listening for Morse...")

signal_start = None
silence_start = None
current_symbol = ''
decoded_message = ''

try:
    while True:
        data = stream.read(1024)
        if is_signal(data):
            if silence_start:
                # calculate silence duration
                silence_time = time.time() - silence_start
                silence_start = None

                # Decide if letter or word space
                if silence_time >= WORD_SPACE:
                    # word boundary
                    if current_symbol:
                        decoded_message += MORSE_CODE_DICT.get(current_symbol, '?')
                        current_symbol = ''
                    decoded_message += ' '
                    print(' ', end='', flush=True)
                elif silence_time >= LETTER_SPACE:
                    # letter boundary
                    if current_symbol:
                        decoded_message += MORSE_CODE_DICT.get(current_symbol, '?')
                        current_symbol = ''
                    print('', end='', flush=True)

            if not signal_start:
                signal_start = time.time()

        else:
            if signal_start:
                # calculate signal length
                signal_time = time.time() - signal_start
                signal_start = None

                # Decide if dot or dash
                if signal_time < (DOT_DURATION + DASH_DURATION) / 2:
                    current_symbol += '.'
                    print('.', end='', flush=True)
                else:
                    current_symbol += '-'
                    print('-', end='', flush=True)

            if not silence_start:
                silence_start = time.time()

except KeyboardInterrupt:
    print("\n🐾 Done decoding!")
    print("Message:", decoded_message)
finally:
    stream.stop_stream()
    stream.close()
    p.terminate()