from datetime import datetime
import streamlit as st
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
st.title('COVID-19 Analysis App')
st.subheader('An Analysis of the Indian Corona-Virus Situation')

st.write(' ## **A History of the Virus**')
if st.checkbox('Show/Hide History'):
    st.write('''
            >Coronavirus disease (COVID-19) is an infectious disease caused by a newly discovered coronavirus.

            >Most people infected with the COVID-19 virus will experience mild to moderate respiratory illness and recover without requiring special treatment.  Older people, and those with underlying medical problems like cardiovascular disease, diabetes, chronic respiratory disease, and cancer are more likely to develop serious illness.

            >The best way to prevent and slow down transmission is be well informed about the COVID-19 virus, the disease it causes and how it spreads. Protect yourself and others from infection by washing your hands or using an alcohol based rub frequently and not touching your face.
            The COVID-19 virus spreads primarily through droplets of saliva or discharge from the nose when an infected person coughs or sneezes, so it’s important that you also practice respiratory etiquette (for example, by coughing into a flexed elbow).

            >At this time, there are no specific vaccines or treatments for COVID-19. However, there are many ongoing clinical trials evaluating potential treatments. WHO will continue to provide updated information as soon as clinical findings become available.
            ''')

# A plot of the Age Distribution affected by covid
age_df = pd.read_csv('covid_data\AgeGroupDetails.csv')
age_plt = plt.bar(age_df['AgeGroup'][0:8], (age_df['TotalCases'][0:8] /
                                            age_df['TotalCases'].sum()), width=0.75, color=['#9e9e9e', '#43ba76', '#1f72b2', '#815c3b',  '#b74cd4'])
plt.xlabel('Age Groups')
plt.ylabel('Normalized Num of Cases')
plt.title('An Age Wise Distribution of total Cases')
st.pyplot()

# conclusion
st.write('''As We can see from the graph above the most people who are affected by the Corona Virus in India And the relatively young age groups of **20-29 and 30-39**.
            This is contrary to the popular belief that only older people are susceptible to the virus.
          ''')

# State wise Testing details
state_test_df = pd.read_csv('covid_data\StatewiseTestingDetails.csv')
states = (state_test_df.State.unique()).tolist()
st.write('# Data Analysis')

# Total Sum cases and tests
statewise_total = state_test_df.groupby('State').sum(
).reset_index().sort_values('TotalSamples', ascending=True)
sns.barplot(x='State', y='TotalSamples', data=statewise_total)
plt.xlabel('States')
plt.ylabel('Total Test done in every state(10^7)')
plt.title('Total Cases in every state')
plt.xticks(rotation=90)
st.pyplot()

# select state choice
st.write('# State-Wise Data Analysis')
state_select = st.selectbox("Select State", states)
st.write(" > **Showing Data for ** ", state_select)

df_per_state = state_test_df[state_test_df.State == state_select].drop(
    'Negative', axis=1)
df_per_state.Date = pd.to_datetime(
    df_per_state.Date, infer_datetime_format=True)
start_date = st.selectbox(
    'Select Start Date', options=df_per_state['Date'].tolist(),)
plt.style.use('seaborn-dark')

plt.bar(df_per_state['Date'][(df_per_state['Date'] >= start_date)],
        df_per_state['TotalSamples'][(df_per_state['Date'] >= start_date)], color="#a83832")
plt.xticks(rotation=45)
plt.xlabel('Date')
plt.ylabel('Number of Tests Done')
plt.title(state_select+' test Data')
st.pyplot()

st.header('Cumulative State Data')
total = df_per_state[(df_per_state['Date'] >= start_date)
                     ].groupby('State').sum()
st.write(total)
sns.barplot(y=[total['TotalSamples'], total['Positive']],
            x=['Total Tested', 'Tested Positive'])
plt.yscale('log')
plt.ylabel('Number of People')
plt.title('Stats in ' + state_select)
plt.yticks(ticks=[10, 100, 1000, 10000, 100000,
                  1000000, 10000000, 100000000, 1000000000])
st.pyplot()


# Hospital Bed Data for each state
hospital_df = pd.read_csv('covid_data\HospitalBedsIndia.csv')

st.header('** Hospital Bed Data **')

choice = st.radio('Show India/State Data', options=['India', 'State'])
if choice == 'India':
    status_bed = hospital_df[hospital_df['State/UT'] == 'All India']
    status_bed.drop('Sno', axis=1, inplace=True)
    status_bed.rename(columns={'NumPrimaryHealthCenters_HMIS': "Number of Primary Health Centers",
                               "NumCommunityHealthCenters_HMIS": 'Number of Community Health Centers',
                               "NumSubDistrictHospitals_HMIS": 'Number of District Hospitals',
                               "NumDistrictHospitals_HMIS": 'Number of District Hospitals',
                               "TotalPublicHealthFacilities_HMIS": 'Total Number of Public Health Facilities',
                               'NumPublicBeds_HMIS': 'Number of Public Beds Avaliable',
                               "NumRuralHospitals_NHP18": 'Number of Rural Hospital',
                               'NumRuralBeds_NHP18': 'Number of Rural Beds Avaliable',
                               'NumUrbanHospitals_NHP18': "Number of Urban Hospitals Avaliable",
                               'NumUrbanBeds_NHP18': 'Number of Urban Beds Avaliable'}, inplace=True)
    status_bed.reset_index(inplace=True)
    st.write(status_bed.T)
elif choice == 'State':
    if(state_select != 'Dadra and Nagar Haveli and Daman and Diu'):
        status_bed = hospital_df[hospital_df['State/UT'] == state_select]
        status_bed.drop('Sno', axis=1, inplace=True)
        status_bed.rename(columns={'NumPrimaryHealthCenters_HMIS': "Number of Primary Health Centers",
                                   "NumCommunityHealthCenters_HMIS": 'Number of Community Health Centers',
                                   "NumSubDistrictHospitals_HMIS": 'Number of District Hospitals',
                                   "NumDistrictHospitals_HMIS": 'Number of District Hospitals',
                                   "TotalPublicHealthFacilities_HMIS": 'Total Number of Public Health Facilities',
                                   'NumPublicBeds_HMIS': 'Number of Public Beds Avaliable',
                                   "NumRuralHospitals_NHP18": 'Number of Rural Hospital',
                                   'NumRuralBeds_NHP18': 'Number of Rural Beds Avaliable',
                                   'NumUrbanHospitals_NHP18': "Number of Urban Hospitals Avaliable",
                                   'NumUrbanBeds_NHP18': 'Number of Urban Beds Avaliable'}, inplace=True)
        status_bed.reset_index(inplace=True)
        st.write(status_bed.T)
    else:
        st.warning('No data Avaliable')


status_bed = status_bed.reset_index().melt(id_vars=["index"])
status_bed = status_bed.iloc[2:11, :]

sns.barplot(y="variable", x="value", data=status_bed)
plt.xlabel('Number of Facilities')
plt.ylabel('Avaliability')
plt.title('Medical Care Avaliability in : '+state_select)

st.pyplot()
