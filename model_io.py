def read_from_file(filename):
    clues = []
    for line in filename:
        clues.append(line.strip().split())
    return clues
