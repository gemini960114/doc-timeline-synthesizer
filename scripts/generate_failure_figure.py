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
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13.0, 4.8), dpi=300, gridspec_kw={'width_ratios': [1.05, 1.15]})
    
    # -------------------------------------------------------------
    # Panel A: Downstream Quantitative Benchmark Accuracy
    # -------------------------------------------------------------
    models = [
        "Condition 1: Raw Single-Store RAG\n(Dense + BM25 + Cross-Encoder)",
        "Condition 2: Hierarchical Dual-Store RAG\n(Raw Top-5 + SSoT Top-5)"
    ]
    scores = [50.0, 85.0]
    colors = ['#F1F5F9', '#1E293B']
    hatches = ['////', '']
    edgecolors = ['#0F172A', '#0F172A']
    
    y_pos = np.arange(len(models))
    bar_height = 0.40
    
    ax1.set_xlim(0, 105)
    ax1.set_ylim(-0.5, len(models) - 0.5)
    
    ax1.xaxis.grid(True, linestyle='--', linewidth=0.6, color='#CBD5E1', alpha=0.8, zorder=0)
    ax1.yaxis.grid(False)
    ax1.set_axisbelow(True)
    
    bars1 = ax1.barh(y_pos, scores, bar_height, color=colors, edgecolor=edgecolors, hatch=hatches, linewidth=1.2, zorder=3)
    
    for i, (bar, score) in enumerate(zip(bars1, scores)):
        w = bar.get_width()
        txt = f"{score:.1f}%"
        color = '#0F172A'
        ax1.text(w + 1.8, bar.get_y() + bar.get_height()/2, txt, va='center', ha='left',
                 fontsize=10.0, fontweight='bold', color=color, zorder=4)
        
    ax1.annotate('+35.0% gain (p < 0.001)', xy=(83.5, 0.88), xytext=(52, 0.50),
                 arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=-0.12", color="#0F172A", lw=1.2),
                 fontsize=9.0, fontweight='bold', color="#0F172A",
                 bbox=dict(boxstyle='round,pad=0.3', facecolor='#F8FAFC', edgecolor='#64748B', lw=0.9))

    ax1.set_yticks(y_pos)
    ax1.set_yticklabels(models, fontsize=9.0, fontweight='bold', color='#0F172A')
    ax1.invert_yaxis()
    ax1.set_xlabel("Benchmark Accuracy (%) [N=100 Questions]", fontsize=9.5, fontweight='bold', color='#0F172A', labelpad=8)
    ax1.set_title("(a) Quantitative Benchmark Accuracy", fontsize=10.5, fontweight='bold', color='#0F172A', pad=12)
    
    for spine in ['top', 'right']:
        ax1.spines[spine].set_visible(False)
    for spine in ['left', 'bottom']:
        ax1.spines[spine].set_color('#64748B')
        ax1.spines[spine].set_linewidth(0.8)

    # -------------------------------------------------------------
    # Panel B: Post-Hoc Qualitative Error Taxonomy
    # -------------------------------------------------------------
    causes = [
        "Surface-Form Variations\n(Structured Lists, Units, Delimiters)",
        "Retrieval Context Truncation\n(Line-item submerged below Top-5)",
        "Benchmark Rubric Ambiguity\n(Unprompted constraint in rubric)",
        "Superseded Draft Adoptions\n(Outdated Temporal Traps)"
    ]
    counts = [13, 1, 1, 0]
    pcts = [86.7, 6.7, 6.7, 0.0]
    cause_colors = ['#334155', '#64748B', '#94A3B8', '#E2E8F0']
    
    y_pos2 = np.arange(len(causes))
    
    ax2.set_xlim(0, 105)
    ax2.set_ylim(-0.6, len(causes) - 0.4)
    
    ax2.xaxis.grid(True, linestyle='--', linewidth=0.6, color='#CBD5E1', alpha=0.8, zorder=0)
    ax2.yaxis.grid(False)
    ax2.set_axisbelow(True)
    
    bars2 = ax2.barh(y_pos2, pcts, 0.45, color=cause_colors, edgecolor='#0F172A', linewidth=1.1, zorder=3)
    
    for bar, count, pct in zip(bars2, counts, pcts):
        w = bar.get_width()
        if pct > 0:
            case_str = "case" if count == 1 else "cases"
            txt = f"{pct:.1f}% ({count} {case_str})"
            ax2.text(w + 1.8, bar.get_y() + bar.get_height()/2, txt, va='center', ha='left',
                     fontsize=8.8, fontweight='bold', color='#0F172A', zorder=4)
        else:
            txt = "0.0% (None observed in sample)"
            ax2.text(2.0, bar.get_y() + bar.get_height()/2, txt, va='center', ha='left',
                     fontsize=8.8, fontweight='bold', color='#334155', zorder=4)
                     
    ax2.set_yticks(y_pos2)
    ax2.set_yticklabels(causes, fontsize=8.8, fontweight='bold', color='#0F172A')
    ax2.invert_yaxis()
    ax2.set_xlabel("Share of Residual Non-Matches (%) [N=15 Failures]", fontsize=9.2, fontweight='bold', color='#0F172A', labelpad=8)
    ax2.set_title("(b) Post-Hoc Qualitative Error Taxonomy", fontsize=10.5, fontweight='bold', color='#0F172A', pad=12)

    for spine in ['top', 'right']:
        ax2.spines[spine].set_visible(False)
    for spine in ['left', 'bottom']:
        ax2.spines[spine].set_color('#64748B')
        ax2.spines[spine].set_linewidth(0.8)

    plt.tight_layout()
    
    out_png = "docs/images/fig4_failure_attribution.png"
    os.makedirs(os.path.dirname(out_png), exist_ok=True)
    fig.savefig(out_png, format='png', dpi=300, bbox_inches='tight', pad_inches=0.08)
    print(f"Saved: {out_png}")
    plt.close(fig)

if __name__ == "__main__":
    main()
