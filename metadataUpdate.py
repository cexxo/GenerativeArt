import json
def get_hash(path):
    fp = open(path,"r")
    text = []
    for i in fp:
        text.append(i.split(' '))
    a = []
    a = text[-1].copy()
    hash = a [1]
    return hash


def meta_update(i_hash,metadata_file_name,count):
    b = open(metadata_file_name,"r")
    a = json.load(b)
    value = str("https://ipfs.io/ipfs/"+ i_hash +"/" + str(count) +".png")
    a["image"] = value
    with open(metadata_file_name, "w") as file:                         #i open the metadata file of the NFT which has been generated and i
        json.dump(a,file)

def main():
    metadata_save = "ERC721/metadata/"
    temp = open("./ERC721/uri.txt","r")
    max = int(temp.readline().strip())
    i_hash = get_hash("./ERC721/strg/images.txt")
    for i in range(max):
        metadata_file_name = (metadata_save + str(i+1) + ".json")
        meta_update(i_hash,metadata_file_name,i+1)

if __name__ == "__main__":
    main()