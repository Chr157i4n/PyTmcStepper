try:
    import _thread
except ImportError:
    # Dummy _thread module for environments without threading support
    class _thread:
        @staticmethod
        def start_new_thread(func, args):
            func(*args)


class Thread:
    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None):
        self.target = target
        self.args = args
        self.kwargs = {} if kwargs is None else kwargs

    def start(self):
        _thread.start_new_thread(self.run, ())

    def run(self):
        self.target(*self.args, **self.kwargs)
