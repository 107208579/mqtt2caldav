#!/usr/bin/env python3

import paho.mqtt.client as mqttClient
import time
from datetime import datetime, timedelta
import sys
import caldav
from utils.constants import *
import utils.logger as logger
import json


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
    logger.info("Message received : " + str(message.payload) + " on " + message.topic)
    print("Message received : " + message.payload.decode('ASCII') + " on " + message.topic)
    # my_new_calendar = my_principal.make_calendar(name="Calendar")
    mqtt_event = json.loads(message.payload.decode('ASCII'))
    for trigger in TRIGGERS:
        if trigger['MQTT_TOPIC'] == message.topic and all((k in mqtt_event and mqtt_event[k] == v) for k, v in trigger['MQTT_EVENT'].iteritems()):
            print("Mqtt event matched with trigger one.")
            logger.info("Mqtt event matched with trigger one.")
            now_datetime = datetime.now()
            end_datetime = now_datetime + timedelta(minutes=int(trigger['EVENT_DURATION']))
            if trigger['EVENT_SECONDS'] == 'False' or trigger['EVENT_SECONDS'] == 'false':
                start_time = now_datetime.strftime('%Y%m%dT%H%M00')
                end_time = end_datetime.strftime('%Y%m%dT%H%M00')
            else:
                start_time = now_datetime.strftime('%Y%m%dT%H%M%S')
                end_time = end_datetime.strftime('%Y%m%dT%H%M%S')
            event_calendar = caldav.Calendar(client=cal_client, url=trigger['EVENT_CALENDAR'])
            str_event = """BEGIN:VCALENDAR
            VERSION:2.0
            PRODID:-//Script//EN
            CALSCALE:GREGORIAN
            BEGIN:VEVENT
            DTSTART;TZID={timezone}:{start_time}
            DTEND;TZID={timezone}:{end_time}
            UID:D04A88A5-A56A-4FC9-BEDF-A064C18EEB83
            DTSTAMP:{start_time}
            LOCATION:{location}
            DESCRIPTION:{description}
            URL;VALUE=URI:{url}
            SUMMARY:{summary}
            GEO:{geo}
            CATEGORY:{category}
            CREATED:{created_time}
            BEGIN:VALARM
            TRIGGER:-PT{trigger_time}M
            ATTACH;VALUE=URI:Chord
            ACTION:AUDIO
            END:VALARM
            END:VEVENT
            END:VCALENDAR
            """
            str_event = str_event.format(timezone=trigger['EVENT_TIMEZONE'], location=trigger['EVENT_LOCATION'], description=trigger['EVENT_DESCRIPTION'], url=trigger['EVENT_URL'],
                                         summary=trigger['EVENT_SUMMARY'], geo=trigger['EVENT_GEO'], category=trigger['EVENT_CATEGORY'], created_time=start_time, trigger_time=trigger['EVENT_TRIGGER'],
                                         start_time=start_time, end_time=end_time)
            # Let's add an event to our newly created calendar
            my_event = event_calendar.save_event(str_event)


if __name__ == '__main__':
    # CALDAV Server Connection
    global cal_client
    cal_client = caldav.DAVClient(url=CALDAV_SERVER_ADDRESS, username=CALDAV_USERNAME, password=CALDAV_PASSWORD)
    my_principal = cal_client.principal()
    calendars = my_principal.calendars()
    if calendars:
        print("your principal has %i calendars:" % len(calendars))
        for c in calendars:
            print("Name: %-20s  URL: %s" % (c.name, c.url))
    else:
        print("your principal has no calendars")

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
