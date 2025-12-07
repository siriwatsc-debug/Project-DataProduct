import streamlit as st
import pandas as pd
import hashlib
import json
import os
from datetime import datetime

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
    .nav-button {
        display: block;
        width: 100%;
        padding: 0.75rem;
        margin: 0.5rem 0;
        background-color: #2E86AB;
        color: white;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        font-size: 1rem;
        text-align: center;
    }
    .nav-button:hover {
        background-color: #1B5E7A;
    }
    .register-button {
        background-color: #A23B72;
    }
    .register-button:hover {
        background-color: #7A2D56;
    }
</style>
""", unsafe_allow_html=True)

# User data file
USER_DATA_FILE = "users.json"
HEALTH_DATA_FILE = "health_data.json"

def load_users():
    """Load user data from JSON file"""
    if os.path.exists(USER_DATA_FILE):
        try:
            with open(USER_DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_users():
    """Save user data to JSON file"""
    try:
        with open(USER_DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(st.session_state.users, f, ensure_ascii=False, indent=2)
    except Exception as e:
        st.error(f"Error saving user data: {e}")

def load_health_data():
    """Load health data from JSON file"""
    if os.path.exists(HEALTH_DATA_FILE):
        try:
            with open(HEALTH_DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_health_data():
    """Save health data to JSON file"""
    try:
        with open(HEALTH_DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(st.session_state.health_data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        st.error(f"Error saving health data: {e}")

def hash_password(password):
    """Simple password hashing"""
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password, user_info):
    """Register a new user"""
    if username in st.session_state.users:
        return False, "Username already exists"
    
    hashed_password = hash_password(password)
    st.session_state.users[username] = {
        'password': hashed_password,
        'user_info': user_info,
        'registration_date': datetime.now().isoformat()
    }
    save_users()
    return True, "Registration successful"

def verify_user(username, password):
    """Verify user credentials"""
    if username in st.session_state.users:
        hashed_password = hash_password(password)
        if st.session_state.users[username]['password'] == hashed_password:
            return True, "Login successful"
    return False, "Invalid username or password"

# Initialize session state for navigation and user management
if 'current_screen' not in st.session_state:
    st.session_state.current_screen = 'home'
if 'username' not in st.session_state:
    st.session_state.username = ''
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'users' not in st.session_state:
    st.session_state.users = load_users()
if 'health_data' not in st.session_state:
    st.session_state.health_data = load_health_data()

# Navigation function
def navigate_to(screen):
    st.session_state.current_screen = screen

# Screen 1: Home with login and registration
def home_screen():
    st.markdown('<div class="main-header">Welcome to Smart Health Checker</div>', unsafe_allow_html=True)
    
    # Create two columns for the images
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="image-placeholder">Picture</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="image-placeholder">Picture</div>', unsafe_allow_html=True)
    
    # Login/Register tabs
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
                    success, message = verify_user(login_username, login_password)
                    if success:
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
                success, message = register_user(reg_username, reg_password, user_info)
                if success:
                    st.success(message)
                    st.info("Please login with your new account")
                else:
                    st.error(message)
        
        st.markdown('</div>', unsafe_allow_html=True)

# Screen 2: Profile
def profile_screen():
    st.markdown('<div class="main-header">ประวัติของฉัน</div>', unsafe_allow_html=True)
    
    # User info display
    user_info = {}
    if st.session_state.username in st.session_state.users:
        user_info = st.session_state.users[st.session_state.username].get('user_info', {})
    
    # Navigation buttons
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        if st.button("Home", use_container_width=True):
            navigate_to('home')
    
    with col2:
        if st.button("Health Form", use_container_width=True):
            navigate_to('health_form')
    
    with col3:
        if st.button("Lab Results", use_container_width=True):
            navigate_to('lab_results')
    
    with col4:
        if st.button("Summary", use_container_width=True):
            navigate_to('summary')
    
    with col5:
        if st.button("Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.username = ''
            navigate_to('home')
            st.rerun()
    
    # Display user info
    st.write(f"**ผู้ใช้:** {st.session_state.username}")
    st.write(f"**ชื่อ:** {user_info.get('firstname', '')} {user_info.get('lastname', '')}")
    st.write(f"**อีเมล:** {user_info.get('email', '')}")
    st.write(f"**เบอร์โทรศัพท์:** {user_info.get('phone', '')}")
    
    # Profile content
    st.markdown('<div class="sub-header">ข้อมูลส่วนตัว</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        firstname = st.text_input("ชื่อ:", value=user_info.get('firstname', ''), key="profile_firstname")
        lastname = st.text_input("นามสกุล:", value=user_info.get('lastname', ''), key="profile_lastname")
        birthdate = st.date_input("วันเกิด:", value=None)
        gender = st.selectbox("เพศ:", ["ชาย", "หญิง", "อื่นๆ"], key="profile_gender")
    
    with col2:
        address = st.text_input("ที่อยู่:", value="", key="profile_address")
        phone = st.text_input("เบอร์โทรศัพท์:", value=user_info.get('phone', ''), key="profile_phone")
        email = st.text_input("อีเมล:", value=user_info.get('email', ''), key="profile_email")
    
    if st.button("Update Profile", key="update_profile"):
        if st.session_state.username in st.session_state.users:
            st.session_state.users[st.session_state.username]['user_info'] = {
                'firstname': firstname,
                'lastname': lastname,
                'email': email,
                'phone': phone
            }
            save_users()
            st.success("Profile updated successfully!")

# Screen 3: Health Form with all fields from Excel
def health_form_screen():
    st.markdown('<div class="main-header">แบบฟอร์มบันทึกสุขภาพ</div>', unsafe_allow_html=True)
    
    # Navigation buttons
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        if st.button("Home", use_container_width=True, key="health_home"):
            navigate_to('home')
    
    with col2:
        if st.button("Profile", use_container_width=True, key="health_profile"):
            navigate_to('profile')
    
    with col3:
        if st.button("Lab Results", use_container_width=True, key="health_lab"):
            navigate_to('lab_results')
    
    with col4:
        if st.button("Summary", use_container_width=True, key="health_summary"):
            navigate_to('summary')
    
    with col5:
        if st.button("Logout", use_container_width=True, key="health_logout"):
            st.session_state.logged_in = False
            st.session_state.username = ''
            navigate_to('home')
            st.rerun()
    
    # Load existing health data for this user
    user_health_data = {}
    if st.session_state.username in st.session_state.health_data:
        user_health_data = st.session_state.health_data[st.session_state.username]
    
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
        lv_weight = st.number_input("น้ำหนัก (kg)", min_value=0.0, value=user_health_data.get('lv_weight', 65.0), 
                                  step=0.1, key="lv_weight")
        lv_height = st.number_input("ส่วนสูง (cm)", min_value=0.0, value=user_health_data.get('lv_height', 170.0), 
                                  step=0.1, key="lv_height")
    
    with col3:
        # Calculate BMI
        if lv_height > 0:
            bmi = lv_weight / ((lv_height/100) ** 2)
            lv_bmi = st.number_input("BMI", value=round(bmi, 2), key="lv_bmi", disabled=True)
        else:
            lv_bmi = st.number_input("BMI", value=user_health_data.get('lv_bmi', 0.0), key="lv_bmi")
        
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
                                   value=user_health_data.get('lv_glucose', 95.0), step=0.1, key="lv_glucose")
        lv_HbA1c = st.number_input("ระดับน้ำตาลสะสม HbA1c", min_value=0.0, 
                                 value=user_health_data.get('lv_HbA1c', 5.5), step=0.1, key="lv_HbA1c")
    
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
                            index=["1", "2", "3", "4"].index(user_health_data.get('lv_ncp', '3')), 
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
                                           value=user_health_data.get('lv_total_bilirubin', 0.7), step=0.1, key="lv_total_bilirubin")
        lv_direct_bilirubin = st.number_input("บิลิรูบินโดยตรง (mg/dL)", min_value=0.0, 
                                            value=user_health_data.get('lv_direct_bilirubin', 0.2), step=0.1, key="lv_direct_bilirubin")
    
    with col2:
        lv_alkphos = st.number_input("Alkaline Phosphotase", min_value=0.0, 
                                   value=user_health_data.get('lv_alkphos', 80.0), step=0.1, key="lv_alkphos")
        lv_sgpt = st.number_input("SGPT Alamine Aminotransferase", min_value=0.0, 
                                value=user_health_data.get('lv_sgpt', 25.0), step=0.1, key="lv_sgpt")
    
    with col3:
        lv_sgot = st.number_input("SGOT Aspartate Aminotransferase", min_value=0.0, 
                                value=user_health_data.get('lv_sgot', 28.0), step=0.1, key="lv_sgot")
        lv_total_protiens = st.number_input("โปรตีนรวม (g/dL)", min_value=0.0, 
                                          value=user_health_data.get('lv_total_protiens', 7.0), step=0.1, key="lv_total_protiens")
    
    with col4:
        lv_alb = st.number_input("อัลบูมิน (g/dL)", min_value=0.0, 
                               value=user_health_data.get('lv_alb', 4.0), step=0.1, key="lv_alb")
        lv_ag_ratio = st.number_input("A/G Ratio", min_value=0.0, 
                                    value=user_health_data.get('lv_ag_ratio', 1.2), step=0.1, key="lv_ag_ratio")
    
    # Section 5: Kidney Function and Cardiovascular
    st.markdown('<div class="section-header">การทำงานของไตและหัวใจ</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        lv_creatinine = st.number_input("ครีเอตินีน (mg/dL)", min_value=0.0, 
                                      value=user_health_data.get('lv_creatinine', 0.9), step=0.1, key="lv_creatinine")
        lv_bun = st.number_input("BUN (mg/dL)", min_value=0.0, 
                               value=user_health_data.get('lv_bun', 15.0), step=0.1, key="lv_bun")
    
    with col2:
        lv_gfr = st.number_input("GFR (mL/min/1.73m²)", min_value=0.0, 
                               value=user_health_data.get('lv_gfr', 90.0), step=0.1, key="lv_gfr")
        lv_urine_output = st.number_input("ปริมาณปัสสาวะ (mL/day)", min_value=0, 
                                        value=user_health_data.get('lv_urine_output', 1500), key="lv_urine_output")
    
    with col3:
        lv_totchol = st.number_input("คอเลสเตอรอลรวม (mg/dL)", min_value=0.0, 
                                   value=user_health_data.get('lv_totchol', 180.0), step=0.1, key="lv_totchol")
        lv_sysbp = st.number_input("ความดันตัวบน", min_value=0.0, 
                                 value=user_health_data.get('lv_sysbp', 120.0), step=0.1, key="lv_sysbp")
    
    with col4:
        lv_diabp = st.number_input("ความดันตัวล่าง", min_value=0.0, 
                                 value=user_health_data.get('lv_diabp', 80.0), step=0.1, key="lv_diabp")
        lv_heartrate = st.number_input("อัตราการเต้นหัวใจ (bpm)", min_value=0, 
                                     value=user_health_data.get('lv_heartrate', 72), key="lv_heartrate")
    
    # Save button
    if st.button("บันทึกข้อมูลสุขภาพ", use_container_width=True, key="save_health_data"):
        health_data = {
            'st_gender': st_gender,
            'lv_age': lv_age,
            'lv_weight': lv_weight,
            'lv_height': lv_height,
            'lv_bmi': lv_bmi,
            'st_smoking': st_smoking,
            'st_hypertension': st_hypertension,
            'lv_glucose': lv_glucose,
            'lv_HbA1c': lv_HbA1c,
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
            'lv_total_bilirubin': lv_total_bilirubin,
            'lv_direct_bilirubin': lv_direct_bilirubin,
            'lv_alkphos': lv_alkphos,
            'lv_sgpt': lv_sgpt,
            'lv_sgot': lv_sgot,
            'lv_total_protiens': lv_total_protiens,
            'lv_alb': lv_alb,
            'lv_ag_ratio': lv_ag_ratio,
            'lv_creatinine': lv_creatinine,
            'lv_bun': lv_bun,
            'lv_gfr': lv_gfr,
            'lv_urine_output': lv_urine_output,
            'lv_cigsperday': lv_cigsperday,
            'st_bpmeds': st_bpmeds,
            'st_prevalentstroke': st_prevalentstroke,
            'st_prevalenthyp': st_prevalenthyp,
            'lv_totchol': lv_totchol,
            'lv_sysbp': lv_sysbp,
            'lv_diabp': lv_diabp,
            'lv_heartrate': lv_heartrate,
            'last_updated': datetime.now().isoformat()
        }
        
        st.session_state.health_data[st.session_state.username] = health_data
        save_health_data()
        st.success("บันทึกข้อมูลสุขภาพเรียบร้อยแล้ว!")

# Screen 4: Lab Results (Simplified view)
def lab_results_screen():
    st.markdown('<div class="main-header">ข้อมูลทางห้องปฏิบัติการ (Lab Results)</div>', unsafe_allow_html=True)
    
    # Navigation buttons
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        if st.button("Home", use_container_width=True, key="lab_home"):
            navigate_to('home')
    
    with col2:
        if st.button("Profile", use_container_width=True, key="lab_profile"):
            navigate_to('profile')
    
    with col3:
        if st.button("Health Form", use_container_width=True, key="lab_health"):
            navigate_to('health_form')
    
    with col4:
        if st.button("Summary", use_container_width=True, key="lab_summary"):
            navigate_to('summary')
    
    with col5:
        if st.button("Logout", use_container_width=True, key="lab_logout"):
            st.session_state.logged_in = False
            st.session_state.username = ''
            navigate_to('home')
            st.rerun()
    
    # Display lab results if available
    if st.session_state.username in st.session_state.health_data:
        health_data = st.session_state.health_data[st.session_state.username]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**ผลตรวจเลือดพื้นฐาน**")
            st.metric("น้ำตาลกลูโคส", f"{health_data.get('lv_glucose', 0)} mg/dL")
            st.metric("HbA1c", f"{health_data.get('lv_HbA1c', 0)} %")
            st.metric("คอเลสเตอรอลรวม", f"{health_data.get('lv_totchol', 0)} mg/dL")
            st.metric("ครีเอตินีน", f"{health_data.get('lv_creatinine', 0)} mg/dL")
        
        with col2:
            st.markdown("**การทำงานของตับ**")
            st.metric("บิลิรูบินรวม", f"{health_data.get('lv_total_bilirubin', 0)} mg/dL")
            st.metric("SGPT", f"{health_data.get('lv_sgpt', 0)} U/L")
            st.metric("SGOT", f"{health_data.get('lv_sgot', 0)} U/L")
            st.metric("อัลบูมิน", f"{health_data.get('lv_alb', 0)} g/dL")
    
    else:
        st.info("ยังไม่มีข้อมูลผลการตรวจ กรุณากรอกข้อมูลในหน้า 'แบบฟอร์มบันทึกสุขภาพ'")

# Screen 5: Summary
def summary_screen():
    st.markdown('<div class="main-header">สรุปผล</div>', unsafe_allow_html=True)
    
    # Navigation buttons
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        if st.button("Home", use_container_width=True, key="summary_home"):
            navigate_to('home')
    
    with col2:
        if st.button("Profile", use_container_width=True, key="summary_profile"):
            navigate_to('profile')
    
    with col3:
        if st.button("Health Form", use_container_width=True, key="summary_health"):
            navigate_to('health_form')
    
    with col4:
        if st.button("Lab Results", use_container_width=True, key="summary_lab"):
            navigate_to('lab_results')
    
    with col5:
        if st.button("Logout", use_container_width=True, key="summary_logout"):
            st.session_state.logged_in = False
            st.session_state.username = ''
            navigate_to('home')
            st.rerun()
    
    # Summary content
    if st.session_state.username in st.session_state.health_data:
        health_data = st.session_state.health_data[st.session_state.username]
        
        st.markdown('<div class="sub-header">สรุปผลสุขภาพโดยรวม</div>', unsafe_allow_html=True)
        
        # Health status indicators
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            bmi_status = "ปกติ" if 18.5 <= health_data.get('lv_bmi', 0) <= 24.9 else "ผิดปกติ"
            st.metric("ดัชนีมวลกาย (BMI)", f"{health_data.get('lv_bmi', 0):.1f}", bmi_status)
        
        with col2:
            bp_status = "ปกติ" if health_data.get('lv_sysbp', 0) <= 120 and health_data.get('lv_diabp', 0) <= 80 else "ผิดปกติ"
            st.metric("ความดันโลหิต", f"{health_data.get('lv_sysbp', 0)}/{health_data.get('lv_diabp', 0)}", bp_status)
        
        with col3:
            glucose_status = "ปกติ" if health_data.get('lv_glucose', 0) <= 100 else "ผิดปกติ"
            st.metric("น้ำตาลในเลือด", f"{health_data.get('lv_glucose', 0)} mg/dL", glucose_status)
        
        with col4:
            chol_status = "ปกติ" if health_data.get('lv_totchol', 0) <= 200 else "ผิดปกติ"
            st.metric("คอเลสเตอรอล", f"{health_data.get('lv_totchol', 0)} mg/dL", chol_status)
        
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

# Main app logic
def main():
    # Check if user is logged in to determine which screens to show
    if not st.session_state.logged_in and st.session_state.current_screen != 'home':
        st.session_state.current_screen = 'home'
    
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
