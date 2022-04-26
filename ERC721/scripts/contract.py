from distutils.command.config import config
from brownie import *
import time

def main():
    uri = []
    dev = accounts.add(config['wallets']['from_key'])
    print("the active network is: " + network.show_active())
    publish_source = False
    contract = NFTProva3.deploy({"from": dev})
    try:
        uris_ = open("uri.txt","r")
    except:
        print("uri file not found...")
    for line in uris_:
        uri.append(line.strip())
    contract.setPaused(False,{"from":dev})
    print("the contract is now unpaused")
    for i in range(len(uri)):
        contract.setUriPrefix(uri[i], {"from":dev})
        print(f"we are minting the {i+1}-th token")
        contract.mint(1,{"from":dev,"value":50*10**15})
        time.sleep(60)
    contract.setRevealed(True)
    print("The NFTs are revealed, look at your wallet in around 20 minutes on https://testnets.opensea.io/")
    contract.setPaused(True)
    print("the contract is now paused")

if __name__ == "__main__":
    main()