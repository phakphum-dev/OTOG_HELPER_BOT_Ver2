import BigDiscord,ENUM
from os import path


def main():

    thisToken = 0

    if path.exists(path.join(ENUM.PATH,"__TOKEN__.txt")):
        with open(path.join(ENUM.PATH,"__TOKEN__.txt")) as f:
            thisToken = f.read().strip()
            print(f"Found __TOKEN__\n{thisToken}\n")
    else:
        thisToken = input("Tell me your TOKEN :) : ")
        if thisToken == "":
            print("WTF MANN")
            exit(1)
        print("You can create file name '__TOKEN__.txt'\nand save with your *token*\nIn next you don't need to tell me your token :)")


    BigDiscord.main(thisToken, True)


main()




