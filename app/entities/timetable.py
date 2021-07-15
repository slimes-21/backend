from app.entities.subject import Subject


class Timetable:
    def __init__(self, data):
        self.subjects = []
        start = False
        for line in data.splitlines():
            if start:
                self.subjects.append(Subject(line))
            else:
                if 'Subject Code!Description!Group!Activity!Day!Time!Campus!Location!Staff!Duration!Dates' in line:
                    start = True
                    continue
