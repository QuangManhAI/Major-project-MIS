"""Chụp màn hình Odoo cho báo cáo (Playwright, Chromium headless)."""
import sys
from playwright.sync_api import sync_playwright
OUT = "/Users/quangmanh/Project/pizza/bao_cao_tuan_1_4/figures/odoo/"
B = "http://localhost:8069"
shots = [a.split("=", 1) for a in sys.argv[1:]]
with sync_playwright() as p:
    br = p.chromium.launch()
    pg = br.new_page(viewport={"width": 1440, "height": 860}, device_scale_factor=1.5, locale="vi-VN")
    pg.goto(B + "/web/login?db=tpc_demo")
    pg.fill("input[name=login]", "admin"); pg.fill("input[name=password]", "admin")
    pg.press("input[name=password]", "Enter"); pg.wait_for_url("**/odoo**", timeout=30000); pg.wait_for_load_state("load")
    for name, path in shots:
        pg.goto(B + path); pg.wait_for_load_state("load"); pg.wait_for_timeout(3500)
        pg.screenshot(path=OUT + name + ".png")
        print("ok", name, pg.url)
    br.close()
