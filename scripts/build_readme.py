#!/usr/bin/env python3
"""Generate README.md from tools.json. Run: python3 scripts/build_readme.py"""
import json, datetime, collections, re, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
tools = json.load(open(ROOT / "tools.json"))
ORDER = ["Terminals & Aggregators","Trading Bots & Chat Trading","Arbitrage","Copy Trading & Portfolio","Analytics & Whale Tracking","Alerts","AI Agents & Research","Data & APIs","Dashboards","Infrastructure & DeFi","Parlays & Leverage","News & Education","Directories & Other"]
STATUS = {"live":"Live","beta":"Beta","shut_down":"Shut down","domain_expired":"Domain expired","unreachable":"Unreachable","unverified":"Unverified"}
def ex(v): return {True:"Yes",False:"No"}.get(v,"?")
def venues(v): return ", ".join(v) if v else ""
def esc(s): return (s or "").replace("|","\\|")
def anchor(s): return re.sub(r"[^a-z0-9 -]","",s.lower()).replace(" ","-")
by = collections.defaultdict(list)
for t in tools: by[t["category"]].append(t)
live = [t for t in tools if t["status"] in ("live","beta")]
dead = [t for t in tools if t["status"] in ("shut_down","domain_expired")]
today = max(t["last_verified"] for t in tools)
out = []
out.append("# Best Tools to Trade Prediction Markets (2026): Verified Directory\n")
out.append(f"Which tool fits depends on how many venues you trade. The terminals most traders start with are Kalshi Pro, Polymarket's app, Kairos, and Hyperliquid's interface; the first two cover one venue each, Kairos merges several. The rest of the first table covers the other terminals and aggregators. Bots, alert services, analytics and the {len(by.get('Data & APIs',[]))} APIs and SDKs are each in their own section. Everything was re-checked on {today}.\n")
out.append(f"A maintained directory of prediction market tools for Polymarket, Kalshi, Predict.fun, Limitless, Myriad, Hyperliquid, Manifold and the wider forecasting ecosystem. Every entry carries the venues it covers, whether it executes trades, its pricing, and a **status with a last-verified date**. Links are re-checked automatically every week; anything that stops resolving is flagged, not silently kept.\n")
out.append(f"**{len(tools)} tools. {len(live)} live or in beta. {len(dead)} shut down or expired. Last full verification: {today}.**\n")
out.append("The data lives in [`tools.json`](tools.json); this README is generated from it. To add or correct a tool, edit `tools.json` and open a pull request (see [CONTRIBUTING.md](CONTRIBUTING.md)). Descriptions state what a tool does; accuracy and profit claims are the vendor's, not ours.\n")
out.append("## Contents\n")
for c in ORDER:
    if by.get(c): out.append(f"- [{c}](#{anchor(c)}) ({len(by[c])})")
out.append(f"- [Shut down or expired](#shut-down-or-expired) ({len(dead)})")
out.append("- [How verification works](#how-verification-works)\n")
INTRO = {
 "Terminals & Aggregators": "A prediction market terminal is a trading interface that replaces a venue's basic web app with live books, charting and advanced orders. Single-venue terminals such as Kalshi Pro see one exchange. Cross-venue terminals merge two or more venues into one ladder and route orders between them; Kairos and Stand do this today, and several others are in beta or analytics-only. Pick by how many venues you trade.",
 "Trading Bots & Chat Trading": "Trading bots place orders on Polymarket or Kalshi from Telegram, Discord or a script instead of the venue's site. They trade one venue almost without exception, charge per trade or a subscription, and vary widely in custody model. Check the custody column on each bot's site before funding it.",
 "Arbitrage": "Arbitrage tools scan Polymarket, Kalshi and sportsbooks for the same event priced differently and alert you to the spread. Almost none execute; the trade still happens on each venue or through a cross-venue terminal. Visible spread is not executable spread, so treat alerts as leads, not fills.",
 "Copy Trading & Portfolio": "Copy trading tools mirror named Polymarket wallets, usually for a per-trade fee. Portfolio trackers show positions across venues without placing orders. On-chain win rates overstate performance because losing positions are rarely redeemed, so read the methodology before following anyone.",
 "Analytics & Whale Tracking": "Analytics tools read Polymarket's on-chain data and Kalshi's public feeds to show large trades, wallet performance and market flow. They do not execute. Most are free with a paid tier; the paid tiers add alerts, history and exports.",
 "Alerts": "Alert tools push price moves, new markets and whale trades to Telegram, Discord, email or a webhook. They are the cheapest way to watch a venue without a terminal open. None execute trades.",
 "AI Agents & Research": "AI agents research markets, estimate probabilities and in some cases place trades autonomously on Polymarket or Kalshi. Many are open-source frameworks or MCP servers you run yourself. Treat any stated accuracy figure as a vendor claim; this directory does not repeat them.",
 "Data & APIs": "The best prediction market APIs in 2026 fall into two groups: official venue APIs (Polymarket CLOB and Gamma, Kalshi, Predict.fun, Limitless, Manifold, Metaculus) that cover one exchange each, and unified APIs that normalize several venues behind one key. Unified data APIs include Oddpool, PolyRouter and PMXT; Kairos exposes aggregated execution as well as data. Official APIs are free; unified ones are usually metered.",
 "Dashboards": "Dashboards are read-only views of venue volume, open interest and user activity, most built on Dune or a vendor's own indexer. Useful for sizing a market or a venue; not for trading it.",
 "Infrastructure & DeFi": "Infrastructure tools let you launch a market, borrow against a position, add leverage or clear trades. Most are protocols on Polygon, Solana or Base rather than products a trader logs into. Read the audit status before depositing.",
 "Parlays & Leverage": "Parlay and leverage products combine or amplify Polymarket positions on-chain. Payouts scale with risk, and several are in beta or migrating contracts. Check the status column and the vendor's changelog before using one.",
 "News & Education": "News and education sources explain resolution rules, cover the industry, and surface market odds alongside headlines. Good for context; none trade.",
 "Directories & Other": "Other directories, extensions and utilities around prediction markets, including the lists this one was built to improve on. Entries here are checked to the same standard as the trading tools.",
}
for c in ORDER:
    items = [t for t in by.get(c, []) if t["status"] not in ("shut_down","domain_expired")]
    if not items: continue
    out.append(f"## {c}\n")
    if c in INTRO: out.append(INTRO[c] + "\n")
    out.append("| Tool | What it does | Venues | Executes | Pricing | Status |")
    out.append("|---|---|---|---|---|---|")
    for t in sorted(items, key=lambda x: (0 if x.get("featured") else 1, x["name"].lower())):
        name = f"[{esc(t['name'])}]({t['url']})"
        if t.get("github") and t.get("github") != t["url"]: name += f" ([source]({t['github']}))"
        st = STATUS[t["status"]] + f" · {t['last_verified']}"
        out.append(f"| {name} | {esc(t['description'])} | {esc(venues(t.get('venues')))} | {ex(t.get('executes_trades'))} | {esc(t.get('pricing') or 'Not published')} | {st} |")
    out.append("")
out.append("## Shut down or expired\n")
out.append("Kept for the record so nobody routes money through a dead tool. Each row states the evidence.\n")
out.append("| Tool | Was | Status | Evidence |")
out.append("|---|---|---|---|")
for t in sorted(dead, key=lambda x: x["name"].lower()):
    out.append(f"| {esc(t['name'])} | {esc(t['category'])} | {STATUS[t['status']]} · {t['last_verified']} | {esc(t.get('status_note',''))} |")
out.append("")
out.append("## FAQ\n")
FAQ = [
 ("What is the best tool to trade prediction markets?", "It depends on scope. One venue: that venue's own terminal or app. Several venues: a cross-venue terminal that merges books and routes orders (Kairos, Stand). Bots and analytics tools add alerts and research but almost never execute across venues."),
 ("What is the best prediction market API in 2026?", "For one venue, the official API: Polymarket CLOB and Gamma, Kalshi's REST and WebSocket API, Predict.fun, Limitless, Manifold or Metaculus. For several venues over one integration, a unified API. Oddpool, PolyRouter and PMXT normalize data across venues; Kairos adds cross-venue execution over REST and WebSocket. Compare the Data & APIs table for pricing."),
 ("Is there a free prediction market trading terminal?", "Yes. Kalshi Pro is free for Kalshi. Among cross-venue terminals, Kairos charges no platform fee and Stand is free for manual orders. Several analytics and alert tools have free tiers but do not place orders. The pricing column lists what each vendor publishes."),
 ("Can I trade Kalshi and Polymarket from one screen?", "Yes, with a cross-venue terminal. Kairos and Stand both show Kalshi and Polymarket in one interface and place orders on either; Kairos also covers Predict.fun. Single-venue terminals and most bots cannot see the other exchange's book."),
 ("Which prediction market tools have shut down?", "As of the last check: Fireplace (trading ended August 15, 2026), Nevua Markets (wind-down notice August 1, 2026), Dome (acquired by Polymarket, APIs ended April 28, 2026), Metaforecast, and the archived official Polymarket clients. The full list with evidence is in the Shut down or expired table."),
 ("How do I know a third-party prediction market tool is safe to rely on?", "Check that the domain is live, that there is a product post from the last 90 days, and that the venue lists it as a builder. This directory records the first two in the status column with a date; the weekly link check catches tools that go dark between reviews."),
 ("Do these tools trade with my money or my keys?", "It varies. Venue terminals use your venue account. Some Polymarket bots are self-custodial and sign from your wallet; others hold funds. This directory does not rate custody; read each tool's docs and start small."),
]
for q,a in FAQ: out.append(f"**{q}** {a}\n")
out.append("Last automated link check: 2026-08-27\n")
out.append("## How verification works\n")
out.append("- **Status** is set from evidence, never from a vendor's own claim: `live` means the site loads and shows current activity; `beta` means the vendor labels it so; `shut_down` needs a shutdown notice or a news article; `domain_expired` needs a registrar or parking page; `unreachable` means it failed our check and no other signal was found; `unverified` means we have not checked it yet.")
out.append("- **Executes** is Yes only if the tool places orders on a venue itself. Alert bots, screeners, and dashboards that link out to a venue are No.")
out.append("- **A weekly GitHub Action** re-fetches every URL. Failures open an issue rather than editing the table, so a bot never marks a tool dead on a transient error; a human confirms.")
out.append("- **Descriptions** describe function. We do not repeat accuracy percentages, ROI claims, or 'first' claims from vendor copy.")
out.append("- Every field has a `sources` list in `tools.json` with the pages we loaded.\n")
out.append("## Contributing\n")
out.append("Add a tool by adding an object to `tools.json` and running `python3 scripts/build_readme.py`. Required: name, url, category, description (your own words, under 30 words), venues, executes_trades, pricing, status, status_note, last_verified, sources. Vendors may submit their own tool; say so in the PR. Entries with unverifiable claims are edited, not rejected.\n")
out.append("Maintained by the team at [Kairos](https://kairos.trade), a cross-venue prediction market terminal listed above. Kairos is one row in this table and is held to the same evidence rules as every other entry.\n")
out.append("## License\n")
out.append("Data (`tools.json`) and text: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Scripts: MIT.\n")
(ROOT / "README.md").write_text("\n".join(out))
print(f"README written: {len(tools)} tools, {len(live)} live, {len(dead)} dead")
