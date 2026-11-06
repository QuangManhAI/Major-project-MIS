"""Đọc Data_do_an.xlsx, chuẩn hoá các bảng dùng cho phân tích (không lấy dữ liệu cá nhân)."""
import pandas as pd

XLSX = "/Users/quangmanh/Project/pizza/data/Data_do_an.xlsx"
WAGE = 40254          # lương TB/giờ (đ)
PROD_T = 330000       # productivity mục tiêu (đ/giờ)
COL_T = 0.1365        # %COL mục tiêu
DOW_VI = {0: "T2", 1: "T3", 2: "T4", 3: "T5", 4: "T6", 5: "T7", 6: "CN"}


def load():
    raw = pd.read_excel(XLSX, sheet_name="Sales data", header=None)
    a = raw.iloc[4:, 0:18].copy()
    a.columns = ["year", "month", "week", "day", "diw", "date", "DI", "HD", "TA_Ecom", "TA_Cus",
                 "Aggr", "sales", "tc_DI", "tc_HD", "tc_Ecom", "tc_Cus", "tc_Aggr", "tc"]
    a = a[pd.to_numeric(a["sales"], errors="coerce").notna()].copy()
    a["date"] = pd.to_datetime(a["date"])
    for c in a.columns[6:]:
        a[c] = a[c].astype(float)
    b = raw.iloc[4:, 19:46].copy()
    b.columns = ["year", "month", "week", "day", "diw", "date", "DI", "HD", "TA_Ecom", "TA_Cus",
                 "Aggr", "sales", "tc_DI", "tc_HD", "tc_Ecom", "tc_Cus", "tc_Aggr", "tc", "guest",
                 "bp_target", "fc_sales", "fc_docket", "completion", "fc_wh", "act_wh", "col", "prod"]
    b = b[pd.to_numeric(b["act_wh"], errors="coerce").notna()].copy()
    b["date"] = pd.to_datetime(b["date"])
    for c in ["sales", "fc_sales", "fc_wh", "act_wh", "col", "prod", "tc"]:
        b[c] = b[c].astype(float)
    for df in (a, b):
        df["dow"] = df["date"].dt.dayofweek
        df["dow_vi"] = df["dow"].map(DOW_VI)
        df["m"] = df["date"].dt.month
    b["excess"] = b["act_wh"] - b["fc_wh"]
    return a, b


if __name__ == "__main__":
    a, b = load()
    print("2025 rows", len(a), "sales", a.sales.sum())
    print(a.groupby("m").sales.sum().round(-6))
    print(a.groupby("dow_vi").sales.mean().round(-3))
    ch = a[["DI", "HD", "TA_Ecom", "TA_Cus", "Aggr"]].sum(); print((ch / ch.sum() * 100).round(1))
    print("2026 rows", len(b))
    m = b.groupby("m").agg(sales=("sales", "sum"), fc=("fc_wh", "sum"), act=("act_wh", "sum"))
    m["excess"] = m.act - m.fc; m["cost"] = m.excess * WAGE
    m["col"] = m.act * WAGE / m.sales; m["col_fc"] = m.fc * WAGE / m.sales
    print(m.round(3)); print("tot excess", m.excess.sum(), "cost", m.cost.sum())
    w = b.groupby("dow").agg(sales=("sales", "mean"), fc=("fc_wh", "mean"), act=("act_wh", "mean"))
    w["col"] = w.act * WAGE / w.sales
    print(w.round(2))
    aug = b[b.m == 8]
    wa = aug.groupby("dow").agg(sales=("sales", "mean"), fc=("fc_wh", "mean"), act=("act_wh", "mean"), n=("sales", "count"))
    wa["col"] = wa.act * WAGE / wa.sales; print(wa.round(2))
    print("corr sales-act", b.sales.corr(b.act_wh), "corr sales-fc", b.sales.corr(b.fc_wh))
    print("min act wh", b.act_wh.min(), "max", b.act_wh.max(), "fc min", b.fc_wh.min(), b.fc_wh.max())
    print("days act<fc", (b.excess < 0).sum(), "of", len(b))
