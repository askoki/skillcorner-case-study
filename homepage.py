import streamlit as st
from helpers.utils import authenticate, add_page_logo, add_sidebar_logo


def main():
    st.title('Task description')
    st.subheader('Streamlit Task (Code)')
    st.markdown(
        '- Adapt the streamlit code to not only upload from a CSV but integrate and retrieve data from the skillcorner API. You can hardcode or make parameters dynamic. The process should be able to extract the data for the 6 competitions you have available. We recommend trying to extract data from at least 2 endpoints (off_ball_runs and physical)')
    st.markdown(
        '- Adapt the streamlit code (below) to use the skillcornerviz library. You can find documentation of the library here')
    st.markdown(
        '- Create an interface to extract insights - feel free to recommend what insights you’d use for a given analysis. You can outline a use case and adapt the tool. Examples could be scouting a player in a set of leagues in a given competition, or enabling the user to create a set of charts to profile players.')
    st.markdown('- Deploy the application (on streamlit) and add some level of security')

    st.subheader('Solution')
    st.markdown('Deployed Streamlit app with basic authentication system and two subpages. One for **team analysis** and exploring your team against the others in the league. The other is for inspecting **individual player** performance and can be used for scouting and assessment.')

if __name__ == "__main__":
    add_page_logo()
    add_sidebar_logo()
    authenticate()
    if st.session_state['authentication_status']:
        main()
