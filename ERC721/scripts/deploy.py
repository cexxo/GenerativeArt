from distutils.command.config import config
from importlib.metadata import metadata
from brownie import *
import time

def get_hash(path):
    fp = open(path,"r")
    text = []
    for i in fp:
        text.append(i.split(' '))
    a = []
    a = text[-1].copy()
    hash = a [1]
    return hash

def main():
    j_hash = get_hash("./strg/jsons.txt")
    uri = "https://ipfs.io/ipfs/"+ j_hash +"/"                                                
    dev = accounts.add(config['wallets']['from_key'])                           #i create a variable dev that will store the wallet of the 
                                                                                #user that is using this program.
    print("the active network is: " + network.show_active())                    #i print the network where the program is running the test
    publish_source = False                                                      #i set the publish source of the contrac to false.
    contract = NFTContract.deploy({"from": dev})                                #i deploy the contract and i store it in the variable contract
    contract.setPaused(False,{"from":dev})                                      #Unpause the contract and use the wallet of the user, then 
    print("the contract is now unpaused")                                       #notify the user that the contract has been succesfully unpaused
    contract.setRevealed(True)                                                  #reveal the contract and notify it to the user.
    contract.mint(1,{"from":dev,"value":50*10**15})
    time.sleep(120)

if __name__ == "__main__":
    main()