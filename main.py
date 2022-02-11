#!/usr/bin/env python

import sys
import pandas as pd
from datetime import datetime, timedelta, time
import pytz
from icalendar import Calendar, Event
import os

# 常數設定
semesterStartDate = datetime(2022, 2, 14)  # 學期開學日，目前預設為 110-2 開學日
semesterWeeks = 16  # 學期週數，每學期改成 16 週後離下一次暑假又更近了些
###

periodsDict = {
    '0': [time(7, 10), time(8, 0)],
    '1': [time(8, 10), time(9, 0)],
    '2': [time(9, 10), time(10, 0)],
    '3': [time(10, 20), time(11, 10)],
    '4': [time(11, 20), time(12, 10)],
    '5': [time(12, 20), time(13, 10)],
    '6': [time(13, 20), time(14, 10)],
    '7': [time(14, 20), time(15, 10)],
    '8': [time(15, 30), time(16, 20)],
    '9': [time(16, 30), time(17, 20)],
    '10': [time(17, 30), time(18, 20)],
    'A': [time(18, 25), time(19, 15)],
    'B': [time(19, 20), time(20, 10)],
    'C': [time(20, 15), time(21, 5)],
    'D': [time(21, 10), time(22, 0)]
}

weekdayDict = {
    '一': 0,
    '二': 1,
    '三': 2,
    '四': 3,
    '五': 4,
    '六': 5,
    '日': 6
}

srcFile = sys.argv[1]

try:
    destFile = sys.argv[2]
except IndexError:
    destFile = f'courseCal {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}.ics'


# Cleanup raw data
try:
    df_courses = pd.read_csv(srcFile, index_col='流水號')
except:
    raise

df_courses.drop(['簡介影片', '全/半年', '必/選修', '加選方式', '總人數', '選課限制條件',
                '課程網頁', '本學期我預計要選的課程'], axis='columns', inplace=True)

reDateTime = r'(一|二|三|四|五|六)((?:[\d{1,2}ABCD]\,?)*)\((\w*\d*)\)'

df_dateTimeLocation = df_courses['時間教室'].str.extractall(reDateTime).reset_index().rename(columns={'match': 'session', 0: 'weekday', 1: 'periods', 2: 'location'})

periods = df_dateTimeLocation['periods'].str.split(',')
df_dateTimeLocation['period_start'] = [p[0] for p in periods]
df_dateTimeLocation['period_end'] = [p[-1] for p in periods]
df_dateTimeLocation['weekday'].replace(weekdayDict, inplace=True)

df_courses = df_courses.merge(df_dateTimeLocation, on='流水號', how='outer')

# Initialize calendar object
Cal = Calendar()

# Find the date of upcoming weekday by given date
def upcomingWeekday(date, wd):
    daysAhead = wd - date.weekday()

    if daysAhead == 0:
        return date
    elif daysAhead > 0:
        return date + timedelta(wd)
    else:
        return date + timedelta(wd + 7)

# Create course events
def createEvent(row):
    e = Event()

    e.add('summary', row['課程名稱'])
    e.add('location', row['location'])

    dtstart = datetime.combine(
        upcomingWeekday(semesterStartDate, row['weekday']),
        periodsDict[row['period_start']][0],
        tzinfo=pytz.timezone('Asia/Taipei')
    )
    dtend = datetime.combine(
        upcomingWeekday(semesterStartDate, row['weekday']),
        periodsDict[row['period_end']][1],
        tzinfo=pytz.timezone('Asia/Taipei')
    )
    e.add('dtstart', dtstart)
    e.add('dtend', dtend)

    # Recurrence rule
    e.add('rrule', {
        'freq': 'weekly',
        'interval': 1,
        'count': semesterWeeks
    })

    # Generate description of the course
    description = f'{row["課號"]} {row["課程名稱"]}\n授課教師：{row["授課教師"]}'

    if not pd.isna(row['備註']):
        description += f'\n備註：{row["備註"]}'

    e.add('description', description)

    # Append the course event to the calendar
    Cal.add_component(e)


# Go through courses list
df_courses.apply(lambda row: createEvent(row), axis=1)


# Write the calendar into .ics file
ics = open(os.path.join(os.getcwd(), destFile), 'wb')
ics.write(Cal.to_ical())
ics.close()