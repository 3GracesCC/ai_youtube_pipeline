import os
from TTS.api import TTS

def generate_voiceover(script_path, output_dir="voiceovers"):
    os.makedirs(output_dir, exist_ok=True)
    with open(script_path, "r", encoding="utf-8") as f:
        text = f.read()
    
    tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=False, gpu=False)
    audio_path = os.path.join(output_dir, os.path.basename(script_path).replace(".txt", ".wav"))
    tts.tts_to_file(text=text, file_path=audio_path)
    
    return audio_path