Antibody (Ab) plays critical roles in both therapeutic and diagnostic applications. Though antibody engineering has enabled high yield of antigen-specific Ab binders, further identification of functional ones, which are often relevant to conformational epitopes, remains a time and cost-intensive endeavor.

Here, we proposed an in-silico tool, SESA, to screen those Abs targeting a pre-defined epitope area by calculating the physio-chemical complementarity between epitopes and paratope pairs.

We also provide a web-based version of SESA for user convenience.

Configuration Instructions:
	
	SESA requires no compilation or installation; simply execute the script file with Python 3 to run it in full. The required dependency packages are listed in the requirements.txt file and as follows:

		scikit-learn==0.24.1
		numpy==1.20.1
		scipy==1.6.2
		pandas==1.2.4
		joblib==1.0.1

	For antibody sequence input, SESA relies on ANARCI for antibody IMGT numbering. Please install and configure ANARCI in your environment. See https://github.com/oxpig/ANARCI. The easiest way to install ANARCI and its dependencies is using conda.

		conda install -c conda-forge biopython -y
		conda install -c bioconda hmmer=3.3.2 -y
		cd ANARCI
		python setup.py install

Usage:

	INPUT:

		antigen: Please provide the PDB structure of the target antigen you wish to inquire about and the residue numbers (resi) of the target epitope.

		antibody: There are three input formats for antibodies, which are as follows:
		 1. Built-in non-redundant antibody structure library (n=2,867).
		 2. User-defined antibody CDR structure library in mutual format (.pdb format, compressed into .zip format, see example_data).
		 3. User-defined antibody sequence library (see example_data).

	OUTPUT:

		SESA Score: The binding likelihood scores (ranging from 0 to 1) of these antibodies to the epitope, along with the corresponding ranking of the antibodies.

RUN SESA:

	To ensure the successful operation of SESA, users are required to install and configure the ANARCI tool in advance and add it to the system path.

	For the three different antibody library inputs mentioned above, users only need to execute the corresponding Python script located in the scripts folder:

	1. 0_main_sub1.py
	2. 0_main_sub2.py
	3. 0_main_sub3.py
	
	The test cases are provided in the "example_data" folder, with an expected total runtime of less than 5 minutes on a standard desktop computer.

Training Code of SESA:
	
	The code files for model training and testing are provided in the "SESA_training" folder, with an expected total runtime of less than 30 minutes on a standard desktop computer. To ensure the traceability of intermediate files, please execute each step's ".py" script in sequence according to the folder order.
	
	Note that the CE-blast algorithm was used during the training process (see Qiu, T., Yang, Y., Qiu, J. et al. CE-BLAST makes it possible to compute antigenic similarity for newly emerging pathogens. Nat Commun 9, 1772 (2018). https://doi.org/10.1038/s41467-018-04171-2). The code has been included in the "CEBLAST" file under the corresponding subpath, and this code needs to be executed in a Python2 environment. Please configure a Python2 environment for this purpose (Python 2.7 is recommended, with numpy 1.16.5 required). The code for configuring this environment is as follows:
	
		conda create -n CEBlast python=2.7 numpy=1.16.5 -y
		conda activate CEBlast

Soure data and code:
	
	The code for data processing and plotting in the SESA paper is located in the "source_data" folder, with detailed annotations and execution instructions.

Notice:
	
	If there is a need for commercial use, please contact the email: zwcao@fudan.edu.cn.
