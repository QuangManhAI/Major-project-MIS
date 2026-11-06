# KẾ HOẠCH THỰC HIỆN ĐỒ ÁN HTTTQL — HƯỚNG 1: NHÂN SỰ

> **Tên đề tài (đề xuất):** Thiết kế hệ thống quản lý tuyển dụng, đào tạo và xếp ca nhân sự theo dự báo doanh thu trên nền tảng Odoo cho chuỗi nhà hàng The Pizza Company
>
> **Mảng nghiệp vụ (theo slide thầy):** HR
> **Thời gian:** 10 tuần · **Nhóm:** 5 ± 1 SV
> **KPI xuyên suốt toàn đồ án:** `%COL` (chi phí nhân công / doanh thu) và `Productivity` (doanh thu / giờ công)

---

## 0. Vì sao đề tài này đứng vững (dùng cho Chương 1 và phần thuyết trình)

| Bằng chứng | Nguồn |
|---|---|
| "Khó khăn chính ở đây đang là nhân sự" · cửa hàng cần 40–50 NV · part-time gắn bó kém · nghỉ nhiều sau Tết · khó tuyển ở Q2 | Phỏng vấn quản lý khu vực |
| Tuyển dụng: dán standee → phỏng vấn → điền link → **mang hồ sơ giấy lên văn phòng** → chờ mã NV (2–3 ngày) | Phỏng vấn |
| Đào tạo: có training plan 2 tuần và bài test, nhưng **tiến độ đào tạo mỗi người khác nhau** và không theo dõi được tập trung | Phỏng vấn |
| **Tháng 08/2026: dùng 5.882 giờ công thực tế, định mức là 4.863 giờ → thừa ~1.018 giờ ≈ 41 triệu đồng/tháng** (lương TB 40.254đ/giờ) | Sheet `Store Perfomance` |
| %COL thực tế **15,5%**, mục tiêu **13,65%**. Nếu xếp đúng định mức giờ thì chỉ còn **12,8%** | Sheet `Store Perfomance` |
| Cuối tuần xếp ca gần đúng định mức. **Thứ 2, 5, 6 thừa 50–70 giờ/ngày**: số giờ gần như không đổi trong khi doanh thu chỉ bằng một nửa → xếp ca theo thói quen, không theo dự báo doanh thu | Tính từ sheet `Store Perfomance` |

| Thứ | Doanh thu TB/ngày (nghìn đ) | Giờ thực tế | Giờ định mức | %COL |
|---|---|---|---|---|
| T2 | 33.588 | 165,1 | 93,5 | **19,8%** |
| T3 | 51.707 | 205,6 | 168,5 | 16,0% |
| T4 | 65.802 | 218,1 | 208,1 | 13,3% |
| T5 | 31.373 | 171,7 | 100,4 | **22,0%** |
| T6 | 40.697 | 164,9 | 115,0 | 16,3% |
| T7 | 56.830 | 198,4 | 195,4 | 14,1% |
| CN | 63.952 | 204,6 | 210,3 | 12,9% |

→ **Câu chuyện của đồ án:** nhân sự vừa *thiếu* (khó tuyển, tuyển chậm, nghỉ nhiều), vừa *xếp sai chỗ* (thừa giờ ngày vắng). Hệ thống cần (1) tuyển nhanh hơn, (2) đào tạo đo lường được, (3) xếp ca theo dự báo doanh thu, (4) báo cáo %COL hằng ngày.

> ⚠️ Lưu ý khi phỏng vấn lại: nên hỏi quản lý về **số người tối thiểu mỗi quầy/ca**. Số này giải thích vì sao ngày vắng không giảm giờ được bằng định mức, và sẽ thành một ràng buộc trong module xếp ca.

---

## 1. Đối chiếu yêu cầu của thầy → việc cần làm

| Yêu cầu trong slide | Việc nhóm phải làm | Mục |
|---|---|---|
| Tìm hiểu nghiệp vụ thực tế | Phỏng vấn chính thức có quay/ghi âm, thu thập biểu mẫu, dữ liệu bổ sung | §2 |
| Phân tích BPMN **AS-IS & TO-BE**, chỉ ra problem/issue và value cải tiến | 4 quy trình × 2 sơ đồ = 8 sơ đồ BPMN, bảng Problem và bảng Value | §3 |
| **Minh chứng & xác nhận cải tiến** | Phân tích số liệu Excel, mô phỏng xếp ca, phiếu xác nhận của doanh nghiệp | §4, §10 |
| Thiết kế hệ thống: **logical & physical** | Use case, ERD/Class diagram (logical); mô hình Odoo, phân quyền, kiến trúc triển khai (physical) | §5 |
| Odoo: tìm hiểu & cài đặt | Cài Odoo Community tự host (Docker) | §6 |
| **Customize Odoo theo đặc thù doanh nghiệp** | Cấu hình các module HR và tùy biến form/field/quy trình | §7 |
| **Add-on module** | Tự viết module `tpc_labour_planning` (xếp ca theo dự báo doanh thu và theo dõi %COL) | §8 |
| Yêu cầu nâng cao cho ERP | Dashboard Power BI, thông báo tự động, cổng ứng viên | §9 |
| **Demo & ghi clip minh chứng** | Kịch bản demo đầu-cuối và quay clip | §10 |
| Nhận xét của đơn vị/doanh nghiệp | Gửi demo cho quản lý xem, xin phiếu nhận xét | §10 |
| Chỉn chu báo cáo + thuyết trình | Báo cáo theo khung của thầy và slide | §11, §12 |
| Mức độ nỗ lực, nghiêm túc → *"AI???"* | Lưu minh chứng quá trình làm (biên bản họp, git log, ảnh màn hình theo ngày) | §14 |

> **Bài học từ N2:** N2 dùng Odoo Online nên **không cài được add-on module tự viết** (tự ghi ở mục Hạn chế 7.2). Slide của thầy yêu cầu rõ "Add-on module", nên nhóm **bắt buộc phải tự host Odoo**. Đây cũng là điểm vượt N2.

---

## 2. Thu thập nghiệp vụ (Tuần 1–2)

### 2.1. Buổi phỏng vấn chính thức (quay hoặc ghi âm, đã được quản lý đồng ý)
Gửi trước câu hỏi cho quản lý (lần trước chú có hỏi sao không gửi trước). Nhóm câu hỏi:

**A. Tuyển dụng**
1. Mỗi tháng cửa hàng tuyển trung bình bao nhiêu người? Bao nhiêu người đến phỏng vấn, bao nhiêu người được nhận?
2. Tính từ lúc ứng viên hỏi việc đến khi có mã NV và đi làm ca đầu tiên thì mất bao nhiêu ngày? Bước nào chậm nhất?
3. Ứng viên đến từ nguồn nào (standee, fanpage, phòng tuyển dụng gửi data, người quen giới thiệu)? Nguồn nào hiệu quả nhất?
4. Có khi nào bị sót ứng viên, quên hẹn, hoặc ứng viên đã hẹn mà không đến không?
5. Thông tin ứng viên đang lưu ở đâu: giấy, link form, hay Excel?

**B. Onboarding và đào tạo**
6. Training plan 2 tuần gồm những gì? Xin bản mẫu (đã che thông tin nội bộ nếu cần).
7. Bài test cuối đào tạo chấm thế nào? Ai chấm? Kết quả lưu ở đâu?
8. Bao nhiêu % nhân viên mới nghỉ trong 2 tuần hoặc 1 tháng đầu?
9. Có bao nhiêu quầy (bếp 4–5 quầy, thu ngân, phục vụ...)? Một người có làm được nhiều quầy không?

**C. Xếp ca và chấm công**
10. Ai xếp ca? Xếp bằng gì (Excel, giấy, nhóm Zalo)? Xếp trước bao lâu?
11. Khi xếp ca có nhìn vào doanh thu dự báo (Forecast Sales) không? Định mức Productivity 330.000đ/giờ dùng thế nào?
12. **Mỗi ca, mỗi quầy tối thiểu cần mấy người?**
13. Đổi ca hoặc nghỉ đột xuất xử lý thế nào? Thường báo trước bao lâu?
14. Chấm công bằng gì? Cuối ngày có so giờ thực tế với giờ định mức không?

**D. Nghỉ việc**
15. Tỷ lệ nghỉ việc theo tháng (nhấn mạnh tháng 2 sau Tết)? Có số liệu 12 tháng không?
16. Lý do nghỉ chủ yếu? Có phỏng vấn trước khi nghỉ (exit interview) không?

**E. Mong muốn**
17. Nếu có một hệ thống tự gợi ý số giờ ca theo dự báo doanh thu thì chú có dùng không? Cần hiện những gì?

### 2.2. Dữ liệu và biểu mẫu cần xin thêm
- [ ] Bảng xếp ca mẫu 1–2 tuần (có thể che tên)
- [ ] Training plan / checklist đào tạo theo quầy
- [ ] Mẫu tin tuyển dụng, mẫu đơn ứng tuyển (chụp màn hình trang tuyển dụng như quản lý gợi ý)
- [ ] Số người nghỉ việc và số người tuyển theo tháng (12 tháng)
- [ ] Danh sách quầy/vị trí và số người tối thiểu

### 2.3. Đầu ra
- File ghi âm/video và **biên bản phỏng vấn** (đánh máy lại, có ngày giờ, người tham gia)
- Bảng tổng hợp yêu cầu (giống Bảng 4.1 của N2)
- Bảng câu hỏi khảo sát (Google Form) gửi thêm **3–5 quản lý ca hoặc nhân viên part-time** để có dữ liệu định lượng (ví dụ: thời gian xếp ca mỗi tuần, số lần đổi ca)

---

## 3. Phân tích nghiệp vụ bằng BPMN (Tuần 3–4)

**Công cụ:** draw.io (diagrams.net) hoặc Camunda Modeler / bpmn.io. Dùng ký hiệu BPMN 2.0 chuẩn: pool/lane, start/end event, gateway, data object, message flow.
**Lane gợi ý:** Ứng viên/Nhân viên · Quản lý cửa hàng (RGM/Shift Manager) · Phòng Nhân sự–Tuyển dụng · Quản lý khu vực · Hệ thống (chỉ có ở TO-BE)

### 3.1. Bốn quy trình cần vẽ (mỗi quy trình 1 AS-IS + 1 TO-BE)

| # | Quy trình | AS-IS (theo phỏng vấn) | TO-BE (trên Odoo) |
|---|---|---|---|
| P1 | **Tuyển dụng** | Phòng TD gửi data hoặc cửa hàng dán standee/đăng fanpage → ứng viên hỏi trực tiếp → hẹn lịch PV → PV → điền link → mang hồ sơ giấy lên văn phòng (thứ 3/thứ 5) → chờ mã NV | Tin tuyển dụng trên trang Jobs → ứng viên nộp online → hồ sơ vào pipeline (Mới → Hẹn PV → PV → Đề nghị → Nhận việc) → tự gửi email/lịch hẹn → nhận việc thì tự tạo hồ sơ nhân viên và gửi Phòng NS duyệt trên hệ thống |
| P2 | **Onboarding và đào tạo** | Phân quầy sau PV → kèm cặp theo training plan giấy → test → không theo dõi tập trung | Kế hoạch onboarding tự sinh khi tạo NV → khóa eLearning theo quầy → bài test (Survey) → hệ thống ghi nhận "đủ điều kiện làm quầy X" (kỹ năng) |
| P3 | **Xếp ca** | Quản lý xếp tay theo kinh nghiệm → gửi Zalo → giờ ca gần như cố định mỗi ngày | Nhập/Import Forecast Sales → **module tự tính giờ cần theo Productivity target và số người tối thiểu** → quản lý điều chỉnh và xếp người có kỹ năng phù hợp → công bố ca → NV xem ca, xin đổi ca qua Approvals/Time Off |
| P4 | **Chấm công và theo dõi %COL** | Chấm công → cuối ngày gõ Actual WH vào Excel → tính COL → gửi email khu vực | Chấm công (Attendances/kiosk) → hệ thống tự tính Actual WH, %COL, Productivity theo ngày → cảnh báo khi %COL vượt mục tiêu → dashboard khu vực |

### 3.2. Bảng Problem/Issue (bắt buộc, mỗi dòng phải có bằng chứng)

| Mã | Vấn đề | Quy trình | Bằng chứng | Ảnh hưởng |
|---|---|---|---|---|
| I1 | Hồ sơ ứng viên phân tán (standee, fanpage, data phòng TD) | P1 | Phỏng vấn | Sót ứng viên, không biết nguồn nào hiệu quả |
| I2 | Thủ tục giấy mang lên văn phòng làm thời gian đi làm kéo dài 2–4 ngày | P1 | Phỏng vấn ("thứ Hai PV… thứ Năm đi làm") | Thiếu người trong lúc chờ |
| I3 | Không theo dõi được tiến độ đào tạo từng người | P2 | Phỏng vấn | Không biết ai làm được quầy nào |
| I4 | Xếp ca không theo dự báo doanh thu | P3 | Excel: thừa ~1.018 giờ/tháng | Thừa ~41 triệu/tháng, %COL 15,5% so với mục tiêu 13,65% |
| I5 | %COL chỉ biết khi nhập tay cuối ngày | P4 | Sheet `Store Perfomance` nhập tay | Phát hiện muộn, không điều chỉnh kịp |
| I6 | Không dự báo được đợt nghỉ việc (sau Tết) | P1 | Phỏng vấn | Tuyển bù bị động |

### 3.3. Bảng Value (giá trị cải tiến, phải đo được)

| Mã | Giá trị | Chỉ số đo | Trước | Sau (mục tiêu/mô phỏng) | Cách chứng minh |
|---|---|---|---|---|---|
| V1 | Rút ngắn thời gian tuyển | Số ngày từ lúc nộp hồ sơ đến ca đầu tiên | 3–5 ngày | 1–2 ngày | Demo luồng; hỏi quản lý xác nhận |
| V2 | Đào tạo đo lường được | % NV hoàn thành đào tạo đúng hạn | Không đo được | Dashboard eLearning | Ảnh màn hình |
| V3 | **Giảm giờ công thừa** | Giờ công/tháng, %COL | 5.882 giờ · 15,5% | ~4.900–5.200 giờ · ~13,5–14% | **Mô phỏng lại tháng 8 bằng add-on module** (§4.2) |
| V4 | Báo cáo %COL tức thời | Thời gian lập báo cáo | Nhập tay cuối ca | Tự động, theo thời gian thực | Demo |
| V5 | Chủ động tuyển trước mùa nghỉ | Số người tuyển trước tháng 2 | Bị động | Có kế hoạch | Báo cáo nghỉ việc theo tháng |

> Số giờ "Sau" ở V3 **không được bịa**. Lấy kết quả chạy mô phỏng thật (§4.2), có tính ràng buộc số người tối thiểu, rồi ghi đúng con số ra được.

---

## 4. Phân tích dữ liệu và minh chứng cải tiến (Tuần 3–5)

### 4.1. Phân tích hiện trạng từ `Data_do_an.xlsx`
Dùng Excel/Python/Power BI để làm và chụp vào báo cáo:
1. **Sheet `Sales data`**: doanh thu và TC (lượt khách) theo ngày năm 2025 → biểu đồ mùa vụ theo tháng và theo thứ trong tuần (để thấy ngày vắng/ngày đông lặp lại theo quy luật).
2. **Sheet `Store Perfomance` (T8/2026)**: so Target Hours với Actual WH theo ngày → bảng ở mục 0, biểu đồ cột chồng giờ thừa theo thứ.
3. Tính **%COL và Productivity theo thứ** → biểu đồ đường so với mục tiêu 13,65% và 330.000đ/giờ.
4. Cơ cấu kênh bán (tại chỗ 41%, aggregator 27%...) → giải thích vì sao cần nhân sự khác nhau cho bếp và phục vụ (có thể dùng để chia giờ theo quầy).

### 4.2. Mô phỏng TO-BE (minh chứng giá trị cải tiến, rất nên có)
- Đưa Forecast Sales tháng 8 vào add-on module → module tính **giờ đề xuất** mỗi ngày = `max(Forecast Sales / Productivity target, số giờ tối thiểu theo quầy)`.
- So sánh: giờ thực tế, giờ đề xuất, chênh lệch theo giờ và theo tiền, %COL mới.
- Đây là phần "xác nhận cải tiến" mà slide thầy yêu cầu. Gửi kết quả cho quản lý xem và xin ý kiến: "con số này có thực tế không?"

### 4.3. Lưu ý dữ liệu nhạy cảm
- File có **tên nhân viên** (sheet `DC STAFF`, `PHỤ CẤP TIỆC`, `BC xóa hủy bill`) và **SĐT khách, ngày sinh của trẻ em** (sheet `BO`) → **không đưa nguyên văn** vào báo cáo hay Odoo demo.
- Dữ liệu nhân viên trong Odoo demo dùng **tên giả**.

---

## 5. Thiết kế hệ thống: Logical & Physical (Tuần 4–5)

### 5.1. Logical
| Sản phẩm | Nội dung |
|---|---|
| **Bảng yêu cầu chức năng** | Mã FR01…FRnn, nhóm theo P1–P4, có mức ưu tiên (Must/Should/Could) |
| **Yêu cầu phi chức năng** | Phân quyền theo vai trò, bảo mật dữ liệu cá nhân NV/ứng viên, dùng được trên điện thoại (NV xem ca), thời gian phản hồi |
| **Bảng Stakeholder** | Ban điều hành, Quản lý khu vực, Quản lý cửa hàng, Quản lý ca, NV part-time, Ứng viên, Phòng NS–Tuyển dụng, IT |
| **Use case diagram** | Actor: Ứng viên, NV, Quản lý ca, Quản lý cửa hàng, Quản lý khu vực, Phòng NS. Khoảng 15–20 use case, **có đặc tả cho 4–5 use case chính** (đây là điểm N2 thiếu) |
| **Class diagram / ERD logic** | Thực thể: Store, Employee, Skill/Station, Applicant, JobPosition, Course, SalesForecast, ShiftTemplate, Shift, Attendance, DailyLabourReport |
| **Sơ đồ hoạt động/tuần tự** | Cho luồng "Tính giờ ca theo dự báo" và "Ứng viên → Nhân viên" |

### 5.2. Physical
| Sản phẩm | Nội dung |
|---|---|
| **Kiến trúc triển khai** | Docker: Odoo + PostgreSQL trên VPS/Railway, domain + HTTPS; Power BI kết nối PostgreSQL (read-only user) |
| **Ánh xạ sang model Odoo** | Store → `res.company` hoặc `stock.warehouse`/model riêng; Employee → `hr.employee`; Applicant → `hr.applicant`; Course → `slide.channel`; Attendance → `hr.attendance`; **model mới** của add-on: `tpc.sales.forecast`, `tpc.shift.template`, `tpc.shift`, `tpc.labour.daily` |
| **Danh sách field tùy biến** | Ví dụ `hr.employee`: `x_station_ids`, `x_employment_type` (FT/PT), `x_bank_tcb_account`, `x_training_status` |
| **Ma trận phân quyền** | Group × Model × CRUD (NV chỉ xem ca của mình; quản lý cửa hàng chỉ thấy cửa hàng mình; khu vực xem tất cả) |
| **Danh sách module cài** | Bảng: module, mục đích, Community/Enterprise |

---

## 6. Cài đặt Odoo (Tuần 1–2)

**Khuyến nghị: Odoo Community 18 (hoặc 19) tự host bằng Docker.**
Lý do: cần cài add-on module tự viết, không bị giới hạn như Odoo Online của N2, và miễn phí.

Các bước:
1. Cài Docker Desktop. Tạo `docker-compose.yml` gồm `odoo:18` + `postgres:16`, mount thư mục `./addons` để chứa module tự viết.
2. Tạo database `tpc_demo`, ngôn ngữ Tiếng Việt, múi giờ Asia/Ho_Chi_Minh, tiền tệ VND.
3. Đưa code lên GitHub (repo của nhóm), mỗi thành viên commit phần mình làm (đây là **minh chứng nỗ lực**).
4. Tuần 5–6: deploy lên server có domain (Railway/VPS/Render) để demo và cho doanh nghiệp truy cập xem.
5. Chụp màn hình từng bước cho Chương 5 của báo cáo.

> Planning, Approvals, Studio, Appraisals là module **Enterprise**, bản Community không có. Có 2 cách:
> (a) Dùng Community và **tự viết phần xếp ca trong add-on** (khuyến nghị: vừa đáp ứng yêu cầu add-on vừa không phụ thuộc bản trả phí).
> (b) Thêm một database Enterprise trial 15 ngày chỉ để chụp/so sánh. Không dùng làm hệ thống chính.

---

## 7. Cấu hình và Customize các module có sẵn (Tuần 3–7)

| Module | Việc cụ thể | Dữ liệu demo |
|---|---|---|
| **Employees** (`hr`) | Tạo cấu trúc: Khu vực → Cửa hàng → Bộ phận (Bếp, Phục vụ, Thu ngân, Giao hàng). Job positions: Crew PT, Crew FT, Shift Manager, RGM. Thêm field tùy biến (FT/PT, quầy đủ điều kiện, TK Techcombank). Dùng **Skills** cho "quầy đã đạt" | 2 cửa hàng (tên thật dạng `TPC LVS`, `TPC VVN` có trong file Excel), ~40 NV tên giả |
| **Recruitment** (`hr_recruitment`) | Stages: Mới → Đã liên hệ → Hẹn PV → Đã PV → Đề nghị → Nhận việc / Loại. Nguồn (UTM): Standee, Fanpage, Phòng TD, Người quen, Website. Mẫu email tự gửi theo stage (xác nhận hồ sơ, mời PV, chúc mừng nhận việc). Hồ sơ "Nhận việc" thì tạo nhân viên | 30–50 ứng viên giả, nhiều nguồn |
| **Website + Jobs** (`website_hr_recruitment`) | Trang tuyển dụng có form nộp đơn kèm câu hỏi: ca muốn làm, khu vực, đã có TK Techcombank chưa | Tin: "Phục vụ part-time – TPC LVS" |
| **eLearning** (`website_slides`) + **Surveys** | Mỗi quầy là một khóa: Phục vụ, Thu ngân, Bếp – Make line, Bếp – Cut & Pack, ATVSTP. Mỗi khóa có bài + quiz/survey test, điểm đạt ≥ 80%. Đạt thì cập nhật Skill của NV (làm bằng Automation hoặc trong add-on) | Nội dung tự soạn ngắn gọn dựa trên checklist doanh nghiệp đưa |
| **Attendances** (`hr_attendance`) | Chế độ Kiosk (quét badge hoặc PIN tại cửa hàng). Giờ thực tế được đẩy vào báo cáo %COL | Sinh dữ liệu chấm công tháng 8 theo Actual WH trong Excel |
| **Time Off** (`hr_holidays`) | Loại nghỉ: Nghỉ phép, Nghỉ đột xuất, **Xin đổi ca** (quy trình duyệt 1 cấp: Quản lý cửa hàng) | Vài đơn mẫu |
| **Discuss / Email** | SMTP Gmail (như N2) để gửi email thật khi demo | — |
| **Automation (base_automation)** | Ví dụ: Ứng viên quá 48h chưa liên hệ → nhắc quản lý; %COL ngày > 15% → gửi email Quản lý khu vực | — |

---

## 8. Add-on module tự viết: `tpc_labour_planning` (Tuần 5–8, phần "ăn điểm" nhất)

### 8.1. Chức năng
1. **Dự báo doanh thu** `tpc.sales.forecast`: cửa hàng, ngày, forecast sales, target sales, forecast TC. Có **wizard import từ Excel** đúng format sheet `Sales data`/`Store Perfomance` mà doanh nghiệp đang dùng (không bắt họ đổi thói quen).
2. **Cấu hình định mức** (trên cửa hàng): Productivity target (330.000đ/giờ), COL target (13,65%), lương TB/giờ (40.254đ), **số người tối thiểu theo quầy và theo khung giờ**.
3. **Tính giờ đề xuất**: `required_hours = max(forecast_sales / productivity_target, min_hours)`. Phân bổ theo khung giờ (ví dụ trưa và tối đông) bằng tỷ lệ doanh thu theo khung giờ.
4. **Mẫu ca** `tpc.shift.template`: Ca sáng 7–15h, chiều 15–22h, ca gãy, ca cao điểm 11–14h...
5. **Xếp ca** `tpc.shift`: giao diện **Calendar/Gantt-like** (view calendar có sẵn ở Community), gán NV vào ca, **chỉ cho chọn NV có Skill quầy tương ứng**, cảnh báo trùng ca hoặc vượt giờ/tuần của NV PT.
6. **Nút "Đề xuất ca tự động"**: sinh ca nháp đủ số giờ cần, ưu tiên NV đã đạt quầy, chia đều giờ.
7. **Công bố ca**: gửi email/thông báo cho NV. NV xem "Ca của tôi" trên portal hoặc điện thoại.
8. **Báo cáo ngày** `tpc.labour.daily`: tự lấy Actual Sales (nhập hoặc import từ POS report), Actual WH (từ Attendances) → tính %COL, Productivity, chênh lệch giờ. Có pivot/graph view và MTD giống sheet `Store Perfomance`.
9. **Cron job**: mỗi tối tính báo cáo ngày, vượt ngưỡng thì gửi cảnh báo.
10. **Báo cáo QWeb PDF**: "Bảng xếp ca tuần" để in dán tại cửa hàng.

### 8.2. Cấu trúc thư mục
```
addons/tpc_labour_planning/
├── __manifest__.py          # depends: hr, hr_attendance, hr_skills, mail, website_slides
├── models/
│   ├── store_config.py       # định mức của cửa hàng
│   ├── sales_forecast.py
│   ├── shift_template.py
│   ├── shift.py
│   └── labour_daily.py       # compute %COL, productivity
├── wizard/
│   ├── import_forecast.py    # đọc .xlsx
│   └── generate_shifts.py    # đề xuất ca tự động
├── views/                    # form, list, calendar, pivot, graph, menu
├── security/
│   ├── ir.model.access.csv
│   └── security.xml          # record rules theo cửa hàng
├── data/cron.xml, mail_template.xml
├── report/shift_week_report.xml
└── demo/demo_data.xml
```

### 8.3. Mức tối thiểu và mức mở rộng
- **MVP (bắt buộc xong trước giữa kỳ/tuần 7):** mục 1, 2, 3, 5, 8.
- **Mở rộng (cuối kỳ):** 6, 7, 9, 10, import Excel.

---

## 9. Yêu cầu nâng cao / tích hợp (Tuần 6–9)
| Hạng mục | Mô tả | Mức độ |
|---|---|---|
| **Dashboard Power BI** | Kết nối PostgreSQL của Odoo (user chỉ đọc). Trang 1: %COL và Productivity theo ngày/thứ, so mục tiêu. Trang 2: giờ thực tế so với giờ đề xuất. Trang 3: tuyển dụng (theo nguồn, theo stage, time-to-hire). Trang 4: nghỉ việc theo tháng | Nên có (N2 mới kết nối được, chưa có dashboard thật → mình làm dashboard thật để vượt) |
| **Dashboard trong Odoo** | Graph/pivot của module + Spreadsheet dashboard (Community có `spreadsheet_dashboard`) | Nên có |
| **Dự báo đơn giản** | Dự báo doanh thu tuần tới bằng trung bình cùng thứ của 4 tuần trước × hệ số mùa vụ từ dữ liệu 2025 (viết trong module, không cần ML phức tạp) | Điểm cộng |
| **Thông báo Zalo/Telegram** | Gửi lịch ca qua bot (doanh nghiệp quen dùng Zalo) | Tùy chọn |

---

## 10. Demo, clip minh chứng và xác nhận doanh nghiệp (Tuần 8–9)

### 10.1. Kịch bản demo (1 clip 8–12 phút, hoặc 4 clip ngắn)
1. **Tuyển dụng:** Ứng viên vào trang Jobs nộp đơn → quản lý thấy trong pipeline → kéo sang "Hẹn PV" → email mời PV tự gửi → "Nhận việc" → tạo hồ sơ NV.
2. **Đào tạo:** NV mới đăng nhập → học khóa "Phục vụ" → làm test đạt 85% → Skill "Phục vụ" được cập nhật.
3. **Xếp ca:** Import Forecast tuần → bấm "Đề xuất ca" → hệ thống ra số giờ cần mỗi ngày (thứ 2 ít, cuối tuần nhiều) → quản lý chỉnh → Công bố → NV nhận email.
4. **Chấm công và %COL:** NV check-in/out ở kiosk → cuối ngày báo cáo tự tính %COL → vượt ngưỡng thì email cảnh báo → mở dashboard Power BI.
5. **Mô phỏng tháng 8:** bảng so sánh giờ thực tế với giờ đề xuất, số tiền tiết kiệm.

Quay bằng OBS, có thuyết minh. Upload Drive/YouTube (không công khai) và để link ở phụ lục.

### 10.2. Xác nhận của doanh nghiệp (tiêu chí chấm riêng trong slide)
- Hẹn quản lý khu vực xem demo 20–30 phút (gặp trực tiếp hoặc Google Meet).
- Chuẩn bị **Phiếu nhận xét/xác nhận** 1 trang: các mục đánh giá (mức độ đúng nghiệp vụ, tính khả thi, giá trị cải tiến), thang điểm 1–5, ý kiến góp ý, chữ ký/xác nhận (nếu chú đồng ý). Đưa vào phụ lục.
- Ghi lại góp ý → sửa → ghi vào báo cáo mục "Phản hồi của doanh nghiệp và điều chỉnh".

---

## 11. Viết báo cáo (song song, hoàn thiện Tuần 9–10)

Theo đúng **khung trong slide của thầy**, tham khảo cách trình bày của N2:

| Chương | Nội dung | Trang dự kiến |
|---|---|---|
| **1. Tổng quan** | Lý do hình thành đề tài (dùng mục 0) · Mục tiêu · Nội dung thực hiện · Phạm vi (HR tại cấp cửa hàng, 2 cửa hàng demo, không gồm tính lương) · Phương pháp · **Kết quả dự kiến** · **Kế hoạch thực hiện** (Gantt 10 tuần, N2 không có phần này) | 5–7 |
| **2. Cơ sở lý thuyết** | ERP, HRM/HRIS, BPMN 2.0, Odoo (kiến trúc, ORM, cấu trúc module), workforce scheduling, các KPI %COL/Productivity/Time-to-hire/Turnover. **Có trích dẫn tài liệu** (N2 làm phần này sơ sài) | 6–8 |
| **3. Tổng quan doanh nghiệp** | The Pizza Company, mô hình cửa hàng, cơ cấu nhân sự, các chỉ tiêu được giao (doanh thu, complaint, audit 90%) | 3–4 |
| **4. Phân tích nghiệp vụ & Thiết kế hệ thống** | Thu thập yêu cầu · phân tích dữ liệu (§4) · 4 AS-IS · bảng Problem · 4 TO-BE · bảng Value · yêu cầu chức năng/phi chức năng · Stakeholder · Use case + đặc tả · **Logical** (Class/ERD) · **Physical** (model Odoo, phân quyền, kiến trúc) | 20–25 |
| **5. Triển khai Odoo** | Cài đặt · cấu hình từng module · **Add-on module** (thiết kế, đoạn code chính, giao diện) · tích hợp Power BI | 20–25 |
| **6. Kết quả, Thảo luận & Đánh giá** | Demo các quy trình · **mô phỏng tháng 8 (trước/sau)** · nhận xét của doanh nghiệp · so sánh AS-IS và TO-BE theo KPI | 5–8 |
| **7. Kết luận** | Kết quả · Hạn chế (trung thực) · Hướng phát triển (tính lương, kết nối POS thật, dự báo bằng ML) | 2–3 |
| **Phụ lục** | Câu hỏi PV, biên bản PV, link video, phiếu khảo sát, phiếu nhận xét của DN, link GitHub, hướng dẫn cài đặt | — |

**Checklist chỉn chu:** mục lục và danh mục hình/bảng tự động · đánh số hình "Hình 4.x" thống nhất · font Times New Roman 13, giãn dòng 1.3–1.5 · soát chính tả (N2 còn lỗi) · ảnh chụp rõ, cắt gọn, có chú thích · sơ đồ BPMN xuất ảnh độ phân giải cao.

---

## 12. Thuyết trình (Tuần 10)
- 15–20 slide, khoảng 15 phút: Vấn đề (số 41 triệu/tháng mở đầu) → AS-IS → TO-BE → Kiến trúc → **Demo trực tiếp** (có clip dự phòng) → Kết quả mô phỏng → Nhận xét DN → Hạn chế.
- Mỗi thành viên trình bày đúng phần mình làm (thầy chấm % đóng góp).
- Chuẩn bị trước các câu hỏi dễ bị hỏi: "Số người tối thiểu lấy ở đâu?", "Vì sao không dùng Planning của Odoo?", "Dữ liệu demo là thật hay giả?", "AI hỗ trợ đến đâu?".

---

## 13. Phân công (gợi ý cho 5 người)

| Vai trò | Phụ trách chính | Hỗ trợ |
|---|---|---|
| **TV1 – Nhóm trưởng / BA** | Liên hệ DN, phỏng vấn, Chương 1, 3; phiếu xác nhận DN; tổng hợp báo cáo; đánh giá % | Bảng Problem/Value |
| **TV2 – BA / BPMN** | 8 sơ đồ BPMN, Chương 4 phần nghiệp vụ, use case + đặc tả | Kịch bản demo |
| **TV3 – Data / BI** | Phân tích Excel (§4), mô phỏng tháng 8, Power BI, Chương 6 | Dữ liệu demo |
| **TV4 – Odoo Functional** | Cài Docker, cấu hình Employees/Recruitment/Website/eLearning/Attendances/Time Off/Email, Chương 5 phần cấu hình | Deploy server |
| **TV5 – Odoo Developer** | Add-on `tpc_labour_planning`, thiết kế Logical/Physical, Chương 5 phần add-on | Cron, báo cáo PDF |
| Cả nhóm | Chương 2 (chia nhau), slide, quay clip, tập thuyết trình | — |

---

## 14. Lịch 10 tuần (bám theo kế hoạch trong slide)

| Tuần | Việc | Đầu ra cần có |
|---|---|---|
| **1** | Chốt đề tài, lập nhóm, gửi câu hỏi cho quản lý; cài Odoo Docker; tạo GitHub + Drive chung | Odoo chạy được ở máy; danh sách câu hỏi |
| **2** | **Phỏng vấn chính thức** (ghi âm/quay), xin biểu mẫu; khảo sát Google Form; học Odoo HR | Biên bản PV, file ghi âm, form khảo sát |
| **3** | Vẽ 4 AS-IS, bảng Problem; phân tích Excel; cài các module HR | 4 sơ đồ AS-IS, bảng phân tích số liệu |
| **4** | Vẽ 4 TO-BE, bảng Value, yêu cầu, use case, ERD; cấu hình Recruitment + Employees | Bản thiết kế Logical/Physical v1 |
| **5** | Code add-on (model + view + tính giờ); cấu hình eLearning/Survey, Attendances | Add-on cài được, tính giờ đề xuất |
| **6** | **Báo cáo giữa kỳ**: slide + demo MVP; deploy server | Slide giữa kỳ, link demo |
| **7** | Sửa theo góp ý của thầy; add-on: xếp ca, skill, báo cáo ngày %COL | Luồng P3, P4 chạy được |
| **8** | Nâng cao: đề xuất ca tự động, cron, email, import Excel; Power BI; mô phỏng tháng 8 | Dashboard, bảng trước/sau |
| **9** | **Demo cho doanh nghiệp, lấy phiếu nhận xét**; quay clip; hoàn thiện báo cáo | Phiếu xác nhận, clip, báo cáo bản nháp |
| **10** | Soát báo cáo, nộp; tập thuyết trình; **Báo cáo cuối kỳ** | Báo cáo PDF, slide, clip, source code |

---

## 15. Minh chứng nỗ lực (slide thầy ghi "AI???")
Thầy có hỏi về AI, nên nhóm cần **chứng minh tự làm**:
- Biên bản họp nhóm hằng tuần (ngày, người tham gia, việc đã làm, việc tuần sau) → đưa vào phụ lục.
- Lịch sử commit GitHub theo từng thành viên.
- Ảnh chụp màn hình có ngày tháng theo tiến độ.
- File ghi âm phỏng vấn gốc và các bản nháp sơ đồ qua từng phiên bản.
- Báo cáo **viết bằng lời của nhóm**, số liệu nào cũng có nguồn. Nếu có dùng AI để hỗ trợ (dịch, gợi ý code) thì ghi rõ phạm vi sử dụng, để khi thầy hỏi thì trả lời thẳng thắn.

---

## 16. Rủi ro và cách xử lý
| Rủi ro | Cách xử lý |
|---|---|
| Quản lý không cung cấp thêm dữ liệu xếp ca/nghỉ việc | Dùng dữ liệu sẵn có (`Store Perfomance` đã đủ cho phần COL), số liệu khác thì nêu rõ là giả định và hỏi quản lý xác nhận mức hợp lý |
| Code add-on không kịp | Giữ chắc phần MVP §8.3 trước tuần 7; phần mở rộng là điểm cộng |
| Module Enterprise không có | Đã thiết kế để chỉ dùng Community + add-on tự viết |
| Server demo lỗi khi thuyết trình | Có clip dự phòng và Odoo chạy local |
| Lộ dữ liệu cá nhân | Dùng tên giả, che SĐT; không công khai repo nếu có dữ liệu thật |
