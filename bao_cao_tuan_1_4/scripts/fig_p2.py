"""P2 – Onboarding & đào tạo: AS-IS và TO-BE."""
from bpmn import *

OUT = "../figures/"


def as_is():
    d = Diagram(1380)
    d.pool("THE PIZZA COMPANY – CỬA HÀNG", [("ql", "Quản lý\ncửa hàng", 120),
                                            ("tr", "Trainer /\nQuản lý ca", 120),
                                            ("nv", "Nhân viên mới", 145)])
    d.event("s", 85, "ql", "start", "message", "Có mã NV")
    d.task("t1", 185, "ql", "Phân quầy, giao\ntraining plan 2 tuần", "manual")
    d.data("do1", 300, d.at("ql", -8), "Training plan\n(giấy)")
    d.task("t2", 300, "tr", "Hướng dẫn tại quầy\ntheo từng ngày", "manual", loop=True)
    d.task("t3", 420, "nv", "Học & thực hành\ntại quầy", "manual", loop=True)
    d.gateway("g1", 525, "nv", "x", "Tiếp tục\nlàm?", lpos="t")
    d.event("x1", 525, "nv", "end", label="Nghỉ việc giữa\nđào tạo", dy=50, lpos="l")
    d.task("t4", 630, "nv", "Làm bài test\n(giấy)", "manual")
    d.task("t5", 745, "tr", "Chấm bài test", "manual")
    d.gateway("g2", 850, "tr", "x", "Đạt?", lpos="r")
    d.task("t6", 960, "ql", "Ghi nhận kết quả\nvào sổ / Excel", "manual", fill=PAIN_FILL)
    d.store("ds1", 1060, d.at("ql", 22), "Sổ tay /\nExcel rời")
    d.task("t7", 1160, "ql", "Xếp NV vào ca\ntại quầy đã học", "manual")
    d.event("e9", 1290, "ql", "end", label="NV làm\nchính thức")
    d.note("n1", 740, d.lane_edge("ql", "top") + 6,
           "Tiến độ mỗi NV khác nhau (1 buổi → 2 tuần) nhưng\nkhông có nơi theo dõi tập trung → QL không biết ai\nđang học tới đâu, ai đã làm được quầy nào", w=245)
    d.note("n2", 575, d.at("nv", 34), "\"Các bạn độ chịu cực không tốt\"\n→ nghỉ ngay trong lúc đào tạo", w=170)
    d.flow("s", "t1"); d.flow("t1", "t2", route="vh"); d.flow("t2", "t3", route="hvh")
    d.flow("t3", "g1")
    d.flow("g1", "x1", route="v", label="Không", lab_dx=3, lab_dy=14)
    d.flow("g1", "t4", label="Có")
    d.flow("t4", "t5", route="hvh"); d.flow("t5", "g2")
    d.flow("g2", "t2", via=[(850, d.at("tr", 48)), (300, d.at("tr", 48))], src="b", dst="b",
           label="Không – học lại", lab_at=1, lab_dx=-130, lab_dy=-2)
    d.flow("g2", "t6", route="vh", label="Có", lab_at=1, lab_dx=8, lab_dy=-2)
    d.flow("t6", "t7"); d.flow("t7", "e9")
    d.assoc("t1", "do1", route="h")
    d.assoc("t6", "ds1", via=[(1060, d.at("ql", 0))], src="r", dst="t")
    d.point("n1b", 960, d.lane_edge("ql", "top") + 6 + 46)
    d.assoc("t6", "n1b", via=[], src="t", dst="t")
    d.point("n2l", 575, d.at("nv", 50))
    d.assoc("x1", "n2l", via=[], src="r", dst="t")
    d.save(OUT + "p2_asis.pdf"); d.save(OUT + "p2_asis.png")


def to_be():
    d = Diagram(1480)
    d.pool("THE PIZZA COMPANY – CỬA HÀNG", [("ql", "Quản lý\ncửa hàng", 105),
                                            ("sys", "Hệ thống Odoo\n(eLearning, Skills)", 135),
                                            ("tr", "Trainer /\nQuản lý ca", 105),
                                            ("nv", "Nhân viên mới", 110)])
    d.event("s", 85, "sys", "start", "conditional", "Hồ sơ NV\nđược tạo (P1)")
    d.task("t1", 185, "sys", "Sinh kế hoạch\nonboarding", "service", fill=SYS_FILL)
    d.task("t2", 305, "sys", "Ghi danh khóa\neLearning theo quầy", "service", fill=SYS_FILL)
    d.gateway("g1", 400, "sys", "+")
    d.task("t3", 500, "nv", "Học bài & video\ntrên điện thoại", "user", loop=True)
    d.task("t4", 500, "tr", "Kèm thực hành,\ntick checklist", "user", loop=True)
    d.gateway("g2", 600, "sys", "+")
    d.task("t5", 700, "nv", "Làm bài test\n(Quiz/Survey)", "user")
    d.task("t6", 815, "sys", "Chấm điểm\ntự động", "service", fill=SYS_FILL)
    d.gateway("g3", 915, "sys", "x", "Điểm ≥ 80%?", lpos="t")
    d.task("t7", 915, "nv", "Ôn lại phần\nchưa đạt", "user", dy=0)
    d.task("t8", 1025, "sys", "Cập nhật Skill\n\"Đạt quầy X\"", "service", fill=SYS_FILL)
    d.task("t9", 1140, "sys", "Thông báo QL:\nNV đủ điều kiện", "send", fill=SYS_FILL)
    d.task("t10", 1260, "ql", "Xem dashboard đào\ntạo, xếp vào ca", "user")
    d.event("e9", 1400, "ql", "end", label="NV làm\nchính thức")
    d.store("ds", 1025, d.at("tr", 0), "Hồ sơ kỹ năng\n(hr.skill)")
    d.note("n1", 160, d.lane_edge("ql", "top") + 12,
           "Tiến độ từng NV hiển thị theo thời gian thực:\n% hoàn thành khóa, điểm test, số ngày còn lại", w=230)
    d.note("n2", 1180, d.at("tr", -30),
           "Automation: quá 14 ngày chưa đạt\n→ nhắc Trainer và QLCH", w=170)
    d.flow("s", "t1"); d.flow("t1", "t2"); d.flow("t2", "g1")
    d.flow("g1", "t3", route="vh"); d.flow("g1", "t4", route="vh")
    d.flow("t3", "g2", route="hv"); d.flow("t4", "g2", route="hv")
    d.flow("g2", "t5", route="vh"); d.flow("t5", "t6", route="hv", dst="b")
    d.flow("t6", "g3")
    d.flow("g3", "t7", route="v", label="Không", lab_at=0, lab_dx=3, lab_dy=40)
    d.flow("t7", "t5", via=[(915, d.at("nv", 44)), (700, d.at("nv", 44))], src="b", dst="b")
    d.flow("g3", "t8", label="Có"); d.flow("t8", "t9")
    d.flow("t9", "t10", route="hv", dst="b"); d.flow("t10", "e9")
    d.assoc("t8", "ds", route="v")
    d.point("n1b", 305, d.lane_edge("ql", "top") + 12 + 36)
    d.assoc("t2", "n1b", via=[], src="t", dst="t")
    d.point("n2l", 1180, d.at("tr", -16))
    d.assoc("t9", "n2l", via=[(1140, d.at("tr", -16))], src="b", dst="t")
    d.save(OUT + "p2_tobe.pdf"); d.save(OUT + "p2_tobe.png")


if __name__ == "__main__":
    as_is(); to_be()
