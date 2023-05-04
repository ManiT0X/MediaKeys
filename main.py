import tkinter as tk
import win32api
import win32con


class AlwaysOnTop(tk.Toplevel):
    def __init__(self, master=None, cnf={}, **kw):
        tk.Toplevel.__init__(self, master, cnf, **kw)
        self.wm_attributes("-topmost", 1)
        self.bind("<FocusIn>", self.check_focus)

    def check_focus(self, event=None):
        self.attributes("-topmost", 1)


class MediaControl(AlwaysOnTop):
    def __init__(self, master=None):
        AlwaysOnTop.__init__(self, master)
        self.overrideredirect(True)  # Remove title bar and close button
        self.attributes("-alpha", 0.5)  # Set window transparency
        self.geometry("200x60")  # Set window size and position
        self.resizable(False, False)

        # Set button styles
        button_style = {"bg": "#ecf0f1", "activebackground": "#bdc3c7", "fg": "#2c3e50", "activeforeground": "#2c3e50"}

        self.play_button = tk.Button(self, text="Play/Pause", width=10, command=self.play_pause)
        self.play_button.pack(side=tk.LEFT, padx=10)

        self.prev_button = tk.Button(self, text="<<", width=5, command=self.prev_track)
        self.prev_button.pack(side=tk.LEFT)

        self.next_button = tk.Button(self, text=">>", width=5, command=self.next_track)
        self.next_button.pack(side=tk.LEFT)

        # Bind mouse events for dragging the window
        self.bind("<ButtonPress-1>", self.on_drag_start)
        self.bind("<ButtonRelease-1>", self.on_drag_stop)
        self.bind("<B1-Motion>", self.on_drag_motion)

        # Initialize variables for dragging
        self._dragging = False
        self._start_x = None
        self._start_y = None

    def play_pause(self):
        # Send the play/pause media key
        win32api.keybd_event(0xB3, 0, win32con.KEYEVENTF_EXTENDEDKEY, 0)
        win32api.keybd_event(0xB3, 0, win32con.KEYEVENTF_EXTENDEDKEY | win32con.KEYEVENTF_KEYUP, 0)

    def prev_track(self):
        # Send the previous track media key
        win32api.keybd_event(0xB1, 0, win32con.KEYEVENTF_EXTENDEDKEY, 0)
        win32api.keybd_event(0xB1, 0, win32con.KEYEVENTF_EXTENDEDKEY | win32con.KEYEVENTF_KEYUP, 0)

    def next_track(self):
        # Send the next track media key
        win32api.keybd_event(0xB0, 0, win32con.KEYEVENTF_EXTENDEDKEY, 0)
        win32api.keybd_event(0xB0, 0, win32con.KEYEVENTF_EXTENDEDKEY | win32con.KEYEVENTF_KEYUP, 0)

    def on_drag_start(self, event):
        # Start dragging the window
        self._dragging = True
        self._start_x = event.x
        self._start_y = event.y

    def on_drag_stop(self, event):
        # Stop dragging the window
        self._dragging = False

    def on_drag_motion(self, event):
        if self._dragging:
            x = self.winfo_x() + (event.x - self._start_x)
            y = self.winfo_y() + (event.y - self._start_y)
            self.geometry(f"+{x}+{y}")


if __name__ == '__main__':
    root = tk.Tk()
    root.withdraw() # Hide the default Tkinter root window
    app = MediaControl(root)
    app.bind("<Control-q>", lambda event: app.destroy())
    app.mainloop()
