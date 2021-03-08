#!/usr/bin/env python3

from vosk import Model, KaldiRecognizer
import sys
import os
import wave
import subprocess

if not os.path.exists("model"):
    print ("Please download the model from https://github.com/alphacep/vosk-api/blob/master/doc/models.md and unpack as 'model' in the current folder.")
    exit (1)

wf = wave.open(sys.argv[1], "rb")
if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
    print ("Audio file must be WAV format mono PCM.")
    exit (1)

model = Model("model")
# You can also specify the possible word list
rec = KaldiRecognizer(model, wf.getframerate(), "what time is it now [unk]")

while True:
    data = wf.readframes(4000)
    if len(data) == 0:
        break
    if rec.AcceptWaveform(data):
        if ("what time is it now" in rec.Result()):
            print("FOUND!!!")
            subprocess.call(['sh', './espeak_demo.sh'])
        else:
            print("NOT FOUND")
    #else:
        #print(rec.PartialResult())
        #if(rec.PartialResult() == "time is it"):
            #print("found")

#print(rec.FinalResult().type())
