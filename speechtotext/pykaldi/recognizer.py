import os
import subprocess
import uuid

from speech_recognition import AudioData

THIS_FILE_DIR      = os.path.dirname(__file__)
REC_SCRIPT_PATH    = os.path.join(THIS_FILE_DIR, "rec.sh")
WORDS_PATH         = os.path.join(THIS_FILE_DIR, "kaldi_gst/tdnn/graph/words.txt")
MFCC_PATH          = os.path.join(THIS_FILE_DIR, "kaldi_gst/tdnn/conf/mfcc.conf")
IVECTOR_EXTRACTION = os.path.join(THIS_FILE_DIR, "kaldi_gst/tdnn/conf/ivector_extractor.conf")
FST_PATH           = os.path.join(THIS_FILE_DIR, "kaldi_gst/tdnn/graph/HCLG.fst")
MODEL_PATH         = os.path.join(THIS_FILE_DIR, "kaldi_gst/tdnn/final.mdl")

def recognize(audiodata: AudioData):
    # Save audiodata to disk and get a path to it
    tmp_path = _save_audio_data_to_disk(audiodata)

    # Start speech recognition
    shellscript = subprocess.Popen(['sh', REC_SCRIPT_PATH, tmp_path, WORDS_PATH, MFCC_PATH, IVECTOR_EXTRACTION, FST_PATH, MODEL_PATH, THIS_FILE_DIR], stdin=subprocess.PIPE)
    shellscript.wait()

    # Read the transcribed text from a temporary file
    path = tmp_path + ".txt"
    text = None
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()

    # Delete the temporary files
    os.remove(path)
    os.remove(tmp_path)

    # Return the transcribed text
    return text

def _save_audio_data_to_disk(audiodata: AudioData):
    name       = str(uuid.uuid4())

    # GStreamer audioconverters may lost during the installation
    # So we use raw audioformat and it is cruicial to resample the audio at the proper rate (mfcc.conf)
    audio_data = audiodata.get_raw_data(convert_rate=8000) 
    path       = name + ".raw"

    with open(path, mode="wb") as f:
        f.write(audio_data)
        path = os.path.abspath(f.name)
    
    return path