import pretty_midi as pm
# Env variables
chrom_notes = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B'] # A list of all the notes/pitch classes with
                                                                                # indices corresponding to 
                                                                                # MIDI note values mod 12
        
chrom_degrees = ['I', 'IIb', 'II', 'IIIb', 'III', 'IV', 'Vb', 'V', 'VIb', 'VI', 'VIIb', 'VII'] # A list of all the relative pitch classes

offsets = { # A list of chord intervals with their corresponding MIDI note value offset
    '1': 0, 
    '2': 2,
    '3': 4,
    '4': 5,
    '5': 7,
    '6': 9,
    '7': 11,
    '8': 12,
    '9': 14,
    '10': 16,
    '11': 17,
    '12': 19,
    '13': 21
}


def first_note(notes):
    """
    Returns the first note by time in a list of notes.
    Parameters:
        notes: list of PrettyMIDI notes
    Returns:
        f_note: the first PrettyMIDI note in the list
    """
    if notes == []:
        return None
    f_note = notes[0]
    for i in range(1, len(notes)):
        if notes[i].start < f_note.start:
            f_note = notes[i]
    return f_note

def last_note(notes):
    """
    Returns the last note by time in a list of notes.
    Parameters:
        notes: list of PrettyMIDI notes
    Returns:
        l_note: the last PrettyMIDI note in the list
    """
    if notes == []:
        return None
    l_note = notes[0]
    for i in range(1, len(notes)):
        if notes[i].start > l_note.start:
            l_note = notes[i]
    return l_note

def consolidate_notes(song):
    """
    Returns a list of all the non-drum notes in a song regardless of instrument.
    Parameters:
        notes: a PrettyMIDI song
    Returns:
        output: list of PrettyMIDI notes
    """
    notes = []
    for instrument in song.instruments:
        if not instrument.is_drum:
            for note in instrument.notes:
                notes.append(note)
    return notes

def get_note(note_n):
    """
    Returns a note name based on its MIDI note number
    Parameters:
        notes: an integer representing the MIDI note number
    Returns:
        output: a string containing the note name
    """
    return chrom_notes[note_n % 12]

def parse_chord(root, number_string):
    """
    Returns the note corresponding to a particular degree in a scale defined by the root note.
    Ex. parse_chord("C", "3") -> "E"
    Ex. parse_chord("G", "(b7)") -> "(F)"
    Parameters:
        root: a string representing the root note of the scale the degree is checked in
        number_string: a string representing the degree of the note in the scale, possibly containing b, #, or ()
    Returns:
        out: a string containing the note (pitch class) of the scale degree
    """
    note_num = chrom_notes.index(root)
    out = ""
    num = ""
    scale_num = 0
    parentheses = False
    for char in number_string:
        if char == '(':
            parentheses = True
        if char == 'b':
            scale_num -= 1
        if char == '#':
            scale_num += 1
        if char >= '0' and char <= '9':
            num += char
    scale_num += offsets.get(num)
    if (parentheses):
        out = "("
    out += str(chrom_notes[(note_num + scale_num) % 12])
    if (parentheses):
        out += ")"
    return out

def generate_chord_list(filepath = ".\\chords without names.txt"):
    """
    Outputs a dictionary of chords mapped to the notes they contain based on a list of chord types in a text file.
    Parameters:
        filepath: the path to a text file containing all the types of chords
    Returns:
        chord_list: a dictionary of strings (representing chord names) 
                    mapped to a list of strings (representing the names of the notes in the chord)
    """
    chord_list = []
    for note in chrom_notes:
        f = open(filepath)
        lines = f.readlines()
        for line in lines:
            parts = line.split()
            chord_name = ''
            note_list = []
            for i in range(len(parts)):
                part = parts[i]
                if i == 0:
                    note_string = note + '-'
                    chord_name = part.replace('_', note_string, 1)
                elif part[0] == 'b' or part[0] == '#' or \
                   (part[0] >= '0' and part[0] <= '9') or \
                   part[0] == '(':
                    note_list.append(parse_chord(note, part))
                else: continue
            chord_list.append([chord_name, note_list])
    return chord_list

def get_chords(notes, 
               offset = 0.01):
    """
    Returns the chords (groups of notes occuring at the same time) in a list of notes.
    Parameters:
        notes: a list of notes
        offset: a parameter shifting the time selected for to allow chords to be picked up
    Returns:
        chords: a list of lists of PrettyMIDI notes (each list of PrettyMIDI notes in the bigger list is a chord)
    """
    start_times = []
    for note in notes:
        if not (note.start in start_times):
            start_times.append(note.start)
    chords = []
    for time in start_times:
        playing_notes = []
        actual = time + offset
        for note in notes:
            if note.start < actual and note.end >= time:
                playing_notes.append(note)
        chords.append(playing_notes)
    return chords

def get_chords_window(notes, 
                      offset = 0.01,
                      window = 0.5):
    """
    Returns the chords (groups of notes occuring at the same time) in a list of notes, with a variable window size.
    Parameters:
        notes: a list of notes
        offset: a parameter shifting the time selected for to allow chords to be picked up
        window: a parameter allowing notes behind the current to be picked up
    Returns:
        chords: a list of lists of PrettyMIDI notes (each list of PrettyMIDI notes in the bigger list is a chord)
    """
    start_times = []
    for note in notes:
        if not (note.start in start_times):
            start_times.append(note.start)
    chords = []
    for time in start_times:
        playing_notes = []
        for note in notes:
            if note.start < time + offset and note.end >= time - window:
                song.instruments[0].notes
                playing_notes.append(note)
        chords.append(playing_notes)
    return chords

def get_note_scores(notes, 
                    octave_multiplier_on = True,
                    end_multiplier_on = True):
    """
    Generates note prominence values for a given list of notes.
    Parameters:
        notes: a list of notes
        octave_multiplier_on: a parameter that switches on/off the octave multiplier, a factor in the
                              note prominence score that reduces the score of the note the higher up in pitch it is
        end_multiplier_on: a parameter that switches on/off the ending time multiplier, a factor in the
                           note prominence score that reduces the score of the note the farther away it is from the last note
    Returns:
        note_scores_octave_agn_dict: an octave-agnostic dictionary of the note pitch classes mapped to their prominence scores
        last_end: the ending time of the last note in notes
        first_start: the starting time of the first note in notes
        overall_dur: the overall duration of the song
    """
    note_scores_octave_agn = []
    note_scores_octave_agn_dict = dict()
    last_start = last_note(notes).start
    first_start = first_note(notes).start
    last_end = last_note(notes).end
    overall_dur = last_end - first_start
    overall_dur_minus_last = last_start - first_start
    for i in range(0, 12):
        note_scores_octave_agn.append(0) # Create bins for each note
    for note in notes:
        duration = note.end - note.start
        score = duration * note.velocity / 127
        octave_multiplier = 1
        end_multiplier = 1
        if octave_multiplier_on: # Reduce the score of the note the higher up in pitch it is
            octave_multiplier = max(0, 1 - (max(0, (round(note.pitch / 12) - 2) / 10000.0)))
        if end_multiplier_on and overall_dur_minus_last > 0: # Reduce the score of the note the farther away it is from the last note
            end_multiplier = (note.start - first_start) / overall_dur_minus_last
        score *= octave_multiplier
        score *= end_multiplier
        note_scores_octave_agn[note.pitch % 12] += score # Add the note scores by pitch class
    for i in range(0, 12):
        if note_scores_octave_agn[i] != 0:
            note_scores_octave_agn_dict[i] = note_scores_octave_agn[i]

    return note_scores_octave_agn_dict, overall_dur, last_end, first_start, last_start
    
# Generates chord scores based on note scores
def get_chord_scores(chord_list, 
                     note_scores_octave_agn_dict, 
                     overall_dur,
                     parentheses_multiplier = 1,
                     min_note_threshold = 0.1, 
                     missing_deweight = 0.5, 
                     root_note_multiplier = 2):
    """
    Generates chord likeliness scores for a given list of chords and an octave-agnostic note scores dictionary.
    Parameters:
        chord_list: a list of all the chords to detect, likely generated above in generate_chord_list()
        note_scores_octave_agn_dict: an octave-agnostic dictionary of the note pitch classes mapped to their prominence scores
        overall_dur: the overall duration of the song
        parentheses_multiplier: a multiplier for the chord likeliness score that scales down the weight of chord notes in
                                parentheses (because they're not required for the chord)
        min_note_threshold: the minimum score a note must have in the note scores dictionary to be counted as "being played"
        missing_deweight: a negative offset applied to each chord score, once for each missing note (threshold determined
                          by the min_note_threshold)
        root_note_multiplier: a multiplier for the chord likeliness score that multiplies the note score for any note that is
                              the root of the chord that's having its score calculated
    Returns:
        chord_scores_dict_sorted: a sorted list of tuples containing a string (the chord name) and a float (the chord score) from
                                  most likely (highest score) to least likely (lowest score)
    """
    chord_scores_dict = {}
    for chord_tuple in chord_list:
        chord_name = chord_tuple[0]
        chord_notes = chord_tuple[1]
        chord_score = 0.0
        for i in range(0, len(chord_notes)):
            note = chord_notes[i]
            multiplier = 1 # A multiplier for the note score when calculating chord matchups
            actual_note = note
            if note[0] == '(':
                multiplier = parentheses_multiplier
                actual_note = note[1 : (len(note) - 1)]
            if i == 0: # If the note is the root note, weight that pitch specifically
                multiplier *= root_note_multiplier
            note_val = chrom_notes.index(actual_note)
            note_score = note_scores_octave_agn_dict.get(note_val, 0) # Grab the actual note score
            if note_score <= min_note_threshold: # Deweight chords with missing notes
                note_score = -1 * missing_deweight
            chord_score += note_score * multiplier # Multiply by the multiplier and sum to the chord score
        if chord_score > 0.0:
            chord_scores_dict[chord_name] = chord_score
    chord_scores_dict_sorted = sorted(chord_scores_dict.items(), key=lambda x:x[1], reverse = True) # Sort the chords
                                                                                                    # by score
    return chord_scores_dict_sorted

def calculate_song_chords(song):
    """
    Makes a list of all the chords in a song using the above methods.
    Parameters:
        song: a PrettyMIDI song object
        all_chords: the chord list
    Returns:
        chord_list: a list of strings (names of chords in the song)
    """
    all_chords = generate_chord_list()
    chord_list = []
    for chord in get_chords(song.instruments[0].notes):
        note_dict, overall_dur, last_end, first_start = get_note_scores(chord)
        
        chord_scores = get_chord_scores(all_chords, note_dict, last_end)
        if chord_scores != []:
            chord = chord_scores[:1][0][0] # Grab the top detected chord for each chord event
            if chord != "":
                chord_list.append(chord)
    return chord_list

def n_grams(my_list, n):
    """
    Makes a list of all the n-grams (subsets of n consecutive elements) in a list.
    This method is used to make chord-grams for NN classification.
    Parameters:
        my_list: a list
        n: a parameter representing how many elements are in each n-gram (hence the name)
    Returns:
        items: a list of all the n-grams in my_list
    """
    items = []
    for i in range(0, len(my_list) - n):
        n_gram = []
        for j in range(i, i + n):
            n_gram.append(my_list[j])
        items.append(n_gram)
    return items

def chord_changes(chord_list, song):
    """
    Returns the number of chord changes per second on average of a song.
    Parameters:
        chord_list: a list of strings (the chords in the song)
        song: the PrettyMIDI song object corresponding to chord_list
    Returns:
        chord_changes_per_time: the number of chord changes per second on average of song
    """
    notes = song.instruments[0].notes
    duration = last_note(notes).end - first_note(notes).start
    chord_changes_per_time = (len(chord_list) - 1) / duration
    return chord_changes_per_time