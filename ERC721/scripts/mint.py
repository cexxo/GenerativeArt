from distutils.command.config import config
from importlib.metadata import metadata
from brownie import *
import time


def main():                                             
    dev = accounts.add(config['wallets']['from_key'])                           #i create a variable dev that will store the wallet of the 
                                                                                #user that is using this program.
    contract = NFTContract[len(NFTContract) - 1]
    print("the active network is: " + network.show_active())                    #i print the network where the program is running the test
    publish_source = False                                                      #i set the publish source of the contrac to false.
    contract.mint(1,{"from":dev,"value":50*10**15})
    time.sleep(120)