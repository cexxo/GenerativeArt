from brownie import *

def main():
    dev = dev = accounts.add(config['wallets']['from_key'])
    NFTProva4.setRevealed(True,{"form":dev})