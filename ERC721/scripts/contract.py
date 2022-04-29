from distutils.command.config import config
from importlib.metadata import metadata
from brownie import *
import time,requests, pathlib
import os  

def main():                                                
    dev = accounts.add(config['wallets']['from_key'])                           #i create a variable dev that will store the wallet of the 
                                                                                #user that is using this program.
    contract = NFTContract[len(NFTContract) - 1]                                #for each elememnt in the uris array, print the item you are
            print(uri[i] + str((i+1)) + ".json")                                #minting and it's uri on the IPFS.
            print(f"we are minting the {i+1}-th token")                         #call the mint function of that accepts the number of tokens 
            contract.mint(1,{"from":dev,"value":50*10**15})                     #you want to mint and the value you have to pay.
            time.sleep(120)                                                     #wait 2 minutes befor the next mint. After if finishes, print
    #print(f"The NFTs are revealed, look at your wallet in around 20 minutes on https://testnets.opensea.io/assets/mumbai/{contract.address}")

if __name__ == "__main__":
    main()