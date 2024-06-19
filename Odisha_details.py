import streamlit as st
import pandas as pd
import plotly.express as px

def ac_lss(selected_option, data):
    data['votes'] = pd.to_numeric(data['votes'], errors='coerce')
    states = data['state'].unique()
    if selected_option in states:
        st.subheader('General Election to Parliamentary Constituencies: Trends & Results June-2024')
        col1, col2, col3 = st.columns([2, 3, 2])
        with col1:
            st.empty()
        with col2:
            st.subheader(f":red[{selected_option}]", divider="blue")
        with col3:
            st.empty()
        df_state = data[data['state'] == selected_option]
        constituencies = sorted(df_state['constituency'].unique())
        constituency_details = []
        for constituency in constituencies:
            df_constituency = df_state[df_state['constituency'] == constituency]
            df_constituency = df_constituency.sort_values(by='votes', ascending=False)
            leading_candidate = df_constituency.iloc[0]['name']
            leading_party = df_constituency.iloc[0]['party_name']
            trailing_candidate = df_constituency.iloc[-1]['name']
            trailing_party = df_constituency.iloc[-1]['party_name']
            margin = df_constituency.iloc[0]['votes'] - df_constituency.iloc[1]['votes']
            status = 'Result Declared'
            constituency_details.append({
                'Constituency': constituency,
                'Leading Candidate': leading_candidate,
                'Leading Party': leading_party,
                'Trailing Candidate': trailing_candidate,
                'Trailing Party': trailing_party,
                'Margin': margin,
                'Status': status
            })
        constituency_details_df = pd.DataFrame(constituency_details)
        st.dataframe(constituency_details_df, hide_index=True, use_container_width=True)
    else:
        st.write("State not found in the data.")

def odisha_show():
    data = pd.read_csv('data/secpageda.csv')
    st.subheader(f':red[Odisha Election Results]', divider="blue")
    won_data = data[data['won_status'] == 'won']
    stat_data = won_data[won_data['state'] == 'Odisha']
    parties_colors = [
        {"name": "Independent", "short_name": "IND", "color": "#808080"},
        {"name": "Communist Party of India  (Marxist)", "short_name": "CPI(M)", "color": "#FF0000"},
        {"name": "Indian National Congress", "short_name": "INC", "color": "#00A2E8"},
        {"name": "Biju Janata Dal", "short_name": "BJD", "color": "#008000"},
        {"name": "Bharatiya Janata Party", "short_name": "BJP", "color": "#FF9933"},
        {"name": "Yuvajana Sramika Rythu Congress Party", "short_name": "YSRCP", "color": "#00BFFF"},
        {"name": "Janasena Party", "short_name": "JSP", "color": "#FF4500"},
        {"name": "Telugu Desam", "short_name": "TDP", "color": "#FFD700"},
    ]
    party_info = {party["name"]: {"short_name": party["short_name"], "color": party["color"]} for party in parties_colors}

    def get_winners_by_state(state_name):
        state_winners = won_data[won_data['state'] == state_name]
        return state_winners[['won_status', 'party_name']]

    selected_option = 'Odisha'
    state_winners_data = get_winners_by_state(selected_option)
    party_counts = state_winners_data['party_name'].value_counts()

    cols = st.columns(len(party_counts))
    st.subheader(":red-background[Party Wise Results]")
    for col, (party, count) in zip(cols, party_counts.items()):
        party_info_entry = party_info.get(party, {"color": "transparent", "short_name": party})
        color = party_info_entry["color"]
        short_name = party_info_entry["short_name"]
        with col:
            st.markdown(f"""
            <div style="background-color:{color}; text-align:center; border: 1px solid black; margin: 5px; padding: 10px;">
                <p><strong>{short_name}</strong></p>
                <p>{count}</p>
            </div>
            """, unsafe_allow_html=True)

    party_counted = pd.DataFrame({
        'party_name': party_counts.index,
        'won': party_counts.values,
        'leading': [0] * len(party_counts),
        'total': party_counts.values
    })
    party_counteds = pd.DataFrame({
        'party': party_counts.index,
        'won': party_counts.values,
        'leading': [0] * len(party_counts),
        'total': party_counts.values
    })

    col7, col8 = st.columns([2, 2])
    with col7:
        st.dataframe(party_counted,use_container_width=True)
    with col8:
        col9, col10 = st.columns([2, 3])
        with col9:
            st.subheader(f':red-background[Constituency Wise Results]')
        with col10:
            st.write('I am coming soon')

    col11, col12 = st.columns([2, 2])
    with col11:
        st.subheader(':red-background[Party Wise Vote Share]')
        state_data = data[data['state'] == selected_option]
        result_df = state_data[['constituency', 'party_name', 'votes']].drop_duplicates()
        fig2 = px.pie(result_df, values='votes', names='party_name', color='party_name',
                      color_discrete_map={party["name"]: party["color"] for party in parties_colors})
        fig2.update_traces(hole=0.4, sort=False, hoverinfo='label', textinfo='none', showlegend=False)
        fig2.update_layout(height=500, width=700)
        st.plotly_chart(fig2)

    with col12:
        st.subheader(":red-background[Party Wise Results]")
        fig3 = px.pie(party_counteds, values='won', names='party', color='party',
                      color_discrete_map={party["name"]: party["color"] for party in parties_colors})
        fig3.update_traces(hole=0.4, sort=False, hoverinfo='label', textinfo='none', showlegend=False)
        fig3.update_layout(height=500, width=700)
        st.plotly_chart(fig3)
       

    od_button = st.button('All Constituencies at a glance', use_container_width=True, type="primary")
    if od_button:
        ac_lss('Odisha', data)