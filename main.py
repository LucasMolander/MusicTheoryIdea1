from dataclasses import dataclass
import numpy as np
import pandas as pd
import plotly.express as px
import simpleaudio as aud
import musicLogic as mus                            #my library of music theory logic funtions


# TODO Use a class like this to compartmentalize things and just pass it around
@dataclass
class Args:
    bpm: float
    beats: float
    fs: int

    def getT(self) -> float:
        return 60.0 * self.beats / self.bpm



# TODO Put the code in main()
def main():
    # TODO args like so
    a = Args(bpm=100.0, beats=2.0, fs=44100)

    # TODO Get rid of these
    bpm = 100.0                                         #beats per minute
    beats = 2.0                                         #number of beats per chord (default to 2)
    T = 60.0*beats/bpm                                  #Period based on number of beats at tempo
    fs=44100                                            #sampling frequency
    pi=np.pi                                            #pi
    t=np.arange(0,T,1.0/fs)                             #samples in time based of period and sampling frequenccy
    wt = t * 2 * pi                                     #multiplier to get freq to w for sin functions

    eighths = mus.twoEighthNotesOnBeat(T,fs)            #1s and 0s to multiply for on-off eighth notes (assuming beats = 2)
    eighthsRev = mus.twoEightNotesOffBeat(T,fs)         #0s and 1s to multiply for off-on eighth notes (assuming beats = 2)

    chord1 = mus.ChordHold("F#", "minor", fs, T, wt)    #hold chord with those notes
    chord1 = chord1 * eighths                           #multiply to make ryhthm eighth notes
    chord1arp = mus.ArpEightSteps("F#", "minor", fs, T) #generate arppegio with same notes
    chord1arp = chord1arp * eighthsRev                  #multiply to make rhythm offbeat eighth notes
    chord1 = chord1/2 + chord1arp/2                     #add chord beats to arp beats for whole 2 beat section

    chord2arp = mus.ArpEightSteps("B","minor7",fs,T)    #arpeggiate chord with new notes
    #chord2arp = chord2arp * eighths
    chord2 = mus.ChordHold("B", "minor", fs, T, wt)
    chord2 = chord2 * eighthsRev
    chord2 = chord2/2 + chord2arp

    chord3 = mus.ChordHold("E", "7", fs, T, wt)
    chord3 = chord3 * eighths
    chord3 = chord3/2 + mus.ArpEightSteps("E", "7", fs, T)/2

    chord4 = mus.ArpEightSteps("A", "Major7", fs, T)
    chord4 = chord4/2 + mus.ChordHold("A", "Major7", fs, T, wt)/2

    audio=np.hstack((chord1, chord2, chord3, chord4))   #concatenate chords together
    audio = audio * (2**15 - 1) / np.max(np.abs(audio)) #normalize (copy-pasted)
    audio = audio.astype(np.int16)                      #16-bit audio
    play_obj = aud.play_buffer(audio,1,2,fs)            #play audio until done
    play_obj.wait_done()

    #fig = px.line(audio)                               #plot waveform
    #fig.show()

# TODO This is for reasons
if __name__ == '__main__':
    main()
