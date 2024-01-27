import streamlit as st

from service import FootballService

st.title('JAK MIERNOTY WYPADAJĄ NA TLE WIELKIEJ CHELSEA')

fs = FootballService()


@st.cache_data
def load_data():
    df = fs.get_data_agg()
    bio_df = fs.get_bio()
    tmp = df.join(bio_df.set_index('playerID'), on='playerID', lsuffix='p')
    tmp = tmp[['name', 'minutesPlayed', 'goals', 'assists', 'GA', 'goals_p90', 'assists_p90', 'GA_p90']]
    tmp.sort_values(by='GA_p90', inplace=True, ascending=False)
    return tmp

data_load_state = st.text('Loading data...')
data = load_data()
data_load_state.text('')
st.dataframe(data, hide_index= True)
