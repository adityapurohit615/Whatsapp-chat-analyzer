import streamlit as st
import preprocess2,helper
import matplotlib.pyplot as plt

st.sidebar.title('WhatsApp Chat Analysis')
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    #now this file that came is a stream and so we have to convert it in
    #utf-8 format
    data = bytes_data.decode("utf-8")
df = preprocess2.preprocess(data)
# st.dataframe(df)


users = df['user'].unique().tolist()
users.remove('group_notification')
users.insert(0,"Overall")
selected_user = st.sidebar.selectbox('Data representation wrt',users)

if st.sidebar.button("Show Analysis"):
    num_messages,words,media,urls = helper.fetch_data(selected_user,df)

    col1,col2,col3,col4 = st.columns(4)

    with col1:
        st.markdown("## Total Messages", unsafe_allow_html=True)
        st.title(num_messages)

    with col2:
        st.markdown("## Total Words", unsafe_allow_html=True)
        st.title(words)

    with col3:
        st.markdown("## Media Shared", unsafe_allow_html=True)
        st.title(media)

    with col4:
        st.markdown("## URLs Shared", unsafe_allow_html=True)
        st.title(urls)

#timeline
    st.title("Monthly Timeline")
    timeline = helper.monthly_timeline(selected_user,df)

    fig,ax = plt.subplots()
    ax.plot(timeline['time'], timeline['message'])
    plt.xticks(rotation='vertical')
    st.pyplot(fig)


    if selected_user == 'Overall':

        st.title("Most Busy Users")
        x,new_df = helper.most_busy_user(df)
        fig,ax = plt.subplots()

        col1, col2 = st.columns(2)


        with col1:
            ax.bar(x.index, x.values)
            st.pyplot(fig)
        with col2:
            st.dataframe(new_df)

#     WordCloud
#     st.title("Word Cloud")
#     df_wc = helper.create_wordcloud(selected_user,df)
#     fig,ax = plt.subplots()
#     ax.imshow(df_wc)
#     st.pyplot(fig)

    

#   most used words
    st.title("most used words")
    most_used_words_df = helper.most_used_words(selected_user,df)

    fig,ax = plt.subplots()

    ax.bar(most_used_words_df[0],most_used_words_df[1])
    plt.xticks(rotation = 'vertical')


    st.pyplot(fig)




