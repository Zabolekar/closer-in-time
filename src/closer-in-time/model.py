from typing import Literal
import datetime as dt


WhichDate = Literal["a", "b", "c"]


class Model:

    _dates: dict[WhichDate, dt.datetime]

    fixed_date: WhichDate
    flash_fixed_date: bool


    @property
    def diff(self) -> dt.timedelta:
        return self._dates["b"] - self._dates["a"]


    def __init__(self):
        self.fixed_date = "c"
        self.reset_to_today()


    def get_date(self, which_date: WhichDate) -> dt.datetime:
        return self._dates[which_date]


    def set_date(self, which_date: WhichDate, value: dt.datetime) -> None:
        assert which_date != self.fixed_date, "Cannot set the fixed date!"

        self._dates[which_date] = value

        if which_date != "a" and self.fixed_date != "a":
            diff = self._dates["c"] - self._dates["b"]
            self._dates["a"] = self._dates["b"] - diff
        elif which_date != "b" and self.fixed_date != "b":
            diff = (self._dates["c"] - self._dates["a"]) / 2
            self._dates["b"] = self._dates["a"] + diff
        elif which_date != "c" and self.fixed_date != "c":
            diff = self._dates["b"] - self._dates["a"]
            self._dates["c"] = self._dates["b"] + diff

        if diff.days < 0:
            # Change the fixed value. It's an abnormal situation,
            # so we flash the value to get the user's attention.
            self.reset_dates(value)
            self.flash_fixed_date = True
        else:
            self.flash_fixed_date = False


    def increment_date(self, which_date: WhichDate, by_value: dt.timedelta) -> None:
        value = self._dates[which_date] + by_value
        self.set_date(which_date, value)


    def reset_dates(self, value: dt.datetime) -> None:
        self._dates = { d: value for d in ["a", "b", "c"] }
        self.flash_fixed_date = False


    def reset_to_today(self) -> None:
        self.reset_dates(dt.date.today())
