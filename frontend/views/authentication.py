import streamlit as st
import requests
from config import Settings
# Constants


settings = Settings()

class Authenticate:

    def __init__(self):
        self.DEFAULT_URL = settings.BACKEND_URLS["default"]
        self.LOGIN_URL = settings.BACKEND_URLS["default"] + "/auth/login"
        self.SIGNUP_URL = settings.BACKEND_URLS["default"] + "/auth/signup"
        self.ME_URL = settings.BACKEND_URLS["default"] + "/auth/me"

        if 'authToken' not in st.session_state:
            st.session_state.authToken = None
    
    def login(self, email, password):
        payload = {"email" : email, "password" : password}
        response = requests.post(self.LOGIN_URL, json = payload)
        if response.status_code == 200:
            st.session_state.authToken = response.json().get("authToken")
            st.success("Logged in Successfully")
        else:
            st.error("Failed to Login. Please check your credentials later.")
    
    def signup(self, name, email, password):
        payload = {"name": name, "email": email, "password": password}
        response = requests.post(self, self.SIGNUP_URL, json=payload)
        if response.status_code == 200:
            st.session_state.authToken = response.json().get("authToken")
            st.success("Signed up successfully!")
        else:
            st.error("Failed to signup. Please check your input.")
    
    def authorized_request(self, method, url, **kwargs):
        headers = kwargs.get("headers", {})
        headers.update({"Authorization" : f"Bearer {st.session_state.authToken}"})
        kwargs["headers"] = headers
        return requests.request(method, url, **kwargs)
    
    def logout(self):
        st.session_state.authToken = None
        st.success("Logged out successfully!")
        st.experimental_rerun()  # Rerun the app to show the login page
    
    def authenticate(self):
        st.title("Welcome to Gurukul")
        if st.session_state.authToken:
            return True  # User is authenticated
        with st.container():
            col1, col2, col3 = st.columns([1,2,1])
            with col2:
                st.markdown("<div class='box'>", unsafe_allow_html=True)
                st.markdown("<h2>Login or Signup</h2>", unsafe_allow_html=True)
                email = st.text_input("Email")
                password = st.text_input("Password", type="password")
                
                if st.button("Login"):
                    self.login(email, password)
                
                name = st.text_input("Name")
                if st.button("Signup"):
                    self.signup(name, email, password)
                st.markdown("</div>", unsafe_allow_html=True)
            
            if st.session_state.authToken:
                if st.sidebar.button('Logout'):
                    self.logout()
            return False  # User is not authenticated