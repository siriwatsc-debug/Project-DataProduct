import streamlit as st
import pandas as pd

# กำหนดค่าเริ่มต้นของหน้า Streamlit
st.set_page_config(layout="wide", page_title="Health Risk Assessment App")

# --- ข้อมูลจากตารางแนบ (จำลองเพื่อใช้งานในโค้ด) ---
input_fields_data = [
    {'name': 'st_gender', 'display_name': 'Gender (เพศ)', 'input_type': 'Dropdown', 'options': ['Female', 'Male']},
    {'name': 'lv_age', 'display_name': 'Age (อายุ)', 'input_type': 'Textbox', 'default': 30, 'format': 'int'},
    {'name': 'lv_weight', 'display_name': 'Weight (น้ำหนัก)', 'input_type': 'Textbox', 'default': 60.0, 'format': 'float'},
    {'name': 'lv_height', 'display_name': 'Height (ส่วนสูง)', 'input_type': 'Textbox', 'default': 170.0, 'format': 'float'},
    {'name': 'st_smoking', 'display_name': 'Smoking (สูบบุหรี่)', 'input_type': 'Dropdown', 'options': ['Yes', 'No']},
    {'name': 'st_hypertension', 'display_name': 'Hypertension (ความดันโลหิตสูง)', 'input_type': 'Dropdown', 'options': ['Yes', 'No']},
    # เพิ่ม field ที่สำคัญอื่นๆ เข้ามาเป็นตัวอย่าง
    {'name': 'lv_glucose', 'display_name': 'Glucose (น้ำตาลในเลือด)', 'input_type': 'Textbox', 'default': 90.0, 'format': 'float'},
    {'name': 'lv_heartrate', 'display_name': 'HeartRate (อัตราการเต้นหัวใจ)', 'input_type': 'Textbox', 'default': 75, 'format': 'int'},
    {'name': 'lv_totchol', 'display_name': 'TotChol (คอเลสเตอรอลรวม)', 'input_type': 'Textbox', 'default': 200.0, 'format': 'float'},
    {'name': 'st_diabetes', 'display_name': 'Diabetes (เบาหวาน)', 'input_type': 'Dropdown', 'options': ['Yes', 'No']},
]

# --- ฟังก์ชันสำหรับสร้าง Input Field (ใช้ในคอลัมน์กลาง) ---
def create_input_widget(field_data):
    """สร้าง widget รับข้อมูลตามประเภทที่กำหนด"""
    name = field_data['name']
    display_name = field_data['display_name']
    input_type = field_data['input_type']
    options = field_data.get('options', [])
    default = field_data.get('default', None)
    data_format = field_data.get('format', 'str') # กำหนด format เพิ่มเติม
    key = f"input_{name}"

    st.write(f"**{display_name}**")
    
    # Textbox input (ใช้ st.number_input ถ้าเป็นตัวเลข)
    if input_type == 'Textbox':
        if data_format == 'float':
            st.number_input("", value=float(default) if default is not None else 0.0, key=key, format="%.2f", step=0.1)
        elif data_format == 'int':
            st.number_input("", value=int(default) if default is not None else 0, key=key, step=1)
        else:
            st.text_input("", value=str(default) if default is not None else "", key=key)

    # Dropdown/Selectbox input
    elif input_type == 'Dropdown' and options:
        st.selectbox("", options, key=key)

# --- ฟังก์ชันดึงข้อมูล Input ทั้งหมดจาก Session State ---
def get_all_input_data():
    """ดึงข้อมูลทั้งหมดที่ผู้ใช้กรอกจาก st.session_state"""
    input_data = {}
    for field in input_fields_data:
        key = f"input_{field['name']}"
        display_name = field['display_name']
        # ดึงค่าจาก session state โดยใช้ key ที่สร้างไว้
        input_data[display_name] = st.session_state.get(key, 'N/A')
    return input_data

# --- แบ่งหน้าจอเป็น 3 คอลัมน์ ---
col1, col2, col3 = st.columns([1.5, 4, 2.5])

# ==============================================================================
## 1. แทบเมนูด้านซ้ายมือ (col1)
# ==============================================================================
with col1:
    st.header("⚙️ เมนูควบคุม")
    st.markdown("---")
    
    # 1.2 Section การเลือก Model
    st.subheader("🤖 การเลือก Model")
    model_choice = st.radio(
        "เลือกประเภทการประมวลผล:",
        ("Traditional Model", "AI Model"),
        key="model_choice"
    )
    st.markdown("---")

    # 1.3 Section ปุ่มกดประมวลผล
    st.subheader("▶️ ประมวลผล")
    # เมื่อกดปุ่มนี้ ให้ตั้งค่า session state 'processed' เป็น True
    if st.button("**ประมวลผลหาความเสี่ยง**", type="primary", use_container_width=True):
        st.session_state['processed'] = True
        st.success("✅ ประมวลผลเสร็จสิ้น")
    
    # กำหนดสถานะเริ่มต้นถ้ายังไม่มีการกดปุ่ม
    if 'processed' not in st.session_state:
         st.session_state['processed'] = False


# ==============================================================================
## 2. แทบกลาง (col2) - แสดงข้อมูล Input Data (พร้อม Scrolling)
# ==============================================================================
with col2:
    st.title("📊 ข้อมูลนำเข้าเพื่อประเมินความเสี่ยง")
    
    # สร้าง Container สำหรับการ Scroll
    st.markdown(
        """
        <div style="height: 700px; overflow-y: scroll; padding-right: 15px; border: 1px solid #ccc; border-radius: 5px;">
        """, 
        unsafe_allow_html=True
    )
    
    st.subheader("กรุณากรอกข้อมูลให้ครบถ้วน:")
    
    # Loop สร้าง Input Fields
    for field in input_fields_data:
        create_input_widget(field)
        st.markdown("---") # เพิ่มเส้นแบ่งให้ดูเป็นระเบียบ

    st.markdown("</div>", unsafe_allow_html=True) # ปิด div สำหรับ Scrolling

# ==============================================================================
## 3. แทบขวามือ (col3) - แสดงผลลัพธ์ (แสดง Input Data หลังกดปุ่ม)
# ==============================================================================
with col3:
    st.header("💡 ผลการประมวลผล")
    st.markdown("---")
    
    # สร้างพื้นที่สำหรับแสดงผลลัพธ์
    results_placeholder = st.empty()

    # ตรวจสอบว่ามีการกดปุ่มประมวลผลหรือไม่
    if st.session_state.get('processed', False):
        
        # 1. ดึงข้อมูล Input ทั้งหมด
        user_input_data = get_all_input_data()
        
        with results_placeholder.container():
            st.subheader("✅ ข้อมูลที่คุณกรอก (Input Data)")
            st.info(f"Model ที่ใช้: **{st.session_state['model_choice']}**")
            
            # --- แสดงผลในรูปแบบตาราง (ง่ายต่อการตรวจสอบ) ---
            
            # สร้าง DataFrame จากข้อมูล Input
            df_input = pd.DataFrame(
                list(user_input_data.items()), 
                columns=['Field Name', 'Value']
            )
            # แสดงตาราง
            st.dataframe(df_input, use_container_width=True, hide_index=True)
            
            st.markdown("---")
            
            # --- จำลองส่วนผลลัพธ์ความเสี่ยง (Simulation) ---
            st.subheader("🔬 ผลการวิเคราะห์ความเสี่ยง (Simulation)")
            risk_score = 10.5 # ค่าจำลอง
            
            st.metric(
                label="คะแนนความเสี่ยงโรคหัวใจ (10-Year Risk)",
                value=f"{risk_score:.1f} %",
                delta_color="inverse", # สีเขียว/แดง ตามค่า
                delta="เทียบกับค่ามาตรฐาน"
            )
            
            st.markdown("---")
            st.markdown("### ข้อเสนอแนะ:")
            st.success("จากการประเมินเบื้องต้น ความเสี่ยงของคุณอยู่ในระดับต่ำ กรุณารักษาพฤติกรรมสุขภาพที่ดีต่อไป")
            

    else:
        # ข้อความเริ่มต้นก่อนการประมวลผล
        results_placeholder.info(
            """
            กรุณากรอกข้อมูลในคอลัมน์กลาง และกด **ปุ่มประมวลผล** ในคอลัมน์ซ้าย
            **ข้อมูล Input ที่กรอก** และ **ผลการวิเคราะห์** จะแสดงที่นี่
            """
        )
