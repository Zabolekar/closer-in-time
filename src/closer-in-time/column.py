# -*- coding: utf-8
import datetime as dt
from Tkinter import Frame, Label, Entry, Radiobutton


DATE_FORMAT = "%d.%m.%Y"


KEY_TO_DELTA = {
    "Up": 1, "Down": -1,
    "Right": 30, "Left": -30,
    "plus": 365, "minus": -365
}

OPTION_AND_KEY_TO_DELTA = {
    "Up": 3650, "Down": -3650
}


class Column(Frame):
    def __init__(self, parent, label):
        Frame.__init__(self, parent, border=5)
        
        self.name = label # won't work if labels are equal

        self._lab = Label(self, text=label)
        self._lab.pack()

        self._entry = Entry(self)
        self._entry.bind("<Key>", self.on_key)
        self._entry.config(foreground="black")
        self._entry.pack()
        self.set_date(dt.date.today())

        self._rb = Radiobutton(self, text="Fix",
                                     variable=parent.fixed_column_name,
                                     value=self.name)
        self._rb.pack()
        
        parent.fixed_column_name.trace("w", self.on_fix_or_unfix)
        self.parent = parent


    def fix(self):
        self.parent.fixed_column_name.set(self.name)


    def on_fix_or_unfix(self, *args):
        self._entry["state"] = "disabled" if self.fixed else "normal"


    @property
    def fixed(self):
        return self.parent.fixed_column_name.get() == self.name


    @property
    def date(self):
        representation = self._entry.get()
        return dt.datetime.strptime(representation, DATE_FORMAT)


    def set_date(self, value):
        representation = value.strftime(DATE_FORMAT)
        self._entry.delete(0, "end")
        self._entry.insert(0, representation)


    def flash_red(self):            
        self._entry.config(state="normal", foreground="red")
        self.parent.after(100, lambda: self._entry.config(state="disabled",
                                                          foreground="black"))

    def enforce_consistency(self):
        """
        Enforces that the equality b = (a+c)/2 holds,
        and that a <= b <= c holds,
        and that the fixed value is not changed
        (unless it would block other values from changing),
        and that the diff label is up to date
        """
        a, b, c = self.parent.columns
        if not a.fixed and self is not a:
            diff = c.date - b.date
            a.set_date(b.date - diff)
        elif not b.fixed and self is not b:
            diff = (c.date - a.date) / 2
            b.set_date(a.date + diff)
        elif not c.fixed and self is not c:
            diff = b.date - a.date
            c.set_date(b.date + diff)
        self.parent.diff_label["text"] = "Δ = %i" % diff.days

        if diff.days < 0:
            # Change the fixed value. It's an abnormal situation,
            # so we flash the value to get the user's attention.
            self.parent.fixed_column.flash_red()
            self.parent.reset_columns(self.date) # resets diff_label, too


    def on_key(self, event):
    
        if event.keysym == "Meta_L":  # ⌥ key used by itself
            return "break" # to stop event propagation

        delta = None

        if event.state == 16: # ⌥ key used as modifier
            try:
                delta = dt.timedelta(OPTION_AND_KEY_TO_DELTA[event.keysym])
            except KeyError:
                print "Key combination ⌥ %s is not a recognized command" % event.keysym
        else:
            try:
                delta = dt.timedelta(KEY_TO_DELTA[event.keysym])
            except KeyError:
                print "Key %s is not a recognized command" % event.keysym
                
        if delta is not None:
            self.set_date(self.date + delta)
            self.enforce_consistency()
        
        return "break" # to stop event propagation
        


    def temporarily_normal_enter(self):
        self._saved_state = self._entry["state"]
        self._entry["state"] = "normal"
    
    def temporarily_normal_exit(self):
        self._entry["state"] = self._saved_state
