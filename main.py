import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import plotly.express as px

df = pd.read_csv('video_games_sales_copy.csv')
df = df.dropna()
df = df[df['year'] >= 2000]
df = df[df['year'] <= 2015]
df['year'] = df['year'].astype(int)
df['year'] = df['year'].astype(str)

genre_list = sorted(df['genre'].unique().tolist())
year_list = sorted(df['year'].unique().tolist(), reverse=True)


st.set_page_config(page_title='Video Game Sales', page_icon=':🎮:', initial_sidebar_state='expanded', layout='wide')

st.sidebar.markdown('## Select Genre ')
menu_genre = st.sidebar.selectbox('select', genre_list)

st.sidebar.markdown('## Select Year ')
menu_year = st.sidebar.selectbox('select', year_list)

df = df[df['genre'].isin([menu_genre])]
df = df[df['year'].isin([menu_year])]
df.drop_duplicates(subset=['name'], inplace=True)

publisher_counts = df['publisher'].value_counts().head(10)
platform_counts = df['platform'].value_counts()

platform_pivot = df.pivot_table(index='platform', values='global_sales', aggfunc='sum')
platform_pivot = platform_pivot.sort_values(by='global_sales', ascending=False)

publisher_pivot = df.pivot_table(index='publisher', values='global_sales', aggfunc='sum')
publisher_pivot = publisher_pivot.sort_values(by='global_sales', ascending=False)
publisher_pivot = publisher_pivot.nlargest(10, 'global_sales').reset_index()

new_df = df.sort_values(by='global_sales', ascending=False).head(10)



table = new_df[['name', 'global_sales']]
table['global_sales'] = table['global_sales']

st.write('<style>table{border-collapse: collapse;}' \
         'th, td{text-align: center; padding: 1px;}' \
         'th{background-color: #e7ecf1; color: #FFF;}' \
         '</style>', unsafe_allow_html=True)


st.markdown('<h4 style="text-align: center;color: gray;">Top 10 Video Games for {} in {} </h4>'.format(menu_genre, menu_year ), unsafe_allow_html=True)
st.write('---')

col1, col2 = st.columns([1,2])
with col1:
    st.table(table)
with col2:
    fig = px.bar(new_df, x='global_sales', y='name',text_auto='.2',orientation='h')
    fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)

    st.plotly_chart(fig)

st.write('---')


st.markdown('<h4 style="text-align: center;color: gray;">Number of Games per Publisher for {} Games in {} </h4>'.format(menu_genre, menu_year ), unsafe_allow_html=True)
st.write('---')
col1, col2 = st.columns([1,2])
with col1:
    st.table(publisher_counts)
with col2:
    fig = px.bar(publisher_counts, x=publisher_counts.values, y=publisher_counts.index,text_auto='.2',orientation='h')
    fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)

    st.plotly_chart(fig)

st.write('---')

st.markdown('<h4 style="text-align: center;color: gray;">Global Sales per Publisher for {} Games in {} </h4>'.format(menu_genre, menu_year ), unsafe_allow_html=True)
st.write('---')
col1, col2 = st.columns([1,2])
with col1:
    st.table(publisher_pivot)
with col2:
    fig = px.bar(publisher_pivot, x=publisher_pivot['global_sales'], y=publisher_pivot.index,text_auto='.2',orientation='h')
    fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)

    st.plotly_chart(fig)

st.write('---')



st.markdown('<h4 style="text-align: center;color: gray;">Number of Games per Platform for {} Games in {} </h4>'.format(menu_genre, menu_year ), unsafe_allow_html=True)
st.write('---')
col1, col2 = st.columns([1,2])
with col1:
    st.table(platform_counts)
with col2:
    fig = px.bar(platform_counts, x=platform_counts.values, y=platform_counts.index,text_auto='.2',orientation='h')
    fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)

    st.plotly_chart(fig)

st.write('---')


st.markdown('<h4 style="text-align: center;color: gray;">Global Sales per Platform for {} Games in {} </h4>'.format(menu_genre, menu_year ), unsafe_allow_html=True)
st.write('---')
col1, col2 = st.columns([1,2])
with col1:
    st.table(platform_pivot)
with col2:
    fig = px.bar(platform_pivot, x=platform_pivot['global_sales'], y=platform_pivot.index,text_auto='.2',orientation='h')
    fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)

    st.plotly_chart(fig)

st.write('---')

st.markdown('<h4 style="text-align: center;color: gray;">Snapshot of Dataframe </h4>', unsafe_allow_html=True)
st.dataframe(df)