"""Tuần 1–4: tạo database tpc_demo và cài các module HR qua XML-RPC."""
import xmlrpc.client, time, sys
URL = "http://localhost:8069"; DB = "tpc_demo"; MASTER = "tpc_master_2026"
ADMIN, PWD = "admin", "admin"
dbs = xmlrpc.client.ServerProxy(URL + "/xmlrpc/2/db", allow_none=True)
if DB not in dbs.list():
    t = time.time()
    dbs.create_database(MASTER, DB, False, "vi_VN", PWD, ADMIN, "vn", "")
    print("created db in", round(time.time() - t), "s")
common = xmlrpc.client.ServerProxy(URL + "/xmlrpc/2/common")
uid = common.authenticate(DB, ADMIN, PWD, {})
m = xmlrpc.client.ServerProxy(URL + "/xmlrpc/2/object", allow_none=True)
x = lambda model, meth, *a, **k: m.execute_kw(DB, uid, PWD, model, meth, list(a), k)
mods = ["hr", "hr_recruitment", "website_hr_recruitment", "hr_skills", "hr_attendance",
        "hr_holidays", "website_slides", "survey", "base_automation", "hr_recruitment_skills"]
for name in mods:
    ids = x("ir.module.module", "search", [("name", "=", name)])
    st = x("ir.module.module", "read", ids, fields=["state"])
    if not st or st[0]["state"] == "installed":
        print(name, st and st[0]["state"]); continue
    t = time.time()
    x("ir.module.module", "button_immediate_install", ids)
    print("installed", name, round(time.time() - t), "s"); sys.stdout.flush()
