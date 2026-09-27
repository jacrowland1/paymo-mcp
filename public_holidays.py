#!/usr/bin/env python3
"""
New Zealand public holidays (national + Auckland Anniversary Day).

Source: Employment New Zealand, "Public holidays and anniversary dates"
https://www.employment.govt.nz/leave-and-holidays/public-holidays/public-holidays-and-anniversary-dates
(page last updated 25 September 2026, retrieved 28 September 2026).

`observed` is the date a Monday-Friday worker gets the day off. When a holiday
falls on a weekend the observed date is the Mondayised (or Tuesdayised) date;
someone who normally works that weekend day observes it on the actual date instead.

The source only publishes 2026 and 2027. Dates after COVERED_THROUGH are not
listed here: update the table from the source page each year rather than
calculating them (Easter and Matariki move, and Matariki is set by legislation).
Note: the source lists Anzac Day 2027 as "Saturday 25 April"; 25 April 2027 is a
Sunday. The observed date (Monday 26 April) is unaffected.
"""

from datetime import date, datetime
from typing import Dict, List, Optional

SOURCE_URL = ("https://www.employment.govt.nz/leave-and-holidays/public-holidays/"
              "public-holidays-and-anniversary-dates")
RETRIEVED = "2026-09-28"
COVERED_THROUGH = "2027-12-31"

NATIONAL = "National"
AUCKLAND = "Auckland"

# (name, actual date, observed date for a Mon-Fri worker, region)
_HOLIDAYS = [
    # 2026
    ("New Year's Day",           "2026-01-01", "2026-01-01", NATIONAL),
    ("Day after New Year's Day", "2026-01-02", "2026-01-02", NATIONAL),
    ("Auckland Anniversary Day", "2026-01-26", "2026-01-26", AUCKLAND),
    ("Waitangi Day",             "2026-02-06", "2026-02-06", NATIONAL),
    ("Good Friday",              "2026-04-03", "2026-04-03", NATIONAL),
    ("Easter Monday",            "2026-04-06", "2026-04-06", NATIONAL),
    ("Anzac Day",                "2026-04-25", "2026-04-27", NATIONAL),
    ("King's Birthday",          "2026-06-01", "2026-06-01", NATIONAL),
    ("Matariki",                 "2026-07-10", "2026-07-10", NATIONAL),
    ("Labour Day",               "2026-10-26", "2026-10-26", NATIONAL),
    ("Christmas Day",            "2026-12-25", "2026-12-25", NATIONAL),
    ("Boxing Day",               "2026-12-26", "2026-12-28", NATIONAL),
    # 2027
    ("New Year's Day",           "2027-01-01", "2027-01-01", NATIONAL),
    ("Day after New Year's Day", "2027-01-02", "2027-01-04", NATIONAL),
    ("Auckland Anniversary Day", "2027-02-01", "2027-02-01", AUCKLAND),
    ("Waitangi Day",             "2027-02-06", "2027-02-08", NATIONAL),
    ("Good Friday",              "2027-03-26", "2027-03-26", NATIONAL),
    ("Easter Monday",            "2027-03-29", "2027-03-29", NATIONAL),
    ("Anzac Day",                "2027-04-25", "2027-04-26", NATIONAL),
    ("King's Birthday",          "2027-06-07", "2027-06-07", NATIONAL),
    ("Matariki",                 "2027-06-25", "2027-06-25", NATIONAL),
    ("Labour Day",               "2027-10-25", "2027-10-25", NATIONAL),
    ("Christmas Day",            "2027-12-25", "2027-12-27", NATIONAL),
    ("Boxing Day",               "2027-12-26", "2027-12-28", NATIONAL),
]


def list_holidays(start_date: Optional[str] = None, end_date: Optional[str] = None,
                  region: Optional[str] = AUCKLAND) -> List[Dict[str, str]]:
    """Holidays whose observed date is between start and end (inclusive, YYYY-MM-DD).

    start_date defaults to today; end_date defaults to COVERED_THROUGH.
    region=AUCKLAND includes Auckland Anniversary Day; region=None gives national only.
    """
    start = start_date or date.today().strftime('%Y-%m-%d')
    end = end_date or COVERED_THROUGH
    result = []
    for name, actual, observed, where in _HOLIDAYS:
        if where not in (NATIONAL, region):
            continue
        if start <= observed <= end:
            result.append({
                'name': name,
                'actual': actual,
                'observed': observed,
                'weekday': datetime.strptime(observed, '%Y-%m-%d').strftime('%A'),
                'region': where,
            })
    return result


def observed_dates(start_date: Optional[str] = None, end_date: Optional[str] = None,
                   region: Optional[str] = AUCKLAND) -> List[str]:
    """Observed holiday dates in range, e.g. for use as exclude_dates."""
    return [h['observed'] for h in list_holidays(start_date, end_date, region)]


def is_covered(end_date: str) -> bool:
    """False if end_date is past the last year this table covers."""
    return end_date <= COVERED_THROUGH


if __name__ == '__main__':
    print(f"NZ public holidays + Auckland Anniversary, from today to {COVERED_THROUGH}")
    print(f"Source: {SOURCE_URL} (retrieved {RETRIEVED})\n")
    for h in list_holidays():
        moved = '' if h['actual'] == h['observed'] else f"  (actual {h['actual']})"
        print(f"  {h['observed']}  {h['weekday']:<9}  {h['name']}{moved}")
