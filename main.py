#!/usr/bin/env python3

### MODULES :: Import ##################################################################
import sys
import json
import time
import caldav
from caldav.lib.error import AuthorizationError
import utils.logger as logger
from utils.constants import *
import paho.mqtt.client as mqttClient
from datetime import datetime, timedelta



### FUNCTION :: Round Time #############################################################
def roundTime(dt=None, dateDelta=timedelta(minutes=1)):
    roundTo = dateDelta.total_seconds()
    if dt is None:
        dt = datetime.now()
    seconds = (dt - dt.min).seconds
    rounding = (seconds+roundTo/2) // roundTo * roundTo
    return dt + timedelta(0, rounding-seconds, -dt.microsecond)
    # https://stackoverflow.com/questions/3463930/how-to-round-the-minute-of-a-datetime-object



### FUNCTION :: Connect MQTT Client ####################################################
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logger.info(f"[MQTT] Broker Connection Successful | {MQTT_USERNAME}@{MQTT_SERVER_ADDRESS}:{MQTT_SERVER_PORT}")
        print(f"[MQTT] Broker Connection Successful | {MQTT_USERNAME}@{MQTT_SERVER_ADDRESS}:{MQTT_SERVER_PORT}")
        for trigger in TRIGGERS:
            client.subscribe(trigger['MQTT_TOPIC'])
    else:
        logger.error(f"[MQTT] Broker Connection Failed | {MQTT_USERNAME}@{MQTT_SERVER_ADDRESS}:{MQTT_SERVER_PORT}")
        print(f"[MQTT] Broker Connection Failed | {MQTT_USERNAME}@{MQTT_SERVER_ADDRESS}:{MQTT_SERVER_PORT}")



### FUNCTION :: Action MQTT Message ####################################################
def on_message(client, userdata, message):
    try:
        logger.info(f"[MQTT] Event Received | {message.topic} | {message.payload.decode('ASCII')}")
        print(f"[MQTT] Event Received | {message.topic} | {message.payload.decode('ASCII')}")

        mqtt_event = json.loads(message.payload.decode('ASCII'))
        for trigger in TRIGGERS:
            if trigger['MQTT_TOPIC'] == message.topic and all((k in mqtt_event and mqtt_event[k] == v) for k, v in trigger['MQTT_EVENT'].items()):
                print(f"[MQTT] Event Matched  | {message.topic} | {message.payload.decode('ASCII')}")
                logger.info(f"[MQTT] Event Matched  | {message.topic} | {message.payload.decode('ASCII')}")

                if trigger['EVENT_ROUNDING'] == '' and trigger['EVENT_ROUNDING'] == '0':
                    now_datetime = datetime.now()
                else:
                    now_datetime = roundTime(datetime.now(), timedelta(minutes=int(trigger['EVENT_ROUNDING'])))
                end_datetime = now_datetime + timedelta(minutes=int(trigger['EVENT_DURATION']))

                if trigger['EVENT_SECONDS'].lower() == 'false':
                    start_time = now_datetime.strftime('%Y%m%dT%H%M00')
                    end_time = end_datetime.strftime('%Y%m%dT%H%M00')
                else:
                    start_time = now_datetime.strftime('%Y%m%dT%H%M%S')
                    end_time = end_datetime.strftime('%Y%m%dT%H%M%S')

                event_calendar = caldav.Calendar(client=cal_client, url=trigger['EVENT_CALENDAR'])
                main_event = f"""
BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//MQTT//EN
CALSCALE:GREGORIAN
BEGIN:VEVENT
DTSTART;TZID={trigger['EVENT_TIMEZONE']}:{start_time}
DTEND;TZID={trigger['EVENT_TIMEZONE']}:{end_time}
DTSTAMP:{start_time}
LOCATION:{trigger['EVENT_LOCATION']}
DESCRIPTION:{trigger['EVENT_DESCRIPTION']}
URL;VALUE=URI:{trigger['EVENT_URL']}
SUMMARY:{trigger['EVENT_SUMMARY']}
GEO:{trigger['EVENT_GEO']}
TRANSP:{trigger['EVENT_TRANSP']}
CATEGORIES:{trigger['EVENT_CATEGORIES']}
CREATED:{start_time}
"""

                end_event = """
END:VEVENT
END:VCALENDAR
"""
                if trigger['EVENT_TRIGGER']:
                    alarm_event = f"""
BEGIN:VALARM
TRIGGER:-PT{trigger['EVENT_TRIGGER']}M
ATTACH;VALUE=URI:Chord
ACTION:AUDIO
END:VALARM
"""
                    str_event = main_event + alarm_event + end_event
                else:
                    str_event = main_event + end_event

                my_event = event_calendar.save_event(str_event)
    except Exception as e:
        logger.error(f"[ERRR] Exception      | on_message: {e}")
        print(f"[ERRR] Exception      | on_message: {e}")

if __name__ == '__main__':


    
### Connect CalDAV Client ##############################################################
    global cal_client
    try:
        cal_client = caldav.DAVClient(url=CALDAV_SERVER_ADDRESS, username=CALDAV_USERNAME, password=CALDAV_PASSWORD)
        my_principal = cal_client.principal()
        calendars = my_principal.calendars()
        if calendars:
            logger.info(f"[CALDAV] Server Connection Successful | {CALDAV_USERNAME}@{CALDAV_SERVER_ADDRESS}")
            print(f"[CALDAV] Server Connection Successful | {CALDAV_USERNAME}@{CALDAV_SERVER_ADDRESS}")
            for c in calendars:
                print(f"[CALDAV] {c.name:<20} {c.url}")
        else:
            print("[CALDAV] Server Connection Successful | 0 Calendar")
    except AuthorizationError:
        logger.error(f'[CALDAV] Server Connection Failed | {CALDAV_USERNAME}@{CALDAV_SERVER_ADDRESS}')
        print(f'[CALDAV] Server Connection Failed | {CALDAV_USERNAME}@{CALDAV_SERVER_ADDRESS}')
        exit(1)



### Manage MQTT Connection #############################################################
    mqtt_client = mqttClient.Client("Python")
    mqtt_client.username_pw_set(MQTT_USERNAME, password=MQTT_PASSWORD)
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    mqtt_client.connect(MQTT_SERVER_ADDRESS, port=int(MQTT_SERVER_PORT))

    mqtt_client.loop_start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.warn("[USER] Keyboard Interrupt | Exit")
        print("[USER] Keyboard Interrupt | Exit")
        mqtt_client.disconnect()
        mqtt_client.loop_stop()
    except Exception as e:
        logger.error(f"[ERRR] Exception      | main loop: {e}")
        print(f"[ERRR] Exception      | main loop: {e}")
        mqtt_client.disconnect()
        mqtt_client.loop_stop()
