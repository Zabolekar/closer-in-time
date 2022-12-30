from .column import Column
import datetime as dt
from tkinter import Tk, StringVar
from tkinter.ttk import Label, Button


HOWTO = """Click on an entry and use
    ↑ and ↓ to increment or decrement by one day,
    → and ← to increment or decrement by 30 days,
    + and - to increment or decrement by 365 days,
    PgUp and PgDn to increment or decrement by 3650 days"""


class Window(Tk):

    def __init__(self):

        super().__init__()
        self.wm_title("Date difference")
        self.resizable(0, 0)

        self.fixed_column_name = StringVar()

        self._howto_label = Label(self, justify="center",
                                        text=HOWTO, relief="ridge")
        
        a = Column(self, label="a = b − Δ")
        b = Column(self, label="b = (a + c) / 2")
        c = Column(self, label="c = b + Δ")
        self.columns = (a, b, c)
        
        self.diff_label = Label(self, justify="center", text="Δ = 0")

        self._reset_to_today = lambda: self.reset_columns(dt.date.today())
        self._reset_button = Button(self, text="Reset",
                                          command=self._reset_to_today)

        self._howto_label.pack()

        for column in self.columns:
            column.pack(side="left")
        c.fix()

        self.diff_label.pack(side="bottom", before=a)
        self._reset_button.pack(side="bottom", fill="x", before=self.diff_label)


    def reset_columns(self, target_date):
        for column in self.columns:
            with column.temporarily_normal():
                column.date = target_date
        self.diff_label["text"] = "Δ = 0"


    @property
    def fixed_column(self):
        for column in self.columns:
            if column.fixed:
                return column
