#include<stdio.h>
#include<string.h>

int main(){
	int a;
	system("python GenerativeArt1.1.py");
	system("cd ERC721 && echo 1 > ./strg/decision.txt && ipfs add --recursive --progress ./metadata/ > ./strg/jsons.txt && ipfs add --recursive --progress ./Results/ > ./strg/images.txt");
	system("python metadataUpdate.py");
	system("cd ERC721  && brownie run scripts/deploy.py --network mumbaiTesnnet");
}