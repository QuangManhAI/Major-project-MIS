"""P4 – Chấm công, báo cáo cuối ngày & theo dõi %COL: AS-IS và TO-BE. Kèm sơ đồ tổng thể."""
from bpmn import *

OUT = "../figures/"


def as_is():
    d = Diagram(1460)
    d.pool("THE PIZZA COMPANY", [("nv", "Nhân viên", 95),
                                 ("ql", "Quản lý ca /\nQuản lý cửa hàng", 230),
                                 ("kv", "Quản lý\nkhu vực", 120)])
    d.event("s", 85, "nv", "start", label="Vào ca")
    d.task("t0", 185, "nv", "Chấm công\nvào / ra", "manual")
    d.event("e0", 290, "nv", "end", label="Hết ca")
    d.event("s1", 85, "ql", "start", "timer", "22:00\nđóng cửa")
    d.task("t1", 185, "ql", "Đóng ca\ntrên POS", "user")
    d.gateway("g1", 280, "ql", "+")
    d.task("a1", 400, "ql", "Lập BC doanh thu\n(Excel)", "manual", dy=-80, h=40, w=132, fill=PAIN_FILL)
    d.task("a2", 400, "ql", "Lập BC tài chính\n(Excel)", "manual", dy=-28, h=40, w=132, fill=PAIN_FILL)
    d.task("a3", 400, "ql", "Ghi giờ công thực tế\nvào file (giả định)", "manual", dy=24, h=40, w=132, fill=PAIN_FILL)
    d.task("a4", 400, "ql", "Nhập tồn hàng\nlên SAP", "user", dy=76, h=40, w=132)
    d.gateway("g2", 520, "ql", "+")
    d.task("t2", 620, "ql", "Gửi email\nbáo cáo", "send")
    d.store("ds", 520, d.at("kv", 10), "File Excel\nmáy cửa hàng")
    d.event("e2", 720, "ql", "end")
    d.event("s3", 620, "kv", "start", "message", "Nhận email", lpos="b", dy=-10)
    d.task("t3", 720, "kv", "Đối chiếu với\nreport hệ thống", "manual", dy=-10)
    d.gateway("g3", 820, "kv", "x", "Lệch số?", lpos="t", dy=-10)
    d.task("t4", 920, "kv", "Gọi hỏi cửa hàng,\nyêu cầu sửa", "manual", dy=-10)
    d.gateway("g4", 1020, "kv", "x", dy=-10)
    d.event("i1", 1100, "kv", "inter", "timer", "Cuối tháng", dy=-10, lpos="t")
    d.task("t5", 1210, "kv", "Tổng hợp giờ công,\n%COL tháng", "manual", dy=-10, fill=PAIN_FILL)
    d.event("e9", 1330, "kv", "end", label="Thấy thừa giờ\n(quá muộn)", dy=-10, lpos="b")
    d.note("n1", 640, d.at("ql", -95),
           "~30 phút mỗi tối, 3–4 file rời;\ntrễ khi mất mạng / POS lỗi\n(theo phỏng vấn QL khu vực)", w=175)
    d.note("n2", 1080, d.lane_edge("ql", "top") + 70,
           "T8/2026: thực tế 5.882 giờ so với định mức\n4.863 giờ → thừa ~1.018 giờ ≈ 41 triệu đ;\n%COL 15,5% so với mục tiêu 13,65%.\nChỉ lộ ra khi tổng hợp cuối tháng.", w=230)
    d.flow("s", "t0"); d.flow("t0", "e0")
    d.flow("s1", "t1"); d.flow("t1", "g1")
    for k in ("a1", "a2", "a3", "a4"):
        d.flow("g1", k, route="vh"); d.flow(k, "g2", route="hv")
    d.flow("g2", "t2"); d.flow("t2", "e2")
    d.msg("t2", "s3", route="v")
    d.flow("s3", "t3"); d.flow("t3", "g3")
    d.flow("g3", "t4", label="Có"); d.flow("t4", "g4")
    d.flow("g3", "g4", via=[(820, d.at("kv", 38)), (1020, d.at("kv", 38))], src="b", dst="b",
           label="Không", lab_at=1, lab_dx=8, lab_dy=-2)
    d.flow("g4", "i1"); d.flow("i1", "t5"); d.flow("t5", "e9")
    d.assoc("a3", "ds", via=[(470, d.at("ql", 24)), (470, d.at("kv", 10))], src="r", dst="l")
    d.point("n1b", 640, d.at("ql", -95) + 21)
    d.assoc("t2", "n1b", via=[(620, d.at("ql", -74))], src="t", dst="t")
    d.point("n2b", 1210, d.lane_edge("ql", "top") + 70 + 62)
    d.assoc("t5", "n2b", route="v")
    d.save(OUT + "p4_asis.pdf"); d.save(OUT + "p4_asis.png")


def to_be():
    d = Diagram(1460)
    d.pool("THE PIZZA COMPANY", [("nv", "Nhân viên", 95),
                                 ("ql", "Quản lý cửa hàng", 105),
                                 ("sys", "Hệ thống Odoo\n(Attendances, add-on)", 150),
                                 ("kv", "Quản lý\nkhu vực", 105)])
    d.event("s", 85, "nv", "start", label="Vào ca")
    d.task("t0", 185, "nv", "Check-in / out\ntại Kiosk (PIN)", "user")
    d.task("t1", 305, "sys", "Ghi nhận giờ công\n(hr.attendance)", "service", fill=SYS_FILL, dy=-35)
    d.event("e0", 410, "sys", "end", label="Giờ công\nđã lưu", dy=-35, lpos="r")
    d.store("ds", 410, d.at("sys", 42), "Chấm công")
    d.event("s2", 85, "ql", "start", "timer", "22:00\nđóng ca")
    d.task("t2", 560, "ql", "Đóng ca POS, import\ndoanh thu ngày", "user")
    d.task("t3", 680, "sys", "Tính Actual WH, %COL,\nProductivity ngày", "service", fill=SYS_FILL, w=125)
    d.gateway("g1", 790, "sys", "x", "%COL > ngưỡng?", lpos="b")
    d.task("t4", 900, "sys", "Gửi cảnh báo\nQLCH & QLKV", "send", fill=SYS_FILL, dy=-38, h=48)
    d.task("t5", 1020, "kv", "Xem nguyên nhân,\nyêu cầu chỉnh ca", "user")
    d.task("t6", 1020, "ql", "Giảm/điều ca\nngày tiếp theo (P3)", "user", sub=True)
    d.gateway("g2", 1130, "sys", "x")
    d.task("t7", 1250, "sys", "Cập nhật dashboard\nMTD theo cửa hàng", "service", fill=SYS_FILL)
    d.event("e9", 1370, "sys", "end", label="Báo cáo ngày\nhoàn tất")
    d.note("n1", 1160, d.lane_edge("ql", "top") + 8,
           "Không còn file Excel báo cáo ca:\nsố liệu %COL có ngay trong đêm,\nQLKV xem cùng 1 dashboard", w=180)
    d.flow("s", "t0"); d.flow("t0", "t1", route="hv")
    d.flow("t1", "e0")
    d.flow("s2", "t2"); d.flow("t2", "t3", route="hv")
    d.flow("t3", "g1")
    d.flow("g1", "t4", route="vh", label="Có", lab_dx=4, lab_dy=-4)
    d.flow("g1", "g2", label="Không", lab_dx=6, lab_dy=-3)
    d.flow("t4", "t5", via=[(960, d.at("sys", -38)), (960, d.at("kv", 0))], src="r", dst="l")
    d.flow("t5", "t6", route="v")
    d.flow("t6", "g2", route="hv")
    d.flow("g2", "t7"); d.flow("t7", "e9")
    d.assoc("ds", "t3", via=[(560, d.at("sys", 42)), (560, d.at("sys", 0))], src="r", dst="l")
    d.point("n1b", 1250, d.lane_edge("ql", "top") + 8 + 49)
    d.assoc("t7", "n1b", route="v")
    d.save(OUT + "p4_tobe.pdf"); d.save(OUT + "p4_tobe.png")


def overview():
    d = Diagram(1300)
    d.pool("THE PIZZA COMPANY", [("a", "Cửa hàng", 170)])
    d.event("s", 90, "a", "start", label="Phát sinh nhu cầu\nnhân sự", dy=-10)
    d.task("p1", 220, "a", "P1. Tuyển dụng", sub=True, dy=-10, w=130)
    d.task("p2", 400, "a", "P2. Onboarding\n& đào tạo", sub=True, dy=-10, w=130)
    d.task("p3", 580, "a", "P3. Xếp ca\n(hằng tuần)", sub=True, loop=True, dy=-10, w=130)
    d.task("p4", 760, "a", "P4. Chấm công\n& theo dõi %COL", sub=True, loop=True, dy=-10, w=130)
    d.gateway("g", 900, "a", "x", "Thiếu người /\nNV nghỉ việc?", lpos="t", dy=-10)
    d.gateway("g2", 1020, "a", "x", "Hết kỳ\nphân tích?", lpos="t", dy=-10)
    d.event("e", 1130, "a", "end", label="Báo cáo nhân sự\n& %COL tháng", dy=-10)
    d.flow("s", "p1"); d.flow("p1", "p2"); d.flow("p2", "p3"); d.flow("p3", "p4"); d.flow("p4", "g")
    d.flow("g", "p1", via=[(900, d.at("a", 62)), (220, d.at("a", 62))], src="b", dst="b",
           label="Có – tuyển bù", lab_at=1, lab_dx=-330, lab_dy=-2)
    d.flow("g", "g2", label="Không")
    d.flow("g2", "p3", via=[(1020, d.at("a", 40)), (580, d.at("a", 40))], src="b", dst="b",
           label="Chưa – tuần tiếp theo", lab_at=1, lab_dx=-220, lab_dy=-2)
    d.flow("g2", "e", label="Rồi")
    d.save(OUT + "overview.pdf"); d.save(OUT + "overview.png")


if __name__ == "__main__":
    as_is(); to_be(); overview()
