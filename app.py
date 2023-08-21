import sounddevice as sd
from scipy.io.wavfile import write
import wavio as wv
import asyncio
from shazamio import Shazam


# Recognizing song
async def recognize():
	freq = 44100
	duration = 5

	# Start recorder with the given values of duration and sample frequency
	recording = sd.rec(int(duration * freq), samplerate=freq, channels=2)
	# Record audio for the given number of seconds
	sd.wait()

	wv.write("temp_rec.wav", recording, freq, sampwidth=2)
	try:
		shazam = Shazam()
		out = await shazam.recognize_song('temp_rec.wav')
		textToDisplay = f"{out['track']['title']} by {out['track']['subtitle']}\n\n"
		try:
			for line in out['track']['sections'][1]['text']:
				textToDisplay = textToDisplay + line + "\n"
			return textToDisplay
		except:
			return textToDisplay
	except:
		return "No music has been found"
