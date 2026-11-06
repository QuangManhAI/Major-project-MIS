"""Biểu đồ phân tích hiện trạng từ Data_do_an.xlsx."""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from data_prep import load, WAGE, PROD_T, COL_T, DOW_VI

OUT = "../figures/"
BLUE, ORANGE, AQUA = "#2a78d6", "#eb6834", "#1baf7a"
REF = "#a3a29c"        # tham chiếu / định mức (trung tính)
TXT, TXT2, GRID = "#0b0b0b", "#52514e", "#e6e5e0"
plt.rcParams.update({
    "font.family": ["Arial", "DejaVu Sans"], "pdf.fonttype": 42, "font.size": 9,
    "axes.edgecolor": "#bdbcb6", "axes.labelcolor": TXT2, "xtick.color": TXT2, "ytick.color": TXT2,
    "axes.spines.top": False, "axes.spines.right": False, "axes.grid": True, "axes.grid.axis": "y",
    "grid.color": GRID, "grid.linewidth": 0.6, "axes.axisbelow": True, "legend.frameon": False,
    "axes.titlesize": 10, "axes.titleweight": "bold", "axes.titlelocation": "left",
})
vn = lambda x, d=0: f"{x:,.{d}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def save(fig, name):
    fig.savefig(OUT + name + ".pdf", bbox_inches="tight")
    fig.savefig(OUT + name + ".png", bbox_inches="tight", dpi=200)
    plt.close(fig)


a, b = load()
order = list(range(7)); labels = [DOW_VI[i] for i in order]

# 1. Doanh thu theo tháng 2025
ms = a.groupby("m").sales.sum() / 1e9
fig, ax = plt.subplots(figsize=(6.4, 2.8))
ax.bar(ms.index, ms.values, color=BLUE, width=0.62)
ax.axhline(ms.mean(), color=REF, ls="--", lw=1)
ax.text(12.45, ms.mean(), f"TB {vn(ms.mean(), 2)} tỷ", va="center", ha="left", color=TXT2, fontsize=8)
for m in (2, 12):
    ax.text(m, ms[m] + 0.02, vn(ms[m], 2), ha="center", va="bottom", fontsize=8, color=TXT)
ax.set_xticks(range(1, 13), [f"T{i}" for i in range(1, 13)])
ax.set_ylabel("Tỷ đồng"); ax.set_ylim(0, 1.85); ax.set_xlim(0.4, 14.2)
ax.set_title("Doanh thu theo tháng năm 2025 (tổng 17,08 tỷ đồng)")
save(fig, "c1_sales_month_2025")

# 2. Doanh thu TB theo thứ 2025
ws = a.groupby("dow").sales.mean().reindex(order) / 1e6
fig, ax = plt.subplots(figsize=(6.4, 2.7))
ax.bar(labels, ws.values, color=[ORANGE if i in (0, 3, 4) else BLUE for i in order], width=0.6)
for i, v in enumerate(ws.values):
    ax.text(i, v + 1, vn(v, 1), ha="center", va="bottom", fontsize=8, color=TXT)
ax.set_ylabel("Triệu đồng/ngày"); ax.set_ylim(0, 80)
ax.set_title("Doanh thu trung bình theo thứ năm 2025 – T2, T5, T6 chỉ bằng ~½ cuối tuần")
save(fig, "c2_sales_dow_2025")

# 3. Giờ công định mức vs thực tế theo tháng 2026
mm = b.groupby("m").agg(sales=("sales", "sum"), fc=("fc_wh", "sum"), act=("act_wh", "sum"))
mm["exc"] = mm.act - mm.fc
x = np.arange(len(mm)); w = 0.38
fig, ax = plt.subplots(figsize=(6.6, 3.0))
ax.bar(x - w / 2 - 0.01, mm.fc, w, color=REF, label="Giờ định mức (Forecast WH)")
ax.bar(x + w / 2 + 0.01, mm.act, w, color=BLUE, label="Giờ thực tế (Actual WH)")
for i, (e, act) in enumerate(zip(mm.exc, mm.act)):
    ax.text(i + w / 2, act + 60, ("+" if e > 0 else "") + vn(e), ha="center", va="bottom", fontsize=7.5,
            color=TXT)
ax.set_xticks(x, [f"T{m}/26" for m in mm.index]); ax.set_ylabel("Giờ công/tháng"); ax.set_ylim(0, 8900)
ax.legend(loc="upper left", ncol=2, fontsize=8)
ax.set_title("Giờ công định mức và thực tế, T1–T8/2026 (số trên cột = giờ chênh lệch)")
save(fig, "c3_hours_month_2026")

# 4. %COL theo tháng
col = mm.act * WAGE / mm.sales * 100
colfc = mm.fc * WAGE / mm.sales * 100
fig, ax = plt.subplots(figsize=(6.6, 2.8))
ax.plot(x, col, color=BLUE, lw=2, marker="o", ms=5, label="%COL thực tế")
ax.plot(x, colfc, color=REF, lw=2, marker="o", ms=5, label="%COL nếu xếp đúng định mức")
ax.axhline(COL_T * 100, color=ORANGE, lw=1.2, ls="--")
ax.text(len(x) - 0.6, COL_T * 100 + 0.12, "Mục tiêu 13,65%", color=TXT2, fontsize=8, ha="right")
for i in (1, 7):
    ax.annotate(vn(col.iloc[i], 1) + "%", (i, col.iloc[i]), textcoords="offset points", xytext=(0, 7),
                ha="center", fontsize=8, color=TXT)
ax.set_xticks(x, [f"T{m}/26" for m in mm.index]); ax.set_ylabel("%COL"); ax.set_ylim(10, 17.5)
ax.legend(loc="lower left", ncol=2, fontsize=8)
ax.set_title("%COL theo tháng 2026: 6/8 tháng vượt mục tiêu 13,65%")
save(fig, "c4_col_month_2026")

# 5. Giờ TB/ngày theo thứ T1–T8/2026
wd = b.groupby("dow").agg(sales=("sales", "mean"), fc=("fc_wh", "mean"), act=("act_wh", "mean")).reindex(order)
xx = np.arange(7)
fig, ax = plt.subplots(figsize=(6.6, 3.0))
ax.bar(xx - w / 2 - 0.01, wd.fc, w, color=REF, label="Định mức TB/ngày")
ax.bar(xx + w / 2 + 0.01, wd.act, w, color=BLUE, label="Thực tế TB/ngày")
for i in xx:
    e = wd.act.iloc[i] - wd.fc.iloc[i]
    ax.text(i, max(wd.act.iloc[i], wd.fc.iloc[i]) + 6, ("+" if e > 0 else "−") + vn(abs(e)), ha="center",
            fontsize=8, color=ORANGE if e > 0 else AQUA, fontweight="bold")
ax.set_xticks(xx, labels); ax.set_ylabel("Giờ công/ngày"); ax.set_ylim(0, 270)
ax.legend(loc="upper left", ncol=2, fontsize=8)
ax.set_title("Giờ công TB theo thứ, T1–T8/2026: thừa ngày vắng, thiếu cuối tuần")
save(fig, "c5_hours_dow_2026")

# 6. Scatter doanh thu - giờ công
fig, ax = plt.subplots(figsize=(6.6, 3.4))
bb = b[b.act_wh <= 300]   # loại 9 ngày lễ/Tết (giờ công > 300, nghi tính hệ số lương lễ)
ax.scatter(bb.sales / 1e6, bb.act_wh, s=14, color=BLUE, alpha=0.65, edgecolor="white", lw=0.4,
           label="Giờ thực tế mỗi ngày")
xs = np.linspace(0, bb.sales.max() / 1e6, 50)
ax.plot(xs, xs * 1e6 / PROD_T, color=ORANGE, lw=1.6, label="Giờ cần theo Productivity 330.000đ/giờ")
ax.set_xlabel("Doanh thu ngày (triệu đồng)"); ax.set_ylabel("Giờ công thực tế")
ax.grid(axis="x", color=GRID, lw=0.6)
ax.legend(loc="upper left", fontsize=8)
r = bb.sales.corr(bb.act_wh)
ax.set_title(f"Giờ công thực tế ít thay đổi theo doanh thu (r = {vn(r, 2)}; định mức r = {vn(bb.sales.corr(bb.fc_wh), 2)})")
ax.text(0.99, 0.02, "Không gồm 9 ngày lễ/Tết có giờ công > 300", transform=ax.transAxes, ha="right", fontsize=7.5, color=TXT2)
save(fig, "c6_scatter_2026")

# 7. Cơ cấu kênh 2025
ch = a[["DI", "Aggr", "TA_Cus", "HD", "TA_Ecom"]].sum()
names = ["Tại chỗ (Dine-in)", "Aggregator (Grab, ShopeeFood…)", "Mang đi – khách đến", "Giao hàng (HD)",
         "Mang đi – đặt online"]
pct = ch / ch.sum() * 100
fig, ax = plt.subplots(figsize=(6.4, 2.4))
ax.barh(names[::-1], pct.values[::-1], color=BLUE, height=0.55)
for i, v in enumerate(pct.values[::-1]):
    ax.text(v + 0.6, i, vn(v, 1) + "%", va="center", fontsize=8, color=TXT)
ax.grid(axis="y", visible=False); ax.grid(axis="x", color=GRID)
ax.set_xlim(0, 50); ax.set_xlabel("% doanh thu 2025")
ax.set_title("Cơ cấu doanh thu theo kênh năm 2025")
save(fig, "c7_channel_2025")
print("charts ok")
