
import streamlit as st
import pandas as pd

# กำหนดค่าเริ่มต้นของหน้า Streamlit
st.set_page_config(layout="wide", page_title="Health Risk Assessment App")

# --- ข้อมูลจากตารางแนบ (จำลองเพื่อใช้งานในโค้ด) ---
# โดยปกติคุณอาจจะต้องโหลดข้อมูลนี้จาก Excel/CSV
# แต่ในตัวอย่างนี้ผมสร้างเป็น list ของ dicts เพื่อให้โค้ดทำงานได้ทันที
input_fields_data = [
    {'name': 'st_gender', 'display_name': 'Gender', 'input_type': 'Dropdown', 'options': ['Female', 'Male']},
    {'name': 'lv_age', 'display_name': 'Age', 'input_type': 'Textbox', 'default': 30},
    {'name': 'lv_weight', 'display_name': 'Weight', 'input_type': 'Textbox', 'default': 60},
    {'name': 'lv_height', 'display_name': 'Height', 'input_type': 'Textbox', 'default': 170},
    {'name': 'lv_bmi', 'display_name': 'BMI', 'input_type': 'Textbox'},
    {'name': 'st_smoking', 'display_name': 'Smoking', 'input_type': 'Dropdown', 'options': ['Yes', 'No']},
    {'name': 'st_hypertension', 'display_name': 'Hypertension', 'input_type': 'Dropdown', 'options': ['Yes', 'No']},
    {'name': 'lv_glucose', 'display_name': 'Glucose', 'input_type': 'Textbox'},
    {'name': 'lv_hba1c', 'display_name': 'HbA1C level', 'input_type': 'Textbox'},
    {'name': 'st_diabetes', 'display_name': 'Diabetes', 'input_type': 'Dropdown', 'options': ['Yes', 'No']},
    {'name': 'st_heart_disease', 'display_name': 'Heart Disease', 'input_type': 'Dropdown', 'options': ['Yes', 'No']},
    {'name': 'st_family_history_with_overweight', 'display_name': 'Family History with Overweight', 'input_type': 'Dropdown', 'options': ['Yes', 'No']},
    {'name': 'st_favc', 'display_name': 'FAVC', 'input_type': 'Dropdown', 'options': ['Sometime', 'Frequently', 'Always']},
    {'name': 'st_fcvc', 'display_name': 'FCVC', 'input_type': 'Dropdown', 'options': ['Sometime', 'Frequently', 'Always']},
    {'name': 'st_ncp', 'display_name': 'NCP', 'input_type': 'Dropdown', 'options': ['1', '2', '3', '4']},
    {'name': 'st_caec', 'display_name': 'CAEC', 'input_type': 'Dropdown', 'options': ['No', 'Sometime', 'Frequently', 'Always']},
    {'name': 'st_ch2o', 'display_name': 'CH2O', 'input_type': 'Dropdown', 'options': ['Sometime', 'Frequently', 'Always']},
    {'name': 'st_scc', 'display_name': 'SCC', 'input_type': 'Dropdown', 'options': ['Yes', 'No']},
    {'name': 'st_faf', 'display_name': 'FAF', 'input_type': 'Dropdown', 'options': ['No', 'Sometime', 'Frequently', 'Always']},
    {'name': 'st_calc', 'display_name': 'CALC', 'input_type': 'Dropdown', 'options': ['No', 'Sometime', 'Frequently', 'Always']},
    {'name': 'lv_total_bilirubin', 'display_name': 'Total Bilirubin', 'input_type': 'Textbox'},
    {'name': 'lv_direct_bilirubin', 'display_name': 'Direct Bilirubin', 'input_type': 'Textbox'},
    {'name': 'lv_alkphos', 'display_name': 'Alkaline Phosphatase', 'input_type': 'Textbox'},
    {'name': 'lv_sgpt', 'display_name': 'SGPT', 'input_type': 'Textbox'},
    {'name': 'lv_sgot', 'display_name': 'SGOT', 'input_type': 'Textbox'},
    {'name': 'lv_total_proteins', 'display_name': 'Total Proteins', 'input_type': 'Textbox'},
    {'name': 'lv_alb', 'display_name': 'ALB Albumin', 'input_type': 'Textbox'},
    {'name': 'lv_a_g_ratio', 'display_name': 'A/G Ratio', 'input_type': 'Textbox'},
    {'name': 'lv_creatinine', 'display_name': 'Creatinine', 'input_type': 'Textbox'},
    {'name': 'lv_bun', 'display_name': 'BUN', 'input_type': 'Textbox'},
    {'name': 'lv_gfr', 'display_name': 'GFR', 'input_type': 'Textbox'},
    {'name': 'lv_urine_output', 'display_name': 'Urine Output', 'input_type': 'Textbox'},
    {'name': 'lv_egfrday', 'display_name': 'eGFR/day', 'input_type': 'Textbox'},
    {'name': 'st_bpmeds', 'display_name': 'BPMeds', 'input_type': 'Dropdown', 'options': ['Yes', 'No']},
    {'name': 'st_prevalentstroke', 'display_name': 'PrevalentStroke', 'input_type': 'Dropdown', 'options': ['Yes', 'No']},
    {'name': 'st_prevalenthyp', 'display_name': 'PrevalentHyp', 'input_type': 'Dropdown', 'options': ['Yes', 'No']},
    {'name': 'lv_totchol', 'display_name': 'TotChol', 'input_type': 'Textbox'},
    {'name': 'lv_sysbp', 'display_name': 'SysBP', 'input_type': 'Textbox'},
    {'name': 'lv_diabp', 'display_name': 'DiaBP', 'input_type': 'Textbox'},
    {'name': 'lv_heartrate', 'display_name': 'HeartRate', 'input_type': 'Textbox'},
    {'name': 'lv_glucose_f', 'display_name': 'Glucose (Fasting)', 'input_type': 'Textbox'},
]

# --- ฟังก์ชันสำหรับสร้าง Input Field (ใช้ในคอลัมน์กลาง) ---
def create_input_widget(field_data):
    """สร้าง widget รับข้อมูลตามประเภทที่กำหนด"""
    name = field_data['name']
    display_name = field_data['display_name']
    input_type = field_data['input_type']
    options = field_data.get('options', [])
    default = field_data.get('default', None)
    key = f"input_{name}"

    st.write(f"**{display_name}**")
    
    # Textbox input
    if input_type == 'Textbox':
        if default is not None:
            # ใช้ st.number_input สำหรับค่าตัวเลข
            try:
                # พยายามแปลงเป็น float ก่อน
                value = float(default)
                st.number_input("", value=value, key=key, format="%.2f")
            except:
                # ถ้าแปลงไม่ได้ให้ใช้ st.text_input
                st.text_input("", value=str(default), key=key)
        else:
            st.text_input("", key=key)

    # Dropdown/Selectbox input
    elif input_type == 'Dropdown' and options:
        st.selectbox("", options, key=key)

# --- แบ่งหน้าจอเป็น 3 คอลัมน์ ---
col1, col2, col3 = st.columns([1.5, 4, 2.5]) # อัตราส่วน: เมนู | Input Data | ผลลัพธ์ (ปรับได้ตามต้องการ)

# ==============================================================================
## 1. แทบเมนูด้านซ้ายมือ (col1)
# ==============================================================================
with col1:
    st.header("⚙️ เมนูควบคุม")
    st.markdown("---")
    
    # 1.1 Section แต่ละ input data (ใช้ expander จัดกลุ่ม)
    with st.expander("📝 ส่วน Input Data"):
        st.subheader("กลุ่มข้อมูล")
        # สร้างปุ่มสำหรับ Scroll ไปยัง Section ต่างๆ ในคอลัมน์กลาง
        if st.button("ข้อมูลพื้นฐาน (Gender, Age, Weight...)"):
            # ใน Streamlit ไม่มี native scroll-to element
            # แต่วิธีนี้ช่วยให้ผู้ใช้รู้ว่ามี Input data อะไรบ้าง
            st.info("โปรดเลื่อนดูที่คอลัมน์กลาง") 
        if st.button("ข้อมูลโรคประจำตัว (Hypertension, Diabetes...)"):
            st.info("โปรดเลื่อนดูที่คอลัมน์กลาง")
        if st.button("ข้อมูลพฤติกรรม (Smoking, Diet, Exercise...)"):
            st.info("โปรดเลื่อนดูที่คอลัมน์กลาง")
        if st.button("ข้อมูลผลเลือด (Bilirubin, Liver Enzymes...)"):
            st.info("โปรดเลื่อนดูที่คอลัมน์กลาง")

    st.markdown("---")

    # 1.2 Section การเลือก Model
    st.subheader("🤖 การเลือก Model")
    model_choice = st.radio(
        "เลือกประเภทการประมวลผล:",
        ("Traditional Model (e.g., Framingham)", "AI Model (e.g., Deep Learning)"),
        key="model_choice"
    )
    st.info(f"คุณเลือก: **{model_choice.split(' ')[0]}**")
    
    st.markdown("---")

    # 1.3 Section ปุ่มกดประมวลผล
    st.subheader("▶️ ประมวลผล")
    if st.button("**ประมวลผลหาความเสี่ยง**", type="primary", use_container_width=True):
        st.session_state['processed'] = True
        st.success("✅ ประมวลผลเสร็จสิ้น")
        # ในสถานการณ์จริง จะมีการเรียกฟังก์ชันประมวลผลที่นี่
        # e.g., result = run_model(st.session_state)
    else:
        st.session_state['processed'] = False

# ==============================================================================
## 2. แทบกลาง (col2) - แสดงข้อมูล Input Data (พร้อม Scrolling)
# ==============================================================================
with col2:
    st.title("📊 ข้อมูลนำเข้าเพื่อประเมินความเสี่ยง")
    st.markdown(
        """
        <div style="height: 700px; overflow-y: scroll; padding-right: 15px; border: 1px solid #ccc; border-radius: 5px;">
        """, 
        unsafe_allow_html=True
    )
    
    st.subheader("👥 ข้อมูลพื้นฐานและพฤติกรรม")
    
    # Loop สร้าง Input Fields
    for i, field in enumerate(input_fields_data):
        create_input_widget(field)
        
        # จัดกลุ่มข้อมูลด้วยการใส่หัวข้อย่อยเพื่อให้อ่านง่ายขึ้น
        if field['name'] == 'st_smoking':
            st.markdown("### 💊 ข้อมูลโรคประจำตัว/ยา")
        elif field['name'] == 'st_favc':
            st.markdown("### 🍎 ข้อมูลพฤติกรรมการกินและกิจกรรม")
        elif field['name'] == 'lv_total_bilirubin':
            st.markdown("### 🔬 ข้อมูลผลเลือดและพารามิเตอร์ทางชีวเคมี")
        elif field['name'] == 'st_bpmeds':
            st.markdown("### 🩺 ข้อมูลความดันโลหิตและอัตราการเต้นของหัวใจ")
        
        # ใส่ตัวแบ่งย่อยเพื่อให้ Scroll แล้วดูง่ายขึ้น
        if i % 3 == 2 and i != len(input_fields_data) - 1:
             st.markdown("---")

    st.markdown("</div>", unsafe_allow_html=True) # ปิด div สำหรับ Scrolling

# ==============================================================================
## 3. แทบขวามือ (col3) - แสดงผลลัพธ์
# ==============================================================================
with col3:
    st.header("💡 ผลการประมวลผล")
    st.markdown("---")
    
    # สร้างพื้นที่แสดงผลลัพธ์
    results_placeholder = st.empty()

    if st.session_state.get('processed', False):
        # จำลองผลลัพธ์เมื่อกดปุ่มประมวลผล
        risk_score = 15.7 # สมมติคะแนนความเสี่ยง
        risk_level = "ความเสี่ยงสูง (High Risk)"
        recommendation = "คุณควรปรึกษาแพทย์เพื่อดำเนินการตรวจเพิ่มเติมและปรับเปลี่ยนพฤติกรรมอย่างเคร่งครัด"

        with results_placeholder.container():
            st.subheader("สรุปผลการประเมินความเสี่ยง")
            
            st.metric(
                label="คะแนนความเสี่ยง (Risk Score)",
                value=f"{risk_score:.1f}%",
                delta="เทียบกับค่าเฉลี่ยประชากร" # สมมติว่ามีการเปรียบเทียบ
            )
            
            if "AI Model" in st.session_state['model_choice']:
                st.info("ประเมินด้วย **AI Model**")
            else:
                st.info("ประเมินด้วย **Traditional Model**")

            st.markdown("### ⚠️ ระดับความเสี่ยง")
            st.error(f"**{risk_level}**")
            
            st.markdown("---")
            
            st.markdown("### 🧑‍⚕️ ข้อเสนอแนะเบื้องต้น")
            st.markdown(f"> **{recommendation}**")
            
            # แสดงข้อมูล Input ที่นำไปใช้ (ตัวอย่างบางส่วน)
            st.markdown("---")
            with st.expander("ดูข้อมูล Input ที่ใช้ประมวลผล"):
                input_summary = {
                    "Gender": st.session_state.get('input_st_gender', 'N/A'),
                    "Age": st.session_state.get('input_lv_age', 'N/A'),
                    "Smoking": st.session_state.get('input_st_smoking', 'N/A'),
                    "Glucose": st.session_state.get('input_lv_glucose', 'N/A'),
                }
                st.json(input_summary)

    else:
        # ข้อความเริ่มต้นก่อนการประมวลผล
        results_placeholder.info(
            """
            กรุณากรอกข้อมูลใน **คอลัมน์กลาง** ให้ครบถ้วน แล้วกด **ปุ่มประมวลผล** ในเมนู **คอลัมน์ซ้าย** เพื่อดูผลลัพธ์การประเมินความเสี่ยงที่นี่
            """
        )

# --- คำแนะนำสำหรับการรันโค้ด ---
# วิธีรัน:
# 1. บันทึกโค้ดด้านบนเป็นไฟล์ .py (เช่น app.py)
# 2. เปิด Terminal/Command Prompt และรันคำสั่ง: streamlit run app.py

