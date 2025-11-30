import streamlit as st
from utils import get_user_profile, update_user_profile, logout_user

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
        status_enabled_text = "✅ **Status:** Feature AI is **Active**."
        status_disabled_text = "🛑 **Status:** Feature AI is **Inactive**."
        col_toggle, col_status = st.columns([1, 10])

        with col_toggle:
            toggled = st.toggle("Placeholder Label", label_visibility="hidden")
            st.session_state.feature_ai = toggled
            
        with col_status:
            if st.session_state.feature_ai:
                st.write(status_enabled_text)
            else:
                st.write(status_disabled_text)
    

