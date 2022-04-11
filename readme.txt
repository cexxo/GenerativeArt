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
IMPORTANT, THE paths.txt FILE MUST BE IN THE SAME DIRECTORY AS GenerativeArt1.4.py

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
the last line must be g, it is a terminator symbol. When the program finds that symbol, it stops searching for paths.
The repository includes some tastecases and generates 216 NFTs that are gonna be unique.

In case the number of NFTs required is gonna be more than all the possible combinations, they are gonna be generated only all the possible combination, so that doubles are not gonna be generated.

After the paths.txt has been created, you just have to launch the program with the instrunction "python GenerativeArt1.4.py".
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
g
#################################################################################
The program also prints a log of all the iterations executed for generating our NFTs. I prints the specific iteration in which the n-th NFT has been generated.
At the end of the log file it's also reported the execution time for generating all the NFTs.
#################################################################################