"""
generate_visuals.py
===================
PythonMuse Article 18 — AI That Runs Before You Log In

Generates the three static visuals for this article:
  1. 18_hero.png         — hero image (title card)
  2. 18_old_vs_new.png   — old manual workflow vs new automated workflow
  3. 18_schedule_timeline.png — scheduled trigger timeline diagram

Run from the article directory:
    python generate_visuals.py

Requirements:
    pip install plotly kaleido
"""

from pathlib import Path
import plotly.graph_objects as go

VISUALS_DIR = Path(__file__).parent / "visuals"
VISUALS_DIR.mkdir(exist_ok=True)

BRAND_BLUE   = "#2E86AB"
BRAND_RED    = "#E63946"
BRAND_TEAL   = "#A8DADC"
BRAND_DARK   = "#1D3557"
BRAND_LIGHT  = "#F1FAEE"
BRAND_GREY   = "#6B6B6B"


# ---------------------------------------------------------------------------
# Visual 1: Hero image
# ---------------------------------------------------------------------------
def hero():
    fig = go.Figure()
    fig.add_annotation(
        text="AI That Runs<br><b>Before You Log In</b>",
        x=0.5, y=0.62, xref="paper", yref="paper",
        showarrow=False,
        font=dict(size=38, color=BRAND_DARK, family="Inter, Arial, sans-serif"),
        align="center",
    )
    fig.add_annotation(
        text="Scheduled Accounting Workflows",
        x=0.5, y=0.42, xref="paper", yref="paper",
        showarrow=False,
        font=dict(size=18, color=BRAND_BLUE, family="Inter, Arial, sans-serif"),
        align="center",
    )
    fig.add_annotation(
        text="<i>PythonMuse</i>",
        x=0.5, y=0.22, xref="paper", yref="paper",
        showarrow=False,
        font=dict(size=14, color=BRAND_GREY, family="Inter, Arial, sans-serif"),
        align="center",
    )
    fig.update_layout(
        width=1200, height=630,
        plot_bgcolor=BRAND_LIGHT,
        paper_bgcolor=BRAND_LIGHT,
        margin=dict(l=0, r=0, t=0, b=0),
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
    )
    out = VISUALS_DIR / "18_hero.png"
    fig.write_image(str(out))
    print(f"Saved: {out}")


# ---------------------------------------------------------------------------
# Visual 2: Old workflow vs new workflow
# ---------------------------------------------------------------------------
def old_vs_new():
    old_steps = [
        "Export CSV from ERP",
        "Open Excel",
        "Refresh pivots",
        "Fix broken formatting",
        "Update charts",
        "Add commentary",
        "Save PDF",
        "Email leadership",
        "Repeat tomorrow…",
    ]
    new_steps = [
        "Script pulls data",
        "Cleans & validates",
        "Calculates metrics",
        "Flags exceptions",
        "Builds HTML dashboard",
        "Generates commentary",
        "Saves to shared folder",
        "(Optional) emails link",
        "Done. Before you log in.",
    ]

    fig = go.Figure()

    # Old workflow bars (red, long to show pain)
    fig.add_trace(go.Bar(
        y=old_steps,
        x=[8, 5, 6, 7, 6, 5, 3, 3, 9],
        name="Old Way (Manual)",
        orientation="h",
        marker_color=BRAND_RED,
        opacity=0.85,
    ))

    # New workflow bars (blue, short to show efficiency)
    fig.add_trace(go.Bar(
        y=new_steps,
        x=[1, 1, 1, 1, 1, 1, 1, 1, 1],
        name="New Way (Scheduled Script)",
        orientation="h",
        marker_color=BRAND_BLUE,
        opacity=0.85,
    ))

    fig.update_layout(
        title=dict(
            text="The Old Way vs. The New Way",
            font=dict(size=20, color=BRAND_DARK),
        ),
        barmode="overlay",
        width=900, height=520,
        plot_bgcolor="white",
        paper_bgcolor="white",
        xaxis=dict(visible=False),
        yaxis=dict(tickfont=dict(size=12)),
        legend=dict(orientation="h", y=1.08),
        margin=dict(l=200, r=40, t=80, b=40),
    )
    out = VISUALS_DIR / "18_old_vs_new.png"
    fig.write_image(str(out))
    print(f"Saved: {out}")


# ---------------------------------------------------------------------------
# Visual 3: Scheduling timeline
# ---------------------------------------------------------------------------
def schedule_timeline():
    events = [
        (0,   "⏰ 7:00 AM",       "Task Scheduler fires",         BRAND_BLUE),
        (1,   "📂 7:00:02",       "Script loads CSV data",        BRAND_BLUE),
        (2,   "📊 7:00:05",       "Metrics calculated",           BRAND_BLUE),
        (3,   "🚩 7:00:06",       "Exceptions flagged",           BRAND_RED),
        (4,   "🌐 7:00:08",       "HTML dashboard built",         BRAND_BLUE),
        (5,   "💾 7:00:09",       "Saved to /outputs/",           BRAND_TEAL),
        (6,   "📧 7:00:10",       "Email sent (optional)",        BRAND_TEAL),
        (7,   "☕ 8:30 AM",       "Accountant arrives",           BRAND_DARK),
        (8,   "✅ 8:30:01",       "Dashboard already waiting",    BRAND_DARK),
    ]

    fig = go.Figure()

    for i, (x, label, desc, color) in enumerate(events):
        fig.add_trace(go.Scatter(
            x=[x], y=[0],
            mode="markers+text",
            marker=dict(size=18, color=color, line=dict(color="white", width=2)),
            text=[label],
            textposition="top center",
            textfont=dict(size=10, color=BRAND_DARK),
            name=desc,
            showlegend=False,
            hovertemplate=f"<b>{label}</b><br>{desc}<extra></extra>",
        ))
        fig.add_annotation(
            x=x, y=-0.25,
            text=desc,
            showarrow=False,
            font=dict(size=9, color=BRAND_GREY),
            align="center",
        )

    # Timeline line
    fig.add_shape(
        type="line",
        x0=-0.3, x1=8.3, y0=0, y1=0,
        line=dict(color=BRAND_GREY, width=2),
    )

    fig.update_layout(
        title=dict(
            text="The Daily Scheduled Workflow Timeline",
            font=dict(size=18, color=BRAND_DARK),
        ),
        width=1100, height=320,
        plot_bgcolor="white",
        paper_bgcolor="white",
        xaxis=dict(visible=False, range=[-0.5, 8.7]),
        yaxis=dict(visible=False, range=[-0.6, 0.5]),
        margin=dict(l=40, r=40, t=60, b=60),
    )
    out = VISUALS_DIR / "18_schedule_timeline.png"
    fig.write_image(str(out))
    print(f"Saved: {out}")


if __name__ == "__main__":
    print("Generating visuals for Article 18...")
    hero()
    old_vs_new()
    schedule_timeline()
    print("\nAll visuals saved to:", VISUALS_DIR)
