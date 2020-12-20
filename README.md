<img src="mqtt2caldav.png" width="300" height="131">  

# mqtt2caldav  
This project reads MQTT events and creates predefined CalDAV events.  
<br />
<br />
<br />



## Licence 
mqtt2caldav is licensed under the [GNU GENERAL PUBLIC LICENSE Version 3](https://github.com/107208579/mqtt2caldav/blob/main/LICENSE.gpl).
<br />
<br />
<br />



## Requirements  
* MQTT Server Connection
* CalDAV Server Connection
<br />
<br />


## Configuration  
**MQTT Server**  
Specifies the MQTT server connection.
```
"MQTT_SERVER_ADDRESS": "localhost",
"MQTT_SERVER_PORT": "1883",
"MQTT_USERNAME": "username",
"MQTT_PASSWORD": "password"
 ```
<br />


**CalDAV Server**  
Specifies the CalDAV server connection.
```
"CALDAV_SERVER_ADDRESS": "https://server.com/remote.php/dav/calendars/user",
"CALDAV_USERNAME": "username",
"CALDAV_PASSWORD": "password"
 ```
<br />


**MQTT Trigger**   
Specifies the MQTT topic and event action to trigger an event creation.
```
"MQTT_TOPIC": "mqtt/Main_Switch_Left_Button",
"MQTT_EVENT": {"action":"on"},
```
<br />


**Event Details**  
Specifies details of the calendar event.
```
"EVENT_CALENDAR": "https://server.com/remote.php/dav/calendars/user/todo",
"EVENT_SUMMARY": "Buy Milk",
"EVENT_LOCATION": "1 Street\\, 23456 City\\, United Country",
"EVENT_GEO": "1.2489458;103.8343056",
"EVENT_CATEGORY": "Tasks",
"EVENT_URL": "http://buymoremilk.com",
"EVENT_DESCRIPTION": "Dont forget to buy fresh milk!",
```
<br />


**Event Details :: Time Zone**  
Specifies the time zone in which events are created.
* List of time zones → https://<span></span>en.wikipedia.org/wiki/List_of_tz_database_time_zones
```
"EVENT_TIMEZONE": "Asia/Singapore",
```
<br />
 
 
**Event Details :: Trigger**  
Specifies if and when when an event alarm triggers.  
* "" → No alert will be set or configured  
* "0" → Alert will trigger at event start time (DTSTART)  
* "15" → Alert will trigger 15 minutes before event start time (DTSTART)  
* ...
```
"EVENT_TRIGGER": "15",
```
<br />


**Event Details :: Seconds**  
Specifies if event start time (DTSTART) and event end time (DTEND) will have seconds set or default to '00'.  
* "True" → 12:34:56  
* "False" → 12:34:00   
```
"EVENT_SECONDS": "True",
```
<br />


**Event Details :: Rounding**  
Specifies if the event start time (DTSTART) has minutes rounded to the closest defined value.
* "1" → 12:42:29 rounds to 12:42:00 and 12:42:30 rounds to 12:43:00
* "5" → 12:42:29 rounds to 12:40:00 and 12:42:30 rounds to 12:45:00 
* "30" → 12:42:29 rounds to 12:30:00 and 12:42:30 rounds to 13:00:00
* ...
```
"EVENT_ROUNDING": "5",
```
<br />


**Event Details :: Duration**  
Specifies the event duration in minutes.
* "1" → If event start time (DTSTART) is 12:34:00, event end time (DTEND) will be set to 12:35:00
* "10" → If event start time (DTSTART) is 12:34:00, event end time (DTEND) will be set to 12:44:00
* "120" → If event start time (DTSTART) is 12:34:00, event end time (DTEND) will be set to 14:34:00
* ...
```
"EVENT_DURATION": "10",
```
<br />
