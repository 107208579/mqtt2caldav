#!/usr/bin/env python3

import paho.mqtt.client as mqttClient
import time
from datetime import datetime, timedelta
import sys
import caldav
from caldav.lib.error import AuthorizationError

from utils.constants import *
import utils.logger as logger
import json


def roundTime(dt=None, dateDelta=timedelta(minutes=1)):
    """Round a datetime object to a multiple of a timedelta
    dt : datetime.datetime object, default now.
    dateDelta : timedelta object, we round to a multiple of this, default 1 minute.
    Author: Thierry Husson 2012 - Use it as you want but don't blame me.
            Stijn Nevens 2014 - Changed to use only datetime objects as variables
    """
    roundTo = dateDelta.total_seconds()

    if dt is None:
        dt = datetime.datetime.now()
    seconds = (dt - dt.min).seconds
    # // is a floor division, not a comment on following line:
    rounding = (seconds+roundTo/2) // roundTo * roundTo
    return dt + timedelta(0, rounding-seconds, -dt.microsecond)


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logger.info("Connected to broker")
        print("Connected to broker")
        for trigger in TRIGGERS:
            client.subscribe(trigger['MQTT_TOPIC'])
    else:
        logger.error("Connection failed")
        print("Connection failed")


def on_message(client, userdata, message):
    logger.info("Message received : " + message.payload.decode('ASCII') + " on " + message.topic)
    print("Message received : " + message.payload.decode('ASCII') + " on " + message.topic)
    # my_new_calendar = my_principal.make_calendar(name="Calendar")
    mqtt_event = json.loads(message.payload.decode('ASCII'))
    for trigger in TRIGGERS:
        if trigger['MQTT_TOPIC'] == message.topic and all((k in mqtt_event and mqtt_event[k] == v) for k, v in trigger['MQTT_EVENT'].items()):
            print("Mqtt event matched with trigger one.")
            logger.info("Mqtt event matched with trigger one.")
            if trigger['EVENT_ROUNDING'] == '' and trigger['EVENT_ROUNDING'] == '0':
                now_datetime = datetime.now()
            else:
                now_datetime = roundTime(datetime.now(), timedelta(minutes=int(trigger['EVENT_ROUNDING'])))
            end_datetime = now_datetime + timedelta(minutes=int(trigger['EVENT_DURATION']))
            if trigger['EVENT_SECONDS'] == 'False' or trigger['EVENT_SECONDS'] == 'false':
                start_time = now_datetime.strftime('%Y%m%dT%H%M00')
                end_time = end_datetime.strftime('%Y%m%dT%H%M00')
            else:
                start_time = now_datetime.strftime('%Y%m%dT%H%M%S')
                end_time = end_datetime.strftime('%Y%m%dT%H%M%S')
            event_calendar = caldav.Calendar(client=cal_client, url=trigger['EVENT_CALENDAR'])
            main_event = """
BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Script//EN
CALSCALE:GREGORIAN
BEGIN:VEVENT
DTSTART;TZID="""+trigger['EVENT_TIMEZONE']+""":"""+start_time+"""
DTEND;TZID="""+trigger['EVENT_TIMEZONE']+""":"""+end_time+"""
DTSTAMP:"""+start_time+"""
LOCATION:"""+trigger['EVENT_LOCATION']+"""
DESCRIPTION:"""+trigger['EVENT_DESCRIPTION']+"""
URL;VALUE=URI:"""+trigger['EVENT_URL']+"""
SUMMARY:"""+trigger['EVENT_SUMMARY']+"""
GEO:"""+trigger['EVENT_GEO']+"""
CATEGORY:"""+trigger['EVENT_CATEGORY']+"""
CREATED:"""+start_time
            end_event = """
END:VEVENT
END:VCALENDAR
"""
            if trigger['EVENT_TRIGGER'] == '':
                str_event = main_event + end_event
            else:
                alarm_event = """
BEGIN:VALARM
TRIGGER:-PT"""+trigger['EVENT_TRIGGER']+"""M
ATTACH;VALUE=URI:Chord
ACTION:AUDIO
END:VALARM
"""
                str_event = main_event + alarm_event + end_event

            # str_event = str_event.format(timezone=trigger['EVENT_TIMEZONE'], location=trigger['EVENT_LOCATION'], description=trigger['EVENT_DESCRIPTION'], url=trigger['EVENT_URL'],
            #                              summary=trigger['EVENT_SUMMARY'], geo=trigger['EVENT_GEO'], category=trigger['EVENT_CATEGORY'], created_time=start_time, trigger_time=trigger['EVENT_TRIGGER'],
            #                              start_time=start_time, end_time=end_time)
            # Let's add an event to our newly created calendar
            my_event = event_calendar.save_event(str_event)


if __name__ == '__main__':
    # CALDAV Server Connection
    global cal_client
    try:
        cal_client = caldav.DAVClient(url=CALDAV_SERVER_ADDRESS, username=CALDAV_USERNAME, password=CALDAV_PASSWORD)
        my_principal = cal_client.principal()
        calendars = my_principal.calendars()
        if calendars:
            print("your principal has %i calendars:" % len(calendars))
            for c in calendars:
                print("Name: %-20s  URL: %s" % (c.name, c.url))
        else:
            print("your principal has no calendars")
    except AuthorizationError:
        logger.error('incorrect CALDAV details')
        print('caldav error: incorrect CALDAV details')
        exit(1)

    # MQTT Broker Connection
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
        logger.warn("exiting")
        print("exiting")
        mqtt_client.disconnect()
        mqtt_client.loop_stop()

# if __name__ == '__main__':
#     print(roundTime(datetime.now(), timedelta(minutes=5)))
