# Tessitura/backend/midi_converter.py 
import os
import librosa 
import numpy as np
import mido
from mido import MidiFile, MidiTrack, Message

#============================================================================================================

def audio_to_midi(audio_path):
    print(f"Attempting to load audio from: {audio_path}")
    if not os.path.exists(audio_path):
        print(f"Error: Audio file not found at {audio_path}")
        return

    try:
        y, sr = librosa.load(audio_path, sr=None)                                   
        print(f"Audio loaded successfully. Sample rate: {sr}")
    except Exception as e:
        print(f"Error loading audio: {e}")
        return

    pitches, magnitudes = librosa.piptrack(y=y, sr=sr)                   # Extract pitch
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)                       # Estimate tempo
    
    tempo = tempo.item() if isinstance(tempo, np.ndarray) else tempo     # Extract scalar value from tempo
    print(f"Estimated tempo: {tempo}")

    midi = MidiFile()                                                    # MIDI file
    track = MidiTrack()                                                  # MIDI track
    midi.tracks.append(track)                                            # Append track to file
    
    t_prev = 0
    for idx, (pitch, magnitude) in enumerate(zip(np.max(pitches, axis=0), np.max(magnitudes, axis=0))):
        if magnitude > 0.1 and pitch > 0:                                # Thresholds
            note = int(69 + 12 * np.log2(pitch / 440.0))                 # Convert pitch (freq) to MIDI note
            time_in_seconds = librosa.frames_to_time([idx], sr=sr)[0]    # Convert to scalar
            
            t = mido.second2tick(time_in_seconds, midi.ticks_per_beat, tempo)   # Seconds to MIDI ticks
            track.append(Message('note_on', note=note, velocity=64, time=int(t - t_prev)))
            t_prev = t


    output_path = os.path.join('output', 'chorus.mid')
    output_dir = os.path.dirname(output_path)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created directory: {output_dir}")

    print(f"Attempting to save MIDI file to: {output_path}")
    try:
        midi.save(output_path)
        print(f"MIDI file saved successfully to {output_path}")
    except Exception as e:
        print(f"Error saving MIDI file: {e}")

#============================================================================================================


if __name__ == "__main__":
    audio_path = 'output/Espresso/chorus.WAV'
    audio_to_midi(audio_path)