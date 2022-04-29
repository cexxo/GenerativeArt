def main():
    fp = open(path,"r")
    text = []
    for i in fp:
        text.append(i.split(' '))
    a = []
    a = text[-1].copy()
    hash = a [1]
    print(hash)

if __name__ == "__main__":
    main()