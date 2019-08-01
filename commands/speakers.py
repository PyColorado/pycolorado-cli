import os
import csv as csvlib
import json
from datetime import timedelta, datetime
import math

import requests
from tqdm import tqdm
from tabulate import tabulate

from common.constants import PYCO_SPEAKERS_JSON_URL, PYCO_FIRST_DAY, PYCO_TIMEZONE
from api.buffer import Buffer


def __speakers_content():
    return requests.get(PYCO_SPEAKERS_JSON_URL).json()


def show():
    print(tabulate(__speakers_content(), headers="keys", tablefmt="fancy_grid"))


def from_csv(input_csv):

    output = []

    with open(input_csv, encoding="utf8") as csv_file:
        csv_reader = csvlib.reader(csv_file, delimiter=',')
        header_row = next(csv_reader)
        headers = [x.lower() for x in header_row]
        for row in csv_reader:
            output.append(dict(zip(headers, row)))

    base_path = os.path.dirname(os.path.abspath(input_csv))
    base_filename, _ = os.path.splitext(os.path.basename(input_csv))

    output_filename = f'{base_filename}-{datetime.now().strftime("%Y%m%d-%H%M%S")}.json'
    output_path = os.path.join(base_path, output_filename)

    with open(output_path, 'w') as f:
        json.dump(output, f)

    print(f"{output_path} successfully generated.")


def schedule_buffer():

    buff = Buffer()

    # We're sharing just on twitter
    share_accounts = [buff.twitter()]

    # We want our last post to occur no later than the day before PyCO
    now = datetime.now(tz=PYCO_TIMEZONE)
    last_post_on = PYCO_FIRST_DAY - timedelta(days=1)
    days_from_now_until_last_post = (last_post_on - now).days

    speaker_list = __speakers_content()

    interval = math.floor(days_from_now_until_last_post / float(len(speaker_list)))

    with tqdm(speaker_list, unit="speaker") as speaker_iter:
        for idx, speaker_data in enumerate(speaker_iter):
            speaker_iter.set_description(f"Processing {speaker_data['speaker']}...")

            speaker_first_name, speaker_last_name = map(
                lambda x: x.lower(), speaker_data["speaker"].split(" ", maxsplit=1)
            )

            shareable = (
                f"https://pycolorado.org/shareables/{speaker_last_name}_shareable.jpg"
            )

            speaker_handle = (
                speaker_data.get("twitter_handle", None) or speaker_data["speaker"]
            )

            if speaker_data["type"] == "Keynote":
                text = f"Speaker Highlight: {speaker_handle} will be giving a keynote titled \"{speaker_data['title'].strip()}\" at #PyColorado. You won't want to miss it! Join us on September 6, 7, and 8th! https://ti.to/pycolorado/pycolorado-2019"
            else:
                text = f"Speaker Highlight: {speaker_handle} will be talking about {speaker_data['title'].strip()} at #PyColorado. Join us on September 6, 7, and 8th! https://ti.to/pycolorado/pycolorado-2019"

            # Share at 8:30am on the day in question
            share_at = now.replace(hour=8, minute=30) + timedelta(
                days=(interval * idx) + 1
            )

            buff.create_post(
                profiles=share_accounts,
                text=text,
                photo_url=shareable,
                scheduled_at=share_at,
            )

        print("Done!")

