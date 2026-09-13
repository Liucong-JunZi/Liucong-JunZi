"""Generate the Tokyo Night themed SVG assets used by README.md.

    python3 assets/gen.py
"""

from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).parent

# Tokyo Night (night variant)
BG = "#1a1b26"
BG2 = "#24283b"
BORDER = "#2f3549"
FG = "#c0caf5"
FG_DIM = "#a9b1d6"
COMMENT = "#565f89"
BLUE = "#7aa2f7"
PURPLE = "#bb9af7"
CYAN = "#7dcfff"
GREEN = "#9ece6a"
ORANGE = "#ff9e64"
RED = "#f7768e"
YELLOW = "#e0af68"

MONO = "'JetBrains Mono','Fira Code','SFMono-Regular',Menlo,Consolas,monospace"
SANS = "-apple-system,'Segoe UI','PingFang SC','Hiragino Sans GB','Noto Sans CJK SC','Microsoft YaHei',sans-serif"


def text_width(s: str, size: float) -> float:
    w = 0.0
    for ch in s:
        if ord(ch) > 0x2E80:
            w += size
        elif ch in "il.,:;'| ":
            w += size * 0.3
        elif ch.isupper():
            w += size * 0.68
        else:
            w += size * 0.55
    return w


def tokens(s: str) -> list[str]:
    """CJK characters break anywhere; latin words stay whole."""
    out, cur = [], ""
    for ch in s:
        if ch in "，。：；、！？）》」":
            if cur:
                out.append(cur)
                cur = ""
            out[-1] += ch
        elif ord(ch) > 0x2E80 or ch == " ":
            if cur:
                out.append(cur)
                cur = ""
            out.append(ch)
        else:
            cur += ch
    if cur:
        out.append(cur)
    return out


def wrap(s: str, size: float, max_w: float) -> list[str]:
    lines, cur = [], ""
    for tok in tokens(s):
        if text_width(cur + tok, size) > max_w and cur.strip():
            lines.append(cur.rstrip())
            cur = tok.lstrip()
        else:
            cur += tok
    if cur.strip():
        lines.append(cur.rstrip())
    return lines


def svg(w: int, h: int, body: str, extra_defs: str = "") -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">\n'
        f"<defs>{extra_defs}</defs>\n{body}\n</svg>\n"
    )


# ---------------------------------------------------------------- header
def header() -> str:
    W, H = 900, 260
    defs = f"""
<linearGradient id="g" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0" stop-color="{BLUE}"/><stop offset="0.55" stop-color="{PURPLE}"/><stop offset="1" stop-color="{ORANGE}"/>
</linearGradient>
<radialGradient id="glow1" cx="0.85" cy="0.1" r="0.6">
  <stop offset="0" stop-color="{PURPLE}" stop-opacity="0.35"/><stop offset="1" stop-color="{PURPLE}" stop-opacity="0"/>
</radialGradient>
<radialGradient id="glow2" cx="0.1" cy="0.95" r="0.6">
  <stop offset="0" stop-color="{BLUE}" stop-opacity="0.30"/><stop offset="1" stop-color="{BLUE}" stop-opacity="0"/>
</radialGradient>
<pattern id="grid" width="28" height="28" patternUnits="userSpaceOnUse">
  <path d="M28 0H0V28" fill="none" stroke="{FG}" stroke-opacity="0.045" stroke-width="1"/>
</pattern>
<clipPath id="r"><rect width="{W}" height="{H}" rx="16"/></clipPath>
<style>
  .name{{font:700 46px {SANS};letter-spacing:1px}}
  .sub{{font:400 15px {MONO};fill:{COMMENT}}}
  .tag{{font:500 13px {MONO}}}
</style>"""
    body = f"""
<g clip-path="url(#r)">
  <rect width="{W}" height="{H}" fill="{BG}"/>
  <rect width="{W}" height="{H}" fill="url(#grid)"/>
  <rect width="{W}" height="{H}" fill="url(#glow1)"/>
  <rect width="{W}" height="{H}" fill="url(#glow2)"/>
  <!-- code fragments as texture -->
  <g class="sub" fill="{COMMENT}" fill-opacity="0.55">
    <text x="600" y="72">__global__ void bfs_kernel(</text>
    <text x="600" y="96">    const int* __restrict__ row,</text>
    <text x="600" y="120">    const int* __restrict__ col,</text>
    <text x="600" y="144">    int* girth)</text>
    <text x="600" y="168">{{ atomicMin(girth, d + 1); }}</text>
  </g>
  <text x="56" y="118" class="name" fill="url(#g)">刘小聪 <tspan fill="{FG}" font-weight="300">/</tspan> Liu Cong</text>
  <text x="58" y="152" class="sub">math major → computer science · 山东大学（威海）</text>
  <g class="tag" transform="translate(56,184)">
    <rect width="72" height="26" rx="13" fill="{BLUE}" fill-opacity="0.14" stroke="{BLUE}" stroke-opacity="0.5"/>
    <text x="36" y="17.5" text-anchor="middle" fill="{BLUE}">CUDA</text>
    <rect x="82" width="88" height="26" rx="13" fill="{PURPLE}" fill-opacity="0.14" stroke="{PURPLE}" stroke-opacity="0.5"/>
    <text x="126" y="17.5" text-anchor="middle" fill="{PURPLE}">LLM · RAG</text>
    <rect x="180" width="90" height="26" rx="13" fill="{CYAN}" fill-opacity="0.14" stroke="{CYAN}" stroke-opacity="0.5"/>
    <text x="225" y="17.5" text-anchor="middle" fill="{CYAN}">AI Agents</text>
    <rect x="280" width="60" height="26" rx="13" fill="{ORANGE}" fill-opacity="0.14" stroke="{ORANGE}" stroke-opacity="0.5"/>
    <text x="310" y="17.5" text-anchor="middle" fill="{ORANGE}">HPC</text>
  </g>
  <rect x="0" y="{H-4}" width="{W}" height="4" fill="url(#g)"/>
</g>
<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="16" fill="none" stroke="{BORDER}"/>"""
    return svg(W, H, body, defs)


# -------------------------------------------------------------- terminal
def terminal() -> str:
    W = 900
    lines = [
        ("$ ", "whoami", None),
        (None, None, ("liucong — a math major crossing over into CS", FG)),
        None,
        ("$ ", "cat interests", None),
        (None, None, ("数学 · 机器学习 / LLM · 高性能计算 (CUDA) · AI Agents", FG)),
        None,
        ("$ ", "cat goal", None),
        (None, None, ("数学 → 跨考 408，用代码把奇思妙想落地", FG)),
        None,
        ("$ ", "echo $MOTTO", None),
        (None, None, ('"那些杀不死我的，会让我变得更加强大。"', YELLOW)),
    ]
    lh = 24
    H = 48 + 24 + lh * len(lines) + 20
    defs = f"""
<clipPath id="r"><rect width="{W}" height="{H}" rx="14"/></clipPath>
<style>
  .t{{font:400 15px {MONO}}}
</style>"""
    rows = []
    y = 48 + 28
    for ln in lines:
        if ln is None:
            y += lh
            continue
        prompt, cmd, out = ln
        if cmd:
            rows.append(
                f'<text x="28" y="{y}" class="t"><tspan fill="{GREEN}">{escape(prompt)}</tspan>'
                f'<tspan fill="{CYAN}">{escape(cmd)}</tspan></text>'
            )
        else:
            s, color = out
            rows.append(f'<text x="28" y="{y}" class="t" fill="{color}">{escape(s)}</text>')
        y += lh
    rows.append(f'<rect x="28" y="{y-14}" width="9" height="17" fill="{FG}" fill-opacity="0.85">'
                f'<animate attributeName="fill-opacity" values="0.85;0;0.85" dur="1.2s" repeatCount="indefinite"/></rect>')
    body = f"""
<g clip-path="url(#r)">
  <rect width="{W}" height="{H}" fill="{BG}"/>
  <rect width="{W}" height="40" fill="{BG2}"/>
  <circle cx="22" cy="20" r="6" fill="{RED}"/><circle cx="42" cy="20" r="6" fill="{YELLOW}"/><circle cx="62" cy="20" r="6" fill="{GREEN}"/>
  <text x="{W/2}" y="25" text-anchor="middle" class="t" fill="{COMMENT}" font-size="13">liucong@sdu — zsh</text>
  {chr(10).join(rows)}
</g>
<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="14" fill="none" stroke="{BORDER}"/>"""
    return svg(W, H, body, defs)


# ------------------------------------------------------------ project card
PROJECTS = [
    dict(
        slug="cuda-girth",
        name="cuda-girth",
        desc="大规模图的 GPU 精确 girth 计算：warp 级 CSR 遍历、atomicMin 全局环检测、跨 BFS 批次提前终止。把经典图论问题搬到现代 GPU 架构上。",
        tags=[("CUDA", GREEN), ("C++", BLUE)],
        accent=GREEN,
    ),
    dict(
        slug="dual-agent",
        name="Voice × Computer Dual-Agent",
        desc="一个 Agent 打电话、另一个 Agent 操作电脑的双智能体协同系统：VAD 语音检测、LLM 意图理解、消息队列异步通信，让 AI 一心二用。",
        tags=[("Python", BLUE), ("Agent", PURPLE)],
        accent=PURPLE,
    ),
    dict(
        slug="financevision",
        name="FinanceVision-AIagent",
        desc="端到端金融视频流水线：实时行情抓取 → DeepSeek-R1 生成文案 → 火山 TTS 配音 → 自动剪辑成片。",
        tags=[("Python", BLUE), ("LLM", PURPLE)],
        accent=ORANGE,
    ),
    dict(
        slug="image-search",
        name="Image Search Eval",
        desc="以文搜图评测系统：VLM caption → bge 向量召回 → reranker 精排，全链路异步并受 RPM / TPM / 并发限流。",
        tags=[("Python", BLUE), ("RAG", CYAN)],
        accent=CYAN,
    ),
    dict(
        slug="junzi-web",
        name="JUNzi Web",
        desc="个人网站全栈：博客、作品集、简历；GitHub OAuth、MinIO、Redis、Nginx，Docker Compose 一键部署。",
        tags=[("React", CYAN), ("Go", BLUE)],
        accent=BLUE,
    ),
    dict(
        slug="xiyou-galgame",
        name="Xiyou Galgame",
        desc="基于 Librian 引擎的《西游记》Galgame，剧情由 LLM 实时生成，可无限续写。",
        tags=[("Python", BLUE), ("LLM", PURPLE)],
        accent=RED,
    ),
]


def card(p: dict) -> str:
    W, H = 440, 188
    defs = f"""
<clipPath id="r"><rect width="{W}" height="{H}" rx="12"/></clipPath>
<style>
  .n{{font:700 17px {SANS}}}
  .d{{font:400 13px {SANS};fill:{FG_DIM}}}
  .g{{font:500 11.5px {MONO}}}
</style>"""
    lines = wrap(p["desc"], 13, W - 60)[:3]
    desc = "".join(f'<text x="28" y="{76 + i*21}" class="d">{escape(l)}</text>' for i, l in enumerate(lines))
    tags, x = [], 28
    for label, color in p["tags"]:
        tw = int(text_width(label, 11.5)) + 20
        tags.append(
            f'<rect x="{x}" y="{H-42}" width="{tw}" height="22" rx="11" fill="{color}" fill-opacity="0.13" stroke="{color}" stroke-opacity="0.45"/>'
            f'<text x="{x + tw/2}" y="{H-27}" text-anchor="middle" class="g" fill="{color}">{escape(label)}</text>'
        )
        x += tw + 8
    body = f"""
<g clip-path="url(#r)">
  <rect width="{W}" height="{H}" fill="{BG}"/>
  <rect width="4" height="{H}" fill="{p['accent']}"/>
  <text x="28" y="44" class="n" fill="{FG}">{escape(p['name'])}</text>
  <text x="{W-26}" y="44" text-anchor="end" class="g" fill="{COMMENT}">↗</text>
  {desc}
  {''.join(tags)}
</g>
<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="12" fill="none" stroke="{BORDER}"/>"""
    return svg(W, H, body, defs)


# -------------------------------------------------------------- section
def section(title: str, sub: str) -> str:
    W, H = 900, 44
    defs = f"""
<linearGradient id="g" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0" stop-color="{BLUE}"/><stop offset="1" stop-color="{PURPLE}" stop-opacity="0"/>
</linearGradient>
<style>
  .h{{font:700 20px {SANS}}}
  .s{{font:400 13px {MONO};fill:{COMMENT}}}
</style>"""
    body = f"""
<text x="0" y="24" class="h" fill="{BLUE}"><tspan fill="{PURPLE}">// </tspan>{escape(title)}</text>
<text x="{text_width(title, 20) + 36}" y="24" class="s">{escape(sub)}</text>
<rect x="0" y="38" width="{W}" height="2" rx="1" fill="url(#g)"/>"""
    return svg(W, H, body, defs)


# --------------------------------------------------------------- contact
def contact() -> str:
    items = [
        ("email", "lc20040517@gmail.com", BLUE),
        ("zhihu", "da-bu-cong", CYAN),
        ("qq", "2765692587", PURPLE),
        ("wechat", "liucong233333", GREEN),
    ]
    W, H = 900, 64
    defs = f"""
<clipPath id="r"><rect width="{W}" height="{H}" rx="12"/></clipPath>
<style>.t{{font:400 14px {MONO}}}</style>"""
    parts, x = [], 28
    for k, v, c in items:
        parts.append(
            f'<text x="{x}" y="39" class="t"><tspan fill="{c}">{k}</tspan><tspan fill="{COMMENT}"> · </tspan><tspan fill="{FG}">{escape(v)}</tspan></text>'
        )
        x += len(f"{k} · {v}") * 14 * 0.62 + 40
    body = f"""
<g clip-path="url(#r)">
  <rect width="{W}" height="{H}" fill="{BG}"/>
  {''.join(parts)}
</g>
<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="12" fill="none" stroke="{BORDER}"/>"""
    return svg(W, H, body, defs)


def main() -> None:
    (OUT / "projects").mkdir(exist_ok=True)
    (OUT / "header.svg").write_text(header())
    (OUT / "terminal.svg").write_text(terminal())
    (OUT / "contact.svg").write_text(contact())
    for title, sub, name in [
        ("Projects", "things I actually shipped", "sec-projects"),
        ("Activity", "commits & languages", "sec-activity"),
        ("Contact", "say hi", "sec-contact"),
    ]:
        (OUT / f"{name}.svg").write_text(section(title, sub))
    for p in PROJECTS:
        (OUT / "projects" / f"{p['slug']}.svg").write_text(card(p))


if __name__ == "__main__":
    main()
