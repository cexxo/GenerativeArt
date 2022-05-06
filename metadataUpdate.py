import json

def get_hash(path):                                                         #this function allows us to get the hash generated from the ipfs
    fp = open(path,"r")                                                     #upload of the images. I open the file specified in the path,
    text = []                                                               #and i create a varaible text tha will memorize the whole text.
    for i in fp:                                                            #for each line in the file, i store all the words by splitting them
        text.append(i.split(' '))                                           #every space.
    a = []                                                                  #In this temporary array i will sotre the last list in the text 
    a = text[-1].copy()                                                     #array, cause it is the one with the clean hash that we need.
    hash = a [1]                                                            #the hash is always the second word that comes in that line, so
    return hash                                                             #i store it in a variable called hash and i return it.


def meta_update(i_hash,metadata_file_name,count):                           #this function allows us to update the metadata file of our NFTS.
    b = open(metadata_file_name,"r")                                        #it opens the file json we need and load the whole content in the 
    a = json.load(b)                                                        #variable a.
    value = str("https://ipfs.io/ipfs/"+ i_hash +"/" + str(count) +".png")  #the value we want to store has the ipfs link format. Once we create
    a["image"] = value                                                      #it, we'll store it in the image field of the json file.
    with open(metadata_file_name, "w") as file:                             #i open the metadata file of the NFT on which we are working on, and 
        json.dump(a,file)                                                   #i update the image field.

def main():                                                                 
    metadata_save = "ERC721/metadata/"                                      #i store the pathe were the metadata have been saved, and i open the 
    temp = open("./ERC721/max_mint.txt","r")                                #max_mint file, which will tell me how many metadata file has been 
    max = int(temp.readline().strip())                                      #generated. I store the value read in the max variable.
    i_hash = get_hash("./ERC721/strg/images.txt")                           #the i_hash, will store the hash returned by the get_hash function.
    for i in range(max):                                                    #for all the json file that have been generated, i update the file name
        metadata_file_name = (metadata_save + str(i+1) + ".json")           #variable, the update it's metadata thorugh the meta_update function 
        meta_update(i_hash,metadata_file_name,i+1)                          #defined earlier.

if __name__ == "__main__":
    main()