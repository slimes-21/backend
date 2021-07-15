import pandas as pd

classes = pd.read_csv("classes.csv", dtype=str)

class_legend = {"l": "Lecture", "t": "Tutorial", "w": "Workshop", "a": "Applied"}

full_class_name = []
for i in range(0, len(classes)):
    curr_class = classes.loc[i, "class"]
    class_str = ""
    for i in range(0, len(curr_class)):
        if curr_class[i].isalpha():
            class_str += curr_class[i].upper()
        else:
            store = i
            break
    for i in range(store, len(curr_class) - 1):
        class_str += curr_class[i]
    class_str += " "
    class_str += class_legend[curr_class[-1]]
    full_class_name.append(class_str)

classes["class"] = full_class_name

date_legend = {"1": "Monday", "2": "Tuesday", "3": "Wednesday", "4": "Thursday", "5": "Friday"}

full_dates = []
for i in range(0, len(classes)):
    curr_date = classes.loc[i, "date"]
    full_dates.append(date_legend[curr_date])

classes["date"] = full_dates

fixed_time = []
for i in range(0, len(classes)):
    curr_time = str(classes.loc[i, "time"])
    temp_time = ""
    for i in range(0, len(curr_time)):
        temp_time += curr_time[i]
        if i == 1:
            temp_time += ":"
    fixed_time.append(temp_time)

classes["time"] = fixed_time

print(classes)