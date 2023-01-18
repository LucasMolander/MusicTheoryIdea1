from typing import Dict, List, Optional
import numpy as np
import pandas as pd
import plotly.express as px
import simpleaudio as aud

# TODO Use a map like this rather than a bunch of if/else statements
NOTE_TO_FREQ: Dict[str, float] = {
    "A": 220.0,
    "A#": 233.08,
    "Bb": 233.08,
    # etc...
}

# TODO Use a map like this rather than some if/else statements
QUAL_TO_MULTS: Dict[str, List[float]] = {
    "Major7": [1.0, 5/4, 3/2, 15/8, 5/2, 3.0, 15/4, 5.0],
    # etc...
}

#finds f1 fundamental frequency for any musical note letter name
# TODO Use the type-hints that Python3 has (List, Optional, Dict, etc.)
def getFreqForNote(noteName) -> Optional[float]:
    if noteName not in NOTE_TO_FREQ:
        print("Please input a valid note name")
        return None
    return NOTE_TO_FREQ[noteName]

def getMultsForQuality(qualName) -> Optional[List[float]]:
    if qualName not in QUAL_TO_MULTS:
        print("Please input a valid chord quality(Major, Major7, minor, minor7, or 7)")
        return None
    return QUAL_TO_MULTS[qualName]

#calculates f2-8 based on f1 and chord quality
# TODO Don't use a capital Q in the variable name "Quality"
def chordBuilder8notes(noteName, qualName) -> Optional[List[float]]:
    f1 = getFreqForNote(noteName)
    if f1 is None:
        return None

    return getMultsForQuality(qualName)

#combine and hold chord for T based on
# calls: noteToFreq, chodBuilder8notes
def ChordHold(noteName, qualName, fs, T, wt):
    #find fundamental frequency based on note name e.g. C or Eb
    f1 = getFreqForNote(noteName)
    if f1 is None:
        return None

    #build chord based on frequency ratios associated with chord quality e.g. Major7
    eightNoteChord = chordBuilder8notes(noteName, qualName)  #returns f2-8
    if eightNoteChord is None:
        return None

    #start with sine wave of fundatmental
    notes = np.sin(f1 * wt)

    #add sine waves of the other 7 notes, weighted
    for i in eightNoteChord:
        notes = notes + (np.sin(i * wt)/(i*2/f1))  #weights lower notes louder based on ratio to fundamental

    return notes[0:int(T*fs)]

#generates ones and zeros to multiply for on-off eighth notes
def twoEighthNotesOnBeat(T, fs):
    ones = int(np.round(T*fs/4))
    envpt1 = np.ones(ones)
    zeros = np.zeros(int(np.round((T*fs/2)-ones)))

    envelope = np.hstack((envpt1, zeros))
    envelope = np.hstack((envelope, envelope))
    return envelope[0:int(T*fs)]
#generates zeros and ones to multiply for off-on eighth notes
def twoEightNotesOffBeat(T,fs):
    ones = int(np.round(T*fs/4))
    envpt1 = np.ones(ones)
    zeros = np.zeros(int(np.round((T*fs/2)-ones)))

    envelope = np.hstack((zeros, envpt1))
    envelope = np.hstack((envelope, envelope))
    return envelope[0:int(T*fs)]

#arpeggiates through all 8 notes in the given numbeer of beats
def ArpEightSteps(noteName, qualName, fs, T):
    f1 = getFreqForNote(noteName)
    if f1 is None:
        return None
    eightNoteChord = chordBuilder8notes(noteName, qualName)
    if eightNoteChord is None:
        return None
    t=np.arange(0,T/8.0,1.0/fs)                             #samples in time based of period and sampling frequenccy
    wt = t * 2 * np.pi                                     #multiplier to get freq to w for sin functions
    notes = np.sin(f1*wt)
    for i in eightNoteChord:
        notes = np.hstack((notes, np.sin(i * wt)))
    return notes[0:int(T*fs)]
