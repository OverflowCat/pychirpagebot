class Message:
    command = ""
    raw = ""
    result = ""

    def __init__(self, command: str, raw: str, result: str):
        self.command = command
        self.raw = raw
        self.result = result

class Logger:
    logs = []

    def __init__(self):
        self.logs = []
    
    def log(self, message: Message):
        self.logs.append(message)
        if (len(self.logs) > 100):
            self.logs.pop(0)
