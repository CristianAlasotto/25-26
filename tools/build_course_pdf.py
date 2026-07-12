#!/usr/bin/env python3
from __future__ import annotations

import html
import os
import re
import shutil
import subprocess
import textwrap
from urllib.parse import quote
from dataclasses import dataclass
from pathlib import Path

from PIL import Image
from pypdf import PdfReader, PdfWriter
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    Flowable,
    Image as RLImage,
    KeepTogether,
    PageBreak,
    Paragraph,
    Preformatted,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
TMP = ROOT / "tmp" / "pdfs"
OUT = ROOT / "output" / "pdf"
FINAL = OUT / "complementi-di-reti-materiali-corso.pdf"
COVERAGE = OUT / "complementi-di-reti-materiali-corso_coverage.md"
SOFFICE = Path(
    os.environ.get(
        "SOFFICE",
        "/Users/cristianalasotto/.cache/codex-runtimes/"
        "codex-primary-runtime/dependencies/bin/soffice",
    )
)


@dataclass(frozen=True)
class Source:
    title: str
    path: str | None = None
    kind: str = "pdf"
    note: str = ""
    children: tuple["Source", ...] = ()


COURSE_ORDER: tuple[Source, ...] = (
    Source(
        "1. Introduzione al corso, Docker e Kathara",
        children=(
            Source("Presentazione del corso", "Theory_slides/001_Complementi_di_Reti.pdf"),
            Source("Introduzione a Docker", "Theory_slides/002_Intro_to_Docker.pdf"),
            Source("Introduzione a Kathara", "Theory_slides/003_001-kathara-introduction.pdf"),
            Source("LAB-K1 - Docker hands-on", "LAB-K1/README.md", "markdown"),
            Source("LAB-K2 - Basics on Kathara", "LAB-K2/README.md", "markdown"),
            Source("KaaS - Kathara as a Service", "KaaS/README.md", "markdown"),
        ),
    ),
    Source(
        "2. Connettivita di base, ARP, IPv6 e routing statico",
        children=(
            Source("Due host e connettivita", "Theory_slides/004_two-computers.pdf"),
            Source("Routing statico", "Theory_slides/005_static-routing.pdf"),
            Source(
                "Comandi Linux di rete",
                "Theory_slides/006_Linux Networking Commands_ net-tools vs iproute2.pdf",
            ),
            Source("Laboratorio ARP", "Theory_slides/007_lab_arp.pdf"),
            Source("IPv6 di base", "Theory_slides/008_basic-ipv6.pdf"),
            Source("Traffic control", "Theory_slides/009_tc_traffic_control.pdf"),
            Source("iperf3", "Theory_slides/010_iperf3.pdf"),
            Source("LAB-K3 - Topologie e routing statico", "LAB-K3/README.md", "markdown"),
            Source("LAB-K3B - Variante", "LAB-K3B/README.md", "markdown"),
        ),
    ),
    Source(
        "3. FRRouting e RIP",
        children=(
            Source("FRRouting", "Theory_slides/011_frr.pdf"),
            Source("FRR - slide sorgente convertite", "Theory_slides/006-kathara-lab_frr_GR_V1.pptx", "pptx"),
            Source("RIP", "Theory_slides/012_rip.pdf"),
            Source("RIP - slide sorgente convertite", "Theory_slides/009-kathara-lab_rip_GR_V1.pptx", "pptx"),
            Source("LAB-FRR - Inventario file", "LAB-FRR and RIP/frrouting-introduction", "tree"),
            Source("LAB-RIP - Inventario file", "LAB-FRR and RIP/rip", "tree"),
        ),
    ),
    Source(
        "4. OSPF",
        children=(
            Source("OSPF - teoria", "Theory_slides/lab_ospf_theory.pptx", "pptx"),
            Source("OSPF multi-area", "Theory_slides/014_lab_ospf_areas.pdf"),
            Source("OSPF multi-area - slide sorgente convertite", "Theory_slides/lab_ospf_areas.pptx", "pptx"),
            Source("Chapter 5 Kurose-Ross", "Theory_slides/013_Chapter_5_Kurose_Ross_CN_101.pdf"),
            Source("LAB-OSPF I", "LAB_RIP_II_OSPF/LAB_OSPF_I.md", "markdown"),
            Source("LAB-OSPF II", "LAB_RIP_II_OSPF/LAB_OSPF_II.md", "markdown"),
        ),
    ),
    Source(
        "5. BGP e data center",
        children=(
            Source("Introduzione a BGP", "Theory_slides/015_BGP_intro.pdf"),
            Source("BGP stubs", "Theory_slides/016_BGP_stubs.pdf"),
            Source("BGP data center", "Theory_slides/017_BGP_datacenter.pdf"),
            Source("LAB-K4 - BGP", "LAB-K4/README.md", "markdown"),
            Source("LAB BGP simple peering", "LAB-K4/bgp-simple-peering/041-kathara-lab_bgp-simple-peering.pdf"),
            Source("LAB BGP announcement", "LAB-K4/bgp-announcement/042-kathara-lab_bgp-announcement.pdf"),
            Source("LAB-K5 - Routing e policy", "LAB-K5/README.md", "markdown"),
            Source("LAB-K6 - Data center BGP", "LAB-K6/README.md", "markdown"),
            Source("LAB data center BGP", "LAB-K6/data-center-bgp/051-kathara-lab_data-center-bgp.pdf"),
            Source("LAB data center BGP - slide sorgente convertite", "LAB-K6/data-center-bgp/051-kathara-lab_data-center-bgp.pptx", "pptx"),
            Source("LAB-K7 - Load balancing", "LAB-K7/README.md", "markdown"),
            Source("Load balancing", "Theory_slides/019_load_balancing.pdf"),
        ),
    ),
    Source(
        "6. Trasporto, QUIC e congestion control",
        children=(
            Source("Transport layer - parte 1", "Theory_slides/Transport layer Compreti_Part_1.pptx", "pptx"),
            Source("Transport layer - parte 2", "Theory_slides/Transport layer Compreti part 2.pptx", "pptx"),
            Source(
                "Rate adaptation, congestion control and fairness",
                "Theory_slides/018_Rate adaptation, Congestion Control and Fairness_ A Tutorial.pdf",
            ),
            Source("LAB congestion control - introduzione", "LAB-CongestionControl/README.md", "markdown"),
            Source("LAB congestion control - scenari", "LAB-CongestionControl/lab/README.md", "markdown"),
        ),
    ),
)


EXCLUDED = (
    ("Appunti completi complementi di reti.pdf", "appunti non ufficiali di altri studenti"),
    ("Laboratorio completi.pdf", "relazione/appunti non ufficiali di laboratorio"),
    ("LAB-K2/K2-intro/001-kathara-introduction.pdf", "duplicato dell'introduzione a Kathara in Theory_slides"),
    ("LAB-K4/2bgp-announcement/042-kathara-lab_bgp-announcement.pdf", "duplicato del lab BGP announcement"),
    ("LAB-K4/Figs/LABK4.pdf", "figura di supporto gia coperta da README/lab BGP"),
    ("LAB-K3/Figs/net-architecture-2.drawio.pdf", "figura di supporto gia coperta da README LAB-K3"),
)


class HR(Flowable):
    def __init__(self, width: float, color=colors.HexColor("#b7c0cc")):
        super().__init__()
        self.width = width
        self.height = 1
        self.color = color

    def draw(self):
        self.canv.setStrokeColor(self.color)
        self.canv.setLineWidth(0.8)
        self.canv.line(0, 0, self.width, 0)


def styles():
    base = getSampleStyleSheet()
    base.add(
        ParagraphStyle(
            "CoverTitle",
            parent=base["Title"],
            fontName="Helvetica-Bold",
            fontSize=26,
            leading=32,
            alignment=TA_CENTER,
            spaceAfter=18,
            textColor=colors.HexColor("#14213d"),
        )
    )
    base.add(
        ParagraphStyle(
            "CoverSub",
            parent=base["Normal"],
            fontSize=12,
            leading=16,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#334155"),
        )
    )
    base.add(
        ParagraphStyle(
            "SectionTitle",
            parent=base["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=22,
            leading=28,
            spaceAfter=14,
            textColor=colors.HexColor("#14213d"),
        )
    )
    base.add(
        ParagraphStyle(
            "DocTitle",
            parent=base["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=15,
            leading=19,
            spaceBefore=12,
            spaceAfter=8,
            textColor=colors.HexColor("#1f2937"),
        )
    )
    base.add(
        ParagraphStyle(
            "Body",
            parent=base["Normal"],
            fontSize=9.2,
            leading=12.5,
            spaceAfter=5,
            alignment=TA_LEFT,
        )
    )
    base.add(
        ParagraphStyle(
            "Small",
            parent=base["Normal"],
            fontSize=8,
            leading=10.5,
            textColor=colors.HexColor("#475569"),
        )
    )
    base.add(
        ParagraphStyle(
            "CodeBlock",
            parent=base["Code"],
            fontName="Courier",
            fontSize=7.2,
            leading=9,
            leftIndent=8,
            rightIndent=4,
            borderColor=colors.HexColor("#d9e2ec"),
            borderWidth=0.4,
            borderPadding=5,
            backColor=colors.HexColor("#f8fafc"),
            spaceBefore=3,
            spaceAfter=7,
        )
    )
    return base


def header_footer(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(colors.HexColor("#64748b"))
    canvas.setFont("Helvetica", 7.5)
    canvas.drawString(doc.leftMargin, 0.75 * cm, "Complementi di Reti - compendio materiali ufficiali")
    canvas.drawRightString(A4[0] - doc.rightMargin, 0.75 * cm, str(canvas.getPageNumber()))
    canvas.restoreState()


def build_pdf(path: Path, story: list) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(path),
        pagesize=A4,
        leftMargin=1.55 * cm,
        rightMargin=1.55 * cm,
        topMargin=1.55 * cm,
        bottomMargin=1.25 * cm,
    )
    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)


def clean_inline(text: str) -> str:
    text = html.escape(text)
    text = re.sub(r"`([^`]+)`", r"<font name='Courier'>\1</font>", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"__([^_]+)__", r"<b>\1</b>", text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"\1", text)
    return text


def add_wrapped_code(story: list, code: str, style: ParagraphStyle) -> None:
    lines = []
    for line in code.rstrip("\n").splitlines() or [""]:
        lines.extend(textwrap.wrap(line, width=92, replace_whitespace=False, drop_whitespace=False) or [""])
    story.append(Preformatted("\n".join(lines), style))


def local_image(markdown_file: Path, image_ref: str) -> Path | None:
    if image_ref.startswith(("http://", "https://", "data:")):
        return None
    img = (markdown_file.parent / image_ref).resolve()
    try:
        img.relative_to(ROOT)
    except ValueError:
        return None
    return img if img.exists() else None


def image_flowable(image_path: Path) -> RLImage | None:
    try:
        with Image.open(image_path) as im:
            width, height = im.size
        max_w = A4[0] - 3.1 * cm
        max_h = 10.5 * cm
        scale = min(max_w / width, max_h / height, 1.0)
        return RLImage(str(image_path), width=width * scale, height=height * scale)
    except Exception:
        return None


def markdown_to_pdf(src: Path, dst: Path, title: str) -> None:
    st = styles()
    text = src.read_text(encoding="utf-8", errors="replace")
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    story: list = [Paragraph(title, st["SectionTitle"]), Paragraph(str(src.relative_to(ROOT)), st["Small"]), Spacer(1, 8)]
    in_code = False
    code_lines: list[str] = []
    pending: list[str] = []

    def flush_pending():
        nonlocal pending
        if not pending:
            return
        para = " ".join(x.strip() for x in pending if x.strip())
        if para:
            story.append(Paragraph(clean_inline(para), st["Body"]))
        pending = []

    for raw in text.splitlines():
        line = raw.rstrip()
        if line.strip().startswith("```") or line.strip().startswith("~~~"):
            if in_code:
                add_wrapped_code(story, "\n".join(code_lines), st["CodeBlock"])
                code_lines = []
                in_code = False
            else:
                flush_pending()
                in_code = True
            continue
        if in_code:
            code_lines.append(line)
            continue

        image_match = re.match(r"\s*!\[[^\]]*\]\(([^)]+)\)", line)
        html_image_match = re.search(r"<img[^>]+src=[\"']([^\"']+)[\"']", line)
        if image_match or html_image_match:
            flush_pending()
            ref = (image_match or html_image_match).group(1)
            img = local_image(src, ref)
            flow = image_flowable(img) if img else None
            if flow:
                story.append(flow)
                story.append(Spacer(1, 6))
            else:
                story.append(Paragraph(f"[immagine esterna o non disponibile: {html.escape(ref)}]", st["Small"]))
            continue

        if not line.strip():
            flush_pending()
            continue
        if line.startswith("#"):
            flush_pending()
            level = len(line) - len(line.lstrip("#"))
            content = line[level:].strip()
            style = st["DocTitle"] if level <= 2 else st["Body"]
            story.append(Paragraph(clean_inline(content), style))
            continue
        if re.match(r"\s*[-+*]\s+", line):
            flush_pending()
            item = re.sub(r"\s*[-+*]\s+", "", line, count=1)
            story.append(Paragraph("&bull; " + clean_inline(item), st["Body"]))
            continue
        if re.match(r"\s*\d+[.)]\s+", line):
            flush_pending()
            story.append(Paragraph(clean_inline(line), st["Body"]))
            continue
        if "|" in line and line.strip().startswith("|"):
            flush_pending()
            add_wrapped_code(story, line, st["CodeBlock"])
            continue
        pending.append(line)

    flush_pending()
    if code_lines:
        add_wrapped_code(story, "\n".join(code_lines), st["CodeBlock"])
    build_pdf(dst, story)


def tree_to_pdf(src: Path, dst: Path, title: str) -> None:
    st = styles()
    story: list = [Paragraph(title, st["SectionTitle"]), Paragraph(str(src.relative_to(ROOT)), st["Small"]), Spacer(1, 8)]
    files = sorted(p for p in src.rglob("*") if p.is_file() and ".DS_Store" not in p.name)
    rels = [str(p.relative_to(ROOT)) for p in files]
    story.append(
        Paragraph(
            "Inventario dei file del laboratorio Kathara. I file restano disponibili nella repository; qui sono elencati per copertura del materiale ufficiale.",
            st["Body"],
        )
    )
    add_wrapped_code(story, "\n".join(rels), st["CodeBlock"])
    build_pdf(dst, story)


def simple_page(path: Path, title: str, paragraphs: list[str], table_rows: list[tuple[str, str]] | None = None) -> None:
    st = styles()
    story: list = [Spacer(1, 4 * cm), Paragraph(title, st["CoverTitle"])]
    for paragraph in paragraphs:
        story.append(Paragraph(clean_inline(paragraph), st["CoverSub"]))
        story.append(Spacer(1, 8))
    if table_rows:
        data = [[Paragraph(clean_inline(a), st["Small"]), Paragraph(clean_inline(b), st["Small"])] for a, b in table_rows]
        table = Table(data, colWidths=[6.2 * cm, 9.7 * cm], hAlign="CENTER")
        table.setStyle(
            TableStyle(
                [
                    ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#d9e2ec")),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
                    ("LEFTPADDING", (0, 0), (-1, -1), 6),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                    ("TOPPADDING", (0, 0), (-1, -1), 5),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ]
            )
        )
        story.append(Spacer(1, 8))
        story.append(table)
    build_pdf(path, story)


def toc_pdf(path: Path, included: list[tuple[str, str, str]], missing: list[tuple[str, str]]) -> None:
    st = styles()
    story: list = [Paragraph("Indice e copertura", st["SectionTitle"])]
    story.append(
        Paragraph(
            "Il documento segue l'ordine logico del corso. Ogni sezione ha un separatore e un segnalibro PDF; i numeri di pagina interni delle slide originali sono preservati.",
            st["Body"],
        )
    )
    story.append(Spacer(1, 6))
    rows = [("Sezione", "Tipo", "Fonte")]
    rows += included
    table = Table(
        [[Paragraph(clean_inline(a), st["Small"]), Paragraph(clean_inline(b), st["Small"]), Paragraph(clean_inline(c), st["Small"])] for a, b, c in rows],
        colWidths=[5.4 * cm, 2.1 * cm, 8.4 * cm],
        repeatRows=1,
    )
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e2e8f0")),
                ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#cbd5e1")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    story.append(table)
    story.append(PageBreak())
    story.append(Paragraph("Materiali esclusi intenzionalmente", st["DocTitle"]))
    story.append(Paragraph("Questi file sono presenti nella repository ma non sono stati inseriti nel compendio principale:", st["Body"]))
    rows2 = [("File", "Motivo")] + list(EXCLUDED) + missing
    table2 = Table(
        [[Paragraph(clean_inline(a), st["Small"]), Paragraph(clean_inline(b), st["Small"])] for a, b in rows2],
        colWidths=[6.5 * cm, 9.4 * cm],
        repeatRows=1,
    )
    table2.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e2e8f0")),
                ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#cbd5e1")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ]
        )
    )
    story.append(table2)
    build_pdf(path, story)


def convert_pptx(src: Path, out_dir: Path) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    expected = out_dir / f"{src.stem}.pdf"
    if expected.exists() and expected.stat().st_mtime >= src.stat().st_mtime:
        return expected
    profile = TMP / "lo-profile"
    profile.mkdir(parents=True, exist_ok=True)
    profile_uri = "file://" + quote(str(profile))
    subprocess.run(
        [
            str(SOFFICE),
            f"-env:UserInstallation={profile_uri}",
            "--headless",
            "--convert-to",
            "pdf",
            "--outdir",
            str(out_dir),
            str(src),
        ],
        cwd=str(ROOT),
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if not expected.exists():
        matches = sorted(out_dir.glob(src.stem + "*.pdf"))
        if matches:
            return matches[0]
        raise FileNotFoundError(f"Conversione PPTX non riuscita: {src}")
    return expected


def count_pages(path: Path) -> int:
    return len(PdfReader(str(path)).pages)


def source_pdf(src: Source, slug: str) -> Path:
    assert src.path
    path = ROOT / src.path
    if src.kind == "pdf":
        return path
    if src.kind == "pptx":
        return convert_pptx(path, TMP / "converted_pptx")
    if src.kind == "markdown":
        dst = TMP / "markdown" / f"{slug}.pdf"
        markdown_to_pdf(path, dst, src.title)
        return dst
    if src.kind == "tree":
        dst = TMP / "trees" / f"{slug}.pdf"
        tree_to_pdf(path, dst, src.title)
        return dst
    raise ValueError(src.kind)


def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")[:80]


def add_pdf(writer: PdfWriter, pdf_path: Path) -> int:
    reader = PdfReader(str(pdf_path))
    for page in reader.pages:
        writer.add_page(page)
    return len(reader.pages)


def build() -> None:
    TMP.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    parts: list[tuple[str, Path, int, int]] = []
    included: list[tuple[str, str, str]] = []
    missing: list[tuple[str, str]] = []

    cover = TMP / "cover.pdf"
    simple_page(
        cover,
        "Complementi di Reti",
        [
            "Compendio ordinato dei materiali ufficiali del corso 2025-2026.",
            "Ordine proposto: prerequisiti e strumenti, routing statico, protocolli dinamici, OSPF, BGP/data center, trasporto e congestion control.",
        ],
    )
    parts.append(("Copertina", cover, 0, count_pages(cover)))

    for section in COURSE_ORDER:
        assert section.children
        for child in section.children:
            if child.path and not (ROOT / child.path).exists():
                missing.append((child.path, "file indicato nella scaletta ma non trovato"))
            else:
                included.append((section.title, child.kind.upper(), child.path or child.title))

    toc = TMP / "toc.pdf"
    toc_pdf(toc, included, missing)
    parts.append(("Indice e copertura", toc, 0, count_pages(toc)))

    for section_index, section in enumerate(COURSE_ORDER, start=1):
        divider = TMP / "sections" / f"{section_index:02d}-{slugify(section.title)}.pdf"
        simple_page(
            divider,
            section.title,
            [
                "Materiali inclusi in questa sezione:",
                "; ".join(child.title for child in section.children),
            ],
        )
        parts.append((section.title, divider, 0, count_pages(divider)))
        for child_index, child in enumerate(section.children, start=1):
            if not child.path or not (ROOT / child.path).exists():
                continue
            pdf_path = source_pdf(child, f"{section_index:02d}-{child_index:02d}-{slugify(child.title)}")
            parts.append((child.title, pdf_path, 1, count_pages(pdf_path)))

    writer = PdfWriter()
    outline_items: list[tuple[str, int, int]] = []
    current_page = 0
    for title, pdf_path, level, pages in parts:
        outline_items.append((title, current_page, level))
        add_pdf(writer, pdf_path)
        current_page += pages

    for title, page, level in outline_items:
        writer.add_outline_item(title, page, parent=None if level == 0 else None)
    writer.add_metadata(
        {
            "/Title": "Complementi di Reti - materiali ufficiali del corso",
            "/Author": "Repository compl-reti-unito/25-26",
            "/Subject": "Compendio ordinato di slide, laboratori e materiali ufficiali",
        }
    )
    with FINAL.open("wb") as fh:
        writer.write(fh)

    coverage_lines = [
        "# Complementi di Reti - copertura materiali",
        "",
        f"PDF finale: `{FINAL.relative_to(ROOT)}`",
        f"Pagine totali: {count_pages(FINAL)}",
        "",
        "## Materiali inclusi",
        "",
    ]
    for section in COURSE_ORDER:
        coverage_lines.append(f"### {section.title}")
        for child in section.children:
            status = "OK" if child.path and (ROOT / child.path).exists() else "MANCANTE"
            coverage_lines.append(f"- [{status}] {child.title}: `{child.path}` ({child.kind})")
        coverage_lines.append("")
    coverage_lines.extend(["## Esclusi", ""])
    for file_name, reason in EXCLUDED:
        coverage_lines.append(f"- `{file_name}` - {reason}")
    if missing:
        coverage_lines.extend(["", "## Mancanti", ""])
        for file_name, reason in missing:
            coverage_lines.append(f"- `{file_name}` - {reason}")
    COVERAGE.write_text("\n".join(coverage_lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    build()
