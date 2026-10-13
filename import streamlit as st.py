import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------
# CẤU HÌNH TRANG
# -----------------------------
st.set_page_config(
    page_title='Quản lý điểm sinh viên',
    page_icon='📊',
    layout='wide'
)

# -----------------------------
# 1. TẠO DATAFRAME
# -----------------------------
students = {
    'Ho_ten': ['An', 'Bình', 'Chi', 'Dũng', 'Hà', 'Lan', 'Minh', 'Nam', 'Phúc', 'Trang'],
    'Chuyen_can': [9, 8, 7, 9, 8, 6, 10, 7, 8, 9],
    'Giua_ky': [8, 7.5, 6.5, 8.5, 7, 6, 9, 6.5, 7.5, 9],
    'Cuoi_ky': [8.5, 8, 6, 9, 7.5, 5.5, 9.5, 6.5, 7, 9]
}

df = pd.DataFrame(students)

# -----------------------------
# 2. TÍNH ĐIỂM TỔNG KẾT
# -----------------------------
df['Tong_ket'] = (
    0.2 * df['Chuyen_can'] +
    0.3 * df['Giua_ky'] +
    0.5 * df['Cuoi_ky']
).round(2)

# -----------------------------
# 3. XẾP LOẠI
# -----------------------------
def xep_loai(diem):
    if diem >= 8.5:
        return 'Giỏi'
    elif diem >= 7.0:
        return 'Khá'
    elif diem >= 5.0:
        return 'Trung bình'
    else:
        return 'Yếu'

df['Xep_loai'] = df['Tong_ket'].apply(xep_loai)

# -----------------------------
# 4. THỐNG KÊ
# -----------------------------
diem_tb = df['Tong_ket'].mean()
sv_max = df.loc[df['Tong_ket'].idxmax()]
sv_min = df.loc[df['Tong_ket'].idxmin()]
so_sv_dat = int((df['Tong_ket'] >= 5).sum())

# -----------------------------
# 5. GIAO DIỆN WEB APP
# -----------------------------
st.title('QUẢN LÝ ĐIỂM SINH VIÊN')
st.caption('Ứng dụng Python - Pandas - Matplotlib - Streamlit')

st.subheader('Bảng điểm của lớp')
display_df = df.rename(columns={
    'Ho_ten': 'Họ tên',
    'Chuyen_can': 'Chuyên cần',
    'Giua_ky': 'Giữa kỳ',
    'Cuoi_ky': 'Cuối kỳ',
    'Tong_ket': 'Tổng kết',
    'Xep_loai': 'Xếp loại'
})
st.dataframe(display_df, use_container_width=True, hide_index=True)

st.subheader('Thống kê')
col1, col2, col3, col4 = st.columns(4)
col1.metric('Điểm trung bình', f'{diem_tb:.2f}')
col2.metric('Cao nhất', f'{sv_max["Tong_ket"]:.2f}', sv_max['Ho_ten'])
col3.metric('Thấp nhất', f'{sv_min["Tong_ket"]:.2f}', sv_min['Ho_ten'])
col4.metric('Số sinh viên đạt', f'{so_sv_dat}/{len(df)}')

st.subheader('Xem chi tiết sinh viên')
selected_name = st.selectbox('Chọn sinh viên:', df['Ho_ten'].tolist())
selected = df[df['Ho_ten'] == selected_name].iloc[0]

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric('Chuyên cần', f'{selected["Chuyen_can"]:g}')
c2.metric('Giữa kỳ', f'{selected["Giua_ky"]:g}')
c3.metric('Cuối kỳ', f'{selected["Cuoi_ky"]:g}')
c4.metric('Tổng kết', f'{selected["Tong_ket"]:.2f}')c5.metric('Xếp loại', selected['Xep_loai'])

st.subheader('Biểu đồ điểm tổng kết')
fig, ax = plt.subplots(figsize=(10, 5))
ax.barh(df['Ho_ten'], df['Tong_ket'])
ax.set_xlabel('Điểm tổng kết')
ax.set_ylabel('Sinh viên')
ax.set_title('Điểm tổng kết của 10 sinh viên')
ax.set_xlim(0, 10)
ax.grid(axis='x', alpha=0.25)
plt.tight_layout()
st.pyplot(fig)

st.divider()
st.markdown(
    '<p style="font-size:13px; color:gray; text-align:center;">'
    'Người thực hiện: [HỌ TÊN] - MSSV: [MSSV]'
    '</p>',
    unsafe_allow_html=True
)