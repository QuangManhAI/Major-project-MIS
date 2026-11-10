# Đồ án HTTTQL – Hệ thống quản lý nhân sự cho The Pizza Company

**Đề tài:** Thiết kế hệ thống quản lý tuyển dụng, đào tạo và xếp ca nhân sự theo dự báo doanh thu trên nền tảng Odoo cho chuỗi nhà hàng The Pizza Company.

**Mảng nghiệp vụ:** HR · **KPI xuyên suốt:** `%COL` (chi phí nhân công / doanh thu) và `Productivity` (doanh thu / giờ công).

Hệ thống giải quyết 4 quy trình:

| Mã | Quy trình | Mục tiêu cải tiến |
|----|-----------|-------------------|
| P1 | Tuyển dụng | Rút ngắn thời gian từ lúc ứng viên ứng tuyển đến ca làm đầu tiên |
| P2 | Đào tạo / onboarding | Theo dõi tiến độ đào tạo và kết quả test tập trung |
| P3 | Xếp ca | Xếp ca theo dự báo doanh thu thay vì theo thói quen |
| P4 | Chấm công | Báo cáo %COL hằng ngày |

Kế hoạch chi tiết 10 tuần: [KE_HOACH_DO_AN.md](KE_HOACH_DO_AN.md).

## Cấu trúc thư mục

```
.
├── KE_HOACH_DO_AN.md            # Kế hoạch thực hiện đồ án
├── P1_TuyenDung_ASIS.drawio     # Sơ đồ BPMN P1 AS-IS (mở bằng draw.io)
├── bản_mẫu.pdf                  # Mẫu báo cáo
├── requirements.txt             # Thư viện Python
├── tpc_hr_<ngày-giờ>.zip        # Bản sao lưu CSDL Odoo (dump.sql + filestore)
├── documents/                   # Tài liệu tham khảo, BPMN, ghi chép phỏng vấn
├── bao_cao_tuan_1_4/            # Báo cáo tuần 1–4 (LaTeX)
│   ├── main.tex / main.pdf
│   ├── figures/                 # Hình đã xuất (PNG + PDF), ảnh chụp Odoo
│   └── scripts/                 # Script Python vẽ BPMN, UML, biểu đồ
└── odoo/                        # Môi trường Odoo tự host
    ├── docker-compose.yml       # Odoo 18 + PostgreSQL 16
    ├── config/odoo.conf
    ├── addons/                  # Module tự viết (tpc_labour_planning)
    └── scripts/                 # Tạo CSDL, cấu hình HR, chụp màn hình qua XML-RPC
```

## Yêu cầu

- Python 3.10 trở lên
- Docker Desktop (để chạy Odoo)
- XeLaTeX (TeX Live / MiKTeX / MacTeX) và font Times New Roman, Courier New (để biên dịch báo cáo)
- [draw.io](https://www.drawio.com/) (tuỳ chọn, để sửa file `.drawio`)

## Cài đặt môi trường Python

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
playwright install chromium      # chỉ cần nếu chụp màn hình Odoo
```

## Chạy Odoo

```bash
cd odoo
docker compose up -d             # Odoo 18 + PostgreSQL 16 tại http://localhost:8069
```

Có hai cách để có dữ liệu:

**Cách 1 – Khôi phục bản sao lưu (khuyến nghị).** Mở http://localhost:8069/web/database/manager → *Restore Database*, nhập master password (`admin_passwd` trong `odoo/config/odoo.conf`), chọn file `tpc_hr_<ngày-giờ>.zip` ở thư mục gốc, đặt tên CSDL `tpc_hr`.

**Cách 2 – Tạo mới bằng script.**

```bash
python scripts/setup_db.py       # tạo CSDL tpc_demo, cài 10 module HR
python scripts/configure_hr.py   # phòng ban, vị trí, giai đoạn tuyển dụng, kỹ năng, dữ liệu mẫu
```

Đăng nhập: `admin` / `admin` (chỉ dùng trên máy cá nhân).

Chụp màn hình cho báo cáo:

```bash
python scripts/screenshots.py pipeline=/odoo/recruitment
```

## Vẽ lại hình cho báo cáo

```bash
cd bao_cao_tuan_1_4/scripts
python fig_legend.py   # bảng ký hiệu BPMN
python fig_p1.py       # P1 tuyển dụng  AS-IS + TO-BE
python fig_p2.py       # P2 đào tạo     AS-IS + TO-BE
python fig_p3.py       # P3 xếp ca      AS-IS + TO-BE
python fig_p4.py       # P4 chấm công   AS-IS + TO-BE + sơ đồ tổng thể
python fig_uml.py      # use case, sơ đồ lớp, kiến trúc, Gantt
python charts.py       # biểu đồ phân tích dữ liệu (cần Data_do_an.xlsx)
```

`scripts/bpmn.py` là thư viện vẽ BPMN 2.0 dùng chung; `scripts/drawio_export.py` xuất sơ đồ sang `.drawio`.

Xuất toàn bộ sơ đồ BPMN sang draw.io (ra thư mục `bao_cao_tuan_1_4/drawio/`, mở bằng draw.io để chỉnh sửa):

```bash
python export_drawio.py
```

> **Lưu ý:** một số script đang để đường dẫn tuyệt đối trên máy macOS. Sửa lại trước khi chạy:
> - `bao_cao_tuan_1_4/scripts/data_prep.py` → biến `XLSX` (đường dẫn tới `Data_do_an.xlsx`)
> - `odoo/scripts/screenshots.py` → biến `OUT` (thư mục lưu ảnh)
>
> File `.xlsx` không được đưa lên git (xem `.gitignore`) vì chứa dữ liệu nội bộ của doanh nghiệp.

## Biên dịch báo cáo

```bash
cd bao_cao_tuan_1_4
xelatex main.tex && xelatex main.tex   # chạy 2 lần để có mục lục, danh mục hình/bảng
```

Xem thêm [bao_cao_tuan_1_4/README.md](bao_cao_tuan_1_4/README.md).
