"""深挖资料：GitHub（仓库/置顶/README/贡献数）、个人网站（子页面/技术栈/RSS）、App Store 应用详情。
用法: python3 research/deep.py [handle ...]   结果写入 research/deep/<handle>.json
"""
import json, os, re, sys, html, subprocess
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urljoin, urlparse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'research', 'deep')
os.makedirs(OUT, exist_ok=True)
UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15'
SKIP = ('github.com', 'x.com', 'twitter.com', 'apps.apple.com', 'youtube.com', 'weibo.com', 'bilibili.com',
        'instagram.com', 'linkedin.com', 'zhihu.com', 'medium.com', 'producthunt.com', 'xiaohongshu.com',
        'testflight.apple.com', 'mastodon', 'threads.net', 'bsky.app', 't.me', 'discord', 'jike', 'okjike')


def sh(args, timeout=40):
    try:
        return subprocess.run(args, capture_output=True, timeout=timeout).stdout.decode('utf-8', 'ignore')
    except Exception:
        return ''


def curl(url, head=False):
    args = ['curl', '-sL', '-m', '25', '--compressed', '-A', UA, '-H', 'Accept-Language: zh-CN,zh;q=0.9,en;q=0.8']
    if head:
        args += ['-D', '-', '-o', '/dev/null']
    return sh(args + [url], 30)


def gh(path, raw=False):
    args = ['gh', 'api', path]
    if raw:
        args += ['-H', 'Accept: application/vnd.github.raw']
    s = sh(args)
    if raw:
        return s
    try:
        return json.loads(s)
    except Exception:
        return None


def text_of(h, lim=3500):
    s = re.sub(r'<(script|style|svg|noscript|head|nav|footer)[^>]*>.*?</\1>', '', h, flags=re.S | re.I)
    s = re.sub(r'<(br|p|div|li|h\d|tr|section|article)[^>]*>', '\n', s, flags=re.I)
    t = html.unescape(re.sub(r'<[^>]+>', ' ', s))
    t = re.sub(r'[ \t\xa0]+', ' ', t)
    t = re.sub(r'\n\s*\n+', '\n', t)
    return t.strip()[:lim]


def jina(url, lim):
    t = sh(['curl', '-s', '-m', '40', 'https://r.jina.ai/' + url], 45)
    if 'Markdown Content:' in t:
        t = t.split('Markdown Content:', 1)[1]
    elif not t.startswith('Title:'):
        return ''
    t = re.sub(r'!\[[^\]]*\]\([^)]*\)', '', t)
    t = re.sub(r'\]\((https?://[^)\s]{60,})\)', lambda m: '](' + m.group(1)[:60] + '…)', t)
    t = re.sub(r'\n\s*\n+', '\n', t)
    return t.strip()[:lim]


def page_text(url, h=None, lim=3500):
    h = curl(url) if h is None else h
    t = text_of(h, lim)
    if len(t) < 400:
        j = jina(url, lim)
        if len(j) > len(t):
            return j, h
    return t, h


# ---------------- GitHub ----------------
def github(login):
    out = {'login': login}
    u = gh(f'users/{login}') or {}
    out['user'] = {k: u.get(k) for k in ('name', 'company', 'blog', 'location', 'bio', 'public_repos', 'followers', 'created_at', 'twitter_username', 'type')}
    repos = []
    if (u.get('public_repos') or 0) > 300:
        r = gh(f'search/repositories?q=user:{login}+fork:false&sort=stars&per_page=20') or {}
        repos = r.get('items', [])
    else:
        for page in (1, 2, 3):
            r = gh(f'users/{login}/repos?per_page=100&page={page}&type=owner') or []
            repos += r
            if len(r) < 100:
                break
    repos = [r for r in repos if isinstance(r, dict) and not r.get('fork')]
    repos.sort(key=lambda r: -(r.get('stargazers_count') or 0))
    keep = ('full_name', 'description', 'stargazers_count', 'forks_count', 'language', 'homepage', 'created_at', 'pushed_at', 'topics', 'archived')
    out['repos'] = [{k: r.get(k) for k in keep} for r in repos[:18]]
    out['repo_count_nonfork'] = len(repos)
    langs = {}
    for r in repos:
        if r.get('language'):
            langs[r['language']] = langs.get(r['language'], 0) + 1
    out['languages'] = sorted(langs.items(), key=lambda x: -x[1])[:8]
    q = ('query($l:String!){user(login:$l){pinnedItems(first:6,types:REPOSITORY){nodes{... on Repository{nameWithOwner '
         'stargazerCount description primaryLanguage{name} homepageUrl}}} contributionsCollection{contributionCalendar{totalContributions}} '
         'organizations(first:10){nodes{login name}}}}')
    g = sh(['gh', 'api', 'graphql', '-f', f'query={q}', '-F', f'l={login}'])
    try:
        d = json.loads(g)['data']['user']
        out['pinned'] = d['pinnedItems']['nodes']
        out['contrib_last_year'] = d['contributionsCollection']['contributionCalendar']['totalContributions']
        out['orgs'] = [o['login'] for o in d['organizations']['nodes']]
    except Exception:
        pass
    out['profile_readme'] = gh(f'repos/{login}/{login}/readme', raw=True)[:3000] if u.get('login') else ''
    if out['profile_readme'].startswith('{'):
        out['profile_readme'] = ''
    names = []
    for p in out.get('pinned') or []:
        names.append(p['nameWithOwner'])
    for r in out['repos'][:4]:
        names.append(r['full_name'])
    seen, readmes = set(), {}
    for n in names:
        if n in seen or len(readmes) >= 5:
            continue
        seen.add(n)
        rd = gh(f'repos/{n}/readme', raw=True)
        if rd and not rd.startswith('{"message"'):
            rd = re.sub(r'<img[^>]*>|!\[[^\]]*\]\([^)]*\)', '', rd)
            rd = re.sub(r'\n\s*\n+', '\n', rd)
            readmes[n] = rd[:2200]
    out['readmes'] = readmes
    return out


# ---------------- 个人网站 ----------------
SIGS = [
    (r'/_next/|__NEXT_DATA__', 'Next.js'), (r'/_nuxt/|__NUXT__', 'Nuxt'), (r'/_astro/|astro-island|data-astro-cid', 'Astro'),
    (r'_app/immutable|__sveltekit', 'SvelteKit'), (r'__remixContext', 'Remix'), (r'framerusercontent\.com|framer-', 'Framer'),
    (r'webflow\.(com|io)|data-wf-page', 'Webflow'), (r'wp-content|wp-includes', 'WordPress'), (r'super\.so|notion-static', 'Notion/Super'),
    (r'vitepress', 'VitePress'), (r'docusaurus', 'Docusaurus'), (r'gatsby', 'Gatsby'), (r'ghost-|content="Ghost', 'Ghost'),
    (r'hexo', 'Hexo'), (r'typecho', 'Typecho'), (r'tailwind', 'Tailwind CSS'), (r'plausible\.io', 'Plausible'),
    (r'umami', 'Umami'), (r'googletagmanager|google-analytics', 'Google Analytics'), (r'vercel-insights|/_vercel/', 'Vercel Analytics'),
    (r'fonts\.googleapis', 'Google Fonts'), (r'three(\.module)?(\.min)?\.js|THREE\.', 'three.js'), (r'gsap', 'GSAP'),
    (r'react', 'React'), (r'vue', 'Vue'), (r'substack', 'Substack'), (r'bearblog', 'Bear Blog'), (r'mataroa', 'Mataroa'),
    (r'readymag', 'Readymag'), (r'carrd', 'Carrd'), (r'giscus', 'giscus 评论'), (r'disqus', 'Disqus'), (r'buttondown', 'Buttondown'),
]
HOSTS = [(r'server: ?github\.com', 'GitHub Pages'), (r'x-vercel-id|server: ?vercel', 'Vercel'), (r'x-nf-request-id|server: ?netlify', 'Netlify'),
         (r'server: ?cloudflare', 'Cloudflare'), (r'fly-request-id', 'Fly.io'), (r'x-amz-cf|amazons3', 'AWS'),
         (r'server: ?framer', 'Framer'), (r'x-powered-by: ?next\.js', 'Next.js'), (r'cf-pages|pages\.dev', 'Cloudflare Pages'),
         (r'x-served-by: ?cache', 'Fastly'), (r'server: ?tengine|aliyun', '阿里云')]
PAGE_RX = re.compile(r'/(about|me|projects?|work|works|now|uses|blog|posts?|writing|articles|notes|portfolio|apps|products|cv|resume|timeline|links|talks)(/|\.html)?$', re.I)


def site(url):
    out = {'url': url}
    hd = curl(url, head=True).lower()
    h = curl(url)
    out['ok'] = bool(h.strip())
    if not h.strip():
        return out
    m = re.search(r'<title[^>]*>(.*?)</title>', h, re.S | re.I)
    out['title'] = html.unescape(m.group(1).strip()) if m else ''
    m = re.search(r'<meta[^>]+name=["\']description["\'][^>]+content=["\']([^"\']*)', h, re.I)
    out['description'] = html.unescape(m.group(1)) if m else ''
    gen = re.search(r'<meta[^>]+name=["\']generator["\'][^>]+content=["\']([^"\']*)', h, re.I)
    stack = [gen.group(1)] if gen else []
    low = h.lower()
    for rx, name in SIGS:
        if re.search(rx, low) and name not in stack:
            stack.append(name)
    host = [name for rx, name in HOSTS if re.search(rx, hd)]
    out['stack'] = stack
    out['hosting'] = sorted(set(host))
    out['lang'] = (re.search(r'<html[^>]+lang=["\']([^"\']+)', h, re.I) or [None, ''])[1]
    out['home_text'], _ = page_text(url, h, 4500)
    out['github_links'] = sorted(set(m for m in re.findall(r'github\.com/([A-Za-z0-9-]{2,39})(?=["/\'\s)])', h + out['home_text']) if m.lower() not in ('orgs', 'sponsors', 'apps', 'features', 'topics', 'about', 'login', 'site', 'pricing')))
    base = urlparse(url)
    links, seen = [], set()
    for href in re.findall(r'href=["\']([^"\'#]+)', h) + re.findall(r'\]\((https?://[^)\s]+)\)', out['home_text']):
        u = urljoin(url, href)
        p = urlparse(u)
        if p.netloc != base.netloc or u in seen:
            continue
        seen.add(u)
        if PAGE_RX.search(p.path.rstrip('/') or '/x'):
            links.append(u)
    out['subpages'] = {}
    for u in links[:6]:
        t, _ = page_text(u, None, 3000)
        if t:
            out['subpages'][u] = t
    feeds = re.findall(r'<link[^>]+type=["\']application/(?:rss|atom)\+xml["\'][^>]*>', h, re.I)
    furl = None
    for f in feeds:
        m = re.search(r'href=["\']([^"\']+)', f)
        if m:
            furl = urljoin(url, m.group(1))
            break
    cands = [furl] if furl else [urljoin(url, p) for p in ('/feed.xml', '/rss.xml', '/atom.xml', '/index.xml', '/feed')]
    for fu in cands:
        x = curl(fu)
        if '<rss' in x[:500] or '<feed' in x[:800]:
            items = []
            for m in re.finditer(r'<(item|entry)\b(.*?)</\1>', x, re.S):
                b = m.group(2)
                t = re.search(r'<title[^>]*>(.*?)</title>', b, re.S)
                d = re.search(r'<(pubDate|published|updated|dc:date)[^>]*>(.*?)</\1>', b, re.S)
                l = re.search(r'<link[^>]*?(?:href=["\']([^"\']+)["\'][^>]*/?>|>(.*?)</link>)', b, re.S)
                title = html.unescape(re.sub(r'<!\[CDATA\[|\]\]>', '', t.group(1)).strip()) if t else ''
                items.append({'title': title[:140], 'date': (d.group(2).strip()[:25] if d else ''),
                              'url': ((l.group(1) or l.group(2) or '').strip() if l else '')})
                if len(items) >= 25:
                    break
            out['feed'] = {'url': fu, 'count_seen': len(re.findall(r'<(item|entry)\b', x)), 'items': items}
            break
    out['appstore_ids'] = sorted(set(re.findall(r'apps\.apple\.com/[^"\']*?/id(\d{6,})', h)))
    return out


# ---------------- App Store ----------------
def itunes(q):
    try:
        return json.loads(curl('https://itunes.apple.com/' + q)).get('results', [])
    except Exception:
        return []


def appstore(ids):
    artists, apps = set(), {}
    for i in list(ids)[:8]:
        for c in ('us', 'cn'):
            r = itunes(f'lookup?id={i}&country={c}')
            if r:
                if r[0].get('artistId'):
                    artists.add((r[0]['artistId'], c))
                break
    for aid, c in list(artists)[:3]:
        for ent in ('software', 'macSoftware'):
            for r in itunes(f'lookup?id={aid}&entity={ent}&country={c}&limit=60'):
                if r.get('wrapperType') != 'software':
                    continue
                apps[r['trackId']] = {
                    'name': r.get('trackName'), 'artist': r.get('artistName'), 'genre': r.get('primaryGenreName'),
                    'price': r.get('formattedPrice'), 'released': (r.get('releaseDate') or '')[:10],
                    'updated': (r.get('currentVersionReleaseDate') or '')[:10], 'version': r.get('version'),
                    'rating': round(r.get('averageUserRating') or 0, 2), 'ratings': r.get('userRatingCount'),
                    'kind': r.get('kind'), 'url': (r.get('trackViewUrl') or '').split('?')[0],
                    'desc': (r.get('description') or '')[:900], 'country': c,
                }
    return list(apps.values())


# ---------------- 汇总 ----------------
def ghmap():
    m = {}
    for line in open(os.path.join(ROOT, 'research', 'ghmap.txt')):
        a = line.split()
        if len(a) == 2:
            m[a[0]] = a[1]
    return m


def candidates(h, data):
    urls = []
    for sec in data.get('sections', []):
        for b in sec.get('blocks', []):
            if 'site' in b:
                urls.append(b['site']['url'])
    for l in data.get('links', []):
        urls.append(l['url'])
    xu = json.load(open(os.path.join(ROOT, 'research', 'urls.json'))).get(h, [])
    urls += xu
    out, doms = [], set()
    for u in urls:
        d = urlparse(u).netloc.lower().removeprefix('www.')
        if not d or any(s in d for s in SKIP) or d in doms:
            continue
        doms.add(d)
        out.append(u)
    return out[:4]


def run(h):
    path = os.path.join(OUT, f'{h}.json')
    dp = os.path.join(ROOT, 'data', 'people', f'{h}.json')
    data = json.load(open(dp)) if os.path.exists(dp) else {}
    res = {'handle': h}
    login = ghmap().get(h)
    if not login:
        for m in re.findall(r'github\.com/([A-Za-z0-9-]+)(?:["/])', json.dumps(data)):
            if m.lower() not in ('orgs', 'sponsors', 'apps', 'features', 'topics'):
                login = m
                break
    res['sites'] = [site(u) for u in candidates(h, data)]
    if not login:
        for s_ in res['sites']:
            if s_.get('github_links'):
                login = s_['github_links'][0]
                res['github_guess'] = True
                break
    if login:
        res['github'] = github(login)
    ids = set(re.findall(r'apps\.apple\.com/[^"]*?/id(\d{6,})', json.dumps(data)))
    for s in res['sites']:
        ids |= set(s.get('appstore_ids', []))
    res['apps'] = appstore(ids) if ids else []
    json.dump(res, open(path, 'w'), ensure_ascii=False, indent=1)
    return h, len(res.get('github', {}).get('repos', [])), len(res['sites']), len(res['apps'])


if __name__ == '__main__':
    hs = sys.argv[1:] or [l.split()[0] for l in open(os.path.join(ROOT, 'research', 'handles.txt')) if l.strip()]
    with ThreadPoolExecutor(6) as ex:
        for r in ex.map(run, hs):
            print(*r, flush=True)
