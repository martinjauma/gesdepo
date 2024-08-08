import pymongo
import yaml

def get_database():
    with open("config/config.yaml") as file:
        config = yaml.safe_load(file)
    client = pymongo.MongoClient(config['mongodb']['uri'])
    return client[config['mongodb']['database']]
