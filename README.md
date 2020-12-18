# mqtt2caldav
Converts an MQTT event to a CalDAV event.


## Requirements
* MQTT Broker Connection
* CalDAV Server Connection


## Configuration
**MQTT Broker**
```
"MQTT_SERVER_ADDRESS": "localhost",
"MQTT_SERVER_PORT": "1883",
"MQTT_USERNAME": "username",
"MQTT_PASSWORD": "password"
 ```

**CalDAV Server**
```
"CALDAV_SERVER_ADDRESS": "https://server.com/remote.php/dav/calendars/user",
"CALDAV_USERNAME": "username",
"CALDAV_PASSWORD": "password"
 ```

**MQTT Trigger**
```
"MQTT_TOPIC": "mqtt/Main_Button_Left",
"MQTT_EVENT": {"action":"on"},
```

**Event Details**
```
"EVENT_CALENDAR": "https://server.com/remote.php/dav/calendars/user/todo",
"EVENT_SUMMARY": "Buy Milk",
"EVENT_LOCATION": "1 Street\\, 23456 City\\, United Country",
"EVENT_GEO": "1.2489458;103.8343056",
"EVENT_CATEGORY": "Tasks",
"EVENT_URL": "http://buymoremilk.com",
"EVENT_DESCRIPTION": "Dont forget to buy fresh milk!",
"EVENT_TIMEZONE": "Asia/Singapore",
```
     
**Event Details :: Trigger**
Specifies when when an event alarm will trigger. Value set is minutes before event start time (DTSTART).
```
"EVENT_TRIGGER": "15",
```

**Event Details :: Seconds**
Specifies if event start time (DTSTART) and event end time (DTEND) should have seconds set accuratley or to '00'.
```
"EVENT_SECONDS": "True",
```

**Event Details :: Rounding**
Specifies if the event start time (DTSTART) and event end time (DTEND) should have minutes rounded to the closest defined value.
```
"EVENT_ROUNDING": "5",
```

**Event Details :: Duration**
Specifies the event duration in minutes.
```
"EVENT_DURATION": "10"
```
