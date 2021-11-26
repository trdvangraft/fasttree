import numpy as np
import pandas as pd

from Bio import AlignIO


def read_atl(file_name):
    format = "fasta"
    return AlignIO.read(file_name, format)


if __name__ == "__main__":
    print(read_atl("data/test-small.aln"))
