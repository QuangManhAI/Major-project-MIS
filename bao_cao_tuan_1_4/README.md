# Báo cáo tuần 1–4 – Đồ án HTTTQL (HR – The Pizza Company)

## Biên dịch báo cáo
```bash
xelatex main.tex && xelatex main.tex     # chạy 2 lần để có mục lục, danh mục hình/bảng
```
Cần font Times New Roman và Courier New (có sẵn trên macOS/Windows).

## Vẽ lại toàn bộ hình (Python 3 + matplotlib, pandas, openpyxl)
```bash
cd scripts
python fig_legend.py   # bảng ký hiệu BPMN
python fig_p1.py       # P1 tuyển dụng   AS-IS + TO-BE
python fig_p2.py       # P2 đào tạo      AS-IS + TO-BE
python fig_p3.py       # P3 xếp ca       AS-IS + TO-BE
python fig_p4.py       # P4 chấm công    AS-IS + TO-BE + sơ đồ tổng thể
python fig_uml.py      # use case, sơ đồ lớp, kiến trúc, Gantt
python charts.py       # biểu đồ phân tích dữ liệu (đọc ../../data/Data_do_an.xlsx)
```
`scripts/bpmn.py` là thư viện vẽ BPMN 2.0 (pool/lane, event, task type, gateway, message flow, data object…).

## Odoo (thư mục ../odoo)
```bash
cd ../odoo && docker compose up -d           # Odoo 18 + PostgreSQL 16, http://localhost:8069
python scripts/setup_db.py                   # tạo CSDL tpc_demo, cài 10 module HR
python scripts/configure_hr.py               # phòng ban, vị trí, giai đoạn tuyển dụng, kỹ năng, dữ liệu giả
python scripts/screenshots.py name=/odoo/... # chụp màn hình (cần: pip install playwright && playwright install chromium)
```
Đăng nhập: admin / admin (chỉ dùng trên máy cá nhân).

## Các chỗ nhóm phải tự điền / tự làm
Tìm `\todo{` trong main.tex: tên khoa, GVHD, mã lớp, họ tên – MSSV, biên bản họp, link ghi âm, phạm vi dùng AI.
Phỏng vấn chính thức + khảo sát → cập nhật các bước "cần xác nhận" trong sơ đồ P3, P4.
