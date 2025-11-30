import streamlit as st
from datetime import datetime
from utils import get_user_health_records, get_health_status, logout_user

# Plotly imports
try:
    import plotly.express as px
    import plotly.graph_objects as go
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False
    px = None
    go = None

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
    

