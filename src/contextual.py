from dataclasses import dataclass
from datetime import datetime


@dataclass
class Context:
    user_id: int
    now: datetime
    budget_level: str | None = None  # low | mid | high
    time_of_day: str | None = None   # morning | lunch | afternoon | dinner

    def ensure(self):
        if not self.time_of_day:
            h = self.now.hour
            if 6 <= h < 11:
                self.time_of_day = "morning"
            elif 11 <= h < 15:
                self.time_of_day = "lunch"
            elif 15 <= h < 18:
                self.time_of_day = "afternoon"
            else:
                self.time_of_day = "dinner"
        return self




