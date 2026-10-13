
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 1. Cấu hình trang
st.set_page_config(page_title="Quản lý điểm sinh viên",
    page_icon="🎓",
    layout="wide"
)

# 2. Giao diện CSS
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #e0f2fe, #f5f3ff, #ffffff);
}
h1 {
    color: #1d4ed8;
    text-align: center;
    font-size: 38px !important;
    font-weight: 800;
}
h2, h3 {
    color: #1e40af;
}
[data-testid="stMetric"] {
    background: white;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.12);
    border-left: 5px solid #3b82f6;
}
</style>
""", unsafe_allow_html=True)

# 3. Tiêu đề
st.title("🎓 QUẢN LÝ ĐIỂM SINH VIÊN")
st.caption("Hệ thống theo dõi kết quả học tập")

# 4. Tạo dữ liệu sinh viên
data = {
    "Họ tên": [
        "An", "Bình", "Chi", "Dũng", "Hà",
        "Lan", "Minh", "Nam", "Phúc", "Trang"
    ],
    "Chuyên cần": [9, 8, 7, 9, 8, 6, 10, 7, 8, 9],
    "Giữa kỳ": [8, 7.5, 6.5, 8.5, 7, 6, 9, 6.5, 7.5, 9],
    "Cuối kỳ": [8.5, 8, 6, 9, 7.5, 5.5, 9.5, 6.5, 7, 9]
}

df = pd.DataFrame(data)

# 5. Tính điểm tổng kết
df["Tổng kết"] = (
    df["Chuyên cần"] * 0.2
    + df["Giữa kỳ"] * 0.3
    + df["Cuối kỳ"] * 0.5
).round(2)

# 6. Xếp loại
def xep_loai(diem):
    if diem >= 8.5:
        return "Giỏi"
    elif diem >= 7:
        return "Khá"
    elif diem >= 5:
        return "Trung bình"
    return "Yếu"

df["Xếp loại"] = df["Tổng kết"].apply(xep_loai)

# 7. Thống kê
diem_tb = df["Tổng kết"].mean()
sv_cao_nhat = df.loc[df["Tổng kết"].idxmax()]
sv_thap_nhat = df.loc[df["Tổng kết"].idxmin()]
so_sv_dat = int((df["Tổng kết"] >= 5).sum())

# 8. Các thẻ thống kê
st.subheader("📊 Thống kê tổng quan")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Điểm trung bình", f"{diem_tb:.2f}")
c2.metric("Điểm cao nhất", f"{sv_cao_nhat['Tổng kết']:.2f}")
c3.metric("Điểm thấp nhất", f"{sv_thap_nhat['Tổng kết']:.2f}")
c4.metric("Sinh viên đạt", f"{so_sv_dat}/{len(df)}")

st.write(
    f"🏆 Điểm cao nhất: **{sv_cao_nhat['Họ tên']}** "
    f"({sv_cao_nhat['Tổng kết']:.2f})"
)
st.write(
    f"📌 Điểm thấp nhất: **{sv_thap_nhat['Họ tên']}** "
    f"({sv_thap_nhat['Tổng kết']:.2f})"
)

# 9. Bảng điểm
st.subheader("📋 Bảng điểm chi tiết")

def mau_xep_loai(row):
    mau = {
        "Giỏi": "background-color: #bbf7d0; color: #166534",
        "Khá": "background-color: #bfdbfe; color: #1e40af",
        "Trung bình": "background-color: #fef3c7; color: #92400e",
        "Yếu": "background-color: #fecaca; color: #991b1b"
    }
    return [
        mau.get(row["Xếp loại"], "")
        if col == "Xếp loại" else ""
        for col in row.index
    ]

styled_df = df.style.apply(mau_xep_loai, axis=1).format({
    "Chuyên cần": "{:.1f}",
    "Giữa kỳ": "{:.2f}",
    "Cuối kỳ": "{:.2f}",
    "Tổng kết": "{:.2f}"
})

st.dataframe(styled_df, use_container_width=True, hide_index=True)

# 10. Tra cứu sinh viên
st.subheader("🔎 Tra cứu sinh viên")

ten_sv = st.selectbox("Chọn sinh viên:", df["Họ tên"])
sv = df[df["Họ tên"] == ten_sv].iloc[0]

a, b, c, d, e = st.columns(5)
a.metric("Chuyên cần", f"{sv['Chuyên cần']:.1f}")
b.metric("Giữa kỳ", f"{sv['Giữa kỳ']:.2f}")
c.metric("Cuối kỳ", f"{sv['Cuối kỳ']:.2f}")
d.metric("Tổng kết", f"{sv['Tổng kết']:.2f}")
e.metric("Xếp loại", sv["Xếp loại"])

# 11. Biểu đồ điểm
st.subheader("📈 Biểu đồ điểm tổng kết")

fig, ax = plt.subplots(figsize=(12, 5))

colors = [
    "#16a34a" if x >= 8.5
    else "#3b82f6" if x >= 7
    else "#f59e0b" if x >= 5
    else "#ef4444"
    for x in df["Tổng kết"]
]

bars = ax.bar(
    df["Họ tên"],
    df["Tổng kết"],
    color=colors,
    edgecolor="white",
    linewidth=1.5
)

ax.set_title("Điểm tổng kết của 10 sinh viên", fontsize=16, pad=15)
ax.set_xlabel("Họ tên sinh viên")
ax.set_ylabel("Điểm")
ax.set_ylim(0, 10)
ax.grid(axis="y", linestyle="--", alpha=0.3)
ax.set_axisbelow(True)

for bar, diem in zip(bars, df["Tổng kết"]):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.1,
        f"{diem:.2f}",
        ha="center",
        fontsize=9
    )

fig.tight_layout()
st.pyplot(fig)
plt.close(fig)

# 12. Chú thích
st.markdown("---")
st.caption("🎓 Ứng dụng quản lý điểm sinh viên | Xây dựng bằng Python và Streamlit")
