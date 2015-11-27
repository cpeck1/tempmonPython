class RequestBuffer:
    def __init__(self):
        self.requests = []

    def append(self, request):
        self.requests.append(request)

    def clear(self):
        self.requests = []

    def remove_expired(self):
        self.requests = [req for req in self.requests if not req.expired()]

    def dispatch_all(self):
        self.remove_expired()

        for request in self.requests:
            request.dispatch()

    def process_reply(self, reply):
        for i in range(len(self.requests)):
            if self.requests[i].correlates_with(reply):
                del self.requests[i]
                return

