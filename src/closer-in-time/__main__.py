import datetime as dt
from typing import Dict
from contextlib import contextmanager
from tkinter import Tk, StringVar
from tkinter.ttk import Frame, Label, Entry, Button, Radiobutton

root = Tk()
root.wm_title("Date difference")
root.resizable(0, 0)

DATE_FORMAT = "%d.%m.%Y"
KEY_TO_DELTA: Dict[str, int] = {
    "Up": 1, "Down": -1,
    "Right": 30, "Left": -30,
    "plus": 365, "minus": -365,
    "Prior": 3650, "Next": -3650
}

who_is_fixed = StringVar()

class Column(Frame):
    def __init__(self, parent, *, label):
        super().__init__(parent, border=5)
        
        self.name = label # won't work if labels are equal

        self._lab = Label(self, text=label)
        self._lab.pack()

        self._entry = Entry(self)
        self._entry.bind("<Key>", self.on_key)
        self._entry.pack()
        self.date = dt.date.today()

        self._rb = Radiobutton(self, text="Fix",
                                    variable=who_is_fixed,
                                    value=self.name)
        self._rb.pack()
        
        who_is_fixed.trace("w", self.on_fix_or_unfix)
        
    def fix(self) -> None:
        who_is_fixed.set(self.name)

    def on_fix_or_unfix(self, *args) -> None:
        self._entry["state"] = "disabled" if self.fixed else "normal"

    @property
    def fixed(self) -> bool:
        return who_is_fixed.get() == self.name

    @property
    def date(self) -> dt.datetime:
        representation: str = self._entry.get()
        return dt.datetime.strptime(representation, DATE_FORMAT)

    @date.setter
    def date(self, value: dt.datetime) -> None:
        representation: str = value.strftime(DATE_FORMAT)
        self._entry.delete(0, "end")
        self._entry.insert(0, representation)

    def flash_red(self):
        self._entry.config(foreground="red")
        root.after(100, lambda: self._entry.config(foreground=""))
        
    def enforce_consistency(self) -> None:
        """
        Enforces that the equality b = (a+c)/2 holds,
        and that a <= b <= c holds,
        and that the fixed value is not changed
        (unless it would block other values from changing),
        and that the diff label is up to date
        """
        diff: dt.timedelta
        if not a.fixed and self is not a:
            diff = c.date - b.date
            a.date = b.date - diff
        elif not b.fixed and self is not b:
            diff = (c.date - a.date)/2
            b.date = a.date + diff
        elif not c.fixed and self is not c:
            diff = b.date - a.date
            c.date = b.date + diff
        diff_label["text"] = f"Δ = {diff.days}"

        if diff.days < 0:
            # Change the fixed value. It's an abnormal situation,
            # so we flash the value to get the user's attention.
            fixed_column().flash_red()
            reset_columns(self.date) # resets diff_label, too

    def on_key(self, event) -> str:

        try:
            delta = dt.timedelta(KEY_TO_DELTA[event.keysym])
            self.date += delta
            self.enforce_consistency()
        except KeyError:
            print(f"Key {event.keysym} is not a recognized command")
        
        return "break" # to stop event propagation
        
    @contextmanager
    def temporarily_normal(self):
        state = self._entry["state"]
        self._entry["state"] = "normal"
        yield
        self._entry["state"] = state

def reset_columns(target_date):
    for column in a, b, c:
        with column.temporarily_normal():
            column.date = target_date
    diff_label["text"] = "Δ = 0"

reset_to_today = lambda: reset_columns(dt.date.today())

def fixed_column():
    for column in a, b, c:
        if column.fixed:
            return column

howto = """
Click on an entry and use ↑ and ↓ to increment or decrement by one day,
→ and ← to increment or decrement by 30 days,
+ and - to increment or decrement by 365 days,
PgUp and PgDn to increment or decrement by 3650 days
"""

howto_label = Label(root, justify="center", text=howto, relief="ridge")
a = Column(root, label="a = b - Δ")
b = Column(root, label="b = (a+c)/2")
c = Column(root, label="c = b + Δ")
diff_label = Label(root, justify="center", text="Δ = 0")
reset_button = Button(root, text="Reset", command=reset_to_today)

howto_label.pack()
a.pack(side="left")
b.pack(side="left")
c.pack(side="left")
c.fix()
diff_label.pack(side="bottom", before=a)
reset_button.pack(side="bottom", fill="x", before=diff_label)

root.mainloop()
