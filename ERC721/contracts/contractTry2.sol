// SPDX-License-Identifier: MIT
pragma solidity >=0.7.0 <0.9.0;

import "./libraries.sol";


contract NFTProva3 is ERC721, Ownable {
  using Strings for uint256;                                                                    //this contract should use all the dependencies
  using Counters for Counters.Counter;                                                          //from the contract libraries.
                                                                                                //Strings and counters are renamings.
  Counters.Counter private supply;                                                              //i declare a private variable that will store
                                                                                                //the supply of NFTs.

  uint256 private currentToken = 1;
  //string public uriPrefix = "";                                                                 //variable that stores the prefi of our URI
  string public uriSuffix = ".json";                                                            //variable that stores the suffix of our URI
  string public hiddenMetadataUri = "https://ipfs.io/ipfs/QmPvfCxLZ1sEyw9VHz4YgFQPpYqWvJkxCgQUFr5QCc5UEU?filename5.json";                                                              //variable that store the URI of the hiddend
                                                                                                //metadata.
  uint256 public cost = 0.01 ether;                                                             //the cost set for our NFTs
  uint256 public maxSupply = 500;                                                               //the number of maxible NFT that are avaiable
  uint256 public maxMintAmountPerTx = 5;                                                        //the max number of NFT we can mint in one 
                                                                                                //transaction.
  mapping(uint256 => string) _uris;
  bool public paused = true;                                                                    //it allows us to set if the NFTs can be minted
                                                                                                //or no.
  bool public revealed = false;                                                                 //variable tha tsets the state of the revealing.

  constructor() ERC721("Shaman", "SHMN") {                                                      //constructor of our token, it accepts 2 parameters
    setHiddenMetadataUri("");//a name and a symbol.
  }                                                                                             //i set the hidden metadata uri.

  modifier mintCompliance(uint256 _mintAmount) {                                                //this modifier checks if the number of minted
    require(_mintAmount > 0 && _mintAmount <= maxMintAmountPerTx, "Invalid mint amount!");      //NFT is higher than the max supply or higher
    require(supply.current() + _mintAmount <= maxSupply, "Max supply exceeded!");               //than the maximum number of mint per transaction
    _;                                                                                          //this code is executed before the implementer 
  } 

  function totalSupply() public view returns (uint256) {                                        //this function allows us to retrieve the total
    return supply.current();                                                                    //supply of minted nft.
  }
                                                                                                //this function uses the modifier mintCompliance
  function mint(uint256 _mintAmount) public payable mintCompliance(_mintAmount) {                       //this function allows us to mint an nft.
    require(!paused, "The contract is paused!");                                                //we have to specify how many NFTs we want to
    require(msg.value >= cost * _mintAmount, "Insufficient funds!");                            //mint with this transaction. if the contract
                                                                                                //is on pause, we cannot mint. same if we don't
    _mintLoop(msg.sender, _mintAmount);                                                         //have enough funds.

  }                                                                                             //we mint all the NFTs the user declared.
  
  function mintForAddress(uint256 _mintAmount, address _receiver) public mintCompliance(_mintAmount) onlyOwner {//this allows us to mint for an
    _mintLoop(_receiver, _mintAmount);                                                          //address we specify. it calls _mintLoop.
  }

  function walletOfOwner(address _owner)                                                        //this function allows us to show the wallet of
    public                                                                                      //an address. it returns an array of the owned
    view                                                                                        //tokens of the specified address.
    returns (uint256[] memory)                                                                  
  {
    uint256 ownerTokenCount = balanceOf(_owner);                                                //the number of tokens is given by the owner's
    uint256[] memory ownedTokenIds = new uint256[](ownerTokenCount);                            //balance. the array size is gonna be the same
    uint256 currentTokenId = 1;                                                                 //as the number of tokens owned.
    uint256 ownedTokenIndex = 0;                                                                //we have now to variables: one keeps track of
                                                                                                //the iterations we did; the other the tokenId
                                                                                                //we are considering.
    while (ownedTokenIndex < ownerTokenCount && currentTokenId <= maxSupply) {                  //while the token index is lower than the number
                                                                                                //of maximum token owned, and the tokenId is 
                                                                                                //lower than the total supply of the tokens:
      address currentTokenOwner = ownerOf(currentTokenId);                                      //the address of the current token is given
                                                                                                //by the function ownerOf.
      if (currentTokenOwner == _owner) {                                                        //if the owner we found is the same as the owner
        ownedTokenIds[ownedTokenIndex] = currentTokenId;                                        //we are considering, we add to the array the Id
                                                                                                //of the tokeen found.
        ownedTokenIndex++;                                                                      //we increment the index of the array.
      }

      currentTokenId++;                                                                         //we increment the iteration variable
    }

    return ownedTokenIds;                                                                       //we return the array with all the Ids.
  }

  function tokenURI(uint256 _tokenId)                                                           //this function allows us to reveal our NFTs
    public                                                                                      //the revealing it's allowed only if the variable
    view                                                                                        //revealed is set to true.
    virtual                                                                                     //if that is not the case, it returns the hidden
    override                                                                                    //metadata URI.
    returns (string memory)                                                                     //It also requires that the token we are looking
  {
    require(                                                                                    //for exists. if not we return an errore message
      _exists(_tokenId),                                                                        
      "ERC721Metadata: URI query for nonexistent token"                                         
    );

    if (revealed == false) {                                                                    //here we controll the revealed variable.
      return hiddenMetadataUri;                                                                 //the return statment in case it is not revealed
    }

    string memory currentBaseURI = _baseURI();                                           //we create our URI with the base URI
    return bytes(currentBaseURI).length > 0                                                     //and we add things only if the baseURI has 
        ? string(abi.encodePacked(currentBaseURI, _tokenId.toString(), uriSuffix))              //a length bigger than 0.
        : "";
  }

  function setRevealed(bool _state) public onlyOwner {                                          //this function can be called only by the owner
    revealed = _state;                                                                          //of the contract. it allows to set the reveal
  }                                                                                             //state variable to true or false.

  function setCost(uint256 _cost) public onlyOwner {                                            //this function can be called only by the owner
    cost = _cost;                                                                               //and it allows to set the cost of the NFTs.
  }

  function setMaxMintAmountPerTx(uint256 _maxMintAmountPerTx) public onlyOwner {                //this function can be called only by the owner
    maxMintAmountPerTx = _maxMintAmountPerTx;                                                   //and it allows to set the maximum number of NFT
  }                                                                                             //that can be minted in a transaction.

  function setHiddenMetadataUri(string memory _hiddenMetadataUri) public onlyOwner {            //this fuction can be called only by the owner
    hiddenMetadataUri = _hiddenMetadataUri;                                                     //and it allows to set the URI of the hidden
  }                                                                                             //metadata.

  function setUriPrefix(string memory _uriPrefix) public onlyOwner {                            //this function can be called only by the owner
    _uris[currentToken] = _uriPrefix;                                                           //and it allows to set the URI prefix.
  }

  function setUriSuffix(string memory _uriSuffix) public onlyOwner {                            //this function can be called only by the owner
    uriSuffix = _uriSuffix;                                                                     //and it allows to set the URI sufix.
  }

  function setPaused(bool _state) public onlyOwner {                                            //this function can be called only by the owner
    paused = _state;                                                                            //and it allows to change the state of the contract
  }

  function withdraw() public onlyOwner {                                                        //this fuction can be called only by the owner.
    (bool os, ) = payable(owner()).call{value: address(this).balance}("");                      //it transfers the balance of the minted NFT
    require(os);                                                                                //to the address of the owner.
  }

  function _mintLoop(address _receiver, uint256 _mintAmount) internal {                         //this function creates the minting loop of the
    for (uint256 i = 0; i < _mintAmount; i++) {                                                 //NFTs. this allows a user to mint more NFTs 
      supply.increment();                                                                       //per transaction. it calles the _safeMint method
      _safeMint(_receiver, supply.current());                                                   //inherited from the ERC721 contract.
      currentToken += 1;
    }
  }

  function _baseURI() internal view virtual override returns (string memory) {           //this function allows the user to get the 
    return _uris[currentToken];                                                                       //baseURI of our NFTs.
  }
}