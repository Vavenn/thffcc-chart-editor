from operator import is_
from sched import Event
import mido
from midiutil import MIDIFile
from ccChartEdit import Event as ccEvent


event_to_pitch = {
    "tap": 60,  # tap
    "slide": 61,  # slide
    "hold start": 69,  # hold start
    "hold end": 70,  # hold end
    "hold slide": 71,  # hold slide
}

GRID_SIZE = 59.8

def ExportMidi(events, output_file):
    output_dir = output_file
    MyMIDI = MIDIFile(1)
    track = 0
    time = 0
    duration = 1/GRID_SIZE
    tempo = 60
    volume = 80
    channel =  0
    grid_offset = 0

    MyMIDI.addTempo(track, time, tempo)

    for event in events:
        pitch = event_to_pitch.get(event.event_type, 60)  # Default to 60 if not found
        if event.event_type == "slide" or event.event_type == "hold slide":
            pitch += event.direction  # Adjust pitch based on direction
        time = event.time_sec*(60/GRID_SIZE)-(grid_offset/GRID_SIZE)
        MyMIDI.addNote(track, channel, pitch, time, duration, volume)
        MyMIDI.addNote(track, channel, 58-event.lane, time, duration, volume)

    with open(output_file, "wb") as output_file:
        MyMIDI.writeFile(output_file)

    return output_dir

def NotesFromMidi(file):
    mid = mido.MidiFile(file)
    current_time = 0
    tempo = next((e.tempo for e in mid if e.type == 'set_tempo'), None)
    out = []

    for track in mid.tracks:
        for msg in track:
            current_time += msg.time
            if msg.type == 'note_on' and msg.velocity > 0:
                time_in_seconds = mido.tick2second(current_time, mid.ticks_per_beat, tempo)
                out.append((msg.note, time_in_seconds*100 / 1.671679))

    return out

def ImportMidi(file):
    notes = NotesFromMidi(file)
    events = []
    for note, time in notes:
        existing_event = next((e for e in events if e.time == time), None)
        if not existing_event:
            existing_event = ccEvent(time)
            existing_event.set_rotation(0)
            events.append(existing_event)
            

        if note >= 50 and note <= 58:
            existing_event.set_lane(58 - note)
        if note == 60:
            existing_event.set_type(0)
        if note >= 61 and note <= 68:
            existing_event.set_type(1)
            existing_event.set_rotation((note - 61) * 45)
        if note == 69:
            existing_event.set_type(2)
        if note == 70:
            existing_event.set_type(4)
        if note >= 71 and note <= 79:
            existing_event.set_type(5)
            existing_event.set_rotation((note - 71) * 45)
    return events
