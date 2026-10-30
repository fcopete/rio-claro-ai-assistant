import json

from pathlib import Path

from config import (
    SAMPLE_DATA_FILE
)

DATA_FILE = Path(
    SAMPLE_DATA_FILE
)


def load_sample_data():

    with open(

        DATA_FILE,

        "r",

        encoding="utf-8"

    ) as file:

        return json.load(
            file
        )