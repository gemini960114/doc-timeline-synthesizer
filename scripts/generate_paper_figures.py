#!/usr/bin/env python3
"""
Generate publication-grade vector PDF figures for the manuscript:
Figure 1: End-to-end multi-document knowledge arbitration and governance workflow
Figure 2: Hierarchical Dual-Store RAG architecture with priority authority arbitration
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle

def setup_matplotlib():
    plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Helvetica', 'Arial']
    plt.rcParams['axes.edgecolor'] = '#CCCCCC'
    plt.rcParams['axes.linewidth'] = 0.8

def draw_badge(ax, x, y, text, color='#2563EB', text_color='white', fontsize=7.5, pad=0.3):
    bbox_props = dict(boxstyle=f"round,pad={pad}", fc=color, ec="none", lw=0)
    ax.text(x, y, text, ha='center', va='center', fontsize=fontsize, 
            fontweight='bold', color=text_color, bbox=bbox_props)

def generate_figure_1(output_paths):
    """
    Figure 1: End-to-End Multi-Document Knowledge Arbitration and Governance Workflow
    Dimensions: 15.5 x 6.5 inches (Publication Full-Width)
    """
    fig, ax = plt.subplots(figsize=(15.5, 6.6), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Main Canvas Background
    bg = FancyBboxPatch((0.5, 0.5), 99, 99, boxstyle="round,pad=0.2",
                        facecolor="#FFFFFF", edgecolor="#CBD5E1", linewidth=1.2)
    ax.add_patch(bg)

    # Header Ribbon
    header_ribbon = FancyBboxPatch((1.5, 91.5), 97, 7, boxstyle="round,pad=0.2",
                                   facecolor="#0F172A", edgecolor="none")
    ax.add_patch(header_ribbon)
    ax.text(50, 95.8, "MULTI-DOCUMENT KNOWLEDGE ARBITRATION & VERIFICATION PIPELINE",
            ha='center', va='center', fontsize=11, fontweight='bold', color='#38BDF8')
    ax.text(50, 93, "Separating Deterministic Ingestion (L1), Multimodal Enrichment (Step 0), Semantic Distillation (L2), and Adversarial Review (L3)",
            ha='center', va='center', fontsize=7.8, color='#E2E8F0')

    # Four Stage Columns
    stages = [
        {
            "id": "L1",
            "title": "Layer 1: Physical Ingestion",
            "tool": "docling-skill",
            "badge": "CONTRACTUAL REPRODUCIBILITY",
            "color": "#1D4ED8",
            "bg": "#F8FAFC",
            "border": "#3B82F6",
            "x": 2, "w": 22.5,
            "items": [
                {
                    "tag": "INPUT CORPUS",
                    "title": "27 Heterogeneous Documents",
                    "lines": [
                        "• Finance & Budget: 16 forms",
                        "• Admin Oversight: 10 reports",
                        "• Technical R&D: 1 document",
                        "• Total 92 embedded images"
                    ]
                },
                {
                    "tag": "PARSING ENGINE",
                    "title": "Physical Layout Normalization",
                    "lines": [
                        "• Clean CJK character spacing",
                        "• Preserve table cell grids",
                        "• Extract image binaries to JSON",
                        "• Output source.manifest.json"
                    ]
                },
                {
                    "tag": "CONTRACTUAL OUTPUT",
                    "title": "Immutable source.md",
                    "lines": [
                        "• Clean markdown text stream",
                        "• [[image:...]] placeholders",
                        "• Base64 evidence stored in",
                        "  source.evidence.json"
                    ]
                }
            ]
        },
        {
            "id": "STEP0",
            "title": "Step Zero: Vision Enrichment",
            "tool": "scan_image_placeholders.py",
            "badge": "MULTIMODAL SIDECAR LAYER",
            "color": "#D97706",
            "bg": "#F8FAFC",
            "border": "#F59E0B",
            "x": 26.5, "w": 22.5,
            "items": [
                {
                    "tag": "IMMUTABILITY POLICY",
                    "title": "Preserve L1 Output (DEC-003)",
                    "lines": [
                        "• source.md is NEVER modified",
                        "• Vision findings written only to",
                        "  sidecar: source.images.md",
                        "• Guarantees audit reproducibility"
                    ]
                },
                {
                    "tag": "IMAGE TRIAGE",
                    "title": "Vision Agent Inspection",
                    "lines": [
                        "• 48 decorative logos skipped",
                        "  (explicitly logged in skip.json)",
                        "• 44 tables & charts inspected",
                        "• Extracts complex non-OCR text"
                    ]
                },
                {
                    "tag": "GROUND TRUTH DISCOVERY",
                    "title": "20x Discrepancy Caught",
                    "lines": [
                        "• Image reveals NT$20M frozen,",
                        "  versus NT$1M narrative text!",
                        "• Recovers unlisted vendor quotes",
                        "  and market-price clippings"
                    ]
                }
            ]
        },
        {
            "id": "L2",
            "title": "Layer 2: SSoT Distillation",
            "tool": "doc-timeline-synthesizer",
            "badge": "SCOPE-AWARE ARBITRATION",
            "color": "#047857",
            "bg": "#F8FAFC",
            "border": "#10B981",
            "x": 51, "w": 22.5,
            "items": [
                {
                    "tag": "CONFLICT TAXONOMY",
                    "title": "4-Mode Conflict Resolution",
                    "lines": [
                        "• Temporal conflicts (superseded)",
                        "• Intra-document contradictions",
                        "• Geographic / scope mismatches",
                        "• Direct factoid controls"
                    ]
                },
                {
                    "tag": "ARBITRATION POLICY",
                    "title": "Entity & Scope Alignment",
                    "lines": [
                        "• Align entity, period, and scope",
                        "• Compare only comparable claims",
                        "• Formal executive decrees outrank",
                        "  preliminary working drafts"
                    ]
                },
                {
                    "tag": "CANONICAL ARTIFACTS",
                    "title": "Single Source of Truth",
                    "lines": [
                        "• 4 Domain Summary Reports",
                        "• reports/*.md (~38k chars)",
                        "• Complete citation provenance",
                        "  for all operative figures"
                    ]
                }
            ]
        },
        {
            "id": "L3",
            "title": "Layer 3: Fresh-Session Review",
            "tool": "doc-timeline-auditor",
            "badge": "ADVERSARIAL OVERSIGHT",
            "color": "#B91C1C",
            "bg": "#F8FAFC",
            "border": "#EF4444",
            "x": 75.5, "w": 22.5,
            "items": [
                {
                    "tag": "OVERSIGHT PROTOCOL",
                    "title": "Zero-Memory Auditor (DEC-002)",
                    "lines": [
                        "• Independent agent context",
                        "• Zero access to L2 conversation",
                        "• Eliminates confirmation bias &",
                        "  verification bottleneck"
                    ]
                },
                {
                    "tag": "AUDIT DIMENSIONS",
                    "title": "5-Point Adversarial Check",
                    "lines": [
                        "1. Citation resolvability to sources",
                        "2. High-risk document disclosure",
                        "3. Cross-timestamp unit splicing",
                        "4. Coverage sampling verification",
                        "5. Numerical recalculation"
                    ]
                },
                {
                    "tag": "KEY ANOMALY DETECTED",
                    "title": "Arithmetic Error Corrected",
                    "lines": [
                        "• Caught 37.7% -> 41.8% error",
                        "• Missed by L2 internal self-check",
                        "• Confirms necessity of fresh-",
                        "  session architectural oversight"
                    ]
                }
            ]
        }
    ]

    for st in stages:
        # Outer Card
        card = FancyBboxPatch((st["x"], 10), st["w"], 79.5, boxstyle="round,pad=0.3",
                              facecolor=st["bg"], edgecolor=st["border"], linewidth=1.4)
        ax.add_patch(card)

        # Header Pill
        head = FancyBboxPatch((st["x"], 82), st["w"], 7.5, boxstyle="round,pad=0.2",
                              facecolor=st["color"], edgecolor="none")
        ax.add_patch(head)
        ax.text(st["x"] + st["w"]/2, 86.8, st["title"], ha='center', va='center',
                fontsize=8.8, fontweight='bold', color='white')
        ax.text(st["x"] + st["w"]/2, 83.5, f"Module: {st['tool']}", ha='center', va='center',
                fontsize=6.8, color='#F1F5F9', fontfamily='monospace')

        # Sub-badge below header
        draw_badge(ax, st["x"] + st["w"]/2, 79.5, st["badge"], color=st["color"],
                   text_color='white', fontsize=6.2, pad=0.25)

        # 3 Item Boxes per column
        box_y_starts = [76, 54, 32]
        for idx, it in enumerate(st["items"]):
            by = box_y_starts[idx]
            bw = st["w"] - 1.8
            bh = 20
            
            # Item container
            it_box = FancyBboxPatch((st["x"] + 0.9, by - bh), bw, bh, boxstyle="round,pad=0.2",
                                    facecolor="white", edgecolor=st["border"], linewidth=0.7)
            ax.add_patch(it_box)

            # Left accent bar
            bar = FancyBboxPatch((st["x"] + 0.9, by - bh), 1.2, bh, boxstyle="round,pad=0.1",
                                 facecolor=st["color"], edgecolor="none")
            ax.add_patch(bar)

            # Tag pill
            ax.text(st["x"] + 2.8, by - 2.8, it["tag"], fontsize=5.8, fontweight='bold',
                    color=st["color"])
            
            # Title
            ax.text(st["x"] + 2.8, by - 6.2, it["title"], fontsize=7.6, fontweight='bold',
                    color='#0F172A')

            # Bullet lines
            line_y = by - 9.5
            for line in it["lines"]:
                ax.text(st["x"] + 2.8, line_y, line, fontsize=6.3, color='#334155')
                line_y -= 2.6

    # Flow Arrows connecting the 4 stages
    arrows = [
        (24.6, 50, 26.4, 50, "#2563EB", "source.md\nplaceholders"),
        (49.1, 50, 50.9, 50, "#D97706", "source.images.md\nsidecars"),
        (73.6, 50, 75.4, 50, "#059669", "Candidate SSoT\nDomain Reports")
    ]
    for x1, y1, x2, y2, color, label in arrows:
        arr = FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=12,
                               color=color, linewidth=2)
        ax.add_patch(arr)
        ax.text((x1 + x2)/2, y1 + 3.5, label, ha='center', va='bottom', fontsize=5.8,
                fontweight='bold', color=color,
                bbox=dict(boxstyle="round,pad=0.15", fc="#FFFFFF", ec=color, lw=0.6))

    # Bottom Banner: Downstream Integration
    bot_banner = FancyBboxPatch((12, 1.8), 76, 6.2, boxstyle="round,pad=0.3",
                                facecolor="#0F172A", edgecolor="#38BDF8", linewidth=1.2)
    ax.add_patch(bot_banner)
    ax.text(50, 5.8, "DOWNSTREAM APPLICATION: AUDITED SINGLE SOURCE OF TRUTH (SSoT)",
            ha='center', va='center', fontsize=8.5, fontweight='bold', color='#38BDF8')
    ax.text(50, 3.4, "Indexed directly into Store 1 of Hierarchical Dual-Store RAG | Powers Verified Decision-Grade Question Answering",
            ha='center', va='center', fontsize=7.2, color='#E2E8F0')

    # Downward arrow from L2/L3 to Bottom Banner
    arr_down = FancyArrowPatch((63.2, 10), (63.2, 8.2), arrowstyle="-|>", mutation_scale=10,
                               color="#059669", linewidth=1.8)
    ax.add_patch(arr_down)
    arr_down3 = FancyArrowPatch((86.7, 10), (86.7, 8.2), arrowstyle="-|>", mutation_scale=10,
                                color="#B91C1C", linewidth=1.8)
    ax.add_patch(arr_down3)

    plt.tight_layout()
    for p in output_paths:
        os.makedirs(os.path.dirname(p), exist_ok=True)
        fig.savefig(p, format='pdf', bbox_inches='tight')
        print(f"Saved Figure 1: {p}")
    plt.close(fig)

def generate_figure_2(output_paths):
    """
    Figure 2: Hierarchical Dual-Store RAG Architecture with Priority Authority Arbitration
    Dimensions: 15.5 x 7.2 inches (Publication Full-Width)
    """
    fig, ax = plt.subplots(figsize=(15.5, 7.2), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Main Canvas Background
    bg = FancyBboxPatch((0.5, 0.5), 99, 99, boxstyle="round,pad=0.2",
                        facecolor="#FFFFFF", edgecolor="#CBD5E1", linewidth=1.2)
    ax.add_patch(bg)

    # Header Ribbon
    header_ribbon = FancyBboxPatch((1.5, 92.5), 97, 6.5, boxstyle="round,pad=0.2",
                                   facecolor="#0F172A", edgecolor="none")
    ax.add_patch(header_ribbon)
    ax.text(50, 96.5, "HIERARCHICAL DUAL-STORE RAG ARCHITECTURE & PRIORITY ARBITRATION",
            ha='center', va='center', fontsize=11, fontweight='bold', color='#38BDF8')
    ax.text(50, 94, "Segregated Vector Collections (SSoT vs. Raw) + Priority Prompting for High-Accuracy, Low-Token Decision Answering",
            ha='center', va='center', fontsize=7.8, color='#E2E8F0')

    # Column 1: User Query / Decision Inquiry (x: 2 to 18)
    q_box = FancyBboxPatch((2, 45), 16.5, 45, boxstyle="round,pad=0.3",
                           facecolor="#F8FAFC", edgecolor="#2563EB", linewidth=1.3)
    ax.add_patch(q_box)
    
    q_head = FancyBboxPatch((2, 84), 16.5, 6, boxstyle="round,pad=0.2", facecolor="#2563EB", edgecolor="none")
    ax.add_patch(q_head)
    ax.text(10.25, 87, "User Decision Inquiry", ha='center', va='center', fontsize=8.5, fontweight='bold', color='white')
    
    draw_badge(ax, 10.25, 80, "100-Question Adversarial Suite", color="#DBEAFE", text_color="#1D4ED8", fontsize=6.2)
    
    ax.text(3.2, 74, "Example Query:", fontsize=7.2, fontweight='bold', color="#0F172A")
    ax.text(3.2, 66, "\"What is the ratified 2026\nAI computing capacity and\nallocated budget for the\nSouthern Taiwan Data Center?\"",
            fontsize=6.5, fontstyle='italic', color="#334155", linespacing=1.25)
    
    ax.text(3.2, 58, "Adversarial Trap Modes:", fontsize=7, fontweight='bold', color="#DC2626")
    ax.text(3.2, 48, "• Superseded draft figures\n• Intra-table misalignments\n• Non-summable MW scopes\n• Direct factoid baselines",
            fontsize=6.2, color="#475569", linespacing=1.25)

    # Column 2: Dual Vector Stores (x: 21 to 45)
    stores_box = FancyBboxPatch((20.5, 42), 24.5, 48, boxstyle="round,pad=0.3",
                                facecolor="#F8FAFC", edgecolor="#64748B", linewidth=1.2, linestyle="--")
    ax.add_patch(stores_box)
    ax.text(32.75, 87.5, "Dual ChromaDB Collections", ha='center', va='center',
            fontsize=8.5, fontweight='bold', color="#0F172A")

    # Store 1 (SSoT)
    s1 = FancyBboxPatch((21.8, 66), 21.9, 19, boxstyle="round,pad=0.25",
                        facecolor="#ECFDF5", edgecolor="#059669", linewidth=1.3)
    ax.add_patch(s1)
    ax.text(32.75, 82.5, "Store 1: SSoT Reports Index", ha='center', va='center',
            fontsize=8.2, fontweight='bold', color="#047857")
    draw_badge(ax, 32.75, 78.2, "HIGH PRIORITY (AUTHORITY)", color="#059669", text_color="white", fontsize=6.2)
    s1_lines = [
        "• 100 chunks (audited Markdown)",
        "• Macro reconciled facts & timelines",
        "• Superseded draft figures resolved",
        "• Cross-domain executive briefing"
    ]
    sy = 74.5
    for sl in s1_lines:
        ax.text(23.2, sy, sl, fontsize=6.3, color="#064E3B", va='top')
        sy -= 2.2

    # Store 2 (Raw)
    s2 = FancyBboxPatch((21.8, 44), 21.9, 20, boxstyle="round,pad=0.25",
                        facecolor="#FFFBEB", edgecolor="#D97706", linewidth=1.3)
    ax.add_patch(s2)
    ax.text(32.75, 61, "Store 2: Raw Corpus Index", ha='center', va='center',
            fontsize=8.2, fontweight='bold', color="#B45309")
    draw_badge(ax, 32.75, 56.8, "LOW PRIORITY (EVIDENCE)", color="#D97706", text_color="white", fontsize=6.2)
    s2_lines = [
        "• 4,655 chunks (500 chars, 80 ovlp)",
        "• Micro-level ground-truth context",
        "• Vendor quotes & procedural trails",
        "• Contains outdated draft figures"
    ]
    sy2 = 53.2
    for sl in s2_lines:
        ax.text(23.2, sy2, sl, fontsize=6.3, color="#78350F", va='top')
        sy2 -= 2.2

    # Column 3: Parallel Hybrid Retrieval (x: 47 to 69)
    ret_box = FancyBboxPatch((47.5, 42), 21.5, 48, boxstyle="round,pad=0.3",
                             facecolor="#F8FAFC", edgecolor="#475569", linewidth=1.2)
    ax.add_patch(ret_box)
    ax.text(58.25, 87.5, "Parallel Hybrid Retrieval", ha='center', va='center',
            fontsize=8.5, fontweight='bold', color="#0F172A")

    # Dense + Sparse
    r1 = FancyBboxPatch((48.8, 72), 18.9, 13, boxstyle="round,pad=0.2",
                        facecolor="white", edgecolor="#3B82F6", linewidth=0.8)
    ax.add_patch(r1)
    ax.text(49.8, 81.5, "Hybrid Search", fontsize=7.4, fontweight='bold', color="#1D4ED8")
    ax.text(49.8, 77, "• Dense: bge-m3 embeddings\n• Sparse: BM25 lexical rank\n• Reciprocal Rank Fusion (k=60)",
            fontsize=6.2, color="#334155", linespacing=1.2)

    # Reranker
    r2 = FancyBboxPatch((48.8, 57), 18.9, 13, boxstyle="round,pad=0.2",
                        facecolor="white", edgecolor="#8B5CF6", linewidth=0.8)
    ax.add_patch(r2)
    ax.text(49.8, 66.5, "Cross-Encoder Scoring", fontsize=7.4, fontweight='bold', color="#6D28D9")
    ax.text(49.8, 62, "• BGE-Reranker-V2-M3\n• Fine-grained context matching\n• Scores relevance to query",
            fontsize=6.2, color="#334155", linespacing=1.2)

    # Top-k Routing
    r3 = FancyBboxPatch((48.8, 44), 18.9, 11.5, boxstyle="round,pad=0.2",
                        facecolor="#FEF3C7", edgecolor="#F59E0B", linewidth=0.8)
    ax.add_patch(r3)
    ax.text(49.8, 52, "Balanced Routing", fontsize=7.4, fontweight='bold', color="#B45309")
    ax.text(49.8, 47.5, "• Top-5 Chunks from Store 1 (SSoT)\n• Top-5 Chunks from Store 2 (Raw)\n• Total: 10 Chunks (~3,000 tokens)",
            fontsize=6.2, color="#92400E", linespacing=1.2)

    # Column 4: Priority Arbitration Prompt & Generation (x: 71.5 to 98)
    gen_container = FancyBboxPatch((71.5, 42), 26.5, 48, boxstyle="round,pad=0.3",
                                  facecolor="#F8FAFC", edgecolor="#4F46E5", linewidth=1.3)
    ax.add_patch(gen_container)
    ax.text(84.75, 87.5, "Prompt Packaging & Generation", ha='center', va='center',
            fontsize=8.5, fontweight='bold', color="#312E81")

    # Priority Arbitration Directive Box
    arb_box = FancyBboxPatch((72.8, 65.5), 23.9, 19.5, boxstyle="round,pad=0.25",
                             facecolor="#EEF2FF", edgecolor="#6366F1", linewidth=1)
    ax.add_patch(arb_box)
    ax.text(74.2, 81.8, "Priority Arbitration Directive:", fontsize=7.2, fontweight='bold', color="#4338CA")
    ax.text(74.2, 72.5, "\"When answering, treat the distilled SSoT\nfindings as authoritative. If figures conflict\nwith raw archival text, explicitly disregard\nsuperseded draft figures and prioritize SSoT.\"",
            fontsize=6.4, fontstyle='italic', color="#1E1B4B", linespacing=1.25)

    # Generator LLM Box
    llm_box = FancyBboxPatch((72.8, 44), 23.9, 19.5, boxstyle="round,pad=0.25",
                            facecolor="#1E1B4B", edgecolor="none")
    ax.add_patch(llm_box)
    ax.text(84.75, 59.5, "Generator LLM Engine", ha='center', va='center',
            fontsize=8, fontweight='bold', color="white")
    ax.text(84.75, 54.5, "gemma-4-31B-it (vLLM local)", ha='center', va='center',
            fontsize=7.5, fontfamily='monospace', color="#A5B4FC")
    ax.text(84.75, 49.5, "Greedy Decoding (temp = 0.0)", ha='center', va='center',
            fontsize=6.5, color="#C7D2FE")
    ax.text(84.75, 46, "Citation-backed, conflict-resolved answer", ha='center', va='center',
            fontsize=6.2, fontstyle='italic', color="#E0E7FF")

    # Arrows between main components
    # Query -> Stores
    ax.add_patch(FancyArrowPatch((18.5, 68), (20.5, 68), arrowstyle="-|>", mutation_scale=12, color="#2563EB", lw=2))
    # Stores -> Retrieval
    ax.add_patch(FancyArrowPatch((43.7, 75), (47.5, 75), arrowstyle="-|>", mutation_scale=12, color="#059669", lw=1.8))
    ax.add_patch(FancyArrowPatch((43.7, 54), (47.5, 54), arrowstyle="-|>", mutation_scale=12, color="#D97706", lw=1.8))
    # Retrieval -> Generation
    ax.add_patch(FancyArrowPatch((69, 65), (71.5, 65), arrowstyle="-|>", mutation_scale=12, color="#4F46E5", lw=2))

    # Bottom Dashboard: Quantitative Empirical Performance
    dash = FancyBboxPatch((2, 2.5), 96, 36.5, boxstyle="round,pad=0.3",
                          facecolor="#0F172A", edgecolor="#334155", linewidth=1.4)
    ax.add_patch(dash)
    ax.text(50, 35.5, "EMPIRICAL PERFORMANCE COMPARISON (100-Question Adversarial Benchmark)",
            ha='center', va='center', fontsize=9.2, fontweight='bold', color='#38BDF8')

    # Card 1: Token Overhead
    c1 = FancyBboxPatch((4.5, 5.5), 28.5, 26.5, boxstyle="round,pad=0.3",
                        facecolor="#1E293B", edgecolor="#0284C7", linewidth=1.2)
    ax.add_patch(c1)
    ax.text(18.75, 28, "PROMPT TOKEN OVERHEAD", ha='center', va='center',
            fontsize=7.8, fontweight='bold', color="#94A3B8")
    ax.text(18.75, 18.5, "-83.3%", ha='center', va='center',
            fontsize=20, fontweight='bold', color="#38BDF8")
    ax.text(18.75, 12, "Full-Context SSoT: ~18,000 tokens", ha='center', va='center', fontsize=6.6, color="#CBD5E1")
    ax.text(18.75, 8.5, "Hierarchical Dual-Store: ~3,000 tokens", ha='center', va='center', fontsize=6.6, fontweight='bold', color="#38BDF8")

    # Card 2: Overall Accuracy
    c2 = FancyBboxPatch((35.75, 5.5), 28.5, 26.5, boxstyle="round,pad=0.3",
                        facecolor="#1E293B", edgecolor="#10B981", linewidth=1.2)
    ax.add_patch(c2)
    ax.text(50, 28, "OVERALL ACCURACY (100 Qs)", ha='center', va='center',
            fontsize=7.8, fontweight='bold', color="#94A3B8")
    ax.text(50, 18.5, "85.0%", ha='center', va='center',
            fontsize=20, fontweight='bold', color="#34D399")
    ax.text(50, 12, "Raw Baseline (Condition 1): 50.0%", ha='center', va='center', fontsize=6.6, color="#CBD5E1")
    ax.text(50, 8.5, "+35.0% Absolute Gain (p < 0.001, McNemar)", ha='center', va='center', fontsize=6.6, fontweight='bold', color="#34D399")

    # Card 3: Temporal Conflict Accuracy
    c3 = FancyBboxPatch((67, 5.5), 28.5, 26.5, boxstyle="round,pad=0.3",
                        facecolor="#1E293B", edgecolor="#F59E0B", linewidth=1.2)
    ax.add_patch(c3)
    ax.text(81.25, 28, "TEMPORAL CONFLICT ACCURACY", ha='center', va='center',
            fontsize=7.8, fontweight='bold', color="#94A3B8")
    ax.text(81.25, 18.5, "86.7%", ha='center', va='center',
            fontsize=20, fontweight='bold', color="#FBBF24")
    ax.text(81.25, 12, "Raw Baseline (Condition 1): 26.7%", ha='center', va='center', fontsize=6.6, color="#CBD5E1")
    ax.text(81.25, 8.5, "+60.0% Gain on Outdated Figures", ha='center', va='center', fontsize=6.6, fontweight='bold', color="#FBBF24")

    plt.tight_layout()
    for p in output_paths:
        os.makedirs(os.path.dirname(p), exist_ok=True)
        fig.savefig(p, format='pdf', bbox_inches='tight')
        print(f"Saved Figure 2: {p}")
    plt.close(fig)

if __name__ == '__main__':
    setup_matplotlib()
    paths_fig1 = [
        "paper/08_arxiv_submission/source/figures/fig1_workflow.pdf",
        "paper/07_arxiv/figures/fig1_workflow.pdf"
    ]
    paths_fig2 = [
        "paper/08_arxiv_submission/source/figures/fig2_dual_store_architecture.pdf",
        "paper/07_arxiv/figures/fig2_dual_store_architecture.pdf"
    ]
    print("Generating Figure 1...")
    generate_figure_1(paths_fig1)
    print("Generating Figure 2...")
    generate_figure_2(paths_fig2)
    print("Figures generated successfully!")
