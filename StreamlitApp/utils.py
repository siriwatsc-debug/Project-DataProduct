import streamlit as st
import hashlib
from datetime import datetime

from MyPackage.myclass import MyMongoDB

@st.cache_resource (ttl=3600)
def init_mongodb():
    uri = st.secrets['MONGODB']['uri']
    return MyMongoDB(uri)
myMongoDB = init_mongodb()


def init_app_data():
    """Initialize application data in session state"""
    if 'users' not in st.session_state:
        st.session_state.users = {}
    if 'health_data' not in st.session_state:
        st.session_state.health_data = {}

def register_user(username, password, user_info):
    myMongoDB.insert_user(username, password, user_info)
    return True, "Registration successful"

def verify_user(username, password):
    """Verify user credentials"""
    user = myMongoDB.login(username, password)
    if user:
        st.session_state.username = username
        st.session_state.password = password
        st.session_state.users = {}
        user_data = myMongoDB.select_user_info(username)
        user_data['user_id'] = str(user_data['_id'])
        if user_data['user_info'] == None:
            user_data['user_info'] = {}
        
        user_data.pop('_id')
        st.session_state.users[username] = user_data
        return True, "Login successful", user_data['user_id']
    return False, "Invalid username or password", None



from datetime import date
def save_health_record(user_id, record_date, health_data):
    data = health_data
    data['username'] = st.session_state.username
    data['date'] = str(record_date.isoformat())
    myMongoDB.insert_user_health_data(data)

    
    # Add timestamp to health data
    health_data_with_meta = health_data.copy()
    health_data_with_meta['last_updated'] = datetime.now().isoformat()
    
    # Convert date to string for consistent key
    date_key = record_date.isoformat()
    if user_id not in st.session_state.health_data:
        st.session_state.health_data[user_id] = {}
    
    st.session_state.health_data[user_id][date_key] = health_data_with_meta
    
    return True

def save_health_recordxx(user_id, record_date, health_data):
    """Save health record"""
    if user_id not in st.session_state.health_data:
        st.session_state.health_data[user_id] = {}
    
    # Add timestamp to health data
    health_data_with_meta = health_data.copy()
    health_data_with_meta['last_updated'] = datetime.now().isoformat()
    
    # Convert date to string for consistent key
    date_key = record_date.isoformat()
    st.session_state.health_data[user_id][date_key] = health_data_with_meta
    
    return True

import json
def get_user_health_records(user_id):
    user_health_records = myMongoDB.select_user_health_data(st.session_state.username, {})
    st.session_state.health_data[user_id] = {}
    for record in user_health_records:
        st.session_state.health_data[user_id][record['date']] = json.loads(record['str_health_data'])

    """Get all health records for a user"""
    if user_id in st.session_state.health_data:
        return st.session_state.health_data[user_id].copy()
    return {}

def get_latest_health_record(user_id):
    """Get the latest health record for a user"""
    if user_id in st.session_state.health_data and st.session_state.health_data[user_id]:
        records = st.session_state.health_data[user_id]
        latest_date = max(records.keys())
        return records[latest_date].copy()
    return {}

def get_user_profile(user_id):
    """Get user profile information"""
    for username, user_data in st.session_state.users.items():
        if user_data['user_id'] == user_id:
            return {
                'username': username,
                'firstname': user_data['user_info'].get('firstname', ''),
                'lastname': user_data['user_info'].get('lastname', ''),
                'email': user_data['user_info'].get('email', ''),
                'phone': user_data['user_info'].get('phone', '')
            }
    return {}


def save_user_profile():
    myMongoDB.insert_user(st.session_state.username, st.session_state.password, st.session_state.user_info)
    return
    
def update_user_profile(user_id, user_info):
    """Update user profile"""
    # Find user by user_id and update
    for username, user_data in st.session_state.users.items():
        if user_data['user_id'] == user_id:
            user_data['user_info'] = {
                'firstname': user_info['firstname'],
                'lastname': user_info['lastname'],
                'email': user_info['email'],
                'phone': user_info['phone']
            }
            st.session_state.user_info = user_data['user_info']
            save_user_profile()
            return True
    return False

def get_health_status(value, normal_range, value_type="normal"):
    """
    Get health status with appropriate indicators
    value_type: "normal" (within range is good), "high_bad" (high is bad), "low_bad" (low is bad)
    """
    if value_type == "normal":
        # For values where being within range is good
        min_val, max_val = normal_range
        if min_val <= value <= max_val:
            return "✅", "ปกติ", "normal"
        elif value < min_val:
            return "❌", "ต่ำ", "abnormal"
        else:
            return "❌", "สูง", "abnormal"
    
    elif value_type == "high_bad":
        # For values where high is bad (like glucose, cholesterol)
        max_val = normal_range
        if value <= max_val:
            return "✅", "ปกติ", "normal"
        else:
            return "❌", "สูง", "abnormal"
    
    elif value_type == "low_bad":
        # For values where low is bad (like GFR)
        min_val = normal_range
        if value >= min_val:
            return "✅", "ปกติ", "normal"
        else:
            return "❌", "ต่ำ", "abnormal"

def logout_user():
    """Logout user and clear session state"""
    st.session_state.logged_in = False
    st.session_state.user_id = None
    st.session_state.username = ''
    st.session_state.password = ''
    st.session_state.current_screen = 'home'
    st.success("ออกจากระบบเรียบร้อยแล้ว!")
    st.rerun()

def navigate_to(screen):
    st.session_state.current_screen = screen
    st.rerun()
