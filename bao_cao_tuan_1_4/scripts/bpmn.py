"""Thư viện nhỏ vẽ sơ đồ BPMN 2.0 bằng Matplotlib.

Ký hiệu bám theo tài liệu "BPMN – Business Process Model and Notation" của giảng viên:
  - Swimlane: Pool (thành phần tham gia) và Lane (vai trò trong pool); pool "hộp đen" cho bên ngoài
  - Event: Start (viền mảnh), Intermediate (viền đôi), End (viền đậm); loại Message, Timer
  - Activity: Task (User / Manual / Service / Send / Receive / Script / Business Rule),
    Sub-Process (dấu +), Loop marker
  - Gateway: Exclusive (X), Parallel (+), Inclusive (O), Event-based
  - Flow: Sequence flow (nét liền), Message flow (nét đứt, gốc tròn rỗng),
    Data association (chấm chấm)
  - Information artifact: Data Object, Data Object Collection, Data Store, Text Annotation
Trục y hướng xuống (giống bản vẽ trên giấy).
"""
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle, Polygon, Rectangle, Ellipse, Wedge, Arc

plt.rcParams["font.family"] = ["Arial", "DejaVu Sans"]
plt.rcParams["pdf.fonttype"] = 42

INK = "#1f2328"
MUTED = "#57606a"
TASK_FILL = "#eef4fb"
SYS_FILL = "#e3f1e6"       # task do hệ thống thực hiện (TO-BE) – tô xanh lá nhạt
PAIN_FILL = "#fdecea"      # task là điểm nghẽn (AS-IS) – tô đỏ nhạt
GW_FILL = "#fff6dc"
START_EDGE = "#2e7d32"
END_EDGE = "#b71c1c"
LANE_HEAD = "#f2f3f5"
POOL_HEAD = "#dfe3e8"

TW, TH = 104, 58      # kích thước task
R = 15                # bán kính event
G = 21                # nửa đường chéo gateway
FS = 7.6              # cỡ chữ trong task


class Diagram:
    def __init__(self, width, scale=0.0105):
        self.W = width
        self.scale = scale
        self.items = []          # các lệnh vẽ được hoãn đến khi biết chiều cao
        self.el = {}
        self.lanes = {}
        self.y = 0
        self.HEAD = 26           # bề rộng dải tên pool / lane

    # ------------------------------------------------------------------ swimlanes
    def pool(self, name, lanes=None, height=None, gap=14):
        """lanes: list[(key, label, height)]. Không có lanes -> pool hộp đen (collapsed)."""
        y0 = self.y
        if not lanes:
            h = height or 46
            self.items.append(("blackbox", name, y0, h))
            self.lanes[name] = (y0, h)
            self.y += h + gap
            return
        total = sum(l[2] for l in lanes)
        self.items.append(("pool", name, y0, total, lanes))
        y = y0
        for key, label, h in lanes:
            self.lanes[key] = (y, h)
            y += h
        self.y = y + gap

    def ly(self, lane, dy=0.0):
        y0, h = self.lanes[lane]
        return y0 + h / 2 + dy

    def lane_edge(self, lane, side):
        y0, h = self.lanes[lane]
        return y0 if side == "top" else y0 + h

    # ------------------------------------------------------------------ nodes
    def _add(self, id_, kind, x, y, w, h, **kw):
        self.el[id_] = dict(kind=kind, x=x, y=y, w=w, h=h, **kw)

    def task(self, id_, x, lane, text, ttype=None, dy=0, w=TW, h=TH, sub=False,
             loop=False, multi=False, fill=None):
        self._add(id_, "task", x, self.ly(lane, dy), w, h, text=text, ttype=ttype,
                  sub=sub, loop=loop, multi=multi, fill=fill)

    def event(self, id_, x, lane, pos="start", trig=None, label=None, dy=0,
              throw=False, lpos="b"):
        self._add(id_, "event", x, self.ly(lane, dy), 2 * R, 2 * R, pos=pos, trig=trig,
                  label=label, throw=throw, lpos=lpos)

    def gateway(self, id_, x, lane, gtype="x", label=None, dy=0, lpos="t"):
        self._add(id_, "gw", x, self.ly(lane, dy), 2 * G, 2 * G, gtype=gtype,
                  label=label, lpos=lpos)

    def data(self, id_, x, y, label, collection=False, io=None):
        self._add(id_, "data", x, y, 26, 34, label=label, collection=collection, io=io)

    def store(self, id_, x, y, label):
        self._add(id_, "store", x, y, 38, 34, label=label)

    def note(self, id_, x, y, text, w=150, h=None, color=MUTED):
        lines = text.count("\n") + 1
        self._add(id_, "note", x, y, w, h or (13 * lines + 10), text=text, color=color)

    def point(self, id_, x, y):
        """Điểm neo vô hình (VD: mép pool hộp đen để nối message flow)."""
        self._add(id_, "pt", x, y, 0, 0)

    def pool_edge(self, id_, x, pool, side="bottom"):
        y0, h = self.lanes[pool]
        self.point(id_, x, y0 + h if side == "bottom" else y0)

    def _draw_pt(self, e):
        pass

    def at(self, lane, dy=0):
        return self.ly(lane, dy)

    # ------------------------------------------------------------------ ports
    def port(self, id_, side):
        e = self.el[id_]
        x, y, w, h = e["x"], e["y"], e["w"], e["h"]
        if e["kind"] == "note":
            return {"l": (x, y + h / 2), "r": (x + w, y + h / 2), "t": (x + 10, y),
                    "b": (x + 10, y + h)}[side]
        return {"r": (x + w / 2, y), "l": (x - w / 2, y), "t": (x, y - h / 2),
                "b": (x, y + h / 2)}[side]

    def center(self, id_):
        e = self.el[id_]
        return e["x"], e["y"]

    # ------------------------------------------------------------------ edges
    def flow(self, a, b, route=None, label=None, via=None, lab_at=0, lab_dx=4,
             lab_dy=-4, src=None, dst=None, kind="seq"):
        """route: 'h' | 'hv' | 'vh' | 'hvh' | 'vhv' ; via: danh sách điểm trung gian."""
        self.items.append(("edge", a, b, route, label, via, lab_at, lab_dx, lab_dy,
                           src, dst, kind))

    def msg(self, a, b, **kw):
        kw.setdefault("route", "v")
        self.flow(a, b, kind="msg", **kw)

    def assoc(self, a, b, **kw):
        self.flow(a, b, kind="assoc", **kw)

    def _route(self, a, b, route, via, src, dst, kind):
        ea, eb = self.el[a], self.el[b]
        ax_, ay = ea["x"], ea["y"]
        bx, by = eb["x"], eb["y"]
        if via is not None:
            p0 = self.port(a, src) if src else self._auto_port(a, via[0])
            p1 = self.port(b, dst) if dst else self._auto_port(b, via[-1])
            return [p0, *via, p1]
        if route is None:
            if abs(ay - by) < 1:
                route = "h"
            elif kind == "msg":
                route = "v"
            elif ea["kind"] == "gw":
                route = "vh"
            elif eb["kind"] == "gw":
                route = "hv"
            else:
                route = "hvh"
        if route == "h":
            p0 = self.port(a, src or ("r" if bx > ax_ else "l"))
            p1 = self.port(b, dst or ("l" if bx > ax_ else "r"))
            return [p0, (p1[0], p0[1])] if abs(p0[1] - p1[1]) < 1 else [p0, p1]
        if route == "v":
            p0 = self.port(a, src or ("b" if by > ay else "t"))
            p1 = self.port(b, dst or ("t" if by > ay else "b"))
            if abs(p0[0] - p1[0]) < 1:
                return [p0, p1]
            my = (p0[1] + p1[1]) / 2
            return [p0, (p0[0], my), (p1[0], my), p1]
        if route == "hv":
            p0 = self.port(a, src or ("r" if bx > ax_ else "l"))
            p1 = self.port(b, dst or ("t" if by > ay else "b"))
            return [p0, (p1[0], p0[1]), p1]
        if route == "vh":
            p0 = self.port(a, src or ("b" if by > ay else "t"))
            p1 = self.port(b, dst or ("l" if bx > ax_ else "r"))
            return [p0, (p0[0], p1[1]), p1]
        if route == "hvh":
            p0 = self.port(a, src or "r")
            p1 = self.port(b, dst or "l")
            mx = (p0[0] + p1[0]) / 2
            return [p0, (mx, p0[1]), (mx, p1[1]), p1]
        if route == "vhv":
            p0 = self.port(a, src or ("b" if by > ay else "t"))
            p1 = self.port(b, dst or ("t" if by > ay else "b"))
            my = (p0[1] + p1[1]) / 2
            return [p0, (p0[0], my), (p1[0], my), p1]
        raise ValueError(route)

    def _auto_port(self, id_, pt):
        e = self.el[id_]
        dx, dy = pt[0] - e["x"], pt[1] - e["y"]
        if abs(dx) * e["h"] >= abs(dy) * e["w"]:
            return self.port(id_, "r" if dx > 0 else "l")
        return self.port(id_, "b" if dy > 0 else "t")

    # ------------------------------------------------------------------ render
    def save(self, path, title=None):
        H = self.y
        fig = plt.figure(figsize=(self.W * self.scale, H * self.scale))
        ax = fig.add_axes([0, 0, 1, 1])
        ax.set_xlim(-2, self.W + 2)
        ax.set_ylim(H + 2, -2)
        ax.axis("off")
        self.ax = ax
        for it in self.items:
            if it[0] == "pool":
                self._draw_pool(*it[1:])
            elif it[0] == "blackbox":
                self._draw_blackbox(*it[1:])
        for it in self.items:
            if it[0] == "edge":
                self._draw_edge(*it[1:])
        for id_, e in self.el.items():
            getattr(self, "_draw_" + e["kind"])(e)
        fig.savefig(path, bbox_inches="tight", pad_inches=0.04, dpi=220)
        plt.close(fig)

    # ---- swimlanes
    def _draw_pool(self, name, y0, total, lanes):
        ax, W, Hd = self.ax, self.W, self.HEAD
        ax.add_patch(Rectangle((0, y0), W, total, fc="white", ec=INK, lw=1.1, zorder=0))
        ax.add_patch(Rectangle((0, y0), Hd, total, fc=POOL_HEAD, ec=INK, lw=1.1, zorder=0.1))
        ax.text(Hd / 2, y0 + total / 2, name, rotation=90, ha="center", va="center",
                fontsize=8.2, fontweight="bold", color=INK)
        y = y0
        for key, label, h in lanes:
            ax.add_patch(Rectangle((Hd, y), Hd, h, fc=LANE_HEAD, ec=INK, lw=0.8, zorder=0.1))
            ax.plot([Hd, W], [y, y], color=INK, lw=0.8, zorder=0.2)
            ax.text(Hd * 1.5, y + h / 2, label, rotation=90, ha="center", va="center",
                    fontsize=7.4, color=INK, linespacing=1.05)
            y += h

    def _draw_blackbox(self, name, y0, h):
        ax = self.ax
        ax.add_patch(Rectangle((0, y0), self.W, h, fc="#fafbfc", ec=INK, lw=1.1, zorder=0))
        ax.text(self.W / 2, y0 + h / 2, name, ha="center", va="center", fontsize=8.6,
                fontweight="bold", color=INK)

    # ---- edges
    def _draw_edge(self, a, b, route, label, via, lab_at, lab_dx, lab_dy, src, dst, kind):
        ax = self.ax
        pts = self._route(a, b, route, via, src, dst, kind)
        xs, ys = zip(*pts)
        if kind == "seq":
            ax.plot(xs, ys, color=INK, lw=0.95, zorder=1, solid_joinstyle="miter")
            self._arrowhead(pts[-2], pts[-1], filled=True)
        elif kind == "msg":
            ax.plot(xs, ys, color=INK, lw=0.85, ls=(0, (4, 3)), zorder=1)
            ax.add_patch(Circle(pts[0], 3.2, fc="white", ec=INK, lw=0.85, zorder=1.2))
            self._arrowhead(pts[-2], pts[-1], filled=False)
        else:  # data association
            ax.plot(xs, ys, color=MUTED, lw=0.85, ls=(0, (1, 2.2)), zorder=1)
            if self.el[b]["kind"] not in ("note", "pt"):
                self._arrowhead(pts[-2], pts[-1], filled=False, open_v=True, color=MUTED)
        if label:
            p, q = pts[lab_at], pts[lab_at + 1]
            ax.text(p[0] + lab_dx, p[1] + lab_dy, label, fontsize=6.6, color=INK,
                    ha="left", va="bottom", zorder=3, linespacing=1.0,
                    bbox=dict(fc="white", ec="none", pad=0.4, alpha=0.85))

    def _arrowhead(self, p, q, filled=True, open_v=False, color=INK, L=8, Wd=3.6):
        ang = math.atan2(q[1] - p[1], q[0] - p[0])
        bx, by = q[0] - L * math.cos(ang), q[1] - L * math.sin(ang)
        nx, ny = -math.sin(ang) * Wd, math.cos(ang) * Wd
        tri = [(q[0], q[1]), (bx + nx, by + ny), (bx - nx, by - ny)]
        if open_v:
            self.ax.plot([tri[1][0], q[0], tri[2][0]], [tri[1][1], q[1], tri[2][1]],
                         color=color, lw=0.85, zorder=1.3)
        else:
            self.ax.add_patch(Polygon(tri, closed=True, fc=INK if filled else "white",
                                      ec=color, lw=0.85, zorder=1.3))

    # ---- nodes
    def _draw_task(self, e):
        ax = self.ax
        x, y, w, h = e["x"], e["y"], e["w"], e["h"]
        fill = e["fill"] or TASK_FILL
        ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h,
                                    boxstyle="round,pad=0,rounding_size=7",
                                    fc=fill, ec=INK, lw=1.0, zorder=2))
        has_icon = e["ttype"] is not None
        ty = y + (2 if has_icon else 0) - (4 if (e["sub"] or e["loop"] or e["multi"]) else 0)
        ax.text(x + (3 if has_icon else 0), ty, e["text"], ha="center", va="center",
                fontsize=FS, color=INK, zorder=3, linespacing=1.05)
        if has_icon:
            getattr(self, "_icon_" + e["ttype"])(x - w / 2 + 10, y - h / 2 + 10)
        markers = [m for m in ("loop", "multi", "sub") if e[m]]
        mx0 = x - (len(markers) - 1) * 6
        for i, m in enumerate(markers):
            getattr(self, "_mark_" + m)(mx0 + i * 12, y + h / 2 - 7)

    def _icon_user(self, cx, cy):
        ax = self.ax
        ax.add_patch(Circle((cx, cy - 2.6), 2.6, fc="white", ec=INK, lw=0.7, zorder=4))
        ax.add_patch(Wedge((cx, cy + 5.2), 5.0, 180, 360, fc="white", ec=INK, lw=0.7, zorder=3.9))

    def _icon_manual(self, cx, cy):
        ax = self.ax
        ax.add_patch(FancyBboxPatch((cx - 6, cy - 2.5), 6, 7, boxstyle="round,pad=0,rounding_size=1.4",
                                    fc="white", ec=INK, lw=0.7, zorder=4))
        for i, ln in enumerate((8, 9, 8, 6)):
            ax.add_patch(FancyBboxPatch((cx - 1, cy - 2.5 + i * 1.75), ln, 1.5,
                                        boxstyle="round,pad=0,rounding_size=0.7",
                                        fc="white", ec=INK, lw=0.6, zorder=4.1))

    def _icon_service(self, cx, cy):
        ax = self.ax
        pts = []
        for i in range(16):
            r = 6.0 if i % 2 == 0 else 4.4
            a = i * math.pi / 8
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
        ax.add_patch(Polygon(pts, closed=True, fc="white", ec=INK, lw=0.7, zorder=4))
        ax.add_patch(Circle((cx, cy), 1.9, fc="white", ec=INK, lw=0.7, zorder=4.1))

    def _envelope(self, cx, cy, filled, w=11, h=7.5, z=4):
        ax = self.ax
        fc, lc = (INK, "white") if filled else ("white", INK)
        ax.add_patch(Rectangle((cx - w / 2, cy - h / 2), w, h, fc=fc, ec=INK, lw=0.7, zorder=z))
        ax.plot([cx - w / 2, cx, cx + w / 2], [cy - h / 2, cy + 0.6, cy - h / 2], color=lc,
                lw=0.7, zorder=z + 0.1)

    def _icon_send(self, cx, cy):
        self._envelope(cx, cy, True)

    def _icon_receive(self, cx, cy):
        self._envelope(cx, cy, False)

    def _icon_script(self, cx, cy):
        ax = self.ax
        ax.add_patch(Rectangle((cx - 4.5, cy - 5.5), 9, 11, fc="white", ec=INK, lw=0.7, zorder=4))
        for k in (-2.5, 0, 2.5):
            ax.plot([cx - 2.8, cx + 2.8], [cy + k, cy + k], color=INK, lw=0.5, zorder=4.1)

    def _icon_rule(self, cx, cy):
        ax = self.ax
        ax.add_patch(Rectangle((cx - 6, cy - 4.5), 12, 9, fc="white", ec=INK, lw=0.7, zorder=4))
        ax.add_patch(Rectangle((cx - 6, cy - 4.5), 12, 2.6, fc="#bbbbbb", ec=INK, lw=0.7, zorder=4.1))
        ax.plot([cx - 6, cx + 6], [cy + 1.2, cy + 1.2], color=INK, lw=0.5, zorder=4.2)
        ax.plot([cx - 2, cx - 2], [cy - 1.9, cy + 4.5], color=INK, lw=0.5, zorder=4.2)

    def _mark_sub(self, cx, cy):
        ax = self.ax
        ax.add_patch(Rectangle((cx - 4.5, cy - 4.5), 9, 9, fc="white", ec=INK, lw=0.7, zorder=4))
        ax.plot([cx - 2.8, cx + 2.8], [cy, cy], color=INK, lw=0.8, zorder=4.1)
        ax.plot([cx, cx], [cy - 2.8, cy + 2.8], color=INK, lw=0.8, zorder=4.1)

    def _mark_loop(self, cx, cy):
        ax = self.ax
        ax.add_patch(Arc((cx, cy), 9, 9, theta1=-40, theta2=250, color=INK, lw=0.8, zorder=4))
        a = math.radians(-40)
        tx, ty = cx + 4.5 * math.cos(a), cy + 4.5 * math.sin(a)
        ax.add_patch(Polygon([(tx - 2.6, ty + 0.2), (tx + 1.2, ty - 2.6), (tx + 1.6, ty + 1.6)],
                             fc=INK, ec=INK, lw=0.4, zorder=4.1))

    def _mark_multi(self, cx, cy):
        for k in (-3, 0, 3):
            self.ax.plot([cx + k, cx + k], [cy - 4, cy + 4], color=INK, lw=1.0, zorder=4)

    def _draw_event(self, e):
        ax = self.ax
        x, y = e["x"], e["y"]
        if e["pos"] == "start":
            ax.add_patch(Circle((x, y), R, fc="#f1f8f1", ec=START_EDGE, lw=1.2, zorder=2))
        elif e["pos"] == "end":
            ax.add_patch(Circle((x, y), R, fc="#fbeeee", ec=END_EDGE, lw=2.8, zorder=2))
        else:
            ax.add_patch(Circle((x, y), R, fc="white", ec=INK, lw=0.9, zorder=2))
            ax.add_patch(Circle((x, y), R - 3, fc="none", ec=INK, lw=0.9, zorder=2.1))
        t = e["trig"]
        if t == "message":
            self._envelope(x, y, e["throw"] or e["pos"] == "end", w=13, h=9, z=3)
        elif t == "timer":
            ax.add_patch(Circle((x, y), R - 5.5, fc="white", ec=INK, lw=0.8, zorder=3))
            for k in range(12):
                a = k * math.pi / 6
                ax.plot([x + 6.5 * math.cos(a), x + 8.3 * math.cos(a)],
                        [y + 6.5 * math.sin(a), y + 8.3 * math.sin(a)], color=INK, lw=0.5, zorder=3.1)
            ax.plot([x, x + 4.5], [y, y - 1.5], color=INK, lw=0.8, zorder=3.2)
            ax.plot([x, x - 0.8], [y, y - 6], color=INK, lw=0.8, zorder=3.2)
        elif t == "conditional":
            ax.add_patch(Rectangle((x - 5, y - 6.5), 10, 13, fc="white", ec=INK, lw=0.7, zorder=3))
            for k in (-3.5, -0.5, 2.5):
                ax.plot([x - 3, x + 3], [y + k, y + k], color=INK, lw=0.6, zorder=3.1)
        elif t == "error":
            ax.add_patch(Polygon([(x - 6, y + 6), (x - 2, y - 6), (x + 2, y + 1), (x + 6, y - 6),
                                  (x + 2, y + 6), (x - 2, y - 1)], fc=INK, ec=INK, zorder=3))
        if e["label"]:
            off = {"b": (0, R + 3, "center", "top"), "t": (0, -R - 3, "center", "bottom"),
                   "r": (R + 4, 0, "left", "center"), "l": (-R - 4, 0, "right", "center")}[e["lpos"]]
            ax.text(x + off[0], y + off[1], e["label"], ha=off[2], va=off[3], fontsize=6.7,
                    color=INK, zorder=3, linespacing=1.0)

    def _draw_gw(self, e):
        ax = self.ax
        x, y = e["x"], e["y"]
        ax.add_patch(Polygon([(x, y - G), (x + G, y), (x, y + G), (x - G, y)], closed=True,
                             fc=GW_FILL, ec=INK, lw=1.0, zorder=2))
        g = e["gtype"]
        k = 7
        if g == "x":
            ax.plot([x - k, x + k], [y - k, y + k], color=INK, lw=2.2, zorder=3)
            ax.plot([x - k, x + k], [y + k, y - k], color=INK, lw=2.2, zorder=3)
        elif g == "+":
            ax.plot([x - 9, x + 9], [y, y], color=INK, lw=2.4, zorder=3)
            ax.plot([x, x], [y - 9, y + 9], color=INK, lw=2.4, zorder=3)
        elif g == "o":
            ax.add_patch(Circle((x, y), 8, fc="none", ec=INK, lw=2.0, zorder=3))
        elif g == "event":
            ax.add_patch(Circle((x, y), 10, fc="none", ec=INK, lw=0.8, zorder=3))
            ax.add_patch(Circle((x, y), 8, fc="none", ec=INK, lw=0.8, zorder=3))
            pts = [(x + 5 * math.cos(a), y + 5 * math.sin(a))
                   for a in [-math.pi / 2 + i * 2 * math.pi / 5 for i in range(5)]]
            ax.add_patch(Polygon(pts, closed=True, fc="none", ec=INK, lw=0.8, zorder=3))
        if e["label"]:
            off = {"t": (0, -G - 3, "center", "bottom"), "b": (0, G + 3, "center", "top"),
                   "r": (G + 3, -G * 0.6, "left", "bottom"), "l": (-G - 3, -G * 0.6, "right", "bottom"),
                   "tl": (-5, -G + 1, "right", "bottom"), "tr": (5, -G + 1, "left", "bottom"),
                   "bl": (-5, G - 1, "right", "top"), "br": (5, G - 1, "left", "top")}[e["lpos"]]
            ax.text(x + off[0], y + off[1], e["label"], ha=off[2], va=off[3], fontsize=6.7,
                    color=INK, zorder=3, linespacing=1.0)

    def _draw_data(self, e):
        ax = self.ax
        x, y, w, h = e["x"], e["y"], e["w"], e["h"]
        f = 7
        x0, y0 = x - w / 2, y - h / 2
        ax.add_patch(Polygon([(x0, y0), (x0 + w - f, y0), (x0 + w, y0 + f), (x0 + w, y0 + h),
                              (x0, y0 + h)], closed=True, fc="white", ec=INK, lw=0.85, zorder=2))
        ax.plot([x0 + w - f, x0 + w - f, x0 + w], [y0, y0 + f, y0 + f], color=INK, lw=0.7, zorder=2.1)
        if e["collection"]:
            for k in (-3, 0, 3):
                ax.plot([x + k, x + k], [y0 + h - 10, y0 + h - 3], color=INK, lw=1.1, zorder=2.2)
        if e["io"] == "in":
            ax.add_patch(Polygon([(x0 + 3, y0 + 4), (x0 + 8, y0 + 4), (x0 + 8, y0 + 2), (x0 + 12, y0 + 6),
                                  (x0 + 8, y0 + 10), (x0 + 8, y0 + 8), (x0 + 3, y0 + 8)],
                                 fc="white", ec=INK, lw=0.6, zorder=2.2))
        elif e["io"] == "out":
            ax.add_patch(Polygon([(x0 + 3, y0 + 4), (x0 + 8, y0 + 4), (x0 + 8, y0 + 2), (x0 + 12, y0 + 6),
                                  (x0 + 8, y0 + 10), (x0 + 8, y0 + 8), (x0 + 3, y0 + 8)],
                                 fc=INK, ec=INK, lw=0.6, zorder=2.2))
        ax.text(x, y0 + h + 3, e["label"], ha="center", va="top", fontsize=6.4, color=INK,
                style="italic", zorder=3, linespacing=1.0)

    def _draw_store(self, e):
        ax = self.ax
        x, y, w, h = e["x"], e["y"], e["w"], e["h"]
        x0, y0 = x - w / 2, y - h / 2
        eh = 9
        ax.add_patch(Rectangle((x0, y0 + eh / 2), w, h - eh, fc="white", ec="none", zorder=2))
        ax.plot([x0, x0], [y0 + eh / 2, y0 + h - eh / 2], color=INK, lw=0.85, zorder=2.1)
        ax.plot([x0 + w, x0 + w], [y0 + eh / 2, y0 + h - eh / 2], color=INK, lw=0.85, zorder=2.1)
        ax.add_patch(Ellipse((x, y0 + h - eh / 2), w, eh, fc="white", ec=INK, lw=0.85, zorder=2.0))
        ax.add_patch(Rectangle((x0 + 0.5, y0 + eh / 2), w - 1, h - eh, fc="white", ec="none", zorder=2.05))
        ax.add_patch(Ellipse((x, y0 + eh / 2), w, eh, fc="white", ec=INK, lw=0.85, zorder=2.2))
        for k in (3, 6):
            ax.add_patch(Arc((x, y0 + eh / 2 + k), w, eh, theta1=0, theta2=180, color=INK, lw=0.6, zorder=2.2))
        ax.text(x, y0 + h + 3, e["label"], ha="center", va="top", fontsize=6.4, color=INK,
                style="italic", zorder=3, linespacing=1.0)

    def _draw_note(self, e):
        ax = self.ax
        x, y, w, h = e["x"], e["y"], e["w"], e["h"]
        ax.plot([x + 8, x, x, x + 8], [y, y, y + h, y + h], color=MUTED, lw=0.9, zorder=2)
        ax.add_patch(Rectangle((x + 1, y + 1), w, h - 2, fc="white", ec="none", alpha=0.9, zorder=1.9))
        ax.text(x + 5, y + h / 2, e["text"], ha="left", va="center", fontsize=6.5,
                color=e["color"], zorder=3, linespacing=1.12)
