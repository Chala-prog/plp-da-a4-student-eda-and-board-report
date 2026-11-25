"""Builds the one-page phone-friendly board report (PNG + PDF) from duka_sales.csv."""
import numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

d = pd.read_csv("duka_sales.csv", parse_dates=["order_date"])
d["revenue"] = d.quantity * d.unit_price
d["month"] = d.order_date.dt.month
d["half"] = np.where(d.month <= 3, "Q1", "Q2")
tot = d.revenue.sum(); n = len(d)
mon = d.groupby("month").revenue.sum()
q = d.groupby("half").revenue.sum(); q_chg = q.Q2 / q.Q1 - 1
prod = d.groupby("product").revenue.sum().sort_values()
prem_share = d[d.unit_price >= 28000].revenue.sum() / tot
br = d.pivot_table(index="branch", columns="half", values="revenue", aggfunc="sum"); br["chg"] = br.Q2 / br.Q1 - 1
br_n = d.groupby(["branch", "half"]).size()
ch = d.pivot_table(index="channel", columns="half", values="revenue", aggfunc="sum"); ch["chg"] = ch.Q2 / ch.Q1 - 1
aov = d.groupby("channel").revenue.sum() / d.groupby("channel").size()

GREY, BLUE, RED, INK, MUTE = "#B4BCC6", "#1F5FBF", "#C8402B", "#1B2430", "#5B6675"
plt.rcParams.update({"font.family": "DejaVu Sans", "axes.spines.top": False, "axes.spines.right": False,
                     "axes.spines.left": False, "axes.edgecolor": GREY})
W, H = 4.5, 17.3
fig = plt.figure(figsize=(W, H), dpi=240, facecolor="white")
fy = lambda inch: 1 - inch / H            # inches from top -> figure fraction
def T(x, y_in, s, **k):
    k.setdefault("color", INK); k.setdefault("va", "top"); return fig.text(x, fy(y_in), s, **k)
M = 0.06
def rect(x, y_in, w, h_in, color):
    fig.patches.append(plt.Rectangle((x, fy(y_in + h_in)), w, h_in / H, transform=fig.transFigure, color=color, zorder=0))
def axes(x, y_in, w, h_in): return fig.add_axes([x, fy(y_in + h_in), w, h_in / H])

# ---- header
T(M, 0.20, "Duka Electronics · H1 2026 board report", fontsize=9.5, color=MUTE, weight="bold")
T(M, 0.50, "Sales held at KES 71.8M, but Q2\nstalled and now rests on laptops\nand Nairobi", fontsize=14, weight="bold", linespacing=1.15)
tiles = [(f"KES {tot/1e6:.1f}M", "revenue, Jan–Jun"), (f"{n:,}", "orders"), (f"{q_chg*100:+.1f}%", "Q2 vs Q1 revenue")]
for i, (big, small) in enumerate(tiles):
    x = M + i * 0.305
    rect(x, 1.50, 0.285, 0.78, "#F2F5F9")
    T(x + 0.012, 1.58, big, fontsize=13, weight="bold", color=BLUE if i != 2 else RED)
    T(x + 0.012, 1.98, small, fontsize=7.5, color=MUTE)

def section(y, title, sub, chart_h, lx=0.06, lw=0.88):
    T(M, y, title, fontsize=11.5, weight="bold", linespacing=1.15)
    T(M, y + 0.52, sub, fontsize=8, color=MUTE)
    return axes(lx, y + 0.80, lw, chart_h)
def note(y, s): T(M, y, s, fontsize=8.5, color=MUTE, linespacing=1.3)

# ---- chart 1 monthly revenue
y = 2.60
ax = section(y, "Q2 was flat on Q1: April peaked,\nthen sales eased", "Monthly revenue, KES millions", 1.15)
names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
cols = [BLUE if m == mon.idxmax() else GREY for m in mon.index]
ax.bar(names, mon.values / 1e6, color=cols, width=0.65)
for i, v in enumerate(mon.values / 1e6): ax.text(i, v + 0.3, f"{v:.1f}", ha="center", fontsize=8.5, weight="bold" if cols[i] == BLUE else "normal")
ax.set_ylim(0, 16); ax.set_yticks([]); ax.tick_params(axis="x", labelsize=8.5, length=0)
note(y + 2.15, f"Q1 KES {q.Q1/1e6:.1f}M vs Q2 KES {q.Q2/1e6:.1f}M.\nJune is {abs(mon[6]/mon[4]-1)*100:.0f}% below April.")

# ---- chart 2 products
y = 5.55
ax = section(y, f"Laptops and tablets bring {prem_share*100:.0f}%\nof revenue", "Share of H1 revenue by product", 1.45, lx=0.25, lw=0.58)
sh = prod / tot * 100
ax.barh(sh.index, sh.values, color=[BLUE if p == "Laptop" else GREY for p in sh.index], height=0.65)
for i, (p, v) in enumerate(sh.items()): ax.text(v + 1, i, f"{v:.0f}%", va="center", fontsize=8.5, weight="bold" if p == "Laptop" else "normal")
ax.set_xlim(0, 75); ax.set_xticks([]); ax.tick_params(axis="y", labelsize=8.5, length=0)
note(y + 2.45, f"Laptops are {d[d['product']=='Laptop'].shape[0]/n*100:.0f}% of orders but {sh['Laptop']:.0f}% of revenue.\nChargers and headphones: {sh[['Charger','Headphones']].sum():.0f}% together.")

# ---- chart 3 branches
y = 8.95
brs = br.sort_values("chg")
ax = section(y, "Mombasa and Nakuru fell about a quarter\nin Q2; Eldoret surged", "Revenue change, Q2 vs Q1", 1.65, lx=0.25, lw=0.58)
ax.barh(brs.index, brs.chg * 100, color=[RED if v < 0 else BLUE for v in brs.chg], height=0.65)
for i, (b, r) in enumerate(brs.iterrows()):
    ax.text(r.chg * 100 + (3 if r.chg > 0 else -3), i, f"{r.chg*100:+.0f}%", va="center", ha="left" if r.chg > 0 else "right", fontsize=8.5, weight="bold")
ax.axvline(0, color=INK, lw=0.8); ax.set_xlim(-48, 68); ax.set_xticks([]); ax.tick_params(axis="y", labelsize=8.5, length=0)
lost = (br.loc[["Mombasa", "Nakuru"], "Q2"] - br.loc[["Mombasa", "Nakuru"], "Q1"]).sum() / 1e6
nsh = br.loc["Nairobi", ["Q1", "Q2"]].sum() / tot * 100
note(y + 2.65, f"Mombasa and Nakuru lost KES {abs(lost):.1f}M between quarters.\nNairobi, the largest branch ({nsh:.0f}% of revenue), grew {br.chg['Nairobi']*100:.0f}%.")

# ---- chart 4 channels
y = 12.40
chs = ch.sort_values("chg")
ax = section(y, "Phone orders are small but growing,\nwith the biggest baskets", "Revenue change, Q2 vs Q1 (avg order value)", 1.05, lx=0.30, lw=0.53)
ax.barh([f"{c}\n(KES {aov[c]/1e3:.0f}K)" for c in chs.index], chs.chg * 100, color=[BLUE if v > 0 else GREY for v in chs.chg], height=0.6)
for i, (c, r) in enumerate(chs.iterrows()):
    ax.text(r.chg * 100 + (1.2 if r.chg > 0 else -1.2), i, f"{r.chg*100:+.1f}%", va="center", ha="left" if r.chg > 0 else "right", fontsize=8.5, weight="bold")
ax.axvline(0, color=INK, lw=0.8); ax.set_xlim(-12, 30); ax.set_xticks([]); ax.tick_params(axis="y", labelsize=8, length=0)

# ---- recommendations + footnote
rect(M - 0.015, 14.60, 0.91, 1.75, "#EAF1FB")
T(M, 14.72, "Where to focus in H2", fontsize=11.5, weight="bold", color=BLUE)
recs = ["1  Protect laptop and tablet supply:\n    they carry 85% of revenue.",
        "2  Diagnose Mombasa and Nakuru now: they are\n    the 2nd and 3rd largest branches (−KES 3.9M).",
        "3  Pilot phone orders and Eldoret's momentum\n    before scaling; both are small."]
for i, r in enumerate(recs): T(M, 14.95 + i * 0.0, "", fontsize=1)
T(M, 15.12, "\n\n".join(recs), fontsize=8.3, linespacing=1.35)
nmin, nmax = int(br_n.min()), int(br_n.max())
T(M, 16.55, f"Revenue = quantity × unit price. Data: 1 Jan–29 Jun 2026, {n:,} orders.\nBranch changes rest on {nmin}–{nmax} orders per branch-quarter: treat as\nsignals to check, not proven trends. No cost, margin or target data.", fontsize=6.6, color=MUTE, linespacing=1.3)
fig.savefig("reports/board_report.png", dpi=240); fig.savefig("reports/board_report.pdf")
print(br_n.min(), br_n.max(), prem_share, lost)
