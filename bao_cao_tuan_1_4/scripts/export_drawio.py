"""Xuất toàn bộ sơ đồ BPMN (fig_p1..fig_p4, chú giải) sang file .drawio trong ../drawio/.

Không vẽ lại PNG/PDF: Diagram.save được thay tạm để gọi to_drawio thay vì Matplotlib.
"""
import os
import runpy

import bpmn
from drawio_export import to_drawio

OUT = "../drawio/"
NAMES = {
    "p1_asis": "P1 - Tuyển dụng (AS-IS)", "p1_tobe": "P1 - Tuyển dụng (TO-BE)",
    "p2_asis": "P2 - Đào tạo (AS-IS)", "p2_tobe": "P2 - Đào tạo (TO-BE)",
    "p3_asis": "P3 - Xếp ca (AS-IS)", "p3_tobe": "P3 - Xếp ca (TO-BE)",
    "p4_asis": "P4 - Chấm công (AS-IS)", "p4_tobe": "P4 - Chấm công (TO-BE)",
    "overview": "Tổng thể quy trình HR", "bpmn_legend": "Chú giải ký hiệu BPMN",
}


def save_drawio(self, path, title=None):
    stem, ext = os.path.splitext(os.path.basename(path))
    if ext != ".pdf":           # mỗi sơ đồ được save 2 lần (pdf + png), chỉ xuất 1 lần
        return
    to_drawio(self, OUT + stem + ".drawio", name=NAMES.get(stem, stem))
    print("ok", OUT + stem + ".drawio")


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    bpmn.Diagram.save = save_drawio
    for script in ["fig_legend.py", "fig_p1.py", "fig_p2.py", "fig_p3.py", "fig_p4.py"]:
        runpy.run_path(script, run_name="__main__")
