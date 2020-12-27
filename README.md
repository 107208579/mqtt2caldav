<img src="mqtt2caldav.png" width="300" height="131">  

# mqtt2caldav  
This project reads MQTT events and creates predefined CALDAV events.  
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
* CALDAV Server Connection
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
<br />


**CALDAV**  
Specifies the CalDAV server connection.
```
"CALDAV_SERVER_ADDRESS": "https://server.com/remote.php/dav/calendars/user",
"CALDAV_USERNAME": "username",
"CALDAV_PASSWORD": "password"
 ```
<br />
<br />


**MQTT**   
Specifies the MQTT topic and MQTT event string to trigger a calendar event creation.
```
"MQTT_TOPIC": "mqtt/Main_Switch",
"MQTT_EVENT": {"action":"on"},
```
<br />
<br />


**EVENT**  
Specifies details of the calendar event.
```
"EVENT_CALENDAR": "https://server.com/remote.php/dav/calendars/user/todo",
"EVENT_SUMMARY": "Buy Milk",
"EVENT_LOCATION": "1 Street\\, 23456 City\\, Country",
"EVENT_GEO": "1.2489458;103.8343056",
"EVENT_CATEGORY": "Tasks",
"EVENT_URL": "http://buymoremilk.com",
"EVENT_DESCRIPTION": "Dont forget to buy fresh milk!",
```
* List of calendar properties → https://<span></span>icalendar.org/RFC-Specifications/iCalendar-RFC-5545/
<br />
<br />


**EVENT :: Time Zone**  
Specifies the time zone in which calendar events are created.
```
"EVENT_TIMEZONE"
```
* List of time zones → https://<span></span>en.wikipedia.org/wiki/List_of_tz_database_time_zones
<br />
<br />
 
 
**EVENT :: Trigger**  
Specifies a calendar event alarm.
```
"EVENT_TRIGGER"
```
* "" → No alert will be set or configured  
* "0" → Alert will trigger at event start time
* "15" → Alert will trigger 15 minutes before event start time
* ...
<br />
<br />


**EVENT :: Seconds**  
Specifies if the calendar event start time and calendar event end time will have seconds set.
```
"EVENT_SECONDS"
```
* "True" → 12:34:56  
* "False" → 12:34:00   
<br />
<br />


**EVENT :: Rounding**  
Specifies if the calendar event start time has minutes rounded up or down to the closest defined value.
```
"EVENT_ROUNDING"
```
* "1" → 12:42:29 rounds to 12:42:00 and 12:42:30 rounds to 12:43:00
* "5" → 12:42:29 rounds to 12:40:00 and 12:42:30 rounds to 12:45:00 
* "30" → 12:42:29 rounds to 12:30:00 and 12:42:30 rounds to 13:00:00
* ...
<br />
<br />


**EVENT :: Duration**  
Specifies the calendar event duration in minutes.
```
"EVENT_DURATION"
```
* "1" → If event start time is 12:34:00, event end time will be set to 12:35:00
* "10" → If event start time is 12:34:00, event end time will be set to 12:44:00
* "120" → If event start time is 12:34:00, event end time will be set to 14:34:00
* ...
<br />
<br />

