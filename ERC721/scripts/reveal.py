from brownie import *

def main():
    dev = dev = accounts.add(config['wallets']['from_key'])                         #in this function we will set the reveal of our NFT.
    NFTContract.setRevealed(True,{"form":dev})                                        #If the program is called, the NFTs are revealed.