#!/usr/bin/env python3
"""Build the static site into docs/ from x-design-devs.md + data/people/*.json."""
import json, os, re, shutil, subprocess, html, datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, 'docs')
DATA = os.path.join(ROOT, 'data', 'people')
RES = os.path.join(ROOT, 'research')
SITE_NAME = '有设计感的开发者'
TODAY = datetime.date.today().isoformat()

esc = lambda s: html.escape(str(s or ''), quote=True)


def parse_roster():
    """Return ordered list of (handle, group, score, note) from the markdown roster."""
    group, score, rows = '', '', []
    for line in open(os.path.join(ROOT, 'x-design-devs.md'), encoding='utf-8'):
        line = line.rstrip()
        if line.startswith('## '):
            group = re.sub(r'（.*?）|\(.*?\)', '', line[3:]).strip()
            note = re.search(r'（(.*?)）', line)
            group_note = note.group(1) if note else ''
            score = ''
        elif line.startswith('### '):
            score = line[4:].strip()
        else:
            m = re.search(r'x\.com/([A-Za-z0-9_]+)\)\s*(?:\((.*?)\))?', line)
            if m:
                rows.append(dict(handle=m.group(1), group=group, group_note=group_note,
                                 score=score, note=m.group(2) or ''))
    return rows


def parse_order():
    """Display order: one handle per line in data/order.txt (from the overall ranking)."""
    path = os.path.join(ROOT, 'data', 'order.txt')
    if not os.path.exists(path):
        return []
    return [l.strip() for l in open(path, encoding='utf-8') if l.strip()]


def load(path, default=None):
    try:
        return json.load(open(path, encoding='utf-8'))
    except Exception:
        return default


def fmt_num(n):
    if n is None:
        return None
    if n >= 10000:
        v = n / 10000
        return (f'{v:.1f}' if v < 100 else f'{v:.0f}').rstrip('0').rstrip('.') + ' 万'
    return f'{n:,}'


def stats_for(h):
    x = (load(os.path.join(RES, 'x', f'{h}.json'), {}) or {}).get('user') or {}
    gh = load(os.path.join(RES, 'gh', f'{h}.json'), {}) or {}
    repos = load(os.path.join(RES, 'repos', f'{h}.json'), []) or []
    out = []
    if x.get('followers') is not None:
        out.append((fmt_num(x['followers']), 'X 关注者'))
    if x.get('joined'):
        out.append((x['joined'][-4:], '加入 X'))
    stars = sum(r.get('stargazers_count') or 0 for r in repos)
    if gh.get('login') and stars:
        out.append((fmt_num(stars), 'GitHub 代表仓库 ★'))
    if gh.get('login') and gh.get('followers'):
        out.append((fmt_num(gh['followers']), 'GitHub 关注者'))
    return out, x


def chrome(prefix):
    return f'''<header class="chrome"><div class="chrome-in">
<a class="brand" href="{prefix}index.html"><span class="brand-mark">Dd</span>{SITE_NAME}</a>
<nav><a href="{prefix}index.html">全部人物</a><a class="hide-sm" href="{prefix}index.html#about">关于</a><a href="https://github.com/Hanqing/design-devs" class="hide-sm">GitHub</a></nav>
</div></header>'''


def head(title, desc, prefix, image=None):
    og = f'<meta property="og:image" content="{esc(image)}">' if image else ''
    return f'''<!doctype html>
<html lang="zh-CN"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}">{og}
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='8' fill='%2326251e'/%3E%3Ctext x='16' y='21' font-family='monospace' font-size='13' font-weight='700' fill='%23e6532f' text-anchor='middle'%3EDd%3C/text%3E%3C/svg%3E">
<link rel="stylesheet" href="{prefix}style.css">
</head>'''


GROUPS_PEOPLE = []


def site_footer(prefix, n):
    return f'''<footer class="drop" data-drop>
<div class="drop-scene" aria-hidden="true"><canvas></canvas><div class="drop-cue" hidden></div></div>
<nav class="drop-grid" aria-label="页脚">
<div class="drop-say"><h3>{n} 位开发者，<br>正从天而降。</h3><p>按住空白处把头像聚到一起，松开让大家落下；点一下头像，打开 TA 的人物页。</p></div>
<div><h2>人物志</h2><ul><li><a href="{prefix}index.html">全部 {n} 位</a></li></ul></div>
<div><h2>项目</h2><ul><li><a href="{prefix}index.html#about">关于这个项目</a></li><li><a href="https://github.com/Hanqing/design-devs" target="_blank" rel="noopener">GitHub 仓库</a></li><li><a href="https://github.com/Hanqing/design-devs/blob/main/x-design-devs.md" target="_blank" rel="noopener">研究池名单</a></li></ul></div>
<div><h2>致谢</h2><ul><li><a href="https://air.build/blog/" target="_blank" rel="noopener">AirBuild · 版式参考</a></li><li><a href="https://brm.io/matter-js/" target="_blank" rel="noopener">Matter.js · 物理引擎</a></li></ul></div>
</nav>
<div class="drop-bar"><span>{SITE_NAME} · 生成于 {TODAY}</span><a href="#">回到顶部 ↑</a></div>
</footer>
<script src="{prefix}drop.js" defer></script>'''


def render_block(b):
    if 'p' in b:
        cls = ' class="lead"' if b.get('lead') else ''
        return f'<p{cls}>{b["p"]}</p>'
    if 'h3' in b:
        return f'<h3>{b["h3"]}</h3>'
    if 'ul' in b:
        return '<ul>' + ''.join(f'<li>{i}</li>' for i in b['ul']) + '</ul>'
    if 'steps' in b:
        items = ''.join(
            f'<li><span class="when">{esc(s.get("when"))}</span><h3>{s["title"]}</h3><p>{s.get("text", "")}</p></li>'
            for s in b['steps'])
        return f'<ol class="steps">{items}</ol>'
    if 'cards' in b:
        out = []
        for i, c in enumerate(b['cards'], 1):
            idx = f'<span class="idx">{esc(c.get("meta") or f"{i:02d}")}</span>'
            inner = f'{idx}<h3>{c["name"]}</h3><p>{c.get("text", "")}</p>'
            if c.get('url'):
                dom = re.sub(r'^https?://(www\.)?', '', c['url']).split('/')[0]
                out.append(f'<a href="{esc(c["url"])}" target="_blank" rel="noopener">{inner}<span class="arrow">{esc(dom)} ↗</span></a>')
            else:
                out.append(f'<div>{inner}</div>')
        return f'<div class="cards">{"".join(out)}</div>'
    if 'checklist' in b:
        return '<ul class="checklist">' + ''.join(f'<li>{i}</li>' for i in b['checklist']) + '</ul>'
    if 'quote' in b:
        cite = f'<cite>— {b["cite"]}</cite>' if b.get('cite') else ''
        return f'<blockquote><p>{b["quote"]}</p>{cite}</blockquote>'
    if 'callout' in b:
        t = f'<b class="t">{b["t"]}</b>' if b.get('t') else ''
        return f'<div class="callout">{t}<p>{b["callout"]}</p></div>'
    if 'note' in b:
        return f'<div class="note">{b["note"]}</div>'
    if 'site' in b:
        s = b['site']
        disp = re.sub(r'^https?://', '', s['url']).rstrip('/')
        ps = ''.join(f'<p>{p}</p>' for p in s.get('paras', []))
        return (f'<div class="sitebox"><div class="bar"><i></i><i></i><i></i>'
                f'<a href="{esc(s["url"])}" target="_blank" rel="noopener">{esc(disp)} ↗</a></div><div class="in">{ps}</div></div>')
    if 'profile' in b:
        rows = ''.join(f'<div><dt>{esc(k)}</dt><dd>{v}</dd></div>' for k, v in b['profile'])
        t = f'<p class="profile-t">{b["t"]}</p>' if b.get('t') else ''
        return f'<div class="profile">{t}<dl>{rows}</dl></div>'
    if 'table' in b:
        tb = b['table']
        head_ = ''.join(f'<th>{c}</th>' for c in tb['cols'])
        body = ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>' for r in tb['rows'])
        cap = f'<caption>{tb["caption"]}</caption>' if tb.get('caption') else ''
        return f'<div class="tbl"><table>{cap}<thead><tr>{head_}</tr></thead><tbody>{body}</tbody></table></div>'
    if 'work' in b:
        w = b['work']
        name = f'<a href="{esc(w["url"])}" target="_blank" rel="noopener">{w["name"]} ↗</a>' if w.get('url') else w['name']
        chips = ''.join(f'<i>{esc(m)}</i>' for m in w.get('meta', []))
        paras = ''.join(f'<p>{x}</p>' for x in w.get('paras', []))
        bl = ('<ul>' + ''.join(f'<li>{x}</li>' for x in w['bullets']) + '</ul>') if w.get('bullets') else ''
        facts = ''
        if w.get('facts'):
            facts = '<dl class="work-facts">' + ''.join(f'<div><dt>{esc(k)}</dt><dd>{v}</dd></div>' for k, v in w['facts']) + '</dl>'
        return f'<article class="work"><header><h3>{name}</h3><div class="chips">{chips}</div></header>{paras}{bl}{facts}</article>'
    if 'posts' in b:
        items = []
        for x in b['posts']:
            t = f'<a href="{esc(x["url"])}" target="_blank" rel="noopener">{x["title"]}</a>' if x.get('url') else x['title']
            d = f'<span class="d">{esc(x.get("date", ""))}</span>' if x.get('date') else ''
            n = f'<p>{x["note"]}</p>' if x.get('note') else ''
            items.append(f'<li>{d}<div>{t}{n}</div></li>')
        return f'<ul class="posts">{"".join(items)}</ul>'
    if 'try' in b:
        items = ''.join(
            f'<li><a href="{esc(x["url"])}" target="_blank" rel="noopener">{x["name"]} ↗</a><p>{x.get("why", "")}</p></li>'
            for x in b['try'])
        return f'<ol class="try">{items}</ol>'
    raise ValueError(f'unknown block {b}')


def plain_len(p):
    s = json.dumps(p, ensure_ascii=False)
    return len(re.sub(r'<[^>]+>|[{}\[\]":,]', '', s))


def render_person(p, prev, nxt, prefix='../../'):
    h = p['handle']
    stats, x = stats_for(h)
    name = p.get('name') or x.get('name') or h
    av = f'{prefix}avatars/{h}.jpg'
    minutes = max(3, round(plain_len(p) / 450))
    meta = [f'<span><strong>@{esc(h)}</strong></span>']
    if p.get('location'):
        meta.append(f'<span>{esc(p["location"])}</span>')
    meta.append(f'<span>约 {minutes} 分钟读完</span>')
    meta.append(f'<span>更新于 {esc(p.get("updated", TODAY))}</span>')
    pills = ''.join(f'<li>{esc(t)}</li>' for t in p.get('tags', []))
    summary = ''.join(f'<p>{s}</p>' for s in p.get('summary', []))
    stat_html = ''.join(f'<div><b>{esc(v)}</b><span>{esc(k)}</span></div>' for v, k in stats)

    secs, toc = [], []
    for s in p['sections']:
        blocks = ''.join(render_block(b) for b in s['blocks'])
        secs.append(f'<section id="{esc(s["id"])}"><h2>{s["title"]}</h2>{blocks}</section>')
        toc.append(f'<li><a href="#{esc(s["id"])}">{re.sub("<[^>]+>", "", s["title"])}</a></li>')
    toc.append('<li><a href="#sources">资料来源</a></li>')

    links = ''.join(f'<a href="{esc(l["url"])}" target="_blank" rel="noopener">{esc(l["label"])} ↗</a>'
                    for l in p.get('links', []))
    sources = ''.join(f'<li><a href="{esc(s["url"])}" target="_blank" rel="noopener">{esc(s["label"])}</a></li>'
                      for s in p.get('sources', []))

    def nav(o, cls, label):
        if not o:
            return '<span></span>'
        img = f'<img src="{prefix}avatars/{o["handle"]}.jpg" alt="" loading="lazy">'
        txt = f'<div style="min-width:0"><small>{label}</small><b>{esc(o["name"])}</b></div>'
        inner = txt + img if cls == 'r' else img + txt
        return f'<a class="{cls}" href="{prefix}people/{o["handle"]}/index.html">{inner}</a>'

    lead = f'<p class="lead">{p["lead"]}</p>' if p.get('lead') else ''
    cta_links = ''.join(f'<a href="{esc(l["url"])}" target="_blank" rel="noopener">{esc(l["label"])}</a>'
                        for l in p.get('links', [])[:3])
    title_plain = re.sub('<[^>]+>', '', p['title'])

    return f'''{head(f"{name} — {title_plain} · {SITE_NAME}", re.sub('<[^>]+>', '', p.get('dek', '')), prefix)}
<body>
{chrome(prefix)}
<main class="layout">
<article class="article">
<nav class="crumb"><a href="{prefix}index.html">全部人物</a><span>/</span><span>{esc(name)}</span></nav>
<header class="hero">
<div class="hero-id"><img class="avatar" src="{av}" alt="{esc(name)} 的头像"><div class="who"><b>{esc(name)}</b><span>{esc(p.get('role', ''))}</span></div></div>
<h1 class="title">{p['title']}</h1>
<p class="dek">{p.get('dek', '')}</p>
<div class="meta">{''.join(meta)}</div>
<ul class="pills">{pills}</ul>
</header>
<div class="body">
<div class="summary">{summary}</div>
{f'<div class="stats">{stat_html}</div>' if stat_html else ''}
{lead}
{''.join(secs)}
<section class="cta"><h2>去看看 {esc(name)} 本人的作品</h2><p>{esc(p.get('cta', '最好的了解方式，是亲手用一用这些作品。'))}</p><div class="acts">{cta_links}</div></section>
<section class="sources" id="sources"><h2>资料来源</h2><ol>{sources}</ol>
<p style="margin-top:12px">本页由公开资料整理，可能存在遗漏或过时之处；以本人公开发布的信息为准。</p></section>
<div class="next">{nav(prev, 'l', '← 上一位')}{nav(nxt, 'r', '下一位 →')}</div>
</div>
</article>
<aside class="toc"><p>本页目录</p><ol>{''.join(toc)}</ol>
<div class="toc-acts"><a href="https://x.com/{esc(h)}" target="_blank" rel="noopener">X 主页 ↗</a>{links}<a href="{prefix}index.html">← 返回全部</a></div></aside>
</main>
{site_footer(prefix, len(GROUPS_PEOPLE))}
<script>
(()=>{{const a=[...document.querySelectorAll('.toc ol a')];const m=new Map(a.map(x=>[x.getAttribute('href').slice(1),x]));
const io=new IntersectionObserver(es=>{{es.forEach(e=>{{if(e.isIntersecting){{a.forEach(x=>x.removeAttribute('aria-current'));const l=m.get(e.target.id);l&&l.setAttribute('aria-current','true')}}}})}},{{rootMargin:'-20% 0px -70% 0px'}});
m.forEach((_,id)=>{{const s=document.getElementById(id);s&&io.observe(s)}})}})();
</script>
</body></html>'''


def render_index(people):
    cards = []
    for p in people:
        tags = ''.join(f'<i>{esc(t)}</i>' for t in p.get('tags', [])[:3])
        search = ' '.join([p['handle'], p.get('name', ''), p.get('role', ''), ' '.join(p.get('tags', [])), re.sub('<[^>]+>', '', p.get('dek', ''))]).lower()
        cards.append(f'''<a class="card" href="people/{p['handle']}/index.html" data-q="{esc(search)}">
<div class="card-top"><img src="avatars/{p['handle']}.jpg" alt="" loading="lazy"><div><b>{esc(p.get('name'))}</b><span>@{esc(p['handle'])}</span></div></div>
<p>{esc(re.sub('<[^>]+>', '', p.get('card', p.get('dek', ''))))}</p>
<div class="tags">{tags}</div></a>''')
    out = [f'<section class="group"><div class="grid">{"".join(cards)}</div></section>']
    n = len(people)
    return f'''{head(f"{SITE_NAME} · {n} 位人物志", f"{n} 位把代码写出审美的开发者：他们的作品、个人网站与成长经历。", '')}
<body>
{chrome('')}
<main class="home">
<header class="home-hero">
<p class="kick">DESIGN × DEV · {n} PROFILES</p>
<h1>{n} 位把代码写出<em>审美</em>的开发者</h1>
<p>独立开发者、设计工程师、开源作者、写作者。每一页整理一个人：做过的作品、个人网站的样子、一路走来的经历，以及我们能从中学到什么。</p>
</header>
<div class="filters"><input type="search" placeholder="搜索名字、作品、标签…" aria-label="搜索"></div>
{''.join(out)}
<section class="body" id="about" style="margin-top:72px;max-width:660px">
<h2>关于这个项目</h2>
<p>名单来自一个持续维护的研究池 <code>x-design-devs.md</code>：从一批种子账号出发，按「设计感 × 工程能力」持续扩展。页面按综合判断排序，主要看代表作的影响与工艺、设计品味、独立完成产品的能力、可学习度和近期活跃程度。</p>
<p>每篇人物志都基于公开资料整理：X 个人资料、GitHub、个人网站与博客、播客与采访等，并在页尾列出来源。视觉风格参考了 AirBuild 的博客排版。</p>
</section>
</main>
{site_footer('', n)}
<script>
(()=>{{const q=document.querySelector('.filters input');
q.oninput=()=>{{const t=q.value.trim().toLowerCase();document.querySelectorAll('.card').forEach(c=>{{c.style.display=!t||c.dataset.q.includes(t)?'':'none'}})}}}})();
</script>
</body></html>'''


def write_drop(people):
    """页脚掉落动效：生成 128px 头像缩略图，并把人物名单写进 drop.js。"""
    small = os.path.join(OUT, 'avatars', 's')
    os.makedirs(small, exist_ok=True)
    for p in people:
        src = os.path.join(OUT, 'avatars', f'{p["handle"]}.jpg')
        dst = os.path.join(small, f'{p["handle"]}.jpg')
        if os.path.exists(src) and not os.path.exists(dst) and shutil.which('sips'):
            subprocess.run(['sips', '-Z', '128', src, '--out', dst], capture_output=True)
    roster = [{'h': p['handle'], 'n': p.get('name') or p['handle']} for p in people]
    js = open(os.path.join(ROOT, 'site', 'drop.js'), encoding='utf-8').read()
    js = js.replace('__PEOPLE__', json.dumps(roster, ensure_ascii=False, separators=(',', ':')))
    open(os.path.join(OUT, 'drop.js'), 'w', encoding='utf-8').write(js)


def main():
    rows = parse_roster()
    os.makedirs(OUT, exist_ok=True)
    shutil.copy(os.path.join(ROOT, 'site', 'style.css'), os.path.join(OUT, 'style.css'))
    os.makedirs(os.path.join(OUT, 'vendor'), exist_ok=True)
    shutil.copy(os.path.join(ROOT, 'site', 'vendor', 'matter.min.js'), os.path.join(OUT, 'vendor', 'matter.min.js'))
    open(os.path.join(OUT, '.nojekyll'), 'w').close()
    order = parse_order()
    handles = order + [r['handle'] for r in rows if r['handle'] not in order]
    people = []
    for h in handles:
        p = load(os.path.join(DATA, f'{h}.json'))
        if p:
            p['handle'] = h
            people.append(p)
    GROUPS_PEOPLE[:] = people
    write_drop(people)
    for i, p in enumerate(people):
        d = os.path.join(OUT, 'people', p['handle'])
        os.makedirs(d, exist_ok=True)
        prev = people[i - 1] if i > 0 else None
        nxt = people[i + 1] if i + 1 < len(people) else None
        open(os.path.join(d, 'index.html'), 'w', encoding='utf-8').write(
            render_person(p, prev, nxt))
    open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8').write(render_index(people))
    missing = [r['handle'] for r in rows if r['handle'] not in {p['handle'] for p in people}]
    print(f'built {len(people)} people; missing {len(missing)}: {" ".join(missing)}')


if __name__ == '__main__':
    main()
