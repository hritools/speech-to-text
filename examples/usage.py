from speechtotext import SpeechToText, SOLUTION_GOOGLE, SOLUTION_KALDI

stt    = SpeechToText()

# Speech to text from audiofile
print("-----------------")
print("Read audio from a file (test_record.wav)")
record = stt.record_from_audiofile("test_record.wav")

text   = stt.translate(record, solution=SOLUTION_KALDI)
print("Kaldi solution: {}".format(text))
text   = stt.translate(record, solution=SOLUTION_GOOGLE)
print("Google solution: {}".format(text))

# Speech to text from a microphone phrase
print("-----------------")
print("Read audio from a microphone.")

print("Important: Adjust for an ambient noise first!")
stt.adjust_for_ambient_noise()
print("Adjusted for an ambient noise.")

print("Speak!")
record = stt.record_from_microphone()

text   = stt.translate(record, solution=SOLUTION_KALDI)
print("Kaldi solution: {}".format(text))
text   = stt.translate(record, solution=SOLUTION_GOOGLE)
print("Google solution: {}".format(text))