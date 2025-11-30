import streamlit as st
from utils import get_user_profile, logout_user, navigate_to

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
