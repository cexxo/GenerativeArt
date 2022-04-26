from ctypes.wintypes import RGB
import image_slicer as sl
import random
from PIL import Image
import datetime
import sample_metadata as sm
import json, pathlib, requests

#ipfs.io/ipfs/QmZqRmpFHtN7vNkEJr2JrjYAuWXHJG3Nb2muC8EPWtWhsa?filenamest-bernard.png address example on ipfs
#ipfs.io/ipfs/QmZqRmpFHtN7vNkEJr2JrjYAuWXHJG3Nb2muC8EPWtWhsa?filenamest-bernard.png
###############################################################################################################################################
names = ['','a','b','c','d','e','f','g','h','i','l']
rituals = [0,1,2,3,4,5,6,7,8,9,10]
masks = [0,1,2,3,4,5,6,7,8,9,10,11,12]
robes = [0,1,2,3,4,5,6]
meta = ["","name","ritual","mask","robe"]
###############################################################################################################################################
def get_meta(string):                                                       #this function allows us to return one of the arrays that will                   
    if string == "name":                                                    #store all the names and charatteristic of our NFTs.
        return names                                                        #according to the string that is gonna be passed as an argument
    elif string == "ritual":                                                #the fuction will decide wich array it should be returned.
        return rituals                                                      #it needs still a bit more of attentio, but for now it works.
    elif string == "mask":                                                  #with 10 NFTs there are no proble. Let's try 500..
        return masks                                                        
    elif string == "robe":                                                  
        return robes                                                        

def upload_to_ipfs(filepath):
    with pathlib.Path(filepath).open("rb") as fp:
        image_binary = fp.read()
        ipfs_url = "http://127.0.0.1:5001"
        response = requests.post(ipfs_url + "/api/v0/add", files={"file": image_binary})
        ipfs_hash = response.json()["Hash"]
        return ipfs_hash

#this function takes care on the conversion of images with a background which is white instead of transparent
def convertImage(path):                                                     #it accept a varible path that is the path to the image i'll work on
    img = Image.open(path)                                                  #i open the image according to the path that was given
    img = img.convert("RGBA")                                               #i convert the image in an image RGBA so that i can controll the
                                                                            # images levels
    datas = img.getdata()                                                   #i get the layer datas of the images, the quantity of red, blue
                                                                            # and yellow. it is expressed as (R,G,B)
    newData = []                                                            #i create an array so that i can store the new RGB's data
                                                                            
    for items in datas:                                                     #i iterate the components of each RGB tuples
        if items[0] == 255 and items[1] == 255 and items[2] == 255:         #if i found that each component of a tuple is 255, i've found the
            newData.append((255, 255, 255, 0))                              #white color, so i convert it into a transparent component
        else:                                                               
            newData.append(items)                                           #othrwise i leave the tuple without modifications
                                                                            
    img.putdata(newData)                                                    #i substitute the old data of the pictures witht the new ones
    img.save(path)                                                          #i save the image in the same path as the old one. i'm overwriting it

#this function is a path cleaner function, which allows us to avoid unpleasent errors :)
def pathManipulation(s):                                                    #with this function i clean the paths in input.
    temp = ""                                                               #due to python's way of interpreting inputs, it is necessary to
    for i in range(len(s)):                                                 #remove the double / from the paths, otherwise the program 
        if s[i] == "//" and s[i+1] == "//":                                 #doesn't work due to errors in finding the necessary files
            continue                                                        #it's a really simple algorith, it replaces // with /
        elif s[i] == "\n":                                                  #it allows to remove the new line character so that the paths
            temp = temp + ""                                                #read from the file will be processed correctly
            break
        temp = temp + s[i]                                                  
    s = temp
    return s

def main():
    try:
        uri = open("ERC721/uri.txt","w")
    except:
        print("something went wrong with generating the uri file...")
    try:
        log = open("log.txt","w")                                           #here is where i'm gonna store all the iterations that generated 
    except:                                                                 #succesfully a unique NFT.
        print("something went wrong with generating the log file")          
    try:
        my_file = open("paths.txt","r")                                     #open the file where i have the parameters i need
    except:
        print("paths.txt non found... check if it is in the same directory")#error message in case the file paths.txt wasn't opened
    try:
        destination = my_file.readline()                                    #try to read the path where i'll store my NFTs
        destination = pathManipulation(destination)                         #clean the path file so that there should be no problem
    except:
        print("the destination path(first line of paths) is uncorrect...")  #error message in case the first line of the file is not a path
    try:
        nLayers = int(my_file.readline())                                   #the second value that you read is the number of layers in the NFT
    except:
        print("the second line of pahts.txt is not a number...")            #error message in case the second line of the file is not a number
    try:
        num_NFT = int(my_file.readline())                                   #the third number is the number of NFTs the user wants to create
    except:
        print("the third line of paths.txt is not a number...")             #error message in case the third line of the file is not a number
    
    Layer = []                                                              #i create an array where i will store my layers
    paths = []                                                              #i create an array where i'll store the path of the i-th layer
    randoms = []                                                            #i'll memorize the random values of each layer here. this number
                                                                            #will determine which element of the layer we'll use.
    pattern = []                                                            #i will store the combinations of each possible NFT so that i won't
                                                                            #have any duplicate.
    nElements = []                                                          #in this array i will store the number of elements each layer has.
    combinations = 1                                                        #here is where i'll store the maximum number of unique NFTs i can 
                                                                            #create
    count = 0                                                               #it will store the number of NFT produced succesfully.
    iterations = 0                                                          #it will store the number of iterations the program does.
    temp_meta = []
    try:                                                                        
        for i in range(nLayers):                                            #i save the n paths i will use for the generation of the NFTs
            temp = my_file.readline()                                       #i read the next n lines so that i can store the paths           
            try:                                                            #each path is followed by a number, which is the number of elements
                read = int(my_file.readline())                              #for that specific layer.
                nElements.append(read)                                      #the number of combinations is given by the multiplication of each
                combinations = combinations*read                            #layer's element with all the other layers' elements.
            except:
                print("the line you are reading is not a number...")        #error message in case the line cannot be converted to a number
            if temp != "g":                                                 #if i do not find the terminator characte
                paths.append(pathManipulation(temp))                        #i can add the path to the list
            else:                                                           #otherwise stop reading the lines
                break
    except:
        print("something went worng with the line reading...")              #errror message in case the readline() found something unusual
    try:
        metadata_save= my_file.readline()
        pathManipulation(metadata_save)
    except:
        print("something went wrong with the metadata path...")

    if num_NFT > combinations:                                              #i check that the number of NFTs required is lower than all the
        num_NFT = combinations                                              #possible combinations, if not i notify it to the user
        print("the number of NFTs has been decreased to the maximum number of combinations...")

    base = paths[0]                                                         #the base image of our NFT is always stored in path 0     
    begin = datetime.datetime.now().timestamp()                             #i store the time then the generating process starts
    while len(pattern) < num_NFT :                                          #this is the whole cycle that generates our NFTs
        iterations = iterations + 1
###############################################################################################################################################
        collectible_metadata = sm.metadata_template
        metadata_file_name = (str(pathlib.Path(metadata_save)) + str(count+1) + ".json")
        print("Creating Metadata File {}".format(metadata_file_name))
###############################################################################################################################################
        randoms.append(0)
        for k in range(1,nLayers):                                          # generate the random numbers for choosing the element i want in
            temp_rand = random.randint(1,nElements[k])
            randoms.append(temp_rand)                                       # my NFT.
            temp_meta = get_meta(meta[k])
            collectible_metadata[meta[k]] = temp_meta[temp_rand]
        if randoms in pattern:                                              #in this iteration cycle i check if a combination of layers has 
            randoms.clear()                                                 #already been used. if that's so, skip the iteration and calculate
            continue                                                        #again the random numbers.
        else:                                                               #otherwise, save the new pattern and increment the couns of the 
            pattern.append(randoms.copy())                                  #iterations done succesfully.
            count = count + 1                                       
        pathManipulation(base)                                              #i clean the path of the base so the process is without issues
        Layer.append(base)                                                  #I add the base image to the Layers
        try:                                                                #here we fill our layer array so that we can use the final path
            for j in range(1,nLayers):                                      #to directly access to the elements of our NFT.
                temp = paths[j] + str(randoms[j]) + ".png"                  #i create the final path of the random element of the j-th layer
                s = pathManipulation(temp)                                  #i clean the path the user put in the command-line
                convertImage(s)                                             #i convert the image so that each single picture has a transparent
                                                                            #background
                Layer.append(s)                                             #that stores the path of the j-th element of the layer
                temp = ""                                                   #i clean the temporari path so that i can create a new one for the
                                                                            #next element of our NFT.
        except:
            print("problem with paths generation...")                       #a generic error for now, gonna be more specific on next versions
        ##The paste function accepts 3 paramethers: the image to paste on our background image, the position (x,y coordinates) where the selected
        # image has to be pasted, the mask layer. I use the second image as mask layer so that i ensure that only the non trasparent part
        # is gonna be merged with our background. For more specifics read the pillow documentation. 
        try:
            baseImage = Image.open(Layer[0])                                #the baseImage is the image that is gonna give us the final result
        except:
            print("error in opening the baseImage file...")                 #error message in case there is a problem in opening the baseImage
        for k in range(1,nLayers):                                          #in layer 0 there should always be tha background image.
            try:
                temp = Image.open(Layer[k])                                 #i open the image of the k-th layer and store it in a temp variable.
                baseImage.paste(temp,(0,0),temp)                            #i'm gonna paste each of the layers to the baseImage so that in the
            except:                                                         #end i will have the complete NFT.
                print("error in opening the {}-th file...".format(k))       #error message in case there is a problem in opening one of the files       
        baseImage.save("{}{}.png".format(destination,count),"PNG")          #I save the image as the i-th result of our production process.
        log.write(f"the {count} NFT has been generate at the {iterations}-th iteration\n")#i write on the log file the n-th iteration on which
                                                                            #the new NFT has been generated.
        randoms.clear()                                                     #I clean the 2 arrayw where i store the definive paths and components.
        Layer.clear()                                                       
        collectible_metadata["description"] = "An {} shaman".format(collectible_metadata["ritual"])
        image_path = f"./Results/{count}.png"
        collectible_metadata["dna"] = upload_to_ipfs(image_path)
        collectible_metadata["image"] = "https://ipfs.io/ipfs/"+collectible_metadata["dna"]+"?filename" + str(count) +".png"
        print(collectible_metadata["image"])
        with open(metadata_file_name, "w") as file:
            json.dump(collectible_metadata,file)
        meta_hash = upload_to_ipfs(metadata_file_name)
        temp_uri = "https://ipfs.io/ipfs/"+meta_hash+"?filename" + str(count) +".json"
        print(temp_uri)
        uri.write(temp_uri + "\n")
    end = datetime.datetime.now().timestamp()                               #i store the time the program stops generating NFTs
    log.write(f"The total generating time is: {int(end-begin)} secondi")    #i write on the file the execution time in seconds to generate all
                                                                            #the NFTs.

if __name__ == '__main__':
    main()