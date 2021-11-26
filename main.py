from itertools import product


def count_v2(motifs, k):
    count = {nucleotide: [1]*k for nucleotide in "ACTG"}
    for i, j in product(range(len(motifs)), range(k)):
        count[motifs[i][j]][j] += 1
    return count


def read_atl(file_name):
    with open(file_name) as f:
        lines = f.readlines()
        return {lines[i].strip(">").strip("\n"): lines[i+1].strip("\n") for i in range(0, len(lines), 2)}


if __name__ == "__main__":
    print(read_atl("data/fasttree-input.aln"))
