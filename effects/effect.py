from components.messages import MessageType


class Effect(object):
    def __init__(self, uid, name, duration, potency, stack=False):
        self.uid = uid
        self.name = name
        self.duration = duration
        self.potency = potency
        self.stack = stack

    def on_start(self, host):
        pass

    def on_end(self, host):
        pass

    def update(self, host):
        pass

    def __str__(self):
        return "{}:{} {}s".format(self.name, abs(self.potency), self.duration)


class AlterStatEffect(Effect):
    def __init__(self, uid, name, duration, potency, stat_altered, stack=False):
        super().__init__(uid, name, duration, potency, stack)
        self.stat_altered = stat_altered

    def update(self, host):
        host.transmit_message(self, MessageType.AlterStat, stat_altered=self.stat_altered, potency=self.potency)

    def copy(self):
        return AlterStatEffect(
            uid=self.uid, name=self.name, duration=self.duration, potency=self.potency, stack=self.stack,
            stat_altered=self.stat_altered
        )


class AlterNeedEffect(Effect):
    def __init__(self, uid, name, duration, potency, need_altered, stack=False):
        super().__init__(uid, name, duration, potency, stack)
        self.need_altered = need_altered

    def update(self, host):
        host.transmit_message(self, MessageType.AlterNeed, need_altered=self.need_altered, potency=self.potency)

    def copy(self):
        return AlterNeedEffect(
            uid=self.uid, name=self.name, duration=self.duration, potency=self.potency, stack=self.stack,
            need_altered=self.need_altered
        )
