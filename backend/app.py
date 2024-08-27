from flask import Flask, jsonify
import os
from midi_converter import audio_to_midi
from note_converter import midi_to_notes, generate_tabs

app = Flask(__name__)

@app.route('/convert', methods=['POST'])
def convert_audio():
    audio_path = 'input/chorus.WAV' # TEST RUN
    midi_path = 'output/chorus.mid'
    
    audio_to_midi(audio_path)
    notes = midi_to_notes(midi_path)
    tabs = generate_tabs(notes)
    
    return jsonify({'tabs': tabs})

if __name__ == '__main__':
    app.run(debug=True)
