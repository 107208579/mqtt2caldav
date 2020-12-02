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
        for trigger in TRIGGERS:
            client.subscribe(trigger['MQTT_TOPIC'])
    else:
        logger.error("Connection failed")
        print("Connection failed")


def on_message(client, userdata, message):
    logger.info("Message received : " + str(message.payload) + " on " + message.topic)
    print("Message received : " + str(message.payload) + " on " + message.topic)
    my_new_calendar = my_principal.make_calendar(name="Calendar")
    for trigger in TRIGGERS:
        if trigger['MQTT_TOPIC'] == message.topic:
            str_event = """BEGIN:VCALENDAR
            VERSION:2.0
            PRODID:-//Script//EN
            CALSCALE:GREGORIAN
            BEGIN:VEVENT
            DTSTART;TZID={timezone}:20201125T220000
            DTEND;TZID={timezone}:20201125T230000
            UID:D04A88A5-A56A-4FC9-BEDF-A064C18EEB83
            DTSTAMP:20201125T140000Z
            LOCATION:{location}
            DESCRIPTION:{description}
            URL;VALUE=URI:{url}
            SUMMARY:{summary}
            GEO:{geo}
            CATEGORY:{category}
            CREATED:20201125T140000Z
            BEGIN:VALARM
            TRIGGER:-PT{trigger_time}M
            ATTACH;VALUE=URI:Chord
            ACTION:AUDIO
            END:VALARM
            END:VEVENT
            END:VCALENDAR
            """
            str_event = str_event.format(timezone=trigger['EVENT_TIMEZONE'], location=trigger['EVENT_LOCATION'], description=trigger['EVENT_DESCRIPTION'], url=trigger['EVENT_URL'],
                                         summary=trigger['EVENT_SUMMARY'], geo=trigger['EVENT_GEO'], category=trigger['EVENT_CATEGORY'], trigger_time=trigger['EVENT_TRIGGER'])
            # Let's add an event to our newly created calendar
            my_event = my_new_calendar.save_event(str_event)


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
