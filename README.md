# Fasttree python implementation

Fasttree is an algorithm that can be used to create a Phylogenetic tree from just a dataset of genomes.
It is specically designed to run faster than the standard nearest neighbor algorithm, which has trouble to create a Phylogentic tree for large genome datasets.

Our implementation of the algorithm is based on the first version of the [paper](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2693737/) that describes it. We tried to stay as close as possible to the original implementation, but had to deviate from the implementation as implementation details were not often clear.

## **Setup**
We have designed the python implementation with easy of use in mind, after running the requiremetns file with ```pip install -r requirements.txt``` the algorithm is ready to be used. The python version should be greater than `3.10`

The algorithm can be used via by just running 
```
python main.py [-h] [--input INPUT] [--num NUM] [--output_img OUTPUT_IMG] [--output_nwk OUTPUT_NWK]
options:
  -h, --help            show this help message and exit
  --input INPUT         Input sequences
  --num NUM             number of sequences, used for large files
  --output_img OUTPUT_IMG
                        path to save the output fasttree image
  --output_nwk OUTPUT_NWK
                        path to save the output fasttree file in newick format
```

## **Datasets**
A few different datasets are included in this repository, which can be found in the data folder. They considerably differ in length. The visualization at the bottom of the readme is based on the `fasttree-input.aln` file and is proven to be a correct Phylogenetic tree validating this algorithm. 

## **The algorithm**

### **Parsing data**
By default `.aln` files are supported and can readily be parsed, we extended the algorithm to also support `.fna` files to support a boarder range of datasets. 

### **Neighborjoining**
Neighbor joining is where the biggest difference can be found between the classic neighbor joining algorithm and the fasttree algorithm. Namely fasttree will make use of profiles instead of raw distance calculation, which are being used in the standard neigbor joining algorithms. 

The added benefit of using dna profiles is that it gives a probalistic insight in how likely a certain nucleotide can be located at a certain location.

### **NNI**
Nearest neighbor interchange (NNI) is a tree rearrange to find a more optimal tree layout. It is often used to identify the tree that best explains the evolutionary history of a specie among a large amount of trees.

During the tree rearrange phase of the algorithm for a binary Phylogentic tree, two cases can happen. 
- The first case is where it discovers four different subtrees, it will then calculate the distance between each different combination of subtrees with the help of the log corrected profile distance.
- The second case is where it discoveres only tree subtrees, this mostly happens when the discoverer is close to the leaf nodes. It still has the compare the same number of subtrees, but has to choose how to rearrange them in an orderly manner. 

### **Local bootstrapping**
Local bootstrapping helps with validating a certain split decision, the split is recalculated N times with differently sampled values, giving and accurate value for the likelihood of a certain split happening.

## **Results**
The final Phylogentic tree that was calculated on the sample dataset with our implementation is given below, it shows the branch distance from each internal node (a common ancestor) to a leaf. Note that the circular tree generation is not actually implemented in the code but can easily be achieved while using the newick format, which is generated in the results forled.
![Final phylogentic tree](./images/final_tree.svg)