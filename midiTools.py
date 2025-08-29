import mido
from midiutil import MIDIFile
from ccChartEdit import Event as ccEvent


event_to_pitch = {
    "tap": 60,  
    "slide": 61, 
    "hold start": 69, 
    "hold end": 70,
    "hold slide": 71,
    "hold midpoint": 59
}

#   ✨magic numbers✨
GRID_SIZE = 59.8
FMS_HEIGHT_MULTIPLIER = 1.28205

def ExportMidi(events, output_file):
    #sort events by time
    events.sort(key=lambda e: e.time)

    for i, event in enumerate(events):
        if i > 0:
            if event.ms_type == "BMS":
                if events[i-1].lane == event.lane:
                    event.lane = -1
            # elif event.ms_type == "FMS":
            #     if events[i-1].fms_height == event.fms_height:
            #         #event.fms_height = -1


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

        if event.ms_type == "FMS":
            volume = round(event.fms_height*FMS_HEIGHT_MULTIPLIER)
            if volume < 1: volume = 0
            if volume > 126: volume = 127


        MyMIDI.addNote(track, channel, pitch, time, duration, volume)

        if event.ms_type == "BMS":
            if not event.lane == -1:
                lane = 58-event.lane
                if lane < 1: lane = 0
                if lane > 254: lane = 255
                MyMIDI.addNote(track, channel, lane, time, duration, volume)
        # elif event.ms_type == "FMS":
        #     if not event.fms_height == -1:
                # MyMIDI.addNote(track, channel, 58, time, duration, round(event.fms_height))
        elif event.ms_type == "EMS":
            MyMIDI.addNote(track, channel, 58, time, duration, volume)

    with open(output_file, "wb") as midi_output_file:
        MyMIDI.writeFile(midi_output_file)

    return output_file

def NotesFromMidi(file):
    mid = mido.MidiFile(file)
    current_time = 0
    tempo = next((e.tempo for e in mid if e.type == 'set_tempo'), None)
    out = []

    for track in mid.tracks:
        for msg in track:
            current_time += msg.time
            if msg.type == 'note_on':
                time_in_seconds = mido.tick2second(current_time, mid.ticks_per_beat, tempo)

                out.append((msg.note, time_in_seconds*100 / 1.671679, msg.velocity))
    return out

def ImportMidi(file, ms_type):
    notes = NotesFromMidi(file)
    events = []
    for note, time, velocity in notes:
        existing_event = next((e for e in events if e.time == time), None)
        if not existing_event:
            existing_event = ccEvent(time, ms_type)
            existing_event.set_rotation(0)
            events.append(existing_event)


        if ms_type == "BMS":
            if note >= 50 and note <= 58:
                existing_event.set_lane(58 - note)
        elif ms_type == "FMS":
                existing_event.set_fms_height(round(velocity/FMS_HEIGHT_MULTIPLIER))
        elif ms_type == "EMS":
            if note == 58:
                existing_event.set_fms_height(velocity)
        if note == 60:
            existing_event.set_type(0)
        if note == 59:
            existing_event.set_type(3)
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
