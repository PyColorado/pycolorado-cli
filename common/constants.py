from datetime import datetime
from pytz import timezone

PYCO_TIMEZONE = timezone("US/Mountain")
PYCO_FIRST_DAY = datetime(year=2019, month=9, day=7, tzinfo=PYCO_TIMEZONE)
PYCO_SPEAKERS_JSON_URL = "https://raw.githubusercontent.com/PyColorado/pycolorado.org/production/src/data/schedule.json"

