from ics import Calendar
import requests
from secret import url
import json
from collections import defaultdict

all_shifts = defaultdict(lambda: {"hours": 0.0, "weekend": False})



'''
Requests calendar. Timeout=10 ensures connection closes if no server response.
Returns a Calendar which is a set of events.
'''
def fetch_calendar(url: str) -> Calendar:
    try:
        c = Calendar(requests.get(url, timeout=10).text)
    except Exception as e:
        print(e)
    return c


'''
Sorts a set of Events in ascending dates.
Returns a date ascending orderered list containing Events. 
'''
def sort_shifts_in_set(c: Calendar) -> list:
    events = sorted(c.events, key=lambda event: event.begin)
    return events


'''
Builds the dictionary containing all shifts, their hours and whether it's a weekday or not
'''
def build_all_shifts_dict(events: Calendar):
    for event in events:
        date = event.begin.format("YYYYMMDD")
        
        all_shifts[date]["hours"] += event.duration.total_seconds() / 3600
        
        if event.begin.weekday() >= 5:
            all_shifts[date]["weekend"] = True


def main():
    c = fetch_calendar(url)
    sorted_events = sort_shifts_in_set(c)
    build_all_shifts_dict(sorted_events)
    print(all_shifts)



if __name__ == "__main__":
    main()
