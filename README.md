Created by Yuan Wang (Email: 1911013@tongji.edu.cn)

Antibody (Ab) plays critical roles in both therapeutic and diagnostic applications. Though antibody engineering has enabled high yield of antigen-specific Ab binders, further identification of functional ones, which are often relevant to conformational epitopes, remains a time and cost-intensive endeavor.

Here, we proposed an in-silico tool, SESA, to screen those Abs targeting a pre-defined epitope area by calculating the physio-chemical complementarity between epitopes and paratope pairs.

INPUT:

antigen: Please provide the PDB structure of the target antigen you wish to inquire about and the residue numbers (resi) of the target epitope.

antibody: There are three input formats for antibodies, which are as follows:
 1. Built-in non-redundant antibody structure library (n=2,867).
 2. User-defined antibody CDR structure library in mutual format (.pdb format, compressed into .zip format, see example_data).
 3. User-defined antibody sequence library (see example_data).

OUTPUT:

SESA Score: The binding likelihood scores (ranging from 0 to 1) of these antibodies to the epitope, along with the corresponding ranking of the antibodies.

RUN:

To ensure the successful operation of SESA, users are required to install and configure the ANARCI tool in advance and add it to the system path.

For the three different antibody library inputs mentioned above, users only need to execute the corresponding Python script located in the scripts folder:

1. 0_main_sub1.py
2. 0_main_sub2.py
3. 0_main_sub3.py

Notice:
If there is a need for commercial use, please contact the email: zwcao@fudan.edu.cn.
