
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge
import pandas as pd
import streamlit as slt

slt.markdown(
    """
    <style>
      div[data-testid="stButton"] > button {
        display: inline-block;         
          width: 100%;          
          white-space: nowrap ;      
            overflow: hidden;                  
          text-overflow: ellipsis;          
             
      }
    </style>
    """,
    unsafe_allow_html=True
)

def draw(score: int):
    """Return a Matplotlib figure with as little empty space as possible."""
    angle = 180 * score / 100        # 0-100  →  0-180°

    fig, ax = plt.subplots(figsize=(4, 2.4))       # smaller, more “banner-like”
    ax.set_aspect("equal", adjustable="box")
    ax.axis("off")                                 # hide ticks, spines

    # ── gauge wedges ────────────────────────────────────────────────────
    ax.add_patch(Wedge((0.5, 0), 0.48, 0, 180,     width=0.18,
                       facecolor=(221/255, 220/255, 220/255, 0.6)))
    ax.add_patch(Wedge((0.5, 0), 0.48, 180-angle, 180, width=0.18,
                       facecolor=(84/255, 255/255, 160/255, 1)))

    # ── limit the data rectangle so we keep only the gauge area ─────────
    ax.set_xlim(0, 1)
    ax.set_ylim(-0.05, 0.55)          # <-- crop the top whitespace away

    # remove the residual figure padding
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
    fig.patch.set_alpha(0)   # figure background
    ax.patch.set_alpha(0)    # axes background
    return fig 

if __name__=="__main__":
    left, right = slt.columns([2, 1])
    score= 79
    missing_keywords = ["test","help me","data brack","kafka","hello there"]
    profile_summary  = "help me uyss"
    with left:
        slt.subheader("Match Score")        
        slt.pyplot(draw(score))
        slt.subheader(f"{score}/100",)
    # ── NEW: missing keywords list ──
    
    with right:                   # 4-A  Missing keyword “pills”
        slt.subheader("Missing Keywords / Skills")
        if missing_keywords:
            for i in range(0, len(missing_keywords), 3):
                cols = slt.columns(3)        # create one row → 3 equal-width cols
                for col, kw in zip(cols, missing_keywords[i:i + 3]):
                    with col:
                        slt.button(kw, key=kw, disabled=True)
        else:
            slt.success("Great job! No major gaps detected.")
    slt.markdown("---")     
    # ── NEW: profile summary ──
    slt.subheader("Profile Summary")
    slt.write(profile_summary)