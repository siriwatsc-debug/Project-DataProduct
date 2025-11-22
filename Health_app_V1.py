import streamlit as st
import pandas as pd

# ----------------------------------------------------
# 1. Configuration and Utility Functions
# ----------------------------------------------------

# ตั้งค่าหน้าเพจ (ต้องอยู่บนสุดของสคริปต์)
st.set_page_config(
    page_title="Smart Health Checker",
    layout="wide",
    # ใช้ "expanded" เป็นค่าเริ่มต้น 
    initial_sidebar_state="expanded" 
)

# รายชื่อ field_name ทั้งหมดที่ต้องการรีเซ็ต
FIELD_NAMES_TO_RESET = [
    'lv_gender', 'lv_age', 'lv_weight', 'lv_height', 'lv_bmi', 'st_smoking', 
    'st_hypertension', 'lv_glucose', 'lv_hba1c', 'st_diabetes', 'st_heart_disease', 
    'st_family_history_with_overweight', 'st_favc', 'lv_fcvc', 'lv_ncp', 'st_caec', 
    'lv_ch2o', 'st_scc', 'lv_faf', 'st_calc', 'lv_total_bilirubin', 'lv_direct_bilirubin', 
    'lv_alkphos', 'lv_sgot', 'lv_total_proteins', 'lv_alb', 'lv_ag_ratio', 
    'lv_creatinine', 'lv_bun', 'lv_gfr', 'lv_urine_output', 'lv_cigsperday', 
    'st_bpmeds', 'st_prevalentstroke', 'st_prevalenthyp', 'lv_totchol', 
    'lv_sysbp', 'lv_diabp', 'lv_hr'
]

# การจัดการสถานะหน้าจอ (Session State)
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'Home'
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = "รอการป้อนข้อมูลและการประมวลผล..."
if 'model_type' not in st.session_state:
    st.session_state.model_type = 'Traditional Model (ML)'
if 'input_data_summary' not in st.session_state:
    st.session_state.input_data_summary = {}

def get_form_data():
    """ดึงข้อมูลทั้งหมดจาก session state ที่ถูกใช้ในฟอร์ม"""
    data = {key: st.session_state.get(key) for key in FIELD_NAMES_TO_RESET}
    return data

def reset_form_data():
    """รีเซ็ตค่าทั้งหมดใน session state ที่เกี่ยวข้องกับข้อมูล Input"""
    for key in FIELD_NAMES_TO_RESET:
        if key in st.session_state:
            del st.session_state[key]
            
    # รีเซ็ตค่าผลลัพธ์และการสรุป
    st.session_state.analysis_results = "รอการป้อนข้อมูลและการประมวลผล..."
    st.session_state.input_data_summary = {}
    
    # Force rerun
    st.rerun()


def mock_process_data(data, model_type):
    """ฟังก์ชันจำลองการประมวลผลความเสี่ยง"""
    if not all(data.values()): 
        return "🚨 กรุณากรอกข้อมูลในแบบฟอร์มให้ครบถ้วนก่อนประมวลผล"

    risk_score = 0
    if data.get('st_smoking') == 'Yes': risk_score += 5
    try:
        if data.get('lv_hba1c', 0) > 6.0: risk_score += 10
        if data.get('lv_sysbp', 0) > 140 or data.get('lv_diabp', 0) > 90: risk_score += 15
    except TypeError:
        return "🚨 ข้อมูลค่าตัวเลขไม่ถูกต้อง กรุณาตรวจสอบและกรอกใหม่"
        
    model_factor = 1.0
    if "AI Model" in model_type:
        model_factor = 1.3 
        
    final_risk = risk_score * model_factor
    
    if final_risk >= 35: risk_level = "สูงมาก (Very High Risk)"
    elif final_risk >= 20: risk_level = "ปานกลาง (Medium Risk)"
    else: risk_level = "ต่ำ (Low Risk)"
        
    return f"""
    ### 📈 ผลการประเมินความเสี่ยง ({model_type})
    
    - **ระดับความเสี่ยงที่ทำนาย:** **{risk_level}**
    - **คะแนนความเสี่ยงโดยรวม (จำลอง):** {final_risk:.2f}
    """

# ----------------------------------------------------
# 2. Page Functions
# ----------------------------------------------------

def screen_home():
    """
    Screen 1: หน้า Home (1 คอลัมน์ ไม่มีรายการเมนูใดๆ)
    """
    st.title("Welcome to Smart Health Checker")
    st.markdown("---")
    
    # ใช้ st.container เพื่อจัดกลุ่มเนื้อหาทั้งหมดในคอลัมน์เดียว
    with st.container(border=True):
        st.header("🎯 ภาพรวมแอปพลิเคชัน")
        
        # จัดวางภาพ 2 ภาพในคอลัมน์ย่อยภายในคอลัมน์หลัก
        col_img1, col_img2 = st.columns(2)
        
        with col_img1:
            st.image("https://via.placeholder.com/600x300/004772/FFFFFF?text=Data+Product+Overview", caption="ภาพรวมของ Data Product", use_column_width=True)
        
        with col_img2:
            st.image("https://via.placeholder.com/600x300/004772/FFFFFF?text=Model+Functionality", caption="การทำงานของ Model", use_column_width=True)
            
        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("💡 คำแนะนำการใช้งาน")
        st.write("แอปพลิเคชันนี้ออกแบบมาเพื่อประเมินความเสี่ยงด้านสุขภาพเบื้องต้น โดยใช้ข้อมูลที่ป้อนเข้าร่วมกับการประมวลผลจาก Machine Learning หรือ AI Model กรุณากดปุ่มด้านล่างเพื่อเริ่มบันทึกข้อมูลและรับผลการวิเคราะห์")
    
    st.markdown("---")
    # ปุ่มเริ่มใช้งาน
    if st.button("🚀 เริ่มบันทึกข้อมูล", type="primary", use_container_width=True):
        st.session_state.current_page = 'Input'
        st.rerun()
            
def screen_input_and_analysis():
    """
    Screen 2: หน้าบันทึกข้อมูลและประมวลผล (Sidebar | Input | Process/Summary)
    """
    
    # ----------------------------------------------------
    # คอลัมน์ 1: Sidebar Menu (แถบเมนูจะปรากฏในหน้านี้)
    # ----------------------------------------------------
    with st.sidebar:
        st.header("⚙️ เมนูและการตั้งค่า")
        
        # 1.1 Home Link
        if st.button("🏠 Home", use_container_width=True):
            st.session_state.current_page = 'Home'
            st.rerun()
            
        st.markdown("---")
        
        # 1.2 Input Data (ใช้ st.expander)
        with st.expander("1.2 Input Data"):
            st.markdown("- [ข้อมูลประชากร](#demographics)")
            st.markdown("- [ประวัติโรคและพฤติกรรม](#behavior)")
            st.markdown("- [ข้อมูลห้องปฏิบัติการ](#lab-results)")
        
        # 1.3 การเลือก Model
        st.subheader("1.3 เลือก Model")
        model_options = [
            "Traditional Model (ML)", 
            "AI Model (ie. Gemini, Deepseek)"
        ]
        st.radio(
            "ประเภท Model ประมวลผล",
            options=model_options,
            key='model_type',
        )

    # ----------------------------------------------------
    # คอลัมน์ 2 และ 3: Main Layout (Input | Process/Summary)
    # ----------------------------------------------------
    
    col_input, col_output = st.columns([5, 5]) 
    
    # --- คอลัมน์ 2: แบบฟอร์มบันทึกฟิลด์ (Input) ---
   
    with col_input:
        st.title("แบบฟอร์มบันทึกฟิลด์จากตาราง")
        st.info("กรุณากรอกข้อมูลสุขภาพทั้งหมดเพื่อประเมินผล")
        
        # ใช้ st.form เพื่อให้สามารถ Scrolling และรวม Input Fields ทั้งหมด
        with st.form(key='health_data_form'):
            
            # --- ส่วนย่อย: ข้อมูลประชากร (Demographics) ---
            st.markdown(f'<a name="demographics"></a>', unsafe_allow_html=True)
            st.subheader("1. ข้อมูลประชากร")
            c2_1, c2_2 = st.columns(2)
            
            with c2_1:
                st.selectbox("Gender (เพศ)", options=["Female", "Male"], key='lv_gender')
                st.number_input("Age (อายุ)", min_value=18, max_value=120, value=st.session_state.get('lv_age', 30), key='lv_age', step=1)
                st.number_input("Weight (น้ำหนัก)", min_value=20.0, max_value=300.0, value=st.session_state.get('lv_weight', 70.0), step=0.1, key='lv_weight')
                st.number_input("Height (ส่วนสูง)", min_value=50.0, max_value=250.0, value=st.session_state.get('lv_height', 170.0), step=0.1, key='lv_height')
                st.number_input("BMI", min_value=10.0, max_value=60.0, value=st.session_state.get('lv_bmi', 25.0), step=0.1, key='lv_bmi')
                st.selectbox("Smoking (สูบบุหรี่)", options=["Yes", "No"], key='st_smoking')
            
            with c2_2:
                st.selectbox("Hypertension (ความดันโลหิตสูง)", options=["Yes", "No"], key='st_hypertension')
                st.number_input("Glucose (ระดับน้ำตาล)", value=st.session_state.get('lv_glucose', 90.0), step=1.0, key='lv_glucose')
                st.number_input("HbA1C_level (ระดับน้ำตาลสะสม)", value=st.session_state.get('lv_hba1c', 5.5), step=0.1, key='lv_hba1c')
                st.selectbox("Diabetes (โรคเบาหวาน)", options=["Yes", "No"], key='st_diabetes')
                st.selectbox("Heart Disease (โรคหัวใจ)", options=["Yes", "No"], key='st_heart_disease')
                st.selectbox("Family History Overweight", options=["Yes", "No"], key='st_family_history_with_overweight')
                
            # --- ส่วนย่อย: พฤติกรรม (Behavior) ---
            st.markdown(f'<a name="behavior"></a>', unsafe_allow_html=True)
            st.subheader("2. ประวัติโรคและพฤติกรรมเสี่ยง")
            c2_3, c2_4 = st.columns(2)
            
            with c2_3:
                st.selectbox("FAVC (ทานอาหารไขมันสูงบ่อย?)", options=["Yes", "No"], key='st_favc')
                st.selectbox("FCVC (ทานผักผลไม้บ่อย?)", options=["Sometime", "Frequently", "Always", "No", "Seldom"], key='lv_fcvc') 
                st.selectbox("NCP (ทานอาหารหลักบ่อย?)", options=["1", "2", "3", "4", "5"], key='lv_ncp') 
                st.selectbox("CAEC (ทานอาหารอื่นบ่อย?)", options=["Sometime", "Frequently", "Always", "No", "Seldom"], key='st_caec')
                st.selectbox("CH2O (ดื่มน้ำบ่อย?)", options=["Sometime", "Frequently", "Always", "No", "Seldom"], key='lv_ch2o')
            with c2_4:
                st.selectbox("SCC (ตรวจสอบแคลอรี่?)", options=["Yes", "No"], key='st_scc')
                st.selectbox("FAF (ออกกำลังกายบ่อย?)", options=["Sometime", "Frequently", "Always", "No", "Seldom"], key='lv_faf')
                st.selectbox("CALC (ดื่มแอลกอฮอล์บ่อย?)", options=["Sometime", "Frequently", "Always", "No", "Seldom"], key='st_calc')
                st.number_input("Total Bilirubin", value=st.session_state.get('lv_total_bilirubin', 1.0), step=0.01, key='lv_total_bilirubin')
                st.number_input("Direct Bilirubin", value=st.session_state.get('lv_direct_bilirubin', 0.2), step=0.01, key='lv_direct_bilirubin')
            
            # --- ส่วนย่อย: ห้องปฏิบัติการและ BP (Lab Results & BP) ---
            st.markdown(f'<a name="lab-results"></a>', unsafe_allow_html=True)
            st.subheader("3. ข้อมูลห้องปฏิบัติการและ BP")
            c2_5, c2_6 = st.columns(2)
            
            with c2_5:
                st.number_input("Alkaline Phosphatase", value=st.session_state.get('lv_alkphos', 70.0), step=0.1, key='lv_alkphos')
                st.number_input("Sgot Aspartate Aminotransferase", value=st.session_state.get('lv_sgot', 25.0), step=0.1, key='lv_sgot')
                st.number_input("Total Proteins", value=st.session_state.get('lv_total_proteins', 7.0), step=0.01, key='lv_total_proteins')
                st.number_input("ALB Albumin", value=st.session_state.get('lv_alb', 4.0), step=0.01, key='lv_alb')
                st.number_input("A/G Ratio", value=st.session_state.get('lv_ag_ratio', 1.5), step=0.01, key='lv_ag_ratio')
                st.number_input("Creatinine", value=st.session_state.get('lv_creatinine', 1.0), step=0.01, key='lv_creatinine')
                st.number_input("BUN", value=st.session_state.get('lv_bun', 15.0), step=0.1, key='lv_bun')
                st.number_input("GFR (mL/min/1.73m²)", value=st.session_state.get('lv_gfr', 90.0), step=1.0, key='lv_gfr')
                st.number_input("Urine Output (mL/day)", value=st.session_state.get('lv_urine_output', 1500.0), step=10.0, key='lv_urine_output')
            with c2_6:
                st.number_input("CigsPerDay (บุหรี่/วัน)", min_value=0, max_value=100, value=st.session_state.get('lv_cigsperday', 0), key='lv_cigsperday')
                st.selectbox("BPmeds (ใช้ยาความดัน)", options=["Yes", "No"], key='st_bpmeds')
                st.selectbox("Prevalent Stroke", options=["Yes", "No"], key='st_prevalentstroke')
                st.selectbox("Prevalent Hyp", options=["Yes", "No"], key='st_prevalenthyp')
                st.number_input("TotChol (คอเลสเตอรอลรวม)", value=st.session_state.get('lv_totchol', 200.0), step=0.1, key='lv_totchol')
                st.number_input("Sys BP (ความดันบน)", min_value=60, max_value=250, value=st.session_state.get('lv_sysbp', 120), key='lv_sysbp')
                st.number_input("Dia BP (ความดันล่าง)", min_value=30, max_value=150, value=st.session_state.get('lv_diabp', 80), key='lv_diabp')
                st.number_input("Heart Rate (bpm)", min_value=30, max_value=200, value=st.session_state.get('lv_hr', 75), key='lv_hr')
                
                show_value_button = st.form_submit_button("แสดงผล Value", type="secondary", use_container_width=True)
        
        if show_value_button:
            st.session_state.input_data_summary = get_form_data()

    # --- คอลัมน์ 3: การประมวลผลและการแสดงผลลัพธ์ (Output) ---
    with col_output:
        st.title("การประมวลผล")
        st.markdown("---")
        
        if st.session_state.input_data_summary:
            st.subheader("Summary ข้อมูล Input")
            data_to_display = st.session_state.input_data_summary
            df_summary = pd.DataFrame(data_to_display.items(), columns=['Field Name', 'Value'])
            st.dataframe(df_summary, height=250, use_container_width=True)
        else:
            st.write("กด 'แสดงผล Value' เพื่อดูข้อมูลสรุป")

        process_button_col3 = st.button("กดประมวลผล", type="primary", use_container_width=True)  
        
        if process_button_col3:
            with st.spinner("กำลังประมวลผล..."):
                input_data = get_form_data()
                results = mock_process_data(input_data, st.session_state.model_type)
                st.session_state.analysis_results = results
                st.session_state.input_data_summary = input_data # อัปเดตข้อมูลล่าสุดก่อนแสดง
        
        st.markdown("---")
        st.subheader("ผลการประเมินความเสี่ยง")
        
        st.markdown(st.session_state.analysis_results)
        
        # เพิ่มปุ่มสำหรับกรอกข้อมูลใหม่
        st.markdown("---")
        st.subheader("ดำเนินการต่อไป")
        if st.button("🔄 กรอกข้อมูลใหม่ (Reset Form)", type="secondary", use_container_width=True):
            reset_form_data()
        
# ----------------------------------------------------
# 3. App Main Run Logic
# ----------------------------------------------------

if __name__ == "__main__":
    if st.session_state.current_page == 'Home':
        screen_home()
    elif st.session_state.current_page == 'Input':
        screen_input_and_analysis()