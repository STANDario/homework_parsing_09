from mongoengine import connect
import configparser


config = configparser.ConfigParser()
config.read("config.ini")

mongo_user = config.get("DB", "USER")
mongo_password = config.get("DB", "PASSWORD")
mongo_db_name = config.get("DB", "DB_NAME")
mongo_domain = config.get("DB", "DOMAIN")

connect(host=f"""mongodb+srv://{mongo_user}:{mongo_password}@{mongo_domain}/{mongo_db_name}?retryWrites=true&w=majority""", ssl=True)

