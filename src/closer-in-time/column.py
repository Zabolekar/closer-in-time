import datetime as dt
from typing import Dict
from contextlib import contextmanager
from tkinter.ttk import Frame, Label, Entry, Radiobutton


DATE_FORMAT = "%d.%m.%Y"


KEY_TO_DELTA: Dict[str, int] = {
    "Up": 1, "Down": -1,
    "Right": 30, "Left": -30,
    "plus": 365, "equal": 365, "KP_Add": 365,
    "minus": -365, "KP_Subtract": -365,
    "Prior": 3650, "Next": -3650
}


class Column(Frame):

    def __init__(self, parent, *, name, label, rb_variable, incremented):
        super().__init__(parent, border=5)

        self.name = name
        self.incremented = incremented

        self._lab = Label(self, text=label)
        self._lab.pack()

        self._entry = Entry(self)
        self._entry.bind("<Key>", self.on_key)
        self._entry.pack()
        self.date = dt.date.today()

        self._rb = Radiobutton(self, text="Fix",
                                     variable=rb_variable,
                                     value=self.name)
        self._rb.pack()


    @property
    def fixed(self) -> bool:
        return self._entry["state"] == "disabled"

    @fixed.setter
    def fixed(self, value: bool) -> None:
        self._entry["state"] = "disabled" if value else "normal"


    @property
    def date(self) -> dt.datetime:
        representation: str = self._entry.get()
        return dt.datetime.strptime(representation, DATE_FORMAT)

    @date.setter
    def date(self, value: dt.datetime) -> None:
        representation: str = value.strftime(DATE_FORMAT)
        with self.temporarily_normal():
            self._entry.delete(0, "end")
            self._entry.insert(0, representation)


    def flash_red(self) -> None:
        self._entry.config(foreground="red")
        self.after(100, lambda: self._entry.config(foreground=""))


    def on_key(self, event) -> str:
        try:
            delta = dt.timedelta(KEY_TO_DELTA[event.keysym])
            self.incremented(self.name, delta)
        except KeyError:
            print(f"Key {event.keysym} is not a recognized command")
        return "break" # to stop event propagation


    @contextmanager
    def temporarily_normal(self):
        state = self._entry["state"]
        self._entry["state"] = "normal"
        yield
        self._entry["state"] = state
