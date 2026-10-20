import json,re,subprocess,os,html,sys
hs=open('research/handles.txt').read().split()
out={}
for h in hs:
    u=(json.load(open(f'research/x/{h}.json')).get('user') or {})
    urls=[]
    w=(u.get('website') or {}).get('url')
    if w: urls.append(w)
    for f in (u.get('raw_description') or {}).get('facets',[]):
        if f.get('type')=='url': urls.append('https://'+f['replacement'].split('://')[-1])
    out[h]=urls
json.dump(out,open('research/urls.json','w'),indent=1,ensure_ascii=False)
