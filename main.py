import BigDiscord
import ENUM
import dataBassSQL as sql
import configparser as cfg
from os import path


def main():

    thisToken = 0

    if path.exists(path.join(ENUM.PATH, "BigConfig.ini")):
        config = cfg.ConfigParser()
        config.read(path.join(ENUM.PATH, "BigConfig.ini"))
        print(f"Read config!")
    else:
        print("BigConfig.ini not found :(")
        exit(1)

    thisToken = config["Discord"]["TOKEN"]

    envConfig = dict()
    if path.exists(path.join(ENUM.PATH, ".env")):
        print(f"Read env!")
        with open(".env","r") as f:
            for line in f:
                if line.strip()[0] != "#" and '=' in line:
                    envConfig[line.split('=')[0]] = ("=".join(line.split('=')[1:])).strip()
    else:
        print(".env not found :(")
        exit(1)

    sql.initData(envConfig["DB_DATABASE"], envConfig["DB_USERNAME"], 
                 envConfig["DB_PASSWORD"], envConfig["DB_HOST"],
                 envConfig["DB_PORT"])

    BigDiscord.main(thisToken, config["Discord"]["Debug_Mode"].lower() == "true")


main()
