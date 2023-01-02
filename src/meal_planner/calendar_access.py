"""Connect to an iCal database and return a list of Events."""

import datetime

import icalevents.icalparser
from icalevents.icalparser import parse_events
from icalevents.icaldownload import ICalDownload

Event_List = list[icalevents.icalparser.Event]


class ICalConnection:
    def __init__(self, calendar_url: str):
        self._calendar_url = calendar_url
        self._fix_apple = "icloud" in calendar_url
        self._all_events = None
        self._ical = None
        self._today = datetime.datetime.now().date()

    @property
    def all_events(self) -> Event_List:
        return self._parse_events()

    def get_n_events_starting_today(self, number_of_days: int = 7) -> Event_List:
        delta = datetime.timedelta(days=number_of_days-1)
        return self._parse_events(number_of_days=delta, start_date=self._today)

    def _get_ical(self):
        if not self._ical:
            self._ical = ICalDownload().data_from_url(self._calendar_url, self._fix_apple)

    def _parse_events(
            self,
            number_of_days: datetime.timedelta | None = None,
            start_date: datetime.date | None = None
    ) -> Event_List:
        self._get_ical()
        if number_of_days is None:
            number_of_days = datetime.timedelta(days=31)
        if start_date is None:
            start_date = self._today

        initial_response = parse_events(self._ical, start=start_date, default_span=number_of_days)
        events = self._clean_events(initial_response)
        return events

    def _clean_events(self, initial_response: Event_List) -> Event_List:
        events = []
        for event in initial_response:
            start_date = event.start.date()
            if start_date >= self._today:
                events.append(event)
        events = sorted(events, key=lambda x: x.start)
        return events

