#include<stdio.h>
#include<string.h>

int main(){
	int a;
	system("python GenerativeArt1.2.py");
	system("cd ERC721 && echo 1 > ./strg/decision.txt  && ipfs add --recursive --progress ./Results/ > ./strg/images.txt");
	system("python metadataUpdate.py && cd ERC721 && ipfs add --recursive --progress ./metadata/ > ./strg/jsons.txt");
	system("cd ERC721  && brownie run scripts/deploy.py --network mumbaiTesnnet");
}
