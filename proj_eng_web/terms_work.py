from random import randint

def get_terms_for_table():
    terms = []
    with open("./data/terms.csv", "r", encoding="utf-8") as f:
        cnt = 1
        for line in f.readlines()[1:]:
            term, translation, source = line.split(";")
            terms.append([cnt, term, translation])
            cnt += 1
    return terms


def write_term(new_term, new_translation, term_src):
    new_term_line = f"{new_term};{new_translation};{term_src}"
    with open("./data/terms.csv", "r", encoding="utf-8") as f:
        existing_terms = [l.strip("\n") for l in f.readlines()]
        title = existing_terms[0]
        old_terms = existing_terms[1:]
    terms_sorted = old_terms + [new_term_line]
    terms_sorted.sort()
    new_terms = [title] + terms_sorted
    with open("./data/terms.csv", "w", encoding="utf-8") as f:
        f.write("\n".join(new_terms))


def get_terms_stats():
    db_terms = 0
    user_terms = 0
    words_len = []
    trans_len = []
    with open("./data/terms.csv", "r", encoding="utf-8") as f:
        for line in f.readlines()[1:]:
            word, trans, added_by = line.split(";")
            words_len.append(len(word))
            trans_len.append(len(trans))
            if "db" in added_by:
                db_terms += 1
            else:
                user_terms += 1
    stats = {
        "terms_all": db_terms + user_terms,
        "terms_own": db_terms,
        "terms_added": user_terms,
        "word_letter_avg": round(sum(words_len)/len(words_len), 2),
        "trans_letter_avg": round(sum(trans_len)/len(trans_len), 2),
        "word_letter_max": max(words_len),
        "trans_letter_max": max(trans_len),
        "word_letter_min": min(words_len),
        "trans_letter_min": min(trans_len)
    }
    return stats

def get_term_to_play():
    terms = get_terms_for_table()
    index = randint(0, len(terms)-1)
    num, term, trans = terms[index]
    with open("./data/tmp", "w", encoding="utf-8") as f:
        f.write(term)
    return trans

def get_term_to_check():
    with open("./data/tmp", "r", encoding="utf-8") as f:
        for line in f.readlines():
            term = line
    return term

def write_note(note_name, note_description):
    notes = []
    with open("./data/notes.csv", "r", encoding="utf-8") as f:
        for line in f.readlines():
            id, name = line.strip("\n").split(";")
            notes.append([id, name])
        notes.append([str(int(id)+1), note_name])
    with open("./data/notes.csv", "w", encoding="utf-8") as f:
        note_lines = []
        for note in notes:
            note_lines.append(";".join(note))
        f.write('\n'.join(note_lines))
    note_file_name = f"./data/notes/note_{str(int(id)+1)}"
    with open(note_file_name, "w", encoding="utf-8") as f:
        f.write(note_description)

def get_notes_to_show():
    notes = []
    ids = []
    with open("./data/notes.csv", "r", encoding="utf-8") as f:
        for line in f.readlines():
            id, name = line.strip("\n").split(";")
            notes.append([id, name])
            ids.append(int(id))
    for id in ids:
        with open(f"./data/notes/note_{id}", "r", encoding="utf-8") as f:
            notes[id-1].append([l.strip('\n') for l in f.readlines()])
    print(notes)
    return notes
