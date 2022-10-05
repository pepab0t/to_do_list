import re
from enum import Enum
from pathlib import Path

PATH: Path = Path(__file__).parent.resolve()

class DateFormat(Enum):
    STANDARD = r'%H:%M %m.%d.%Y'
    NO_HOURS_MINS = r'%m.%d.%Y'

date_pattern: re.Pattern = re.compile(r'^(\d{2})\.(\d{2})\.(\d{4})$')
