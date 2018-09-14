import fileManagement

mappings = fileManagement.load_note_mappings('note_mappings.csv')


def note_to_category(note, length):
    length_string = ''
    if float(length) % 1 == 0:
        length_string = "%.0f" % float(length)
    else:
        length_string = "%.1f" % float(length)
    note = ("%.0f" % float(note)) + ';' + length_string

    return mappings[note]


def category_to_note(category):
    for k in mappings:
        if mappings[k] == category:
            spl = k.split(';')
            return spl[0], spl[1]
