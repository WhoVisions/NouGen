#!/usr/bin/env python3
"""
NouGen Voice Gateway (speak.py)
Unified, local-first neural speech synthesis with hardware-bound speaker routing.
Priority: Kokoro-82M (af_bella studio neural voice) -> native fallback (device 181).
"""
import os
import sys
import subprocess

DEFAULT_VOICE = os.environ.get("NOUGEN_VOICE", "af_bella")
DEFAULT_SPEED = float(os.environ.get("NOUGEN_VOICE_SPEED", "1.1"))
DEVICE_ID = "181"  # Mac mini internal physical speaker

def speak(text: str, voice: str = DEFAULT_VOICE, speed: float = DEFAULT_SPEED):
    if not text or not text.strip():
        return

    # Guarantee volume is unmuted
    subprocess.run(["osascript", "-e", "set volume output volume 100 without output muted"], 
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # 1. Primary: Kokoro-82M Neural Synthesis
    try:
        from kokoro_onnx import Kokoro
        import soundfile as sf

        voice_dir = os.path.expanduser("~/.nougen/voices")
        model_path = os.path.join(voice_dir, "kokoro-v0_19.onnx")
        voices_path = os.path.join(voice_dir, "voices.bin")

        if os.path.exists(model_path) and os.path.exists(voices_path):
            kokoro = Kokoro(model_path, voices_path)
            lang = "en-gb" if voice.startswith("b") else "en-us"
            samples, sr = kokoro.create(text, voice=voice, speed=speed, lang=lang)

            wav_path = f"/tmp/nougen_voice_{os.getpid()}.wav"
            sf.write(wav_path, samples, sr)

            subprocess.run(["afplay", wav_path], check=True)
            if os.path.exists(wav_path):
                os.remove(wav_path)
            return
    except Exception:
        pass

    # 2. Fallback: macOS native synthesis directed to Device 181
    try:
        subprocess.run(["say", f"--audio-device={DEVICE_ID}", "-v", "Samantha", text], check=True)
    except Exception:
        subprocess.run(["say", text])

if __name__ == "__main__":
    if len(sys.argv) > 1:
        message = " ".join(sys.argv[1:])
        speak(message)
