from distutils.command.config import config
from importlib.metadata import metadata
from brownie import *
import time

def get_hash(path):                                                             #this function allows us to get the metadata hash, it works
    fp = open(path,"r")                                                         #in the same way as in the metadataUpdate script.
    text = []
    for i in fp:
        text.append(i.split(' '))
    a = []
    a = text[-1].copy()
    hash = a [1]
    return hash

def main():                                             
    dev = accounts.add(config['wallets']['from_key'])                           #i create a variable dev that will store the wallet of the 
                                                                                #user that is using this program.
    j_hash = get_hash("./strg/jsons.txt")                                       #i store the hash of the metadata files.
    uri = "https://ipfs.io/ipfs/"+ j_hash +"/"                                  #i create the uri with the ipfs link format.
    contract = NFTContract[len(NFTContract) - 1]                                #i store the last contract that has been deployed.
    print("the active network is: " + network.show_active())                    #i print the network where the program is running the test
    contract.setUriPrefix(uri,{"from":dev})                                     #i set the uri prefix variable of the contract.