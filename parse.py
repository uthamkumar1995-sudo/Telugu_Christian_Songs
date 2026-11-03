import re
SRC="/mnt/user-data/uploads/andhra_kraistava_keerthanalu_songs__1_.txt"
def songs():
    txt=open(SRC,encoding='utf-8').read().split('\n')
    res={};cur=None
    for ln in txt:
        m=re.match(r'^│\s+కీర్తన (\d+) — (.+)$',ln)
        if m:
            cur={'n':int(m.group(1)),'title':m.group(2).strip(),'lines':[],'composer':''}
            res[cur['n']]=cur;continue
        if cur is None: continue
        if ln.startswith('╰'): cur=None;continue
        if ln.startswith('│  –'): cur['composer']=ln[1:].strip(' –'); continue
        if ln.startswith('│'): cur['lines'].append(ln[1:])
    return res
def clean(s):
    s=re.sub(r'॥.*?॥','',s).replace('॥','')
    s=re.sub(r'\s*–\s*',' ',s)
    s=re.sub(r'[¹²³⁴⁵⁶⁷⁸⁹⁰]','',s)
    s=s.replace(' ః ',' : ')
    return re.sub(r'\s+',' ',s).strip(' ;')
def pallavi(song):
    L=song['lines'];out=[];on=False
    for l in L:
        if 'పల్లవి' in l: on=True;continue
        if on:
            if re.match(r'\s*\d+\.',l) or not l.strip(): 
                if out: break
                continue
            out.append(l.strip())
    return clean(' '.join(out))
def verses_text(song):
    return '\n'.join(x for x in song['lines'] if x.strip())

def preview(song):
    t=pallavi(song)
    if t: return t
    out=[];on=False
    for l in song['lines']:
        m=re.match(r'\s*\d+\.\s*(.*)',l)
        if m: on=True;out.append(m.group(1));continue
        if on:
            if not l.strip(): break
            out.append(l.strip())
    return clean(' '.join(out))

def paragraphs(song):
    paras=[];cur=None
    for l in song['lines']:
        if 'అర్థములు' in l or 'సూచనలు' in l: break
        if 'పల్లవి' in l and l.strip().endswith(':'):
            cur=['పల్లవి',[]];paras.append(cur);continue
        m=re.match(r'\s*(\d+)\.\s*(.*)',l)
        if m:
            cur=[m.group(1),[m.group(2)]];paras.append(cur);continue
        if not l.strip(): continue
        if cur is None: cur=['',[]];paras.append(cur)
        cur[1].append(l.strip())
    return [(k,clean(' '.join(v))) for k,v in paras if clean(' '.join(v))]
