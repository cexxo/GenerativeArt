from functools import total_ordering
from brownie import *
import pytest
import time


@pytest.fixture(scope="module")
def NFT():
    return NFTContract.deploy({"from":accounts[0]})

def test_priceRangesToMine(NFT):
    NFT.setPaused(False,{"from":accounts[0]})
    val = 1
    while True:
        try:
            NFT.mint(1,{"from":accounts[0],"value":val*10**15})
            break
        except:
            val += 0.5
    assert val == 10

def test_tryNewPriceForAll(NFT):
    val = 10**16
    iterations = 1
    while iterations < 500:
        try:
            NFT.mint(1,{"from":accounts[0],"value":val})
            print(f"iteration {i}-th")
        except:
            iterations += 1
            if iterations <= 10:
                val = int(5*iterations*10**15)
            if iterations == 600:
                break
    assert NFT.totalSupply() == 500
    assert val == 5*10**16
