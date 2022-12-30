from .column import Column
from .model import Model, WhichDate
import datetime as dt
from tkinter import Tk, StringVar
from tkinter.ttk import Label, Button


HOWTO = """
Click on an entry and use ↑ and ↓ to increment or decrement by one day,
→ and ← to increment or decrement by 30 days,
+ and - to increment or decrement by 365 days,
PgUp and PgDn to increment or decrement by 3650 days
"""


class Window(Tk):

    def __init__(self):

        super().__init__()
        self.wm_title("Date difference")
        self.resizable(0, 0)

        self.model = Model()
        self.fixed_column_name = StringVar()
        self.fixed_column_name.trace_add("write", self.on_fixed_changed)

        self._howto_label = Label(self, justify="center",
                                        text=HOWTO, relief="ridge")

        a = Column(self, name="a", label="a = b - Δ",
                         rb_variable = self.fixed_column_name,
                         incremented=self.on_date_incremented)
        b = Column(self, name="b", label="b = (a+c)/2",
                         rb_variable = self.fixed_column_name,
                         incremented=self.on_date_incremented)
        c = Column(self, name="c", label="c = b + Δ",
                         rb_variable = self.fixed_column_name,
                         incremented=self.on_date_incremented)
        self.columns = (a, b, c)

        self.diff_label = Label(self, justify="center", text="Δ = 0")

        self._reset_button = Button(self, text="Reset",
                                          command=self.model.reset_to_today)

        self._howto_label.pack()

        for column in self.columns:
            column.pack(side="left")

        self.diff_label.pack(side="bottom", before=a)
        self._reset_button.pack(side="bottom", fill="x", before=self.diff_label)

        self.update()


    def on_date_incremented(self, which_date: WhichDate, by_value: dt.timedelta):
        self.model.increment_date(which_date, by_value)
        self.update()


    def on_fixed_changed(self, *args):
        self.model.fixed_date = self.fixed_column_name.get()
        self.update()


    def update(self):
        self.fixed_column_name.set(self.model.fixed_date)

        for column in self.columns:
            column.fixed = self.model.fixed_date == column.name
            column.date = self.model.get_date(column.name)

            if self.model.fixed_date == column.name and self.model.flash_fixed_date:
                column.flash_red()

        self.diff_label["text"] = f"Δ = {self.model.diff.days}"
