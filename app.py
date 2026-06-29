import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta
import random

# تنظیمات صفحه
st.set_page_config(
    page_title="داشبورد هوشمند پایتون",
    page_icon="🐍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# استایل سفارشی
st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 30px;
    }
    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
    }
    .metric-value {
        font-size: 36px;
        font-weight: bold;
        color: #667eea;
    }
    </style>
""", unsafe_allow_html=True)

# هدر
st.markdown('<div class="main-header"><h1>📊 داشبورد مدیریت داده</h1><p>تحلیل داده با پایتون و Streamlit</p></div>', unsafe_allow_html=True)

# سایدبار
with st.sidebar:
    st.image("https://www.python.org/static/img/python-logo.png", width=150)
    st.title("⚙️ تنظیمات")
    
    # انتخاب نوع داده
    data_type = st.selectbox(
        "نوع داده:",
        ["تصادفی", "فروش", "کاربران", "محصولات"]
    )
    
    # تعداد رکوردها
    num_records = st.slider(
        "تعداد رکوردها:",
        min_value=10,
        max_value=1000,
        value=100,
        step=10
    )
    
    # تاریخ شروع
    start_date = st.date_input(
        "تاریخ شروع:",
        datetime.now() - timedelta(days=30)
    )
    
    st.divider()
    st.caption("ساخته شده با ❤️ و پایتون")
    st.caption(f"ورژن: 1.0.0")

# تولید داده‌های تصادفی
@st.cache_data(ttl=300)
def generate_data(data_type, num_records, start_date):
    np.random.seed(42)
    
    dates = [start_date + timedelta(days=i) for i in range(num_records)]
    
    if data_type == "تصادفی":
        data = {
            'تاریخ': dates,
            'مقدار': np.random.randint(10, 1000, num_records),
            'دسته': np.random.choice(['A', 'B', 'C', 'D'], num_records),
            'وضعیت': np.random.choice(['فعال', 'غیرفعال', 'در انتظار'], num_records, p=[0.6, 0.2, 0.2])
        }
    elif data_type == "فروش":
        data = {
            'تاریخ': dates,
            'مقدار': np.random.normal(500, 150, num_records).astype(int),
            'محصول': np.random.choice(['محصول ۱', 'محصول ۲', 'محصول ۳', 'محصول ۴'], num_records),
            'منطقه': np.random.choice(['تهران', 'اصفهان', 'شیراز', 'مشهد'], num_records)
        }
    elif data_type == "کاربران":
        data = {
            'تاریخ': dates,
            'مقدار': np.random.randint(50, 500, num_records),
            'منبع': np.random.choice(['گوشی', 'کامپیوتر', 'تبلت'], num_records),
            'جنسیت': np.random.choice(['مرد', 'زن'], num_records)
        }
    else:  # محصولات
        data = {
            'تاریخ': dates,
            'مقدار': np.random.randint(1, 100, num_records),
            'دسته‌بندی': np.random.choice(['الکترونیک', 'پوشاک', 'کتاب', 'غذا'], num_records),
            'فروشنده': np.random.choice(['فروشنده A', 'فروشنده B', 'فروشنده C'], num_records)
        }
    
    return pd.DataFrame(data)

# تولید داده
df = generate_data(data_type, num_records, start_date)

# متریک‌های اصلی
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
        <div class="metric-card">
            <span style="font-size: 14px; color: #666;">تعداد کل</span>
            <div class="metric-value">{:,}</div>
        </div>
    """.format(len(df)), unsafe_allow_html=True)

with col2:
    avg_value = df['مقدار'].mean()
    st.markdown("""
        <div class="metric-card">
            <span style="font-size: 14px; color: #666;">میانگین مقدار</span>
            <div class="metric-value">{:,.0f}</div>
        </div>
    """.format(avg_value), unsafe_allow_html=True)

with col3:
    max_value = df['مقدار'].max()
    st.markdown("""
        <div class="metric-card">
            <span style="font-size: 14px; color: #666;">حداکثر مقدار</span>
            <div class="metric-value">{:,}</div>
        </div>
    """.format(max_value), unsafe_allow_html=True)

with col4:
    min_value = df['مقدار'].min()
    st.markdown("""
        <div class="metric-card">
            <span style="font-size: 14px; color: #666;">حداقل مقدار</span>
            <div class="metric-value">{:,}</div>
        </div>
    """.format(min_value), unsafe_allow_html=True)

# نمودارها
st.divider()
st.subheader("📈 تحلیل داده‌ها")

tab1, tab2, tab3, tab4 = st.tabs(["📊 نمودار خطی", "📊 نمودار میله‌ای", "📊 توزیع", "📋 داده‌ها"])

with tab1:
    fig_line = px.line(
        df, 
        x='تاریخ', 
        y='مقدار',
        title='روند تغییرات مقدار',
        template='plotly_white'
    )
    fig_line.update_layout(height=400)
    st.plotly_chart(fig_line, use_container_width=True)

with tab2:
    if len(df.columns) >= 3:
        col1, col2 = st.columns(2)
        with col1:
            # ستون‌های دسته‌بندی را پیدا کن
            categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
            if categorical_cols:
                selected_col = st.selectbox("انتخاب ستون دسته‌بندی:", categorical_cols)
                fig_bar = px.bar(
                    df.groupby(selected_col)['مقدار'].mean().reset_index(),
                    x=selected_col,
                    y='مقدار',
                    title=f'میانگین مقدار بر اساس {selected_col}',
                    template='plotly_white',
                    color=selected_col
                )
                st.plotly_chart(fig_bar, use_container_width=True)
        
        with col2:
            if categorical_cols:
                fig_pie = px.pie(
                    df,
                    names=categorical_cols[0],
                    title=f'توزیع {categorical_cols[0]}',
                    template='plotly_white'
                )
                st.plotly_chart(fig_pie, use_container_width=True)

with tab3:
    fig_hist = px.histogram(
        df,
        x='مقدار',
        nbins=30,
        title='توزیع مقدارها',
        template='plotly_white'
    )
    fig_hist.update_layout(height=400)
    st.plotly_chart(fig_hist, use_container_width=True)

with tab4:
    st.dataframe(
        df,
        use_container_width=True,
        height=400,
        column_config={
            "تاریخ": st.column_config.DateColumn("تاریخ"),
            "مقدار": st.column_config.NumberColumn("مقدار", format="%d"),
        }
    )
    
    # دکمه دانلود
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 دانلود CSV",
        data=csv,
        file_name=f"data_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )

# بخش تحلیل آماری
st.divider()
st.subheader("🔍 تحلیل آماری پیشرفته")

col1, col2 = st.columns([2, 1])

with col1:
    st.write("### آمار توصیفی")
    st.dataframe(
        df.describe(),
        use_container_width=True
    )

with col2:
    st.write("### اطلاعات ستون‌ها")
    info_df = pd.DataFrame({
        'ستون': df.columns,
        'نوع داده': df.dtypes.values,
        'تعداد نال': df.isnull().sum().values,
        'تعداد یکتا': df.nunique().values
    })
    st.dataframe(info_df, use_container_width=True)

# بخش پیش‌بینی ساده
st.divider()
st.subheader("🤖 پیش‌بینی ساده")

with st.expander("پیش‌بینی مقدار آینده"):
    st.write("""
    این بخش از یک مدل رگرسیون خطی ساده برای پیش‌بینی مقدار آینده استفاده می‌کند.
    """)
    
    from sklearn.linear_model import LinearRegression
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import mean_squared_error, r2_score
    
    # آماده‌سازی داده
    df['day_num'] = (df['تاریخ'] - df['تاریخ'].min()).dt.days
    
    X = df[['day_num']].values
    y = df['مقدار'].values
    
    # تقسیم داده
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # آموزش مدل
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    # پیش‌بینی
    y_pred = model.predict(X_test)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("R² Score", f"{r2_score(y_test, y_pred):.2%}")
    with col2:
        st.metric("RMSE", f"{np.sqrt(mean_squared_error(y_test, y_pred)):.2f}")
    with col3:
        # پیش‌بینی روز بعد
        next_day = df['day_num'].max() + 1
        next_pred = model.predict([[next_day]])[0]
        st.metric("پیش‌بینی روز آینده", f"{next_pred:.0f}")
    
    # نمودار پیش‌بینی
    fig_pred = px.scatter(
        x=df['تاریخ'], 
        y=df['مقدار'],
        title='داده‌ها و خط رگرسیون',
        template='plotly_white',
        labels={'x': 'تاریخ', 'y': 'مقدار'}
    )
    
    # اضافه کردن خط رگرسیون
    x_range = np.array([df['day_num'].min(), df['day_num'].max()]).reshape(-1, 1)
    y_range = model.predict(x_range)
    fig_pred.add_scatter(
        x=df['تاریخ'].iloc[[0, -1]],
        y=y_range,
        mode='lines',
        name='رگرسیون',
        line=dict(color='red', width=2)
    )
    
    fig_pred.update_layout(height=400)
    st.plotly_chart(fig_pred, use_container_width=True)

# فوتر
st.divider()
st.markdown("""
    <div style="text-align: center; color: #666; padding: 20px;">
        <p>🚀 ساخته شده با Streamlit &nbsp;|&nbsp; 🐍 پایتون &nbsp;|&nbsp; 📊 Plotly</p>
        <p style="font-size: 12px;">آخرین بروزرسانی: {}</p>
    </div>
""".format(datetime.now().strftime("%Y-%m-%d %H:%M")), unsafe_allow_html=True)
