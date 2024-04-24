from urlextract import URLExtract
# from wordcloud import WordCloud
import pandas as pd
from collections import Counter

def fetch_data(selected_user,df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]
    # fetch the total number of messages sent by a user
    num_messages = df['message'].shape[0]

    # fetch the total number of words written by a user
    words=[]
    for message in df['message']:
        words.extend(message)

    #fetch the number of media messages sent by the user
    media_sent = df[df['message'] == ' <Media omitted>\n'].shape[0]

    #Fetch number of links shared
    urls = []
    url = URLExtract()
    for links in df['message']:
        urls.extend(url.find_urls(links))

    return num_messages, len(words), media_sent, len(urls)

def most_busy_user(df):
    # returning the dataframe of the users who have the most messages
    x = df['user'].value_counts().head()

    df = round((df['user'].value_counts() / df.shape[0])*100,2).reset_index().rename(columns = {'user':'names','count':'percent'})
    return x,df
# def create_wordcloud(selected_user,df):
#
#     if selected_user != 'Overall':
#         df[df['user'] == selected_user]
#
#
#     # for that lets first create a database with no rows with group notification and media omitted values
#     temp = df[df['user'] != 'group_notification']
#     temp = temp[temp['message'] != ' <Media omitted>\n']
#
#
#     wc = WordCloud(width = 500, height = 500, min_font_size=10,background_color='white')
#     df_wc = wc.generate(temp['message'].str.cat(sep=" "))
#     return df_wc
def most_used_words(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()
    # stop_words = stop_words.split()

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != ' <Media omitted>\n']

    words = []
    for word in temp['message']:
        words.extend(word.split())

    words2 = [word for word in words if word.lower() not in stop_words]

    return_df = pd.DataFrame(Counter(words2).most_common(20))

    return return_df

def monthly_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month num', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append((timeline['month'][i]) + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline







