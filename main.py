#!/usr/bin/env python3

import paho.mqtt.client as mqttClient
import time
from datetime import datetime
import sys
import caldav
from utils.constants import *
import utils.logger as logger


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logger.info("Connected to broker")
        print("Connected to broker")
        client.subscribe("topic/1")
        client.subscribe("topic/2")
        client.subscribe("topic/3")
        client.subscribe("topic/4")

    else:
        logger.error("Connection failed")
        print("Connection failed")


def on_message(client, userdata, message):
    logger.info("Message received : " + str(message.payload) + " on " + message.topic)
    print("Message received : " + str(message.payload) + " on " + message.topic)
    my_new_calendar = my_principal.make_calendar(name="Calendar")

    # Let's add an event to our newly created calendar
    my_event = my_new_calendar.save_event("""BEGIN:VCALENDAR
    VERSION:2.0
    PRODID:-//Script//EN
    CALSCALE:GREGORIAN
    BEGIN:VEVENT
    DTSTART;TZID=Asia/Singapore:20201125T220000
    DTEND;TZID=Asia/Singapore:20201125T230000
    UID:D04A88A5-A56A-4FC9-BEDF-A064C18EEB83
    DTSTAMP:20201125T140000Z
    LOCATION:12 Main Road\, 7344 Nowhere\, Alaska
    DESCRIPTION:Meeting to discuss new product launches
    URL;VALUE=URI:http://example.com
    SUMMARY:Meeting Awesome Inc
    GEO:48.85299;2.36885
    CATEGORY:Meeting
    CREATED:20201125T140000Z
    BEGIN:VALARM
    TRIGGER:-PT15M
    ATTACH;VALUE=URI:Chord
    ACTION:AUDIO
    END:VALARM
    END:VEVENT
    END:VCALENDAR
    """)


if __name__ == '__main__':
    # CALDAV Server Connection
    client = caldav.DAVClient(url=CALDAV_SERVER_ADDRESS, username=CALDAV_USERNAME, password=CALDAV_PASSWORD)
    my_principal = client.principal()
    calendars = my_principal.calendars()
    if calendars:
        print("your principal has %i calendars:" % len(calendars))
        for c in calendars:
            print("Name: %-20s  URL: %s" % (c.name, c.url))
    else:
        print("your principal has no calendars")

    # MQTT Broker Connection
    mqttClient.username_pw_set(MQTT_USERNAME, password=MQTT_PASSWORD)
    client = mqttClient.Client("Python")
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_SERVER_ADDRESS, port=MQTT_SERVER_PORT)
    client.loop_start()

    try:
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        logger.warn("exiting")
        print("exiting")
        client.disconnect()
        client.loop_stop()
