# from itertools import product
from src.nni import nni_interchange, nni_runner
from src.TreeNode import TreeNode
from src.profile import Profile
from src.TreeCrawler import TreeCrawler
from src.visualize import Visualize
from operator import itemgetter
from collections import Counter
import math
import time
import os

def read_atl(file_name):
    with open(file_name) as f:
        lines = f.readlines()
        return {lines[i].strip(">").strip("\n"): lines[i+1].strip("\n") for i in range(0, len(lines), 2)}

def readAlternative(file_name):
    f = open(file_name, "r")
    index = 0
    sequences = []
    name = ""
    currentSequence = ""
    for line in f:
        if index % 10000000 == 0:
            print("at index: " + str(index))
        index += 1

        line = line.removesuffix("\n")
        if not line:
            print("End Of File")
            break

        if ">" in line:
            #new sequence
            if len(currentSequence) == 29903 and not ("N" in currentSequence or "S" in currentSequence or "H" in currentSequence or "W" in currentSequence or "Y" in currentSequence or "M" in currentSequence or "R" in currentSequence or "K" in currentSequence):
                sequences.append({"Name":name, "Sequence":currentSequence,"length":len(currentSequence)})
            name = line.strip(">")
            currentSequence = ""
        else:
            currentSequence += line

    f.close()

    return sequences[1:]

def writeToDataset(fileName, sequences):
    f = open(fileName, 'w')
    for sequence in sequences:
        string = ">" + sequence["Name"] + "\n" + sequence["Sequence"] + "\n"
        f.write(string)

    f.close()


def createDataset():
    sequences = readAlternative("E:\Downloads\SARS-CoV-2\\ncbi_dataset\data\\tiny-SARS-CoV-2.txt")
    writeToDataset("E:\Downloads\SARS-CoV-2\\ncbi_dataset\data\\tiny-SARS-CoV-2.txt",sequences)

def runProgram():
    # sequences = read_atl("E:\Downloads\SARS-CoV-2\\ncbi_dataset\data\\tiny-SARS-CoV-2.txt")
    sequences = read_atl('data/fasttree-input.aln')
    numnodes = 10

    root: TreeNode = TreeNode(Profile("A", "root"))
    root.m = int(math.sqrt(numnodes))

    #put nodes in a temporary array so we can limit it
    nodes = []
    for n in sequences:
        #print(n)
        # print(sequences[n])
        node = TreeNode(Profile(sequences[n], n))
        node.m = root.m
        nodes.append(node)

    print("start timer")
    start = time.time()


    nodes = nodes[:numnodes]
    for n in nodes:
        root.addNode(n)


    #
    root.generateProfileFromChildren()
    root.upDistance = root.setSelfUpDistanceFromChild()
    root.selfDistance = root.setSelfDistance()
    # print(root.profile.get_frequency_profile())
    root.calcDistances()
    print("calculated all distances")
    crawler = TreeCrawler(root)
    crawler.startMerging()
    #
    # ## ADD NNI STEP
    #
    # print(root)
    end = time.time()
    print("time elapsed:" + str(end-start))

    vis = Visualize(root)
    if not os.path.exists('./results'):
        os.mkdir('./results')
    
    vis.visualize(path="./results/first_tree.png")


if __name__ == "__main__":
    # createDataset()
    runProgram()
    print("done running")

    # sequences = sorted(sequences, key=itemgetter('length'))
    # occurences = [s["length"] for s in sequences]
    # counted = []
    # c = Counter(occurences)
    # for len in occurences:
    #     print("len" + str(len) + " appeared " + str(c[len]) +" times")
    #     counted.append({"lenth": len,"counted":c[len]})
    #
    # counted = sorted(counted, key=itemgetter('counted'),reverse=True)
    # print(counted[0:10])
    # print(Counter[occurences])


