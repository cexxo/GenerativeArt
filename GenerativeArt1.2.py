import random
from ctypes.wintypes import RGB
import image_slicer as sl
import random
from PIL import Image
import datetime
import sample_metadata as sm
import json, pathlib, requests

#ipfs.io/ipfs/QmZqRmpFHtN7vNkEJr2JrjYAuWXHJG3Nb2muC8EPWtWhsa?filenamest-bernard.png address example on ipfs
#ipfs.io/ipfs/QmZqRmpFHtN7vNkEJr2JrjYAuWXHJG3Nb2muC8EPWtWhsa?filenamest-bernard.png

def set_meta_dict(filepath):                                                #this function allows us to set the metadata list.
    d = []                                                                  #it reads the filepath of where the document is stored.
    fp = open(filepath, "r")                                                #in the first line there are the names of the field that will appear
    line1 = fp.readline().strip()                                           #in the json file. The fields are divided by a space.
    line1 = line1.split(' ')                                                #For all the lines that comes next, append a list containing the  
    for line in fp:                                                         #possible values of the fied inside of our list.
        temp = line.strip()                                                 #return in the end the final list containing all the single lists.
        temp = temp.split(' ')                                              
        d.append(temp)                                                      
    return d,line1                                                          

def get_meta(fields,p):                                                     #this function allows us to return one of the arrays that will                   
    return fields[p]                                                        #give us the value of the metadata.


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
    try:                                                                    #this file is gonna contain an integer which will tell to the 
        max_mint = open("ERC721/max_mint.txt","w")                          #minting script how many images has been generated in the end.
    except:                                                                 #If there is a problem with the generation or the opening of the
        print("something went wrong with generating the uri file...")       #file, throw an error.
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
    return max_mint,log, my_file,destination, nLayers,num_NFT

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
        metadata_save= my_file.readline().strip()                           #in case the path is wrong or not found is gonna be thrown an 
        pathManipulation(metadata_save)                                     #exception and notify the user the error.
    except:                                                                 #otherwise, it's gonna be called the path manipulation function
        print("something went wrong with the metadata path...")             #of the stored path for the metadata folder.
    return nLayers, nElements, combinations, paths, metadata_save

def limit_check(num_NFT, combinations):
    if num_NFT > combinations:                                              #i check that the number of NFTs required is lower than all the
        num_NFT = combinations                                              #possible combinations, if not i notify it to the user
        print("the number of NFTs has been decreased to the maximum number of combinations...")

def randomness(nLayers, nElements,randoms,fields,d,collectible_metadata):   #This function takes care of the random generation of the image's 
    temp_list = []                                                          #charateristics. temp_list stores temporaly the possible elements
    temp_weight = []                                                        #of the layer and temp_weight stores temporaly the weights that will
                                                                            #determines the choice of the element that will be chosen. Higher the
                                                                            #j-th weight value, higher is the chanse that the j-th element is gonna
                                                                            #be chosen over the others. Here we decided to use a quadratic function,
                                                                            #but it can be modified as it occurs.
    for k in range(1,nLayers):                                              #For all the layers of our image and for each element in the layer,
        for j in range(1,nElements[k]):                                     #we will fill the temp_list and the temp_weights as described earlier,
            temp_list.append(j)                                             #so that the first element is gonna be the least frequent one.
            temp_weight.append(j*j)                                         #i store in the temp_rand the result of the choice of that layer, and 
        temp_rand = random.choices(temp_list,temp_weight)                   # i append that specific element in the randoms array.
        randoms.append(temp_rand[0])                                        
        temp_meta = get_meta(fields,k)                                      #temp_meta is the array that will store the k-th field that we have
        list = d[k-1]                                                       #to fill in the json file, so that the value of that field is the
        collectible_metadata[temp_meta] = list[temp_rand[0]]                #one related to the image choosen for the k-th specific layer.
                                                                            #I write on the json file, in the specific field, the value just
        temp_list.clear()                                                   #found. In the end i clean the two temporary array so that they 
        temp_weight.clear()                                                 #will be ready for the next iteration.

def is_unique(randoms,pattern):                                             #This fuction determins if an element is unique or not.
        if randoms in pattern:                                              #In case the randoms array that has been generated has already been 
            return False                                                    #used it will return false.
        else:                                                               #Otherwise it will return True so that it becomes explicit that                                    
            return True                                                     #the new found sequence of values is unique.
 
def base_initialization(paths,Layer):
    base = paths[0]                                                         #the base image of our NFT is always stored in path 0
    pathManipulation(base)                                                  #i clean the path of the base so the process is without issues
    Layer.append(base)                                                      #I add the base image to the Layers
    return Layer                                                            #i return the base layer just created.

def path_generation(nLayers,paths,randoms,Layer):
    try:                                                                    #here we fill our layer array so that we can use the final path
        for j in range(1,nLayers):                                          #to directly access to the elements of our NFT.
            temp = paths[j] + str(randoms[j]) + ".png"                      #i create the final path of the random element of the j-th layer
            s = pathManipulation(temp)                                      #i clean the path the user put in the command-line
            convertImage(s)                                                 #i convert the image so that each single picture has a transparent
                                                                            #background
            Layer.append(s)                                                 #that stores the path of the j-th element of the layer
            temp = ""                                                       #i clean the temporari path so that i can create a new one for the
                                                                            #next element of our NFT.
    except:
        print("problem with paths generation...")                           #a generic error for now, gonna be more specific on next versions
    return Layer

##The paste function accepts 3 paramethers: the image to paste on our background image, the position (x,y coordinates) where the selected
# image has to be pasted, the mask layer. I use the second image as mask layer so that i ensure that only the non trasparent part
# is gonna be merged with our background. For more specifics read the pillow documentation. 
def image_generator(Layer,nLayers,destination,count):
    try:
            baseImage = Image.open(Layer[0])                                #the baseImage is the image that is gonna give us the final result
    except:
        print("error in opening the baseImage file...")                     #error message in case there is a problem in opening the baseImage
    for k in range(1,nLayers):                                              #in layer 0 there should always be tha background image.
        try:
            temp = Image.open(Layer[k])                                     #i open the image of the k-th layer and store it in a temp variable.
            baseImage.paste(temp,(0,0),temp)                                #i'm gonna paste each of the layers to the baseImage so that in the
        except:                                                             #end i will have the complete NFT.
            print("error in opening the {}-th file...".format(k))           #error message in case there is a problem in opening one of the files       
    baseImage.save("{}{}.png".format(destination,count),"PNG")              #I save the image as the i-th result of our production process.

def NFT_generator(paths,randoms,pattern,num_NFT,metadata_save,nLayers,nElements,Layer,log,destination,iterations,count,d,fields):
       
    begin = datetime.datetime.now().timestamp()                             #i store the time then the generating process starts
    while len(pattern) < num_NFT :                                          #this is the whole cycle that generates our NFTs
        iterations = iterations + 1                                         #i count the number of iterations the cycle runs to generate all the
                                                                            #NFTs.
        collectible_metadata = sm.metadata_template                         #i store in this variable the sample of our metadata files.
        metadata_file_name = (metadata_save + str(count+1) + ".json")       #i call it with the format n.json, where n is the n-th NFT generated
        randoms.append(0)                                                   #the first value of the randoms is 0 cause the first layer has only
                                                                            #the base image.
        randomness(nLayers, nElements,randoms,fields,d,collectible_metadata)#i calle the randomness function create earlier to generate the new
                                                                            #NFT. 
        if (is_unique(randoms,pattern)):                                    #i check if the new found pattern of elements is unique or not. If it 
            pattern.append(randoms.copy())                                  #is, i will add this pattern in the array patterns, i update the count
            count = count + 1                                               #of generated NFTs and i print which NFT is being generated at this
            print(f"generating the {count}-th NFT")                         #iteration.
        else:                                                               #Otherwise, i clean the random array which stores the patterns and i
            randoms.clear()                                                 #skip an iteration of the cycle.
            continue                                                        
        Layer = base_initialization(paths,Layer)                            #The array of layer has as fisrt layer the base one, generated with the
                                                                            #base initialization function defined earlier.
        Layer = path_generation(nLayers,paths,randoms,Layer)                #The next layers are gonna be added through the path_generation function.
        image_generator(Layer,nLayers,destination,count)                    #After the layer function has been generated, i generate the images
                                                                            #through the image_generator function.
        log.write(f"the {count} NFT has been generate at the {iterations}-th iteration\n")#i write on the log file the n-th iteration on which
                                                                            #the new NFT has been generated.
        randoms.clear()                                                     #I clean the 2 arrayw where i store the definive paths and components.
        Layer.clear()                                                       
        collectible_metadata["description"] = "An {} shaman".format(collectible_metadata["ritual"])#i update the description field of the NFT.
        with open(metadata_file_name, "w") as file:                         #i open the metadata file of the NFT which has been generated and i
            json.dump(collectible_metadata,file)                            #update all the values i got during the iteration.
    end = datetime.datetime.now().timestamp()                               #i store the time the program stops generating NFTs
    log.write(f"The total generating time is: {int(end-begin)} secondi")    #i write on the file the execution time in seconds to generate all
                                                                            #the NFTs.
    return collectible_metadata, metadata_file_name                         #i return the two metadata element i need, the collectilble_metadata
                                                                            #and the relative path of where they have to be stored.

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
    d,fields = set_meta_dict("field_values.txt")                            #the d list and the fields are given by the set_meta_dict function.
    max_mint,log, my_file,destination, nLayers,num_NFT = setup()                 #the first elements we need are given by setup() fuction
    nLayers, nElements, combinations, paths,metadata_save = step2(my_file,nLayers,nElements)#same with the reading of the paths.txt file thorugh
                                                                            #the step2() function.
    limit_check(num_NFT, combinations)                                      #i check that the number of NFT the user requested are less than all
                                                                            #the possible combinations.
    NFT_generator(paths,randoms,pattern,num_NFT,metadata_save,nLayers,nElements,Layer,log,destination,iterations,count,d,fields)#i generate all
                                                                            #the images.
    max_mint.write(str(num_NFT))
    max_mint.close()                                                             #i free all the resources.
    my_file.close()
    log.close()

if __name__ == '__main__':
    main()
