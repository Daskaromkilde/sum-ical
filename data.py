from ics import Calendar, Event
import requests
from secret import url
import json
from collections import defaultdict
import os
from datetime import datetime





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
def sort_shifts_in_set(c: Calendar) -> list[Event]:
    events = sorted(c.events, key=lambda event: event.begin)
    return events




def merge_shift_history(history: dict, current_shifts: dict) -> dict:
    today = datetime.now().strftime("%Y%m%d")

    for date, shift in current_shifts.items():
        if date < today:
            history[date] = shift

    return history



def save_dict_to_json(all_shifts: dict):
    json_str = json.dumps(all_shifts, indent=4)
    with open("shifts.json", 'w') as f:
        f.write(json_str)



def load_json_to_dict() -> dict:
    if not os.path.exists("shifts.json"):
        return {}
    
    with open("shifts.json", "r") as f:
        return json.load(f)



'''
Builds the dictionary containing all shifts, their hours and whether it's a weekday or not
'''
def build_current_shifts(events: list[Event]) -> dict:
    current_shifts = {}

    for event in events:
        if event.begin is None or event.duration is None:
            continue

        date = event.begin.format("YYYYMMDD")

        current_shifts[date] = {
            "hours": event.duration.total_seconds() / 3600,
            "weekend": event.begin.weekday() >= 5
        }

    return current_shifts


def loop(history: dict) -> dict:
    calendar = fetch_calendar(url)
    sorted_events = sort_shifts_in_set(calendar)

    current_shifts = build_current_shifts(sorted_events)

    return merge_shift_history(history, current_shifts)



def print_debug_json(history: dict) -> None:
    print(f"{'Date':<12} {'Hours':>8} {'Weekend':>8}")
    print("-" * 32)

    for date, shift in sorted(history.items()):
        formatted_date = f"{date[:4]}-{date[4:6]}-{date[6:]}"
        weekend = "Yes" if shift["weekend"] else "No"

        print(f"{formatted_date:<12} {shift['hours']:>8.2f} {weekend:>8}")


def main():
    # TODO add loop + sleep
    history = load_json_to_dict()

    print_debug_json(history)

    history = loop(history)

    print()
    print()
    print()

    print_debug_json(history)

    save_dict_to_json(history)




if __name__ == "__main__":
    main()
