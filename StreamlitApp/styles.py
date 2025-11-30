import streamlit as st

def load_css():
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
