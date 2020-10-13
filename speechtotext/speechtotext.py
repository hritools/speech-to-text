# TODO:
#   1. Adjust for ambient noises

import speech_recognition              as sr
import speechtotext.pykaldi.recognizer as kaldi


SOLUTION_GOOGLE = {"name": "google", "config": {}}
SOLUTION_KALDI  = {"name": "kaldi",  "config": {}}

class SpeechToText:
    def __init__(self, microphone_device_ind=None):
        self._recognizer            = sr.Recognizer()
        self._microphone            = None
        self._microphone_device_ind = microphone_device_ind

    def adjust_for_ambient_noise(self, duration=0.5):
        """
        Adjusts the recognizers for an ambient noise.
        """
        self._init_microphone()

        # Access the microphone
        with self._microphone:
            self._recognizer.adjust_for_ambient_noise(self._microphone, duration=duration)

    def record_from_microphone(self):
        """
        Records a phrase from the user.
        End of the phrase is identified automatically.
        """
        self._init_microphone()

        # Access the microphone
        with self._microphone:
            return self._recognizer.listen(self._microphone)

    def record_from_audiofile(self, path):
        with sr.AudioFile(path) as source:
            return self._recognizer.record(source)

    def translate(self, record, solution=SOLUTION_GOOGLE, language="ru-RU"):
        if solution["name"] == "google":
            # Check if the user specified its own key
            if "key" in solution["config"]:
                key = solution["config"]["key"]
            else:
                key = None
            return self._recognizer.recognize_google(record, key=key, language=language)
        elif solution["name"] == "kaldi":
            return kaldi.recognize(record)
        else:
            raise NotImplementedError("The desired solution is not implemented.")

    def _init_microphone(self):
        if self._microphone is None:
            self._microphone = sr.Microphone(device_index=self._microphone_device_ind)
