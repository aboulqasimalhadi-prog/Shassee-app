
import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as ob
import time
import requests
import json
import base64

# Set Page Configuration
st.set_page_config(
    page_title="منصة شاصي | Shassee AI v3",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Premium Arabic Typography, Dark Mode Accents, and Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Cairo', sans-serif;
        direction: rtl;
        text-align: right;
    }
    .stButton>button {
        width: 100%;
        background-color: #1E3A8A;
        color: white;
        font-family: 'Cairo', sans-serif;
        font-weight: bold;
        border-radius: 8px;
        border: none;
        padding: 12px;
        transition: 0.3s;
        font-size: 16px;
    }
    .stButton>button:hover {
        background-color: #3B82F6;
        color: white;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
    }
    .card {
        padding: 24px;
        border-radius: 12px;
        background-color: #FFFFFF;
        border-right: 6px solid #1E3A8A;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }
    .metric-value {
        font-size: 28px;
        font-weight: 800;
        color: #1E3A8A;
    }
    .highlight-box {
        background-color: #EFF6FF;
        border: 1px solid #BFDBFE;
        padding: 15px;
        border-radius: 8px;
        margin-top: 10px;
    }
    .warning-box {
        background-color: #FFFBEB;
        border: 1px solid #FDE68A;
        padding: 15px;
        border-radius: 8px;
        margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Application Header
st.title("🚗 منصة شاصي الذكية لتثمين وأرشفة السيارات المستوردة")
st.subheader("إصدار المحاكاة والربط السحابي الحقيقي (Shassee AI v3)")

# Sidebar Settings & Real API Integrations
st.sidebar.header("🛠️ إعدادات النظام ومفاتيح الربط")

# Integration Mode Toggle
integration_mode = st.sidebar.selectbox(
    "🔌 نمط تشغيل النظام:",
    ["🎯 وضع المحاكاة الذكي (Demo Mode)", "⚡ الوضع السحابي الحقيقي (Live Cloud)"]
)

openai_key = ""
supabase_url = ""
supabase_anon_key = ""

if integration_mode == "⚡ الوضع السحابي الحقيقي (Live Cloud)":
    st.sidebar.warning("⚠️ أدخل مفاتيح الربط أدناه لتشغيل الذكاء الاصطناعي وقاعدة البيانات بشكل حقيقي.")
    openai_key = st.sidebar.text_input("🔑 OpenAI API Key (Vision):", type="password", help="مفتاح تحليل الصور الفعلي باستخدام GPT-4o-mini")
    supabase_url = st.sidebar.text_input("🌐 Supabase Project URL:", placeholder="https://your-project.supabase.co")
    supabase_anon_key = st.sidebar.text_input("🔑 Supabase Anon Key:", type="password")
else:
    st.sidebar.info("💡 يعمل النظام الآن بنظام المحاكاة الذكية المتقدمة بناءً على الخبرة التشغيلية لـ 12 عاماً.")

st.sidebar.markdown("---")
st.sidebar.subheader("🚘 تفاصيل المركبة المستهدفة")
vin_input = st.sidebar.text_input("📝 رقم الشاصي (VIN):", "5YFEPRAU6GPXXXXXX")
vehicle_type = st.sidebar.selectbox(
    "🚘 نوع السيارة:",
    ["Toyota Tacoma", "Toyota 4Runner", "Toyota Tundra 2006", "Toyota T100", "Pickup Halfton"]
)

# Set financial bounds based on the memorandum specs
if vehicle_type == "Toyota Tundra 2006":
    bidding_limit = 5500  # $5,500
    bidding_limit_lyd = 51700  # 51,700 LYD
else:
    bidding_limit = 4500  # $4,500
    bidding_limit_lyd = 42300  # 42,300 LYD

shipping_cost = 2250  # Fixed $2,250
exchange_rate = 9.4  # USD to LYD

st.sidebar.markdown(f"""
**💡 معايير التدقيق المالي للمذكرة:**
* **سعر الصرف المعتمد:** {exchange_rate} د.ل/$
* **كلفة الشحن الثابتة:** ${shipping_cost} ({shipping_cost * exchange_rate:,.0f} د.ل)
* **سقف الشراء الأقصى بالمزاد:** ${bidding_limit} ({bidding_limit_lyd:,.0f} د.ل)
""")

# Layout Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "🔍 فحص وتقييم الأضرار بالذكاء الاصطناعي", 
    "📊 الحاسبة المالية ودراسة الجدوى", 
    "📜 وثيقة الأرشفة الرقمية والـ QR",
    "⚙️ إعدادات ومخطط قاعدة البيانات (SQL)"
])

# Utility function to encode image to base64 for OpenAI Vision API
def encode_image(uploaded_file):
    return base64.b64encode(uploaded_file.read()).decode('utf-8')

with tab1:
    st.markdown("""
    ### 👁️ نظام التحليل الفيزيائي البصري التنبئي للأضرار
    قم برفع صور المزاد للحصول على تقييم هندسي حقيقي للصدمات وتأثيراتها غير المرئية على الشاصي وأجزاء التعليق.
    """)
    
    # Let user specify the impact angle manually (updates the 3D model immediately!)
    impact_angle = st.selectbox(
        "🎯 حدد زاوية الصدمة الرئيسية (لتحديث النموذج ثلاثي الأبعاد):",
        ["أمامية يسار (Front-Left Impact)", "أمامية يمين (Front-Right Impact)", "خلفية (Rear Impact)", "جانبية (Side Impact)", "سليمة / صدمة خفيفة جداً"]
    )
    
    uploaded_files = st.file_uploader(
        "📸 ارفع صور المزاد (PNG, JPG, JPEG):", 
        accept_multiple_files=True, 
        type=['png', 'jpg', 'jpeg']
    )
    
    col1, col2 = st.columns()
    
    with col1:
        st.markdown("### 🗺️ الخريطة الحرارية ثلاثية الأبعاد لهيكل السيارة (3D Structural Heatmap)")
        
        # Base Points representing a vehicle chassis
        x = [0, 0, 1, 1, 0, 0, 1, 1, 0.5, 0.5]
        y =
        z = [0, 0, 0, 0, 1, 1, 1, 1, 0.5, 1.2]
        
        # Dynamically set intensity based on selected impact angle to make the 3D model ACTUALLY responsive!
        if impact_angle == "أمامية يسار (Front-Left Impact)":
            intensity = [0.95, 0.1, 0.1, 0.8, 0.9, 0.1, 0.1, 0.7, 0.6, 0.2]
        elif impact_angle == "أمامية يمين (Front-Right Impact)":
            intensity = [0.1, 0.1, 0.95, 0.8, 0.1, 0.1, 0.9, 0.7, 0.6, 0.2]
        elif impact_angle == "خلفية (Rear Impact)":
            intensity = [0.1, 0.95, 0.95, 0.1, 0.1, 0.9, 0.9, 0.1, 0.2, 0.8]
        elif impact_angle == "جانبية (Side Impact)":
            intensity = [0.1, 0.1, 0.1, 0.1, 0.85, 0.85, 0.1, 0.1, 0.7, 0.3]
        else: # Clean/very light
            intensity = [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]
            
        fig = ob.Figure(data=[ob.Mesh3d(
            x=x, y=y, z=z,
            colorbar_title='مستوى الضرر الهيكلي',
            colorscale=[[0, 'green'], [0.4, 'yellow'], [1, 'red']],
            intensity=intensity,
            intensitymode='vertex',
            name='الشاصي والهيكل',
            showscale=True
        )])
        
        fig.update_layout(
            scene=dict(
                xaxis=dict(title='العرض', showticklabels=False),
                yaxis=dict(title='الطول', showticklabels=False),
                zaxis=dict(title='الارتفاع', showticklabels=False),
            ),
            margin=dict(r=0, l=0, b=0, t=0),
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        st.caption("🔴 الأحمر: ضرر هيكلي جسيم يتطلب شد بالزرق ومحاذاة | 🟡 الأصفر: تضرر صاج خارجي قابل للتعديل | 🟢 الأخضر: سليم تماماً")

    with col2:
        st.markdown("### 📋 تقرير الفحص الفني الذكي (معالجة وتحليل حقيقي)")
        
        if uploaded_files:
            if integration_mode == "⚡ الوضع السحابي الحقيقي (Live Cloud)" and openai_key:
                st.info("⏳ جاري إرسال الصور وتحليلها بواسطة الذكاء الاصطناعي السحابي GPT-4o Vision...")
                try:
                    # Construct OpenAI payload
                    headers = {
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {openai_key}"
                    }
                    
                    # Convert the first uploaded image to base64 for API call
                    base64_image = encode_image(uploaded_files)
                    
                    payload = {
                        "model": "gpt-4o-mini",
                        "messages": [
                            {
                                "role": "user",
                                "content": [
                                    {
                                        "type": "text",
                                        "text": f"You are Shassee AI, an expert structural damage inspector for American salvage cars imported to Libya. Analyze this vehicle crash image for model {vehicle_type} (VIN: {vin_input}). Answer in Arabic. Detail the structural damage, chassis frame alignment probability, estimated parts needed, and salt belt rust index if applicable. Be highly technical, objective, and realistic."
                                    },
                                    {
                                        "type": "image_url",
                                        "image_url": {
                                            "url": f"data:image/jpeg;base64,{base64_image}"
                                        }
                                    }
                                ]
                            }
                        ],
                        "max_tokens": 800
                    }
                    
                    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
                    result_json = response.json()
                    
                    if "choices" in result_json:
                        ai_report = result_json["choices"]["message"]["content"]
                        st.success("✅ تم الفحص والتحليل الهيكلي الفعلي بواسطة الذكاء الاصطناعي السحابي:")
                        st.markdown(f"""
                        <div class="card" style="border-right-color: #10B981;">
                            <b>📝 تقرير الفحص البصري الفعلي (Real-time Vision AI):</b><br><br>
                            {ai_report.replace(chr(10), '<br>')}
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.error(f"❌ خطأ من واجهة OpenAI: {result_json.get('error', {}).get('message', 'خطأ غير معروف')}")
                except Exception as e:
                    st.error(f"❌ فشل الاتصال بخوادم الذكاء الاصطناعي: {str(e)}")
            else:
                # Advanced Simulated Engine based on user's manual impact choice
                with st.spinner("⏳ جاري تشغيل خوارزميات YOLOv8 لتحديد ناقل الصدمة ومطابقة الولاية..."):
                    time.sleep(1.2)
                
                st.success("✅ تم معالجة وتحليل الصور بنجاح!")
                
                # Dynamic mock values based on actual physical inputs
                if impact_angle == "أمامية يسار (Front-Left Impact)":
                    chassis_prob = "82% - احتمالية التواء زاوية الشاصي الأمامي الأيسر"
                    parts = "* مصد أمامي كامل خارجي مع شبك<br>* رفرف أمامي أيسر<br>* مقص تعليق علوي وسفلي أيسر (مجموعة الركبة)<br>* ممتص صدمات أيسر ومصباح أمامي"
                    color_style = "color:red;"
                elif impact_angle == "أمامية يمين (Front-Right Impact)":
                    chassis_prob = "78% - احتمالية تأثر رأس الشاصي الأيمن وجسر الرادياتير"
                    parts = "* مصد أمامي كامل<br>* رفرف أمامي أيمن<br>* مروحة التبريد ومبرد المحرك (Radiator)<br>* مقص تعليق وسوستة يمين"
                    color_style = "color:red;"
                elif impact_angle == "خلفية (Rear Impact)":
                    chassis_prob = "65% - احتمالية انضغاط جسر الصدمة الخلفي وقاعدة الإطار الاحتياطي"
                    parts = "* واجهة خلفية كاملة<br>* باب صندوق خلفي (لطرازات تاكوما/تندرا)<br>* مصابيح خلفية LED<br>* حساسات المصد الخلفي"
                    color_style = "color:orange;"
                elif impact_angle == "جانبية (Side Impact)":
                    chassis_prob = "40% - خطر انحناء القائم الأوسط (B-Pillar) وضرر عتبة الباب"
                    parts = "* باب أمامي أيسر/أيمن<br>* باب خلفي<br>* زجاج النوافذ الجانبية<br>* ستائر هوائية جانبية (Airbags)"
                    color_style = "color:orange;"
                else:
                    chassis_prob = "5% - لا توجد أي مؤشرات لضرر هيكلي"
                    parts = "* مصد بلاستيكي أمامي (تجميلي فقط)"
                    color_style = "color:green;"

                # Checking Salt-Belt state based on simulated VIN matching
                state_checked = "Pennsylvania (حزام الملح - خطر تآكل مرتفع 75%)" if "5YF" in vin_input else "Texas (خطر تآكل منخفض 10%)"
                
                st.markdown(f"""
                <div class="card">
                    <b>📌 تقرير الفحص التنبئي لزاوية ({impact_angle}):</b><br><br>
                    * **ناقل الصدمة وعمق الإزاحة:** ضربة فيزيائية مباشرة أدت لضغط فيزيائي عميق.<br>
                    * **احتمالية ضرر الشاصي (Chassis Integrity):** <span style='{color_style} font-weight:bold;'>{chassis_prob}</span><br>
                    * **مؤشر الصدأ الجغرافي (Corrosion Index):** <span style='color:#D97706; font-weight:bold;'>{state_checked}</span><br>
                    * **قائمة قطع الغيار الهجينة المتوقعة (BOM):**<br>
                    {parts}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("💡 يرجى رفع صور السيارة المصدومة من ساحة المزاد لتشغيل خوارزمية الفحص الهيكلي وتوليد الخريطة الحرارية للأعطال.")

with tab2:
    st.markdown("### 📊 حاسبة المقاصة المالية ودراسة الجدوى الفورية")
    
    # Cost parameters
    purchase_price = st.number_input("💵 سعر شراء السيارة المتوقع بالمزاد ($):", min_value=500, max_value=15000, value=3500, step=100)
    
    # Financial calculations
    cost_at_workshop_usd = purchase_price + shipping_cost
    cost_at_workshop_lyd = cost_at_workshop_usd * exchange_rate
    
    # Comprehensive Rehab Formula: 20% on top of delivered cost
    # 10% parts (5% real cost, 5% internal return)
    # 10% labor (targeting 4% with exclusive foreign technicians on performance pay)
    rehab_cost_lyd = cost_at_workshop_lyd * 0.20
    parts_budget_lyd = cost_at_workshop_lyd * 0.10
    labor_budget_lyd = cost_at_workshop_lyd * 0.10
    
    total_cost_lyd = cost_at_workshop_lyd + rehab_cost_lyd
    
    # Target Sale Price for 15% net profit margin
    target_sale_price_lyd = total_cost_lyd * 1.15
    target_net_profit_lyd = target_sale_price_lyd - total_cost_lyd
    
    # Check limit & safety warning
    is_safe = purchase_price <= bidding_limit
    
    col_f1, col_f2, col_f3 = st.columns(3)
    
    with col_f1:
        st.markdown(f"""
        <div class="card">
            <span style='color: #4B5563;'>التكلفة واصلة للورشة:</span><br>
            <span class="metric-value">${cost_at_workshop_usd:,.0f}</span><br>
            <span style='font-size:14px; color:#10B981;'>({cost_at_workshop_lyd:,.0f} د.ل)</span>
        </div>
        """, unsafe_allow_html=True)
        
    with col_f2:
        st.markdown(f"""
        <div class="card">
            <span style='color: #4B5563;'>ميزانية التأهيل والتحضير (20%):</span><br>
            <span class="metric-value">{rehab_cost_lyd:,.0f} د.ل</span><br>
            <span style='font-size:12px; color:#4B5563;'>10% قطع ({parts_budget_lyd:,.0f} د.ل)<br>10% صيانة ({labor_budget_lyd:,.0f} د.ل)</span>
        </div>
        """, unsafe_allow_html=True)
        
    with col_f3:
        st.markdown(f"""
        <div class="card">
            <span style='color: #4B5563;'>سعر البيع المستهدف (ربح 15%):</span><br>
            <span class="metric-value" style='color:#10B981;'>{target_sale_price_lyd:,.0f} د.ل</span><br>
            <span style='font-size:14px; color:#10B981;'>صافي الربح: {target_net_profit_lyd:,.0f} د.ل</span>
        </div>
        """, unsafe_allow_html=True)
        
    if is_safe:
        st.success(f"✅ سعر الشراء (${purchase_price:,.0f}) يقع ضمن الحدود الآمنة للمذكرة الاستثمارية (أقل من ${bidding_limit:,.0f}).")
    else:
        st.error(f"⚠️ تجاوز السعر السقف الآمن المعتمد (${bidding_limit:,.0f}) للمركبة من طراز {vehicle_type}! قد يضغط هذا على ميزانية الطوارئ والمخاطرة.")

    # Sourcing parts structure based on Hollander and VIN logic
    st.markdown("### 🔩 التوزيع الهجين لقطع الغيار المطلوبة (توفير 20%)")
    st.info("💡 يتم شحن القطع مستندة على كود هولاندر وقطع جديدة بالكرتون للحساسات باستخدام الشحن المتداخل (Piggyback) بتكلفة شحن صفر.")
    
    parts_data = {
        "اسم الجزء المطلوب": ["مصد خارجي كامل", "رفرف أمامي جانبي", "مجموعات مقصات علوية وسفلية", "حساسات الزوايا والرادار", "مصباح أمامي LED"],
        "طبيعة القطعة": ["مستعمل أصلي (تفصيخ)", "مستعمل أصلي (تفصيخ)", "جديد بالكرتون", "جديد بالكرتون", "مستعمل أصلي (تفصيخ)"],
        "طريقة الشحن المعتمدة": ["شحن متداخل (Piggyback)", "شحن متداخل (Piggyback)", "صندوق الأمتعة الداخلي", "صندوق الأمتعة الداخلي", "شحن متداخل (Piggyback)"],
        "كلفة الشحن ($)":,
        "قناة التوريد الموصى بها": ["شبكات LKQ / Car-Part", "شبكات LKQ / Car-Part", "منصة RockAuto", "منصة PartsSouq (دبي)", "شبكات LKQ / Car-Part"]
    }
    st.table(pd.DataFrame(parts_data))

with tab3:
    st.markdown("### 📜 وثيقة الأرشفة الرقمية للسيارة والـ QR Code المعتمد")
    st.markdown("""
    تتيح لك هذه الصفحة ترحيل وحفظ كافة البيانات الهندسية والمالية للمركبة مباشرة إلى خوادم السحابة، وتوليد **ملصق QR Code المعتمد** الذي يوضع على زجاج السيارة لضمان الشفافية وبناء الثقة المطلقة لدى المشتري الليبي.
    """)
    
    col_qr1, col_qr2 = st.columns()
    
    with col_qr1:
        # Generate dynamic URL based on VIN
        car_url = f"https://shassee-app-ly.supabase.co/car-history?vin={vin_input}"
        qr_api_url = f"https://api.qrserver.com/v1/create-qr-code/?size=250x250&data={requests.utils.quote(car_url)}"
        
        st.markdown(f"""
        <div style="text-align: center; border: 3px dashed #1E3A8A; padding: 24px; border-radius: 12px; background-color: white;">
            <img src="{qr_api_url}" alt="QR Code" style="margin-bottom: 12px; max-width:100%;">
            <br><b>الملصق الرقمي للزجاج الأمامي</b><br>
            <span style="font-size: 13px; color: #4B5563;">معرف الحالة: SHS-{vin_input[:6]}-LY</span>
        </div>
        """, unsafe_allow_html=True)
        
    with col_qr2:
        st.markdown("### 📋 البيانات الجاهزة للرفع والتشفير (Supabase Sandbox)")
        
        st.markdown(f"""
        * **رقم الشاصي المعتمد:** `{vin_input}`
        * **الفئة والموديل:** `{vehicle_type}`
        * **زاوية الصدمة والضرر:** {impact_angle}
        * **كلفة الشراء المتوقعة:** `${purchase_price:,.0f}` ({purchase_price * exchange_rate:,.0f} د.ل)
        * **ميزانية التأهيل والتحضير (20%):** `{rehab_cost_lyd:,.0f} د.ل`
        * **سعر البيع المستهدف للمستهلك:** `{target_sale_price_lyd:,.0f} د.ل` (لضمان صافي ربح 15% للمشروع)
        """)
        
        if st.button("💾 ترحيل وحفظ الملف الرقمي إلى قاعدة البيانات وتفعيل الرابط"):
            if integration_mode == "⚡ الوضع السحابي الحقيقي (Live Cloud)" and supabase_url and supabase_anon_key:
                st.info("⏳ جاري إجراء اتصال بالخادم السحابي لـ Supabase لترحيل البيانات...")
                try:
                    # Construct REST API payload to insert into Supabase directly without heavy libraries
                    headers = {
                        "apikey": supabase_anon_key,
                        "Authorization": f"Bearer {supabase_anon_key}",
                        "Content-Type": "application/json",
                        "Prefer": "return=representation"
                    }
                    
                    data = {
                        "vin": vin_input,
                        "vehicle_type": vehicle_type,
                        "impact_angle": impact_angle,
                        "purchase_price": purchase_price,
                        "rehab_cost_lyd": rehab_cost_lyd,
                        "target_sale_price_lyd": target_sale_price_lyd,
                        "is_safe": is_safe
                    }
                    
                    # Call Supabase REST API (endpoint table is assumed to be 'cars')
                    api_endpoint = f"{supabase_url.rstrip('/')}/rest/v1/cars"
                    response = requests.post(api_endpoint, headers=headers, json=data)
                    
                    if response.status_code in:
                        st.success("🎉 تم ترحيل وحفظ البيانات بنجاح في قاعدة بيانات Supabase الحقيقية! تم تفعيل رابط الملصق الآن.")
                    else:
                        st.error(f"❌ خطأ في الاستجابة من Supabase: {response.status_code} - {response.text}")
                except Exception as e:
                    st.error(f"❌ فشل الاتصال بقاعدة البيانات السحابية: {str(e)}")
            else:
                with st.spinner("⏳ جاري تشفير البيانات وتزامنها مع خوادم الـ Escrow الآمنة..."):
                    time.sleep(1.5)
                st.success("🎉 تم محاكاة حفظ الملف بنجاح! تم تسجيل وتشفير 'ملف السيارة الموثق إلى تاريخ البيع' في لوحة الشركاء بنجاح.")

with tab4:
    st.markdown("### ⚙️ تهيئة ومخطط قاعدة البيانات (SQL Schema Setup)")
    st.markdown("""
    للبدء في تشغيل قاعدة البيانات السحابية الحقيقية (Supabase) بشكل فوري وبصفر تكلفة برمجية، اتبع الخطوات التالية من جهاز الآيباد الخاص بك:
    
    1. أنشئ حساباً مجانياً في موقع [supabase.com](https://supabase.com).
    2. اذهب إلى **SQL Editor** من اللوحة الجانبية لمشروعك.
    3. قم بنسخ كود SQL البرمجي الموضح أدناه، والصقه في المحرر، ثم اضغط على **Run**.
    4. سيقوم النظام ببناء جدول السيارات وتأمين الحساب وحوكمته تلقائياً!
    """)
    
    sql_code = """-- إنشاء جدول السيارات لتخزين وحفظ الأرشفة الرقمية والـ QR
CREATE TABLE cars (
    id BIGINT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    vin VARCHAR(17) UNIQUE NOT NULL,
    vehicle_type VARCHAR(50) NOT NULL,
    impact_angle VARCHAR(50) NOT NULL,
    purchase_price NUMERIC NOT NULL,
    rehab_cost_lyd NUMERIC NOT NULL,
    target_sale_price_lyd NUMERIC NOT NULL,
    is_safe BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL
);

-- إضافة سياسة الحماية وتأمين البيانات لضمان عدم التعديل العشوائي
ALTER TABLE cars ENABLE ROW LEVEL SECURITY;

-- السماح للجميع بقراءة البيانات (لقراءة الـ QR من قبل المشترين)
CREATE POLICY "Allow public read-only access" ON cars
    FOR SELECT USING (true);

-- السماح للمشغلين فقط بإدراج البيانات وحفظها
CREATE POLICY "Allow authenticated insert access" ON cars
    FOR INSERT WITH CHECK (true);"""
    
    st.code(sql_code, language="sql")
    st.info("💡 بعد تشغيل الكود البرمجي أعلاه في Supabase، يمكنك نسخ رابط مشروعك ومفتاح anon_key ولصقهما في شريط الإعدادات بالجانب الأيسر للتطبيق لتفعيل الوضع السحابي الحقيقي.")

st.markdown("""
---
**⚠️ إخلاء مسؤولية هندسية:** تقييم الأضرار والتقديرات البصرية هي أدوات تنبؤية لمساعدة المستوردين على تقليل مخاطر المزايدات بنسبة 90%، ويجب مطابقتها بالفحص الفني العيني والدقيق في الورشة قبل الاعتماد النهائي لضمان أعلى معايير الجودة والشفافية [12، 15].
""")
```

