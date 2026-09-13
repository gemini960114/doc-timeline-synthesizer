#!/usr/bin/env python3
"""
Generate publication-grade academic chart:
Figure 4: Attribution of Factual Accuracy and Residual Non-Matches (Condition 2 Dual-Store RAG)
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os

def setup_matplotlib():
    plt.rcParams['font.family'] = 'DejaVu Sans'
    plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Liberation Sans', 'Arial']
    plt.rcParams['mathtext.fontset'] = 'cm'

def main():
    setup_matplotlib()
    
    fig, ax = plt.subplots(figsize=(8.0, 2.5), dpi=300)
    
    # 3 categories aligned with paper text (N=15)
    categories = [
        "Potential Matching or Coverage Issues\n[Exploratory labels; no semantic rescoring]",
        "Retrieved Evidence Not Used\n[Correct amount present in raw context]",
        "Unasked Gold-Answer Requirement\n[Rubric requires unprompted amount]"
    ]
    counts = [13, 1, 1]
    pcts = [86.7, 6.7, 6.7]
    colors = ['#1E293B', '#475569', '#64748B']
    
    y_pos = np.arange(len(categories))
    bar_height = 0.45
    
    ax.set_xlim(0, 108)
    ax.set_ylim(-0.55, len(categories) - 0.45)
    
    ax.xaxis.grid(True, linestyle='--', linewidth=0.6, color='#CBD5E1', alpha=0.8, zorder=0)
    ax.yaxis.grid(False)
    ax.set_axisbelow(True)
    
    bars = ax.barh(y_pos, pcts, bar_height, color=colors, edgecolor='#0F172A', linewidth=1.1, zorder=3)
    
    for bar, count, pct in zip(bars, counts, pcts):
        w = bar.get_width()
        case_str = "case" if count == 1 else "cases"
        txt = f"{pct:.1f}% ({count} {case_str})"
        ax.text(w + 1.8, bar.get_y() + bar.get_height()/2, txt, va='center', ha='left',
                fontsize=9.2, fontweight='bold', color='#0F172A', zorder=4)
                 
    ax.set_yticks(y_pos)
    ax.set_yticklabels(categories, fontsize=8.8, fontweight='bold', color='#0F172A')
    ax.invert_yaxis()
    ax.set_xlabel("Share of Automated Non-Matches (%) [Total N=15]", fontsize=9.2, fontweight='bold', color='#0F172A', labelpad=6)
    ax.set_title("Exploratory Diagnostics of Non-Matches (Condition 2)", fontsize=10.2, fontweight='bold', color='#0F172A', pad=10)

    for spine in ['top', 'right']:
        ax.spines[spine].set_visible(False)
    for spine in ['left', 'bottom']:
        ax.spines[spine].set_color('#64748B')
        ax.spines[spine].set_linewidth(0.8)

    plt.tight_layout()
    
    # Save destinations
    destinations = [
        "paper/08_arxiv_submission/source/figures/fig4_error_adjudication.pdf",
        "paper/08_arxiv_submission/source/figures/fig4_error_adjudication.png",
        "paper/10_taai2026/figures/fig4_error_adjudication.pdf",
        "docs/images/fig4_failure_attribution.png"
    ]
    
    for path in destinations:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        fmt = 'pdf' if path.endswith('.pdf') else 'png'
        fig.savefig(path, format=fmt, bbox_inches='tight', pad_inches=0.05, dpi=300 if fmt == 'png' else None)
        print(f"Saved: {path}")
    plt.close(fig)

if __name__ == "__main__":
    main()
