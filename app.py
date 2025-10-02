import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout='wide', page_title='StartUp Analysis')

df = pd.read_csv('startup_clean.csv')

df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d', errors='coerce')
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.day

def load_overall_analysis():
    st.title('Overall Analysis')

st.sidebar.title('Startup Funding Analysis')

option = st.sidebar.selectbox('Select One',['Overall Analysis','Startup','Inverstor'])

if option=='Overall Analysis':
    #btn0 = st.sidebar.button('Show Overall Analysis')
    #if btn0:
        load_overall_analysis()
        col1,col2, col3, col4 = st.columns(4)

        #Load total invested amount
        total_invested_amount = round(df['amount'].sum())
        #Load Maximum invested startup 
        max_invested_amount = df.groupby('startup')['amount'].max().sort_values(ascending=False).head(1).values[0]
        #Average ticketsize
        average_funding = df.groupby('startup')['amount'].sum().mean()
        #total funded startups
        num_startups = df['startup'].nunique()
        with col1:
             st.metric('Total Invested', str(total_invested_amount) + ' '+'Crores')
        with col2:
            st.metric('Maximum Investment', str(max_invested_amount) + ' ' + 'Crores')
        with col3:
            st.metric('Average Funding Received', str(round(average_funding)) + ' ' +'Crores')
        with col4:
            st.metric('Funded Startups',num_startups)
        
        st.header('Month-On-Month Graph')
        selected_option = st.selectbox('Select Type',['Total','Count'])
        if selected_option=='Total':
            temp_df = df.groupby(['year','month'])['amount'].sum().reset_index()
        else:
            temp_df = df.groupby(['year','month'])['amount'].count().reset_index()

        temp_df['x_axis'] = temp_df['month'].astype('str')+ '-' +temp_df['year'].astype('str')

        fig3, ax3 = plt.subplots()
        ax3.plot(temp_df['x_axis'], temp_df['amount'])
        st.pyplot(fig3)



elif option=='Startup':
    #st.sidebar.selectbox('Select Startup',['Byjus','Ola','Flipkart'])
    st.sidebar.selectbox('Select Startup',sorted(df['startup'].unique().tolist()))
    btn1 = st.sidebar.button('Find Startup Details')
    st.title('Startup Analysis')

else:
    def load_investor_details(investor):
        st.title(investor)
        #Load the recent 5 investment of the investor.
        last_five_df = df[df['investors'].str.contains(' IDG Ventures')].head()[['date','startup','Vertical','city','round','amount']]
        st.subheader('Most Recent Investments')
        st.dataframe(last_five_df)

        col1, col2 = st.columns(2)
        with col1:
        #Biggest Investment by the investors in a startup
            big_series = df[df['investors'].str.contains(investor)].groupby('startup')['amount'].sum().sort_values(ascending=False).head()
            st.subheader('Biggest Investments')
            st.bar_chart(big_series)   
        with col2:
            st.subheader('Data')
            st.dataframe(big_series)
        
        #Investment by the investors according to Vertical
        col1,col2=st.columns(2)
        with col1:
            st.subheader('Data')
            vertical_series = df[df['investors'].str.contains(investor)].groupby('Vertical')['amount'].sum().head()
            st.dataframe(vertical_series)
        with col2:
            st.subheader('Sectors invested in')
            fig1,ax1=plt.subplots()
            ax1.pie(vertical_series, labels=vertical_series.index, autopct="%0.01f")
            st.pyplot(fig1)
        
        #Investment by the investors according to Stage Round
        col1,col2=st.columns(2)
        with col1:
            st.subheader('Data')
            round_series = df[df['investors'].str.contains(investor)].groupby('round')['amount'].sum().head()
            st.dataframe(round_series)
        with col2:
            st.subheader('Stage Round')
            fig1,ax1=plt.subplots()
            ax1.pie(round_series, labels=round_series.index, autopct="%0.01f")
            st.pyplot(fig1)
        
        #Invest by the investors according to city
        col1,col2=st.columns(2)
        with col1:
            st.subheader('Data')
            city_series = df[df['investors'].str.contains(investor)].groupby('city')['amount'].sum().head()
            st.dataframe(city_series)
        with col2:
            st.subheader('City')
            fig1,ax1=plt.subplots()
            ax1.pie(city_series, labels=city_series.index, autopct="%0.01f")
            st.pyplot(fig1)
        
        #Invest by the investors according to year
        col1,col2=st.columns(2)
        with col1:
            st.subheader('Data')
            df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d', errors='coerce')
            df['year'] = df['date'].dt.year
            year_series = df[df['investors'].str.contains(investor)].groupby('year')['amount'].sum()
            st.dataframe(year_series)
        with col2:
            st.subheader('Year On Year Investment')
            fig1,ax1=plt.subplots()
            ax1.plot(year_series.index, year_series.values)
            st.pyplot(fig1)





    selected_investor = st.sidebar.selectbox('Investors', sorted(set(df['investors'].str.split(',').sum()))) 
    btn2 = st.sidebar.button('Find Investor Detials')
    if btn2:
        load_investor_details(selected_investor)
