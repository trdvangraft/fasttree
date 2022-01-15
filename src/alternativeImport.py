def readAll(file_name):
    sequences = []
    f = open(file_name, "r")
    (k) = f.readline().removesuffix("\n")

    k = int(k)

    sequences = []
    name = ""
    currentSequence = ""
    for line in f:
        line = line.removesuffix("\n")
        if not line:
            print("End Of File")
            break

        if ">" in line:
            #new sequence
            sequences.append({name:currentSequence})
            name = line.strip(">")
        else:
            currentSequence += line

    f.close()

    return sequences[1:]
