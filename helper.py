"""Helper functions for airfare project:
https://github.com/wordswithchung/hackbright-project."""

import calendar
from datetime import date, datetime, timedelta


def calc_months():
    """Function generates the months to display on the homepage. Calculates:
    (1) Two weeks from today (to provide a safety buffer);
    (2) 12 months total in while-loop.

    http://stackoverflow.com/a/12736311
    """

    today = datetime.today()
    months = []

    if today.day < calendar.monthrange(today.year, today.month)[1] / 2:
        months.append(today)

    while len(months) < 12:
        days_in_month = calendar.monthrange(today.year, today.month)[1]
        month = today + timedelta(days=days_in_month)
        months.append(month)
        today = month

    month_names = []
    for month in months:
        m, y = month.month, month.year
        m = calendar.month_name[m]
        month_names.append(m + " " + str(y))

    return months, month_names


def choose_dates(month, year, duration):
    """Figure out the start_date and end_date for the search."""

    today = date.today()
    safe_day = today + timedelta(days=14)

    search_date = safe_day
    c = calendar.monthcalendar(year, month)

    for i in range(4):
        if c[i][1]:
            if date(year, month, c[i][1]) > safe_day:
                search_date = date(year, month, c[i][1])
                break
            else:
                continue

    end_date = search_date + timedelta(days=duration)
    end_date = end_date.strftime("%Y-%m-%d")
    start_date = search_date.strftime("%Y-%m-%d")

    return start_date, end_date


