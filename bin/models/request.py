
class Request:
    def __init__(
            self,
            id,
            dispatcher,
            args,
            hop_limit=1,
            splat_args=False
    ):
        self.id = id

        self.dispatcher = dispatcher
        self.args = args

        self.hops = 0
        self.hop_limit = hop_limit

        self.splat_args = splat_args

    def dispatch(self):
        self.hops += 1

        if self.splat_args:
            ret_val = self.dispatcher(*self.args)
        else:
            ret_val = self.dispatcher(self.args)
        return ret_val

    def correlates_with(self, reply):
        # makes the assumption that whatever reply is it has an "id" field
        # this model is halfway aware of the message construct in the
        # services package but the convenience of this module outweighs
        # whatever principles its existence violates
        return self.id == reply.id

    def expired(self):
        return self.hops >= self.hop_limit
