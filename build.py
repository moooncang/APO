# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from data import FACTIONS, C, CR
from detail import DETAIL

OUT = os.path.dirname(os.path.abspath(__file__))
TITLE = "TAMER IN APOCALYPSE"
KR = "테이머 IN 아포칼립스"
DESC = "붕괴 후 30년, 무저갱. 5개 세력과 19인, 그리고 그들이 계약한 파트너 19종. 크랙 채팅봇."
CRACK = "#"   # 봇 링크 확정되면 이 값만 교체

NAV = [("home.html","HOME"),("world.html","WORLD"),("factions.html","FACTIONS"),
       ("characters.html","CHARACTERS"),("creatures.html","CREATURES"),("play.html","PLAY")]

def head(page, title, up=""):
    ON = ' class="on"'
    nav = "\n".join('      <li><a href="%s%s"%s>%s</a></li>' % (up, h, ON if h==page else "", t)
                    for h,t in NAV if h!="home.html")
    return f'''<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{DESC}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{DESC}">
<meta property="og:type" content="website">
<link rel="preconnect" href="https://cdn.jsdelivr.net">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css">
<link rel="stylesheet" href="{up}assets/css/style.css">
</head>
<body>
<header>
  <nav class="nav">
    <a class="brand" href="{up}home.html">TAMER IN APOCALYPSE</a>
    <button class="navtoggle" aria-label="메뉴">MENU</button>
    <ul>
{nav}
    </ul>
  </nav>
</header>
<main>
'''

def foot(up=""):
    return f'''</main>
<footer>
  <div class="wrap">
    <div>TAMER IN APOCALYPSE<br><span style="color:var(--dimmer)">크랙 채팅봇 · 수록 이미지는 전부 생성물이며 무단 전재를 금합니다</span></div>
    <div><a href="{CRACK}">크랙에서 플레이 →</a></div>
  </div>
</footer>
<script src="{up}assets/js/main.js"></script>
</body>
</html>'''

CRT = """
<div id="crt" hidden><div class="fl"></div><div class="cb top"></div><div class="cb bot"></div><div class="cl"></div></div>
<script>
(function(){
  var on=false;
  try{ on = sessionStorage.getItem('crt')==='1'; if(on) sessionStorage.removeItem('crt'); }catch(e){}
  if(!on) return;
  var el=document.getElementById('crt'); if(!el) return;
  el.hidden=false;
  requestAnimationFrame(function(){ el.classList.add('play'); });
  setTimeout(function(){ el.hidden=true; }, 1000);
})();
</script>
"""

def fac(s): return FACTIONS[s]
def cvar(s): return f'--fc:{fac(s)["color"]}'

CMAP  = {c[0]: c for c in C}
CRMAP = {c[5]: c for c in CR}

def sec(label, lead_h2=None, lead_p=None):
    h = f'  <div class="lbl rv">{label}</div>\n'
    if lead_h2: h += f'  <h2 class="rv">{lead_h2}</h2>\n'
    if lead_p:  h += f'  <p class="lead rv">{lead_p}</p>\n'
    return h

# ─────────────────────────────────────────── index (표지)
def build_index():
    fx = "".join(f'''
      <a class="fxc" href="factions.html#{s}" style="{cvar(s)}">
        <div class="fno">F-0{i+1}</div>
        <img src="assets/img/symbol/{s}.png" alt="{d['kr']} 문장" loading="lazy">
        <div class="fn">{d['kr']}</div><div class="fe">{d['en']}</div>
        <div class="fs">{d['short']}</div>
      </a>''' for i,(s,d) in enumerate(FACTIONS.items()))

    ids = "".join(f'''
      <a class="idc" href="char/{c[0]}.html" style="{cvar(c[3])}">
        <div class="ih"><span class="mono">P-{i+1:02d}</span><b>{fac(c[3])['en']}</b></div>
        {'<span class="irk">RANKER</span>' if c[6] else ''}
        <img src="assets/img/char/{c[0]}.webp" alt="{c[1]}" loading="lazy">
        <div class="ib"><div class="inm">{c[1]}</div><div class="ien">{c[2]}</div></div>
      </a>''' for i,c in enumerate(C))

    TOC = [("01","WORLD","world.html","무저갱의 지형과 이 세계가 굴러가는 규칙"),
           ("02","FACTIONS","factions.html","4대 조직과 부랑자, 그리고 그 사이의 균형"),
           ("03","CHARACTERS","characters.html","이름이 붙은 인물 19인의 개별 기록"),
           ("04","CREATURES","creatures.html","계열과 진화 단계, 확인된 파트너 도감"),
           ("05","PLAY","play.html","시작 모드와 정보창, 플레이 전 주의사항")]
    toc = "".join(f'''
      <a href="{h}"><span class="no mono">{n}</span><span class="en">{e}</span>
        <span class="dots"></span><span class="ko">{k}</span><span class="ar">→</span></a>'''
      for n,e,h,k in TOC)

    return head("home.html", f"{TITLE} — {KR}") + f'''<section class="cover"><div class="wrap">
  <div class="sheet">
    <div class="sheet-tab">ABYSS ARCHIVE</div>
    <div class="sheet-no mono">RETRIEVED 30.214 · 06 SHEETS</div>
    <div class="docmeta mono">
      <span>DOC NO.<b>TIA-001</b></span>
      <span>CLASS<b class="red">RESTRICTED</b></span>
      <span>ORIGIN<b>무저갱 / ABYSS</b></span>
      <span>STATUS<b>OPEN</b></span>
    </div>
    <div class="cover-grid">
      <div class="cover-l">
        <p class="kicker">FIELD DOSSIER · 현장 기록</p>
        <h1>TAMER IN<br>APOCALYPSE</h1>
        <p class="cover-kr">테이머 IN 아포칼립스</p>
        <p class="abstract">30년 전 열린 균열은 아직 닫히지 않았다. 국가도 행정도 남지 않은 이 땅에서,
          살아남은 사람들은 균열 너머에서 건너온 짐승과 계약해 하루를 번다.
          이 문서는 그 이후의 기록을 정리한 것이다.</p>
        <dl class="fields mono">
          <div><dt>SUBJECT</dt><span class="dots"></span><dd>균열 · 크리처 · 테이머</dd></div>
          <div><dt>ELAPSED</dt><span class="dots"></span><dd>붕괴 후 30년</dd></div>
          <div><dt>SECTORS</dt><span class="dots"></span><dd>심층 · 잔해지 · 거점지대</dd></div>
          <div><dt>RECORDS</dt><span class="dots"></span><dd>세력 5 · 인물 19 · 파트너 18 + 1</dd></div>
        </dl>
        <div class="btns">
          <a class="btn pri" href="{CRACK}">크랙에서 플레이</a>
          <a class="btn" href="world.html">문서 열람</a>
        </div>
      </div>
      <figure class="plate">
        <img src="assets/img/bg/hero.webp" alt="">
        <span class="stamp">RESTRICTED</span>
        <figcaption class="mono">PLATE 01 · 잔해지 남부 — 6단계 개체 접촉 기록 / 촬영자 미상</figcaption>
      </figure>
    </div>
    <div class="barcode"></div>
  </div>
</div></section>

<section><div class="wrap">
{sec("CONTENTS","수록 문서 다섯 건","각 항목은 독립된 기록으로, 어디부터 읽어도 상관없다.")}
  <nav class="toc rv">{toc}
  </nav>
</div></section>

<section><div class="wrap">
{sec("ABSTRACT","먼저 알아야 할 세 가지","나머지 기록은 전부 이 세 항목 위에 얹혀 있다.")}
  <div class="recs rv">
    <div class="rec"><div class="rh mono"><span>A-01</span><b>RIFT</b></div>
      <div class="rb">균열은 30년 전 각지에서 동시에 열렸고 지금도 간헐적으로 열린다.
        여는 조건도 닫는 방법도 아직 밝혀진 바가 없다.</div></div>
    <div class="rec"><div class="rh mono"><span>A-02</span><b>PARTNER</b></div>
      <div class="rb">생존자는 한 사람당 파트너 한 체를 둔다. 선택이 아니라 생존 조건에 가깝고, 둘 이상은 불가능하다.
        싸우는 쪽은 언제나 파트너이고, 테이머가 하는 일은 지시와 판단이다.</div></div>
    <div class="rec"><div class="rh mono"><span>A-03</span><b>FACTION</b></div>
      <div class="rb">네 개의 큰 조직과, 어디에도 속하지 않은 부랑자들이 있다.
        불가침 협정은 존재하지만 문서로 남은 적은 한 번도 없다.</div></div>
  </div>
</div></section>

<section><div class="wrap">
{sec("FACTION INDEX","무저갱을 나눠 가진 다섯","앞의 넷은 서로를 견제하며 아슬아슬한 균형을 유지하고 있고, 부랑자는 그 사이를 오가는 변수다.")}
  <div class="fx rv">{fx}
  </div>
  <p class="more rv"><a href="factions.html">세력별 편제와 소속 인물 보기 →</a></p>
</div></section>

<section><div class="wrap">
{sec("PERSONNEL","등재된 인물 열아홉","세력마다 랭커가 한 명씩 있고, 다섯 명 전원이 6단계 이상의 파트너를 데리고 있다. 카드를 누르면 개별 기록으로 넘어간다.")}
  <div class="idrail rv">{ids}
  </div>
  <p class="more rv"><a href="characters.html">전체 목록 보기 →</a></p>
</div></section>

<section><div class="wrap">
{sec("ENTRY","어느 쪽에서 시작할지 고른다","세션을 시작할 때 한 번 정하고, 이후 AI가 임의로 바꾸지 않는다.")}
  <div class="entry rv">
    <div><div class="eh"><span class="eno mono">E-01</span><span class="een">SYNDICATE</span></div>
      <div class="et">여명 · 라그나로크 · 라이징 중 하나를 골라 소속으로 시작한다.</div>
      <div class="ed">조직 안의 입지와 임무를 처음부터 가지고 출발하며, 명령은 대체로 위에서 내려온다.</div></div>
    <div><div class="eh"><span class="eno mono">E-02</span><span class="een">HAWK</span></div>
      <div class="et">호크 소속으로 시작하고, 나머지 전체와 적대한다.</div>
      <div class="ed">약탈과 습격이 일상이 되는 대신, 등 뒤를 가장 조심해야 하는 곳은 조직 안쪽이다.</div></div>
    <div><div class="eh"><span class="eno mono">E-03</span><span class="een">VAGABOND</span></div>
      <div class="et">무소속. 모든 세력과 중립에서 경계 사이에 놓인다.</div>
      <div class="ed">자유도가 가장 높고, 원한다면 나중에 어느 쪽으로든 들어갈 수 있다.</div></div>
  </div>
</div></section>
{CRT}''' + foot()

# ─────────────────────────────────────────── world
def build_world():
    terr = [
      ("심층","DEEP","deep",
       "구 도심이 그대로 묻혀 있는 구역이다. 균열이 가장 촘촘하게 몰려 있고 재해급 개체가 서식한다. 들어가는 사람은 있어도 돌아 나오는 사람은 드물다."),
      ("잔해지","RUINS","ruins",
       "심층과 거점지대 사이에 깔린 폐허 벨트. 누구의 관할도 아니라서 거래와 약탈이 같은 자리에서 벌어진다. 대부분의 사건이 여기서 시작된다."),
      ("거점지대","STRONGHOLD","base",
       "외곽에 자리 잡은 네 조직의 요새다. 배급과 치안이 돌아가는 유일한 구역이지만, 그 규칙은 어디까지나 담장 안에서만 작동한다."),
    ]
    t = "".join(f'''
    <div class="terr rv">
      <img src="assets/img/bg/{img}.webp" alt="{n}" loading="lazy">
      <div class="t-in"><div class="t-e">{en}</div><div class="t-n">{n}</div><div class="t-d">{d}</div></div>
    </div>''' for n,en,img,d in terr)

    return head("world.html", f"WORLD — {TITLE}") + f'''<section><div class="wrap">
{sec("TIMELINE","30년 전에 한 번 끝났다","재건 시도는 전부 무산됐고, 지금 남은 것은 그 잔해 위에 다시 세워진 질서뿐이다.")}
  <div class="steps rv">
    <div><div class="n">-30</div><div class="t">붕괴</div><div class="d">각지에 균열이 열리며 크리처가 대량으로 넘어왔다. 국가와 행정은 몇 달을 버티지 못하고 무너졌다.</div></div>
    <div><div class="n">-30 → 0</div><div class="t">재건 실패</div><div class="d">여러 차례 시도가 있었지만 전부 무산됐다. 구 세계의 지식도 이 과정에서 대부분 소실됐다.</div></div>
    <div><div class="n">NOW</div><div class="t">현재</div><div class="d">균열은 지금도 간헐적으로 열린다. 닫는 방법은 여전히 알려지지 않았다.</div></div>
  </div>
  <p class="hint rv">서른 살이 넘은 사람은 대붕괴를 어렴풋이 기억한다. 그 아래 세대는 붕괴 이후의 세계밖에 모른다.</p>
</div></section>

<section><div class="wrap">
{sec("TERRAIN","무대는 무저갱, 세 겹으로 나뉜다","안쪽으로 들어갈수록 균열이 잦아지고, 바깥으로 나올수록 규칙이 생긴다.")}
  {t}
</div></section>

<section><div class="wrap">
{sec("RULES","이 세계가 굴러가는 방식","알아 두지 않으면 첫날부터 막히는 것들만 모았다.")}
  <div class="stack rv">
    <div><div class="k">화폐</div><div class="v">돈은 붕괴와 함께 종잇장이 됐다. 지금 통용되는 것은 <b>크리처 사체에서 나오는 코어와 파편</b>이며, 이것은 화폐인 동시에 파트너를 강화하는 자원이기도 하다.</div></div>
    <div><div class="k">테이머</div><div class="v">생존자는 전원 파트너 한 체를 둔다. 그중 실제로 싸울 수 있는 사람은 소수고, 대다수는 1단계 언저리에서 멈춘다. 그 정점에 있는 다섯 명을 <b>랭커</b>라고 부른다.</div></div>
    <div><div class="k">계약</div><div class="v">계약에 필요한 도구나 매개물은 없다. 손을 대고 서로 받아들이면 그것으로 성립한다.<br>다만 <b>한 사람이 맺을 수 있는 계약은 하나뿐이다.</b> 파트너가 살아 있는 한 다른 개체와는 계약할 수 없고, 잃은 뒤에야 다시 가능해진다.</div></div>
    <div><div class="k">전투</div><div class="v">싸우는 쪽은 파트너다. 테이머가 맡는 것은 <b>지시와 판단, 그리고 엄호</b>다. 사람이 직접 무기를 들고 맞붙는 장면은 극히 드물게만 나온다.</div></div>
    <div><div class="k">육체</div><div class="v">파트너가 강해질수록 테이머의 몸도 그 성질을 닮아 간다. 브루트를 데리고 다니면 완력이, 헥스를 데리고 다니면 감각이 예민해지는 식이다. 다만 튼튼해지는 수준이지 <b>초인이 되지는 않는다</b>.</div></div>
    <div><div class="k">불가침</div><div class="v">안전지대 안에서는 싸우지 않는다는 식의 암묵적 협정이 있다. 문서로 남은 적은 없고, 그래서 언제든 깨질 수 있는 균형이다.</div></div>
  </div>
</div></section>

<section><div class="wrap">
{sec("RIFT","균열에 대해 알려진 것","30년 동안 사람들이 알아낸 것은 생각보다 적다.")}
  <div class="stack rv">
    <div><div class="k">확인된 것</div><div class="v">30년 전 각지에서 동시에 열렸고, 지금도 간헐적으로 열린다. 새로운 개체는 예외 없이 이쪽을 통해 들어온다.</div></div>
    <div><div class="k">확인되지 않은 것</div><div class="v">여는 조건, 닫는 방법, 그리고 저편에 무엇이 있는지. 세 가지 모두 30년째 그대로다.</div></div>
  </div>
  <p class="rumor rv">다만 심층 안쪽까지 혼자 들어갔다 나오는 노인이 하나 있다는 이야기가 잔해지에 돈다. 그가 무엇을 봤다고 말하든, 증명할 방법이 없어 아무도 믿지 않는다.</p>
</div></section>
''' + foot()

# ─────────────────────────────────────────── factions
def build_factions():
    secs = []
    for s,d in FACTIONS.items():
        mem = [c for c in C if c[3]==s]
        chips = "".join(f'<a href="char/{c[0]}.html">{c[1]}<span> · {c[4]}</span></a>' for c in mem)
        slog = (f'<p class="slogan rv">"{d["slogan"]}"</p>' if d["slogan"]
                else '<p class="slogan rv">내건 슬로건도 깃발도 없다. 그래서 어디든 드나들 수 있다.</p>')
        rumor = f'<p class="rumor rv">{d["rumor"]}</p>' if d["rumor"] else ""
        secs.append(f'''<section class="fac" id="{s}" style="{cvar(s)}">
  <img class="ghost" src="assets/img/symbol/{s}.png" alt="" loading="lazy">
  <div class="in">
    <div class="head rv">
      <img src="assets/img/symbol/{s}.png" alt="{d['kr']} 문장">
      <div><div class="en">{d['en']}</div><h2>{d['kr']}</h2></div>
    </div>
    {slog}
    <p class="lead rv">{d['body']}</p>
    <div class="spec rv">
      <div><dt>거점</dt><dd>{d['base']}</dd></div>
      <div><dt>편제</dt><dd>{d['org']}</dd></div>
      <div><dt>규모</dt><dd>{d['scale']}</dd></div>
      <div><dt>하는 일</dt><dd>{d['role']}</dd></div>
    </div>
    <div class="members rv">{chips}</div>
    {rumor}
  </div>
</section>''')
    intro = f'''<section><div class="wrap">
{sec("STRUCTURE","판도는 이렇게 짜여 있다","네 조직이 무저갱을 나눠 가졌고, 그 바깥에 이름 없는 무리와 부랑자가 있다.")}
  <div class="stack rv">
    <div><div class="k">신디케이트 · 4대 조직</div><div class="v"><b>여명 · 라그나로크 · 라이징 · 호크</b>를 묶어 그렇게 부른다. 앞의 셋은 서로를 견제하면서도 불가침에 가까운 균형을 유지하고 있고, 호크는 나머지 전부의 공공의 적이다.</div></div>
    <div><div class="k">군소 세력</div><div class="v">네 조직 바깥에도 구역 패거리와 생존자 공동체, 약탈단이 각지에 흩어져 있다. 대개는 큰 조직에 줄을 대거나 상납하며 연명하고, 독립을 고수하면 토벌되거나 흡수된다.</div></div>
    <div><div class="k">부랑자</div><div class="v">어느 쪽에도 속하지 않은 생존자를 통칭한다. 갈 곳이 없어서 떠도는 난민도 있고, 소속이 필요 없을 만큼 강해서 떠도는 개인도 있다.</div></div>
  </div>
</div></section>'''
    return head("factions.html", f"FACTIONS — {TITLE}") + intro + "\n".join(secs) + foot()

# ─────────────────────────────────────────── characters (목록)
def build_characters():
    cards = []
    for slug,kr,en,f,role,age,rk,mbti,arch,p,sk,no in C:
        pn = p[0] if p else "???"
        pd = f"{p[1]} · {p[2]}" if p else "??? · ???"
        cards.append(f'''
    <a class="card" href="char/{slug}.html" data-f="{f}" style="{cvar(f)}">
      <div class="ph"><span class="bar"></span>{'<span class="rk">RANKER</span>' if rk else ''}
        <img src="assets/img/char/{slug}.webp" alt="{kr}" loading="lazy"></div>
      <div class="info">
        <div class="cn">{kr}<span>{en}</span></div>
        <div class="cm">{fac(f)['kr']} · {role} · {age}세</div>
        <div class="cd">{arch}</div>
        <div class="cp">{pn} <span>· {pd}</span></div>
      </div>
    </a>''')
    btns = '<button class="on" data-f="all">ALL 19</button>' + "".join(
        f'<button data-f="{s}">{d["kr"]} {len([c for c in C if c[3]==s])}</button>' for s,d in FACTIONS.items())
    return head("characters.html", f"CHARACTERS — {TITLE}") + f'''<section><div class="wrap">
{sec("CHARACTERS","이름이 붙은 사람은 열아홉","세력마다 랭커가 한 명씩 배치돼 있고, 그 다섯은 전원 6단계 이상의 파트너를 데리고 다닌다. 카드를 누르면 외형과 말투, 파트너 정보까지 정리된 상세 페이지로 넘어간다.")}
  <div class="filters rv">{btns}</div>
  <div class="grid" id="grid">{"".join(cards)}
  </div>
</div></section>
''' + foot()

# ─────────────────────────────────────────── char/<slug>.html
def build_char(i):
    slug,kr,en,f,role,age,rk,mbti,arch,p,sk,notes = C[i]
    d = DETAIL[slug]; F = fac(f)
    prev = C[(i-1) % len(C)]; nxt = C[(i+1) % len(C)]
    body_p = "".join(f"<p>{x}</p>" for x in d["bio"])
    skills = "".join(f'<li><b>{x.split(" · ")[0]}</b><span>{x.split(" · ")[1]}</span></li>' for x in sk)

    if p:
        cr = CRMAP[slug]
        partner = f'''
  <div class="pt rv">
    <a class="pt-ph" href="../creatures.html#{cr[0]}"><img src="../assets/img/creature/{cr[0]}.webp" alt="{cr[1]}" loading="lazy"></a>
    <div class="pt-in">
      <div class="pt-e">PARTNER · {cr[2]}</div>
      <h3>{cr[1]}</h3>
      <div class="pt-tags"><span class="tag">{p[1]}</span><span class="tag">{p[2]}</span><span class="tag">유대 {p[3]}</span></div>
      <p>{cr[6]}</p>
    </div>
  </div>'''
    else:
        partner = '''
  <div class="pt rv sealed">
    <div class="pt-ph"><span class="q">?</span></div>
    <div class="pt-in">
      <div class="pt-e">PARTNER · UNRECORDED</div>
      <h3>???</h3>
      <div class="pt-tags"><span class="tag">???</span><span class="tag">???</span><span class="tag">유대 ???</span></div>
      <p>무엇과 계약했는지 알려진 바가 없다. 심층에서 그를 봤다는 사람은 있지만, 곁에 무엇이 있었는지를 끝까지 말한 사람은 아직 없다.</p>
    </div>
  </div>'''

    return head("characters.html", f"{kr} — {TITLE}", up="../") + f'''<article class="cp-page" style="{cvar(f)}">
<section class="cp-hero">
  <div class="cp-bg"><img src="../assets/img/char/{slug}.webp" alt="{kr}"></div>
  <div class="wrap cp-hero-in">
    <a class="back" href="../characters.html">← CHARACTERS</a>
    <div class="cp-e">{en}</div>
    <h1>{kr}</h1>
    <div class="cp-tags">
      <span class="tag f">{F['kr']}</span><span class="tag">{role}</span>
      <span class="tag">{age}세</span><span class="tag">{mbti}</span>
      {'<span class="tag r">RANKER</span>' if rk else ''}
    </div>
    <p class="cp-arch">{arch}</p>
  </div>
</section>

<section><div class="wrap cp-grid">
  <div class="cp-main">
    <div class="lbl rv">PROFILE</div>
    <div class="prose rv">{body_p}</div>

    <div class="lbl rv" style="margin-top:52px">PARTNER</div>{partner}
  </div>

  <aside class="cp-side">
    <div class="lbl rv">DATA</div>
    <dl class="rows rv">
      <div class="row"><dt>소속</dt><dd>{F['kr']} <span class="d">{F['en']}</span></dd></div>
      <div class="row"><dt>직책</dt><dd>{role}</dd></div>
      <div class="row"><dt>나이</dt><dd>{age}세</dd></div>
      <div class="row"><dt>MBTI</dt><dd>{mbti}</dd></div>
      <div class="row"><dt>파트너</dt><dd>{(p[0] + ' · ' + p[1] + ' · ' + p[2]) if p else '??? · ??? · ???'}</dd></div>
      <div class="row"><dt>유대</dt><dd>{p[3] if p else '???'}</dd></div>
    </dl>

    <div class="lbl rv" style="margin-top:40px">SKILLS</div>
    <ul class="skills rv">{skills}</ul>
    <p class="hint rv">정보창에 올라온 기술만 쓸 수 있다. 전투 중에 새로 만들어 내는 일은 없다.</p>

    <div class="lbl rv" style="margin-top:40px">APPEARANCE</div>
    <p class="side-p rv">{d['look']}</p>

    <div class="lbl rv" style="margin-top:40px">VOICE</div>
    <p class="side-p rv">{d['voice']}</p>
  </aside>
</div></section>

<nav class="pager">
  <div class="wrap">
    <a href="{prev[0]}.html"><span>← PREV</span><b>{prev[1]}</b></a>
    <a class="r" href="{nxt[0]}.html"><span>NEXT →</span><b>{nxt[1]}</b></a>
  </div>
</nav>
</article>
''' + foot(up="../")

# ─────────────────────────────────────────── creatures
def build_creatures():
    lines = [("브루트","BRUTE","완력과 질량, 속도와 이빨과 발톱으로 싸운다. 가장 흔하고 가장 안정적인 계열이다."),
             ("헥스","HEX","화염이나 전격, 환각 같은 초자연 능력을 쓴다. 몸이 아니라 현상으로 싸운다."),
             ("헤이즈","HAZE","독과 소리, 냄새와 은신으로 감각을 교란한다. 타격력은 낮지만 판을 흔드는 데 강하다."),
             ("퓨즈","FUSE","브루트와 헥스를 겸비한 희소 계열이다. 선택지가 많은 대신 제어 난이도가 높다."),
             ("리프트","RIFT","태생부터 희귀한 종으로, 다른 계열에는 없는 특수 능력을 개체별로 하나씩 지닌다. 진화로 도달할 수 있는 영역이 아니라서, 존재가 확인되는 것 자체가 사건이 된다.")]
    l5 = "".join(f'<div><div class="n">{n}</div><div class="e">{e}</div><div class="d">{d}</div></div>' for n,e,d in lines)
    ev = [("0","해츨링","계약 직후의 상태"),("1","플레질링","생존자 대다수가 여기에 머문다"),
          ("2","프라울러","싸울 수 있는 테이머의 영역에 들어선다"),("3","헌터","싸우는 자의 절대다수가 여기서 멈춘다"),
          ("4","브레이커","재능 있는 소수만 뚫는 벽이자 세력 간부급"),("5","드레드","천재라고 불리는 영역"),
          ("6","타이런트","랭커권. 등장 자체가 사건이 된다"),("7","카타스트로프","야생 재해급과 대등한 극소수")]
    steps = "".join(f'<div><div class="n">STAGE {n}</div><div class="t">{t}</div><div class="d">{d}</div></div>' for n,t,d in ev)
    cmap = {c[0]: c for c in C}
    cx = []
    for slug,kr,en,line,stage,tam,desc in CR:
        t = cmap[tam]
        cx.append(f'''
    <div class="cx" id="{slug}">
      <div class="ph"><img src="assets/img/creature/{slug}.webp" alt="{kr}" loading="lazy"></div>
      <div class="info"><div class="n">{kr}</div><div class="e">{en}</div>
        <div class="m">{line} · {stage}</div>
        <p class="cxd">{desc}</p>
        <a class="o" href="char/{tam}.html">{t[1]} · {fac(t[3])['kr']} →</a></div>
    </div>''')
    cx.append('''
    <div class="cx sealed">
      <div class="ph"><span class="q">?</span></div>
      <div class="info"><div class="n">???</div><div class="e">UNRECORDED</div>
        <div class="m">??? · ???</div>
        <p class="cxd">기록이 남아 있지 않다. 목격담은 돌지만 형태를 제대로 말한 사람은 아직 없다.</p>
        <a class="o" href="char/mujin.html">무진 · 부랑자 →</a></div>
    </div>''')

    return head("creatures.html", f"CREATURES — {TITLE}") + f'''<section><div class="wrap">
{sec("CLASS","다섯 계열로 나뉜다","태생으로 결정되며 이후 바뀌지 않는다. 같은 단계라도 계열이 다르면 싸우는 방식이 완전히 달라진다.")}
  <div class="line5 rv">{l5}</div>
</div></section>

<section><div class="wrap">
{sec("EVOLUTION","진화는 여덟 단계","유대와 실전 경험이 촉매가 되고, 계기는 대개 생사의 순간에 찾아온다. 의도적으로 유도할 수는 없다.")}
  <div class="steps s8 rv">{steps}</div>
</div></section>

<section><div class="wrap">
{sec("BOND","유대는 네 단계","진화 단계와는 별개로 움직인다. 유대가 낮으면 지시가 늦게 전달되고, 최악의 경우 파트너에게 역습당하는 쪽은 테이머다.")}
  <div class="steps rv">
    <div><div class="n">01</div><div class="t">임시계약</div><div class="d">지시의 절반쯤은 무시된다</div></div>
    <div><div class="n">02</div><div class="t">신뢰</div><div class="d">한 박자 늦게 따라온다</div></div>
    <div><div class="n">03</div><div class="t">공명</div><div class="d">말보다 의도를 먼저 읽기 시작한다</div></div>
    <div><div class="n">04</div><div class="t">완전결속</div><div class="d">지시가 없어도 호흡이 맞는다</div></div>
  </div>
</div></section>

<section><div class="wrap">
{sec("CODEX","확인된 파트너 열여덟","열아홉 번째 칸은 아직 비어 있다.")}
  <div class="codex rv">{"".join(cx)}
  </div>
</div></section>
''' + foot()

# ─────────────────────────────────────────── play
def build_play():
    panel = """[⌛12] 9일째 | 잔해지 · 폐병원 지하 | 밤 | 부랑자
[파트너] 라이카 · 브루트 · 3단계 헌터 · 신뢰 · 왼앞다리 부상
[기술]
└목덜미 물기(급소 고정)·숙련
└흙먼지 차기(시야 차단)·미숙
[인물]
└[알마 : 부랑자 : 💰🤝 : 탄약 떨어짐, 초조함]
[약속]
└[알마 : D-3 : 코어 두 개로 호위 비용 지불]
[관계]
└알마 💰🤝, 이설린 👁🙇
[상황] 지하 통로에서 야생 헤이즈 무리와 조우, 후퇴 중"""
    emo = [("🗡","적대"),("👁","경계"),("🧊","무관심"),("💰","거래"),("🎣","이용"),("🤝","동행"),
           ("🛡","신뢰"),("⛓","빚짐"),("😨","두려움"),("🙇","존경"),("⚔","경쟁"),("💗","호감")]
    erows = "".join(f'<td><div class="em">{e}</div><div class="en2">{n}</div></td>'
                    + ("</tr><tr>" if (i+1)%6==0 and i<11 else "") for i,(e,n) in enumerate(emo))

    return head("play.html", f"PLAY — {TITLE}") + f'''<section><div class="wrap">
{sec("MODE","어느 쪽에서 시작할지 고른다","고른 소속에 따라 첫 장면과 초기 관계가 달라진다. 한번 정하면 AI가 임의로 바꾸지 않는다.")}
  <table class="tbl rv">
    <tr><th>모드</th><th>소속</th><th>시작 조건</th><th>자유도</th></tr>
    <tr><td><b>신디케이트</b></td><td>여명 · 라그나로크 · 라이징 중 택 1</td><td class="d">조직 안의 입지와 임무를 갖고 시작한다</td><td class="d">중</td></tr>
    <tr><td><b>호크</b></td><td>호크</td><td class="d">나머지 전체와 적대하며 약탈과 습격 중심으로 굴러간다</td><td class="d">중</td></tr>
    <tr><td><b>부랑자</b></td><td>무소속</td><td class="d">모든 세력과 중립~경계에서 출발하고, 이후 어디든 가입할 수 있다</td><td class="d">최상</td></tr>
  </table>
</div></section>

<section><div class="wrap">
{sec("STATUS PANEL","매 응답 아래에 상황판이 붙는다","날짜와 위치, 파트너 상태, 약속 기한이 전부 여기서 굴러간다. 실제로 출력되는 형태는 이렇다.")}
  <pre class="panel rv">{panel}</pre>
  <div class="stack rv" style="margin-top:26px">
    <div><div class="k">기술란</div><div class="v">훈련 장면을 거친 기술만 올라간다. 진화했다고 해서 자동으로 늘어나지는 않는다.</div></div>
    <div><div class="k">약속란</div><div class="v">구두 약속이나 거래가 성립하면 등재된다. 기한이 있으면 하루씩 줄어들고, 이행하거나 파기하면 사라진다.</div></div>
    <div><div class="k">관계란</div><div class="v">한 번이라도 만난 인물은 전부 누적된다. 1인당 이모지는 두 개고, 앞에 오는 쪽이 주된 감정이다.</div></div>
  </div>
</div></section>

<section><div class="wrap">
{sec("RELATION","관계는 열두 가지로 표시된다","두 개를 조합해 쓴다. 사건이 쌓여야 움직이며, 급상승하는 일은 없다. 반대로 악화는 즉시 반영된다.")}
  <table class="tbl emo rv"><tr>{erows}</tr></table>
</div></section>

<section><div class="wrap">
{sec("NOTES","플레이 전에 알아 두면 좋은 것","이 봇이 다른 봇과 다르게 굴러가는 지점만 모았다.")}
  <div class="stack rv">
    <div><div class="k">기술</div><div class="v">기술은 테이머와 파트너가 함께 약속해 만든 동작이다. 합의된 신호와 반복 훈련 장면을 거쳐야 성립하고, 숙련도는 미숙에서 익숙, 숙련, 체화 순으로 올라간다. 전투 중에 즉흥적으로 만들어 쓰는 일은 없다.</div></div>
    <div><div class="k">판정</div><div class="v">당신의 행동은 전부 시도로 처리된다. 결과는 성공, 대가 있는 성공, 실패 중 하나로 갈린다. 기본 난이도가 높은 편이고 랭커를 상대할 때는 최상까지 올라가지만, 실패가 막다른 길이 되는 일은 없다.</div></div>
    <div><div class="k">랭커</div><div class="v">무저갱 전역에서 통용되는 다섯 명이고 공식 서열은 없다. 정면충돌은 현실적인 선택지가 아니어서, 대개는 회피하거나 협상하거나 이용하는 쪽으로 풀린다.</div></div>
    <div><div class="k">파트너를 잃으면</div><div class="v">테이머는 일정 기간 전투 불능에 빠진다. 반대로 테이머가 죽으면 파트너는 고아 개체가 되어 폭주하고, 그 처리를 두고 세력이 충돌한다.</div></div>
    <div><div class="k">주인공</div><div class="v">세계는 당신을 중심으로 돌지 않는다. 개입하지 않아도 인물들끼리 거래하고 다투며 상황이 진행된다. 그리고 당신의 행동과 대사는 당신이 정한다. AI가 대신 쓰지 않는다.</div></div>
  </div>
  <div class="btns rv" style="margin-top:36px"><a class="btn pri" href="{CRACK}">크랙에서 플레이</a></div>
</div></section>
''' + foot()

JS = '''document.querySelector('.navtoggle')?.addEventListener('click',function(){
  document.querySelector('.nav ul').classList.toggle('open');
});
var io=new IntersectionObserver(function(es){es.forEach(function(e){
  if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target);}});},{threshold:.05});
document.querySelectorAll('.rv').forEach(function(el){io.observe(el);});
document.querySelectorAll('.filters button').forEach(function(b){
  b.addEventListener('click',function(){
    document.querySelectorAll('.filters button').forEach(function(x){x.classList.remove('on');});
    b.classList.add('on');
    var f=b.dataset.f;
    document.querySelectorAll('#grid .card').forEach(function(c){
      c.hidden = !(f==='all'||c.dataset.f===f);
    });
  });
});
'''

if __name__ == "__main__":
    os.makedirs(os.path.join(OUT,"assets","js"), exist_ok=True)
    os.makedirs(os.path.join(OUT,"char"), exist_ok=True)
    files = {"world.html":build_world(),"factions.html":build_factions(),
             "characters.html":build_characters(),"creatures.html":build_creatures(),"play.html":build_play(),
             os.path.join("assets","js","main.js"):JS}
    for i in range(len(C)):
        files[os.path.join("char", C[i][0]+".html")] = build_char(i)
    for name, txt in files.items():
        with open(os.path.join(OUT,name),"w",encoding="utf-8") as fh: fh.write(txt)
    print("%d files" % len(files))
