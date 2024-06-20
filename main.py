import asyncio
import os

from stt import record_audio, recognize_speech


async def main():
    audio_file_path = record_audio()
    text = await recognize_speech(audio_file_path)
    os.remove(audio_file_path)

    if text:
        print("Распознанный текст:", text)
    else:
        print("Не удалось распознать речь")


if __name__ == "__main__":
    while True:
        asyncio.run(main())
