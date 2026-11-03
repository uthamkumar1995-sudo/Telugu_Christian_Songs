import sys,random,math
from PIL import Image,ImageDraw,ImageFont,ImageFilter
from parse import songs,preview,paragraphs
from translit import tr,slug
W,H=1200,630
F='fonts/NotoSansTelugu-%s.ttf'
GOLD=(226,184,96);CREAM=(250,238,214);MAROON=(88,14,28)
LOGO=Image.open('/mnt/user-data/uploads/07_music_cross_appicon_full_1024.png').convert('RGBA')
def font(w,s): return ImageFont.truetype(F%w,s,layout_engine=ImageFont.Layout.RAQM)
def bg(H):
    from PIL import ImageChops
    img=Image.new('RGB',(W,H));d=ImageDraw.Draw(img)
    for y in range(H):
        t=y/H;d.line((0,y,W,y),fill=tuple(int(a+(b-a)*t) for a,b in zip((120,22,38),(52,6,16))))
    glow=Image.new('RGB',(W,H),(0,0,0));gd=ImageDraw.Draw(glow)
    gd.ellipse((W/2-420,H/2-min(H/2,400),W/2+420,H/2+min(H/2,400)),fill=(150,80,30))
    glow=glow.filter(ImageFilter.GaussianBlur(160))
    img=ImageChops.add(img,glow.point(lambda v:int(v*0.5)))
    r=random.Random(7);ov=Image.new('RGBA',(W,H),(0,0,0,0));od=ImageDraw.Draw(ov)
    for _ in range(max(26,H//24)):
        x,y,s=r.randint(0,W),r.randint(0,H),r.randint(6,26)
        od.ellipse((x-s,y-s,x+s,y+s),fill=(255,210,130,r.randint(14,38)))
    ov=ov.filter(ImageFilter.GaussianBlur(2))
    img=Image.alpha_composite(img.convert('RGBA'),ov)
    d=ImageDraw.Draw(img)
    d.rectangle((20,20,W-21,H-21),outline=GOLD,width=2)
    d.rectangle((28,28,W-29,H-29),outline=(226,184,96,90),width=1)
    return img
def wrap(d,text,f,maxw):
    lines=[];cur=''
    for w in text.split():
        t=(cur+' '+w).strip()
        if d.textlength(t,font=f)<=maxw: cur=t
        else: lines.append(cur);cur=w
    if cur: lines.append(cur)
    return lines
def card(s,path):
    from PIL import ImageFont as IF
    tmp=ImageDraw.Draw(Image.new('RGB',(10,10)))
    tf=font('Bold',60)
    for sz in (60,52,44,38):
        tf=font('Bold',sz);tl=wrap(tmp,s['title'],tf,W-200)
        if len(tl)<=2: break
    lf=font('Regular',32);lab=font('Medium',26);MW=W-240;pf=font('Bold',42)
    blocks=[]
    sub=''
    for k,t in paragraphs(s):
        if k=='':
            if len(t)>3 and not sub: sub=t
            continue
        blocks.append((k,wrap(tmp,t,lf,MW)))
    sf=font('Regular',26)
    y=130+len(tl)*int(tf.size*1.5)+40+(50 if sub else 0)
    for k,ls in blocks: y+=44+len(ls)*54+18
    if s['composer']: y+=60
    H=max(630,y+150)
    img=bg(H);d=ImageDraw.Draw(img)
    d.text((W//2,64),"కీర్తన %d"%s['n'],font=font('Medium',30),fill=GOLD,anchor='mm')
    y=130
    for l in tl:
        d.text((W//2,y),l,font=tf,fill=GOLD,anchor='ma');y+=int(tf.size*1.5)
    d.line((W//2-90,y+2,W//2+90,y+2),fill=GOLD,width=2);y+=30
    if sub: d.text((W//2,y),sub,font=sf,fill=(226,200,150),anchor='ma');y+=50
    else: y+=10
    for k,ls in blocks:
        label=k if k=='పల్లవి' else k+'.'
        if False:
            bh=44+len(ls)*76+10
            ov=Image.new('RGBA',(W,H),(0,0,0,0));ImageDraw.Draw(ov).rounded_rectangle((80,y-12,W-80,y-12+bh+12),20,fill=(40,4,12,110),outline=(226,184,96,150),width=2)
            img.alpha_composite(ov);d=ImageDraw.Draw(img)
            d.text((120,y),label,font=lab,fill=GOLD);y+=44
            for l in ls:
                d.text((120,y),l,font=pf,fill=(255,244,220));y+=76
            y+=50;continue
        d.text((120,y),label,font=lab,fill=GOLD);y+=44
        for l in ls:
            d.text((120,y),l,font=lf,fill=CREAM);y+=54
        y+=18
    if s['composer']:
        d.text((W-120,y+10),'– '+s['composer'],font=lab,fill=GOLD,anchor='ra')
    fy=H-112
    d.line((60,fy,W-60,fy),fill=(226,184,96,110),width=1)
    lg=LOGO.resize((80,80),Image.LANCZOS)
    m=Image.new('L',(80,80),0);ImageDraw.Draw(m).rounded_rectangle((0,0,79,79),16,fill=255)
    img.paste(lg,(64,fy+12),m)
    d.text((160,fy+24),"Telugu Christian Songs",font=font('Medium',24),fill=GOLD)
    d.text((160,fy+56),"by UTHAM",font=font('Regular',19),fill=(226,184,96,200))
    d.text((W-64,fy+50),"ఆంధ్ర క్రైస్తవ కీర్తనలు",font=font('Regular',24),fill=CREAM,anchor='rm')
    img.convert('RGB').save(path,optimize=True)
if __name__=='__main__':
    a,b=int(sys.argv[1]),int(sys.argv[2]);S=songs()
    for n in range(a,b+1):
        s=S[n];p='out/%s-andhra-kristava-kirtanalu-song-%d.png'%(slug(s['title']),n);card(s,p);print(p)
