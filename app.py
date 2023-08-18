import sounddevice as sd
from scipy.io.wavfile import write
import wavio as wv
import asyncio
from shazamio import Shazam
 
freq = 44100
duration = 5

# Start recorder with the given values of duration and sample frequency
recording = sd.rec(int(duration * freq), samplerate=freq, channels=2)
# Record audio for the given number of seconds
sd.wait()

wv.write("./recordings/recording1.wav", recording, freq, sampwidth=2)

# Recognizing song
async def main():
  shazam = Shazam()
  out = await shazam.recognize_song('./recordings/recording1.wav')
  print(f"{out['track']['title']} by {out['track']['subtitle']}")

loop = asyncio.get_event_loop()
loop.run_until_complete(main())