import datetime
import sys

import requests


# we maintain the time as the number of minutes since the midnight
def parse_time_to_norm(timestr):
    parts = timestr.split(":")
    if len(parts) != 2:
        raise Exception(f'unexpected time format "{timestr}"')
    return int(parts[0]) * 60 + int(parts[1])


class Truck:
    def __init__(
        self, dayorder, start24, end24, applicant, location, **kwargs
    ):
        self.start = parse_time_to_norm(start24)
        self.end = parse_time_to_norm(end24)
        self.dayorder = int(dayorder)
        self.applicant = applicant
        self.location = location

    @property
    def name(self):
        return self.applicant

    def is_open(self, dayorder, time):
        return self.dayorder == dayorder and self.start <= time < self.end

    def __str__(self):
        return f"{self.applicant} ({self.location})"


def do_work(url, chunk_size, interactive):
    now = datetime.datetime.now()
    # Api's weekdays start with 1
    norm_dayorder = now.weekday() + 1
    # our time is the number of minutes since the midnight
    norm_time = now.hour * 60 + now.minute
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(
            f"cannot pull the data from Api, status {response.statuc_code}"
        )
    trucks_json = response.json()
    trucks = [Truck(**item) for item in trucks_json]
    filtered = (
        truck for truck in trucks if truck.is_open(norm_dayorder, norm_time)
    )
    ordered = sorted(filtered, key=lambda truck: truck.name)
    for chunk in range(0, len(ordered), chunk_size):
        for item in ordered[chunk : chunk + chunk_size]:  # noqa
            print(item)
        if interactive and chunk + chunk_size < len(ordered):
            print("ENTER to continue...")
            input()


if __name__ == "__main__":
    url = "https://data.sfgov.org/resource/bbb8-hzi6.json"
    chunk_size = 10
    try:
        do_work(url, chunk_size, True)
    except Exception as ex:
        sys.stderr.write(ex)
