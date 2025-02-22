import streamlit as st

from streamlit_authenticator import Authenticate


def authenticate():
    credentials = {
        'usernames': {}
    }
    for user in st.secrets.auth.users:
        single_cred_dict: dict = {}
        single_cred_dict[user['username']] = {
            'email': user['email'],
            'name': user['name'],
            'password': user['password']
        }
        credentials['usernames'].update(single_cred_dict)

    authenticator = Authenticate(
        credentials,
        st.secrets.auth.cookie['name'],
        st.secrets.auth.cookie['key'],
        st.secrets.auth.cookie['expiry_days'],
    )
    authenticator.login()

    if st.session_state['authentication_status']:
        authenticator.logout()
        st.write(f'Welcome *{st.session_state["name"]}*')
    elif st.session_state['authentication_status'] is False:
        st.error('Username/password is incorrect')
    elif st.session_state['authentication_status'] is None:
        st.warning('Please enter your username and password')
