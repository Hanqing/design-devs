import sys,re,html,subprocess
lim=int(sys.argv[2]) if len(sys.argv)>2 else 4000
u=sys.argv[1]
s=subprocess.run(['curl','-sL','-m','25','-A','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 Safari/605.1.15',u],capture_output=True).stdout.decode('utf-8','ignore')
s=re.sub(r'<(script|style|svg|noscript|head)[^>]*>.*?</\1>','',s,flags=re.S|re.I)
s=re.sub(r'<(br|p|div|li|h\d|tr)[^>]*>','\n',s,flags=re.I)
t=html.unescape(re.sub(r'<[^>]+>',' ',s))
t=re.sub(r'[ \t]+',' ',t); t=re.sub(r'\n\s*\n+','\n',t)
print(t.strip()[:lim])
