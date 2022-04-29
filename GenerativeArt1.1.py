from ctypes.wintypes import RGB
import image_slicer as sl
import random
from PIL import Image
import datetime
import sample_metadata as sm
import json, pathlib, requests

#ipfs.io/ipfs/QmZqRmpFHtN7vNkEJr2JrjYAuWXHJG3Nb2muC8EPWtWhsa?filenamest-bernard.png address example on ipfs
#ipfs.io/ipfs/QmZqRmpFHtN7vNkEJr2JrjYAuWXHJG3Nb2muC8EPWtWhsa?filenamest-bernard.png

def set_meta_dict(filepath):
    d = []
    fp = open(filepath, "r")
    line1 = fp.readline().strip()
    line1 = line1.split(' ')
    for line in fp:
        temp = line.strip()
        temp = temp.split(' ')
        d.append(temp)
    return d,line1

def get_meta(fields,p):                                                     #this function allows us to return one of the arrays that will                   
    return fields[p]                                               


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
def setup():
    try:                                                                    #this text file is gonna store all the uris generated from the
        uri = open("ERC721/uri.txt","w")                                    #upload of our NFTs. in case there is a problem with the generation
    except:                                                                 #of the file in the specific path then an exceptiuon is gonna be 
        print("something went wrong with generating the uri file...")       #thrown to the user.
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
    return uri,log, my_file,destination, nLayers,num_NFT

def step2(my_file,nLayers,nElements):
    paths = []
    combinations = 1
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
    try:                                                                    #I try to read the path of where i'm gonna save my metadata files.
        metadata_save= my_file.readline().strip()                                   #in case the path is wrong or not found is gonna be thrown an 
        pathManipulation(metadata_save)                                     #exception and notify the user the error.
    except:                                                                 #otherwise, it's gonna be called the path manipulation function
        print("something went wrong with the metadata path...")             #of the stored path for the metadata folder.
    return nLayers, nElements, combinations, paths, metadata_save

def limit_check(num_NFT, combinations):
    if num_NFT > combinations:                                              #i check that the number of NFTs required is lower than all the
        num_NFT = combinations                                              #possible combinations, if not i notify it to the user
        print("the number of NFTs has been decreased to the maximum number of combinations...")

def randomness(nLayers, nElements,randoms,fields,d,collectible_metadata):
    for k in range(1,nLayers):                                          # generate the random numbers for choosing the element i want in
            temp_rand = random.randint(1,nElements[k])                      # the NFT. 
            randoms.append(temp_rand)                                       #The metadata file is gonna be updated with the corresponing value
            temp_meta = get_meta(fields,k)                                  #of the element we chose for our layer.
            list = d[k-1]
            collectible_metadata[temp_meta] = list[temp_rand]               #the metadata field is gonna be updated with the value of the 
                                                                            #chosen field.
def is_unique(randoms,pattern):
        if randoms in pattern:                                              
            return False                                                    
        else:                                                                                                                             
            return True 
 
def base_initialization(paths,Layer):
    base = paths[0]                                                         #the base image of our NFT is always stored in path 0
    pathManipulation(base)                                                  #i clean the path of the base so the process is without issues
    Layer.append(base)                                                      #I add the base image to the Layers
    return Layer

def path_generation(nLayers,paths,randoms,Layer):
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
    return Layer

##The paste function accepts 3 paramethers: the image to paste on our background image, the position (x,y coordinates) where the selected
# image has to be pasted, the mask layer. I use the second image as mask layer so that i ensure that only the non trasparent part
# is gonna be merged with our background. For more specifics read the pillow documentation. 
def image_generator(Layer,nLayers,destination,count):
    try:
            baseImage = Image.open(Layer[0])                            #the baseImage is the image that is gonna give us the final result
    except:
        print("error in opening the baseImage file...")                 #error message in case there is a problem in opening the baseImage
    for k in range(1,nLayers):                                          #in layer 0 there should always be tha background image.
        try:
            temp = Image.open(Layer[k])                                 #i open the image of the k-th layer and store it in a temp variable.
            baseImage.paste(temp,(0,0),temp)                            #i'm gonna paste each of the layers to the baseImage so that in the
        except:                                                         #end i will have the complete NFT.
            print("error in opening the {}-th file...".format(k))       #error message in case there is a problem in opening one of the files       
    baseImage.save("{}{}.png".format(destination,count),"PNG")          #I save the image as the i-th result of our production process.

def NFT_generator(paths,randoms,pattern,num_NFT,metadata_save,nLayers,nElements,Layer,log,destination,iterations,count,d,fields):
       
    begin = datetime.datetime.now().timestamp()                             #i store the time then the generating process starts
    while len(pattern) < num_NFT :                                          #this is the whole cycle that generates our NFTs
        iterations = iterations + 1
        collectible_metadata = sm.metadata_template                         #i store in this variable the sample of our metadata files.
        metadata_file_name = (metadata_save + str(count+1) + ".json")#i call it with the format n.json, where n is the 
        randoms.append(0)
        randomness(nLayers, nElements,randoms,fields,d,collectible_metadata)
        if (is_unique(randoms,pattern)):
            pattern.append(randoms.copy())                                  
            count = count + 1 
            print(f"generating the {count}-th NFT")
        else:
            randoms.clear()
            continue                            
        Layer = base_initialization(paths,Layer)
        Layer = path_generation(nLayers,paths,randoms,Layer)
        image_generator(Layer,nLayers,destination,count)
        log.write(f"the {count} NFT has been generate at the {iterations}-th iteration\n")#i write on the log file the n-th iteration on which
                                                                            #the new NFT has been generated.
        randoms.clear()                                                     #I clean the 2 arrayw where i store the definive paths and components.
        Layer.clear()                                                       
        collectible_metadata["description"] = "An {} shaman".format(collectible_metadata["ritual"])#i update the description field of the NFT.
        image_path = f"./Results/{count}.png"                               #the path image is stored in the result folder and it has the name
                                                                            #n.png
        with open(metadata_file_name, "w") as file:                         #i open the metadata file of the NFT which has been generated and i
            json.dump(collectible_metadata,file)                            #update all the values i got during the iteration.
    end = datetime.datetime.now().timestamp()                               #i store the time the program stops generating NFTs
    log.write(f"The total generating time is: {int(end-begin)} secondi")    #i write on the file the execution time in seconds to generate all
                                                                            #the NFTs.
    return collectible_metadata, metadata_file_name

def main():
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
    d,fields = set_meta_dict("field_values.txt")
    uri,log, my_file,destination, nLayers,num_NFT = setup()
    nLayers, nElements, combinations, paths,metadata_save = step2(my_file,nLayers,nElements)
    limit_check(num_NFT, combinations)
    NFT_generator(paths,randoms,pattern,num_NFT,metadata_save,nLayers,nElements,Layer,log,destination,iterations,count,d,fields)
    uri.write(str(num_NFT))
    uri.close()                                                             #i free all the resources.
    my_file.close()
    log.close()




"""     collectible_metadata["dna"] = upload_to_ipfs(image_path)            #the dna field of our NFT is the hash generated from the response
                                                                            #to the IPFS upload request.
        collectible_metadata["image"] = "https://ipfs.io/ipfs/"+collectible_metadata["dna"]+"?filename" + str(count) +".png"#the image field is
                                                                            #gonna be the dna of our image combined with the sintax of IPFS uris
        print(collectible_metadata["image"])                                #i print the link i generated in the previous step.
        meta_hash = upload_to_ipfs(metadata_file_name)                      #i store the hash of the metadata file uploaded in the IPFS
        temp_uri = "https://ipfs.io/ipfs/"+meta_hash+"?filename" + str(count) +".json"#and i create the uri for that metadata file.
        print(temp_uri)                                                     #i print the uri of the metadata file that has been uploaded in this
        uri.write("https://ipfs.io/ipfs/"+meta_hash+"?filename" + "\n")     #iteration and i store it in the uris file created earlier.
"""

if __name__ == '__main__':
    main()