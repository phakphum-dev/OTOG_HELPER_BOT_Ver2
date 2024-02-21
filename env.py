# Quick env
from os import path

class EnvConfig:
    DB_HOST = ""
    DB_PORT = ""
    DB_DATABASE = ""
    DB_USERNAME = ""
    DB_PASSWORD = ""

    OTOG_HOST = ""
    OTOG_API_HOST = ""

    DISCORD_BOT_TOKEN = ""
    DISCORD_DEBUG = ""

_env: EnvConfig = EnvConfig()
_isInit = False

def initEnv():
    global _env
    if _isInit:
        return
    if path.exists(".env"):
        with open(".env","r") as f:
            for line in f:
                # Ignore comments and find a '='
                thisLine = line.strip()
                if thisLine.find("#") != -1:
                    thisLine = thisLine[:thisLine.find("#")].strip()
                
                if  '=' in thisLine:
                    key = thisLine.split('=')[0]
                    value = ("=".join(thisLine.split('=')[1:])).strip()
                    if hasattr(_env, key):
                        setattr(_env, key, value)
    else:
        print(".env not found :(")
        exit(1)

def get():
    if not _isInit:
        initEnv()
    
    return _env

if __name__ == "__main__":
    print(get().DISCORD_DEBUG)
