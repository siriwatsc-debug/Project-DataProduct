import streamlit as st
import pandas as pd
import hashlib
import json
from datetime import datetime

# Plotly imports - make sure to install plotly first
try:
    import plotly.express as px
    import plotly.graph_objects as go
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False
    px = None
    go = None

# Set page configuration
st.set_page_config(
    page_title="Smart Health Checker",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #2E86AB;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.8rem;
        color: #A23B72;
        margin-bottom: 1rem;
    }
    .section-header {
        font-size: 1.4rem;
        color: #2E86AB;
        margin-bottom: 1rem;
        padding: 0.5rem;
        background-color: #f0f8ff;
        border-radius: 5px;
    }
    .login-container {
        max-width: 400px;
        margin: 0 auto;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        background-color: #f9f9f9;
    }
    .image-placeholder {
        width: 100%;
        height: 200px;
        background-color: #e0e0e0;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 10px;
        margin-bottom: 1rem;
        color: #666;
    }
    .nav-container {
        display: flex;
        justify-content: center;
        margin-bottom: 2rem;
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .nav-button {
        flex: 1;
        margin: 0 0.5rem;
        padding: 0.75rem 1rem;
        background-color: #2E86AB;
        color: white;
        border: none;
        border-radius: 8px;
        cursor: pointer;
        font-size: 1rem;
        text-align: center;
        transition: all 0.3s ease;
        border: 2px solid transparent;
    }
    .nav-button:hover {
        background-color: #1B5E7A;
        transform: translateY(-2px);
    }
    .nav-button.active {
        background-color: #A23B72;
        border: 2px solid #dc3545;
        box-shadow: 0 4px 8px rgba(220, 53, 69, 0.3);
        font-weight: bold;
    }
    .register-button {
        background-color: #A23B72;
    }
    .register-button:hover {
        background-color: #7A2D56;
    }
    .logout-button {
        background-color: #dc3545;
        color: white;
        border: none;
        padding: 0.75rem 1rem;
        border-radius: 8px;
        cursor: pointer;
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    .logout-button:hover {
        background-color: #c82333;
        transform: translateY(-2px);
    }
    .user-card {
        background-color: #e9ecef;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        border-left: 4px solid #2E86AB;
    }
    .lab-record {
        border: 1px solid #ddd;
        border-radius: 5px;
        padding: 1rem;
        margin: 0.5rem 0;
        background-color: #f9f9f9;
    }
    .normal-value {
        color: #28a745;
        font-weight: bold;
    }
    .abnormal-value {
        color: #dc3545;
        font-weight: bold;
    }
    .status-good {
        color: #28a745;
        font-weight: bold;
    }
    .status-warning {
        color: #ffc107;
        font-weight: bold;
    }
    .status-danger {
        color: #dc3545;
        font-weight: bold;
    }
    .lab-value-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.5rem;
        margin: 0.25rem 0;
        border-radius: 5px;
    }
    .lab-value-normal {
        background-color: #f8fff8;
        border-left: 4px solid #28a745;
    }
    .lab-value-abnormal {
        background-color: #fff8f8;
        border-left: 4px solid #dc3545;
    }
    /* แก้ไขฟอนต์สำหรับภาษาไทย */
    * {
        font-family: 'Segoe UI', 'Tahoma', 'Geneva', 'Verdana', 'sans-serif';
    }
    
    /* ปรับปรุงการแสดงผลปุ่ม */
    .stButton button {
        font-family: 'Segoe UI', 'Tahoma', 'Geneva', 'Verdana', 'sans-serif';
    }
</style>
""", unsafe_allow_html=True)

def hash_password(password):
    """Simple password hashing"""
    return hashlib.sha256(password.encode()).hexdigest()

def cache_key(user_id, data_type, date=None):
    """Generate cache key"""
    if date:
        return f"user:{user_id}:{data_type}:{date}"
    return f"user:{user_id}:{data_type}"

@st.cache_data(ttl=3600)  # Cache for 1 hour
def get_cached_data(_key):
    """Get data from cache - using st.cache_data for immutable data"""
    return None

@st.cache_resource
def get_app_cache():
    """Initialize application cache using st.cache_resource for singleton objects"""
    return {}

def clear_user_cache(user_id):
    """Clear cache for user - using Streamlit's cache clearing mechanisms"""
    pass

def init_app_data():
    """Initialize application data in session state"""
    if 'users' not in st.session_state:
        st.session_state.users = {}
    if 'health_data' not in st.session_state:
        st.session_state.health_data = {}

def register_user(username, password, user_info):
    """Register a new user"""
    if username in st.session_state.users:
        return False, "Username already exists", None
    
    hashed_password = hash_password(password)
    user_id = f"user_{len(st.session_state.users) + 1}"
    
    st.session_state.users[username] = {
        'user_id': user_id,
        'password_hash': hashed_password,
        'user_info': user_info,
        'registration_date': datetime.now().isoformat()
    }
    
    return True, "Registration successful", user_id

def verify_user(username, password):
    """Verify user credentials"""
    if username in st.session_state.users:
        user_data = st.session_state.users[username]
        if user_data['password_hash'] == hash_password(password):
            return True, "Login successful", user_data['user_id']
    return False, "Invalid username or password", None

def save_health_record(user_id, record_date, health_data):
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

@st.cache_data(ttl=1800)  # Cache for 30 minutes
def get_user_health_records_cached(_user_id, health_data_dict):
    """Get all health records for a user with caching"""
    return health_data_dict.get(_user_id, {}).copy()

def get_user_health_records(user_id):
    """Get all health records for a user"""
    if user_id in st.session_state.health_data:
        return st.session_state.health_data[user_id].copy()
    return {}

@st.cache_data(ttl=1800)  # Cache for 30 minutes
def get_latest_health_record_cached(_user_id, health_data_dict):
    """Get the latest health record for a user with caching"""
    if _user_id in health_data_dict and health_data_dict[_user_id]:
        records = health_data_dict[_user_id]
        latest_date = max(records.keys())
        return records[latest_date].copy()
    return {}

def get_latest_health_record(user_id):
    """Get the latest health record for a user"""
    if user_id in st.session_state.health_data and st.session_state.health_data[user_id]:
        records = st.session_state.health_data[user_id]
        latest_date = max(records.keys())
        return records[latest_date].copy()
    return {}

@st.cache_data(ttl=3600)  # Cache for 1 hour
def get_user_profile_cached(_user_id, users_dict):
    """Get user profile information with caching"""
    for username, user_data in users_dict.items():
        if user_data['user_id'] == _user_id:
            return {
                'username': username,
                'firstname': user_data['user_info'].get('firstname', ''),
                'lastname': user_data['user_info'].get('lastname', ''),
                'email': user_data['user_info'].get('email', ''),
                'phone': user_data['user_info'].get('phone', '')
            }
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
            return True
    return False

@st.cache_data(ttl=86400)  # Cache for 24 hours - normal ranges don't change often
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
    st.session_state.current_screen = 'home'
    st.success("ออกจากระบบเรียบร้อยแล้ว!")
    st.rerun()

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

# Navigation function
def navigate_to(screen):
    st.session_state.current_screen = screen

def render_navigation():
    """Render fixed navigation buttons with user info and logout"""
    # User info bar at the top
    if st.session_state.logged_in:
        user_profile = get_user_profile(st.session_state.user_id) or {}
        full_name = f"{user_profile.get('firstname', '')} {user_profile.get('lastname', '')}".strip()
        
        # ใช้ Streamlit components แทน JavaScript
        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(f"""
            <div class="user-card">
                <h4>👤 ข้อมูลผู้ใช้</h4>
                <strong>ชื่อผู้ใช้:</strong> {st.session_state.username}<br>
                {f"<strong>ชื่อ-สกุล:</strong> {full_name}" if full_name else ""}
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            if st.button("🚪 ออกจากระบบ", key="header_logout", use_container_width=True):
                logout_user()
    
    # Main navigation
    st.markdown('<div class="nav-container">', unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        if st.button("🏠 หน้าแรก", use_container_width=True, key="nav_home"):
            navigate_to('home')
    
    with col2:
        if st.button("👤 ประวัติของฉัน", use_container_width=True, key="nav_profile"):
            navigate_to('profile')
    
    with col3:
        if st.button("📝 บันทึกสุขภาพ", use_container_width=True, key="nav_health_form"):
            navigate_to('health_form')
    
    with col4:
        if st.button("🔬 ผลแล็บ", use_container_width=True, key="nav_lab_results"):
            navigate_to('lab_results')
    
    with col5:
        if st.button("📊 สรุปผล", use_container_width=True, key="nav_summary"):
            navigate_to('summary')
    
    st.markdown('</div>', unsafe_allow_html=True)

# Screen 1: Home with login and registration
def home_screen():
    st.markdown('<div class="main-header">🏥 Smart Health Checker</div>', unsafe_allow_html=True)
    
    # If user is logged in, show welcome message
    if st.session_state.logged_in:
        user_profile = get_user_profile(st.session_state.user_id) or {}
        full_name = f"{user_profile.get('firstname', '')} {user_profile.get('lastname', '')}".strip()
        
        # การ์ดต้อนรับ
        st.markdown(f"""
        <div class="user-card">
            <h3>👋 สวัสดี {full_name if full_name else st.session_state.username}</h3>
            <p>✅ คุณล็อกอินเข้าสู่ระบบเรียบร้อยแล้ว</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Create two columns for the images
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="image-placeholder">📊 ดูผลวิเคราะห์สุขภาพ</div>', unsafe_allow_html=True)
            if st.button("📊 ดูสรุปผลสุขภาพ", use_container_width=True, key="home_to_summary"):
                navigate_to('summary')
        
        with col2:
            st.markdown('<div class="image-placeholder">📝 บันทึกข้อมูลใหม่</div>', unsafe_allow_html=True)
            if st.button("📝 บันทึกสุขภาพ", use_container_width=True, key="home_to_health_form"):
                navigate_to('health_form')
        
        # ปุ่มออกจากระบบกลางหน้า
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🚪 ออกจากระบบ", use_container_width=True, key="home_logout_main"):
                logout_user()
        
        return
    
    # Login/Register tabs (only show if not logged in)
    tab1, tab2 = st.tabs(["🔐 เข้าสู่ระบบ", "📝 ลงทะเบียน"])
    
    with tab1:
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        st.markdown('<div class="sub-header">Login</div>', unsafe_allow_html=True)
        
        login_username = st.text_input("Username:", key="login_username")
        login_password = st.text_input("Password:", type="password", key="login_password")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Login", use_container_width=True, key="login_btn"):
                if login_username and login_password:
                    success, message, user_id = verify_user(login_username, login_password)
                    if success:
                        st.session_state.user_id = user_id
                        st.session_state.username = login_username
                        st.session_state.logged_in = True
                        st.success(f"Welcome {login_username}!")
                        st.session_state.current_screen = 'profile'
                        st.rerun()
                    else:
                        st.error(message)
                else:
                    st.error("Please enter both username and password")
        
        with col2:
            if st.button("Clear", use_container_width=True, key="clear_login"):
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        st.markdown('<div class="sub-header">Register</div>', unsafe_allow_html=True)
        
        reg_username = st.text_input("Username:", key="reg_username")
        reg_password = st.text_input("Password:", type="password", key="reg_password")
        reg_confirm_password = st.text_input("Confirm Password:", type="password", key="reg_confirm_password")
        
        # Additional registration information
        st.markdown("**ข้อมูลส่วนตัว**")
        col1, col2 = st.columns(2)
        with col1:
            reg_firstname = st.text_input("ชื่อ", key="reg_firstname")
            reg_lastname = st.text_input("นามสกุล", key="reg_lastname")
        with col2:
            reg_email = st.text_input("อีเมล", key="reg_email")
            reg_phone = st.text_input("เบอร์โทรศัพท์", key="reg_phone")
        
        if st.button("Register", use_container_width=True, key="register_btn"):
            if not reg_username or not reg_password:
                st.error("Please enter username and password")
            elif reg_password != reg_confirm_password:
                st.error("Passwords do not match")
            elif len(reg_password) < 6:
                st.error("Password must be at least 6 characters long")
            else:
                user_info = {
                    'firstname': reg_firstname,
                    'lastname': reg_lastname,
                    'email': reg_email,
                    'phone': reg_phone
                }
                success, message, user_id = register_user(reg_username, reg_password, user_info)
                if success:
                    st.success(message)
                    st.info("Please login with your new account")
                else:
                    st.error(message)
        
        st.markdown('</div>', unsafe_allow_html=True)

# Screen 2: Profile
def profile_screen():
    st.markdown('<div class="main-header">ประวัติของฉัน</div>', unsafe_allow_html=True)
    
    # Get user profile
    user_profile = get_user_profile(st.session_state.user_id) or {}
    
    # Display user info
    st.write(f"**ผู้ใช้:** {st.session_state.username}")
    st.write(f"**ชื่อ:** {user_profile.get('firstname', '')} {user_profile.get('lastname', '')}")
    st.write(f"**อีเมล:** {user_profile.get('email', '')}")
    st.write(f"**เบอร์โทรศัพท์:** {user_profile.get('phone', '')}")
    
    # Profile content
    st.markdown('<div class="sub-header">ข้อมูลส่วนตัว</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        firstname = st.text_input("ชื่อ:", value=user_profile.get('firstname', ''), key="profile_firstname")
        lastname = st.text_input("นามสกุล:", value=user_profile.get('lastname', ''), key="profile_lastname")
        birthdate = st.date_input("วันเกิด:", value=None)
        gender = st.selectbox("เพศ:", ["ชาย", "หญิง", "อื่นๆ"], key="profile_gender")
    
    with col2:
        address = st.text_input("ที่อยู่:", value="", key="profile_address")
        phone = st.text_input("เบอร์โทรศัพท์:", value=user_profile.get('phone', ''), key="profile_phone")
        email = st.text_input("อีเมล:", value=user_profile.get('email', ''), key="profile_email")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Update Profile", use_container_width=True, key="update_profile"):
            user_info = {
                'firstname': firstname,
                'lastname': lastname,
                'email': email,
                'phone': phone
            }
            if update_user_profile(st.session_state.user_id, user_info):
                st.success("Profile updated successfully!")
            else:
                st.error("Error updating profile")
    
    with col2:
        if st.button("🚪 ออกจากระบบ", use_container_width=True, key="profile_logout"):
            logout_user()

# Screen 3: Health Form
def health_form_screen():
    st.markdown('<div class="main-header">แบบฟอร์มบันทึกสุขภาพ</div>', unsafe_allow_html=True)
    
    # Load latest health data for this user
    user_health_data = get_latest_health_record(st.session_state.user_id) or {}
    
    # Date selection for new record
    record_date = st.date_input("วันที่บันทึกข้อมูล", value=datetime.now(), key="record_date")
    
    # Section 1: Basic Information
    st.markdown('<div class="section-header">ข้อมูลพื้นฐาน</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st_gender = st.selectbox("เพศ", ["Female", "Male"], 
                               index=0 if user_health_data.get('st_gender') == 'Female' else 1, 
                               key="st_gender")
        lv_age = st.number_input("อายุ", min_value=0, max_value=120, 
                               value=user_health_data.get('lv_age', 25), key="lv_age")
    
    with col2:
        lv_weight = st.number_input("น้ำหนัก (kg)", min_value=0.0, value=float(user_health_data.get('lv_weight', 65.0)), 
                                  step=0.1, key="lv_weight")
        lv_height = st.number_input("ส่วนสูง (cm)", min_value=0.0, value=float(user_health_data.get('lv_height', 170.0)), 
                                  step=0.1, key="lv_height")
    
    with col3:
        # Calculate BMI
        if lv_height > 0:
            bmi = lv_weight / ((lv_height/100) ** 2)
            lv_bmi = st.number_input("BMI", value=round(bmi, 2), key="lv_bmi", disabled=True)
        else:
            lv_bmi = st.number_input("BMI", value=float(user_health_data.get('lv_bmi', 0.0)), key="lv_bmi")
        
        st_smoking = st.selectbox("สูบบุหรี่", ["Yes", "No"], 
                                index=0 if user_health_data.get('st_smoking') == 'Yes' else 1, 
                                key="st_smoking")
    
    with col4:
        st_hypertension = st.selectbox("ความดันโลหิตสูง", ["Yes", "No"], 
                                     index=0 if user_health_data.get('st_hypertension') == 'Yes' else 1, 
                                     key="st_hypertension")
        lv_cigsperday = st.number_input("จำนวนบุหรี่ต่อวัน", min_value=0, 
                                      value=user_health_data.get('lv_cigsperday', 0), key="lv_cigsperday")
    
    # Section 2: Diabetes and Heart Disease
    st.markdown('<div class="section-header">โรคประจำตัว</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        lv_glucose = st.number_input("ระดับน้ำตาลกลูโคส (mg/dL)", min_value=0.0, 
                                   value=float(user_health_data.get('lv_glucose', 95.0)), step=0.1, key="lv_glucose")
        lv_HbA1c = st.number_input("ระดับน้ำตาลสะสม HbA1c", min_value=0.0, 
                                 value=float(user_health_data.get('lv_HbA1c', 5.5)), step=0.1, key="lv_HbA1c")
    
    with col2:
        st_diabetes = st.selectbox("เบาหวาน", ["Yes", "No"], 
                                 index=0 if user_health_data.get('st_diabetes') == 'Yes' else 1, 
                                 key="st_diabetes")
        st_heart_disease = st.selectbox("โรคหัวใจ", ["Yes", "No"], 
                                      index=0 if user_health_data.get('st_heart_disease') == 'Yes' else 1, 
                                      key="st_heart_disease")
    
    with col3:
        st_bpmeds = st.selectbox("ใช้ยาลดความดัน", ["Yes", "No"], 
                               index=0 if user_health_data.get('st_bpmeds') == 'Yes' else 1, 
                               key="st_bpmeds")
        st_prevalentstroke = st.selectbox("ประวัติหลอดเลือดสมอง", ["Yes", "No"], 
                                        index=0 if user_health_data.get('st_prevalentstroke') == 'Yes' else 1, 
                                        key="st_prevalentstroke")
    
    with col4:
        st_prevalenthyp = st.selectbox("เคยเป็นความดันโลหิตสูง", ["Yes", "No"], 
                                     index=0 if user_health_data.get('st_prevalenthyp') == 'Yes' else 1, 
                                     key="st_prevalenthyp")
        st_family_history_with_overweight = st.selectbox("ประวัติครอบครัวน้ำหนักเกิน", ["Yes", "No"], 
                                                       index=0 if user_health_data.get('st_family_history_with_overweight') == 'Yes' else 1, 
                                                       key="st_family_history_with_overweight")
    
    # Section 3: Dietary Habits
    st.markdown('<div class="section-header">พฤติกรรมการกิน</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st_favc = st.selectbox("ทานอาหารแคลอรี่สูงบ่อย", ["Yes", "No"], 
                             index=0 if user_health_data.get('st_favc') == 'Yes' else 1, 
                             key="st_favc")
        st_fcvc = st.selectbox("กินผักในมื้ออาหาร", ["Sometimes", "Frequently", "Always"], 
                             index=["Sometimes", "Frequently", "Always"].index(user_health_data.get('st_fcvc', 'Sometimes')), 
                             key="st_fcvc")
    
    with col2:
        lv_ncp = st.selectbox("มื้ออาหารต่อวัน", ["1", "2", "3", "4"], 
                            index=["1", "2", "3", "4"].index(str(user_health_data.get('lv_ncp', '3'))), 
                            key="lv_ncp")
        st_caec = st.selectbox("กินของว่างระหว่างมื้อ", ["No", "Sometimes", "Frequently", "Always"], 
                             index=["No", "Sometimes", "Frequently", "Always"].index(user_health_data.get('st_caec', 'Sometimes')), 
                             key="st_caec")
    
    with col3:
        st_ch2o = st.selectbox("ดื่มน้ำบ่อย", ["Sometimes", "Frequently", "Always"], 
                             index=["Sometimes", "Frequently", "Always"].index(user_health_data.get('st_ch2o', 'Sometimes')), 
                             key="st_ch2o")
        st_scc = st.selectbox("ตรวจสอบแคลอรี่", ["Yes", "No"], 
                            index=0 if user_health_data.get('st_scc') == 'Yes' else 1, 
                            key="st_scc")
    
    with col4:
        st_faf = st.selectbox("ออกกำลังกาย", ["No", "Sometimes", "Frequently", "Always"], 
                            index=["No", "Sometimes", "Frequently", "Always"].index(user_health_data.get('st_faf', 'Sometimes')), 
                            key="st_faf")
        st_calc = st.selectbox("ดื่มแอลกอฮอล์", ["No", "Sometimes", "Frequently", "Always"], 
                             index=["No", "Sometimes", "Frequently", "Always"].index(user_health_data.get('st_calc', 'Sometimes')), 
                             key="st_calc")
    
    # Section 4: Lab Results
    st.markdown('<div class="section-header">ผลการตรวจเลือด</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        lv_total_bilirubin = st.number_input("บิลิรูบินรวม (mg/dL)", min_value=0.0, 
                                           value=float(user_health_data.get('lv_total_bilirubin', 0.7)), step=0.1, key="lv_total_bilirubin")
        lv_direct_bilirubin = st.number_input("บิลิรูบินโดยตรง (mg/dL)", min_value=0.0, 
                                            value=float(user_health_data.get('lv_direct_bilirubin', 0.2)), step=0.1, key="lv_direct_bilirubin")
    
    with col2:
        lv_alkphos = st.number_input("Alkaline Phosphotase", min_value=0.0, 
                                   value=float(user_health_data.get('lv_alkphos', 80.0)), step=0.1, key="lv_alkphos")
        lv_sgpt = st.number_input("SGPT Alamine Aminotransferase", min_value=0.0, 
                                value=float(user_health_data.get('lv_sgpt', 25.0)), step=0.1, key="lv_sgpt")
    
    with col3:
        lv_sgot = st.number_input("SGOT Aspartate Aminotransferase", min_value=0.0, 
                                value=float(user_health_data.get('lv_sgot', 28.0)), step=0.1, key="lv_sgot")
        lv_total_protiens = st.number_input("โปรตีนรวม (g/dL)", min_value=0.0, 
                                          value=float(user_health_data.get('lv_total_protiens', 7.0)), step=0.1, key="lv_total_protiens")
    
    with col4:
        lv_alb = st.number_input("อัลบูมิน (g/dL)", min_value=0.0, 
                               value=float(user_health_data.get('lv_alb', 4.0)), step=0.1, key="lv_alb")
        lv_ag_ratio = st.number_input("A/G Ratio", min_value=0.0, 
                                    value=float(user_health_data.get('lv_ag_ratio', 1.2)), step=0.1, key="lv_ag_ratio")
    
    # Section 5: Kidney Function and Cardiovascular
    st.markdown('<div class="section-header">การทำงานของไตและหัวใจ</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        lv_creatinine = st.number_input("ครีเอตินีน (mg/dL)", min_value=0.0, 
                                      value=float(user_health_data.get('lv_creatinine', 0.9)), step=0.1, key="lv_creatinine")
        lv_bun = st.number_input("BUN (mg/dL)", min_value=0.0, 
                               value=float(user_health_data.get('lv_bun', 15.0)), step=0.1, key="lv_bun")
    
    with col2:
        lv_gfr = st.number_input("GFR (mL/min/1.73m²)", min_value=0.0, 
                               value=float(user_health_data.get('lv_gfr', 90.0)), step=0.1, key="lv_gfr")
        lv_urine_output = st.number_input("ปริมาณปัสสาวะ (mL/day)", min_value=0, 
                                        value=user_health_data.get('lv_urine_output', 1500), key="lv_urine_output")
    
    with col3:
        lv_totchol = st.number_input("คอเลสเตอรอลรวม (mg/dL)", min_value=0.0, 
                                   value=float(user_health_data.get('lv_totchol', 180.0)), step=0.1, key="lv_totchol")
        lv_sysbp = st.number_input("ความดันตัวบน", min_value=0.0, 
                                 value=float(user_health_data.get('lv_sysbp', 120.0)), step=0.1, key="lv_sysbp")
    
    with col4:
        lv_diabp = st.number_input("ความดันตัวล่าง", min_value=0.0, 
                                 value=float(user_health_data.get('lv_diabp', 80.0)), step=0.1, key="lv_diabp")
        lv_heartrate = st.number_input("อัตราการเต้นหัวใจ (bpm)", min_value=0, 
                                     value=user_health_data.get('lv_heartrate', 72), key="lv_heartrate")
    
    # Save button and logout
    col1, col2 = st.columns(2)
    with col1:
        if st.button("บันทึกข้อมูลสุขภาพ", use_container_width=True, key="save_health_data"):
            health_data = {
                'st_gender': st_gender,
                'lv_age': lv_age,
                'lv_weight': float(lv_weight),
                'lv_height': float(lv_height),
                'lv_bmi': float(lv_bmi),
                'st_smoking': st_smoking,
                'st_hypertension': st_hypertension,
                'lv_glucose': float(lv_glucose),
                'lv_HbA1c': float(lv_HbA1c),
                'st_diabetes': st_diabetes,
                'st_heart_disease': st_heart_disease,
                'st_family_history_with_overweight': st_family_history_with_overweight,
                'st_favc': st_favc,
                'st_fcvc': st_fcvc,
                'lv_ncp': lv_ncp,
                'st_caec': st_caec,
                'st_ch2o': st_ch2o,
                'st_scc': st_scc,
                'st_faf': st_faf,
                'st_calc': st_calc,
                'lv_total_bilirubin': float(lv_total_bilirubin),
                'lv_direct_bilirubin': float(lv_direct_bilirubin),
                'lv_alkphos': float(lv_alkphos),
                'lv_sgpt': float(lv_sgpt),
                'lv_sgot': float(lv_sgot),
                'lv_total_protiens': float(lv_total_protiens),
                'lv_alb': float(lv_alb),
                'lv_ag_ratio': float(lv_ag_ratio),
                'lv_creatinine': float(lv_creatinine),
                'lv_bun': float(lv_bun),
                'lv_gfr': float(lv_gfr),
                'lv_urine_output': lv_urine_output,
                'lv_cigsperday': lv_cigsperday,
                'st_bpmeds': st_bpmeds,
                'st_prevalentstroke': st_prevalentstroke,
                'st_prevalenthyp': st_prevalenthyp,
                'lv_totchol': float(lv_totchol),
                'lv_sysbp': float(lv_sysbp),
                'lv_diabp': float(lv_diabp),
                'lv_heartrate': lv_heartrate
            }
            
            if save_health_record(st.session_state.user_id, record_date, health_data):
                st.success("บันทึกข้อมูลสุขภาพเรียบร้อยแล้ว!")
            else:
                st.error("เกิดข้อผิดพลาดในการบันทึกข้อมูล")
    
    with col2:
        if st.button("🚪 ออกจากระบบ", use_container_width=True, key="health_form_logout"):
            logout_user()

# Screen 4: Lab Results with History and Dashboard
def lab_results_screen():
    st.markdown('<div class="main-header">ข้อมูลทางห้องปฏิบัติการ (Lab Results)</div>', unsafe_allow_html=True)
    
    # Check if user has health data
    user_records = get_user_health_records(st.session_state.user_id)
    
    if not user_records:
        st.info("ยังไม่มีข้อมูลผลการตรวจ กรุณากรอกข้อมูลในหน้า 'แบบฟอร์มบันทึกสุขภาพ'")
        # Add logout button
        if st.button("🚪 ออกจากระบบ", key="lab_results_logout_empty"):
            logout_user()
        return
    
    # Create tabs for different views
    tab1, tab2, tab3 = st.tabs(["📊 ผลแล็บทั้งหมด", "📈 กราฟแนวโน้ม", "📋 ประวัติผลแล็บ"])
    
    with tab1:  # All Lab Results Tab
        st.markdown('<div class="sub-header">ผลการตรวจแล็บทั้งหมด</div>', unsafe_allow_html=True)
        
        # Date selection for specific record
        record_dates = sorted(user_records.keys(), reverse=True)
        selected_date = st.selectbox("เลือกวันที่แสดงผล", record_dates, 
                                   format_func=lambda x: datetime.fromisoformat(x).strftime("%d/%m/%Y"))
        
        if selected_date:
            health_data = user_records[selected_date]
            
            # Display all lab results in organized sections
            col1, col2 = st.columns(2)
            
            with col1:
                # Section 1: Basic Health Metrics
                st.markdown("#### 🩺 ข้อมูลสุขภาพพื้นฐาน")
                
                # BMI
                bmi_value = health_data.get('lv_bmi', 0)
                bmi_icon, bmi_status, bmi_class = get_health_status(bmi_value, (18.5, 24.9), "normal")
                bmi_style = "lab-value-normal" if bmi_class == "normal" else "lab-value-abnormal"
                st.markdown(f"""
                <div class="lab-value-container {bmi_style}">
                    <div><strong>ดัชนีมวลกาย (BMI)</strong></div>
                    <div>{bmi_value:.1f} {bmi_icon} <span class="{bmi_class}-value">{bmi_status}</span></div>
                </div>
                <div style="font-size: 0.8rem; color: #666; margin-bottom: 1rem;">ค่าปกติ: 18.5-24.9</div>
                """, unsafe_allow_html=True)
                
                # Blood Pressure
                sysbp = health_data.get('lv_sysbp', 0)
                diabp = health_data.get('lv_diabp', 0)
                bp_normal = sysbp <= 120 and diabp <= 80
                bp_icon = "✅" if bp_normal else "❌"
                bp_status = "ปกติ" if bp_normal else "สูง"
                bp_class = "normal" if bp_normal else "abnormal"
                bp_style = "lab-value-normal" if bp_normal else "lab-value-abnormal"
                st.markdown(f"""
                <div class="lab-value-container {bp_style}">
                    <div><strong>ความดันโลหิต</strong></div>
                    <div>{sysbp}/{diabp} mmHg {bp_icon} <span class="{bp_class}-value">{bp_status}</span></div>
                </div>
                <div style="font-size: 0.8rem; color: #666; margin-bottom: 1rem;">ค่าปกติ: ≤ 120/80 mmHg</div>
                """, unsafe_allow_html=True)
                
                # Heart Rate
                heartrate = health_data.get('lv_heartrate', 0)
                hr_icon, hr_status, hr_class = get_health_status(heartrate, (60, 100), "normal")
                hr_style = "lab-value-normal" if hr_class == "normal" else "lab-value-abnormal"
                st.markdown(f"""
                <div class="lab-value-container {hr_style}">
                    <div><strong>อัตราการเต้นหัวใจ</strong></div>
                    <div>{heartrate} bpm {hr_icon} <span class="{hr_class}-value">{hr_status}</span></div>
                </div>
                <div style="font-size: 0.8rem; color: #666; margin-bottom: 1rem;">ค่าปกติ: 60-100 bpm</div>
                """, unsafe_allow_html=True)
                
                # Section 2: Blood Sugar
                st.markdown("#### 🩸 ระดับน้ำตาลในเลือด")
                
                # Glucose
                glucose_value = health_data.get('lv_glucose', 0)
                glucose_icon, glucose_status, glucose_class = get_health_status(glucose_value, 100, "high_bad")
                glucose_style = "lab-value-normal" if glucose_class == "normal" else "lab-value-abnormal"
                st.markdown(f"""
                <div class="lab-value-container {glucose_style}">
                    <div><strong>น้ำตาลกลูโคส</strong></div>
                    <div>{glucose_value} mg/dL {glucose_icon} <span class="{glucose_class}-value">{glucose_status}</span></div>
                </div>
                <div style="font-size: 0.8rem; color: #666; margin-bottom: 1rem;">ค่าปกติ: ≤ 100 mg/dL</div>
                """, unsafe_allow_html=True)
                
                # HbA1c
                hba1c_value = health_data.get('lv_HbA1c', 0)
                hba1c_icon, hba1c_status, hba1c_class = get_health_status(hba1c_value, 5.6, "high_bad")
                hba1c_style = "lab-value-normal" if hba1c_class == "normal" else "lab-value-abnormal"
                st.markdown(f"""
                <div class="lab-value-container {hba1c_style}">
                    <div><strong>HbA1c</strong></div>
                    <div>{hba1c_value} % {hba1c_icon} <span class="{hba1c_class}-value">{hba1c_status}</span></div>
                </div>
                <div style="font-size: 0.8rem; color: #666; margin-bottom: 1rem;">ค่าปกติ: ≤ 5.6 %</div>
                """, unsafe_allow_html=True)
                
                # Section 3: Lipid Profile
                st.markdown("#### 🫀 ไขมันในเลือด")
                
                # Total Cholesterol
                chol_value = health_data.get('lv_totchol', 0)
                chol_icon, chol_status, chol_class = get_health_status(chol_value, 200, "high_bad")
                chol_style = "lab-value-normal" if chol_class == "normal" else "lab-value-abnormal"
                st.markdown(f"""
                <div class="lab-value-container {chol_style}">
                    <div><strong>คอเลสเตอรอลรวม</strong></div>
                    <div>{chol_value} mg/dL {chol_icon} <span class="{chol_class}-value">{chol_status}</span></div>
                </div>
                <div style="font-size: 0.8rem; color: #666; margin-bottom: 1rem;">ค่าปกติ: ≤ 200 mg/dL</div>
                """, unsafe_allow_html=True)
            
            with col2:
                # Section 4: Liver Function
                st.markdown("#### 🫁 การทำงานของตับ")
                
                # SGPT
                sgpt_value = health_data.get('lv_sgpt', 0)
                sgpt_icon, sgpt_status, sgpt_class = get_health_status(sgpt_value, 40, "high_bad")
                sgpt_style = "lab-value-normal" if sgpt_class == "normal" else "lab-value-abnormal"
                st.markdown(f"""
                <div class="lab-value-container {sgpt_style}">
                    <div><strong>SGPT (ALT)</strong></div>
                    <div>{sgpt_value} U/L {sgpt_icon} <span class="{sgpt_class}-value">{sgpt_status}</span></div>
                </div>
                <div style="font-size: 0.8rem; color: #666; margin-bottom: 1rem;">ค่าปกติ: ≤ 40 U/L</div>
                """, unsafe_allow_html=True)
                
                # SGOT
                sgot_value = health_data.get('lv_sgot', 0)
                sgot_icon, sgot_status, sgot_class = get_health_status(sgot_value, 40, "high_bad")
                sgot_style = "lab-value-normal" if sgot_class == "normal" else "lab-value-abnormal"
                st.markdown(f"""
                <div class="lab-value-container {sgot_style}">
                    <div><strong>SGOT (AST)</strong></div>
                    <div>{sgot_value} U/L {sgot_icon} <span class="{sgot_class}-value">{sgot_status}</span></div>
                </div>
                <div style="font-size: 0.8rem; color: #666; margin-bottom: 1rem;">ค่าปกติ: ≤ 40 U/L</div>
                """, unsafe_allow_html=True)
                
                # Section 5: Kidney Function
                st.markdown("#### 🫘 การทำงานของไต")
                
                # Creatinine
                creat_value = health_data.get('lv_creatinine', 0)
                creat_icon, creat_status, creat_class = get_health_status(creat_value, (0.6, 1.2), "normal")
                creat_style = "lab-value-normal" if creat_class == "normal" else "lab-value-abnormal"
                st.markdown(f"""
                <div class="lab-value-container {creat_style}">
                    <div><strong>ครีเอตินีน</strong></div>
                    <div>{creat_value} mg/dL {creat_icon} <span class="{creat_class}-value">{creat_status}</span></div>
                </div>
                <div style="font-size: 0.8rem; color: #666; margin-bottom: 1rem;">ค่าปกติ: 0.6-1.2 mg/dL</div>
                """, unsafe_allow_html=True)
                
                # BUN
                bun_value = health_data.get('lv_bun', 0)
                bun_icon, bun_status, bun_class = get_health_status(bun_value, (7, 20), "normal")
                bun_style = "lab-value-normal" if bun_class == "normal" else "lab-value-abnormal"
                st.markdown(f"""
                <div class="lab-value-container {bun_style}">
                    <div><strong>BUN</strong></div>
                    <div>{bun_value} mg/dL {bun_icon} <span class="{bun_class}-value">{bun_status}</span></div>
                </div>
                <div style="font-size: 0.8rem; color: #666; margin-bottom: 1rem;">ค่าปกติ: 7-20 mg/dL</div>
                """, unsafe_allow_html=True)
                
                # GFR
                gfr_value = health_data.get('lv_gfr', 0)
                gfr_icon, gfr_status, gfr_class = get_health_status(gfr_value, 90, "low_bad")
                gfr_style = "lab-value-normal" if gfr_class == "normal" else "lab-value-abnormal"
                st.markdown(f"""
                <div class="lab-value-container {gfr_style}">
                    <div><strong>GFR</strong></div>
                    <div>{gfr_value} {gfr_icon} <span class="{gfr_class}-value">{gfr_status}</span></div>
                </div>
                <div style="font-size: 0.8rem; color: #666; margin-bottom: 1rem;">ค่าปกติ: ≥ 90 mL/min/1.73m²</div>
                """, unsafe_allow_html=True)
    
    with tab2:  # Trends Tab
        st.markdown('<div class="sub-header">กราฟแนวโน้มผลแล็บ</div>', unsafe_allow_html=True)
        
        if not PLOTLY_AVAILABLE:
            st.error("⚠️ กรุณาติดตั้ง Plotly โดยใช้คำสั่ง: pip install plotly")
            return
        
        # Prepare data for trends
        dates = []
        glucose_data = []
        hba1c_data = []
        cholesterol_data = []
        sgpt_data = []
        creatinine_data = []
        
        for date_key in sorted(user_records.keys()):
            record = user_records[date_key]
            dates.append(datetime.fromisoformat(date_key).strftime("%d/%m/%Y"))
            glucose_data.append(record.get('lv_glucose', 0))
            hba1c_data.append(record.get('lv_HbA1c', 0))
            cholesterol_data.append(record.get('lv_totchol', 0))
            sgpt_data.append(record.get('lv_sgpt', 0))
            creatinine_data.append(record.get('lv_creatinine', 0))
        
        if len(dates) > 1:
            # Create trend charts
            col1, col2 = st.columns(2)
            
            with col1:
                # Blood Glucose and HbA1c trends
                fig1 = go.Figure()
                fig1.add_trace(go.Scatter(x=dates, y=glucose_data, mode='lines+markers', 
                                        name='น้ำตาลกลูโคส (mg/dL)', line=dict(color='blue')))
                fig1.add_trace(go.Scatter(x=dates, y=hba1c_data, mode='lines+markers', 
                                        name='HbA1c (%)', line=dict(color='red'), yaxis='y2'))
                
                fig1.update_layout(
                    title='แนวโน้มน้ำตาลในเลือด',
                    xaxis_title='วันที่',
                    yaxis_title='น้ำตาลกลูโคส (mg/dL)',
                    yaxis2=dict(title='HbA1c (%)', overlaying='y', side='right'),
                    height=400
                )
                st.plotly_chart(fig1, use_container_width=True)
            
            with col2:
                # Cholesterol and Liver/Kidney function trends
                fig2 = go.Figure()
                fig2.add_trace(go.Scatter(x=dates, y=cholesterol_data, mode='lines+markers', 
                                        name='คอเลสเตอรอล (mg/dL)', line=dict(color='green')))
                fig2.add_trace(go.Scatter(x=dates, y=sgpt_data, mode='lines+markers', 
                                        name='SGPT (U/L)', line=dict(color='orange')))
                fig2.add_trace(go.Scatter(x=dates, y=creatinine_data, mode='lines+markers', 
                                        name='ครีเอตินีน (mg/dL)', line=dict(color='purple')))
                
                fig2.update_layout(
                    title='แนวโน้มคอเลสเตอรอลและการทำงานของอวัยวะ',
                    xaxis_title='วันที่',
                    yaxis_title='ค่า',
                    height=400
                )
                st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("ต้องการข้อมูลอย่างน้อย 2 ครั้งเพื่อแสดงกราฟแนวโน้ม")
    
    with tab3:  # History Tab
        st.markdown('<div class="sub-header">ประวัติผลแล็บทั้งหมด</div>', unsafe_allow_html=True)
        
        # Date filter
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("วันที่เริ่มต้น", 
                                     value=datetime.fromisoformat(min(user_records.keys())).date())
        with col2:
            end_date = st.date_input("วันที่สิ้นสุด", 
                                   value=datetime.fromisoformat(max(user_records.keys())).date())
        
        # Filter records by date
        filtered_records = {}
        for date_key, record in user_records.items():
            record_date = datetime.fromisoformat(date_key).date()
            if start_date <= record_date <= end_date:
                filtered_records[date_key] = record
        
        if filtered_records:
            # Display each record
            for date_key in sorted(filtered_records.keys(), reverse=True):
                record = filtered_records[date_key]
                display_date = datetime.fromisoformat(date_key).strftime("%d/%m/%Y")
                
                with st.expander(f"📅 ผลแล็บวันที่ {display_date}"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("**ผลตรวจเลือดพื้นฐาน**")
                        
                        glucose_value = record.get('lv_glucose', 0)
                        glucose_icon, glucose_status, _ = get_health_status(glucose_value, 100, "high_bad")
                        glucose_color = "🔴" if glucose_status != "ปกติ" else "🟢"
                        st.write(f"{glucose_color} น้ำตาลกลูโคส: {glucose_value} mg/dL ({glucose_icon} {glucose_status})")
                        
                        hba1c_value = record.get('lv_HbA1c', 0)
                        hba1c_icon, hba1c_status, _ = get_health_status(hba1c_value, 5.6, "high_bad")
                        hba1c_color = "🔴" if hba1c_status != "ปกติ" else "🟢"
                        st.write(f"{hba1c_color} HbA1c: {hba1c_value} % ({hba1c_icon} {hba1c_status})")
                        
                        chol_value = record.get('lv_totchol', 0)
                        chol_icon, chol_status, _ = get_health_status(chol_value, 200, "high_bad")
                        chol_color = "🔴" if chol_status != "ปกติ" else "🟢"
                        st.write(f"{chol_color} คอเลสเตอรอลรวม: {chol_value} mg/dL ({chol_icon} {chol_status})")
                    
                    with col2:
                        st.markdown("**การทำงานของตับและไต**")
                        
                        sgpt_value = record.get('lv_sgpt', 0)
                        sgpt_icon, sgpt_status, _ = get_health_status(sgpt_value, 40, "high_bad")
                        sgpt_color = "🔴" if sgpt_status != "ปกติ" else "🟢"
                        st.write(f"{sgpt_color} SGPT: {sgpt_value} U/L ({sgpt_icon} {sgpt_status})")
                        
                        creat_value = record.get('lv_creatinine', 0)
                        creat_icon, creat_status, _ = get_health_status(creat_value, (0.6, 1.2), "normal")
                        creat_color = "🔴" if creat_status != "ปกติ" else "🟢"
                        st.write(f"{creat_color} ครีเอตินีน: {creat_value} mg/dL ({creat_icon} {creat_status})")
                        
                        gfr_value = record.get('lv_gfr', 0)
                        gfr_icon, gfr_status, _ = get_health_status(gfr_value, 90, "low_bad")
                        gfr_color = "🔴" if gfr_status != "ปกติ" else "🟢"
                        st.write(f"{gfr_color} GFR: {gfr_value} mL/min/1.73m² ({gfr_icon} {gfr_status})")
        else:
            st.info("ไม่พบข้อมูลในช่วงวันที่เลือก")
    
    # Logout button at the bottom
    st.markdown("---")
    if st.button("🚪 ออกจากระบบ", key="lab_results_logout"):
        logout_user()

# Screen 5: Summary
def summary_screen():
    st.markdown('<div class="main-header">สรุปผล</div>', unsafe_allow_html=True)
    
    # Summary content
    user_records = get_user_health_records(st.session_state.user_id)
    
    if user_records:
        latest_date = max(user_records.keys())
        health_data = user_records[latest_date]
        
        st.markdown('<div class="sub-header">สรุปผลสุขภาพโดยรวม</div>', unsafe_allow_html=True)
        
        # Health status indicators
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            bmi_value = health_data.get('lv_bmi', 0)
            icon, status, status_class = get_health_status(bmi_value, (18.5, 24.9), "normal")
            delta_color = "normal" if status_class == "normal" else "off"
            st.metric("ดัชนีมวลกาย (BMI)", f"{bmi_value:.1f}", 
                     delta=f"{icon} {status}", delta_color=delta_color)
        
        with col2:
            sysbp = health_data.get('lv_sysbp', 0)
            diabp = health_data.get('lv_diabp', 0)
            bp_normal = sysbp <= 120 and diabp <= 80
            icon = "✅" if bp_normal else "❌"
            status = "ปกติ" if bp_normal else "สูง"
            delta_color = "normal" if bp_normal else "off"
            st.metric("ความดันโลหิต", f"{sysbp}/{diabp}", 
                     delta=f"{icon} {status}", delta_color=delta_color)
        
        with col3:
            glucose_value = health_data.get('lv_glucose', 0)
            icon, status, status_class = get_health_status(glucose_value, 100, "high_bad")
            delta_color = "normal" if status_class == "normal" else "off"
            st.metric("น้ำตาลในเลือด", f"{glucose_value} mg/dL", 
                     delta=f"{icon} {status}", delta_color=delta_color)
        
        with col4:
            chol_value = health_data.get('lv_totchol', 0)
            icon, status, status_class = get_health_status(chol_value, 200, "high_bad")
            delta_color = "normal" if status_class == "normal" else "off"
            st.metric("คอเลสเตอรอล", f"{chol_value} mg/dL", 
                     delta=f"{icon} {status}", delta_color=delta_color)
        
        # Risk factors
        st.markdown('<div class="sub-header">ปัจจัยเสี่ยง</div>', unsafe_allow_html=True)
        
        risk_factors = []
        if health_data.get('st_smoking') == 'Yes':
            risk_factors.append("การสูบบุหรี่")
        if health_data.get('st_hypertension') == 'Yes':
            risk_factors.append("ความดันโลหิตสูง")
        if health_data.get('st_diabetes') == 'Yes':
            risk_factors.append("เบาหวาน")
        if health_data.get('st_heart_disease') == 'Yes':
            risk_factors.append("โรคหัวใจ")
        if health_data.get('st_family_history_with_overweight') == 'Yes':
            risk_factors.append("ประวัติครอบครัวน้ำหนักเกิน")
        
        if risk_factors:
            st.warning(f"**ปัจจัยเสี่ยงที่พบ:** {', '.join(risk_factors)}")
        else:
            st.success("**ไม่พบปัจจัยเสี่ยงหลัก**")
        
        # Recommendations
        st.markdown('<div class="sub-header">คำแนะนำ</div>', unsafe_allow_html=True)
        
        recommendations = []
        if health_data.get('lv_bmi', 0) > 24.9:
            recommendations.append("ควรควบคุมน้ำหนักและออกกำลังกายสม่ำเสมอ")
        if health_data.get('lv_glucose', 0) > 100:
            recommendations.append("ควรควบคุมระดับน้ำตาลในเลือด")
        if health_data.get('lv_totchol', 0) > 200:
            recommendations.append("ควรควบคุมระดับคอเลสเตอรอล")
        if health_data.get('st_smoking') == 'Yes':
            recommendations.append("ควรลดหรือหยุดสูบบุหรี่")
        if health_data.get('st_faf') in ['No', 'Sometimes']:
            recommendations.append("ควรออกกำลังกายให้บ่อยขึ้น")
        
        if not recommendations:
            recommendations.append("สุขภาพโดยรวมอยู่ในเกณฑ์ดี ควรดูแลรักษาสุขภาพตามปกติ")
        
        for i, rec in enumerate(recommendations, 1):
            st.info(f"{i}. {rec}")
    
    else:
        st.info("ยังไม่มีข้อมูลสุขภาพ กรุณากรอกข้อมูลในหน้า 'แบบฟอร์มบันทึกสุขภาพ'")
    
    # Logout button
    st.markdown("---")
    if st.button("🚪 ออกจากระบบ", key="summary_logout"):
        logout_user()

# Main app logic
def main():
    # Clear any existing query parameters on load
    if "logout" in st.query_params:
        st.query_params.clear()
    
    # Check if user is logged in to determine which screens to show
    if not st.session_state.logged_in and st.session_state.current_screen != 'home':
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
