#!/usr/bin/env python3
"""Build a Vietnamese brokerage-style mining analysis memo (.docx) from data.json.

Usage:  python build_memo.py data.json output.docx

Requires python-docx:  pip install python-docx --break-system-packages
Structure: title band → context → 2 principles → 6 criteria → comparison table →
conclusions & ranking → next steps → disclaimer. No house name / no addressee, to
match the concise style of Vietnamese securities-firm research notes.
"""
import json, sys
from docx import Document
from docx.shared import Pt, RGBColor, Twips
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

FONT = "Times New Roman"
NAVY = RGBColor(0x1F, 0x38, 0x64)
BLUE = RGBColor(0x2E, 0x54, 0x96)
GREY = RGBColor(0x66, 0x66, 0x66)

CRITERIA = [
    ("reserves",   "3.1. Trữ lượng & tuổi thọ mỏ",
     "Chúng tôi xem đây là yếu tố nền tảng: trữ lượng, tỷ lệ Trữ lượng/Sản lượng (đời mỏ) và khả năng thay thế quyết định tính bền vững của dòng lợi nhuận."),
    ("production", "3.2. Sản lượng khai thác",
     "Sản lượng phản ánh quy mô thực và cho phép tách bạch tăng trưởng đến từ sản lượng hay từ giá bán."),
    ("margin",     "3.3. Biên lợi nhuận",
     "Biên lợi nhuận là chỉ báo cho vị thế chi phí; doanh nghiệp chi phí thấp có khả năng trụ vững khi giá hàng hóa điều chỉnh."),
    ("fcf",        "3.4. Dòng tiền tự do (FCF)",
     "Do đặc thù thâm dụng vốn, chúng tôi ưu tiên dòng tiền tự do sau capex duy trì hơn là EBITDA hay lợi nhuận kế toán."),
    ("debt",       "3.5. Nợ & bảng cân đối",
     "Đòn bẩy cao đi cùng lợi nhuận biến động theo giá hàng hóa làm gia tăng rủi ro tài chính, đặc biệt tại pha giảm giá."),
    ("valuation",  "3.6. Định giá",
     "Chúng tôi ưu tiên EV/EBITDA và P/NAV hơn P/E đơn thuần do lợi nhuận mang tính chu kỳ và khấu hao lớn."),
]


def set_cell_bg(cell, hexcolor):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear"); shd.set(qn("w:color"), "auto"); shd.set(qn("w:fill"), hexcolor)
    tcPr.append(shd)


def set_cell_borders(cell):
    tcPr = cell._tc.get_or_add_tcPr()
    borders = OxmlElement("w:tcBorders")
    for edge in ("top", "left", "bottom", "right"):
        e = OxmlElement(f"w:{edge}")
        e.set(qn("w:val"), "single"); e.set(qn("w:sz"), "4"); e.set(qn("w:color"), "AAB4C4")
        borders.append(e)
    tcPr.append(borders)


def style_cell(cell, text, size=8.5, bold=False, color=None, fill=None, align="left"):
    cell.text = ""
    p = cell.paragraphs[0]
    p.alignment = {"left": WD_ALIGN_PARAGRAPH.LEFT, "center": WD_ALIGN_PARAGRAPH.CENTER}[align]
    run = p.add_run(str(text))
    run.font.name = FONT; run.font.size = Pt(size); run.font.bold = bold
    if color: run.font.color.rgb = color
    if fill: set_cell_bg(cell, fill)
    set_cell_borders(cell)


def add_para(doc, runs, size=11, after=6, align=None, italic=False, color=None):
    """runs = str OR list of (text, bold) tuples."""
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(after)
    if align == "center": p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    if isinstance(runs, str):
        runs = [(runs, False)]
    for text, bold in runs:
        r = p.add_run(text)
        r.font.name = FONT; r.font.size = Pt(size); r.font.bold = bold; r.font.italic = italic
        if color: r.font.color.rgb = color
    return p


def add_heading(doc, text, size=13, color=NAVY, before=12, after=6):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(before); p.paragraph_format.space_after = Pt(after)
    r = p.add_run(text); r.font.name = FONT; r.font.size = Pt(size); r.font.bold = True; r.font.color.rgb = color
    return p


def hrule(doc, color="1F3864", size=12, after=8):
    p = doc.add_paragraph(); p.paragraph_format.space_after = Pt(after)
    pPr = p._p.get_or_add_pPr(); pbdr = OxmlElement("w:pBdr")
    bottom = OxmlElement("w:bottom")
    bottom.set(qn("w:val"), "single"); bottom.set(qn("w:sz"), str(size))
    bottom.set(qn("w:space"), "1"); bottom.set(qn("w:color"), color)
    pbdr.append(bottom); pPr.append(pbdr)


def main(data_path, out_path):
    with open(data_path, encoding="utf-8") as f:
        d = json.load(f)
    companies = d["companies"]
    notes = d.get("criteria_notes", {})

    doc = Document()
    doc.styles["Normal"].font.name = FONT
    doc.styles["Normal"].font.size = Pt(11)
    for s in doc.sections:
        s.top_margin = s.bottom_margin = Twips(1134)
        s.left_margin = s.right_margin = Twips(1134)

    # Title band
    add_para(doc, [(d.get("sector_title", "NGÀNH KHOÁNG SẢN"), True)], size=15, after=2, align="center", color=NAVY)
    add_para(doc, [(d.get("subtitle", ""), True)], size=11.5, after=2, align="center")
    add_para(doc, [(" · ".join(c["ticker"] for c in companies), True)], size=10.5, after=2, align="center", color=BLUE)
    add_para(doc, f"Báo cáo phân tích  |  {d.get('report_date','')}  |  Số liệu tại {d.get('data_date','')}",
             size=9, after=2, align="center", italic=True, color=GREY)
    hrule(doc)

    # 1. Context
    add_heading(doc, "1. Bối cảnh")
    for para in d.get("context", []):
        add_para(doc, para)

    # 2. Principles
    add_heading(doc, "2. Hai đặc thù khi định giá")
    add_para(doc, [
        ("Doanh nghiệp khoáng sản là ", False), ("tài sản cạn kiệt dần", True),
        (" (mỗi tấn khai thác là một tấn trữ lượng mất đi) và phần lớn ", False),
        ("chấp nhận giá", True),
        (" (lợi nhuận do giá hàng hóa chi phối). Do đó thứ tự đánh giá đúng: mỏ còn khai thác bao lâu → chi phí có đủ thấp → dòng tiền thực sau đầu tư → bảng cân đối chịu được đáy giá → rồi mới đến định giá.", False),
    ])

    # 3. Six criteria
    add_heading(doc, "3. Sáu tiêu chí then chốt")
    for key, label, why in CRITERIA:
        add_heading(doc, label, size=11.5, color=BLUE, before=8, after=3)
        note = notes.get(key)
        add_para(doc, (why + " " + note) if note else why)

    doc.add_page_break()

    # 4. Comparison table
    add_heading(doc, "4. Bảng tổng hợp so sánh")
    add_para(doc, f"Số liệu tại {d.get('data_date','')}; đơn vị giá trị: VND.", size=9, italic=True, color=GREY, after=5)
    headers = ["Mã", "Trữ lượng & đời mỏ", "Sản lượng/năm", "Biên LN ròng", "FCF & Nợ", "ROE", "P/E · EV/EBITDA"]
    widths = [820, 1560, 1500, 1180, 1560, 900, 1120]  # twips, sum ~8640
    table = doc.add_table(rows=1 + len(companies), cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    for j, h in enumerate(headers):
        style_cell(table.rows[0].cells[j], h, size=9, bold=True, color=RGBColor(0xFF, 0xFF, 0xFF), fill="2E5496", align="center")
    for i, comp in enumerate(companies):
        row = table.rows[i + 1].cells
        fill = "F2F5FA" if i % 2 == 0 else None
        vals = [comp.get("ticker", ""), comp.get("reserves", ""), comp.get("production", ""),
                comp.get("net_margin", ""), comp.get("fcf_debt", ""), comp.get("roe", ""),
                f"{comp.get('pe','')} · {comp.get('ev_ebitda','')}"]
        for j, v in enumerate(vals):
            style_cell(row[j], v, size=8.5, bold=(j == 0), fill=fill)
    for j, w in enumerate(widths):
        for row in table.rows:
            row.cells[j].width = Twips(w)

    # 5. Conclusions
    add_heading(doc, "5. Kết luận & thứ tự ưu tiên")
    add_para(doc, "Trên cơ sở tổng hợp sáu tiêu chí (trọng số cao dành cho trữ lượng, biên lợi nhuận và dòng tiền), chúng tôi xếp thứ tự ưu tiên như sau:")
    for c in d.get("conclusions", []):
        add_para(doc, [(f"{c.get('ticker','')} — ", True), (c.get("note", ""), False)])

    # Disclaimer
    hrule(doc, color="AAB4C4", size=6, after=6)
    disc = ("Tài liệu chỉ nhằm mục đích tham khảo, không phải khuyến nghị mua/bán. Số liệu tổng hợp từ "
            "công bố của doanh nghiệp và nhà cung cấp dữ liệu thị trường" +
            (f" tại {d.get('data_date','')}" if d.get("data_date") else "") +
            "; một số chỉ tiêu vận hành (giá thành đơn vị, trữ lượng chi tiết) cần đối chiếu báo cáo "
            "thường niên/kiểm toán. Đầu tư khoáng sản chịu rủi ro cao từ biến động giá hàng hóa.")
    if d.get("sources"):
        disc += " Nguồn: " + d["sources"]
    add_para(doc, disc, size=8.5, italic=True, color=GREY)

    doc.save(out_path)
    print(f"saved {out_path}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python build_memo.py data.json output.docx"); sys.exit(1)
    main(sys.argv[1], sys.argv[2])
