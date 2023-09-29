import streamlit as st
from streamlit_option_menu import option_menu
from config import Settings
from tools.utilities import load_css, load_html

from views.authentication import Authenticate
from views.dashboard import Dashboard
from views.playground import Playground
from views.courses import Courses
from views.problems import Problems

st.set_page_config(
    page_title = "Gurucool",
    page_icon = "favicon.ico",
    layout="wide"
)


load_css()

class Model:
    menuTitle = "Gurukul"
    option1 = "Dashboard"
    option2 = "Courses Enrolled"
    option3 = "Playground"
    option4 = "Profile"
    option5 = "Problems"

    menuIcon = "menu-up"
    icon1 = "speedometer"
    icon2 = "activity"
    icon3 = "motherboard"
    icon4 = "graph-up-arrow"
    icon5 = "motherboard"

def view(model):

    with st.sidebar:
        menuItem = option_menu(
            model.menuTitle,
            [model.option1, model.option2, model.option3, model.option4, model.option5],
            icons = [model.icon1, model.icon2, model.icon3, model.icon4, model.icon5],
            menu_icon = model.menuIcon,
            default_index = 0,
            styles={
                                   "container": {"padding": "5!important", "background-color": "#fafafa"},
                                   "icon": {"color": "black", "font-size": "25px"},
                                   "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px",
                                                "--hover-color": "#eee"},
                                   "nav-link-selected": {"background-color": "#037ffc"},
                               }

            )
        
    if menuItem == model.option1:
        Dashboard().view(Dashboard.Model())
    
    if menuItem == model.option2:
        Courses().view(Courses.Model())
    
    if menuItem == model.option3:
        Playground().view(Playground.Model())

    if menuItem == model.option4:
        st.write("Profile")
    if menuItem == model.option5:
        Problems().view()
        


authenticator = Authenticate()

if authenticator.authenticate():  # If user is authenticated
    col1, col2 = st.columns([5, 1])  # Create two columns
    with col1:
        pass
    with col2:
        if st.button('Logout'):
            authenticator.logout()
    view(Model)
else:
    pass