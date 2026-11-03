#!/usr/bin/env python3
"""Daily builder: publishes the next N unpublished songs into ./site
Usage: python3 build_site.py [N=10]   (edit BASE_URL in config.json first)"""
import json,os,sys,html,datetime
from parse import songs,paragraphs,preview
from translit import tr,slug
from make_cards import card
N=int(sys.argv[1]) if len(sys.argv)>1 else 10
cfg=json.load(open('config.json'))
BASE=cfg['base_url'].rstrip('/');BOOK=cfg['book_en'];BOOK_TE=cfg['book_te']
os.makedirs('site/images',exist_ok=True);os.makedirs('site/songs',exist_ok=True)
prog=json.load(open('progress.json')) if os.path.exists('progress.json') else {'done':{}}
S=songs();todo=[n for n in sorted(S) if str(n) not in prog['done']][:N]
today=datetime.date.today().isoformat()
def first_line(s,k=7): return ' '.join(preview(s).split()[:k])
for n in todo:
    s=S[n];sl=slug(s['title'])
    base='%s-andhra-kristava-kirtanalu-song-%d'%(sl,n)
    card(s,'site/images/%s.png'%base)
    fl=first_line(s);fl_en=tr(fl);t_en=tr(s['title']).title()
    title='%s – %s | కీర్తన %d | %s'%(fl,s['title'],n,BOOK_TE)
    alt='%s (%s) – %s Song %d, %s lyrics'%(fl,fl_en,t_en,n,BOOK)
    body=''
    for k,t in paragraphs(s):
        if k=='': continue
        lab='పల్లవి (Pallavi)' if k=='పల్లవి' else 'చరణం %s'%k
        body+='<h2>%s</h2><p>%s</p>\n'%(lab,html.escape(t))
    page='''<!doctype html><html lang="te"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>%(title)s</title>
<meta name="description" content="%(desc)s">
<link rel="canonical" href="%(base)s/songs/%(b)s.html">
<meta property="og:title" content="%(title)s"><meta property="og:image" content="%(base)s/images/%(b)s.png">
<style>body{font-family:'Noto Sans Telugu',system-ui,sans-serif;background:#3a0a14;color:#faeed6;margin:0;line-height:1.9}main{max-width:760px;margin:auto;padding:20px}
img{width:100%%;height:auto;border:2px solid #e2b860;border-radius:8px}h1,h2{color:#e2b860}a{color:#e2b860}footer{text-align:center;opacity:.8;padding:20px}</style></head><body><main>
<p><a href="../index.html">← %(book)s</a></p>
<h1>%(h1)s</h1>
<img src="../images/%(b)s.png" alt="%(alt)s" title="%(alt)s" width="1200" loading="eager">
<p><em>%(en)s</em></p>
%(body)s<p>– %(comp)s</p>
<footer>Telugu Christian Songs · by UTHAM</footer></main></body></html>'''%dict(
        title=html.escape(title),desc=html.escape('%s – %s. %s కీర్తన %d పూర్తి సాహిత్యం (lyrics). %s'%(fl,s['title'],BOOK_TE,n,fl_en)),
        base=BASE,b=base,book=BOOK_TE,h1=html.escape('కీర్తన %d – %s'%(n,s['title'])),alt=html.escape(alt),
        en=html.escape('%s – %s'%(t_en,fl_en)),body=body,comp=html.escape(s['composer']))
    open('site/songs/%s.html'%base,'w',encoding='utf-8').write(page)
    prog['done'][str(n)]={'base':base,'title':s['title'],'first':fl,'date':today}
    print('published',n,base)
json.dump(prog,open('progress.json','w'),ensure_ascii=False,indent=1)
# index (all published, grouped by number)
items=''.join('<li><a href="songs/%s.html">%s. %s</a> – %s</li>\n'%(v['base'],n,html.escape(v['title']),html.escape(v['first'])) for n,v in sorted(prog['done'].items(),key=lambda x:int(x[0])))
open('site/index.html','w',encoding='utf-8').write('''<!doctype html><html lang="te"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>%s – Telugu Christian Songs Lyrics | by UTHAM</title><meta name="description" content="%s – full lyrics with pallavi and charanalu. Telugu Christian Songs by UTHAM.">
<link rel="canonical" href="%s/"><style>body{font-family:'Noto Sans Telugu',system-ui,sans-serif;background:#3a0a14;color:#faeed6;max-width:760px;margin:auto;padding:20px;line-height:1.9}h1{color:#e2b860}a{color:#e2b860}</style></head><body>
<h1>%s</h1><p>Telugu Christian Songs · by UTHAM</p><ul>%s</ul></body></html>'''%(BOOK_TE,BOOK_TE,BASE,BOOK_TE,items))
# sitemap with image entries
u='<url><loc>%s/</loc></url>\n'%BASE
for n,v in sorted(prog['done'].items(),key=lambda x:int(x[0])):
    u+='<url><loc>%s/songs/%s.html</loc><lastmod>%s</lastmod><image:image><image:loc>%s/images/%s.png</image:loc></image:image></url>\n'%(BASE,v['base'],v['date'],BASE,v['base'])
open('site/sitemap.xml','w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n'+u+'</urlset>')
open('site/robots.txt','w').write('User-agent: *\nAllow: /\nSitemap: %s/sitemap.xml\n'%BASE)
print('done: %d total published, %d remaining'%(len(prog['done']),len(S)-len(prog['done'])))
