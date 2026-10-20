import json,re,subprocess,html,sys,concurrent.futures as cf
urls=json.load(open('research/urls.json'))
def text(u):
    try:
        r=subprocess.run(['curl','-sL','-m','20','-A','Mozilla/5.0 (Macintosh) AppleWebKit Safari',u],capture_output=True,timeout=30)
        s=r.stdout.decode('utf-8','ignore')
    except Exception as e: return ''
    t=re.search(r'<title[^>]*>(.*?)</title>',s,re.S)
    md=re.search(r'<meta[^>]+name="description"[^>]+content="([^"]*)"',s)
    s=re.sub(r'<(script|style|svg|noscript)[^>]*>.*?</\1>','',s,flags=re.S|re.I)
    links=re.findall(r'<a[^>]+href="(http[^"]+)"[^>]*>(.*?)</a>',s,re.S)
    body=html.unescape(re.sub(r'\s+',' ',re.sub(r'<[^>]+>',' ',s))).strip()
    ls='\n'.join(f'- {html.unescape(re.sub("<[^>]+>","",b)).strip()[:60]} -> {a}' for a,b in links[:80])
    return f'URL: {u}\nTITLE: {t and html.unescape(t.group(1).strip())}\nDESC: {md and html.unescape(md.group(1))}\n\n{body[:6000]}\n\nLINKS:\n{ls}\n'
def job(h):
    res=''.join(text(u)+'\n=====\n' for u in urls[h][:3] if 'github.com' not in u and 'x.com' not in u and 't.me' not in u)
    open(f'research/sites/{h}.txt','w').write(res)
    return h,len(res)
with cf.ThreadPoolExecutor(12) as ex:
    for h,n in ex.map(job,urls): print(h,n,end='; ')
