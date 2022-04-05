import re
import pandas as pd


def processor(data):
    patterns = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s|\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\sPM\s-\s|\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\sAM\s-\s'

    messages = re.split(patterns, data)[1:]
    dates = re.findall(patterns, data)
    s = dates[0]
    if (s[3] == "/" and s[6] == ',') or (s[5] == '/' and s[8] == ',') or (s[4] == '/' and s[7] == ','):
        date = []
        for s in dates:
            i = s.find(',', 1)
            date.append(s[:i - 2] + "20" + s[i - 2:])
        dates = date

    x = []
    for i in dates:
        y = i.split(',')
        x.append(y)

    date = []
    time = []
    for i in range(len(x)):
        date.append(x[i][0])
        time.append(x[i][1])

    df = pd.DataFrame({'messages': messages, "dates": date, 'time': time})

    sp = []

    def spaceremover(s):
        a = s[1:len(s) - 3]
        sp.append(a)

    df['time'].apply(spaceremover)
    df['time'] = sp

    try:
        df['time'] = pd.to_datetime(df['time'], format='%H:%M').dt.time
    except:
        df['time'] = pd.to_datetime(df['time'], format='%I:%M %p').dt.time
    df['time'] = df['time'].apply(lambda x: str(x))
    df['dates'] = df['dates'] + " " + df['time']
    try:
        df['dates'] = pd.to_datetime(df['dates'], format='%d/%m/%Y %H:%M:%S')
    except:
        df['dates'] = pd.to_datetime(df['dates'], format='%m/%d/%Y %H:%M:%S')

    # convert date into format
    try:
        df['dates'] = pd.to_datetime(df['dates'], format='%d/%m/%Y, %H:%M - ')
    except ValueError as ve:
        df['dates'] = pd.to_datetime(df['dates'], format='%m/%d/%Y, %H:%M - ')
    except:
        df['dates'] = pd.to_datetime(df['dates'], format='%d/%m/%Y, %I:%M %p - ')

    texts = []
    user = []
    for i in df['messages']:
        entry = re.split('([\w\W]+?):\s', i)
        if entry[1:]:
            texts.append(entry[2])
            user.append(entry[1])
        else:
            user.append("Notification")
            texts.append(entry[0])
    df['messages'] = texts
    df['user'] = user
    df['day'] = df['dates'].dt.day_name()
    df['date_only'] = df['dates'].dt.date
    df['year'] = df['dates'].dt.year
    df['month'] = df['dates'].dt.month_name()
    df['date'] = df['dates'].dt.day
    df['hour'] = df['dates'].dt.hour
    df['minute'] = df['dates'].dt.minute
    period = []
    for hour in df[['day', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period
    return df
