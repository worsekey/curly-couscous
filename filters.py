from telegram.ext.filters import MessageFilter


class StopFilter(MessageFilter):
    def filter(self, message):
        return 'Stop' in message.text


class StartFilter(MessageFilter):
    def filter(self, message):
        return 'Begin' in message.text


stopfilter = StopFilter()
startfilter = StartFilter()