import calendar
import sqlite3
print(calendar.monthcalendar(2021, 10))

dates = []
conn = sqlite3.connect(r'C:\Users\BUH8TW\Desktop\thesis\thesis-application\databases\database.db')
c = conn.cursor()
office = c.execute(f'')

month = 1
year = 2022
for i in range(1,13):
    month = i
    for day in calendar.monthcalendar(year, month):
        for i in range(len(day)):
            if day[i] != 0:
                if day[i] < 10 and month < 10:
                    print(f"{year}-{'0'+str(month)}-{'0'+str(day[i])} ", day.index(day[i]) + 1, "patient_id")
                    c.execute(f"INSERT INTO calendar VALUES (strftime('{year}-{'0'+str(month)}-{'0'+str(day[i])}'), {day.index(day[i]) + 1}, 0)")

                elif day[i] < 10 and month >= 10:
                    print(f"{year}-{month}-{'0'+str(day[i])}", day.index(day[i]) + 1, "patient_id")
                    c.execute(f"INSERT INTO calendar VALUES (strftime('{year}-{month}-{'0'+str(day[i])}'), {day.index(day[i]) + 1}, 0)")

                elif day[i] >= 10 and month < 10:
                    print(f"{year}-{'0'+str(month)}-{day[i]}", day.index(day[i]) + 1, "patient_id")
                    c.execute(f"INSERT INTO calendar VALUES (strftime('{year}-{'0'+str(month)}-{day[i]}'), {day.index(day[i]) + 1}, 0)")

                elif day[i] >= 10 and month >= 10:
                    print(f"{year}-{month}-{day[i]}", day.index(day[i]) + 1, "patient_id")
                    c.execute(f"INSERT INTO calendar VALUES (strftime('{year}-{month}-{day[i]}'), {day.index(day[i]) + 1}, 0)")          
                conn.commit()
