#!/usr/bin/env python3
"""
Generate publication-grade vector PDF figures for the manuscript:
Academic Monochrome / True Grayscale Theme (Top CS/AI Systems Standard):
- 100% Monochrome & Grayscale: Perfectly compliant with B&W laser printing and strict reviewers
- Standard System Architecture Schematics:
  * Figure 1: Pipeline Flow with document stack icons, sidecar branching, audit checkpoint gate, and integrated findings
  * Figure 2: System Architecture with 3D database cylinders (ChromaDB), parallel simultaneous dispatch (no diamond bug!), hybrid fusion, and prompt packaging
  * Figure 3: Pure monochrome bar chart with solid black vs. diagonal hatched bars
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle, Ellipse

def setup_matplotlib():
    plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Helvetica', 'Arial']
    plt.rcParams['axes.edgecolor'] = '#1E293B'
    plt.rcParams['axes.linewidth'] = 0.9

def draw_cylinder(ax, x, y, w, h, facecolor='#FFFFFF', top_facecolor='#E2E8F0', edgecolor='#1E293B', linewidth=1.2):
    """Draw a 3D-style database cylinder icon."""
    eh = h * 0.18  # ellipse height
    bot_el = Ellipse((x + w/2, y + eh/2), w, eh, facecolor=facecolor, edgecolor=edgecolor, linewidth=linewidth)
    ax.add_patch(bot_el)
    body = Rectangle((x, y + eh/2), w, h - eh, facecolor=facecolor, edgecolor='none')
    ax.add_patch(body)
    ax.plot([x, x], [y + eh/2, y + h - eh/2], color=edgecolor, linewidth=linewidth)
    ax.plot([x + w, x + w], [y + eh/2, y + h - eh/2], color=edgecolor, linewidth=linewidth)
    top_el = Ellipse((x + w/2, y + h - eh/2), w, eh, facecolor=top_facecolor, edgecolor=edgecolor, linewidth=linewidth)
    ax.add_patch(top_el)

def draw_doc_stack(ax, x, y, w, h, count=3, offset=0.8, facecolor='#FFFFFF', edgecolor='#1E293B', linewidth=1.1):
    """Draw a stacked documents icon."""
    sw = w - (count - 1) * offset
    sh = h - (count - 1) * offset
    for i in range(count - 1, -1, -1):
        ox = x + i * offset
        oy = y + (count - 1 - i) * offset
        rect = FancyBboxPatch((ox, oy), sw, sh,
                              boxstyle="round,pad=0.1,rounding_size=0.4",
                              facecolor=facecolor, edgecolor=edgecolor, linewidth=linewidth)
        ax.add_patch(rect)
        if i == 0:
            for ly in [0.72, 0.52, 0.32]:
                ax.plot([ox + sw * 0.2, ox + sw * 0.8], [oy + sh * ly, oy + sh * ly], color='#64748B', lw=1.0)

def draw_pill(ax, x, y, w, h, text, facecolor='#F1F5F9', edgecolor='#475569', text_color='#0F172A', fontsize=7.2, bold=True):
    """Draw a compact label pill."""
    pill = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.15,rounding_size=0.4",
                          facecolor=facecolor, edgecolor=edgecolor, linewidth=0.9)
    ax.add_patch(pill)
    ax.text(x + w/2, y + h/2, text, ha='center', va='center', fontsize=fontsize,
            fontweight='bold' if bold else 'normal', color=text_color)


def generate_figure_1(output_paths):
    """
    Figure 1: End-to-End Multi-Document Knowledge Arbitration and Governance Workflow
    Pure Academic Monochrome Pipeline Flow Diagram.
    """
    fig, ax = plt.subplots(figsize=(15.8, 6.8), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Canvas Background
    bg = FancyBboxPatch((0.5, 0.5), 99, 99, boxstyle="round,pad=0.2",
                        facecolor="#FFFFFF", edgecolor="#CBD5E1", linewidth=1.2)
    ax.add_patch(bg)

    # Top Header Ribbon (Monochrome)
    head_ribbon = FancyBboxPatch((1.5, 92), 97, 6.8, boxstyle="round,pad=0.2",
                                 facecolor="#F8FAFC", edgecolor="#475569", linewidth=1.0)
    ax.add_patch(head_ribbon)
    # Left accent bar (solid dark slate)
    ax.add_patch(FancyBboxPatch((1.5, 92), 1.0, 6.8, boxstyle="round,pad=0.05", facecolor="#0F172A", edgecolor="none"))
    ax.text(50, 96.2, "MULTI-DOCUMENT KNOWLEDGE ARBITRATION & GOVERNANCE PIPELINE",
            ha='center', va='center', fontsize=11.5, fontweight='bold', color='#0F172A')
    ax.text(50, 93.6, "Separating Ingestion (L1), Multimodal Sidecar Enrichment (Step 0), Scope-Aware SSoT Distillation (L2), and Fresh-Session Review (L3)",
            ha='center', va='center', fontsize=8.0, color='#475569')

    # ==========================================
    # STAGE 1: RAW CORPUS & LAYER 1 INGESTION
    # ==========================================
    col1_x, col1_w = 2.0, 20.5
    ax.add_patch(FancyBboxPatch((col1_x, 13.5), col1_w, 76.5, boxstyle="round,pad=0.2",
                                facecolor="#FAFAFA", edgecolor="#94A3B8", linewidth=1.0))
    
    # Header
    ax.add_patch(FancyBboxPatch((col1_x, 84.0), col1_w, 6.0, boxstyle="round,pad=0.1",
                                facecolor="#0F172A", edgecolor="none"))
    ax.text(col1_x + col1_w/2, 87.0, "Layer 1: Physical Ingestion",
            ha='center', va='center', fontsize=9.2, fontweight='bold', color='#FFFFFF')
    ax.text(col1_x + col1_w/2, 82.0, "Module: docling-skill",
            ha='center', va='center', fontsize=7.5, fontweight='bold', color='#475569')

    # Graphic: Document Stack
    draw_doc_stack(ax, col1_x + 7.2, 71.5, 6.0, 8.0, count=3, offset=0.8, facecolor="#FFFFFF", edgecolor="#1E293B")
    ax.text(col1_x + col1_w/2, 68.5, "27 Heterogeneous Files", ha='center', va='center', fontsize=8.2, fontweight='bold', color='#0F172A')
    ax.text(col1_x + col1_w/2, 66.5, "• 16 Finance & Budget forms\n• 10 Admin Oversight reports\n• 1 Technical R&D spec\n• 92 embedded images",
            ha='center', va='top', fontsize=7.0, color='#334155', linespacing=1.3)

    # Engine Box
    eng1 = FancyBboxPatch((col1_x + 1.2, 33.5), col1_w - 2.4, 20.0, boxstyle="round,pad=0.2",
                          facecolor="#FFFFFF", edgecolor="#64748B", linewidth=0.9)
    ax.add_patch(eng1)
    ax.text(col1_x + col1_w/2, 50.0, "Physical Layout Normalizer", ha='center', va='center', fontsize=7.8, fontweight='bold', color='#0F172A')
    ax.text(col1_x + col1_w/2, 47.5, "• Clean CJK character spacing\n• Preserve table cell grids\n• Extract embedded figures\n• Log structural manifest",
            ha='center', va='top', fontsize=7.0, color='#475569', linespacing=1.3)

    # Contractual Outputs
    draw_pill(ax, col1_x + 1.5, 23.5, col1_w - 3.0, 5.5, "source.md (Immutable)", facecolor="#F1F5F9", edgecolor="#334155", text_color="#0F172A")
    draw_pill(ax, col1_x + 1.5, 16.0, col1_w - 3.0, 5.5, "source.manifest.json", facecolor="#F8FAFC", edgecolor="#94A3B8", text_color="#475569")

    # ==========================================
    # STAGE 2: STEP ZERO (MULTIMODAL SIDECAR)
    # ==========================================
    col2_x, col2_w = 27.0, 21.0
    ax.add_patch(FancyBboxPatch((col2_x, 13.5), col2_w, 76.5, boxstyle="round,pad=0.2",
                                facecolor="#FAFAFA", edgecolor="#94A3B8", linewidth=1.0))
    
    # Header
    ax.add_patch(FancyBboxPatch((col2_x, 84.0), col2_w, 6.0, boxstyle="round,pad=0.1",
                                facecolor="#1E293B", edgecolor="none"))
    ax.text(col2_x + col2_w/2, 87.0, "Step Zero: Vision Sidecar",
            ha='center', va='center', fontsize=9.2, fontweight='bold', color='#FFFFFF')
    ax.text(col2_x + col2_w/2, 82.0, "Module: scan_image_placeholders.py",
            ha='center', va='center', fontsize=7.5, fontweight='bold', color='#475569')

    # Immutability Rule Banner
    draw_pill(ax, col2_x + 1.2, 74.0, col2_w - 2.4, 5.2, "Preserve L1 Immutability (DEC-003)", facecolor="#F1F5F9", edgecolor="#334155", text_color="#0F172A", fontsize=6.8)

    # Inspection Box
    eng2 = FancyBboxPatch((col2_x + 1.2, 47.0), col2_w - 2.4, 24.5, boxstyle="round,pad=0.2",
                          facecolor="#FFFFFF", edgecolor="#64748B", linewidth=0.9)
    ax.add_patch(eng2)
    ax.text(col2_x + col2_w/2, 68.0, "Vision Agent Triage", ha='center', va='center', fontsize=7.8, fontweight='bold', color='#0F172A')
    ax.text(col2_x + col2_w/2, 65.0, "• 48 decorative logos skipped\n  (explicitly logged to skip.json)\n• 44 tables & charts inspected\n• Resolves non-OCR raster scans\n• Recovers unlisted quotes",
            ha='center', va='top', fontsize=7.0, color='#475569', linespacing=1.3)

    # Integrated Key Finding Box (Monochrome Academic Callout)
    callout1 = FancyBboxPatch((col2_x + 1.2, 27.5), col2_w - 2.4, 17.5, boxstyle="round,pad=0.2",
                              facecolor="#F1F5F9", edgecolor="#0F172A", linewidth=1.1)
    ax.add_patch(callout1)
    ax.text(col2_x + col2_w/2, 41.5, "CRITICAL FINDING", ha='center', va='center', fontsize=7.0, fontweight='bold', color='#0F172A')
    ax.text(col2_x + col2_w/2, 38.5, "20x Monetary Gap Surfaced\nRaster image uncovers NT$20M\nfrozen vs. NT$1M narrative text",
            ha='center', va='top', fontsize=7.1, fontweight='bold', color='#0F172A', linespacing=1.25)

    # Output Pill
    draw_pill(ax, col2_x + 1.2, 16.0, col2_w - 2.4, 8.5, "source.images.md\n(Multimodal Sidecar Layer)", facecolor="#FFFFFF", edgecolor="#1E293B", text_color="#0F172A", fontsize=7.2)

    # ==========================================
    # STAGE 3: LAYER 2 (SSOT DISTILLATION)
    # ==========================================
    col3_x, col3_w = 52.5, 21.0
    ax.add_patch(FancyBboxPatch((col3_x, 13.5), col3_w, 76.5, boxstyle="round,pad=0.2",
                                facecolor="#FAFAFA", edgecolor="#94A3B8", linewidth=1.0))
    
    # Header
    ax.add_patch(FancyBboxPatch((col3_x, 84.0), col3_w, 6.0, boxstyle="round,pad=0.1",
                                facecolor="#0F172A", edgecolor="none"))
    ax.text(col3_x + col3_w/2, 87.0, "Layer 2: SSoT Distillation",
            ha='center', va='center', fontsize=9.2, fontweight='bold', color='#FFFFFF')
    ax.text(col3_x + col3_w/2, 82.0, "Module: doc-timeline-synthesizer",
            ha='center', va='center', fontsize=7.5, fontweight='bold', color='#475569')

    # Arbitration Box
    eng3 = FancyBboxPatch((col3_x + 1.2, 47.0), col3_w - 2.4, 32.5, boxstyle="round,pad=0.2",
                          facecolor="#FFFFFF", edgecolor="#64748B", linewidth=0.9)
    ax.add_patch(eng3)
    ax.text(col3_x + col3_w/2, 76.0, "Scope-Aware Arbitration", ha='center', va='center', fontsize=7.8, fontweight='bold', color='#0F172A')
    ax.text(col3_x + col3_w/2, 73.0, "• 4-Mode Conflict Resolution:\n  - Temporal supersede\n  - Intra-doc contradiction\n  - Geographic/scope mismatch\n  - Direct factoid controls\n• Ratified decrees outrank\n  preliminary draft figures",
            ha='center', va='top', fontsize=7.0, color='#475569', linespacing=1.3)

    # Artifacts Box
    eng3_out = FancyBboxPatch((col3_x + 1.2, 16.0), col3_w - 2.4, 29.0, boxstyle="round,pad=0.2",
                              facecolor="#F8FAFC", edgecolor="#475569", linewidth=0.9)
    ax.add_patch(eng3_out)
    ax.text(col3_x + col3_w/2, 41.5, "Single Source of Truth", ha='center', va='center', fontsize=7.8, fontweight='bold', color='#0F172A')
    ax.text(col3_x + col3_w/2, 38.5, "4 Domain SSoT Reports:\n• Finance & Procurements\n• Oversight & Governance\n• Infrastructure Capacity\n• Cross-cutting Timeline",
            ha='center', va='top', fontsize=7.0, color='#334155', linespacing=1.3)
    draw_pill(ax, col3_x + 2.0, 18.0, col3_w - 4.0, 5.2, "Candidate SSoT (~38k chars)", facecolor="#FFFFFF", edgecolor="#1E293B", text_color="#0F172A", fontsize=6.8)

    # ==========================================
    # STAGE 4: LAYER 3 (FRESH-SESSION AUDITOR)
    # ==========================================
    col4_x, col4_w = 78.0, 20.5
    ax.add_patch(FancyBboxPatch((col4_x, 13.5), col4_w, 76.5, boxstyle="round,pad=0.2",
                                facecolor="#FAFAFA", edgecolor="#94A3B8", linewidth=1.0))
    
    # Header
    ax.add_patch(FancyBboxPatch((col4_x, 84.0), col4_w, 6.0, boxstyle="round,pad=0.1",
                                facecolor="#1E293B", edgecolor="none"))
    ax.text(col4_x + col4_w/2, 87.0, "Layer 3: Fresh-Session Review",
            ha='center', va='center', fontsize=9.2, fontweight='bold', color='#FFFFFF')
    ax.text(col4_x + col4_w/2, 82.0, "Module: doc-timeline-auditor",
            ha='center', va='center', fontsize=7.5, fontweight='bold', color='#475569')

    # Protocol Box
    eng4 = FancyBboxPatch((col4_x + 1.2, 50.0), col4_w - 2.4, 29.5, boxstyle="round,pad=0.2",
                          facecolor="#FFFFFF", edgecolor="#64748B", linewidth=0.9)
    ax.add_patch(eng4)
    ax.text(col4_x + col4_w/2, 76.0, "Zero-Memory Auditor (DEC-002)", ha='center', va='center', fontsize=7.8, fontweight='bold', color='#0F172A')
    ax.text(col4_x + col4_w/2, 73.0, "• Independent agent context\n• Zero access to L2 history\n• 5-Point Adversarial Audit:\n  1. Citation resolvability\n  2. Source risk disclosure\n  3. Cross-timestamp splicing\n  4. Coverage sampling\n  5. Arithmetic recalculation",
            ha='center', va='top', fontsize=6.8, color='#475569', linespacing=1.25)

    # Integrated Key Finding Box (Monochrome Academic Callout)
    callout2 = FancyBboxPatch((col4_x + 1.2, 29.5), col4_w - 2.4, 18.5, boxstyle="round,pad=0.2",
                              facecolor="#F1F5F9", edgecolor="#0F172A", linewidth=1.1)
    ax.add_patch(callout2)
    ax.text(col4_x + col4_w/2, 44.5, "VERIFICATION BOTTLENECK", ha='center', va='center', fontsize=7.0, fontweight='bold', color='#0F172A')
    ax.text(col4_x + col4_w/2, 41.5, "Arithmetic Error Corrected\nCatches 37.7% -> 41.8% discrepancy\nmissed by L2 self-checking",
            ha='center', va='top', fontsize=7.1, fontweight='bold', color='#0F172A', linespacing=1.25)

    # Terminal Trust Anchor Pill
    draw_pill(ax, col4_x + 1.2, 16.0, col4_w - 2.4, 10.5, "AUDITED SSoT ARCHIVE\nIndexed to Store 1 of RAG\nPowers Decision Support", facecolor="#0F172A", edgecolor="#000000", text_color="#FFFFFF", fontsize=7.2)

    # ==========================================
    # INTER-STAGE ARROWS & FLOW CONNECTORS
    # ==========================================
    arrow_style = dict(arrowstyle='simple,tail_width=1.3,head_width=4.0,head_length=4.5', color='#334155', lw=0.5)
    
    # 1 -> 2 connector (L1 output -> Step 0)
    ax.add_patch(FancyArrowPatch((col1_x + col1_w, 52.0), (col2_x, 52.0), **arrow_style))
    draw_pill(ax, (col1_x + col1_w + col2_x)/2 - 2.1, 53.5, 4.2, 4.2, "source.md\nplaceholders", facecolor="#FFFFFF", edgecolor="#475569", text_color="#0F172A", fontsize=5.6)

    # 2 -> 3 connector (Step 0 sidecar -> L2)
    ax.add_patch(FancyArrowPatch((col2_x + col2_w, 52.0), (col3_x, 52.0), **arrow_style))
    draw_pill(ax, (col2_x + col2_w + col3_x)/2 - 2.1, 53.5, 4.2, 4.2, "source.images.md\nsidecars", facecolor="#FFFFFF", edgecolor="#475569", text_color="#0F172A", fontsize=5.6)

    # 3 -> 4 connector (L2 Candidate SSoT -> L3 Auditor)
    ax.add_patch(FancyArrowPatch((col3_x + col3_w, 52.0), (col4_x, 52.0), **arrow_style))
    draw_pill(ax, (col3_x + col3_w + col4_x)/2 - 2.1, 53.5, 4.2, 4.2, "Candidate\nSSoT Reports", facecolor="#FFFFFF", edgecolor="#475569", text_color="#0F172A", fontsize=5.6)

    # Bottom Foundation Ribbon (Monochrome)
    bot_ribbon = FancyBboxPatch((1.5, 3.5), 97, 7.5, boxstyle="round,pad=0.2",
                                facecolor="#F8FAFC", edgecolor="#475569", linewidth=1.0)
    ax.add_patch(bot_ribbon)
    ax.text(50, 8.5, "DOWNSTREAM INTEGRATION: AUDITED SINGLE SOURCE OF TRUTH (SSoT)",
            ha='center', va='center', fontsize=9.2, fontweight='bold', color='#0F172A')
    ax.text(50, 5.5, "Indexed directly into Store 1 of Hierarchical Dual-Store RAG • Eliminates Hallucination & Hallucinated Draft Traps",
            ha='center', va='center', fontsize=7.6, color='#475569')

    plt.tight_layout()
    for p in output_paths:
        os.makedirs(os.path.dirname(p), exist_ok=True)
        fig.savefig(p, format='pdf', bbox_inches='tight', pad_inches=0.05)
        print(f"Saved Figure 1: {p}")
    plt.close(fig)


def generate_figure_2(output_paths):
    """
    Figure 2: Hierarchical Dual-Store RAG Architecture & Priority Arbitration
    Pure Academic Monochrome System Schematic:
    - Parallel simultaneous dispatch (NO wrong diamond router!)
    - 3D database cylinders for ChromaDB Store 1 and Store 2
    - Parallel dual-lane hybrid search & rerank (Store 1 vs Store 2)
    - Prompt packaging with priority arbitration directive
    - Generator LLM and verified answer
    - Compact empirical benchmark dashboard at bottom
    """
    fig, ax = plt.subplots(figsize=(15.8, 7.5), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Canvas Background
    bg = FancyBboxPatch((0.5, 0.5), 99, 99, boxstyle="round,pad=0.2",
                        facecolor="#FFFFFF", edgecolor="#CBD5E1", linewidth=1.2)
    ax.add_patch(bg)

    # Top Header Ribbon
    head_ribbon = FancyBboxPatch((1.5, 92.5), 97, 6.2, boxstyle="round,pad=0.2",
                                 facecolor="#F8FAFC", edgecolor="#475569", linewidth=1.0)
    ax.add_patch(head_ribbon)
    ax.add_patch(FancyBboxPatch((1.5, 92.5), 1.0, 6.2, boxstyle="round,pad=0.05", facecolor="#0F172A", edgecolor="none"))
    ax.text(50, 96.2, "HIERARCHICAL DUAL-STORE RAG ARCHITECTURE & PRIORITY ARBITRATION",
            ha='center', va='center', fontsize=11.2, fontweight='bold', color='#0F172A')
    ax.text(50, 93.8, "Parallel Dual-Store Indexing (SSoT vs. Raw) + Priority Rule Arbitration achieving 85.0% Accuracy & 83.3% Token Reduction",
            ha='center', va='center', fontsize=7.8, color='#475569')

    arrow_f = dict(arrowstyle='simple,tail_width=1.3,head_width=4.0,head_length=4.5', color='#0F172A', lw=0.5)
    inner_arrow = dict(arrowstyle='simple,tail_width=1.0,head_width=3.2,head_length=3.5', color='#475569', lw=0.4)

    # 1. User Decision Query (Left)
    q_x, q_y, q_w, q_h = 2.0, 36.0, 15.5, 52.0
    ax.add_patch(FancyBboxPatch((q_x, q_y), q_w, q_h, boxstyle="round,pad=0.2", facecolor="#FAFAFA", edgecolor="#475569", linewidth=1.0))
    ax.add_patch(FancyBboxPatch((q_x, q_y + q_h - 6.0), q_w, 6.0, boxstyle="round,pad=0.1", facecolor="#0F172A", edgecolor="none"))
    ax.text(q_x + q_w/2, q_y + q_h - 3.0, "User Decision Query", ha='center', va='center', fontsize=8.8, fontweight='bold', color='#FFFFFF')
    draw_pill(ax, q_x + 1.0, q_y + q_h - 12.5, q_w - 2.0, 4.2, "100-Question Adversarial Suite", fontsize=6.4)
    ax.text(q_x + 1.2, q_y + q_h - 16.5, "Example Query:", fontsize=7.2, fontweight='bold', color='#0F172A')
    query_text = '"What is the ratified 2026\nAI computing capacity and\nallocated budget for the\nSouthern Taiwan Data Center?"'
    ax.text(q_x + 1.2, q_y + q_h - 19.0, query_text,
            ha='left', va='top', fontsize=6.6, style='italic', color='#334155', linespacing=1.25)
    ax.text(q_x + 1.2, q_y + 15.0, "Adversarial Trap Modes:", fontsize=7.0, fontweight='bold', color='#0F172A')
    ax.text(q_x + 1.2, q_y + 13.0, "• Superseded draft figures\n• Intra-table misalignments\n• Non-summable MW scopes\n• Direct factoid baselines",
            ha='left', va='top', fontsize=6.5, color='#475569', linespacing=1.3)

    # 2. Segregated Stores (ChromaDB)
    stores_x, stores_y, stores_w, stores_h = 21.5, 36.0, 23.0, 52.0
    ax.add_patch(FancyBboxPatch((stores_x, stores_y), stores_w, stores_h, boxstyle="round,pad=0.2", facecolor="#FAFAFA", edgecolor="#475569", linestyle='--', linewidth=1.0))
    ax.text(stores_x + stores_w/2, stores_y + stores_h - 3.0, "Segregated Stores (ChromaDB)", ha='center', va='center', fontsize=8.2, fontweight='bold', color='#0F172A')

    # Store 1 (Top Cylinder)
    cyl1_x, cyl1_y, cyl1_w, cyl1_h = stores_x + 1.2, stores_y + 26.5, 5.0, 18.0
    draw_cylinder(ax, cyl1_x, cyl1_y, cyl1_w, cyl1_h, edgecolor='#0F172A')
    s1_text_x = cyl1_x + cyl1_w + 1.2
    ax.text(s1_text_x, cyl1_y + 17.0, "Store 1: SSoT Reports", fontsize=7.5, fontweight='bold', color='#0F172A')
    draw_pill(ax, s1_text_x, cyl1_y + 11.5, 14.5, 3.8, "HIGH PRIORITY (AUTHORITY)", facecolor="#0F172A", text_color="#FFFFFF", fontsize=6.0)
    ax.text(s1_text_x, cyl1_y + 9.5, "• 100 chunks (audited)\n• Macro reconciled facts\n• Superseded drafts resolved", ha='left', va='top', fontsize=6.4, color='#334155', linespacing=1.2)

    # Store 2 (Bottom Cylinder)
    cyl2_x, cyl2_y, cyl2_w, cyl2_h = stores_x + 1.2, stores_y + 2.5, 5.0, 18.0
    draw_cylinder(ax, cyl2_x, cyl2_y, cyl2_w, cyl2_h, edgecolor='#475569')
    s2_text_x = cyl2_x + cyl2_w + 1.2
    ax.text(s2_text_x, cyl2_y + 17.0, "Store 2: Raw Corpus", fontsize=7.5, fontweight='bold', color='#0F172A')
    draw_pill(ax, s2_text_x, cyl2_y + 11.5, 14.5, 3.8, "LOW PRIORITY (EVIDENCE)", facecolor="#F1F5F9", text_color="#0F172A", fontsize=6.0)
    ax.text(s2_text_x, cyl2_y + 9.5, "• 4,655 chunks (500 chars)\n• Micro ground-truth trails\n• Contains outdated figures", ha='left', va='top', fontsize=6.4, color='#475569', linespacing=1.2)

    # Query -> Stores Fork
    q_out_x = q_x + q_w
    q_mid_y = q_y + q_h/2
    ax.add_patch(FancyArrowPatch((q_out_x, q_mid_y + 4), (stores_x, cyl1_y + cyl1_h/2), connectionstyle="arc3,rad=-0.15", **arrow_f))
    ax.add_patch(FancyArrowPatch((q_out_x, q_mid_y - 4), (stores_x, cyl2_y + cyl2_h/2), connectionstyle="arc3,rad=0.15", **arrow_f))
    draw_pill(ax, (q_out_x + stores_x)/2 - 2.6, q_mid_y - 2.6, 5.2, 5.2, "Parallel\nDispatch", facecolor="#FFFFFF", edgecolor="#0F172A", text_color="#0F172A", fontsize=6.2)

    # 3. Parallel Hybrid Retrieval Engine
    ret_x, ret_y, ret_w, ret_h = 48.0, 36.0, 22.5, 52.0
    ax.add_patch(FancyBboxPatch((ret_x, ret_y), ret_w, ret_h, boxstyle="round,pad=0.2", facecolor="#FAFAFA", edgecolor="#475569", linewidth=1.0))
    ax.text(ret_x + ret_w/2, ret_y + ret_h - 3.0, "Parallel Hybrid Retrieval Engine", ha='center', va='center', fontsize=8.2, fontweight='bold', color='#0F172A')

    # Lane 1 (Store 1 Retrieval): Top
    r1_box = FancyBboxPatch((ret_x + 1.2, ret_y + 26.5), ret_w - 2.4, 20.0, boxstyle="round,pad=0.2", facecolor="#FFFFFF", edgecolor="#64748B", linewidth=0.9)
    ax.add_patch(r1_box)
    ax.text(ret_x + 2.2, ret_y + 44.0, "Store 1 Hybrid Search & Rerank", fontsize=7.4, fontweight='bold', color='#0F172A')
    ax.text(ret_x + 2.2, ret_y + 41.5, "• Dense bge-m3 + BM25 sparse\n• Cross-encoder re-scoring\n• Selects Top-5 SSoT Chunks", ha='left', va='top', fontsize=6.6, color='#475569', linespacing=1.25)
    draw_pill(ax, ret_x + 2.5, ret_y + 28.0, ret_w - 5.0, 4.2, "Yields: Top-5 SSoT Chunks", facecolor="#F1F5F9", edgecolor="#0F172A", text_color="#0F172A", fontsize=6.5)

    # Lane 2 (Store 2 Retrieval): Bottom
    r2_box = FancyBboxPatch((ret_x + 1.2, ret_y + 4.5), ret_w - 2.4, 20.0, boxstyle="round,pad=0.2", facecolor="#FFFFFF", edgecolor="#64748B", linewidth=0.9)
    ax.add_patch(r2_box)
    ax.text(ret_x + 2.2, ret_y + 22.0, "Store 2 Hybrid Search & Rerank", fontsize=7.4, fontweight='bold', color='#0F172A')
    ax.text(ret_x + 2.2, ret_y + 19.5, "• Dense bge-m3 + BM25 sparse\n• Cross-encoder re-scoring\n• Selects Top-5 Raw Chunks", ha='left', va='top', fontsize=6.6, color='#475569', linespacing=1.25)
    draw_pill(ax, ret_x + 2.5, ret_y + 6.0, ret_w - 5.0, 4.2, "Yields: Top-5 Raw Chunks", facecolor="#F1F5F9", edgecolor="#475569", text_color="#475569", fontsize=6.5)

    # Horizontal Arrows from Stores to Retrieval
    ax.add_patch(FancyArrowPatch((stores_x + stores_w, cyl1_y + cyl1_h/2), (ret_x, cyl1_y + cyl1_h/2), **arrow_f))
    ax.add_patch(FancyArrowPatch((stores_x + stores_w, cyl2_y + cyl2_h/2), (ret_x, cyl2_y + cyl2_h/2), **arrow_f))

    # 4. Prompt Packaging & Generation
    gen_x, gen_y, gen_w, gen_h = 77.0, 36.0, 21.0, 52.0
    ax.add_patch(FancyBboxPatch((gen_x, gen_y), gen_w, gen_h, boxstyle="round,pad=0.2", facecolor="#FAFAFA", edgecolor="#475569", linewidth=1.0))
    ax.text(gen_x + gen_w/2, gen_y + gen_h - 3.0, "Prompt Packaging & Generation", ha='center', va='center', fontsize=8.2, fontweight='bold', color='#0F172A')

    # Directive
    pd_box = FancyBboxPatch((gen_x + 1.2, gen_y + 28.5), gen_w - 2.4, 18.5, boxstyle="round,pad=0.2", facecolor="#FFFFFF", edgecolor="#475569", linewidth=0.9)
    ax.add_patch(pd_box)
    ax.text(gen_x + 2.2, gen_y + 43.5, "Priority Arbitration Directive:", fontsize=7.4, fontweight='bold', color='#0F172A')
    ax.text(gen_x + 2.2, gen_y + 40.5, "“When answering, treat the distilled SSoT\nfindings as authoritative. If figures conflict\nwith raw archival text, explicitly disregard\nsuperseded draft figures and prioritize SSoT.”",
            ha='left', va='top', fontsize=6.6, style='italic', color='#334155', linespacing=1.25)

    # LLM Box
    llm_box = FancyBboxPatch((gen_x + 1.2, gen_y + 12.0), gen_w - 2.4, 14.5, boxstyle="round,pad=0.2", facecolor="#F1F5F9", edgecolor="#0F172A", linewidth=1.0)
    ax.add_patch(llm_box)
    ax.add_patch(FancyBboxPatch((gen_x + 1.2, gen_y + 22.5), gen_w - 2.4, 4.0, boxstyle="round,pad=0.05", facecolor="#334155", edgecolor="none"))
    ax.text(gen_x + gen_w/2, gen_y + 24.5, "Generator LLM Engine", ha='center', va='center', fontsize=7.4, fontweight='bold', color='#FFFFFF')
    ax.text(gen_x + gen_w/2, gen_y + 18.5, "gemma-4-31B-it (vLLM local)", ha='center', va='center', fontsize=7.4, fontweight='bold', color='#0F172A')
    ax.text(gen_x + gen_w/2, gen_y + 14.5, "Greedy Decoding (temp = 0.0)", ha='center', va='center', fontsize=6.8, color='#475569')

    # Final Output Pill
    draw_pill(ax, gen_x + 1.2, gen_y + 2.0, gen_w - 2.4, 8.0, "Verified Decision Answer\nCitation-backed, conflict-resolved", facecolor="#0F172A", text_color="#FFFFFF", fontsize=7.2)

    # Arrows from Retrieval Lanes into Prompt Directive (High vs Low Priority Context)
    gap_mid_x = (ret_x + ret_w + gen_x) / 2
    ax.add_patch(FancyArrowPatch((ret_x + ret_w, cyl1_y + cyl1_h/2), (gen_x, cyl1_y + cyl1_h/2), **arrow_f))
    draw_pill(ax, gap_mid_x - 2.7, cyl1_y + cyl1_h/2 + 1.2, 5.4, 4.0, "Top-5 SSoT\n(Authority)", facecolor="#FFFFFF", edgecolor="#0F172A", text_color="#0F172A", fontsize=5.8)

    ax.add_patch(FancyArrowPatch((ret_x + ret_w, cyl2_y + cyl2_h/2), (gen_x, gen_y + 32.0), connectionstyle="arc3,rad=-0.12", **arrow_f))
    draw_pill(ax, gap_mid_x - 2.7, (cyl2_y + cyl2_h/2 + gen_y + 32.0)/2 - 2.0, 5.4, 4.0, "Top-5 Raw\n(Evidence)", facecolor="#FFFFFF", edgecolor="#475569", text_color="#475569", fontsize=5.8)

    # Internal arrows inside Gen
    ax.add_patch(FancyArrowPatch((gen_x + gen_w/2, gen_y + 28.5), (gen_x + gen_w/2, gen_y + 26.5), **inner_arrow))
    ax.add_patch(FancyArrowPatch((gen_x + gen_w/2, gen_y + 12.0), (gen_x + gen_w/2, gen_y + 10.0), **inner_arrow))

    # Bottom Dashboard
    dash_x, dash_y, dash_w, dash_h = 1.5, 3.5, 97.0, 29.5
    ax.add_patch(FancyBboxPatch((dash_x, dash_y), dash_w, dash_h, boxstyle="round,pad=0.2", facecolor="#F8FAFC", edgecolor="#475569", linewidth=1.0))
    ax.text(50, dash_y + dash_h - 3.2, "EMPIRICAL PERFORMANCE COMPARISON (100-Question Adversarial Benchmark)",
            ha='center', va='center', fontsize=9.2, fontweight='bold', color='#0F172A')

    card_w, gap = 30.0, 2.5
    c1_x = dash_x + 1.5
    c2_x = c1_x + card_w + gap
    c3_x = c2_x + card_w + gap
    card_h, card_y = 21.0, dash_y + 2.0

    for cx, title, metric, baseline, gain in [
        (c1_x, "PROMPT TOKEN OVERHEAD", "-83.3%", "Full-Context SSoT: ~18,000 tokens", "Hierarchical Dual-Store: ~3,000 tokens"),
        (c2_x, "OVERALL ACCURACY (100 Qs)", "85.0%", "Raw Baseline (Condition 1): 50.0%", "+35.0% Absolute Gain (p < 0.001, McNemar)"),
        (c3_x, "TEMPORAL CONFLICT ACCURACY", "86.7%", "Raw Baseline (Condition 1): 26.7%", "+60.0% Gain on Outdated Figures")
    ]:
        ax.add_patch(FancyBboxPatch((cx, card_y), card_w, card_h, boxstyle="round,pad=0.2", facecolor="#FFFFFF", edgecolor="#475569", linewidth=1.0))
        ax.add_patch(FancyBboxPatch((cx, card_y + card_h - 2.0), card_w, 2.0, boxstyle="round,pad=0.05", facecolor="#0F172A", edgecolor="none"))
        ax.text(cx + card_w/2, card_y + card_h - 4.5, title, ha='center', va='center', fontsize=7.6, fontweight='bold', color='#475569')
        ax.text(cx + card_w/2, card_y + 11.0, metric, ha='center', va='center', fontsize=22.0, fontweight='bold', color='#0F172A')
        ax.text(cx + card_w/2, card_y + 6.0, baseline, ha='center', va='center', fontsize=7.0, color='#64748B')
        ax.text(cx + card_w/2, card_y + 3.0, gain, ha='center', va='center', fontsize=7.2, fontweight='bold', color='#0F172A')

    plt.tight_layout()
    for p in output_paths:
        os.makedirs(os.path.dirname(p), exist_ok=True)
        fig.savefig(p, format='pdf', bbox_inches='tight', pad_inches=0.05)
        print(f"Saved Figure 2: {p}")
    plt.close(fig)


def generate_figure_3(output_paths):
    """
    Figure 3: Factual Accuracy by Question Category: Condition 1 vs. Condition 2
    Pure Monochrome Bar Chart (Publication Standard):
    - Solid black bars for Condition 2 (Dual-Store RAG)
    - Clean hatched bars (///) with dark border for Condition 1 (Raw Baseline)
    - 100% compliant with black-and-white laser printing
    """
    fig, ax = plt.subplots(figsize=(10.5, 4.8), dpi=300)
    
    categories = [
        'Temporal\n(N=30)',
        'Intra-Doc\n(N=20)',
        'Scope\n(N=20)',
        'Factoid\n(N=30)',
        'Overall\n(N=100)'
    ]
    
    cond1_acc = [26.7, 65.0, 50.0, 63.3, 50.0]
    cond2_acc = [86.7, 70.0, 85.0, 93.3, 85.0]
    
    import numpy as np
    x = np.arange(len(categories))
    width = 0.35
    
    # Pure Monochrome: White with dense hatch vs Solid Black
    rects1 = ax.bar(x - width/2, cond1_acc, width, label='Condition 1: Raw-Only Hybrid RAG (Top-5 Chunks)',
                    color='#FFFFFF', edgecolor='#0F172A', linewidth=1.2, hatch='///')
    rects2 = ax.bar(x + width/2, cond2_acc, width, label='Condition 2: Hierarchical Dual-Store RAG (Top-5 SSoT + Top-5 Raw)',
                    color='#0F172A', edgecolor='#000000', linewidth=1.2)
    
    ax.set_ylabel('Factual Accuracy (%)', fontsize=11, fontweight='bold', color='#0F172A')
    ax.set_title('Factual Accuracy Across Conflict Categories: Raw Baseline vs. Dual-Store RAG',
                 fontsize=12, fontweight='bold', pad=16, color='#0F172A')
    ax.set_xticks(x)
    ax.set_xticklabels(categories, fontsize=9.5, fontweight='bold', color='#0F172A')
    ax.set_ylim(0, 110)
    
    # Value labels on top of bars
    for rect in rects1:
        height = rect.get_height()
        ax.annotate(f'{height:.1f}%',
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 4), textcoords="offset points",
                    ha='center', va='bottom', fontsize=9.0, fontweight='bold', color='#0F172A')
                    
    for rect in rects2:
        height = rect.get_height()
        ax.annotate(f'{height:.1f}%',
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 4), textcoords="offset points",
                    ha='center', va='bottom', fontsize=9.0, fontweight='bold', color='#0F172A')
    
    # Styling: clean minimal spine
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#475569')
    ax.spines['bottom'].set_color('#475569')
    ax.yaxis.grid(True, linestyle='--', alpha=0.5, color='#CBD5E1')
    ax.set_axisbelow(True)
    
    # Legend
    legend = ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.16),
                       ncol=2, frameon=False, fontsize=9.0)
    for text in legend.get_texts():
        text.set_color('#0F172A')
        text.set_fontweight('bold')
    
    plt.tight_layout()
    for p in output_paths:
        os.makedirs(os.path.dirname(p), exist_ok=True)
        fig.savefig(p, format='pdf', bbox_inches='tight', pad_inches=0.05)
        print(f"Saved Figure 3: {p}")
    plt.close(fig)


def main():
    setup_matplotlib()
    
    base_dirs = [
        "paper/08_arxiv_submission/source/figures",
        "paper/07_arxiv/figures"
    ]
    
    print("Generating Figure 1 (Monochrome Academic Pipeline Flow)...")
    fig1_paths = [os.path.join(d, "fig1_workflow.pdf") for d in base_dirs]
    generate_figure_1(fig1_paths)
    
    print("Generating Figure 2 (Monochrome Academic Architecture Schematic)...")
    fig2_paths = [os.path.join(d, "fig2_dual_store_architecture.pdf") for d in base_dirs]
    generate_figure_2(fig2_paths)
    
    print("Generating Figure 3 (Pure Monochrome Bar Chart)...")
    fig3_paths = [os.path.join(d, "fig3_accuracy_comparison.pdf") for d in base_dirs]
    generate_figure_3(fig3_paths)
    
    print("All 3 figures generated successfully!")

if __name__ == "__main__":
    main()
