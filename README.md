# SESA: Screening Epitope-Specific Antibodies

Antibody (Ab) plays critical roles in both therapeutic and diagnostic applications. Though antibody engineering has enabled high yield of antigen-specific Ab binders, further identification of functional ones, which are often relevant to conformational epitopes, remains a time and cost-intensive endeavor.

Here, we proposed an in-silico tool, SESA, to screen those Abs targeting a pre-defined epitope area by calculating the physio-chemical complementarity between epitopes and paratope pairs.



## Configuration Instructions

Note: To ensure the proper functioning of ANARCI and SESA, we recommend running SESA in a Linux/macOS environment. It is recommended to create an isolated environment using conda with the following command:

```bash
conda create -n sesa python=3.8.20 -y
```

Then, activate the environment using:

```bash
conda activate sesa
```

The required dependency packages are listed in the requirements.txt file and can be installed using the following command:

```bash
pip install scikit-learn==0.22.1 numpy==1.23.0 scipy==1.10.1 pandas==1.2.4 joblib==1.0.1
```

For Antibody sequence input, SESA relies on ANARCI for antibody IMGT numbering. Please install and configure ANARCI in your environment. (See https://github.com/oxpig/ANARCI). The easiest way to install ANARCI and its dependencies is using conda:

```bash
conda install -c conda-forge biopython -y
conda install -c bioconda hmmer=3.3.2 -y
cd ANARCI
python setup.py install
```



## Usage

**INPUT:**

**Antigen:** 

Please provide the PDB structure of the target antigen, with antigen chain and the residue numbers (resi) of the target epitope.



**Antibody (3 Modes):**

Mode 1: Built-in non-redundant antibody structure library (n=2,867).

Mode 2: User-defined antibody CDR structure library (.pdb format, compressed into a .zip file).

Mode 3: User-defined antibody sequence library (.fasta format).



**OUTPUT:**

A .tsv or .csv file specified by the user via the -o argument. It contains the binding likelihood scores (ranging from 0 to 1) and the corresponding ranking of the antibodies.



**Example Commands:**

We provide sample files in the exmaple_data directory. You can test the three modes using the following commands from the project root directory. The expected total runtime is less than 5 minutes on a standard desktop computer.

1. Screen against the built-in non-redundant antibody structure library (Mode 1):

```bash
python SESA.py -m 1 -ag './exmaple_data/exmaple1/2NXZ.pdb' -c 'A' -s '119,120,122,200,202,203,419,421,422,423,434,437' --host 'Unspecified' -o './result_mode1.tsv'
```

2. Screen against a user-defined antibody CDR structure library (Mode 2):

```bash
python SESA.py -m 2 -ag './exmaple_data/exmaple2/2NXZ.pdb' -c 'A' -s '119,120,122,200,202,203,419,421,422,423,434,437' --ab_zip './exmaple_data/exmaple2/test.zip' --host 'Unspecified' -o './result_mode2.tsv'
```

3. Screen against a user-defined antibody sequence library (Mode 3):

```bash
python SESA.py -m 3 -ag './exmaple_data/exmaple3/2NXZ.pdb' -c 'A' -s '119,120,122,200,202,203,419,421,422,423,434,437' --heavy './exmaple_data/exmaple3/test_heavy.fasta' --light './exmaple_data/exmaple3/test_light.fasta' --host 'Unspecified' -o './result_mode3.tsv'
```



**Command-line Arguments Explanation:**	

```bash
	-ag, --antigen : The path to your antigen .pdb file.
	-c, --chain    : The epitope chain name of your antigen pdb file, choose from ('A'-'Z', 'a'-'z', '0'-'9').
	-s, --sites    : The comma-separated epitope resi, e.g. '119,120,122...'.
	-m, --mode     : Execution mode. 1 (Built-in lib), 2 (Custom structure zip), 3 (Custom sequences fasta).
	-o, --output   : [Required] The path and filename to save the final ranking result (e.g., ./output/my_result.tsv).
	--host         : Immune host. Choose from: (Homo, Mus, and Unspecified). Decides which SESA sub-model to use.
	--ab_zip       : The path to your CDR structure .zip file (Required for Mode 2).
	--heavy        : The path to your antibody heavy chain .fasta sequence file (Required for Mode 3).
	--light        : The path to your antibody light chain .fasta sequence file (Required for Mode 3).
```



## Training Code of SESA

The code files for model training and testing are provided in the "SESA_training" folder, with an expected total runtime of less than 30 minutes on a standard desktop computer. To ensure the traceability of intermediate files, please execute each step's ".py" script in sequence according to the folder order.

Note that the CE-blast algorithm was used during the training process (see Qiu, T., Yang, Y., Qiu, J. et al. CE-BLAST makes it possible to compute antigenic similarity for newly emerging pathogens. Nat Commun 9, 1772 (2018). https://doi.org/10.1038/s41467-018-04171-2). The code has been included in the "CEBLAST" file under the corresponding subpath, and this code needs to be executed in a Python2 environment. Please configure a Python2 environment for this purpose (Python 2.7 is recommended, with numpy 1.16.5 required). The code for configuring this environment is as follows:

```bash
conda create -n CEBlastenv python=2.7 numpy=1.16.5 -y
conda activate CEBlastenv
```



## Soure data and code

The code for data processing and plotting in the SESA paper is located in the "source_data" folder, with detailed annotations and execution instructions.



## Notice

If there is a need for commercial use, please contact the email: zwcao@fudan.edu.cn. For the convenience of users, we also provide a web-based version of SESA, which is accessible via the URL: https://www.badd-cao.net/sesa/