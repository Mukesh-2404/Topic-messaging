import firebase_admin
from firebase_admin import credentials
import configparser

# Read configuration from the config file
config = configparser.ConfigParser()
config.read(r"./notifier.cfg")

cred = credentials.Certificate(r"./push-notification-1479e-firebase-adminsdk-qllb5-219a131716.json")

try:
    firebase_admin.initialize_app(cred)
except ValueError:
    # Firebase app is already initialized
    pass

db_config = {
    'host': config["DATABASE"]["host"],
    'user': config["DATABASE"]["user"],
    'password': config["DATABASE"]["password"],
    'database': config["DATABASE"]["database"]
}
