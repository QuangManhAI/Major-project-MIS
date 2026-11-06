"""P1 – Quy trình tuyển dụng: AS-IS và TO-BE."""
from bpmn import *

OUT = "../figures/"


def as_is():
    d = Diagram(1430)
    d.pool("ỨNG VIÊN")
    d.pool("THE PIZZA COMPANY", [("ql", "Quản lý cửa hàng\n(RGM)", 190),
                                 ("ns", "Phòng Nhân sự –\nTuyển dụng", 120)])
    L = "ql"
    d.event("s", 85, L, "start", label="Thiếu\nnhân sự")
    d.task("t1", 180, L, "Xác định nhu cầu\n(số người, ca, quầy)", "manual")
    d.gateway("g1", 280, L, "x", "Cần phòng\nTD hỗ trợ?", lpos="bl")
    d.task("t2", 385, L, "Dán standee,\nđăng fanpage CH", "manual", dy=-50)
    d.task("t3", 385, "ns", "Đăng tin, lọc data\nứng viên, gửi CH", "user")
    d.gateway("g2", 480, L, "x")
    d.event("e1", 548, L, "inter", "message", "Ứng viên hỏi\n(trực tiếp/inbox)")
    d.task("t4", 640, L, "Hẹn lịch PV\n(VD: T2, T5 10–12h)", "manual")
    d.task("t5", 760, L, "Phỏng vấn chung,\nchọn quầy phù hợp", "manual")
    d.gateway("g3", 860, L, "x", "Đạt?")
    d.event("x1", 860, L, "end", label="Từ chối", dy=68, lpos="r")
    d.task("t6", 960, L, "Kiểm tra / hướng dẫn\nmở TK Techcombank", "manual")
    d.task("t7", 1075, L, "Điền link thông tin\n+ phiếu hồ sơ giấy", "manual")
    d.task("t8", 1190, L, "Mang hồ sơ giấy\nlên văn phòng", "manual", fill=PAIN_FILL)
    d.task("t9", 1190, "ns", "Nhận hồ sơ,\nnhập liệu lại", "manual", fill=PAIN_FILL)
    d.task("t10", 1305, "ns", "Cấp mã\nnhân viên", "user")
    d.task("t11", 1305, L, "Báo ngày\nđi làm", "send")
    d.event("e9", 1395, L, "end", label="NV vào ca\nđầu tiên")
    d.data("do1", 1133, d.at(L, 64), "Hồ sơ giấy")
    d.store("ds1", 1075, d.at("ns", 0), "Link form /\nExcel")
    d.note("n1", 545, d.at(L, 42),
           "Ứng viên đến từ 3 nguồn rời rạc (standee,\nfanpage, data phòng TD) – không có danh\nsách tập trung, dễ sót, không đo được nguồn", w=215)
    d.note("n2", 985, d.lane_edge(L, "top") + 6,
           "Mất 2–4 ngày từ PV đến khi có mã NV\n(PV thứ Hai → nộp hồ sơ thứ Ba → có mã\nthứ Tư → đi làm thứ Năm)", w=205)
    d.note("n3", 470, d.at("ns", -22), "Phụ thuộc lịch QL lên văn phòng;\nthông tin nhập 2 lần (link + giấy)", w=180)
    # pool hộp đen
    for k, x in (("c2", 385), ("c1", 548), ("c4", 640), ("c11", 1305)):
        d.pool_edge(k, x, "ỨNG VIÊN")
    # sequence flows
    d.flow("s", "t1"); d.flow("t1", "g1")
    d.flow("g1", "t2", route="vh", label="Không", lab_at=1, lab_dx=8, lab_dy=-2)
    d.flow("g1", "t3", route="vh", label="Có", lab_at=1, lab_dx=8, lab_dy=-2)
    d.flow("t2", "g2", route="hv"); d.flow("t3", "g2", route="hv")
    d.flow("g2", "e1"); d.flow("e1", "t4"); d.flow("t4", "t5"); d.flow("t5", "g3")
    d.flow("g3", "x1", route="v", label="Không", lab_dx=3, lab_dy=12)
    d.flow("g3", "t6", label="Có", lab_dx=4)
    d.flow("t6", "t7"); d.flow("t7", "t8")
    d.flow("t8", "t9", route="v"); d.flow("t9", "t10")
    d.flow("t10", "t11", route="v"); d.flow("t11", "e9")
    # message flows
    d.msg("t2", "c2", label="Tin tuyển dụng", lab_dx=4, lab_dy=-2)
    d.msg("c1", "e1", label="Liên hệ", lab_dx=5, lab_dy=22)
    d.msg("t4", "c4", label="Lịch hẹn PV", lab_dx=4, lab_dy=-2)
    d.msg("t11", "c11", label="Mã NV, lịch ca", lab_dx=4, lab_dy=-2)
    # data
    d.assoc("t7", "do1", via=[(1110, d.at(L, 29))], src="b", dst="t")
    d.assoc("do1", "t8", via=[(1160, d.at(L, 64))], src="r", dst="b")
    d.assoc("t7", "ds1", route="v")
    d.assoc("t9", "ds1", route="h")
    d.assoc("g2", "n1", via=[(480, d.at(L, 62))], src="b", dst="l")
    d.point("n2b", 1190, d.lane_edge(L, "top") + 6 + 49)
    d.assoc("t8", "n2b", route="v")
    d.assoc("t3", "n3", route="h")
    d.save(OUT + "p1_asis.pdf"); d.save(OUT + "p1_asis.png")
    return d


def to_be():
    d = Diagram(1480)
    d.pool("ỨNG VIÊN")
    d.pool("THE PIZZA COMPANY", [("ql", "Quản lý cửa hàng\n(RGM)", 135),
                                 ("sys", "Hệ thống Odoo\n(Recruitment, Website)", 150),
                                 ("ns", "Phòng Nhân sự –\nTuyển dụng", 105)])
    d.event("s", 85, "ql", "start", label="Thiếu nhân sự")
    d.task("t1", 180, "ql", "Mở tin tuyển dụng\n(Job Position)", "user")
    d.task("t2", 300, "sys", "Đăng tin lên trang\nJobs (website)", "service", fill=SYS_FILL)
    d.event("e1", 410, "sys", "inter", "message", "Nhận đơn online", dy=-30, lpos="t")
    d.event("s2", 300, "ns", "start", "message", "Có data ứng viên\ntừ nguồn khác", lpos="b")
    d.task("t3", 410, "ns", "Nhập/import ứng\nviên vào pipeline", "user")
    d.gateway("g1", 495, "sys", "x")
    d.task("t4", 595, "sys", "Tạo hồ sơ ứng viên,\ngắn nguồn (UTM)", "service", fill=SYS_FILL)
    d.task("t5", 715, "sys", "Gửi email xác nhận\n+ lời mời PV", "send", fill=SYS_FILL)
    d.task("t6", 830, "ql", "Phỏng vấn, đánh giá\ntrên Odoo", "user")
    d.gateway("g2", 925, "ql", "x", "Đạt?")
    d.task("t7", 925, "sys", "Gửi email\ntừ chối (mẫu)", "send", fill=SYS_FILL, dy=35)
    d.event("x1", 1010, "sys", "end", dy=35, label="Ứng viên\nbị loại", lpos="r")
    d.task("t8", 1030, "ql", "Chọn quầy, gửi\nđề nghị (Offer)", "user")
    d.task("t9", 1145, "sys", "Tạo hồ sơ nhân viên\ntừ ứng viên", "service", fill=SYS_FILL, dy=-25)
    d.task("t10", 1255, "ns", "Duyệt hồ sơ, cấp\nmã NV trên Odoo", "user")
    d.task("t11", 1360, "sys", "Email chào mừng\n+ lịch ca đầu tiên", "send", fill=SYS_FILL, dy=-25)
    d.event("e9", 1445, "sys", "end", label="NV sẵn sàng\nvào ca", dy=-25)
    d.store("db", 595, d.at("sys", 50), "CSDL Odoo\n(hr.applicant)")
    for k, x in (("c2", 300), ("c1", 410), ("c5", 715), ("c11", 1360)):
        d.pool_edge(k, x, "ỨNG VIÊN")
    top = d.lane_edge("ql", "top")
    d.note("n1", 1100, top + 8,
           "Không còn hồ sơ giấy: thông tin ứng viên\nđã có sẵn → cấp mã trong ngày\n(mục tiêu: 1–2 ngày từ PV đến ca đầu tiên)", w=215)
    d.point("n1l", 1100, top + 8 + 24)
    d.note("n2", 472, top + 8, "Automation: ứng viên ở giai đoạn 'Mới'\nquá 48h chưa xử lý → nhắc QLCH", w=190)
    d.point("n2b", 595, top + 8 + 36)
    d.flow("s", "t1"); d.flow("t1", "t2", route="hvh")
    d.flow("t2", "e1", route="hv", dst="l")
    d.flow("e1", "g1", route="hv")
    d.flow("s2", "t3", route="h"); d.flow("t3", "g1", route="hv")
    d.flow("g1", "t4"); d.flow("t4", "t5"); d.flow("t5", "t6", route="hv", dst="b")
    d.flow("t6", "g2")
    d.flow("g2", "t7", route="v", label="Không", lab_dx=3, lab_dy=30)
    d.flow("t7", "x1")
    d.flow("g2", "t8", label="Có")
    d.flow("t8", "t9", route="vh"); d.flow("t9", "t10", route="hv")
    d.flow("t10", "t11", route="hv"); d.flow("t11", "e9")
    d.msg("t2", "c2", label="Tin tuyển dụng", lab_dx=4, lab_dy=-60)
    d.msg("c1", "e1", label="Nộp đơn", lab_dx=4, lab_dy=40)
    d.msg("t5", "c5", label="Email mời PV", lab_dx=4, lab_dy=-60)
    d.msg("t11", "c11", label="Mã NV, lịch ca", lab_dx=4, lab_dy=-30)
    d.assoc("t4", "db", route="v")
    d.assoc("t4", "n2b", via=[], src="t", dst="t")
    d.assoc("t8", "n1l", via=[(1030, top + 8 + 24)], src="t", dst="t")
    d.save(OUT + "p1_tobe.pdf"); d.save(OUT + "p1_tobe.png")


if __name__ == "__main__":
    as_is(); to_be()
