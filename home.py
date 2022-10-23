import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px

plt.style.use('seaborn-v0_8')

st.set_page_config(
    page_title= 'Air Quality Analytic Dashboard',
    page_icon = '📅',
    layout= 'wide'
)

@st.cache
def load_data_df1():
    df1 = pd.read_csv('datasets/site_272.csv',index_col=0, parse_dates=['From Date','To Date'])
    df1.set_index('From Date', inplace=True)
    df1.rename(columns={'WD (deg)':'WD (degree)'},inplace=True)
    return df1

@st.cache
def load_data_df2():
    df2 = pd.read_csv('datasets/site_277.csv',index_col=0, parse_dates=['From Date','To Date'])
    df2.set_index('From Date', inplace=True)
    df2.rename(columns={'WD (deg)':'WD (degree)'},inplace=True)
    return df2


df1 = load_data_df1()
df2 = load_data_df2()

st.title("Air Quality Analytic Dashboard")
st.subheader("by Rehbar Abbas")

st.sidebar.title("Option Sidebar")

if st.sidebar.checkbox("show data 1"):
    st.dataframe(df1)

if st.sidebar.checkbox('show data 1 Analysis'):
    cols = df1.columns.to_list()
    graphs = ['line','area','bar','funnel']
    cols.remove('To Date')
    
    sel_col = st.sidebar.radio("select a column",cols)
    sel_graph = st.selectbox("select graph type", graphs)
    if sel_graph == graphs[0]:
        fig = px.line(df1, x=df1.index, y=sel_col, title=f"{sel_col} line chart from data 1" )
    elif sel_graph == graphs[1]:
        fig = px.area(df1, x=df1.index, y=sel_col, title=f"{sel_col} area chart from data 1" )
    elif sel_graph == graphs[2]:

        df1_monthly = df1.resample('M').sum()
        fig = px.bar(df1_monthly, x=df1_monthly.index, y=sel_col, title=f"{sel_col} month wise bar chart from data 1" )
    elif sel_graph == graphs[3]:
        df1_monthly = df1.resample('M').sum()
        fig = px.funnel(df1_monthly, x=df1_monthly.index, y=sel_col, title=f"{sel_col}  month wise funnel chart from data 1" )
    st.plotly_chart(fig, use_container_width=True)
    

# last me
if st.sidebar.checkbox("Show Comparison between data"):
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(25,5), squeeze=False)
    df1['PM2.5 (ug/m3)'].resample('M').sum().plot(kind='area', ax=ax[0,0])
    df2['PM2.5 (ug/m3)'].resample('M').sum().plot(kind='area', ax=ax[0,1])
    st.pyplot(fig, clear_figure=True)
