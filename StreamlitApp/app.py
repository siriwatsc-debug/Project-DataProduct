import streamlit as st
import pandas as pd
import numpy as np
import json
from styles import load_css
from utils import init_app_data
from views.navigation import render_navigation
from views.home import home_screen
from views.profile import profile_screen
from views.health_form import health_form_screen
from views.lab_results import lab_results_screen
from views.summary import summary_screen

# Set page configuration
st.set_page_config(
    page_title="Smart Health Checker",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load CSS
load_css()

# Initialize application data
init_app_data()




# Initialize session state for navigation and user management
if 'current_screen' not in st.session_state:
    st.session_state.current_screen = 'home'
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'username' not in st.session_state:
    st.session_state.username = ''
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# Main app logic
def main():
    # Clear any existing query parameters on load
    if "logout" in st.query_params:
        st.query_params.clear()
    
    
    # Check if user is logged in to determine which screens to show
    if not st.session_state.logged_in and st.session_state.current_screen != 'home':
        st.cache_data.clear()
        st.cache_resource.clear()
        st.session_state.clear()
        
        st.session_state.current_screen = 'home'
    
    # Render fixed navigation for logged-in users
    if st.session_state.logged_in:
        render_navigation()
    
    # Display the appropriate screen based on current state
    if st.session_state.current_screen == 'home':
        home_screen()
    elif st.session_state.current_screen == 'profile':
        profile_screen()
    elif st.session_state.current_screen == 'health_form':
        health_form_screen()
    elif st.session_state.current_screen == 'lab_results':
        lab_results_screen()
    elif st.session_state.current_screen == 'summary':
        summary_screen()

if __name__ == "__main__":
    main()