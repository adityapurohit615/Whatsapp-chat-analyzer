import pandas as pd
import re
def preprocess(data):
    pattern = "\d{2}/\d{2}/\d{4},\s\d{1,2}:\d{2}\\u202f(?:am|pm)\s-"
    temp = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)
    for i in range(len(dates)):
        dates[i] = dates[i].replace('\u202f', '')
    df = pd.DataFrame({'message': temp, 'message date': dates})
    df['message date'] = pd.to_datetime(df['message date'], format='%d/%m/%Y, %I:%M%p -')

    user = []
    message = []
    for i in df['message']:
        entry = re.split('^(.*?):', i)
        if entry[1:]:
            user.append(entry[1])
            message.append(entry[2])
        else:
            user.append('group_notification')
            message.append(entry[0])
    df['user'] = user
    df['message'] = message

    df['year'] = df['message date'].dt.year
    df['month'] = df['message date'].dt.month
    df['day'] = df['message date'].dt.day
    df['hour'] = df['message date'].dt.hour
    df['minute'] = df['message date'].dt.minute

    return df