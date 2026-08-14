import threading

TIMEOUT_SECONDS = 5 * 60  # 5 minutes


class SessionManager:
    """Tracks activity and automatically locks the vault after 5 minutes of
    inactivity. Uses a background thread timer (not just checking timestamps),
    so the lock genuinely takes effect even while the CLI is sitting idle at
    a prompt, rather than only being noticed after the user's next action."""

    def __init__(self, on_timeout):
        self.on_timeout = on_timeout  # function to call when the timeout fires
        self._timer = None
        self._locked = False

    def start(self):
        self._locked = False
        self._reset_timer()

    def _reset_timer(self):
        if self._timer:
            self._timer.cancel()
        self._timer = threading.Timer(TIMEOUT_SECONDS, self._trigger_timeout)
        self._timer.daemon = True  # doesn't block the program from exiting
        self._timer.start()

    def _trigger_timeout(self):
        self._locked = True
        self.on_timeout()

    def record_activity(self):
        """Call this after every user action to reset the inactivity clock."""
        if not self._locked:
            self._reset_timer()

    def is_locked(self):
        return self._locked

    def stop(self):
        if self._timer:
            self._timer.cancel()
