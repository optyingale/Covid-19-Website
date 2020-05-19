from datetime import datetime


def log(log_message):
    now = datetime.now()
    date = now.date()
    current_time = now.strftime("%H:%M:%S")
    with open("logs.txt", 'a') as file:
        file.write(str(date) + "/" + str(current_time) + "\t\t" + log_message +"\n")
