/* TAMER IN APOCALYPSE — UI 효과음
   톤(피치) 성분 배제. 광대역 트랜지언트 + 비조화 공명 + 비트크러시 노이즈로만 구성. */
(function(g){
'use strict';
var AC=null, RIG=null, MUTE=false, NB=null, GN=1;
try{ MUTE = localStorage.getItem('tia_mute')==='1'; }catch(e){}

function ac(){
  if(MUTE) return null;
  if(!AC){ try{ AC=new (g.AudioContext||g.webkitAudioContext)(); }catch(e){ return null; } }
  if(!AC) return null;
  if(AC.state==='suspended'){ try{ AC.resume(); }catch(e){} }
  return AC;
}
function dist(c,k){
  var n=2048, cur=new Float32Array(n);
  for(var i=0;i<n;i++){ var x=i*2/n-1; cur[i]=(1+k)*x/(1+k*Math.abs(x)); }
  var w=c.createWaveShaper(); w.curve=cur; w.oversample='2x'; return w;
}
function crush(c,bits){
  var n=4096, cur=new Float32Array(n), q=Math.pow(2,bits);
  for(var i=0;i<n;i++){ var x=i*2/n-1; cur[i]=Math.round(x*q)/q; }
  var w=c.createWaveShaper(); w.curve=cur; w.oversample='none'; return w;
}
function rig(c){
  if(RIG && RIG.c===c) return RIG;
  var cp=c.createDynamicsCompressor();
  cp.threshold.value=-11; cp.knee.value=6; cp.ratio.value=9;
  cp.attack.value=.0008; cp.release.value=.07;
  var out=c.createGain(); out.gain.value=.9;
  cp.connect(out); out.connect(c.destination);
  var m=Math.floor(c.sampleRate*.14), ir=c.createBuffer(2,m,c.sampleRate);
  for(var ch=0;ch<2;ch++){ var d=ir.getChannelData(ch), lp=0;
    for(var j=0;j<m;j++){ var u=j/m, x=(Math.random()*2-1)*Math.pow(1-u,7);
      lp+=(x-lp)*.62; d[j]=lp*1.4; } }
  var cv=c.createConvolver(); cv.buffer=ir;
  var rg=c.createGain(); rg.gain.value=.11; cv.connect(rg); rg.connect(cp);
  var bus=c.createGain(); bus.connect(cp); bus.connect(cv);
  RIG={c:c,bus:bus}; return RIG;
}
function BUS(c){ return rig(c).bus; }
function nz(c){
  if(!NB){ var n=Math.floor(c.sampleRate*1.2), b=c.createBuffer(2,n,c.sampleRate);
    for(var ch=0;ch<2;ch++){ var d=b.getChannelData(ch);
      for(var i=0;i<n;i++) d[i]=Math.random()*2-1; }
    NB=b; }
  var s=c.createBufferSource(); s.buffer=NB; s.loop=true;
  s.playbackRate.value=.85+Math.random()*.35; return s;
}
function pan(c,v){ var p; try{ p=c.createStereoPanner(); p.pan.value=v||0; }catch(e){ p=c.createGain(); } return p; }
function env(gn,t,a,d,pk){
  a=Math.max(.0004,Math.min(a,d*.5));
  gn.gain.setValueAtTime(.0001,t);
  gn.gain.exponentialRampToValueAtTime(Math.max(.0004,pk*GN),t+a);
  gn.gain.exponentialRampToValueAtTime(.0001,t+d);
}
/* 필터 노이즈 */
function N(c,t,o){
  var s=nz(c), f=c.createBiquadFilter(), gn=c.createGain(), p=pan(c,o.pan), tail=f;
  f.type=o.type||'bandpass'; f.Q.value=o.q||4;
  f.frequency.setValueAtTime(Math.max(40,o.f0),t);
  f.frequency.exponentialRampToValueAtTime(Math.max(40,o.f1||o.f0),t+o.d);
  if(o.crush){ var cr=crush(c,o.crush); f.connect(cr); tail=cr; }
  if(o.drive){ var dr=dist(c,o.drive); tail.connect(dr); tail=dr; }
  tail.connect(gn); gn.connect(p); p.connect(BUS(c));
  env(gn,t,o.a||.0005,o.d,o.g||.3);
  s.connect(f); s.start(t); s.stop(t+o.d+.02);
}
/* 비조화 공명 — 짧게 감쇠시키면 '칵', 길게 두면 금속 울림 */
var RT={ clack:[1,2.41,3.87,5.12], glass:[1,2.32,4.25,6.63], plate:[1,1.73,2.61,3.44] };
function M(c,t,o){
  var rt=RT[o.mat||'clack'], ex=o.ex||.0035, p=pan(c,o.pan);
  p.connect(BUS(c));
  var s=nz(c), eg=c.createGain();
  s.connect(eg); env(eg,t,.0004,ex,1);
  s.start(t); s.stop(t+ex+.02);
  for(var i=0;i<rt.length;i++){
    var f=c.createBiquadFilter(); f.type='bandpass';
    f.frequency.value=Math.min(c.sampleRate/2.2, o.f*rt[i]*(1+(Math.random()-.5)*.02));
    f.Q.value=o.q||24;
    var gn=c.createGain();
    eg.connect(f); f.connect(gn); gn.connect(p);
    env(gn,t,.0006,(o.dec||.02)/(1+i*.75),(o.g||.3)/(1+i*.9));
  }
}
/* 벨 — 판독음 전용 */
function B(c,t,o){
  var p=pan(c,o.pan), gn=c.createGain();
  gn.connect(p); p.connect(BUS(c));
  for(var i=0;i<2;i++){
    var s=c.createOscillator(), sg=c.createGain();
    s.type='triangle'; s.detune.value=(i-.5)*(o.spread||4);
    s.frequency.setValueAtTime(o.f,t);
    s.frequency.exponentialRampToValueAtTime(o.f*.998,t+o.d);
    sg.gain.value=.5; s.connect(sg); sg.connect(gn);
    s.start(t); s.stop(t+o.d+.2);
  }
  env(gn,t,.003,o.d,o.g||.3);
}
/* 기계식 접점 한 방 */
function CK(c,t,o){
  o=o||{};
  N(c,t,{d:o.tr||.005,f0:o.hp||3600,f1:(o.hp||3600)*.6,q:.7,type:'highpass',g:o.g||.5,crush:o.crush});
  M(c,t+.0008,{f:o.f||1900,dec:o.dec||.02,g:(o.g||.5)*.55,q:o.q||22,pan:o.pan});
}

/* 디지털 채터 — 짧은 공명 버스트 연발 = 삐리리릭 */
function CH(c,t,o){
  var n=o.n||6, st=o.st||.016;
  for(var i=0;i<n;i++){
    var k = o.down ? (n-1-i) : i;
    var f = o.f0 * Math.pow(o.ratio||1.17, k) * (1+(Math.random()-.5)*.08);
    N(c,t+i*st,{d:o.d||.0085,f0:f,f1:f*.86,q:o.q||16,g:(o.g||.24)*3.2*(1-i*.035),
      crush:o.crush||3,pan:(i%2?1:-1)*(o.w||.45)});
  }
}
/* 하드 스태틱 — 지지지직 */
function ST(c,t,o){
  var s=nz(c), f=c.createBiquadFilter(), gn=c.createGain(), p=pan(c,o.pan),
      cr=crush(c,o.crush||2), dr=dist(c,o.drive||9);
  f.type='bandpass'; f.Q.value=o.q||2.4;
  f.frequency.setValueAtTime(Math.max(60,o.f0),t);
  var steps=o.steps||7;
  for(var i=1;i<=steps;i++){
    var u=i/steps, fr=o.f0+(o.f1-o.f0)*u + (Math.random()-.5)*o.f0*.55;
    f.frequency.setValueAtTime(Math.max(60,fr), t+o.d*u);
  }
  f.connect(cr); cr.connect(dr); dr.connect(gn); gn.connect(p); p.connect(BUS(c));
  env(gn,t,o.a||.0008,o.d,o.g||.26);
  s.connect(f); s.start(t); s.stop(t+o.d+.02);
}

var CUE={
  /* 로그 한 줄 */
  tick:function(c,t){
    N(c,t,{d:.006,f0:8200+Math.random()*2600,f1:5200,q:14,g:1.1,crush:3,
      pan:(Math.random()*2-1)*.6}); },
  /* 패널 전환 — 삐릭 */
  click:function(c,t){
    CH(c,t,{n:3,st:.011,f0:3400,ratio:1.28,g:.34,d:.008,q:18,crush:3,w:.35}); },
  /* 하위 분류 — 더 얇게 */
  sub:function(c,t){
    CH(c,t,{n:2,st:.01,f0:5600,ratio:1.34,g:.26,d:.006,q:20,crush:3,w:.3}); },
  /* 기록 열림 — 삐리리리릭 + 지지직 */
  open:function(c,t){
    CH(c,t,{n:11,st:.0175,f0:2000,ratio:1.135,g:.3,d:.009,q:17,crush:3,w:.5});
    ST(c,t+.2,{d:.17,f0:1400,f1:6400,q:2.2,g:.22,crush:2,drive:11,steps:9});
    CH(c,t+.29,{n:3,st:.013,f0:7200,ratio:.82,g:.2,d:.007,q:20,crush:2,w:.5}); },
  /* 닫힘 — 역방향 채터 + 짧은 스태틱 */
  back:function(c,t){
    CH(c,t,{n:5,st:.0135,f0:6800,ratio:.79,g:.28,d:.008,q:16,crush:3,w:.4});
    ST(c,t+.055,{d:.075,f0:5200,f1:900,q:2.6,g:.2,crush:2,drive:8,steps:5}); },
  /* 수거품 판독 — 벨 유지 */
  evi:function(c,t){
    CK(c,t,{hp:5600,f:3200,dec:.012,g:.24,crush:4});
    B(c,t,{f:1760,d:.44,g:.3,pan:-.16});
    B(c,t+.08,{f:2637,d:.36,g:.16,spread:5,pan:.2});
    N(c,t+.01,{d:.12,f0:5600,f1:2000,q:3,g:.07,crush:6}); },
  /* 재생 — 상승 3연 */
  play:function(c,t){
    CH(c,t,{n:3,st:.026,f0:2400,ratio:1.42,g:.34,d:.012,q:15,crush:3,w:.3});
    ST(c,t+.072,{d:.05,f0:3200,f1:1200,q:3,g:.14,crush:2,drive:7}); },
  /* 정지 — 하강 2연 */
  stop:function(c,t){
    CH(c,t,{n:2,st:.024,f0:3600,ratio:.62,g:.3,d:.011,q:15,crush:3,w:.25}); },
  seek:function(c,t){
    CH(c,t,{n:4,st:.009,f0:2800,ratio:1.3,g:.24,d:.006,q:19,crush:3,w:.45}); },

  /* ── 입장 화면 ── */
  /* 기동 — 스태틱 상승 + 부팅 채터 */
  boot:function(c,t){
    ST(c,t,{d:.42,f0:320,f1:7200,q:1.5,g:.3,crush:2,drive:12,steps:14});
    CH(c,t+.1,{n:9,st:.032,f0:2200,ratio:1.16,g:.26,d:.01,q:16,crush:3,w:.55});
    ST(c,t+.4,{d:.13,f0:6800,f1:2200,q:3,g:.16,crush:2,drive:9,steps:6}); },
  /* 조준 고정 */
  lock:function(c,t){
    CH(c,t,{n:2,st:.03,f0:4200,ratio:1.55,g:.38,d:.013,q:14,crush:3,w:.3});
    ST(c,t+.038,{d:.06,f0:5600,f1:2400,q:3,g:.18,crush:2,drive:8,steps:4}); },
  /* ACCESS GRANTED */
  grant:function(c,t){
    CH(c,t,{n:8,st:.022,f0:2600,ratio:1.22,g:.34,d:.011,q:15,crush:3,w:.5});
    ST(c,t+.14,{d:.2,f0:1800,f1:8200,q:2,g:.26,crush:2,drive:12,steps:10});
    CH(c,t+.26,{n:4,st:.018,f0:8200,ratio:.84,g:.22,d:.008,q:19,crush:2,w:.55}); },
  /* 화면 전개 */
  wipe:function(c,t){
    ST(c,t,{d:.3,f0:420,f1:9200,q:1.4,g:.34,crush:2,drive:13,steps:12,pan:-.6});
    ST(c,t+.02,{d:.3,f0:520,f1:8600,q:1.4,g:.34,crush:2,drive:13,steps:12,pan:.6});
    CH(c,t+.24,{n:5,st:.015,f0:6200,ratio:.83,g:.26,d:.008,q:18,crush:2,w:.6}); },
  /* 본 화면 점등 */
  crt:function(c,t){
    ST(c,t,{d:.26,f0:600,f1:7600,q:1.6,g:.3,crush:2,drive:11,steps:9});
    N(c,t+.05,{d:.5,f0:15600,f1:15400,q:30,g:.06});
    CH(c,t+.2,{n:3,st:.02,f0:5200,ratio:.88,g:.2,d:.008,q:18,crush:2,w:.4}); }
};

/* 오프라인 렌더로 측정한 정규화 계수 */
var LVL={tick:1.292,click:2.206,sub:1.991,open:2.031,back:1.936,evi:2.119,play:3.017,stop:2.116,seek:2.556,boot:2.693,lock:2.111,grant:1.869,wipe:1.314,crt:2.814};

function play(n){
  var c=ac(); if(!c) return;
  var f=CUE[n]; if(!f) return;
  GN=LVL[n]||1;
  try{ f(c, c.currentTime+.01); }catch(e){}
  GN=1;
}
var lastTick=0;
g.SFX={
  play:play,
  tick:function(){ var n=(g.performance&&performance.now)?performance.now():Date.now();
    if(n-lastTick<32) return; lastTick=n; play('tick'); },
  cues:CUE,
  muted:function(){ return MUTE; },
  setMute:function(v){ MUTE=!!v; try{ localStorage.setItem('tia_mute',MUTE?'1':'0'); }catch(e){} },
  toggle:function(){ this.setMute(!MUTE); return MUTE; },
  _lvl:function(o){ LVL=o; },
  _gn:function(v){ GN=v; },
  _reset:function(){ RIG=null; NB=null; }
};
})(window);
