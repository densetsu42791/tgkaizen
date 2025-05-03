class NotAChannelError(Exception):
    """Исключение, если объект — не канал."""


class BotNotAdminError(Exception):
    """Исключение, если бот не является админом канала."""