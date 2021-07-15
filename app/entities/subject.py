class Subject:
    def __init__(self, data):
        attributes = data.split('!')
        self.code = attributes[1]
        self.group = attributes[3]
        self.activity = attributes[4]
        self.day = attributes[5]
        self.time = attributes[6]
        self.location = attributes[8]
        self.duration = attributes[10]

    def __eq__(self, other):
        if not isinstance(other, Subject):
            return False
        return self.code == other.code and self.group == other.group and self.activity == other.activity and self.day == other.day and self.time == other.time and self.location == other.location and self.duration == other.duration

    def __ne__(self, other):
        return self.__eq__(other)
