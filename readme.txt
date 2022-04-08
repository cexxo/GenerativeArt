IMPORTANT, THE paths.txt FILE MUST BE IN THE SAME DIRECTORY AS slicer1.2.py

the first line is the number of layers your image has, including the base image.
the second line is the number of element each layer can choose from.
the third number is the number of NFTs you want to create.
the number of following lines must equal the first number of the file. Each one
of these lines is the specific file path of each layer folder. it has to stop
at the base name of each element.
Each folder must have all the elements named as follows:
element_n.png
where n is the number of each element, which goes from 1 to the number put in input at the second line.
an example path would be: NFT\hair\hair
let's suppose now we have 6 elements inside the layer hair, we must have in that 
folder six elements: hair_1, hair_2, hair_3, hair_4, hair_5, hair_6
pay attentions that the second hair in the path above is about the plain name of our elements in the layer folder.
the last line must be g, it is a terminator symbol. When the program finds that symbol, it stops searching for paths.