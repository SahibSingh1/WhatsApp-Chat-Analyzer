import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt

st.sidebar.title("WhatsApp Chat Analyzer")
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
     # To read file as bytes:
     bytes_data = uploaded_file.getvalue()
     data=bytes_data.decode('utf-8')

     df=preprocessor.processor(data)

     # fetching unique users
     user_list=df['user'].unique().tolist()
     user_list.remove('Notification')
     user_list.sort()
     user_list.insert(0,"Overall")
     selected_user=st.sidebar.selectbox("Analysis with respect to",user_list)

     # stats stuff
     if st.sidebar.button("Start Analysis"):
          st.title("Top Statistics")
          col1, col2, col3, col4= st.columns(4)
          total_messages,word_count,media_count,link_count=helper.fetch_stats(selected_user,df)
          with col1:
               st.header("Total Messages")
               st.subheader(total_messages)
          with col2:
               st.header("Total Words")
               st.subheader(word_count)
          with col3:
               st.header("Media shared")
               st.subheader(media_count)
          with col4:
               st.header("Links shared")
               st.subheader(link_count)

     # monthly time line
          timeline=helper.monthly_timeline(selected_user,df)
          st.title("Monthly Timeline")
          fig,ax=plt.subplots()
          ax.plot(timeline['time'],timeline['messages'],color='green')
          plt.xticks(rotation='vertical')
          st.pyplot(fig)
     # daily timeline
          daily_timeline = helper.daily_timeline(selected_user, df)
          st.title("Daily Timeline")
          fig, ax = plt.subplots()
          ax.plot(daily_timeline['date_only'], daily_timeline['messages'], color='red')
          plt.xticks(rotation='vertical')
          st.pyplot(fig)

     # weekly activity map
          st.title("Activity Map")
          col1,col2=st.columns(2)
          with col1:
               st.header("Days")
               busy_day=helper.weekly_activity(selected_user,df)
               fig,ax= plt.subplots()
               ax.bar(busy_day.index,busy_day.values,color='coral')
               plt.xticks(rotation='vertical')
               st.pyplot(fig)


          with col2:
               st.header("Months")
               busy_month = helper.monthly_activity(selected_user,df)
               fig, ax = plt.subplots()
               ax.bar(busy_month.index, busy_month.values,color='bisque')
               plt.xticks(rotation='vertical')
               st.pyplot(fig)



     # busiest users (only applicable on group, not individual)
          if selected_user=="Overall":
               st.title("Busiest Users")
               x,new_df=helper.busy_users(df)
               fig,ax=plt.subplots()

               col1,col2=st.columns(2)
               with col1:
                    ax.bar(x.index, x.values,color='olive')
                    plt.xticks(rotation='vertical')
                    st.pyplot(fig)
               with col2:
                    st.dataframe(new_df)
                    
          # heat map
          st.title("Weekly Activity Map")
          user_heatmap = helper.activity_heatmap(selected_user,df)
          fig,ax = plt.subplots()
          ax = sns.heatmap(user_heatmap)
          st.pyplot(fig)
          
          # word cloud
          word_cloud=helper.wordcloud(df,selected_user)
          fig, ax=plt.subplots()
          ax.imshow(word_cloud)
          st.title("Word Cloud")
          st.pyplot(fig )
          most_common=helper.most_common(selected_user,df)
          fig,ax=plt.subplots()
          ax.barh(most_common[0],most_common[1],color='skyblue')
          plt.xticks(rotation='vertical')
          st.title("Most Comon Words")
          st.pyplot(fig)

          # emojis
          emoji_df=helper.top_emoji(selected_user,df)
          st.title("Emoji Analysis")
          if emoji_df.empty:
               st.subheader("This person sent 0 emoji")
          else:
               col1,col2=st.columns(2)
               with col1:
                    st.dataframe(emoji_df)
               with col2:
                    fig, ax=plt.subplots()
                    ax.pie(emoji_df[1],labels=emoji_df[0],autopct="%0.2f")
                    st.pyplot(fig)
