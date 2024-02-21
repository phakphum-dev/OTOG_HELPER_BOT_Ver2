import BigDiscord
import ENUM
import env
import dataBassSQL as sql
import configparser as cfg
import OTOG_API as otog
from os import path


def main():
    env.initEnv()
    sql.initData(env.get().DB_DATABASE, env.get().DB_USERNAME, 
                 env.get().DB_PASSWORD, env.get().DB_HOST,
                 env.get().DB_PORT)
    otog.init(env.get().OTOG_HOST, env.get().OTOG_API_HOST)
    BigDiscord.main(env.get().DISCORD_BOT_TOKEN, env.get().DISCORD_DEBUG.lower() == "true")


main()
