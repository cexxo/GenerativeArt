from distutils.command.config import config
from importlib.metadata import metadata
from brownie import *
import time


def main():                                             
    dev = accounts.add(config['wallets']['from_key'])                           #i create a variable dev that will store the wallet of the 
                                                                                #user that is using this program.
    contract = NFTContract[len(NFTContract) - 1]                                #i store the last contract that has been deployed.
    print("insert the id of the token you want to know: ")                      #i ask the user which token he is looking for.
    s = int(input())                                                            #i store the input.
    print("the active network is: " + network.show_active())                    #i print the network where the program is running the test
    print(contract.tokenURI(s,{"from":dev}))                                    #i print the uri of the chosen token.