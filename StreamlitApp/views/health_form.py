import streamlit as st
from datetime import datetime
from utils import get_latest_health_record, save_health_record, logout_user

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
    