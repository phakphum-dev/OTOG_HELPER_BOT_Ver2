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
    sql.initData(config["SQL"]["Name"], config["SQL"]
                 ["User"], config["SQL"]["Password"], config["SQL"]["Host"],
                 config["SQL"]["Port"])

    BigDiscord.main(thisToken, config["Discord"]
                    ["Debug_Mode"].lower() == "true")


main()
