class EventBus:

    def __init__(self):
        self.subscribers = dict()

    def register(self, event_class, callback):
        self.subscribers[event_class] = callback

    def publish(self, event):
        event_class = event.__class__.__name__
        if event_class in self.subscribers:
            for callback in self.subscribers[event_class]:
                callback(event)