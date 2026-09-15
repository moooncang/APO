/* TAMER IN APOCALYPSE — 효과음 엔진
   외부 음원 없이 Web Audio로 합성. 모달 임팩트 + 필터 스윕 + 서브 + 새추레이션 + 컨볼루션 리버브. */
(function(g){
'use strict';

var AC=null, RIG=null, MUTE=false, GN=1;
try{ MUTE = localStorage.getItem('tia_mute')==='1'; }catch(e){}

function ctx(){
  if(MUTE) return null;
  if(!AC){ try{ AC=new (g.AudioContext||g.webkitAudioContext)(); }catch(e){ return null; } }
  if(!AC) return null;
  if(AC.state==='suspended'){ try{ AC.resume(); }catch(e){} }
  return AC;
}

/* ── 노이즈 버퍼 (핑크 기울기) ── */
var NB=null;
function nbuf(c){
  if(NB && NB.sampleRate===c.sampleRate) return NB;
  var n=Math.floor(c.sampleRate*2.2), b=c.createBuffer(2,n,c.sampleRate);
  for(var ch=0;ch<2;ch++){
    var d=b.getChannelData(ch), b0=0,b1=0,b2=0;
    for(var i=0;i<n;i++){
      var w=Math.random()*2-1;
      b0=.99765*b0+w*.0990460; b1=.96300*b1+w*.2965164; b2=.57000*b2+w*1.0526913;
      d[i]=(b0+b1+b2+w*.1848)*.28;
    }
  }
  NB=b; return b;
}
function nsrc(c){ var s=c.createBufferSource(); s.buffer=nbuf(c); s.loop=true;
  s.playbackRate.value=.85+Math.random()*.3; return s; }

/* ── 임펄스 응답 ── */
function mkIR(c,sec,decay,bright,er){
  var n=Math.max(64,Math.floor(c.sampleRate*sec)), b=c.createBuffer(2,n,c.sampleRate);
  for(var ch=0;ch<2;ch++){
    var d=b.getChannelData(ch), lp=0;
    for(var i=0;i<n;i++){
      var u=i/n, e=Math.pow(1-u,decay);
      var x=(Math.random()*2-1)*e;
      lp += (x-lp)*(bright*(1-u*.72)+.015);
      d[i]=lp*1.6;
    }
    if(er) for(var k=0;k<5;k++){
      var p=Math.floor([.0063,.0117,.0191,.0283,.0397][k]*c.sampleRate*(1+ch*.06));
      if(p<n) d[p]+=(.42/(k+1))*(Math.random()>.5?1:-1);
    }
  }
  return b;
}
function shaper(c,amt){
  var ws=c.createWaveShaper(), n=1024, cur=new Float32Array(n), th=Math.tanh(amt);
  for(var i=0;i<n;i++){ var x=i*2/n-1; cur[i]=Math.tanh(x*amt)/th; }
  ws.curve=cur; ws.oversample='2x'; return ws;
}

/* ── 마스터 체인 ── */
function rig(c){
  if(RIG && RIG.c===c) return RIG;
  var comp=c.createDynamicsCompressor();
  comp.threshold.value=-15; comp.knee.value=16; comp.ratio.value=5.5;
  comp.attack.value=.0025; comp.release.value=.16;
  var sat=shaper(c,1.7), out=c.createGain();
  out.gain.value=.9;
  sat.connect(comp); comp.connect(out); out.connect(c.destination);

  var hall=c.createConvolver(); hall.buffer=mkIR(c,1.05,3.8,.24,true);
  var room=c.createConvolver(); room.buffer=mkIR(c,.34,2.2,.55,true);
  var pre=c.createDelay(.2); pre.delayTime.value=.021;
  var hg=c.createGain(); hg.gain.value=.19;
  var rg=c.createGain(); rg.gain.value=.17;
  var damp=c.createBiquadFilter(); damp.type='lowpass'; damp.frequency.value=3600;
  pre.connect(hall); hall.connect(damp); damp.connect(hg); hg.connect(sat);
  room.connect(rg); rg.connect(sat);

  var bus=c.createGain(); bus.gain.value=1;
  bus.connect(sat); bus.connect(pre); bus.connect(room);
  RIG={c:c,bus:bus,hg:hg,rg:rg};
  return RIG;
}
function BUS(c){ return rig(c).bus; }
function pan(c,v){ var p; try{ p=c.createStereoPanner(); p.pan.value=Math.max(-1,Math.min(1,v||0)); }
  catch(e){ p=c.createGain(); } return p; }
function env(gn,t,a,d,pk,hold){
  a=Math.max(.0012,Math.min(a,d*.6)); hold=hold||0;
  var rel=Math.max(.02,d-a), p=Math.max(.0003,pk*GN);
  gn.gain.setValueAtTime(.00008,t);
  gn.gain.exponentialRampToValueAtTime(p,t+a);
  if(hold) gn.gain.setValueAtTime(p,t+a+hold);
  gn.gain.exponentialRampToValueAtTime(.00008,t+a+hold+rel);
  return a+hold+rel;
}

/* ── 보이스 ── */
/* 필터 스윕 노이즈 */
function NS(c,t,o){
  var s=nsrc(c), f=c.createBiquadFilter(), gn=c.createGain(), p=pan(c,o.pan);
  f.type=o.type||'bandpass'; f.Q.value=o.q||1.1;
  f.frequency.setValueAtTime(Math.max(28,o.f0),t);
  if(o.fm) f.frequency.exponentialRampToValueAtTime(Math.max(28,o.fm),t+o.dur*.35);
  f.frequency.exponentialRampToValueAtTime(Math.max(28,o.f1||o.f0),t+o.dur);
  s.connect(f); f.connect(gn); gn.connect(p); p.connect(BUS(c));
  var L=env(gn,t,o.a||.008,o.dur,o.g||.3,o.h);
  s.start(t); s.stop(t+L+.05);
}
/* 디튠 스택 톤 */
function TN(c,t,o){
  var n=o.det||1, p=pan(c,o.pan), gn=c.createGain();
  gn.connect(p); p.connect(BUS(c));
  for(var i=0;i<n;i++){
    var s=c.createOscillator(), sg=c.createGain();
    s.type=o.type||'sine';
    var dt=(n>1)?(i-(n-1)/2)*(o.spread||7):0;
    s.detune.value=dt;
    s.frequency.setValueAtTime(Math.max(16,o.f0),t);
    s.frequency.exponentialRampToValueAtTime(Math.max(16,o.f1||o.f0),t+o.dur);
    sg.gain.value=1/n; s.connect(sg); sg.connect(gn);
    s.start(t); s.stop(t+o.dur+.4);
  }
  env(gn,t,o.a||.006,o.dur,o.g||.3,o.h);
}
/* 모달 임팩트 — 공명체 타격 */
var MAT={
  metal:[1,2.76,5.40,8.93,13.34], glass:[1,2.32,4.25,6.63,9.38],
  stone:[1,1.61,2.49,3.38,4.52],  drum:[1,1.59,2.14,2.30,2.65],
  bone:[1,2.05,3.22,4.61,6.02],   wood:[1,1.44,2.09,2.88]
};
function MD(c,t,o){
  var rt=MAT[o.mat||'metal'], ex=o.ex||.01, p=pan(c,o.pan);
  p.connect(BUS(c));
  var s=nsrc(c), eg=c.createGain();
  s.connect(eg); env(eg,t,.0015,ex,1);
  s.start(t); s.stop(t+ex+.05);
  for(var i=0;i<rt.length;i++){
    if(o.n && i>=o.n) break;
    var f=c.createBiquadFilter(); f.type='bandpass';
    f.frequency.value=Math.min(c.sampleRate/2.2, o.f*rt[i]*(1+(Math.random()-.5)*.012));
    f.Q.value=o.q||26;
    var gn=c.createGain();
    eg.connect(f); f.connect(gn); gn.connect(p);
    env(gn,t,.0018,(o.dec||.5)/(1+i*(o.damp||.55)),(o.g||.3)*(o.amps?o.amps[i]:1/(1+i*.8)));
  }
}
/* 서브 임팩트 */
function SB(c,t,o){
  var s=c.createOscillator(), gn=c.createGain(), d=shaper(c,o.drive||1.2);
  s.type='sine';
  s.frequency.setValueAtTime(o.f0,t);
  s.frequency.exponentialRampToValueAtTime(Math.max(16,o.f1||o.f0*.3),t+o.dur*.7);
  s.connect(gn); gn.connect(d); d.connect(BUS(c));
  env(gn,t,o.a||.004,o.dur,o.g||.5);
  s.start(t); s.stop(t+o.dur+.1);
}
/* 초단 트랜지언트 */
function CK(c,t,o){
  o=o||{};
  var s=nsrc(c), f=c.createBiquadFilter(), gn=c.createGain(), p=pan(c,o.pan);
  f.type='highpass'; f.frequency.value=o.hp||1800;
  s.connect(f); f.connect(gn); gn.connect(p); p.connect(BUS(c));
  env(gn,t,.0008,o.dur||.016,o.g||.35);
  s.start(t); s.stop(t+.06);
}
/* 하강/상승 공기 */
function AIR(c,t,o){
  NS(c,t,{dur:o.dur,f0:o.f0,f1:o.f1,q:o.q||.6,g:o.g||.22,a:o.a||.05,pan:o.pan,type:'bandpass'});
}

/* ══════ 큐 ══════ */
var CUE={
/* ── 인물 19 ── */
seolrin:function(c,t){                       /* 낙일 — 불티 하강 + 착탄 */
  CK(c,t,{hp:2600,g:.3});
  NS(c,t,{dur:.62,f0:4200,f1:240,q:.85,g:.4,pan:-.15});
  NS(c,t+.04,{dur:.58,f0:3600,f1:300,q:.8,g:.26,pan:.2});
  SB(c,t+.3,{dur:.55,f0:190,f1:38,g:.62,drive:1.9});
  MD(c,t+.3,{f:320,mat:'stone',dec:.5,g:.3,pan:-.1});
  NS(c,t+.31,{dur:.6,f0:1500,f1:180,q:.55,g:.24,type:'lowpass',a:.02});
  TN(c,t+.33,{dur:.8,f0:88,f1:62,type:'triangle',det:3,spread:9,g:.18,a:.06}); },
theodore:function(c,t){                      /* 감화 — 부풀어 오르는 화음 */
  TN(c,t,{dur:1.05,f0:69,f1:138,det:3,spread:6,g:.42,a:.36});
  TN(c,t+.06,{dur:.98,f0:103.8,f1:207,type:'triangle',det:2,spread:9,g:.24,a:.36,pan:-.25});
  TN(c,t+.14,{dur:.86,f0:207,f1:276,det:2,spread:12,g:.11,a:.38,pan:.28});
  AIR(c,t+.1,{dur:.8,f0:500,f1:1700,q:.45,g:.1,a:.34}); },
kyle:function(c,t){                          /* 돌진 — 물살 + 충돌 */
  NS(c,t,{dur:.34,f0:380,f1:2900,q:.75,g:.36,pan:-.45});
  NS(c,t+.05,{dur:.3,f0:520,f1:2400,q:.9,g:.24,pan:.45});
  CK(c,t+.24,{hp:900,g:.42});
  SB(c,t+.24,{dur:.46,f0:110,f1:30,g:.72,drive:2.4});
  MD(c,t+.24,{f:160,mat:'drum',dec:.42,g:.34});
  NS(c,t+.26,{dur:.5,f0:2200,f1:380,q:1.6,g:.16,pan:.15}); },
lucia:function(c,t){                         /* 안개 — 숨죽인 공기 */
  NS(c,t,{dur:1.05,f0:1300,f1:240,q:.4,g:.46,type:'lowpass',a:.34,pan:-.2});
  NS(c,t+.08,{dur:.95,f0:900,f1:320,q:.45,g:.3,type:'lowpass',a:.34,pan:.24});
  TN(c,t+.12,{dur:.85,f0:392,f1:294,det:3,spread:5,g:.07,a:.34});
  AIR(c,t+.2,{dur:.7,f0:3400,f1:1100,q:.55,g:.06,a:.24}); },
isabel:function(c,t){                        /* 개안 — 유리 종 */
  CK(c,t,{hp:5200,g:.2});
  MD(c,t,{f:1318,mat:'glass',dec:1.15,damp:.35,q:36,g:.34,pan:-.1});
  MD(c,t+.015,{f:1976,mat:'glass',dec:.9,damp:.4,q:32,g:.18,pan:.22});
  TN(c,t+.02,{dur:1,f0:659,f1:657,det:2,spread:4,g:.14,a:.03});
  NS(c,t,{dur:.3,f0:5600,f1:7600,q:1.4,g:.12});
  TN(c,t+.28,{dur:.62,f0:987,f1:985,det:2,spread:6,g:.1,a:.06,pan:.15}); },
barhan:function(c,t){                        /* 저주 — 디튠 드론 */
  TN(c,t,{dur:1,f0:55,f1:41,type:'sawtooth',det:3,spread:14,g:.32,a:.18});
  TN(c,t+.02,{dur:.98,f0:82.4,f1:61.7,type:'sawtooth',det:2,spread:20,g:.14,a:.18,pan:-.3});
  TN(c,t+.18,{dur:.66,f0:233,f1:219,type:'square',det:2,spread:16,g:.06,a:.12,pan:.3});
  NS(c,t+.16,{dur:.64,f0:380,f1:105,q:2.8,g:.2,a:.07});
  MD(c,t+.34,{f:92,mat:'bone',dec:.6,g:.16}); },
rhea:function(c,t){                          /* 가시 — 뼈 찌름 4연 */
  for(var i=0;i<4;i++){
    var tt=t+i*.072, pn=(i%2?1:-1)*.35;
    CK(c,tt,{hp:3200,g:.26,pan:pn});
    MD(c,tt,{f:820+i*260,mat:'bone',dec:.3,damp:.7,q:22,g:.3,pan:pn}); }
  SB(c,t+.3,{dur:.5,f0:210,f1:62,g:.42,drive:1.6});
  NS(c,t+.3,{dur:.52,f0:2600,f1:560,q:1.1,g:.13}); },
haito:function(c,t){                         /* 독 — 젖은 저역 */
  NS(c,t,{dur:.9,f0:560,fm:180,f1:88,q:4.2,g:.42,a:.07,pan:-.2});
  TN(c,t+.1,{dur:.75,f0:104,f1:56,type:'triangle',det:3,spread:11,g:.3});
  TN(c,t+.26,{dur:.58,f0:155,f1:97,det:2,spread:9,g:.12,pan:.26});
  NS(c,t+.42,{dur:.48,f0:1600,f1:360,q:2.2,g:.12,pan:.3}); },
woojin:function(c,t){                        /* 절단 — 베임, 정적, 낙하 */
  CK(c,t+.05,{hp:6000,g:.5});
  NS(c,t+.05,{dur:.07,f0:7000,f1:2600,q:5,g:.4});
  NS(c,t+.09,{dur:.2,f0:3000,f1:900,q:3,g:.08,pan:.3});
  SB(c,t+.4,{dur:.52,f0:140,f1:28,g:.7,drive:2.2});
  MD(c,t+.4,{f:110,mat:'stone',dec:.62,g:.28,pan:-.15});
  NS(c,t+.4,{dur:.44,f0:460,f1:86,q:.8,g:.2,type:'lowpass'});
  TN(c,t+.44,{dur:.7,f0:74,f1:51,type:'triangle',det:2,spread:7,g:.14,a:.05}); },
wolyoung:function(c,t){                      /* 잠식 — 삼킴 */
  TN(c,t,{dur:.9,f0:210,f1:26,det:3,spread:5,g:.52,a:.05});
  NS(c,t,{dur:.85,f0:1000,f1:62,q:.5,g:.3,type:'lowpass',a:.04,pan:-.18});
  NS(c,t+.06,{dur:.7,f0:700,f1:70,q:.6,g:.2,type:'lowpass',a:.06,pan:.22});
  TN(c,t+.36,{dur:.6,f0:62,f1:34,type:'triangle',det:2,spread:6,g:.22,a:.05}); },
mika:function(c,t){                          /* 서리 — 결정 균열 + 파쇄 */
  for(var i=0;i<7;i++){
    var tt=t+i*.05, pn=((i*.37)%1)*2-1;
    MD(c,tt,{f:2400+i*520,mat:'glass',dec:.2,damp:.8,q:30,g:.2,pan:pn*.5}); }
  CK(c,t+.42,{hp:2400,g:.34});
  MD(c,t+.42,{f:640,mat:'glass',dec:.7,damp:.45,q:24,g:.34});
  NS(c,t+.42,{dur:.4,f0:3000,f1:520,q:1.1,g:.3});
  SB(c,t+.43,{dur:.46,f0:170,f1:54,g:.3,drive:1.4});
  TN(c,t+.06,{dur:.75,f0:1046,f1:1042,det:2,spread:5,g:.06,a:.12}); },
gard:function(c,t){                          /* 붕괴 — 돌진 + 잔해 */
  CK(c,t,{hp:700,g:.5});
  SB(c,t,{dur:.9,f0:96,f1:22,g:.85,drive:3});
  MD(c,t,{f:120,mat:'stone',dec:.75,damp:.45,g:.4});
  NS(c,t,{dur:.66,f0:340,f1:56,q:.55,g:.36,type:'lowpass'});
  for(var i=0;i<6;i++){
    var tt=t+.15+i*.065;
    MD(c,tt,{f:700+Math.random()*1500,mat:'stone',dec:.17,damp:.9,q:18,g:.16,
      pan:(Math.random()*2-1)*.6}); }
  TN(c,t+.2,{dur:.66,f0:48,f1:29,type:'triangle',det:2,spread:5,g:.2,a:.04}); },
shera:function(c,t){                         /* 화염 — 교차 */
  NS(c,t,{dur:.42,f0:620,f1:3400,q:.65,g:.4,pan:-.55});
  NS(c,t+.15,{dur:.48,f0:3200,f1:460,q:.65,g:.38,pan:.55});
  CK(c,t+.15,{hp:1600,g:.22});
  SB(c,t+.16,{dur:.5,f0:130,f1:44,g:.34,drive:2});
  NS(c,t+.3,{dur:.52,f0:1400,f1:280,q:1,g:.18,type:'lowpass'}); },
dor:function(c,t){                           /* 음파 — 소나 */
  var f=[1480,1174,987];
  for(var i=0;i<3;i++){
    var tt=t+i*.22, pn=(i-1)*.4;
    CK(c,tt,{hp:4000,g:.1,pan:pn});
    TN(c,tt,{dur:.5+i*.1,f0:f[i],f1:f[i]-6,det:2,spread:3,g:.36-i*.09,a:.004,pan:pn}); }
  NS(c,t,{dur:.22,f0:4200,f1:2200,q:2.6,g:.08});
  TN(c,t+.5,{dur:.55,f0:247,f1:246,det:2,spread:5,g:.07,a:.08}); },
nina:function(c,t){                          /* 껍질 — 3단 걸쇠 */
  for(var i=0;i<3;i++){
    var tt=t+.05+i*.2, pn=(i-1)*.3;
    CK(c,tt,{hp:2000,g:.3,pan:pn});
    MD(c,tt,{f:380+i*90,mat:'wood',dec:.24,damp:.85,q:18,g:.32,pan:pn});
    TN(c,tt,{dur:.1,f0:210,f1:104,det:2,spread:6,g:.26,a:.002}); }
  MD(c,t+.62,{f:150,mat:'stone',dec:.5,g:.22});
  TN(c,t+.62,{dur:.45,f0:150,f1:78,type:'triangle',det:2,spread:5,g:.16,a:.02}); },
mujin:function(c,t){                         /* 결손 — 스태틱 */
  for(var i=0;i<7;i++){
    var tt=t+i*.105+Math.random()*.03;
    NS(c,tt,{dur:.03+Math.random()*.06,f0:500+Math.random()*3600,f1:380,q:1.1,g:.32,a:.002,
      pan:(Math.random()*2-1)*.7}); }
  TN(c,t+.18,{dur:.6,f0:41,f1:41,type:'sawtooth',det:2,spread:24,g:.1,a:.12});
  TN(c,t+.5,{dur:.44,f0:64,f1:37,type:'square',det:2,spread:14,g:.18});
  NS(c,t+.56,{dur:.34,f0:2400,f1:660,q:1,g:.22}); },
havel:function(c,t){                         /* 교체 — 미끄러짐 + 정지 */
  NS(c,t,{dur:.74,f0:460,f1:120,q:.75,g:.34,type:'lowpass',a:.11,pan:-.4});
  NS(c,t+.1,{dur:.6,f0:300,f1:150,q:1.4,g:.14,pan:.4});
  CK(c,t+.46,{hp:1200,g:.3});
  MD(c,t+.46,{f:240,mat:'wood',dec:.35,damp:.8,q:16,g:.3});
  SB(c,t+.46,{dur:.34,f0:160,f1:52,g:.4,drive:1.6}); },
rico:function(c,t){                          /* 방전 — 3연 스파크 */
  [0,.185,.395].forEach(function(o,i){
    var tt=t+o, pn=(i-1)*.45;
    CK(c,tt,{hp:5000,g:.42,pan:pn});
    NS(c,tt,{dur:.09,f0:6000,f1:1100,q:2.2,g:.4,a:.002,pan:pn});
    TN(c,tt,{dur:.08,f0:2100-i*380,f1:240,type:'square',det:2,spread:28,g:.2,a:.002,pan:pn}); });
  NS(c,t+.42,{dur:.44,f0:3400,f1:760,q:1,g:.16});
  SB(c,t+.42,{dur:.42,f0:100,f1:40,g:.3,drive:1.8}); },
alma:function(c,t){                          /* 급강하 — 돌풍 */
  NS(c,t,{dur:.76,f0:3600,f1:280,q:.5,g:.42,a:.06,pan:.5});
  NS(c,t+.06,{dur:.7,f0:2600,f1:340,q:.6,g:.26,a:.06,pan:-.45});
  TN(c,t+.3,{dur:.5,f0:320,f1:78,type:'triangle',det:3,spread:9,g:.24});
  NS(c,t+.5,{dur:.44,f0:1000,f1:240,q:1.3,g:.16,type:'lowpass'}); },

/* ── 공용 UI ── */
tab:function(c,t){
  CK(c,t,{hp:3000,g:.2});
  MD(c,t,{f:920,mat:'metal',dec:.14,damp:.95,q:16,g:.16,n:3});
  TN(c,t,{dur:.07,f0:1200,f1:700,det:2,spread:8,g:.1,a:.002}); },
back:function(c,t){
  CK(c,t,{hp:1600,g:.18});
  TN(c,t,{dur:.12,f0:520,f1:300,det:2,spread:8,g:.14,a:.003});
  NS(c,t,{dur:.16,f0:1400,f1:500,q:1.4,g:.1}); },
evi:function(c,t){                           /* 수거품 판독 */
  CK(c,t,{hp:3400,g:.22});
  TN(c,t,{dur:.5,f0:1760,f1:1755,det:2,spread:4,g:.16,a:.004,pan:-.15});
  TN(c,t+.09,{dur:.44,f0:2637,f1:2630,det:2,spread:5,g:.09,a:.004,pan:.2});
  NS(c,t,{dur:.3,f0:4600,f1:1600,q:2,g:.12});
  NS(c,t+.18,{dur:.3,f0:900,f1:2400,q:1.2,g:.08}); },

/* ── 입장 게이트 ── */
gateHover:function(c,t){ CK(c,t,{hp:4200,g:.1});
  TN(c,t,{dur:.05,f0:1900,f1:1500,g:.07,a:.002}); },
gateOpen:function(c,t){                      /* CLICK HERE — 기동 */
  CK(c,t,{hp:800,g:.4});
  MD(c,t,{f:180,mat:'metal',dec:.6,damp:.5,q:20,g:.3});
  SB(c,t,{dur:.7,f0:70,f1:38,g:.6,drive:2.2});
  NS(c,t+.02,{dur:.9,f0:200,f1:2600,q:.5,g:.26,a:.22});
  TN(c,t+.05,{dur:1.1,f0:55,f1:110,det:3,spread:7,g:.24,a:.4});
  TN(c,t+.3,{dur:.9,f0:165,f1:220,type:'triangle',det:2,spread:10,g:.1,a:.35,pan:.2}); },
gateType:function(c,t){                      /* 로그 한 줄 */
  CK(c,t,{hp:5200,g:.07,pan:(Math.random()*2-1)*.6});
  TN(c,t,{dur:.026,f0:2600+Math.random()*1400,f1:1400,type:'square',g:.045,a:.001}); },
gateLock:function(c,t){                      /* 조준 고정 */
  CK(c,t,{hp:3600,g:.24});
  MD(c,t,{f:1480,mat:'metal',dec:.28,damp:.7,q:26,g:.24,n:3});
  TN(c,t,{dur:.18,f0:880,f1:1320,det:2,spread:6,g:.16,a:.004});
  NS(c,t,{dur:.24,f0:5000,f1:1800,q:2.4,g:.1}); },
gateGrant:function(c,t){                     /* ACCESS GRANTED */
  CK(c,t,{hp:2000,g:.34});
  [523.25,659.25,783.99,1046.5].forEach(function(f,i){
    TN(c,t+i*.045,{dur:.7-i*.08,f0:f,f1:f-2,det:2,spread:5,g:.2-i*.035,a:.005,pan:(i-1.5)*.22}); });
  SB(c,t,{dur:.6,f0:120,f1:46,g:.5,drive:2});
  NS(c,t,{dur:.5,f0:1200,f1:5000,q:.7,g:.2,a:.05}); },
gateWipe:function(c,t){                      /* 화면 전개 */
  NS(c,t,{dur:.5,f0:260,f1:5200,q:.55,g:.36,a:.06,pan:-.6});
  NS(c,t+.02,{dur:.5,f0:300,f1:5000,q:.55,g:.36,a:.06,pan:.6});
  TN(c,t,{dur:.46,f0:60,f1:2400,type:'triangle',det:2,spread:9,g:.16,a:.02});
  CK(c,t+.32,{hp:1000,g:.3});
  SB(c,t+.32,{dur:.5,f0:150,f1:34,g:.5,drive:2.4});
  TN(c,t+.34,{dur:.6,f0:15600,f1:15600,g:.03,a:.02}); },
crt:function(c,t){                           /* 본 화면 점등 */
  CK(c,t,{hp:600,g:.36});
  SB(c,t,{dur:.5,f0:110,f1:32,g:.46,drive:2});
  NS(c,t,{dur:.42,f0:400,f1:4200,q:.6,g:.24,a:.03});
  TN(c,t+.04,{dur:.8,f0:15700,f1:15680,g:.035,a:.03});
  MD(c,t+.02,{f:260,mat:'metal',dec:.5,damp:.6,q:18,g:.16}); }
};

/* 오프라인 렌더로 측정한 라우드니스 정규화 계수 */
var LVL={seolrin:1.071,theodore:1.5,kyle:1.114,lucia:1.113,isabel:3.603,barhan:1.865,rhea:1.14,haito:1.579,woojin:1.09,wolyoung:1.121,mika:1.192,gard:1.098,shera:1.109,dor:1.792,nina:1.449,mujin:2.182,havel:1.127,rico:1.167,alma:1.411,tab:2.272,back:2.269,evi:2.813,gateHover:2.352,gateOpen:1.324,gateType:2.284,gateLock:3.105,gateGrant:1.283,gateWipe:1.105,crt:1.414};

function play(name){
  var c=ctx(); if(!c) return;
  var f=CUE[name]; if(!f) return;
  GN=LVL[name]||1;
  try{ f(c, c.currentTime+.02); }catch(e){}
  GN=1;
}
g.SFX={
  play:play,
  cues:CUE,
  muted:function(){ return MUTE; },
  setMute:function(v){ MUTE=!!v; try{ localStorage.setItem('tia_mute',MUTE?'1':'0'); }catch(e){} },
  toggle:function(){ this.setMute(!MUTE); return MUTE; },
  _lvl:function(o){ LVL=o; },
  _gn:function(v){ GN=v; },
  _reset:function(){ RIG=null; NB=null; },
  _rig:rig
};
})(window);
