import curses
import time

class UIElement:
    def __init__(self, label, outputfunc):
        self.label = label
        self.outputfunc = outputfunc

class UIAction:
    def __init__(self, key, label, func):
        self.key = key
        self.label = label
        self.func = func

class UIScreen:
    def __init__(self, refresh_rate=1):
        self.stdscr = curses.initscr()
        self.refresh_rate = refresh_rate
        self.last_refresh = 0
        curses.noecho()
        curses.cbreak()
        self.stdscr.nodelay(True)
        self.elements = []
        self.actions = []
        self.key2actions = {}
        self.last_ch = -1
        self.elements_win = curses.newwin(1, 42, 0, 0)
        self.action_win = curses.newwin(1, 42, 1, 1)

    def _element_lines(self):
        lines = []
        for elem in self.elements:
            lines += [elem.label]
            lines += elem.outputfunc().splitlines()
        return lines

    def _read_key(self):
        ch = self.stdscr.getch()
        if ch > 0 and ch != self.last_ch:
            key = chr(ch)
            if key in self.key2actions:
                self.key2actions[key].func()
        self.last_ch = ch

    def _refresh_actions(self):
        if not self.actions:
            return
        win = self.action_win
        win.erase()
        _, w = win.getmaxyx()
        win.addnstr(0, 0, "Menu:", w)
        y = 1
        for action in self.actions:
            win.addnstr(y, 0, "{} - {}".format(action.key, action.label), w)
            y+= 1
        win.refresh()

    def _refresh_elements(self):
        self.last_refresh = time.time()
        win = self.elements_win
        win.erase()
        _, w = win.getmaxyx()
        for y, line in enumerate(self._element_lines()):
            win.addnstr(y, 0, line, w)
        win.refresh()

    def _resize_windows(self):
        h, w = self._win_elements_size()
        self.elements_win.resize(h, w)
        self.action_win.mvwin(h + 2, 0)
        self.action_win.resize(*self._win_actions_size())
        self.last_refresh = 0
        self.refresh()

    def _win_elements_size(self):
        lines = self._element_lines()
        h = len(lines)
        # Let's give ourselves a little buffer of 4 chars...
        w = max((len(line) for line in lines), default=1) + 4
        return (h, w)

    def _win_actions_size(self):
        h = len(self.actions) + 1
        # 5 chars are for key prefixes
        w = max((len(a.label) for a in self.actions), default=1) + 5
        return (h, w)

    def stop(self):
        curses.nocbreak()
        curses.echo()
        curses.endwin()

    def add_element(self, label, outputfunc):
        self.elements.append(UIElement(label, outputfunc))
        self._resize_windows()

    def add_action(self, key, label, func):
        self.actions.append(UIAction(key, label, func))
        self.key2actions = {a.key: a for a in self.actions}
        self._resize_windows()
        self._refresh_actions()

    def refresh(self):
        if time.time() - self.last_refresh >= self.refresh_rate:
            self._refresh_elements()
            self.stdscr.refresh()

        self._read_key()

