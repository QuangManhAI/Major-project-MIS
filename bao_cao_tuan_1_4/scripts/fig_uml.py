"""Use case diagram, class diagram (logical), kiến trúc triển khai (physical), Gantt."""
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, FancyBboxPatch, Rectangle, Circle, Polygon

plt.rcParams["font.family"] = ["Arial", "DejaVu Sans"]
plt.rcParams["pdf.fonttype"] = 42
INK, MUTED = "#1f2328", "#57606a"
OUT = "../figures/"


def canvas(w, h, scale=0.0105):
    fig = plt.figure(figsize=(w * scale, h * scale))
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, w); ax.set_ylim(h, 0); ax.axis("off")
    return fig, ax


def save(fig, name):
    fig.savefig(OUT + name + ".pdf", bbox_inches="tight", pad_inches=0.04)
    fig.savefig(OUT + name + ".png", bbox_inches="tight", pad_inches=0.04, dpi=200)
    plt.close(fig)


def arrow(ax, p, q, ls="-", head="filled", color=INK, lw=0.9, label=None, z=1):
    ax.plot([p[0], q[0]], [p[1], q[1]], color=color, lw=lw, ls=ls, zorder=z)
    if head:
        ang = math.atan2(q[1] - p[1], q[0] - p[0]); L, W = 8, 3.8
        bx, by = q[0] - L * math.cos(ang), q[1] - L * math.sin(ang)
        nx, ny = -math.sin(ang) * W, math.cos(ang) * W
        if head == "open":
            ax.plot([bx + nx, q[0], bx - nx], [by + ny, q[1], by - ny], color=color, lw=lw, zorder=z)
        else:
            ax.add_patch(Polygon([q, (bx + nx, by + ny), (bx - nx, by - ny)], fc=color, ec=color, zorder=z))
    if label:
        ax.text((p[0] + q[0]) / 2, (p[1] + q[1]) / 2 - 3, label, fontsize=6.6, ha="center", va="bottom",
                color=MUTED, style="italic", bbox=dict(fc="white", ec="none", pad=0.3), zorder=z + 1)


# ---------------------------------------------------------------- USE CASE
def actor(ax, x, y, name):
    ax.add_patch(Circle((x, y - 26), 7, fc="white", ec=INK, lw=1.0, zorder=3))
    ax.plot([x, x], [y - 19, y + 4], color=INK, lw=1.0, zorder=3)
    ax.plot([x - 13, x + 13], [y - 12, y - 12], color=INK, lw=1.0, zorder=3)
    ax.plot([x - 10, x, x + 10], [y + 20, y + 4, y + 20], color=INK, lw=1.0, zorder=3)
    ax.text(x, y + 24, name, ha="center", va="top", fontsize=7.6, fontweight="bold", zorder=3,
            linespacing=1.05)
    return (x, y - 4)


def use_case():
    W, H = 1250, 900
    fig, ax = canvas(W, H)
    bx0, bx1, by0, by1 = 170, 1080, 20, 885
    ax.add_patch(Rectangle((bx0, by0), bx1 - bx0, by1 - by0, fc="#fbfcfd", ec=INK, lw=1.2, zorder=0.1))
    ax.text((bx0 + bx1) / 2, by0 + 14, "Hệ thống quản lý nhân sự cửa hàng TPC (Odoo 18 + add-on tpc_labour_planning)",
            ha="center", fontsize=8.6, fontweight="bold")
    bands = [("P1. Tuyển dụng", 45, 235), ("P2. Onboarding & đào tạo", 240, 420),
             ("P3. Xếp ca", 425, 660), ("P4. Chấm công & %COL", 665, 880)]
    fills = ["#eef4fb", "#f1f8f1", "#fff8e8", "#fbeff4"]
    for (t, y0, y1), f in zip(bands, fills):
        ax.add_patch(FancyBboxPatch((bx0 + 12, y0), bx1 - bx0 - 24, y1 - y0 - 6,
                                    boxstyle="round,pad=0,rounding_size=8", fc=f, ec="#c9ccd1", lw=0.8, zorder=0.5))
        ax.text(bx0 + 22, y0 + 6, t, fontsize=7.8, fontweight="bold", color=MUTED, va="top")
    UC = {}

    def uc(k, x, y, text, w=170, h=46):
        ax.add_patch(Ellipse((x, y), w, h, fc="white", ec=INK, lw=0.95, zorder=2))
        ax.text(x, y, f"{k}\n{text}", ha="center", va="center", fontsize=6.9, zorder=3, linespacing=1.05)
        UC[k] = (x, y, w, h)

    c1, c2, c3 = 360, 620, 880
    uc("UC01", c2, 100, "Đăng tin tuyển dụng")
    uc("UC02", c1, 175, "Nộp đơn ứng tuyển online")
    uc("UC03", c3, 178, "Quản lý pipeline ứng viên")
    uc("UC04", c2, 178, "Lên lịch & đánh giá\nphỏng vấn")
    uc("UC05", c3, 98, "Tạo hồ sơ NV,\ncấp mã nhân viên")
    uc("UC06", c1, 335, "Học khóa eLearning\ntheo quầy")
    uc("UC07", c1, 387, "Làm bài test quầy")
    uc("UC08", c1, 283, "Xác nhận checklist\nthực hành")
    uc("UC09", c2, 330, "Theo dõi tiến độ\nđào tạo, Skill")
    uc("UC10", c3, 527, "Import Forecast Sales")
    uc("UC11", c2, 540, "Tính giờ công đề xuất")
    uc("UC12", c3, 455, "Đề xuất & duyệt ca")
    uc("UC13", c1, 450, "Khai báo lịch rảnh")
    uc("UC14", c1, 515, "Xem \"Ca của tôi\"")
    uc("UC15", c2, 645, "Yêu cầu / duyệt\nđổi ca")
    uc("UC16", c1, 720, "Chấm công tại Kiosk")
    uc("UC17", c2, 720, "Xem báo cáo %COL,\nProductivity ngày")
    uc("UC18", c2, 800, "Nhận cảnh báo\n%COL vượt ngưỡng")
    uc("UC19", c3, 830, "Cấu hình định mức\ncửa hàng")
    A = {}
    A["uv"] = actor(ax, 70, 140, "Ứng viên")
    A["nv"] = actor(ax, 70, 470, "Nhân viên\n(FT/PT)")
    A["tr"] = actor(ax, 70, 300, "Trainer /\nQuản lý ca")
    A["ql"] = actor(ax, 1170, 500, "Quản lý\ncửa hàng")
    A["ns"] = actor(ax, 1170, 135, "Phòng Nhân sự\n– Tuyển dụng")
    A["kv"] = actor(ax, 1170, 760, "Quản lý\nkhu vực")
    # tổng quát hoá: Trainer là một Nhân viên
    arrow(ax, (70, 340), (70, 410), head=None)
    ax.add_patch(Polygon([(70, 412), (63, 400), (77, 400)], fc="white", ec=INK, lw=0.9, zorder=3))

    def edge(a, u):
        x, y, w, h = UC[u]
        ax_, ay = A[a]
        side = -1 if ax_ < x else 1
        ax.plot([ax_ + (-side) * 16, x + side * w / 2], [ay, y], color=INK, lw=0.7, zorder=1)

    links = {"uv": ["UC02"], "nv": ["UC06", "UC07", "UC13", "UC14", "UC15", "UC16"],
                  "tr": ["UC08"], "ql": ["UC01", "UC03", "UC04", "UC09", "UC10", "UC12", "UC15", "UC17"],
                  "ns": ["UC03", "UC05"], "kv": ["UC17", "UC18", "UC19"]}
    for a, us in links.items():
        for u in us:
            edge(a, u)

    def dep(u1, u2, kind):
        x1, y1, w1, h1 = UC[u1]; x2, y2, w2, h2 = UC[u2]
        ang = math.atan2(y2 - y1, x2 - x1)
        p = (x1 + w1 / 2 * math.cos(ang), y1 + h1 / 2 * math.sin(ang))
        q = (x2 - w2 / 2 * math.cos(ang), y2 - h2 / 2 * math.sin(ang))
        arrow(ax, p, q, ls=(0, (4, 3)), head="open", label=f"«{kind}»", lw=0.8)

    import numpy as np
    for a, us in links.items():
        for u in us:
            ax_, ay = A[a]; x, y, w, h = UC[u]
            for k, (cx, cy, cw, ch) in UC.items():
                if k == u: continue
                for t in np.linspace(0, 1, 200):
                    px, py = ax_ + (x - ax_) * t, ay + (y - ay) * t
                    if ((px - cx) / (cw / 2 + 4)) ** 2 + ((py - cy) / (ch / 2 + 4)) ** 2 < 1:
                        print("CROSS", a, u, "through", k); break
    dep("UC12", "UC11", "include")
    dep("UC11", "UC10", "include")
    dep("UC18", "UC17", "extend")
    dep("UC05", "UC03", "extend")
    save(fig, "usecase")


# ---------------------------------------------------------------- CLASS DIAGRAM
def class_box(ax, x, y, name, attrs, w=180, tag=None, fill="#eef4fb"):
    lh = 11.5
    h = 22 + lh * len(attrs) + 8
    ax.add_patch(Rectangle((x, y), w, h, fc="white", ec=INK, lw=1.0, zorder=2))
    ax.add_patch(Rectangle((x, y), w, 22, fc=fill, ec=INK, lw=1.0, zorder=2.1))
    ax.text(x + w / 2, y + 11, name, ha="center", va="center", fontsize=7.6, fontweight="bold", zorder=3)
    if tag:
        ax.text(x + w - 4, y - 2, tag, ha="right", va="bottom", fontsize=6.2, color=MUTED, style="italic")
    for i, a in enumerate(attrs):
        ax.text(x + 6, y + 22 + 6 + lh * i + lh / 2, a, ha="left", va="center", fontsize=6.6, zorder=3,
                family=["Arial", "DejaVu Sans"])
    return dict(x=x, y=y, w=w, h=h)


def link(ax, A, B, m1, m2, side_a, side_b, label=None, via=None, comp=False):
    def port(c, s, t=0.5):
        return {"r": (c["x"] + c["w"], c["y"] + c["h"] * t), "l": (c["x"], c["y"] + c["h"] * t),
                "t": (c["x"] + c["w"] * t, c["y"]), "b": (c["x"] + c["w"] * t, c["y"] + c["h"])}[s]
    p = port(A, side_a[0], side_a[1]); q = port(B, side_b[0], side_b[1])
    pts = [p] + (via or []) + [q]
    ax.plot([u[0] for u in pts], [u[1] for u in pts], color=INK, lw=0.85, zorder=1)
    if comp:
        ang = math.atan2(pts[1][1] - p[1], pts[1][0] - p[0])
        d = [(p[0] + 7 * math.cos(ang) * k + 4.5 * math.cos(ang + math.pi / 2) * s,
              p[1] + 7 * math.sin(ang) * k + 4.5 * math.sin(ang + math.pi / 2) * s) for k, s in ((0, 0), (1, 1), (2, 0), (1, -1))]
        ax.add_patch(Polygon(d, fc=INK, ec=INK, zorder=1.5))

    def lab(pt, nxt, txt):
        dx, dy = nxt[0] - pt[0], nxt[1] - pt[1]
        n = math.hypot(dx, dy) or 1
        ox, oy = pt[0] + dx / n * 12, pt[1] + dy / n * 12
        ax.text(ox + (5 if abs(dy) > abs(dx) else 0), oy - (0 if abs(dy) > abs(dx) else 4), txt, fontsize=6.6,
                ha="left", va="bottom" if abs(dy) <= abs(dx) else "center", color=INK, zorder=3)
    lab(p, pts[1], m1); lab(q, pts[-2], m2)
    if label:
        mid = pts[len(pts) // 2 - 1], pts[len(pts) // 2]
        mx, my = (mid[0][0] + mid[1][0]) / 2, (mid[0][1] + mid[1][1]) / 2
        ax.text(mx, my - 3, label, fontsize=6.4, color=MUTED, style="italic", ha="center", va="bottom",
                bbox=dict(fc="white", ec="none", pad=0.2), zorder=3)


def class_diagram():
    fig, ax = canvas(1300, 760)
    NEW = "#e3f1e6"
    C = {}
    C["store"] = class_box(ax, 540, 20, "Store (Cửa hàng)", ["code: string", "name: string", "area: string",
                           "productivity_target: money = 330.000", "col_target: % = 13,65",
                           "avg_wage_hour: money = 40.254"], w=200, tag="add-on mở rộng")
    C["station"] = class_box(ax, 120, 20, "Station (Quầy)", ["name: string (Phục vụ, Thu ngân,", "   Make line, Cut & Pack…)",
                             "min_staff_peak: int", "min_staff_offpeak: int"], w=185)
    C["emp"] = class_box(ax, 540, 230, "Employee (Nhân viên)", ["employee_code: string", "name: string",
                         "employment_type: FT | PT", "max_hours_week: float", "bank_tcb_account: string",
                         "training_status: enum"], w=200)
    C["skill"] = class_box(ax, 120, 230, "StationSkill (Đạt quầy)", ["level: Đang học | Đạt", "qualified_date: date",
                           "score: %"], w=185)
    C["job"] = class_box(ax, 960, 20, "JobPosition (Vị trí)", ["name: string", "no_of_recruitment: int",
                         "state: open | closed"], w=185)
    C["app"] = class_box(ax, 960, 175, "Applicant (Ứng viên)", ["name, phone, email", "source: Standee | Fanpage |",
                         "   Phòng TD | Website | Giới thiệu", "stage: Mới → … → Nhận việc",
                         "interview_date: datetime", "has_tcb_account: bool"], w=185)
    C["course"] = class_box(ax, 120, 400, "Course (Khóa đào tạo)", ["name: string", "station_id", "pass_score: % = 80",
                            "duration_days: int = 14"], w=185)
    C["avail"] = class_box(ax, 960, 400, "Availability (Lịch rảnh)", ["date: date", "time_from, time_to: float"],
                           w=185, fill=NEW)
    C["fc"] = class_box(ax, 820, 560, "SalesForecast (Dự báo DT)", ["date: date", "forecast_sales: money",
                        "forecast_tc: int", "actual_sales: money"], w=200, fill=NEW)
    C["tmpl"] = class_box(ax, 120, 590, "ShiftTemplate (Mẫu ca)", ["name: Sáng 7–15h, Chiều 15–22h…",
                          "time_from, time_to: float", "paid_hours: float"], w=200, fill=NEW)
    C["shift"] = class_box(ax, 440, 470, "Shift (Ca làm việc)", ["date: date", "time_from, time_to: float",
                           "hours: float (compute)", "state: Nháp | Đã công bố |", "   Hoàn thành"], w=185, fill=NEW)
    C["att"] = class_box(ax, 660, 400, "Attendance (Chấm công)", ["check_in: datetime", "check_out: datetime",
                         "worked_hours: float"], w=170)
    C["daily"] = class_box(ax, 470, 650, "LabourDaily (Báo cáo ngày)", ["date: date", "required_hours: float",
                           "actual_hours: float", "col_pct, productivity (compute)", "variance_hours (compute)"],
                           w=210, fill=NEW)
    lk = lambda a, b, m1, m2, sa, sb, **k: link(ax, C[a], C[b], m1, m2, sa, sb, **k)
    lk("store", "station", "1", "1..*", ("l", .3), ("r", .3), label="có")
    lk("store", "emp", "1", "0..*", ("b", .5), ("t", .5), label="làm việc tại")
    lk("store", "job", "1", "0..*", ("r", .4), ("l", .4), label="mở")
    lk("job", "app", "1", "0..*", ("b", .5), ("t", .5), label="ứng tuyển")
    lk("app", "emp", "0..1", "0..1", ("l", .4), ("r", .4), label="trở thành")
    lk("emp", "skill", "1", "0..*", ("l", .35), ("r", .35))
    lk("station", "skill", "1", "0..*", ("b", .5), ("t", .5))
    lk("station", "course", "1", "1..*", ("l", .8), ("l", .3), via=[(95, C["station"]["y"] + C["station"]["h"] * .8), (95, C["course"]["y"] + C["course"]["h"] * .3)], label="")
    lk("course", "skill", "1", "0..*", ("t", .5), ("b", .5), label="đạt → cập nhật")
    lk("emp", "avail", "1", "0..*", ("r", .8), ("t", .3), via=[(1015, C["emp"]["y"] + C["emp"]["h"] * .8)])
    lk("emp", "att", "1", "0..*", ("b", .8), ("t", .4), via=[(700, 380)])
    lk("emp", "shift", "0..1", "0..*", ("b", .3), ("t", .5), via=[(600, 390), (532, 390)], label="được xếp")
    lk("station", "shift", "1", "0..*", ("r", .85), ("l", .3), via=[(400, C["station"]["y"] + C["station"]["h"] * .85), (400, C["shift"]["y"] + C["shift"]["h"] * .3)])
    lk("tmpl", "shift", "1", "0..*", ("r", .3), ("l", .7), via=[(380, C["tmpl"]["y"] + C["tmpl"]["h"] * .3), (380, C["shift"]["y"] + C["shift"]["h"] * .7)])
    lk("store", "fc", "1", "0..*", ("r", .85), ("t", .5), via=[(1220, C["store"]["y"] + C["store"]["h"] * .85), (1220, 535), (920, 535)], label="theo ngày")
    lk("fc", "daily", "1", "1", ("l", .7), ("r", .4), via=[(770, C["fc"]["y"] + C["fc"]["h"] * .7), (770, C["daily"]["y"] + C["daily"]["h"] * .4)], label="tính")
    lk("shift", "daily", "0..*", "1", ("b", .5), ("t", .3), label="tổng hợp")
    lk("att", "daily", "0..*", "1", ("b", .5), ("t", .8), via=[(745, 620), (638, 620)])
    # chú giải
    ax.add_patch(Rectangle((1010, 660), 14, 10, fc=NEW, ec=INK, lw=0.7))
    ax.text(1030, 665, "Lớp mới của add-on tpc_labour_planning", fontsize=6.8, va="center")
    ax.add_patch(Rectangle((1010, 680), 14, 10, fc="#eef4fb", ec=INK, lw=0.7))
    ax.text(1030, 685, "Lớp có sẵn trong Odoo (mở rộng field)", fontsize=6.8, va="center")
    save(fig, "class_diagram")


# ---------------------------------------------------------------- ARCHITECTURE
def box(ax, x, y, w, h, title, lines=(), fill="#eef4fb", bold=True, fs=7.4):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=7", fc=fill, ec=INK, lw=1.0, zorder=2))
    ax.text(x + w / 2, y + 12, title, ha="center", va="center", fontsize=fs + 0.4,
            fontweight="bold" if bold else "normal", zorder=3)
    for i, l in enumerate(lines):
        ax.text(x + 8, y + 30 + i * 12.5, l, ha="left", va="center", fontsize=fs - 0.6, zorder=3)


def architecture():
    fig, ax = canvas(1200, 490)
    ax.add_patch(FancyBboxPatch((300, 20), 560, 455, boxstyle="round,pad=0,rounding_size=10", fc="#f6f8fa",
                                ec="#8c959f", lw=1.0, ls=(0, (5, 3))))
    ax.text(312, 34, "Máy chủ (VPS / Railway) – Docker Compose", fontsize=8, fontweight="bold", color=MUTED)
    box(ax, 30, 40, 200, 80, "Người dùng (trình duyệt)", ["• QL cửa hàng, QL khu vực, Phòng NS", "• Back-office Odoo, dashboard"])
    box(ax, 30, 145, 200, 68, "Nhân viên (điện thoại)", ["• Portal: \"Ca của tôi\", eLearning"])
    box(ax, 30, 238, 200, 68, "Kiosk chấm công", ["• Tablet tại cửa hàng (PIN/badge)"])
    box(ax, 30, 331, 200, 68, "Ứng viên (Internet)", ["• Trang Jobs, form ứng tuyển"])
    box(ax, 330, 55, 200, 70, "Nginx (reverse proxy)", ["• HTTPS (Let's Encrypt)", "• tên miền của nhóm"], fill="#fff6dc")
    box(ax, 330, 160, 500, 165, "Container: Odoo 18 Community", [
        "Module có sẵn: hr, hr_recruitment, website_hr_recruitment, hr_skills, hr_attendance,",
        "                     hr_holidays, website_slides, survey, base_automation, mail",
        "Add-on tự viết: tpc_labour_planning",
        "   • models: tpc.sales.forecast, tpc.shift.template, tpc.shift, tpc.labour.daily",
        "   • wizard: import Forecast (xlsx), đề xuất ca tự động",
        "   • cron 23:00: tính %COL ngày, gửi cảnh báo",
        "   • security: nhóm quyền + record rule theo cửa hàng",
        "Thư mục mount: ./addons → /mnt/extra-addons",
    ], fill="#e3f1e6")
    box(ax, 330, 360, 260, 90, "Container: PostgreSQL 16", ["• CSDL tpc_demo", "• volume tpc-db-data (sao lưu hằng ngày)",
                                                             "• user readonly cho Power BI"], fill="#eef4fb")
    box(ax, 925, 40, 250, 105, "Power BI Desktop / Service", ["• Kết nối PostgreSQL (read-only)", "• Dashboard khu vực: %COL,",
                                                               "   Productivity, giờ thừa,", "   tuyển dụng, đào tạo"], fill="#fff6dc")
    box(ax, 925, 185, 250, 70, "Hệ thống hiện có (ngoài phạm vi)", ["• POS bán hàng, SAP kho", "• Chỉ trao đổi qua file xuất"], fill="#f2f3f5")
    box(ax, 925, 295, 250, 85, "Dịch vụ ngoài", ["• Gmail SMTP: email ứng viên, cảnh báo", "• GitHub: mã nguồn add-on",
                                                  "• Google Drive: tài liệu nhóm"], fill="#fbeff4")
    for y in (80, 179, 272, 365):
        arrow(ax, (230, y), (330, 90), head="filled", lw=0.8)
    arrow(ax, (430, 125), (430, 160), lw=0.9, label="HTTP :8069")
    arrow(ax, (460, 325), (460, 360), lw=0.9, label="TCP :5432")
    ax.plot([590, 885, 885], [405, 405, 92], color=INK, lw=0.9, ls=(0, (4, 3)))
    arrow(ax, (885, 92), (925, 92), lw=0.9, ls=(0, (4, 3)), head="open")
    ax.text(740, 401, "SQL read-only", fontsize=6.6, color=MUTED, style="italic", ha="center", va="bottom")
    arrow(ax, (925, 220), (830, 220), lw=0.9, ls=(0, (2, 2)), head="open", label="file .xlsx")
    arrow(ax, (830, 300), (925, 330), lw=0.9, ls=(0, (4, 3)), head="open", label="SMTP")
    save(fig, "architecture")


# ---------------------------------------------------------------- GANTT
def gantt():
    rows = [("Chốt đề tài, lập nhóm, GitHub/Drive", 1, 1, "QL"), ("Cài Odoo (Docker), tạo CSDL", 1, 2, "OD"),
            ("Soạn câu hỏi, phỏng vấn chính thức", 1, 2, "BA"), ("Khảo sát Google Form", 2, 2, "BA"),
            ("Phân tích dữ liệu Excel", 2, 4, "DA"), ("Vẽ 4 sơ đồ AS-IS, bảng Problem", 3, 3, "BA"),
            ("Vẽ 4 sơ đồ TO-BE, bảng Value", 4, 4, "BA"), ("Yêu cầu, Use case, Class, Physical v1", 4, 4, "BA"),
            ("Cài & cấu hình module HR", 3, 4, "OD"), ("Code add-on MVP", 5, 6, "DEV"),
            ("Báo cáo giữa kỳ", 6, 6, "QL"), ("Add-on mở rộng, cron, import", 7, 8, "DEV"),
            ("Power BI, mô phỏng tháng 8", 8, 8, "DA"), ("Demo cho doanh nghiệp, clip", 9, 9, "QL"),
            ("Hoàn thiện báo cáo, thuyết trình", 9, 10, "QL")]
    NEED = {"Chốt đề tài, lập nhóm, GitHub/Drive", "Soạn câu hỏi, phỏng vấn chính thức", "Khảo sát Google Form"}
    col = {"QL": "#2a78d6", "BA": "#eb6834", "DA": "#1baf7a", "OD": "#6250d6", "DEV": "#e34948"}
    name = {"QL": "Quản lý/Báo cáo", "BA": "Phân tích nghiệp vụ", "DA": "Dữ liệu/BI", "OD": "Odoo chức năng", "DEV": "Lập trình add-on"}
    fig, ax = plt.subplots(figsize=(7.4, 4.3))
    for i, (t, s, e, k) in enumerate(rows):
        done = e <= 4
        ax.barh(i, e - s + 1, left=s - 0.5, height=0.62, color=col[k], alpha=1 if done else 0.38,
                edgecolor="white", lw=1.5)
        if done:
            mark, c = ("!", "#b35900") if t in NEED else ("✓", "#1a7f37")
            ax.text(e + 0.55, i, mark, va="center", fontsize=8.5, color=c, family="DejaVu Sans", fontweight="bold")
    ax.axvline(4.5, color="#0b0b0b", lw=1, ls="--")
    ax.text(4.55, -0.9, "Hết tuần 4 (hiện tại)", fontsize=7.5, va="center")
    ax.set_yticks(range(len(rows)), [r[0] for r in rows], fontsize=7.6)
    ax.invert_yaxis(); ax.set_xticks(range(1, 11), [f"T{w}" for w in range(1, 11)], fontsize=8)
    ax.set_xlim(0.5, 10.9); ax.set_ylim(len(rows) - 0.4, -1.4)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    ax.grid(axis="x", color="#e6e5e0", lw=0.6); ax.set_axisbelow(True)
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(color=col[k], label=name[k]) for k in col], loc="upper right", fontsize=7, frameon=False)
    ax.set_xlabel("Tuần (đậm: tuần 1–4; nhạt: kế hoạch)   ✓ đã có sản phẩm   ! nhóm cần thực hiện trực tiếp", fontsize=8)
    fig.savefig(OUT + "gantt.pdf", bbox_inches="tight"); fig.savefig(OUT + "gantt.png", bbox_inches="tight", dpi=200)
    plt.close(fig)


if __name__ == "__main__":
    use_case(); class_diagram(); architecture(); gantt()
