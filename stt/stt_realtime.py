import os
import tempfile
import logging
import pyaudio
import wave

from httpx import AsyncClient, HTTPError
from pydub import AudioSegment
from config import settings

from .log_setup import setup_logging


FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 5

setup_logging()


def record_audio():
    audio = pyaudio.PyAudio()
    stream = audio.open(
        format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK
    )
    logging.info("Recording...")

    frames = []
    for _ in range(int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    logging.info("Finished Recording")
    stream.stop_stream()
    stream.close()
    audio.terminate()

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio_file:
        wf = wave.open(temp_audio_file.name, "wb")
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b"".join(frames))
        wf.close()

        return temp_audio_file.name


async def recognize_speech(audio_file_path):
    with open(audio_file_path, "rb") as audio_file:
        files = {"file": ("audio.wav", audio_file, "audio/wav")}
        data = {
            "return_offsets": "false",
            "run_diarization": "false",
            "language": settings.LANGUAGE,
            "blocking": "true",
        }
        headers = {"Authorization": f"Bearer {settings.API_KEY}"}

        async with AsyncClient() as client:
            response = await client.post(
                settings.API_URL, headers=headers, files=files, data=data
            )

    try:
        response.raise_for_status()

        if response.status_code == 200:
            result = response.json()
            return result["result"]["text"]

        else:
            logging.error(f"Error: {response.status_code}, {response.text}")

    except HTTPError as e:
        logging.error("Some Internet Connection Error")
