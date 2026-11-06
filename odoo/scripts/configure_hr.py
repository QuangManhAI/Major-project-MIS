"""Tuần 3–4: cấu hình Employees + Recruitment + Skills cho cửa hàng demo (dữ liệu giả, không dùng tên thật)."""
import random
import xmlrpc.client

URL, DB, USER, PWD = "http://localhost:8069", "tpc_demo", "admin", "admin"
uid = xmlrpc.client.ServerProxy(URL + "/xmlrpc/2/common").authenticate(DB, USER, PWD, {})
M = xmlrpc.client.ServerProxy(URL + "/xmlrpc/2/object", allow_none=True)
CTX = {"context": {"lang": "vi_VN", "tz": "Asia/Ho_Chi_Minh"}}


def x(model, method, *args, **kw):
    kw = {**CTX, **kw}
    return M.execute_kw(DB, uid, PWD, model, method, list(args), kw)


def get_or_create(model, domain, vals):
    ids = x(model, "search", domain, limit=1)
    return ids[0] if ids else x(model, "create", vals)


random.seed(2026)

# 1. Công ty, tiền tệ, múi giờ
vnd = x("res.currency", "search", [("name", "=", "VND")], context={"active_test": False})[0]
x("res.currency", "write", [vnd], {"active": True})
company = x("res.company", "search", [], limit=1)[0]
x("res.company", "write", [company], {"name": "TPC – Cửa hàng demo LVS", "currency_id": vnd})
x("res.users", "write", [uid], {"tz": "Asia/Ho_Chi_Minh", "lang": "vi_VN", "name": "Quản lý cửa hàng (demo)"})

# 2. Phòng ban = khu vực làm việc trong cửa hàng
depts = {}
for d in ["Phục vụ", "Thu ngân", "Bếp", "Giao hàng", "Quản lý cửa hàng"]:
    depts[d] = get_or_create("hr.department", [("name", "=", d)], {"name": d})

# 3. Vị trí công việc
jobs = {}
for name, dept, n in [("Phục vụ part-time", "Phục vụ", 4), ("Thu ngân part-time", "Thu ngân", 1),
                      ("Bếp part-time (Make line / Cut & Pack)", "Bếp", 3), ("Giao hàng", "Giao hàng", 1),
                      ("Shift Manager", "Quản lý cửa hàng", 0)]:
    jobs[name] = get_or_create("hr.job", [("name", "=", name)],
                               {"name": name, "department_id": depts[dept], "no_of_recruitment": n})
    x("hr.job", "write", [jobs[name]], {"is_published": n > 0})

# 4. Giai đoạn tuyển dụng theo quy trình TO-BE
old = x("hr.recruitment.stage", "search", [])
wanted = [("Mới", False, False), ("Đã liên hệ", False, False), ("Hẹn phỏng vấn", False, False),
          ("Đã phỏng vấn", False, False), ("Đề nghị nhận việc", False, False), ("Nhận việc", True, True)]
stages = {}
for seq, (n, hired, fold) in enumerate(wanted, 1):
    sid = get_or_create("hr.recruitment.stage", [("name", "=", n)], {"name": n})
    x("hr.recruitment.stage", "write", [sid], {"sequence": seq, "hired_stage": hired, "fold": fold})
    stages[n] = sid
for sid in old:
    if sid not in stages.values():
        try:
            x("hr.recruitment.stage", "unlink", [sid])
        except Exception:
            pass

# 5. Nguồn ứng viên (UTM)
sources = {s: get_or_create("utm.source", [("name", "=", s)], {"name": s})
           for s in ["Standee tại cửa hàng", "Fanpage cửa hàng", "Phòng Tuyển dụng gửi", "Người quen giới thiệu",
                     "Website Jobs"]}

# 6. Kỹ năng = quầy đã đạt
st = get_or_create("hr.skill.type", [("name", "=", "Quầy làm việc")], {"name": "Quầy làm việc"})
skills = {}
for s in ["Phục vụ", "Thu ngân", "Bếp – Make line", "Bếp – Cut & Pack", "Giao hàng", "ATVSTP"]:
    skills[s] = get_or_create("hr.skill", [("name", "=", s), ("skill_type_id", "=", st)],
                              {"name": s, "skill_type_id": st})
levels = {}
for n, p, dflt in [("Đang học", 30, True), ("Đạt", 100, False)]:
    levels[n] = get_or_create("hr.skill.level", [("name", "=", n), ("skill_type_id", "=", st)],
                              {"name": n, "level_progress": p, "default_level": dflt, "skill_type_id": st})

# 7. Nhân viên giả
ho = ["Nguyễn", "Trần", "Lê", "Phạm", "Hoàng", "Võ", "Đặng", "Bùi", "Đỗ", "Huỳnh"]
lot = ["Minh", "Thu", "Gia", "Ngọc", "Anh", "Bảo", "Khánh", "Thanh", "Hải", "Tuấn"]
ten = ["An", "Bình", "Châu", "Dũng", "Hà", "Hân", "Khoa", "Linh", "My", "Nam", "Phúc", "Quân", "Tâm", "Trang",
       "Vy", "Yến"]
used = set()


def fake_name():
    while True:
        n = f"{random.choice(ho)} {random.choice(lot)} {random.choice(ten)}"
        if n not in used:
            used.add(n)
            return n


if x("hr.employee", "search_count", []) < 10:
    plan = [("Phục vụ", "Phục vụ part-time", 8), ("Thu ngân", "Thu ngân part-time", 3),
            ("Bếp", "Bếp part-time (Make line / Cut & Pack)", 8), ("Giao hàng", "Giao hàng", 2),
            ("Quản lý cửa hàng", "Shift Manager", 3)]
    skill_of = {"Phục vụ": ["Phục vụ"], "Thu ngân": ["Thu ngân", "Phục vụ"],
                "Bếp": ["Bếp – Make line", "Bếp – Cut & Pack"], "Giao hàng": ["Giao hàng"],
                "Quản lý cửa hàng": ["Phục vụ", "Thu ngân", "Bếp – Make line"]}
    for dept, job, n in plan:
        for i in range(n):
            nm = fake_name()
            e = x("hr.employee", "create", {"name": nm, "department_id": depts[dept], "job_id": jobs[job],
                                            "job_title": job, "pin": str(random.randint(1000, 9999))})
            for k, sk in enumerate(skill_of[dept]):
                lv = "Đạt" if (k == 0 or random.random() < 0.5) else "Đang học"
                x("hr.employee.skill", "create", {"employee_id": e, "skill_id": skills[sk],
                                                  "skill_level_id": levels[lv], "skill_type_id": st})
            for sk in ["ATVSTP"]:
                x("hr.employee.skill", "create", {"employee_id": e, "skill_id": skills[sk],
                                                  "skill_level_id": levels["Đạt"], "skill_type_id": st})

# 8. Ứng viên giả trên pipeline
has_candidate = bool(x("ir.model", "search", [("model", "=", "hr.candidate")]))
if x("hr.applicant", "search_count", []) < 5:
    dist = [("Mới", 6), ("Đã liên hệ", 4), ("Hẹn phỏng vấn", 4), ("Đã phỏng vấn", 3), ("Đề nghị nhận việc", 2)]
    jl = [jobs["Phục vụ part-time"], jobs["Phục vụ part-time"], jobs["Bếp part-time (Make line / Cut & Pack)"],
          jobs["Thu ngân part-time"], jobs["Giao hàng"]]
    k = 0
    for stg, n in dist:
        for _ in range(n):
            nm = fake_name(); k += 1
            vals = {"job_id": random.choice(jl), "stage_id": stages[stg],
                    "source_id": random.choice(list(sources.values())), "priority": str(random.randint(0, 2))}
            email, phone = f"ungvien{k:02d}@example.com", f"09000000{k:02d}"
            if has_candidate:
                vals["candidate_id"] = x("hr.candidate", "create", {"partner_name": nm, "email_from": email,
                                                                     "partner_phone": phone})
            else:
                vals.update({"partner_name": nm, "email_from": email, "partner_phone": phone, "name": nm})
            x("hr.applicant", "create", vals)
print("employees", x("hr.employee", "search_count", []), "applicants", x("hr.applicant", "search_count", []))
