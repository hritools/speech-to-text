# Speech to Text
A speech recognition library with a primary use for Russian language. Mostly, it is a wrapper over the [SpeechRecognition library](https://github.com/Uberi/speech_recognition) but with the additional solutions such as Kaldi.

## Getting Started


### Installation

#### Linux
```
$ sudo apt-get install libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0
```

If you want to use Kaldi solution, follow [this](speechtotext/pykaldi/INSTALL.md) installation guide before you run ```pip install . ```

```
$ pip install .
```

#### Windows
```
TBD
```



### Different audio sources
```
from speechtotext import SpeechToText

# Initialize the speech to text solution
stt    = SpeechToText()

# Speech to text from audiofile
record = stt.record_from_audiofile("test_record.wav")
text   = stt.translate(record)
print(text)

# Speech to text from a microphone phrase
stt.adjust_for_ambient_noise()
record = stt.record_from_microphone()
text   = stt.translate(record)
print(text)
```

### Different recognition solutions
```
from speechtotext import SpeechToText
from speechtotext import SOLUTION_KALDI, SOLUTION_GOOGLE

# Initialize the speech to text solution
stt    = SpeechToText()

# Speech to text from audiofile using Kaldi solution
record = stt.record_from_audiofile("test_record.wav")
text   = stt.translate(record, solution=SOLUTION_KALDI)
print(text)

# Speech to text from audiofile using Google solution
record = stt.record_from_audiofile("test_record.wav")
text   = stt.translate(record, solution=SOLUTION_GOOGLE)
print(text)
```

### Supported audio formats
- WAV
- AIFF
- FLAC

### Supported solutions
What are the benchmarking datasets? - Relevant datasets to be found.

| Solution | Offline Usage | Supported Platforms | WER | RTF (Plato-CPU) | RTF (Plato-GPU) | Model Size (Acoustic and Language) |
:---:|:---:|:---:|:---:|:---:|:---:|:---:
Google Speech-to-Text | False | Ubuntu/Windows | TBD | TBD | TBD | TBD | TBD |
Kaldi | True | Ubuntu |TBD | TBD | TBD | TBD | TBD |
~~Mozilla DeepSpeech~~ | ? | True | TBD| TBD | TBD | TBD| TBD |