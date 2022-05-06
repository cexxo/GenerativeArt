from brownie import *
import pytest



@pytest.fixture(scope="module")
def NFT():
    return NFTContract.deploy({"from":accounts[0]})

def test_setPaused(NFT):
    assert NFT.isPaused() == True
    NFT.setPaused(False,{"from":accounts[0]})
    assert NFT.isPaused() == False

def test_name(NFT):
    assert NFT.name() == "Shaman"

def test_symbol(NFT):
    assert NFT.symbol() == "SHMN"

def test_balancing(NFT):
    NFT.setPaused(False,{"from":accounts[0]})
    NFT.mint(1,{"from":accounts[0],"value":50*10**15})
    assert (NFT.totalSupply() == 1)

def test_walletOfOwner(NFT):
    assert NFT.walletOfOwner(accounts[0]) == [1]

def test_tokenURI(NFT):
    uri = NFT.tokenURI(1)
    assert uri == ""

def test_reveal(NFT):
    assert NFT.isRevealed() == False
    NFT.setRevealed(True,{"from":accounts[0]})
    assert NFT.isRevealed() == True

def test_setCost(NFT):
    assert NFT.cost() == 0.01*10**18 
    NFT.setCost(0.05*10**18,{"from":accounts[0]})
    assert NFT.cost() == 0.05*10**18

def test_SetMaxMintAmmountPerTx(NFT):
    assert NFT.maxMintAmountPerTx() == 5
    NFT.setMaxMintAmountPerTx(1,{"from":accounts[0]})
    assert NFT.maxMintAmountPerTx() == 1

def test_setHiddenMetadataUri(NFT):
    assert NFT.hiddenMetadataUri() == ""
    NFT.setHiddenMetadataUri("questa_e_una_prova",{"from":accounts[0]})
    assert NFT.hiddenMetadataUri() == "questa_e_una_prova"

def test_setUriPrefix(NFT):
    assert NFT.uriPrefix() == ""
    NFT.setUriPrefix("new_prefix",{"from":accounts[0]})
    assert NFT.uriPrefix() == "new_prefix"

def test_setUriSuffix(NFT):
    assert NFT.uriSuffix() == ".json"
    NFT.setUriSuffix(".new_suffix",{"from":accounts[0]})
    assert NFT.uriSuffix() == ".new_suffix"

def test_mintLoop(NFT):
    temp = [1]
    for i in range (1,15):
        temp.append(i+1)
        NFT.mint(1,{"from":accounts[0],"value":50*10**15})
        assert (NFT.totalSupply() == i+1)
        assert NFT.walletOfOwner(accounts[0]) == temp
        assert NFT.balanceOf(accounts[0]) == i + 1
    try :
        NFT.mint(3,{"from":accounts[0],"value":50*10**15})
    except:
        print("except")
        assert False == False
    NFT.setMaxMintAmountPerTx(3,{"from":accounts[0]})
    NFT.mint(3,{"from":accounts[0],"value":3*50*10**15})
    temp.append(16)
    temp.append(17)
    temp.append(18)
    assert NFT.totalSupply() == 18
    assert NFT.walletOfOwner(accounts[0]) == temp
    assert NFT.balanceOf(accounts[0]) == 18
        
def test_allURI(NFT):
    for i in range (1,NFT.totalSupply()+1):
        assert NFT.tokenURI(i) == f"new_prefix{i}.new_suffix"