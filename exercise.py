#!/usr/bin/env python

import subprocess, time, sys

class Speaker():
    def __init__(self, voice = "Alex"):
        self.voice = voice

    def say(self, phrase):
        subprocess.Popen(["say", "-v", self.voice, phrase])

class Timer():
    def __init__(self, speaker):
        self.phrases = []
        self.lastTime = 0.0
        self.speaker = speaker

    def addPhrase(self, phrase, wait):
        self.phrases.append((phrase, self.lastTime + wait))
        self.lastTime += wait

    def run(self):
        phrasePointer = 0
        timeStarted = time.time()
        while (phrasePointer != len(self.phrases)):
            (phrase, trigger) = self.phrases[phrasePointer]
            self.speaker.say(phrase)
            print("Said '%s', waiting until %d seconds." % (phrase, trigger))
            while ((time.time() - timeStarted) < trigger):
                time.sleep(0.1)
            phrasePointer += 1

class Exercise():
    def __init__(self, exerciseTime, warnTime, restTime, repeatCount, timer):
        self.exerciseTime = exerciseTime
        self.warnTime = warnTime
        self.restTime = restTime
        self.repeatCount = repeatCount
        self.timer = timer
        self.exercises = []

    def addPhrase(self, name, time):
        self.timer.addPhrase(name, time)

    def addExercise(self, name, shouldSwitchSides):
        self.exercises.append((name, shouldSwitchSides))

    def finish(self):
        idx = 0
        while (idx != len(self.exercises)):
            (name, switch) = self.exercises[idx]
            if (not switch):
                self.timer.addPhrase(name, self.exerciseTime - self.warnTime)
            else:
                self.timer.addPhrase(name, (self.exerciseTime / 2))
                self.timer.addPhrase("Switch sides", (self.exerciseTime / 2) - self.warnTime)
            self.timer.addPhrase(str(self.warnTime) + " seconds left", self.warnTime)

            idx += 1

            if (idx != len(self.exercises)):
                (nextExercise, _) = self.exercises[idx]
                self.timer.addPhrase("Rest, get ready for " + nextExercise, self.restTime)
            else:
                self.timer.addPhrase("Done!", self.restTime)

    def run(self):
        for i in xrange(0, self.repeatCount):
            self.timer.run()

def usage():
    print("exercise.py [-f] [-t <exercise time>] [-w <warning time>] [-r <rest time>] [-n <times to repeat>]")
    print("  -f : Use a female voice")
    print("  -h : Get this help")
    print("Default is (-t) 30s exercise time, warning (-w) 5s before the end, resting for (-r) 10s after each exercise, repeating (-n) once.")

speaker = None
exerciseTime = 30
warnTime = 5
restTime = 10
repeat = 1

idx = 1
while (idx < len(sys.argv)):
    if (sys.argv[idx] == "-f"):
        speaker = Speaker("Victoria")
    elif (sys.argv[idx] == "-v"):
        speaker = Speaker(sys.argv[idx+1])
        idx += 1
    elif (sys.argv[idx] == "-t"):
        exerciseTime = int(sys.argv[idx+1])
        idx += 1
    elif (sys.argv[idx] == "-w"):
        warnTime = int(sys.argv[idx+1])
        idx += 1
    elif (sys.argv[idx] == "-r"):
        restTime = int(sys.argv[idx+1])
        idx += 1
    elif (sys.argv[idx] == "-n"):
        repeat = int(sys.argv[idx+1])
        idx += 1
    elif (sys.argv[idx] == "-h"):
        usage()
        sys.exit(0)
    else:
        print("Unrecognised option: " + sys.argv[idx])
        usage()
        sys.exit(1)
    idx += 1

if (speaker == None):
    speaker = Speaker()

exercise = Exercise(exerciseTime, warnTime, restTime, repeat, Timer(speaker))
exercise.addPhrase("Starting in 10 seconds...", 7)
exercise.addPhrase("3", 1)
exercise.addPhrase("2", 1)
exercise.addPhrase("1", 1)
exercise.addExercise("Jumping jacks", False)
exercise.addExercise("Wall sit", False)
exercise.addExercise("Press ups", False)
exercise.addExercise("Abdominal crunch", False)
exercise.addExercise("Step up onto chair", True)
exercise.addExercise("Squats", False)
exercise.addExercise("Triceps dip on chair", False)
exercise.addExercise("Plank", False)
exercise.addExercise("High knees running", False)
exercise.addExercise("Lunge", True)
exercise.addExercise("Press ups with rotation", True)
exercise.addExercise("Side plank", True)
exercise.finish()
exercise.run()
