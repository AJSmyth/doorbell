from PyQt5.QtWidgets import *
from PyQt5 import QtMultimedia, QtCore
from tones import SINE_WAVE
from tones.mixer import Mixer
import re

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.loLarge = QVBoxLayout()
        self.loEnter = QHBoxLayout()

        self.text = QLineEdit()
        self.text.returnPressed.connect(self.on_submit)
        self.submit = QPushButton('Submit')
        self.submit.clicked.connect(self.on_submit)
        self.bpm = QSpinBox()
        self.bpm.setValue(30)
        self.bpm.setRange(5, 180)
        self.label = QLabel('BPM:')

        self.loEnter.addStretch(1)
        self.loEnter.addWidget(self.text, 0)
        self.loEnter.addWidget(self.label, 0)
        self.loEnter.addWidget(self.bpm, 0)
        self.loEnter.addWidget(self.submit, 0)

        self.label = QLabel('Enter a doorbell code string:')
        self.loLarge.addStretch(1)
        self.loLarge.addWidget(self.label, 0)
        self.loLarge.addLayout(self.loEnter, 0)

        self.setLayout(self.loLarge)

    def on_submit(self):
        string_to_wav(self.text.text(), self.bpm.value())
        self.sound = QtMultimedia.QSoundEffect()
        self.sound.setSource(QtCore.QUrl.fromLocalFile('doorbell.wav'))
        self.sound.setVolume(50)
        self.sound.play()

def main():
    app = QApplication([])
    window = Window()
    window.show()
    app.exec_()

def string_to_wav(string, bpm):
    spb = (1 / bpm) * 60
    mixer = Mixer(44100, 0.5)
    mixer.create_track(1, SINE_WAVE, attack=0.05, decay=0.05)

    x = re.findall("\*?[0-9a-b][1-6]", string)
    if '00' in x:
        x.remove('00')
    octaves = [(5 + (len(i) > 2)) for i in x]
    notes = [code_to_note(i[len(i)//3]) for i in x]
    lengths = [(code_to_frac(i[(len(i)*2)//3]) * spb / 8) for i in x]

    for i in range(len(notes)):
        mixer.add_note(1, note=notes[i], octave=octaves[i], duration=lengths[i])
    mixer.write_wav('doorbell.wav')

def code_to_note(code):
    notes = {
    '0': 'c',
    '1': 'c#',
    '2': 'd',
    '3': 'd#',
    '4': 'e',
    '5': 'f',
    '6': 'f#',
    '7': 'g',
    '8': 'g#',
    '9': 'a',
    'a': 'a#',
    'b': 'b'
    }
    return notes.get(code)

def code_to_frac(code):
    fracs = {
    '1': 1,
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 8
    }
    return fracs.get(code)

if __name__ == "__main__":
    main()
