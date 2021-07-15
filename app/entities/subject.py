class Subject:
    def __init__(self, data):
        attributes = data.split(',')
        if len(attributes) != 12:
            return
        self.code = attributes[1]
        self.group = attributes[3]
        self.activity = attributes[4]
        self.day = attributes[5]
        self.time = attributes[6]
        self.location = attributes[8]
        self.duration = attributes[10]
        print(self.code)
