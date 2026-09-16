document.querySelector('.navtoggle')?.addEventListener('click',function(){
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
