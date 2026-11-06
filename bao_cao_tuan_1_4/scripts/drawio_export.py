"""Xuất một Diagram (bpmn.py) sang file .drawio dùng thư viện hình BPMN có sẵn của draw.io.

Pool/Lane -> swimlane (chứa phần tử, kéo lane thì phần tử đi theo); task/event/gateway/data ->
shape mxgraph.bpmn.*; sequence/message flow/association -> edge có điểm gấp như bản Matplotlib.
"""
import xml.etree.ElementTree as ET

TASK_MARK = {None: "abstract", "user": "user", "manual": "manual", "service": "service",
             "send": "send", "receive": "receive", "script": "script", "rule": "businessRule"}
GW_TYPE = {"x": "exclusive", "+": "parallel", "o": "inclusive", "event": "eventBased"}
EV_OUTLINE = {"start": "standard", "end": "end", "inter": "catching"}


class _Ids:
    def __init__(self):
        self.n = 1

    def __call__(self, prefix="c"):
        self.n += 1
        return f"{prefix}{self.n}"


def to_drawio(d, path, name="BPMN"):
    nid = _Ids()
    mxfile = ET.Element("mxfile", host="drawio", type="device")
    diagram = ET.SubElement(mxfile, "diagram", id="bpmn", name=name)
    model = ET.SubElement(diagram, "mxGraphModel", dx="1400", dy="800", grid="1", gridSize="10",
                          guides="1", tooltips="1", connect="1", arrows="1", fold="1", page="1",
                          pageScale="1", pageWidth=str(int(d.W + 40)), pageHeight=str(int(d.y + 40)),
                          math="0", shadow="0")
    root = ET.SubElement(model, "root")
    ET.SubElement(root, "mxCell", id="0")
    ET.SubElement(root, "mxCell", id="1", parent="0")

    def cell(id_, value, style, parent, x, y, w, h, vertex=True):
        c = ET.SubElement(root, "mxCell", id=id_, value=value, style=style, parent=parent,
                          vertex="1" if vertex else None)
        if not vertex:
            del c.attrib["vertex"]
        ET.SubElement(c, "mxGeometry", x=f"{x:.1f}", y=f"{y:.1f}", width=f"{w:.1f}", height=f"{h:.1f}",
                      **{"as": "geometry"})
        return c

    lab = lambda t: (t or "").replace("\n", "<br>")
    HEAD = d.HEAD
    lane_cells = []        # (cell_id, abs_x, abs_y, w, h)
    pool_cells = {}        # name -> (id, y0, h)

    for it in d.items:
        if it[0] == "pool":
            _, pname, y0, total, lanes = it
            pid = nid("pool")
            cell(pid, pname, "swimlane;html=1;horizontal=0;startSize=%d;fontStyle=1;fontSize=12;"
                 "fillColor=#dfe3e8;swimlaneFillColor=#ffffff;" % HEAD, "1", 0, y0, d.W, total)
            pool_cells[pname] = (pid, y0, total)
            y = y0
            for key, label, h in lanes:
                lid = nid("lane")
                cell(lid, lab(label), "swimlane;html=1;horizontal=0;startSize=%d;fontStyle=0;fontSize=11;"
                     "fillColor=#f2f3f5;swimlaneFillColor=#ffffff;" % HEAD, pid, HEAD, y - y0, d.W - HEAD, h)
                lane_cells.append((lid, HEAD, y, d.W - HEAD, h))
                y += h
        elif it[0] == "blackbox":
            _, pname, y0, h = it
            pid = nid("pool")
            cell(pid, pname, "rounded=0;whiteSpace=wrap;html=1;fontStyle=1;fontSize=13;fillColor=#fafbfc;",
                 "1", 0, y0, d.W, h)
            pool_cells[pname] = (pid, y0, h)

    def lane_of(cx, cy):
        for lid, lx, ly, lw, lh in lane_cells:
            if lx <= cx <= lx + lw and ly <= cy <= ly + lh:
                return lid, lx, ly
        return "1", 0, 0

    ids = {}
    for key, e in d.el.items():
        k = e["kind"]
        if k == "pt":
            continue
        if k == "note":
            x0, y0, w, h = e["x"], e["y"], e["w"], e["h"]
        else:
            x0, y0, w, h = e["x"] - e["w"] / 2, e["y"] - e["h"] / 2, e["w"], e["h"]
        parent, px, py = lane_of(x0 + w / 2, y0 + h / 2)
        rx, ry = x0 - px, y0 - py
        cid = nid(k)
        ids[key] = cid
        if k == "task":
            st = ("shape=mxgraph.bpmn.task;whiteSpace=wrap;html=1;rectStyle=rounded;size=10;fontSize=10;"
                  f"taskMarker={TASK_MARK[e['ttype']]};fillColor={e['fill'] or '#eef4fb'};")
            if e["loop"]:
                st += "isLoopStandard=1;"
            if e["multi"]:
                st += "isLoopMultiParallel=1;"
            if e["sub"]:
                st += "isLoopSub=1;"
            cell(cid, lab(e["text"]), st, parent, rx, ry, w, h)
        elif k == "event":
            outline = EV_OUTLINE[e["pos"]]
            if e["pos"] == "inter" and e["throw"]:
                outline = "throwing"
            sym = e["trig"] or "general"
            if e["pos"] == "end" and sym == "message":
                sym = "message"
            fill = {"start": "#f1f8f1", "end": "#fbeeee"}.get(e["pos"], "#ffffff")
            stroke = {"start": "#2e7d32", "end": "#b71c1c"}.get(e["pos"], "#000000")
            lp = {"b": "verticalLabelPosition=bottom;verticalAlign=top;",
                  "t": "verticalLabelPosition=top;verticalAlign=bottom;",
                  "r": "labelPosition=right;align=left;", "l": "labelPosition=left;align=right;"}[e["lpos"]]
            st = (f"shape=mxgraph.bpmn.event;html=1;outline={outline};symbol={sym};fontSize=9;"
                  f"fillColor={fill};strokeColor={stroke};labelBackgroundColor=none;" + lp)
            cell(cid, lab(e["label"]), st, parent, rx, ry, w, h)
        elif k == "gw":
            lp = "verticalLabelPosition=bottom;verticalAlign=top;" if e["lpos"] in ("b", "bl", "br") else \
                 "verticalLabelPosition=top;verticalAlign=bottom;" if e["lpos"] in ("t", "tl", "tr") else \
                 "labelPosition=right;align=left;"
            st = (f"shape=mxgraph.bpmn.gateway2;html=1;perimeter=rhombusPerimeter;outline=none;symbol=none;"
                  f"gwType={GW_TYPE[e['gtype']]};fillColor=#fff6dc;fontSize=9;" + lp)
            cell(cid, lab(e["label"]), st, parent, rx, ry, w, h)
        elif k == "data":
            st = ("shape=mxgraph.bpmn.data;html=1;size=8;labelPosition=center;verticalLabelPosition=bottom;"
                  "align=center;verticalAlign=top;fontSize=9;fontStyle=2;")
            if e["collection"]:
                st += "isCollection=1;"
            if e["io"] == "in":
                st += "bpmnTransferType=input;"
            elif e["io"] == "out":
                st += "bpmnTransferType=output;"
            cell(cid, lab(e["label"]), st, parent, rx, ry, w, h)
        elif k == "store":
            st = ("shape=datastore;html=1;labelPosition=center;verticalLabelPosition=bottom;align=center;"
                  "verticalAlign=top;fontSize=9;fontStyle=2;")
            cell(cid, lab(e["label"]), st, parent, rx, ry, w, h)
        elif k == "note":
            st = ("shape=partialRectangle;html=1;top=0;bottom=0;right=0;left=1;fillColor=none;align=left;"
                  "verticalAlign=middle;spacingLeft=6;whiteSpace=wrap;fontSize=9;fontColor=#57606a;"
                  "strokeColor=#57606a;")
            cell(cid, lab(e["text"]), st, parent, rx, ry, w, h)

    def anchor_target(pt):
        """Điểm neo vô hình -> nối vào note hoặc pool chứa nó (kèm toạ độ entry tương đối)."""
        px, py = pt
        for key, e in d.el.items():
            if e["kind"] == "note" and e["x"] - 4 <= px <= e["x"] + e["w"] + 4 and e["y"] - 4 <= py <= e["y"] + e["h"] + 4:
                return ids[key], (px - e["x"]) / e["w"], (py - e["y"]) / e["h"]
        for pname, (pid, y0, h) in pool_cells.items():
            if y0 - 2 <= py <= y0 + h + 2:
                return pid, px / d.W, (py - y0) / h
        return None, 0, 0

    for it in d.items:
        if it[0] != "edge":
            continue
        _, a, b, route, label, via, lab_at, lab_dx, lab_dy, src, dst, kind = it
        pts = d._route(a, b, route, via, src, dst, kind)
        if kind == "seq":
            st = "html=1;rounded=0;endArrow=block;endFill=1;endSize=7;fontSize=9;"
        elif kind == "msg":
            st = ("html=1;rounded=0;dashed=1;dashPattern=8 4;endArrow=block;endFill=0;startArrow=oval;"
                  "startFill=0;startSize=6;fontSize=9;")
        else:
            st = "html=1;rounded=0;dashed=1;dashPattern=1 3;strokeColor=#57606a;fontSize=9;"
            st += "endArrow=none;" if d.el[b]["kind"] in ("note", "pt") else "endArrow=open;endFill=0;"
        attrs = {}
        geo_pts = []
        for end, key, p in (("source", a, pts[0]), ("target", b, pts[-1])):
            if d.el[key]["kind"] == "pt":
                tid, fx, fy = anchor_target(p)
                if tid:
                    attrs[end] = tid
                    pre = "exit" if end == "source" else "entry"
                    st += f"{pre}X={fx:.4f};{pre}Y={fy:.4f};{pre}Dx=0;{pre}Dy=0;"
                else:
                    geo_pts.append((end, p))
            else:
                attrs[end] = ids[key]
                # cố định điểm nối đúng cổng ra/vào như bản vẽ Matplotlib
                e = d.el[key]
                fx = (p[0] - (e["x"] - e["w"] / 2)) / e["w"] if e["w"] else 0.5
                fy = (p[1] - (e["y"] - e["h"] / 2)) / e["h"] if e["h"] else 0.5
                if e["kind"] == "note":
                    fx = (p[0] - e["x"]) / e["w"]; fy = (p[1] - e["y"]) / e["h"]
                pre = "exit" if end == "source" else "entry"
                st += f"{pre}X={min(max(fx, 0), 1):.4f};{pre}Y={min(max(fy, 0), 1):.4f};{pre}Dx=0;{pre}Dy=0;"
        eid = nid("edge")
        c = ET.SubElement(root, "mxCell", id=eid, value=lab(label), style=st, parent="1", edge="1", **attrs)
        g = ET.SubElement(c, "mxGeometry", relative="1", **{"as": "geometry"})
        for end, p in geo_pts:
            ET.SubElement(g, "mxPoint", x=f"{p[0]:.1f}", y=f"{p[1]:.1f}",
                          **{"as": "sourcePoint" if end == "source" else "targetPoint"})
        inner = pts[1:-1]
        if inner:
            arr = ET.SubElement(g, "Array", **{"as": "points"})
            for p in inner:
                ET.SubElement(arr, "mxPoint", x=f"{p[0]:.1f}", y=f"{p[1]:.1f}")

    ET.indent(mxfile)
    ET.ElementTree(mxfile).write(path, encoding="utf-8", xml_declaration=False)
