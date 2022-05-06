##################################################################################
					REQUIREMENTS
##################################################################################
For execute the program you must have the following libraries avaiable:
ctypes.wintypes
image_slicer
random
PIL
datetime
##################################################################################
All the layers must be in separate directories where each part has always the same name and a progressive number, like hair1, hair2, hair3 and so on.
all the lements of all the layers must be in .png format.
##################################################################################
				INSTRUCTION FOR THE USE
##################################################################################
IMPORTANT, THE paths.txt FILE MUST BE IN THE SAME DIRECTORY AS GenerativeArt1.2.py

The structure of the paths.txt has to be the following:
The first line is the destination path where the NFTs are gonna be saved.
the second line is the number of layers your image has, including the base image.
The third number is the number of NFTs you want to create.
The following lines must be structured as it follows:
The path of the first directory where you'll contain the elements of the layers.
The line right after that has to be the number of the elements in that layer.
Each folder must have all the elements named as follows:
elementn.png, where n is the number of each element, which goes from 1 to the number SPECIFIED after the layer's directory.
an example path would be: NFT\hair\hair
let's suppose now we have 6 elements inside the layer hair, we must have in that 
folder six elements: hair1, hair2, hair3, hair4, hair5, hair6
pay attentions that the second hair in the path above is about the plain name of our elements in the layer folder.
the line before the las must be the path where you want to save your new metadata.
the last line must be g, it is a terminator symbol. When the program finds that symbol, it stops searching for paths.
The repository includes some tastecases and generates 216 NFTs that are gonna be unique.

In case the number of NFTs required is gonna be more than all the possible combinations, they are gonna be generated only all the possible combination, so that doubles are not gonna be generated.

After the paths.txt has been created, you just have to launch the program with the instrunction "python GenerativeArt1.2.py".
#################################################################################
PATHS.TXT EXAMPLE:
#################################################################################
Results\
4
216
NFT\pace\pace1.png
1
NFT\hair\hair
6
NFT\eyes\eyes
6
NFT\mouth\mouth
6
\metadata
g
#################################################################################
The program also prints a log of all the iterations executed for generating our NFTs. I prints the specific iteration in which the n-th NFT has been generated.
At the end of the log file it's also reported the execution time for generating all the NFTs.
#################################################################################
For the generation of the metadata files, a new file txt is necessary. It has to be called fiel_values and it has to have the following formatting:
-the number of lines must be the same as the number of layers.
-each line must start with zero and it has to be followed by the same number of elements of each layer.
-the order of the lines must be identical to the order of the layers in the paths.txt file.
-each value after the zero must be divided by a single space.
-the first line must have the name of the fields you intend to give to your NFT, without considering the image field.
-each one of the values can be and integer or a character or a string.
Here is an example of a field_values.txt:
0 name ritual mask robe
0 a b c d e f g h i l
0 1 2 3 4 5 6 7 8 9 10
0 1 2 3 4 5 6 7 8 9 10 11 12
0 1 2 3 4 5 6
#################################################################################
METADATAUPDATE INSTRUCTION
#################################################################################
The program metadataUpdate.py has to be run after the ipfs upload command of the images, otherwise it will update nothing. It's given in the folder, a c compiled file that will execute in order all the programs.
#################################################################################
BROWNIE SCRIPTS
#################################################################################
All the cripts brownie have a purpose, the deploy one sets automatically the contract in unpause and reveals the NFTs. In case you want to delay the reveal, you can delete the revealing line in the deploy.py script, and set the revealing afterwards by using the reveal.py script. Other scripts are given, such as setTokenUri.py, which will set automatically the uri of the NFTs that have been uploaded while executing the myexe file. 
As a last script, there is the tokenUri script, which allows the user to see which one is the uri of the token the user inputs.
##################################################################################
BROWNIE TESTS
##################################################################################
There are 3 brownie tests file:
-the first one, does silly test. it just check that all the methods works as they should.
-the second one tests intensively the mintin function, for the owner account or for an another account.
-the last one tests the limit of the minting function, tries to mint all the NFTs or more, and checks if there can be NFTs that can be minted for a lower price.
##################################################################################
BROWNIE CONTRACTS
##################################################################################
The contracts are 2:
-the libraries.sol, which includes all the libraries necessary to make a contract that follows the ERC721 standard guidelines. It is from the openzeppeling github page.
-the NFTContract, is a modified version of the chep gas expense one from the hashlips github repository. Some other function has been included to test it better and to automate as much process as possible.