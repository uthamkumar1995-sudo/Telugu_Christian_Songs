# Simple Telugu -> Latin transliteration (readable, for filenames/alt text)
V={'అ':'a','ఆ':'aa','ఇ':'i','ఈ':'ee','ఉ':'u','ఊ':'oo','ఋ':'ru','ఎ':'e','ఏ':'e','ఐ':'ai','ఒ':'o','ఓ':'o','ఔ':'au'}
M={'ా':'aa','ి':'i','ీ':'ee','ు':'u','ూ':'oo','ృ':'ru','ె':'e','ే':'e','ై':'ai','ొ':'o','ో':'o','ౌ':'au'}
C={'క':'k','ఖ':'kh','గ':'g','ఘ':'gh','ఙ':'ng','చ':'ch','ఛ':'chh','జ':'j','ఝ':'jh','ఞ':'ny','ట':'t','ఠ':'th','డ':'d','ఢ':'dh','ణ':'n','త':'t','థ':'th','ద':'d','ధ':'dh','న':'n','ప':'p','ఫ':'ph','బ':'b','భ':'bh','మ':'m','య':'y','ర':'r','ఱ':'r','ల':'l','ళ':'l','వ':'v','శ':'sh','ష':'sh','స':'s','హ':'h'}
def tr(s):
    out=[];i=0
    while i<len(s):
        ch=s[i]
        if ch in C:
            b=C[ch];i+=1
            if i<len(s) and s[i]=='్': out.append(b);i+=1
            elif i<len(s) and s[i] in M: out.append(b+M[s[i]]);i+=1
            else: out.append(b+'a')
        elif ch in V: out.append(V[ch]);i+=1
        elif ch=='ం': out.append('m');i+=1
        elif ch in 'ః': out.append('h');i+=1
        elif ch in 'ఁ': i+=1
        elif ch.isascii(): out.append(ch);i+=1
        else: out.append(' ');i+=1
    t=''.join(out)
    # drop trailing inherent 'a' before space/end for readability
    import re
    t=re.sub(r'a(?= |$)','',t) if False else t
    return re.sub(r'\s+',' ',t).strip()
def slug(s):
    import re
    return re.sub(r'[^a-z0-9]+','-',tr(s).lower()).strip('-')
