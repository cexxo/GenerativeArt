from brownie import *
import pytest
import time


@pytest.fixture(scope="module")
def NFT():
    return NFTContract.deploy({"from":accounts[0]})

def test_alternateAccounts(NFT):
    NFT.setPaused(False,{"from":accounts[0]})
    NFT.setRevealed(True,{"form":accounts[0]})
    NFT.setMaxMintAmountPerTx(3,{"from":accounts[0]})
    NFT.mint(3,{"from":accounts[0],"value":50*10**15})
    NFT.mintForAddress(3,accounts[1])
    assert NFT.totalSupply() == 6
    assert NFT.walletOfOwner(accounts[0]) == [1,2,3]
    assert NFT.walletOfOwner(accounts[1]) == [4,5,6]
    assert NFT.balanceOf(accounts[0]) == NFT.balanceOf(accounts[1])
    assert NFT.balanceOf(accounts[0]) == 3
    assert NFT.balanceOf(accounts[1]) == 3

def test_havings(NFT):
    assert NFT.totalSupply() == 6
    assert NFT.walletOfOwner(accounts[0]) == [1,2,3]
    assert NFT.walletOfOwner(accounts[1]) == [4,5,6]
    assert NFT.balanceOf(accounts[0]) == NFT.balanceOf(accounts[1])
    assert NFT.balanceOf(accounts[0]) == 3
    assert NFT.balanceOf(accounts[1]) == 3

def test_mintLoop(NFT):
    NFT.mintForAddress(2,accounts[2])
    NFT.mintForAddress(3,accounts[3])
    assert NFT.totalSupply() == 11
    assert NFT.walletOfOwner(accounts[0]) == [1,2,3]
    assert NFT.walletOfOwner(accounts[1]) == [4,5,6]
    assert NFT.walletOfOwner(accounts[2]) == [7,8]
    assert NFT.walletOfOwner(accounts[3]) == [9,10,11]
    assert NFT.balanceOf(accounts[0]) == NFT.balanceOf(accounts[1])
    assert NFT.balanceOf(accounts[0]) == 3
    assert NFT.balanceOf(accounts[1]) == 3
    assert NFT.balanceOf(accounts[2]) == 2
    assert NFT.balanceOf(accounts[3]) == 3
    assert NFT.balanceOf(accounts[2]) != NFT.balanceOf(accounts[3])

def test_IdOutOfIndex(NFT):
    try:
        NFT.tokenURI(99,{"from":accounts[0]})
    except:
        assert True == True

def test_mintLimit(NFT):
    while True:
        try:
            NFT.mint(1,{"from":accounts[0],"value":50*10**15})
        except:
            assert NFT.totalSupply() == 500
            break

def test_allTokenUri(NFT):
    count = 0
    NFT.setUriPrefix("prefix",{"from":accounts[0]})
    for i in range(1,NFT.totalSupply()+1):
        count += 1
        assert NFT.tokenURI(i) == f"prefix{i}.json"
    assert count == 500
    NFT.setUriPrefix("new_prefix",{"from":accounts[0]})
    count = 0
    for i in range(1,NFT.totalSupply()+1):
        count += 1
        assert NFT.tokenURI(i) == f"new_prefix{i}.json"
    assert count == 500

def test_wholeWallet(NFT):
    assert NFT.walletOfOwner(accounts[1]) == [4,5,6]
    assert NFT.walletOfOwner(accounts[2]) == [7,8]
    assert NFT.walletOfOwner(accounts[3]) == [9,10,11]
    temp = [1,2,3]
    for i in range(12,NFT.totalSupply()+1):
        temp.append(i)
    assert NFT.walletOfOwner(accounts[0]) == temp
