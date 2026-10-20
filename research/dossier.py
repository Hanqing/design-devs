import json,sys,os
for h in sys.argv[1:]:
    print('#'*10,h)
    u=json.load(open(f'research/x/{h}.json')).get('user') or {}
    print('X:',u.get('name'),'|',u.get('followers'),'followers | joined',u.get('joined'),'|',u.get('location'),'|',(u.get('website') or {}).get('url'))
    print('BIO:',(u.get('description') or '').replace('\n',' '))
    g=json.load(open(f'research/gh/{h}.json')) if os.path.exists(f'research/gh/{h}.json') else {}
    if g.get('login'): print('GH:',g.get('login'),'|',g.get('name'),'|',g.get('company'),'|',g.get('location'),'|',g.get('blog'),'| followers',g.get('followers'),'| since',g.get('created_at'),'|',(g.get('bio') or '').replace('\n',' '))
    p=f'research/repos/{h}.json'
    if os.path.exists(p):
        for r in json.load(open(p))[:10]: print(f"  ★{r['stargazers_count']:>6} {r['name']} [{r['language']}] {r['created_at'][:4]} — {(r['description'] or '')[:120]}")
    s=open(f'research/sites/{h}.txt').read() if os.path.exists(f'research/sites/{h}.txt') else ''
    lim=int(os.environ.get('LIM','3000'))
    print('SITE:',s[:lim].replace('\n\n','\n'))
