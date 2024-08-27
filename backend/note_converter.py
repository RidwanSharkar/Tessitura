# Tessitura/Backend/note-converter.py 
import mido
import os

#============================================================================================================

def midi_to_notes(midi_path):
    midi_file = mido.MidiFile(midi_path)
    notes = []
    for track in midi_file.tracks:
        for msg in track:
            if msg.type == 'note_on' and msg.velocity > 0:
                note_name = get_note_name(msg.note)
                notes.append((note_name, msg.note))
    return notes

#============================================================================================================
    
def get_note_name(note_number, sharps=True):
    notes_sharp = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    notes_flat = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
    notes = notes_sharp if sharps else notes_flat
    octave = note_number // 12 - 1
    return f"{notes[note_number % 12]}{octave}"

#============================================================================================================

def generate_tabs(notes):
    tabs = []
    for note_name, note_number in notes:
        string, fret, octave = note_to_guitar_tab(note_number)
        if string != 'X': 
            tabs.append(f"{string} string, {fret} fret, octave {octave}")
    return tabs

#============================================================================================================

def note_to_guitar_tab(note_number):
    string_fret_map = {
        # Low E (MIDI note range no. 40-69)
        40: ('LowE', 2, 0),  # E2
        41: ('LowE', 2, 1),  # F2
        42: ('LowE', 2, 2),  # F#2
        43: ('LowE', 2, 3),  # G2
        44: ('LowE', 2, 4),  # G#2
        45: ('LowE', 2, 5),  # A2
        # A string
        45: ('A', 3, 0),  # A2
        46: ('A', 3, 1),  # A#2/Bb2
        47: ('A', 3, 2),  # B2
        48: ('A', 3, 3),  # C3
        49: ('A', 3, 4),  # C#3/Db3
        50: ('A', 3, 5),  # D3
        # D string
        50: ('D', 4, 0),  # D3
        51: ('D', 4, 1),  # D#3/Eb3
        52: ('D', 4, 2),  # E3
        53: ('D', 4, 3),  # F3
        54: ('D', 4, 4),  # F#3/Gb3
        55: ('D', 4, 5),  # G3
        # G string
        55: ('G', 5, 0),  # G3
        56: ('G', 5, 1),  # G#3/Ab3
        57: ('G', 5, 2),  # A3
        58: ('G', 5, 3),  # A#3/Bb3
        59: ('G', 5, 4),  # B3
        60: ('G', 5, 5),  # C4
        # B string
        59: ('B', 6, 0),  # B3
        60: ('B', 6, 1),  # C4
        61: ('B', 6, 2),  # C#4/Db4
        62: ('B', 6, 3),  # D4
        63: ('B', 6, 4),  # D#4/Eb4
        64: ('B', 6, 5),  # E4
        # High E 
        64: ('highE', 1, 0),  # E4
        65: ('highE', 1, 1),  # F4
        66: ('highE', 1, 2),  # F#4/Gb4
        67: ('highE', 1, 3),  # G4
        68: ('highE', 1, 4),  # G#4/Ab4
        69: ('highE', 1, 5),  # A4
    } 
    return string_fret_map.get(note_number, ('X', 0, 0))  # Return (String, Fretnum, Octave) if note num is found in map

#============================================================================================================

midi_path = os.path.join('output', 'chorus.mid')
notes = midi_to_notes(midi_path)
tabs = generate_tabs(notes)
for tab in tabs:
    print(tab)

#============================================================================================================
#============================================================================================================
