import streamlit as st
from utils import get_user_health_records, get_health_status, logout_user

import plotly.graph_objects as go
import numpy as np

from MyPackage.myclass import MyModel, MyAIGenerator

@st.cache_resource(ttl=3600)
def init_model():
    mm = MyModel()
    return mm
mm = init_model()

@st.cache_resource(ttl=3600)
def get_model_prediction(health_data):
    prediction = mm.predict_all_models(health_data)
    return prediction


if 'feature_ai' not in st.session_state:
    st.session_state.feature_ai = False


@st.cache_resource(ttl=3600)
def init_ai(google_api_key, model_name):
    ai = MyAIGenerator(google_api_key, model_name)
    return ai

@st.cache_resource(ttl=3600)
def get_ai_recommendations(health_data, google_api_key, model_name):
    ai = init_ai(google_api_key, model_name)
    ai_recommendations = ai.get_response(health_data)
    return ai_recommendations



def plot_feature(name, df, feature, mark_value):
    """
    Dynamic plot for a given feature in dataframe.
    - Numeric → Bell curve
    - Category → Bar chart
    """
    print(feature)

    col_data = df[feature].dropna()

    # Detect numeric column
    is_numeric = np.issubdtype(col_data.dtype, np.number)

    # ============================================================
    # NUMERIC → Bell Curve
    # ============================================================
    height = 100
    if is_numeric:
        # สมมติ numeric column
        data = df[feature].dropna().astype(float)

        # แปลง mark_value เป็น float
        try:
            mark_value_float = float(mark_value)
        except:
            mark_value_float = None  # กรณีแปลงไม่ได้ ให้ skip mark

        # สร้าง histogram จากข้อมูลจริง
        counts, bins = np.histogram(data, bins=20)  # ปรับ bins ได้
        bin_centers = 0.5 * (bins[1:] + bins[:-1])

        fig = go.Figure()
        fig.add_trace(go.Bar(x=bin_centers, y=counts))

        # Highlight selected value
        if mark_value_float is not None:
            y_mark = counts[np.abs(bin_centers - mark_value_float).argmin()]
            fig.add_trace(go.Scatter(
                x=[mark_value_float],
                y=[y_mark],
                mode="markers+text",
                text=[str(mark_value_float)],
                textposition="bottom left",
                marker=dict(size=12, color="red")
            ))

        fig.update_layout(
            showlegend=False,
            height=height,
            template="plotly_white",
            margin=dict(l=2, r=2, t=2, b=2),
            xaxis=dict(
                showgrid=False,
                showticklabels=False,
                zeroline=False,
                title=None
            ),
            yaxis=dict(
                showgrid=False,
                showticklabels=False,
                zeroline=False,
                title=None
            ),
        )

        st.plotly_chart(fig, use_container_width=True, key=name + feature + "_bar_chart")


    # ============================================================
    # CATEGORY → Bar Chart
    # ============================================================
    else:
        counts = col_data.value_counts()

        fig = go.Figure()
        fig.add_trace(go.Bar(x=counts.index, y=counts.values))

        # Highlight selected category
        if mark_value in counts.index:
            fig.add_trace(go.Scatter(
                x=[mark_value],
                y=[counts[mark_value]],
                mode="markers+text",
                # text=[str(mark_value)],
                textposition="bottom left",
                marker=dict(size=12, color="red")
            ))

        fig.update_layout(
            # title=None,
            showlegend=False,
            height=height,
            template="plotly_white",
            margin=dict(l=2, r=2, t=2, b=2),
            xaxis=dict(
                showgrid=False,
                showticklabels=False,
                zeroline=False,
                title=None
            ),
            yaxis=dict(
                showgrid=False,
                showticklabels=False,
                zeroline=False,
                title=None
            ),
        )

        st.plotly_chart(fig, use_container_width=True, key=name + feature + "_bar_chart")

def summary_screen():
    st.markdown('<div class="main-header">สรุปผล</div>', unsafe_allow_html=True)
    
    # Summary content
    user_records = get_user_health_records(st.session_state.user_id)
    count_data_error = 0 # Count fields with data error

    if user_records:
        latest_date = max(user_records.keys())
        health_data = user_records[latest_date]
        
        st.markdown('<div class="sub-header">สรุปผลสุขภาพโดยรวม</div>', unsafe_allow_html=True)
        
        # Health status indicators
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            bmi_value = health_data.get('lv_bmi', 0)
            icon, status, status_class = get_health_status(bmi_value, (18.5, 24.9), "normal")

            if bmi_value == 0:
                icon = "❌"
                status = "Data Error"
                status_class = "abnormal"
                delta_color = "off" 
                count_data_error = count_data_error + 1
            else:
                if bmi_value < 18.5:
                    icon = "⬇️❌" 
                    status = "น้ำหนักต่ำ"
                    status_class = "abnormal"
                    delta_color = "off" 
                elif 18.5 <= bmi_value <= 24.9:
                    icon = "✅"
                    status = "ปกติ"
                    status_class = "normal"
                    delta_color = "normal" 
                elif bmi_value > 24.9:  
                    icon = "❌" 
                    status = "น้ำหนักเกิน"
                    status_class = "abnormal"
                    delta_color = "off" 
                    
            #delta_color = "normal" if status_class == "normal" else "off"
            st.metric("ดัชนีมวลกาย (BMI)", f"{bmi_value:.1f}", 
                     delta=f"{icon} {status}", delta_color=delta_color)
        
        with col2:
            sysbp = health_data.get('lv_sysbp', 0)
            diabp = health_data.get('lv_diabp', 0)

            if sysbp == 0 or diabp == 0:
                icon = "❌"
                status = "Data Error"
                delta_color = "off"
                count_data_error = count_data_error + 1
            else:
                if sysbp <= 120 or diabp <= 80: 
                    icon = "✅"
                    status = "ปกติ" 
                    delta_color = "normal"
                else:
                    if sysbp > 120 or diabp > 80:
                        icon = "❌"
                        status = "สูง" 
                        delta_color = "off"
                
            st.metric("ความดันโลหิต", f"{sysbp}/{diabp}", 
                     delta=f"{icon} {status}", delta_color=delta_color)
        
        with col3:
            glucose_value = health_data.get('lv_glucose', 0)
            icon, status, status_class = get_health_status(glucose_value, 100, "high_bad")

            if glucose_value == 0:
                icon = "❌"
                status = "Data Error"
                status_class = "abnormal"
                delta_color = "off"
                count_data_error = count_data_error + 1
            else:
                if glucose_value <= 100:
                    icon = "✅"
                    status = "ปกติ" 
                    status_class = "normal"
                    delta_color = "normal"
                elif glucose_value > 100:
                    icon = "❌"
                    status = "สูง" 
                    status_class = "abnormal"
                    delta_color = "off"

            st.metric("น้ำตาลในเลือด", f"{glucose_value} mg/dL", 
                     delta=f"{icon} {status}", delta_color=delta_color)
        
        with col4:
            chol_value = health_data.get('lv_totchol', 0)
            icon, status, status_class = get_health_status(chol_value, 200, "high_bad")
            
            if chol_value == 0:
                icon = "❌"
                status = "Data Error"
                status_class = "normal"
                delta_color = "off"
                count_data_error = count_data_error + 1
            else:
                if chol_value <= 200:
                    icon = "✅"
                    status = "ปกติ" 
                    status_class = "normal"
                    delta_color = "normal"
                elif chol_value > 200:
                    icon = "❌"
                    status = "สูง" 
                    status_class = "abnormal"
                    delta_color = "off"
            
            st.metric("คอเลสเตอรอล", f"{chol_value} mg/dL", 
                     delta=f"{icon} {status}", delta_color=delta_color)
        
        # Risk factors
        st.markdown('<div class="sub-header">ทำนายผลโรค</div>', unsafe_allow_html=True)
        if count_data_error : #Input data = 0 some fields
            st.error("Data Error : การวิเคราะห์ผลอาจคลาดเคลื่อน กรุณาตรวจสอบข้อมูลสุขภาพ")

        # model_prediction = []
        # if health_data.get('st_smoking') == 'Yes':
        #     model_prediction.append("การสูบบุหรี่")
        # if health_data.get('st_hypertension') == 'Yes':
        #     model_prediction.append("ความดันโลหิตสูง")
        # if health_data.get('st_diabetes') == 'Yes':
        #     model_prediction.append("เบาหวาน")
        # if health_data.get('st_heart_disease') == 'Yes':
        #     model_prediction.append("โรคหัวใจ")
        # if health_data.get('st_family_history_with_overweight') == 'Yes':
        #     model_prediction.append("ประวัติครอบครัวน้ำหนักเกิน")
        
        # if model_prediction:
        #     st.warning(f"**ปัจจัยเสี่ยงที่พบ:** {', '.join(model_prediction)}")
        # else:
        #     st.success("**ไม่พบปัจจัยเสี่ยงหลัก**")
        


        name_deceases = {
            'Diabetes $ label': 'โรคเบาหวาน',
            'Obesity $ Label': 'โรคอ้วน',
            'Liver $ Label': 'โรคตับ',
            'Kidney $ Label1': 'โรคไต',
            'Kidney $ Label2': 'ความต้องการฟอกไต',
        }
        ignore_feature = [
            'st_gender',
            'lv_age',
            'lv_weight',
            'label',
        ]
        ml_predictions = get_model_prediction(health_data)
        col_d1, col_d2, col_d3, col_d4, col_d5 = st.columns(5)
        for key in ml_predictions:
            name_decease = name_deceases[key]
            predict = ml_predictions[key]['predict']
            feature_input = ml_predictions[key]['feature_input']
            original_df = ml_predictions[key]['original_df']

            with col_d1:
                st.write(name_decease)
            with col_d2:
                #st.write(predict)
                #risk_status = "เสี่ยงต่ำ" if (predict == 0 or predict == 'Normal_Weight')  else "เสี่ยงสูง"
                #st.write(f"{predict} - {risk_status}")

                if predict == 0 :
                    st.success("เสี่ยงต่ำ")
                if predict == 1 :
                    st.error("เสี่ยงสูง")
                if predict == 'Normal_Weight' :
                    st.success("น้ำหนักตัวอยู่ในเกณฑ์สุขภาพดี")
                if predict == 'Insufficient_Weight' :
                    st.warning("น้ำหนักตัวน้อยกว่ามาตรฐาน")
                if predict == 'Overweight_Level_I' or predict == 'Overweight_Level_II' :
                    st.error("น้ำหนักเกินมาตรฐาน")
                if predict == 'Obesity_Type_I' or predict == 'Obesity_Type_II' or predict == 'Obesity_Type_III':
                    st.error("มีความเสี่ยงโรคอ้วน")  

            with col_d3:
                # Inputs
                columns = original_df.columns
                feature = columns[1]

                # for feature in columns:
                #     if feature not in ignore_feature:
                #         st.write(feature)
                #         plot_feature(key, original_df, feature, feature_input[feature])
            

            
        if st.session_state.feature_ai:
            ai_recommendations = get_ai_recommendations(health_data, st.secrets['GOOGLE_API']['api_key'], st.secrets['GOOGLE_API']['model_name'])

            st.markdown('<div class="sub-header">วิเคราะห์โรคโดย AI</div>', unsafe_allow_html=True)
            
            risks = []
            for rec in ai_recommendations['desease_risk']:
                risks.append(rec)

            for i, rec in enumerate(risks, 1):
                st.info(f"{i}. {rec['name']} ({rec['risk']}) - {rec['recommendation']}")


            # Recommendations
            st.markdown('<div class="sub-header">คำแนะนำ</div>', unsafe_allow_html=True)
            


            recommendations = []
            for rec in ai_recommendations['overall_recommendation']:
                recommendations.append(rec)

            # if health_data.get('lv_bmi', 0) > 24.9:
            #     recommendations.append("ควรควบคุมน้ำหนักและออกกำลังกายสม่ำเสมอ")
            # if health_data.get('lv_glucose', 0) > 100:
            #     recommendations.append("ควรควบคุมระดับน้ำตาลในเลือด")
            # if health_data.get('lv_totchol', 0) > 200:
            #     recommendations.append("ควรควบคุมระดับคอเลสเตอรอล")
            # if health_data.get('st_smoking') == 'Yes':
            #     recommendations.append("ควรลดหรือหยุดสูบบุหรี่")
            # if health_data.get('st_faf') in ['No', 'Sometimes']:
            #     recommendations.append("ควรออกกำลังกายให้บ่อยขึ้น")
            
            if not recommendations:
                recommendations.append("สุขภาพโดยรวมอยู่ในเกณฑ์ดี ควรดูแลรักษาสุขภาพตามปกติ")
            
            for i, rec in enumerate(recommendations, 1):
                st.info(f"{i}. {rec}")
    
    else:
        st.info("ยังไม่มีข้อมูลสุขภาพ กรุณากรอกข้อมูลในหน้า 'แบบฟอร์มบันทึกสุขภาพ'")
    

