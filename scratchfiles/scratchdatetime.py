from datetime import datetime, timedelta


test = datetime.strptime('2025-01-01','%Y-%m-%d')

start_datetime = datetime.strptime('2025-01-01','%Y-%m-%d')
end_datetime = datetime.strptime('2025-01-03','%Y-%m-%d')

current_datetime = start_datetime

diff_days = (end_datetime-start_datetime).days

dayslist = []

while (diff_days+1) > 0:
    dayslist.append(current_datetime)
    current_datetime += timedelta(days=1)
    diff_days -= 1

print(dayslist)