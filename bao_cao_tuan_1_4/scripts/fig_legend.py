"""Bảng chú giải ký hiệu BPMN dùng trong báo cáo."""
from bpmn import *

d = Diagram(1000)
d.pool("Chú giải ký hiệu BPMN 2.0", [("a", "Sự kiện", 78), ("b", "Hoạt động\n(Task)", 86),
                                    ("c", "Cổng\n(Gateway)", 78), ("d", "Dữ liệu &\nLuồng", 92)])
x0 = 110
evs = [("start", None, "Start\n(bắt đầu)"), ("start", "message", "Start\nMessage"), ("start", "timer", "Start\nTimer"),
       ("inter", "message", "Intermediate\nMessage (nhận)"), ("inter", "timer", "Intermediate\nTimer (chờ)"),
       ("inter", "conditional", "Intermediate\nConditional"), ("end", None, "End\n(kết thúc)"),
       ("end", "message", "End\nMessage (gửi)")]
for i, (p, t, l) in enumerate(evs):
    d.event(f"e{i}", x0 + i * 112, "a", p, t, l, dy=-10)
tks = [(None, "Task"), ("user", "User Task\n(trên hệ thống)"), ("manual", "Manual Task\n(thủ công)"),
       ("service", "Service Task\n(hệ thống tự động)"), ("send", "Send Task"), ("receive", "Receive Task"),
       ("rule", "Business Rule\nTask")]
for i, (t, l) in enumerate(tks):
    d.task(f"t{i}", x0 + 10 + i * 118, "b", l, ttype=t, w=100, h=54)
d.task("sp", x0 + 10 + 7 * 118 - 4, "b", "Sub-Process\n+ Loop", sub=True, loop=True, w=92, h=54)
gws = [("x", "Exclusive (XOR)\nchỉ 1 nhánh"), ("+", "Parallel (AND)\nmọi nhánh"),
       ("o", "Inclusive (OR)\n1 hoặc nhiều nhánh"), ("event", "Event-based\ntheo sự kiện")]
for i, (g, l) in enumerate(gws):
    d.gateway(f"g{i}", x0 + 20 + i * 150, "c", g, l, lpos="r", dy=4)
d.task("ts", 790, "c", "Task do hệ thống\nthực hiện (TO-BE)", w=110, h=46, fill=SYS_FILL)
d.task("tp", 920, "c", "Bước gây tắc nghẽn\n(AS-IS)", w=110, h=46, fill=PAIN_FILL)
yb = d.at("d") - 14
d.data("do", x0, yb, "Data Object")
d.data("dc", x0 + 95, yb, "Data Object\nCollection", collection=True)
d.store("ds", x0 + 190, yb, "Data Store")
d.note("nt", x0 + 255, yb - 16, "Text Annotation\n(ghi chú)", w=95)
# luồng mẫu
y = d.at("d")
for k, (lab, kind) in enumerate([("Sequence Flow", "seq"), ("Message Flow", "msg"), ("Data Association", "assoc")]):
    d.el[f"pa{k}"] = dict(kind="pt", x=500 + k * 165, y=y - 8, w=0, h=0)
    d.el[f"pb{k}"] = dict(kind="pt", x=610 + k * 165, y=y - 8, w=0, h=0)
    d.flow(f"pa{k}", f"pb{k}", via=[], src="r", dst="l", kind=kind)
    d.el[f"pl{k}"] = dict(kind="lbl", x=555 + k * 165, y=y + 8, w=0, h=0, text=lab)
Diagram._draw_pt = lambda self, e: None
Diagram._draw_lbl = lambda self, e: self.ax.text(e["x"], e["y"], e["text"], ha="center", va="top", fontsize=6.8)
d.save("../figures/bpmn_legend.pdf")
d.save("../figures/bpmn_legend.png")
