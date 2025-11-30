import streamlit as st
from utils import get_user_profile, verify_user, register_user, logout_user, navigate_to

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
