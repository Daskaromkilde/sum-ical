from ics import Calendar
import requests
from .secret import url
import json


try:
    c = Calendar(requests.get(url, timeout=10).text)
except Exception as e:
    print(e)


events = sorted(c.events, key=lambda event: event._begin)

for event in events:
    date = event._begin.format("YYYY-MM-DD HH:mm")

event1 = events[0]
event2 = events[1]


print(event1.duration)

print((event1.duration.total_seconds()/3600) * 150)

print((event1.duration).total_seconds()/3600)