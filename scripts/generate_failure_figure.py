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
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13.0, 5.0), dpi=300, gridspec_kw={'width_ratios': [1.1, 1.0]})
    
    # -------------------------------------------------------------
    # Panel A: Accuracy Progression: Deterministic vs. Semantic
    # -------------------------------------------------------------
    models = [
        "Condition 1: Raw Single-Store RAG\n(Dense + BM25 + Cross-Encoder)",
        "Condition 2: Dual-Store RAG\n(Deterministic String Match)",
        "Condition 2: Dual-Store RAG\n(Underlying Semantic Factual Accuracy)"
    ]
    scores = [50.0, 85.0, 98.0]
    colors = ['#F8FAFC', '#334155', '#0F172A']
    hatches = ['////', '', '']
    edgecolors = ['#0F172A', '#0F172A', '#0F172A']
    
    y_pos = np.arange(len(models))
    bar_height = 0.45
    
    ax1.set_xlim(0, 112)
    ax1.set_ylim(-0.6, len(models) - 0.4)
    
    ax1.xaxis.grid(True, linestyle='--', linewidth=0.6, color='#CBD5E1', alpha=0.8, zorder=0)
    ax1.yaxis.grid(False)
    ax1.set_axisbelow(True)
    
    bars1 = ax1.barh(y_pos, scores, bar_height, color=colors, edgecolor=edgecolors, hatch=hatches, linewidth=1.2, zorder=3)
    
    for i, (bar, score) in enumerate(zip(bars1, scores)):
        w = bar.get_width()
        txt = f"{score:.1f}%"
        color = '#0F172A' if i == 2 else '#334155'
        ax1.text(w + 1.8, bar.get_y() + bar.get_height()/2, txt, va='center', ha='left',
                 fontsize=9.5, fontweight='bold', color=color, zorder=4)
        
    ax1.annotate('+35.0% gain', xy=(85.0, 1), xytext=(92, 0.45),
                 arrowprops=dict(arrowstyle="->", color="#0F172A", lw=1.0),
                 fontsize=8.5, fontweight='bold', color="#0F172A",
                 bbox=dict(boxstyle='round,pad=0.25', facecolor='#F1F5F9', edgecolor='#64748B', lw=0.8))

    ax1.annotate('+13.0% harness false neg.', xy=(98.0, 2), xytext=(85, 2.45),
                 arrowprops=dict(arrowstyle="->", color="#0F172A", lw=1.0),
                 fontsize=8.5, fontweight='bold', color="#0F172A",
                 bbox=dict(boxstyle='round,pad=0.25', facecolor='#F1F5F9', edgecolor='#64748B', lw=0.8))

    ax1.set_yticks(y_pos)
    ax1.set_yticklabels(models, fontsize=8.8, fontweight='bold', color='#0F172A')
    ax1.invert_yaxis()
    ax1.set_xlabel("Benchmark Accuracy (%) [N=100 Questions]", fontsize=9.2, fontweight='bold', color='#0F172A', labelpad=8)
    ax1.set_title("(a) Accuracy Benchmark & Latent Semantic Quality", fontsize=10.5, fontweight='bold', color='#0F172A', pad=12)
    
    for spine in ['top', 'right']:
        ax1.spines[spine].set_visible(False)
    for spine in ['left', 'bottom']:
        ax1.spines[spine].set_color('#64748B')
        ax1.spines[spine].set_linewidth(0.8)

    # -------------------------------------------------------------
    # Panel B: Attribution of 15% Residual Errors
    # -------------------------------------------------------------
    causes = [
        "Harness Format False Negatives\n(Markdown, Chinese Units, Delimiters)",
        "Retrieval Chunk Granularity\n(Sub-case submerged below Top-5)",
        "Target Rubric Scope Misalignment\n(Unprompted field in rubric)",
        "Superseded Draft / Hallucinatory Traps\n(Catastrophic Errors)"
    ]
    counts = [13, 1, 1, 0]
    pcts = [86.7, 6.7, 6.7, 0.0]
    cause_colors = ['#334155', '#64748B', '#94A3B8', '#DC2626']
    
    y_pos2 = np.arange(len(causes))
    
    ax2.set_xlim(0, 105)
    ax2.set_ylim(-0.6, len(causes) - 0.4)
    
    ax2.xaxis.grid(True, linestyle='--', linewidth=0.6, color='#CBD5E1', alpha=0.8, zorder=0)
    ax2.yaxis.grid(False)
    ax2.set_axisbelow(True)
    
    bars2 = ax2.barh(y_pos2, pcts, bar_height, color=cause_colors, edgecolor='#0F172A', linewidth=1.1, zorder=3)
    
    for bar, count, pct in zip(bars2, counts, pcts):
        w = bar.get_width()
        if pct > 0:
            txt = f"{pct:.1f}% ({count} cases)"
            ax2.text(w + 1.8, bar.get_y() + bar.get_height()/2, txt, va='center', ha='left',
                     fontsize=8.8, fontweight='bold', color='#0F172A', zorder=4)
        else:
            txt = "0.0% (0 cases - ZERO Traps Adopted!)"
            ax2.text(2.0, bar.get_y() + bar.get_height()/2, txt, va='center', ha='left',
                     fontsize=8.8, fontweight='bold', color='#15803D', zorder=4)
                     
    ax2.set_yticks(y_pos2)
    ax2.set_yticklabels(causes, fontsize=8.8, fontweight='bold', color='#0F172A')
    ax2.invert_yaxis()
    ax2.set_xlabel("Share of Residual Misclassifications (%) [N=15 Failures]", fontsize=9.2, fontweight='bold', color='#0F172A', labelpad=8)
    ax2.set_title("(b) Root-Cause Attribution of Residual Non-Matches", fontsize=10.5, fontweight='bold', color='#0F172A', pad=12)

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
