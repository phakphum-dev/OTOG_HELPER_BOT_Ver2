import BigDiscord
import ENUM
import env
import dataBassSQL as sql
import configparser as cfg
import OTOG_API as otog
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


    env.initEnv()
    sql.initData(env.get().DB_DATABASE, env.get().DB_USERNAME, 
                 env.get().DB_PASSWORD, env.get().DB_HOST,
                 env.get().DB_PORT)
    otog.init(env.get().OTOG_HOST, env.get().OTOG_API_HOST)
    BigDiscord.main(env.get().DISCORD_BOT_TOKEN, env.get().DISCORD_DEBUG.lower() == "true")


main()
