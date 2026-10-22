"""打印一个人的研究简报：X 资料 + 现有页面要点 + GitHub + 网站 + App Store。用法: python3 research/brief.py <handle> [LIM]"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
h = sys.argv[1]
LIM = int(sys.argv[2]) if len(sys.argv) > 2 else 2500
strip = lambda s: re.sub(r'<[^>]+>', '', s or '')

x = (json.load(open(f'{ROOT}/research/x/{h}.json')).get('user') or {}) if os.path.exists(f'{ROOT}/research/x/{h}.json') else {}
print(f'## {h} · X: {x.get("name")} | {x.get("followers")} 关注 | {x.get("following")} 正在关注 | 推文 {x.get("tweets")} | 加入 {x.get("joined")} | {x.get("location")} | {(x.get("website") or {}).get("url")}')
print('BIO:', (x.get('description') or '').replace('\n', ' '))

dp = f'{ROOT}/data/people/{h}.json'
d = json.load(open(dp)) if os.path.exists(dp) else {'sections': []}
print('\n# 现有页面:', d.get('role'), '|', strip(d.get('title')), '|', d.get('location'))
print('DEK:', strip(d.get('dek')))
for sec in d['sections']:
    bits = []
    for b in sec['blocks']:
        if 'steps' in b:
            bits += [f'[{s.get("when")}] {strip(s["title"])}: {strip(s.get("text"))}' for s in b['steps']]
        elif 'cards' in b:
            bits += [f'<{c["name"]}> {c.get("meta","")} {strip(c.get("text"))} {c.get("url","")}' for c in b['cards']]
        elif 'site' in b:
            bits += [b['site']['url']] + [strip(p) for p in b['site'].get('paras', [])]
        else:
            v = next((b[k] for k in ('p', 'callout', 'note', 'quote', 'h3') if k in b), None)
            if v:
                bits.append(strip(v))
            elif 'ul' in b or 'checklist' in b:
                bits += [strip(i) for i in b.get('ul') or b.get('checklist')]
    print(f'- {sec["title"]}: ' + ' ‖ '.join(bits))
print('SOURCES:', ' | '.join(f'{s["label"]} {s["url"]}' for s in d.get('sources', [])))

p = f'{ROOT}/research/deep/{h}.json'
if not os.path.exists(p):
    print('\n(no deep research yet)')
    sys.exit()
r = json.load(open(p))
g = r.get('github')
if g:
    u = g.get('user', {})
    print(f'\n# GitHub {g["login"]}{" (从网站推断)" if r.get("github_guess") else ""}: {u.get("name")} | {u.get("company")} | {u.get("location")} | {u.get("blog")} | 粉丝 {u.get("followers")} | 公开仓库 {u.get("public_repos")} | 注册 {(u.get("created_at") or "")[:10]} | 近一年贡献 {g.get("contrib_last_year")} | orgs {g.get("orgs")}')
    print('BIO:', u.get('bio'))
    print('语言分布:', g.get('languages'))
    if g.get('pinned'):
        print('置顶:', ' | '.join(f'{p["nameWithOwner"]} ★{p["stargazerCount"]} {(p.get("primaryLanguage") or {}).get("name")} — {p.get("description") or ""}' for p in g['pinned']))
    for rp in g.get('repos', [])[:14]:
        print(f'  ★{rp["stargazers_count"]:>6} ⑂{rp["forks_count"]:>5} {rp["full_name"]} [{rp["language"]}] {rp["created_at"][:7]}→{rp["pushed_at"][:7]}{" archived" if rp.get("archived") else ""} {rp.get("homepage") or ""} — {(rp["description"] or "")[:150]}')
    if g.get('profile_readme'):
        print('PROFILE README:', re.sub(r'\s+', ' ', g['profile_readme'])[:900])
    for n, rd in (g.get('readmes') or {}).items():
        print(f'README {n}:', re.sub(r'\s+', ' ', rd)[:int(LIM * 0.4)])
for s in r.get('sites', []):
    print(f'\n# 网站 {s["url"]} ok={s.get("ok")} | title: {s.get("title")} | desc: {s.get("description")} | lang {s.get("lang")}')
    print('技术栈:', s.get('stack'), '| 托管:', s.get('hosting'), '| GitHub 链接:', s.get('github_links'))
    if s.get('home_text'):
        print('HOME:', re.sub(r'\s+', ' ', s['home_text'])[:LIM])
    for u, t in (s.get('subpages') or {}).items():
        if u.rstrip('/') == s['url'].rstrip('/') or t[:300] == (s.get('home_text') or '')[:300]:
            continue
        print(f'SUB {u}:', re.sub(r'\s+', ' ', t)[:int(LIM * 0.6)])
    f = s.get('feed')
    if f:
        print(f'FEED {f["url"]} ({f["count_seen"]} 条):', ' | '.join(f'{i["date"][:16]} {i["title"]}' for i in f['items'][:18]))
for a in sorted(r.get('apps', []), key=lambda a: -(a['ratings'] or 0))[:14]:
    print(f'\nAPP {a["name"]} | {a["artist"]} | {a["genre"]} | {a["price"]} | 首发 {a["released"]} | 更新 {a["updated"]} v{a["version"]} | ★{a["rating"]} ({a["ratings"]}) | {a["kind"]} | {a["url"]}')
    print('  ', re.sub(r'\s+', ' ', a['desc'])[:280])
