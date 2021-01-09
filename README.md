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
* [paho-mqtt](https://pypi.org/project/paho-mqtt/)
* [caldav](https://pypi.org/project/caldav/)
<br />
<br />


## Configuration  
The configuration file is located under `config/config.json` and holds some sample data. 
<br />
<br />


**MQTT :: Connection**  
Specifies the MQTT server connection.
```
"MQTT_SERVER_ADDRESS": "localhost",
"MQTT_SERVER_PORT": "1883",
"MQTT_USERNAME": "username",
"MQTT_PASSWORD": "password"
 ```
<br />
<br />


**CALDAV :: Connection**  
Specifies the CALDAV server connection.
```
"CALDAV_SERVER_ADDRESS": "https://server.com/remote.php/dav/calendars/user",
"CALDAV_USERNAME": "username",
"CALDAV_PASSWORD": "password"
 ```
<br />
<br />


**MQTT :: Trigger**   
Specifies the MQTT topic and MQTT event string to trigger a calendar event creation.
```
"MQTT_TOPIC": "mqtt/Main_Switch",
"MQTT_EVENT": {"action":"on"},
```
<br />
<br />


**EVENT :: Calendar**  
Specifies the calendar in which a calendar event is created.
```
"EVENT_CALENDAR": "https://server.com/remote.php/dav/calendars/user/todo",
```
<br />
<br />


**EVENT :: Summary**  
Specifies the event title.
```
"EVENT_SUMMARY": "Buy Milk",
```
<br />
<br />


**EVENT :: Location**  
Specifies the event location.
```
"EVENT_LOCATION": "1 Street\\, 23456 City\\, Country",
```
<br />
<br />


**EVENT :: Geo**  
Specifies the event location in latitude and longitude GPS coordinates.
```
"EVENT_GEO": "1.2489458;103.8343056",
```
<br />
<br />


**EVENT :: Categories**  
Specifies the category/categories for a calendar event.
```
"EVENT_CATEGORIES": "Appointment",
```
<br />
<br />


**EVENT :: URL**  
Specifies a Uniform Resource Locator (URL) associated with a calendar event.
```
"EVENT_URL": "http://buymoremilk.com",
```
<br />
<br />


**EVENT :: Description**  
Specifies the description for a calendar event.
```
"EVENT_DESCRIPTION": "Dont forget to buy fresh milk!",
```
<br />
<br />


**EVENT :: Transparency**  
Specifies if a calendar event is listed as busy or free.
```
"EVENT_TRANSP"
```
* "OPAQUE" → Busy
* "TRANSPARENT" → Free 
<br />
<br />


**EVENT :: Time Zone**  
Specifies the time zone in which a calendar event is created.
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
Specifies if a calendar event start time and calendar event end time will have seconds set.
```
"EVENT_SECONDS"
```
* "True" → 12:34:56  
* "False" → 12:34:00   
<br />
<br />


**EVENT :: Rounding**  
Specifies if a calendar event start time has minutes rounded up or down to the closest defined value.
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
Specifies a calendar event duration in minutes.
```
"EVENT_DURATION"
```
* "1" → If event start time is 12:34:00, event end time will be set to 12:35:00
* "10" → If event start time is 12:34:00, event end time will be set to 12:44:00
* "120" → If event start time is 12:34:00, event end time will be set to 14:34:00
* ...
<br />
<br />
