import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as ob
import time

# Set Page Configuration
st.set_page_config(
    page_title="منصة شاصي | Shassee AI",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Premium Arabic Typography and Styling
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
        padding: 10px;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #3B82F6;
        color: white;
    }
    .card {
        padding: 20px;
        border-radius: 10px;
        background-color: #F3F4F6;
        border-right: 5px solid #1E3A8A;
        margin-bottom: 15px;
    }
    .metric-value {
        font-size: 24px;
        font-weight: bold;
        color: #1E3A8A;
    }
</style>
""", unsafe_allow_html=True)

# Application Header
st.title("🚗 منصة شاصي الذكية لتثمين وأرشفة السيارات المستوردة")
st.subheader("النسخة التشغيلية الأولية (MVP) - بروتوكول الهندسة التنبؤية والتسعير العيني")

# Sidebar - Settings & Inputs
st.sidebar.header("🛠️ إعدادات النظام والمدخلات")

vin_input = st.sidebar.text_input("📝 أدخل رقم الشاصي (VIN):", "5YFEPRAU6GPXXXXXX")
vehicle_type = st.sidebar.selectbox(
    "🚘 نوع السيارة المستهدفة:",
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
---
**💡 معايير التدقيق المالي للمذكرة:**
* **سعر الصرف:** {exchange_rate} د.ل/$
* **كلفة الشحن الثابتة:** ${shipping_cost} ({shipping_cost * exchange_rate:,.0f} د.ل)
* **سقف الشراء الأقصى:** ${bidding_limit} ({bidding_limit_lyd:,.0f} د.ل)
""")

# Layout Tabs
tab1, tab2, tab3 = st.tabs(["🔍 فحص وتقييم الأضرار بالذكاء الاصطناعي", "📊 الحاسبة المالية ودراسة الجدوى", "📜 مستند الأرشفة الرقمية (QR Code)"])

with tab1:
    st.markdown("""
    ### 👁️ نظام التحليل الفيزيائي البصري التنبئي للأضرار
    قم برفع صور المزاد الحالية للسيارة المصدومة، وسيقوم المحرك الذكي بتحليل هندسة الصدمة وتوقع التلفيات غير المرئية في الشاصي والقطع الداخلية.
    """)
    
    uploaded_files = st.file_uploader("📸 ارفع صور المزاد (10-15 صورة للحصول على أفضل دقة):", accept_multiple_files=True, type=['png', 'jpg', 'jpeg'])
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 🗺️ الخريطة الحرارية ثلاثية الأبعاد لهيكل السيارة (3D Heatmap)")
        
        # Plotting a simulated 3D mesh chassis to show AI structural damage detection
        # Define 3D points representing a simplified vehicle chassis
        x = [0, 0, 1, 1, 0, 0, 1, 1, 0.5, 0.5]
        y = [0, 4, 4, 0, 0, 4, 4, 0, 0, 4]
        z = [0, 0, 0, 0, 1, 1, 1, 1, 0.5, 1.2]
        
        # Color coding: red for damaged front, yellow for mid/sides, green for rear
        intensity = [0.9, 0.2, 0.1, 0.9, 0.8, 0.1, 0.1, 0.8, 0.5, 0.5] # Damage scale
        
        fig = ob.Figure(data=[ob.Mesh3d(
            x=x, y=y, z=z,
            colorbar_title='مستوى الضرر',
            colorscale=[[0, 'green'], [0.5, 'yellow'], [1, 'red']],
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
        st.caption("🔴 اللون الأحمر: ضرر هيكلي جسيم في الشاصي/المقدمة | 🟡 الأصفر: ضرر صاج خارجي | 🟢 الأخضر: سليم")

    with col2:
        st.markdown("### 📋 تقرير الفحص الفني الذكي (التخمين البصري والهندسي)")
        
        if uploaded_files:
            with st.spinner("⏳ جاري تشغيل خوارزمية YOLOv8 و Mask R-CNN لتحليل ناقل الصدمة..."):
                time.sleep(1.5)
            
            st.success("✅ تم تحليل الصور ومطابقتها هندسياً بنجاح!")
            
            # Simulated AI output based on actual engineering rules
            st.markdown(f"""
            <div class="card">
                <b>📌 تفاصيل الصدمة المرصودة:</b><br>
                * **زاوية الاصطدام الرئيسية (Collision Vector):** صدمة أمامية منحرفة بزاوية 30 درجة من الجهة اليسرى.<br>
                * **الأجزاء الخارجية المتضررة (Segmented Parts):** المصد الأمامي (تلف كلي)، الرفرف الأمامي الأيسر (تلف كلي)، غطاء المحرك (انبعاج متوسط).<br>
                * **الضرر الهيكلي المتوقع في الشاصي (Chassis Impact Prob):** <span style='color:red; font-weight:bold;'>82% احتمال التواء في زاوية رأس الشاصي الأيسر</span> (بسبب عمق الإزاحة البالغ 28 سم).<br>
                * **الصدأ والتآكل الجغرافي (Corrosion Index):** <span style='color:orange; font-weight:bold;'>متوسط (45%)</span> - تم تسجيل المركبة سابقاً في ولاية (Pennsylvania) الواقعة في حزام الملح (Salt Belt). ينصح بتنظيف قواعد المساعدين جيداً.
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("💡 قم برفع صور السيارة المصدومة لتشغيل محاكاة الكشف والخرائط الحرارية للأعطال.")

with tab2:
    st.markdown("### 📊 حاسبة المقاصة المالية وقائمة قطع الغيار الهجينة")
    
    # Financial Inputs
    purchase_price = st.number_input("💵 سعر شراء السيارة في المزاد ($):", min_value=500, max_value=15000, value=3500, step=100)
    
    # Mathematical computations matching the memorandum's exact equations
    cost_at_workshop_usd = purchase_price + shipping_cost
    cost_at_workshop_lyd = cost_at_workshop_usd * exchange_rate
    
    # Rehabilitation formula: 20% on top of delivered cost
    # 10% parts (5% real cost, 5% internal return)
    # 10% labor (targeting 4% with exclusive foreign technicians on performance pay)
    rehab_cost_lyd = cost_at_workshop_lyd * 0.20
    parts_budget_lyd = cost_at_workshop_lyd * 0.10
    labor_budget_lyd = cost_at_workshop_lyd * 0.10
    
    total_cost_lyd = cost_at_workshop_lyd + rehab_cost_lyd
    
    # Target Sale Price for 15% net profit margin
    target_sale_price_lyd = total_cost_lyd * 1.15
    target_net_profit_lyd = target_sale_price_lyd - total_cost_lyd
    
    # Verification check against bidding limit
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
        
    # Check limit & safety warning
    if is_safe:
        st.success(f"✅ سعر الشراء في المزاد ضمن الحدود الآمنة المعتمدة للمذكرة الاستثمارية (أقل من ${bidding_limit}).")
    else:
        st.error(f"⚠️ تحذير: سعر الشراء يتجاوز السقف الآمن المعتمد (${bidding_limit}). هامش الربح قد يتقلص أو يتأثر صندوق الطوارئ.")

    # Sourcing hybrid parts based on detected damage (Interactive List)
    st.markdown("### 🔩 قائمة قطع الغيار الهجينة المقترحة (تحقيق توفير 20%)")
    st.info("💡 تم تصنيف القطع آلياً بالاعتماد على كود هولاندر (Hollander Interchange) لقطع التفصيخ، وقطع جديدة بالكرتون للحساسات الميكانيكية.")
    
    parts_data = {
        "اسم القطعة": ["مصد أمامي كامل", "رفرف أمامي أيسر", "مجموعة مقصات تعليق", "حساسات المصد الأمامي", "مصباح أمامي أيسر LED"],
        "التصنيف": ["مستعمل أصلية (تفصيخ)", "مستعمل أصلية (تفصيخ)", "جديدة بالكرتون", "جديدة بالكرتون", "مستعمل أصلية (تفصيخ)"],
        "مصدر التوريد الموصى به": ["شبكة LKQ / Car-Part", "شبكة LKQ / Car-Part", "منصة RockAuto", "منصة PartsSouq", "شبكة LKQ / Car-Part"],
        "طريقة الشحن الموصى بها": ["شحن متداخل (Piggyback)", "شحن متداخل (Piggyback)", "شحن بالصندوق الداخلي", "شحن بالصندوق الداخلي", "شحن متداخل (Piggyback)"],
        "كلفة الشحن المقدرة ($)": [0, 0, 15, 5, 0],
        "الحالة الفنية المتوقعة": ["تطابق تام (رقم الهيكل VIN)", "تطابق تام (رقم الهيكل VIN)", "أصلي مطابقة برقم الجزء", "أصلي مطابقة برقم الجزء", "تطابق تام (رقم الهيكل VIN)"]
    }
    st.table(pd.DataFrame(parts_data))

with tab3:
    st.markdown("### 📜 وثيقة الأرشفة الرقمية للسيارة (QR Code Document)")
    st.markdown("""
    يقوم هذا القسم بإنشاء **"ملف السيارة الموثق إلى تاريخ البيع"** وحفظه على خوادم قاعدة البيانات (Supabase).
    هذا الملف يمثل جواز السفر الرقمي الدائم للسيارة، لكسر الركود في السوق الليبي وإثبات جودة تشطيب ورشتك ونظام الصيانة للزبون النهائي بكل شفافية.
    """)
    
    col_qr1, col_qr2 = st.columns([1, 2])
    
    with col_qr1:
        # Drawing a mock QR code layout
        st.markdown("""
        <div style="text-align: center; border: 2px dashed #1E3A8A; padding: 20px; border-radius: 10px; background-color: white;">
            <img src="https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=https://shassee-app-ly.supabase.co/car-history?vin=5YFEPRAU6GPXXXXXX" alt="QR Code" style="margin-bottom: 10px;">
            <br><b>الملصق المعتمد للزجاج الأمامي</b><br>
            <span style="font-size: 12px; color: #4B5563;">مسجل برقم: SHS-9482-LY</span>
        </div>
        """, unsafe_allow_html=True)
        
    with col_qr2:
        st.markdown("### 📋 البيانات المحفوظة في قاعدة البيانات (Supabase Dashboard):")
        st.markdown(f"""
        * **رقم الشاصي (VIN):** `{vin_input}`
        * **الموديل المعتمد فنيّاً:** `{vehicle_type}`
        * **حالة الصدمة عند الاستيراد:** موثقة بالكامل بصور المزاد وصور الميناء (ممنوع إخفاء الحوادث) [12، 15].
        * **القطع التي تم تبديلها وتأهيلها بالكامل:** (موضحة بنوع القطعة، جديدة أم تفصيخ أصلية، وموثقة برقم الفاتورة) [13].
        * **الفني المشرف على التأهيل والسمكرة:** (طاقم عمالتنا الأجنبية الحصرية لضمان جودة التشطيب الخارجي) [15، 19].
        * **قراءة العداد (Odometer):** موثقة ومطابقة لتقارير الجمارك لضمان عدم التلاعب.
        """)
        
        if st.button("💾 ترحيل وحفظ الملف الرقمي إلى قاعدة البيانات وتوليد الملصق"):
            with st.spinner("⏳ جاري تشفير البيانات وتزامنها مع قاعدة بيانات Supabase المشتركة..."):
                time.sleep(1.0)
            st.success("🎉 تم حفظ 'ملف السيارة الموثق' بنجاح! يمكن للوسيط والمستثمر الآن تتبع التفاصيل المالية والتشغيلية للحالة لحظياً.")

st.markdown("""
---
**⚠️ إخلاء مسؤولية فنية:** التحليلات والتقديرات البصرية هي أداة استرشادية مبنية على الذكاء التنبئي وتحليل إحصاءات الحوادث في أمريكا، ويجب مطابقتها دائماً بالفحص العيني الفني عند وصول السيارة لضمان الجودة المطلقة [12، 15].
""")
