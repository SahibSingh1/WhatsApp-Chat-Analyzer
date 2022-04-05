from urlextract import URLExtract
extract= URLExtract()
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji
def fetch_stats(selected_user, df):
    if selected_user!="Overall":
        df = df[df['user'] == selected_user]

    total_messages= df.shape[0]

    # word count
    words=[]
    for i in df['messages']:
        words.extend(i.split())

    # media count
    media_count=df[df['messages']=="<Media omitted>\n"].shape[0]

    # links count
    link=[]
    for i in df['messages']:
        link.extend(extract.find_urls(i))

    return total_messages, len(words),media_count,len(link)

def busy_users(df):
    df=df[df['user']!='Notification']
    x=df['user'].value_counts().head()
    ed = df[df['user'] != 'Notification']
    y = round((ed['user'].value_counts() / ed.shape[0]) * 100, 2).reset_index().rename(columns={'index': 'Name', 'user': 'Percentage'})
    return x,y


def wordcloud(df, selected_user):
    if selected_user!="Overall":
        df = df[df['user'] == selected_user]
    df=df[df['messages']!='<Media omitted>\n']
    df=df[df['user'] != 'Notification']

    def remove_stopwords(message):
        f = open('hinglish_stopwords.txt', 'r')
        stopwords = f.read()
        y=[]
        for i in message.lower().split():
            if i not in stopwords:
                y.append((i))
        return " ".join(y)

    df['messages']=df['messages'].apply(remove_stopwords)
    wc=WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    df_wc=wc.generate(df['messages'].str.cat(sep=" "))
    return df_wc
def most_common(selected_user,df):
    if selected_user!="Overall":
        df = df[df['user'] == selected_user]
    df=df[df['messages'] != '<Media omitted>\n']
    df=df[df['user'] != 'Notification']

    f = open('hinglish_stopwords.txt', 'r')
    stopwords = f.read()
    words=[]
    for i in df['messages']:
        for j in i.lower().split():
            if j not in stopwords:
                words.append(j)
    most_used=pd.DataFrame(Counter(words).most_common(20))
    return most_used

def top_emoji(selected_user,df):
    if selected_user!="Overall":
        df = df[df['user'] == selected_user]
    emojis=[]
    for i in df['messages']:
        for j in i.split():
            if j in emoji.UNICODE_EMOJI_ENGLISH:
                emojis.extend(j)
    x=pd.DataFrame(Counter(emojis).most_common(5))
    return x

def monthly_timeline(selected_user,df):
    if selected_user!="Overall":
        df = df[df['user'] == selected_user]
    timeline=df.groupby(['year','month']).count()['messages'].reset_index()
    time=[]

    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i]+"-"+str(timeline['year'][i]))
    timeline['time']=time
    return timeline
def daily_timeline(selected_user,df):
    if selected_user!="Overall":
        df = df[df['user'] == selected_user]
    daily_timeline=df.groupby('date_only').count()['messages'].reset_index()
    return daily_timeline

def weekly_activity(selected_user,df):
    if selected_user!="Overall":
        df = df[df['user'] == selected_user]
    return df['day'].value_counts()



def monthly_activity(selected_user,df):
    if selected_user!="Overall":
        df = df[df['user'] == selected_user]
    return df['month'].value_counts()


def activity_heatmap(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    return user_heatmap
