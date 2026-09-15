# -*- coding: utf-8 -*-
import re, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from data import FACTIONS, C, CR, CRX
from detail import DETAIL

F = FACTIONS
def fc(s): return F[s]["color"]
CRBY = {c[5]: c for c in CR}

# ── 인물 상세 JSON ──
DAT = {}
for slug,kr,en,f,role,age,rk,mbti,arch,p,sk,notes in C:
    d = DETAIL[slug]; cr = CRBY.get(slug)
    DAT[slug] = dict(n=kr,e=en,f=F[f]["kr"],fe=F[f]["en"],fc=fc(f),r=role,a=age,rk=rk,
        mb=mbti,ar=arch,sk=sk,no=d["bio"],kf=notes,look=d["look"],voice=d["voice"],
        p=(" · ".join(p) if p else "??? · ??? · ??? · ???"),
        cx=(CRX.get(cr[0],"") if cr else ""),
        cn=(cr[1] if cr else "???"), cs=(cr[0] if cr else ""), cd=(cr[6] if cr else
            "무엇과 계약했는지 알려진 바가 없다. 심층에서 그를 봤다는 사람은 있지만, 곁에 무엇이 있었는지를 끝까지 말한 사람은 아직 없다."))

# ── P0 OVERVIEW ──
P0 = '''<div class="phead"><span class="pn">00</span><span class="pt">OVERVIEW</span><span class="px">SHEET 1 / 1</span></div>
<div class="split">
  <div>
    <p class="note">30년 전 열린 균열은 아직 닫히지 않았다. 국가도 행정도 남지 않은 이 땅에서,
      살아남은 사람들은 균열 너머에서 건너온 짐승과 계약해 하루를 번다.
      이 단말기에 남은 것은 그 이후를 정리한 기록이다.</p>
    <dl class="fld" style="margin-top:20px">
      <div><dt>SUBJECT</dt><span class="dots"></span><dd>균열 · 크리처 · 테이머</dd></div>
      <div><dt>ELAPSED</dt><span class="dots"></span><dd>붕괴 후 30년</dd></div>
      <div><dt>SECTORS</dt><span class="dots"></span><dd>심층 · 잔해지 · 거점지대</dd></div>
      <div><dt>RECORDS</dt><span class="dots"></span><dd>세력 5 · 인물 19 · 파트너 18 + 1</dd></div>
      <div><dt>ORIGIN</dt><span class="dots"></span><dd>무저갱 / ABYSS</dd></div>
    </dl>
    <div class="kv3">
      <div><b>RIFT</b><span>30년 전 동시에 열렸고 지금도 간헐적으로 열린다. 여는 조건도 닫는 방법도 밝혀진 바가 없다.</span></div>
      <div><b>PARTNER</b><span>한 사람당 한 체. 선택이 아니라 생존 조건이며 둘 이상은 불가능하다.</span></div>
      <div><b>FACTION</b><span>네 조직과 부랑자. 불가침 협정은 문서로 남은 적이 없다.</span></div>
    </div>
  </div>
  <figure class="plate2">
    <img src="assets/img/bg/hero.webp" alt="">
    <span class="stamp2">RESTRICTED</span>
    <figcaption>PLATE 01 · 잔해지 남부 — 6단계 개체 접촉 기록 / 촬영자 미상</figcaption>
  </figure>
</div>'''

# ── P1 WORLD ──
TERR=[("deep","심층과 구 도심. 균열이 가장 촘촘하게 몰려 있고 재해급 개체가 서식한다. 들어가는 사람은 있어도 돌아 나오는 사람은 드물다."),
      ("ruins","심층과 거점지대 사이에 깔린 폐허 벨트. 누구의 관할도 아니라서 거래와 약탈이 같은 자리에서 벌어진다."),
      ("strongholds","외곽에 자리 잡은 네 조직의 요새. 배급과 치안이 돌아가는 유일한 구역이지만 그 규칙은 담장 안에서만 작동한다.")]
terr="".join(f'<figure class="loc"><img src="assets/img/loc/{i}.webp" alt="" loading="lazy"><figcaption>{d}</figcaption></figure>' for i,d in TERR)
SPOT=[("first_rift","30년 전 가장 먼저 열린 균열. 주변 수백 미터가 유리처럼 굳어 있고 그 표면은 30년 동안 한 번도 갈라진 적이 없다."),
      ("station07","라이징이 세운 무인 관측소. 계측기만 돌아가고 사람은 없다. 최근 회수한 기록지에 손으로 고쳐 쓴 수치가 남아 있었는데 라이징 필체가 아니었다."),
      ("pit","도살장 지하에서 열리는 도박장. 파트너끼리 붙이고 코어를 건다. 진 쪽의 파트너는 대개 살아서 나오지 못한다."),
      ("unmarked","테이머와 파트너를 같은 자리에 묻는 공동 묘지. 이름을 새기지 않는 것이 규칙이고, 언제부터 그랬는지는 남아 있지 않다.")]
spot="".join(f'<figure class="loc"><img src="assets/img/loc/{i}.webp" alt="" loading="lazy"><figcaption>{d}</figcaption></figure>' for i,d in SPOT)
RULES=[("화폐","돈은 붕괴와 함께 종잇장이 됐다. 지금 통용되는 것은 <b>크리처 사체에서 나오는 코어와 파편</b>이며, 화폐인 동시에 파트너를 강화하는 자원이다."),
 ("계약","도구도 매개물도 필요 없다. 손을 대고 서로 받아들이면 성립한다. 다만 <b>한 사람이 맺을 수 있는 계약은 하나뿐</b>이고, 잃은 뒤에야 다시 가능해진다."),
 ("전투","싸우는 쪽은 파트너다. 테이머가 맡는 것은 <b>지시와 판단, 엄호</b>. 사람이 직접 무기를 들고 맞붙는 장면은 극히 드물다."),
 ("육체","파트너가 강해질수록 테이머의 몸도 그 성질을 닮아 간다. 튼튼해지는 수준이지 <b>초인이 되지는 않는다</b>."),
 ("불가침","안전지대 안에서는 싸우지 않는다는 암묵적 협정이 있다. 문서로 남은 적이 없어 언제든 깨질 수 있다.")]
rules="".join(f'<div><div class="k">{k}</div><div class="v">{v}</div></div>' for k,v in RULES)
P1 = f'''<div class="phead"><span class="pn">01</span><span class="pt">WORLD</span><span class="px">무저갱 / ABYSS</span></div>
<div class="grp"><span class="gn">TIMELINE</span><span class="gc">연표</span></div>
<div class="steps s3">
  <div><div class="n">-30</div><div class="t">붕괴</div><div class="d">각지에 균열이 열리며 크리처가 대량으로 넘어왔다. 국가와 행정은 몇 달을 버티지 못했다.</div></div>
  <div><div class="n">-30 → 0</div><div class="t">재건 실패</div><div class="d">여러 차례 시도가 있었지만 전부 무산됐다. 구 세계의 지식도 이때 대부분 소실됐다.</div></div>
  <div><div class="n">NOW</div><div class="t">현재</div><div class="d">균열은 지금도 간헐적으로 열린다. 닫는 방법은 여전히 알려지지 않았다.</div></div>
</div>
<div class="grp"><span class="gn">TERRAIN</span><span class="gc">지형 3</span></div>
<div class="locs">{terr}</div>
<div class="grp"><span class="gn">RULES</span><span class="gc">이 세계가 굴러가는 방식</span></div>
<div class="stack2">{rules}</div>
<div class="grp"><span class="gn">RIFT</span><span class="gc">균열</span></div>
<div class="stack2">
  <div><div class="k">확인된 것</div><div class="v">30년 전 각지에서 동시에 열렸고, 지금도 간헐적으로 열린다. 새로운 개체는 예외 없이 이쪽을 통해 들어온다.</div></div>
  <div><div class="k">확인되지 않은 것</div><div class="v">여는 조건, 닫는 방법, 저편에 무엇이 있는지. 세 가지 모두 30년째 그대로다.</div></div>
</div>
<div class="grp"><span class="gn">LOCATIONS</span><span class="gc">특정 장소 4</span></div>
<div class="locs">{spot}</div>
<p class="rum">심층 안쪽까지 혼자 들어갔다 나오는 노인이 하나 있다는 이야기가 잔해지에 돈다. 그가 무엇을 봤다고 말하든 증명할 방법이 없어 아무도 믿지 않는다.</p>'''

# ── P2 FACTIONS ──
fx=""
for i,(s,d) in enumerate(F.items()):
    mem=[c for c in C if c[3]==s]
    chips="".join(f'<button class="chip" data-go="{c[0]}">{c[1]}<i>{c[4]}</i></button>' for c in mem)
    slog = f'"{d["slogan"]}"' if d["slogan"] else "내건 슬로건도 깃발도 없다"
    rum  = f'<p class="rum sm">{d["rumor"]}</p>' if d["rumor"] else ""
    BAN={"dawn":"twilight_spire","ragnarok":"sanctum","rising":"nest","hawk":"yard","vagabond":"exchange"}
    fx += f'''<div class="fcard" style="--fc:{fc(s)}">
  <img class="fban" src="assets/img/loc/{BAN[s]}.webp" alt="" loading="lazy">
  <img class="fsym" src="assets/img/symbol/{s}.png" alt="" loading="lazy">
  <div class="fno2">F-0{i+1}</div>
  <h4>{d['kr']}</h4><div class="fen">{d['en']}</div>
  <p class="fslog">{slog}</p>
  <p class="fbody">{d['body']}</p>
  <dl class="fld sm">
    <div><dt>거점</dt><span class="dots"></span><dd>{d['base']}</dd></div>
    <div><dt>편제</dt><span class="dots"></span><dd>{d['org']}</dd></div>
    <div><dt>규모</dt><span class="dots"></span><dd>{d['scale']}</dd></div>
  </dl>
  <div class="chips">{chips}</div>{rum}
</div>'''
P2 = f'''<div class="phead"><span class="pn">02</span><span class="pt">FACTIONS</span><span class="px">05 ENTRIES</span></div>
<p class="note" style="margin-bottom:18px">네 조직이 무저갱을 나눠 가졌다. 앞의 셋은 서로를 견제하며 불가침에 가까운 균형을 유지하고 있고, 호크는 나머지 전부의 공공의 적이다. 부랑자는 그 사이를 오가는 변수다.</p>
<div class="fgrid">{fx}</div>'''

# ── P3 CHARACTERS (세력별) ──
ch=""
for s_,d in F.items():
    mem=[c for c in C if c[3]==s_]
    hero=[c for c in mem if c[6]]
    rest=[c for c in mem if not c[6]]
    fkey = fc(s_).replace("var(--f-","").replace(")","")
    blk=""
    for slug,kr,en,f,role,age,rk,mbti,arch,p,sk,notes in hero:
        pn = (" · ".join(p) if p else "??? · ??? · ??? · ???")
        bio = DETAIL[slug]["bio"][0]
        li = "".join('<li>%s</li>' % x for x in notes[1:3])
        blk += f'''<button class="cc hero" data-go="{slug}" style="--fc:{fc(f)}">
  <div class="ph"><img src="assets/img/char/{slug}.webp" alt="{kr}"><span class="rk">RANKER</span></div>
  <div class="bd"><div class="nm">{kr}<i>{en}</i></div><div class="mt">{role} · {age}세 · {mbti}</div>
    <div class="ar">{arch}</div>
    <p class="ds">{bio}</p>
    <ul class="dsl">{li}</ul>
    <div class="pt2">{pn}</div></div></button>'''
    cards=""
    for slug,kr,en,f,role,age,rk,mbti,arch,p,sk,notes in rest:
        pn = (p[0]+" · "+p[2]) if p else "??? · ???"
        cards += f'''<button class="cc" data-go="{slug}" style="--fc:{fc(f)}">
  <div class="ph"><img src="assets/img/char/{slug}.webp" alt="{kr}" loading="lazy"></div>
  <div class="bd"><div class="nm">{kr}<i>{en}</i></div><div class="mt">{role} · {age}세 · {mbti}</div>
    <div class="ar">{arch}</div>
    <p class="ds">{notes[0]}</p>
    <div class="pt2">{pn}</div></div></button>'''
    ch += f'''<div class="fgrp" data-f="{fkey}">
<div class="grp" style="--fc:{fc(s_)}"><span class="gn">{d['kr']}</span><span class="gc">{d['en']} · {len(mem)}</span></div>
{blk}
<div class="cards">{cards}</div>
</div>'''

P3 = f'''<div class="phead"><span class="pn">03</span><span class="pt">CHARACTERS</span><span class="px">19 ENTRIES</span></div>
<p class="note" style="margin-bottom:6px">세력마다 랭커가 한 명씩 있고, 그 다섯은 전원 6단계 이상의 파트너를 데리고 다닌다. 카드를 누르면 개별 기록이 열린다.</p>
{ch}'''

# ── P4 CREATURES (계열별) ──
LINE=[("브루트","BRUTE","완력과 질량, 이빨과 발톱으로 싸운다. 가장 흔하고 가장 안정적이다."),
      ("헥스","HEX","화염이나 전격, 환각 같은 초자연 능력을 쓴다. 몸이 아니라 현상으로 싸운다."),
      ("헤이즈","HAZE","독과 소리, 냄새와 은신으로 감각을 교란한다. 타격력은 낮고 판을 흔드는 데 강하다."),
      ("퓨즈","FUSE","브루트와 헥스를 겸비한 희소 계열. 선택지가 많은 대신 제어가 어렵다."),
      ("리프트","RIFT","태생부터 희귀한 종. 다른 계열에 없는 능력을 개체별로 하나씩 지니며 진화로 도달할 수 없다.")]
cmap={c[0]:c for c in C}
cx=""
for kr,en,desc in LINE:
    grp=[c for c in CR if c[3]==kr]
    cards=""
    for slug,n,e,ln,stage,tam,dsc in grp:
        t=cmap[tam]
        cards+=f'''<button class="cc cr" data-go="{tam}" style="--fc:{fc(t[3])}">
  <div class="ph"><img src="assets/img/creature/{slug}.webp" alt="{n}" loading="lazy"></div>
  <div class="bd"><div class="nm">{n}<i>{e}</i></div><div class="mt">{stage}</div>
    <div class="ar">{dsc}</div><p class="ds">{CRX.get(slug,"")}</p>
    <div class="pt2">{t[1]} · {F[t[3]]['kr']}</div></div></button>'''
    if kr=="리프트":
        cards+='''<div class="cc cr sealed"><div class="ph"><span class="q">?</span></div>
  <div class="bd"><div class="nm">???<i>UNRECORDED</i></div><div class="mt">??? 단계</div>
    <div class="ar">기록이 남아 있지 않다. 목격담은 돌지만 형태를 제대로 말한 사람은 아직 없다.</div>
    <div class="pt2">무진 · 부랑자</div></div></div>'''
    cx+=f'''<div class="grp"><span class="gn">{kr}</span><span class="gc">{en} · {len(grp)+(1 if kr=="리프트" else 0)}</span></div>
<p class="gdesc">{desc}</p><div class="cards">{cards}</div>'''
EV=[("0","해츨링","계약 직후"),("1","플레질링","생존자 대다수"),("2","프라울러","싸울 수 있는 영역"),
    ("3","헌터","절대다수가 여기서 멈춤"),("4","브레이커","세력 간부급"),("5","드레드","천재 영역"),
    ("6","타이런트","랭커권"),("7","카타스트로프","야생 재해급과 대등")]
ev="".join(f'<div><div class="n">{n}</div><div class="t">{t}</div><div class="d">{d}</div></div>' for n,t,d in EV)
P4 = f'''<div class="phead"><span class="pn">04</span><span class="pt">CREATURES</span><span class="px">18 + 1</span></div>
<div class="grp"><span class="gn">EVOLUTION</span><span class="gc">진화 8단계</span></div>
<div class="steps s8">{ev}</div>
<div class="grp"><span class="gn">BOND</span><span class="gc">유대 4단계</span></div>
<div class="steps s4">
  <div><div class="n">01</div><div class="t">임시계약</div><div class="d">지시의 절반쯤은 무시된다</div></div>
  <div><div class="n">02</div><div class="t">신뢰</div><div class="d">한 박자 늦게 따라온다</div></div>
  <div><div class="n">03</div><div class="t">공명</div><div class="d">말보다 의도를 먼저 읽는다</div></div>
  <div><div class="n">04</div><div class="t">완전결속</div><div class="d">지시 없이도 호흡이 맞는다</div></div>
</div>
{cx}'''

# ── P5 PLAY ──
PANEL = """[⌛12] 9일째 | 잔해지 · 폐병원 지하 | 밤 | 부랑자
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
EMO=[("🗡","적대"),("👁","경계"),("🧊","무관심"),("💰","거래"),("🎣","이용"),("🤝","동행"),
     ("🛡","신뢰"),("⛓","빚짐"),("😨","두려움"),("🙇","존경"),("⚔","경쟁"),("💗","호감")]
emo="".join(f'<div class="em"><span>{e}</span><i>{n}</i></div>' for e,n in EMO)
NOTES=[("기술","테이머와 파트너가 함께 약속해 만든 동작이다. 합의된 신호와 반복 훈련을 거쳐야 성립하고, 숙련도는 미숙 → 익숙 → 숙련 → 체화 순으로 오른다. 전투 중에 즉흥으로 만들어 쓰는 일은 없다."),
 ("판정","당신의 행동은 전부 시도로 처리된다. 결과는 성공, 대가 있는 성공, 실패 중 하나다. 기본 난이도가 높고 랭커를 상대할 때는 최상이지만, 실패가 막다른 길이 되지는 않는다."),
 ("랭커","무저갱 전역에서 통용되는 다섯 명이고 공식 서열은 없다. 정면충돌은 현실적인 선택지가 아니라 회피·협상·이용 쪽으로 풀린다."),
 ("파트너를 잃으면","테이머는 일정 기간 전투 불능에 빠진다. 반대로 테이머가 죽으면 파트너는 고아 개체가 되어 폭주하고, 그 처리를 두고 세력이 충돌한다."),
 ("주인공","세계는 당신을 중심으로 돌지 않는다. 개입하지 않아도 인물들끼리 거래하고 다툰다. 그리고 <b>당신의 행동과 대사는 당신이 정한다</b>.")]
notes="".join(f'<div><div class="k">{k}</div><div class="v">{v}</div></div>' for k,v in NOTES)
P5 = f'''<div class="phead"><span class="pn">05</span><span class="pt">PLAY</span><span class="px">GUIDE</span></div>
<div class="grp"><span class="gn">MODE</span><span class="gc">시작 모드 3</span></div>
<div class="stack2">
  <div><div class="k">SYNDICATE · 신디케이트</div><div class="v"><b>여명 · 라그나로크 · 라이징 중 하나를 골라 소속으로 시작한다.</b><br>조직 안의 입지와 임무를 처음부터 갖고 출발하며, 명령은 대체로 위에서 내려온다.</div></div>
  <div><div class="k">HAWK · 호크</div><div class="v"><b>호크 소속으로 시작하고 나머지 전체와 적대한다.</b><br>약탈과 습격이 일상이 되는 대신, 등 뒤를 가장 조심해야 하는 곳은 조직 안쪽이다.</div></div>
  <div><div class="k">VAGABOND · 부랑자</div><div class="v"><b>무소속. 모든 세력과 중립에서 경계 사이에 놓인다.</b><br>자유도가 가장 높고, 원한다면 나중에 어느 쪽으로든 들어갈 수 있다.</div></div>
</div>
<div class="grp"><span class="gn">STATUS PANEL</span><span class="gc">정보창</span></div>
<p class="gdesc">매 응답 최하단에 붙는다. 날짜와 위치, 파트너 상태, 약속 기한이 전부 여기서 굴러간다.</p>
<pre class="panel2">{PANEL}</pre>
<div class="grp"><span class="gn">RELATION</span><span class="gc">관계 이모지 12</span></div>
<p class="gdesc">두 개를 조합해 쓰고 앞에 오는 쪽이 주된 감정이다. 사건이 쌓여야 움직이며 급상승은 없다. 악화는 즉시 반영된다.</p>
<div class="emo">{emo}</div>
<div class="grp"><span class="gn">NOTES</span><span class="gc">알아 둘 것</span></div>
<div class="stack2">{notes}</div>'''

PANES = {"p0":P0,"p1":P1,"p2":P2,"p3":P3,"p4":P4,"p5":P5}

src = open('home.html',encoding='utf-8').read()
for pid,html in PANES.items():
    pat = re.compile(r'(<section class="pane" id="%s"[^>]*>).*?(</section>)' % pid, re.S)
    src = pat.sub(lambda m: m.group(1)+"\n"+html+"\n          "+m.group(2), src)

# 상세 데이터 주입 (멱등)
blob = "<script>window.DAT=%s;</script>" % json.dumps(DAT, ensure_ascii=False)
if "window.DAT=" in src:
    src = re.sub(r'<script>window\.DAT=.*?</script>', lambda m: blob, src, count=1, flags=re.S)
else:
    src = src.replace("<script>\n(function(){\n  var evi=", blob+"\n<script>\n(function(){\n  var evi=")
open('home.html','w',encoding='utf-8').write(src)
print("panes injected", {k:len(v) for k,v in PANES.items()})
