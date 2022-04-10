from ctypes.wintypes import RGB
import image_slicer as sl
import random
from PIL import Image

class NFT:
    def NFT(self,id_):
        id = id_

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
    for i in range(len(s)):                                                 #remove the double \ from the paths, otherwise the program 
        if s[i] == "\\" and s[i+1] == "\\":                                 #doesn't work due to errors in finding the necessary files
            continue                                                        #it's a really simple algorith, it replaces \\ with \
        elif s[i] == "\n":                                                  #it allows to remove the new line character so that the paths
            temp = temp + ""                                                #read from the file will be processed correctly
            break
        temp = temp + s[i]                                                  
    s = temp
    return s

def main():
    try:
        my_file = open("paths.txt","r")                                     #open the file where i have the parameters i need
    except:
        print("paths.txt non tound... check if it is in the same directory")#error message in case the file paths.txt wasn't opened
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
        nElements = int(my_file.readline())                                 #the third value is the number of elements that our layer has avaiable
    except:
        print("the third line of paths.txt is non a number...")             #error message in case the third line of the file is not a number
    try:
        num_NFT = int(my_file.readline())                                   #the fouth number is the number of NFTs the user wants to create
    except:
        print("the fourth line of paths.txt is not a number...")            #error message in case the fourth line of the file is not a number
    if num_NFT > nElements**(nLayers-1):                                    #i check that the number of NFTs required is lower than all the
        num_NFT = nElements**(nLayers-1)                                    #possible combinations, if not i notify it to the user
        print("the number of NFTs has been decreased to the maximum number of combinations...")
    
    Layer = []                                                              #i create an array where i will store my layers
    paths = []                                                              #i create an array where i'll store the path of the i-th layer
    randoms = []                                                            #i'll memorize the random values of each layer here. this number
                                                                            #will determine which element of the layer we'll use.
    pattern = []                                                            #i will store the combinations of each possible NFT so that i won't
                                                                            #have any duplicate.
    count = 0                                                               #it will store the number of NFT produced succesfully.
    try:                                                                        
        for i in range(nLayers):                                            #i save the n paths i will use for the generation of the NFTs
            temp = my_file.readline()                                       #i read the next n lines so that i can store the paths
            if temp != "g":                                                 #if i do not find the terminator characte
                paths.append(pathManipulation(temp))                        #i can add the path to the list
            else:                                                           #otherwise stop reading the lines
                break
    except:
        print("something went worng with the line reading...")              #errror message in case the readline() found something unusual

    base = paths[0]                                                         #the base image of our NFT is always stored in path 0     
    while len(pattern) < num_NFT :                                          #this is the whole cycle that generates our NFTs
        randoms.append(0)
        for k in range(1,nLayers):                                          # generate the random numbers for choosing the element i want in
            randoms.append(random.randint(1,nElements))                     # my NFT.

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
        baseImage.save("{}result{}.png".format(destination,count),"PNG")    #I save the image as the i-th result of our production process.
        randoms.clear()                                                     #I clean the 2 arrayw where i store the definive paths and components.
        Layer.clear()                                                       

if __name__ == '__main__':
    main()