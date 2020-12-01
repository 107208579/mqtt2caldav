import os
import json

# PATHS
_cur_dir = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.join(_cur_dir, os.pardir)
LOG_DIR = os.path.join(ROOT_DIR, 'logs')
CONF_DIR = os.path.join(ROOT_DIR, 'config')
config_file = "config.json"


with open(CONF_DIR+'\\'+config_file) as json_file:
    json_data = json.load(json_file)
    MQTT_SERVER_ADDRESS = json_data['mqtt']['MQTT_SERVER_ADDRESS']
    MQTT_SERVER_PORT = json_data['mqtt']['MQTT_SERVER_PORT']
    MQTT_USERNAME = json_data['mqtt']['MQTT_USERNAME']
    MQTT_PASSWORD = json_data['mqtt']['MQTT_PASSWORD']

    CALDAV_SERVER_ADDRESS = json_data['caldav']['CALDAV_SERVER_ADDRESS']
    CALDAV_USERNAME = json_data['caldav']['CALDAV_USERNAME']
    CALDAV_PASSWORD = json_data['caldav']['CALDAV_PASSWORD']

    TOPICS = json_data['topics']
