# The shell the interactive piece lives in: markup, style and behaviour, kept apart from the
# drawing so src/site.py stays about the drawing.
# __SVG__ / __ING__ / __DR__ / __HUE__ / __INDEX__ / __SHELF_LINE__ / __ICON__ filled by site.py.

PAGE = r"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Half the shelf pours one drink</title>
<meta name="description" content="143 classic cocktails call for 177 ingredients. Ninety-two of them pour exactly one drink and nothing else. Point at any bottle.">
<meta name="theme-color" content="#ffffff">
<link rel="icon" href="__ICON__">
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#E9E7E2;font-family:'Century Gothic',Questrial,Futura,sans-serif;color:#2E2A24;
     -webkit-text-size-adjust:100%}
#wrap{position:relative;width:min(100%,1000px);margin:0 auto;background:#fff;
      box-shadow:0 1px 24px rgba(0,0,0,.13)}
svg{display:block;width:100%;height:auto}
.o{cursor:pointer}
.o .hit{fill:transparent}
.o>*{transition:opacity .16s ease}
/* pointing at one bottle ghosts the other 176 - the relationship the paper cannot show */
#sheet.focus .o:not(.on)>*:not(.hit){opacity:.10}
#sheet.buy .o:not(.on)>*:not(.hit){opacity:.09}
@keyframes flash{0%,100%{opacity:1}35%{opacity:.12}}
.o.flash>*:not(.hit){animation:flash .55s ease 2}

/* The card is anchored to the bottle it is about, never parked at the top of the page: the
   ninety-two live 900px down, and a readout you have to scroll away from to read is no readout. */
#pop{position:absolute;width:252px;background:#fff;z-index:6;display:none;
     border-left:2px solid #B23A26;padding:10px 12px 11px;
     box-shadow:0 3px 16px rgba(0,0,0,.17)}
#pop.show{display:block}
#pop h3{font-size:16px;font-weight:400;line-height:1.15}
#pop .sub{font-size:9.5px;opacity:.5;margin-top:3px;letter-spacing:.7px;text-transform:uppercase}
#pop .one{font-size:15px;margin-top:9px;color:#B23A26;line-height:1.2;cursor:pointer}
#pop .with{font-size:9.5px;opacity:.5;margin-top:9px;letter-spacing:.7px;text-transform:uppercase}
/* a grid, not CSS columns: multi-column inside a capped height spills into MORE columns
   sideways, which gave gin's forty-two drinks a horizontal scrollbar */
#pop ul{list-style:none;margin-top:7px;max-height:212px;overflow-y:auto;overflow-x:hidden;
        scrollbar-width:thin;display:grid;grid-template-columns:1fr 1fr;column-gap:12px;
        align-content:start}
#pop ul.one-col{grid-template-columns:1fr}
#pop li{font-size:10.5px;line-height:1.62;opacity:.85;cursor:pointer;white-space:nowrap;
        overflow:hidden;text-overflow:ellipsis;break-inside:avoid}
#pop li:hover{opacity:1;color:#B23A26}
#pop i{display:inline-block;width:5px;height:5px;border-radius:50%;margin-right:5px;
       vertical-align:middle;font-style:normal}
#pop ul.fade{-webkit-mask-image:linear-gradient(#000 calc(100% - 20px),transparent);
             mask-image:linear-gradient(#000 calc(100% - 20px),transparent)}

#bar{position:absolute;left:7.6%;top:24.5%;display:flex;gap:calc(7px * var(--s));z-index:4}
button{font:inherit;font-size:calc(9.5px * var(--s));letter-spacing:calc(1.3px * var(--s));
       text-transform:uppercase;padding:calc(6px * var(--s)) calc(11px * var(--s));
       background:#fff;color:#2E2A24;border:calc(1px * var(--s)) solid rgba(46,42,36,.30);
       cursor:pointer;line-height:1;white-space:nowrap}
button:hover{border-color:#B23A26;color:#B23A26}
button.on{background:#B23A26;border-color:#B23A26;color:#fff}
#count{position:absolute;left:7.6%;top:17.2%;width:52%;display:none;z-index:3}
#count.show{display:block}
#sheet .deck,#sheet .teach{transition:opacity .2s ease}
#sheet.buy .deck{opacity:0}
#sheet.buy .teach,#sheet.focus .teach{opacity:0}
#count .big{font-size:calc(31px * var(--s));line-height:1.15}
#count em{font-style:normal;color:#B23A26}
#count .lede{font-size:calc(12px * var(--s));opacity:.62;margin-top:calc(7px * var(--s));
             line-height:1.5;max-width:calc(430px * var(--s))}
#hint{display:none;padding:0 12px 10px;font-size:11px;letter-spacing:.5px;opacity:.5;
      text-transform:uppercase;background:#fff}

/* the ninety-two, given the room the poster cannot give them */
#ninety{width:min(100%,1000px);margin:0 auto 30px;background:#fff;padding:34px 76px 40px;
        box-shadow:0 1px 24px rgba(0,0,0,.13);border-top:1px solid rgba(46,42,36,.13)}
#ninety h2{font-size:31px;font-weight:400;line-height:1.15}
#ninety .lede{font-size:13px;opacity:.66;margin-top:10px;line-height:1.65;max-width:640px}
#ninety .lede b{font-weight:400;color:#B23A26}
#grid{margin-top:26px;columns:3;column-gap:26px}
#grid article{break-inside:avoid;margin-bottom:15px;padding-bottom:13px;
              border-bottom:1px solid rgba(46,42,36,.10)}
#grid h4{font-size:12.5px;font-weight:400;line-height:1.25}
#grid h4 i{display:inline-block;width:6px;height:6px;border-radius:50%;margin-right:6px;
           vertical-align:middle;font-style:normal}
#grid h4 s{text-decoration:none;opacity:.4;font-size:10px}
#grid ul{list-style:none;margin-top:5px}
#grid li{font-size:10.5px;line-height:1.6;opacity:.62;cursor:pointer;padding-left:12px;
         position:relative}
#grid li:before{content:'';position:absolute;left:2px;top:.72em;width:5px;height:1px;
                background:#B23A26;opacity:.6}
#grid li:hover{opacity:1;color:#B23A26}

@media (max-width:900px){#grid{columns:2}#ninety{padding:30px 40px 34px}}
@media (max-width:719px){
  /* a card pinned beside a 7px bottle is unusable; on a phone it becomes a sheet that is always
     in frame, with targets a thumb can actually hit */
  #pop{position:fixed!important;left:0!important;top:auto!important;bottom:0;width:100%;
       max-height:56vh;overflow:auto;border-left:0;border-top:3px solid #B23A26;
       padding:14px 16px 20px;box-shadow:0 -2px 18px rgba(0,0,0,.18)}
  #pop h3{font-size:20px}#pop .sub{font-size:11px}#pop .one{font-size:19px}
  #pop .with{font-size:11px}
  #pop ul{max-height:32vh}#pop li{font-size:13px;line-height:1.9}
  #bar{position:static;display:flex;flex-wrap:wrap;padding:10px 12px;background:#fff;
       border-bottom:1px solid rgba(46,42,36,.14);gap:7px}
  button{font-size:11px;padding:9px 12px;border-width:1px}
  #count{position:static;width:auto;padding:13px 15px 3px}
  #count .big{font-size:29px}#count .lede{font-size:13px;max-width:none}
  #hint{display:block}
  #ninety{padding:26px 18px 30px;margin-bottom:0}#grid{columns:1}
  #ninety h2{font-size:25px}#grid li{font-size:12.5px;line-height:1.95}
  #grid h4{font-size:14px}
}
</style></head><body>
<div id="wrap">
  <div id="bar">
    <button id="mRead" class="on">Point at a bottle</button>
    <button id="mBuy">Buy the shelf</button>
  </div>
  <div id="hint">Pinch to zoom &#183; tap any bottle</div>
  <div id="count"><div class="big"></div><div class="lede"></div></div>
  <div id="pop"></div>
  __SVG__
</div>
__INDEX__
<script>
var ING=__ING__, DR=__DR__, HUE=__HUE__;
var sheet=document.getElementById('sheet'), pop=document.getElementById('pop'),
    wrap=document.getElementById('wrap'), countBox=document.getElementById('count'),
    bar=document.getElementById('bar');
var nodes=Array.prototype.slice.call(sheet.querySelectorAll('.o'));
var byIng={}; nodes.forEach(function(n){byIng[+n.dataset.i]=n});
var uses={}; DR.forEach(function(d,di){d[2].forEach(function(i){(uses[i]=uses[i]||[]).push(di)})});
function phone(){return matchMedia('(max-width:719px)').matches}

var mode='read', owned={}, ownedN=0;

function rescale(){wrap.style.setProperty('--s', wrap.clientWidth/1000);
  /* a desktop anchor left inline on a now-narrow window is stale; the sheet re-pins itself */
  pop.style.left=''; pop.style.top=''; if(pop.classList.contains('show'))clear()}
addEventListener('resize',rescale); rescale();

function cap(s){return s.charAt(0).toUpperCase()+s.slice(1)}
function dot(base){return '<i style="background:'+(HUE[base]||'#B9A489')+'"></i>'}
function lit(on){nodes.forEach(function(n){
  if(on[+n.dataset.i]) n.classList.add('on'); else n.classList.remove('on')})}
function only(list){var o={};list.forEach(function(i){o[i]=1});return o}

/* Put the card against the bottle it is about: above by default, flipped below when it would run
   off the top, clamped so it never leaves the page on either side. */
function anchor(i){
  if(phone()){pop.style.left='';pop.style.top='';return}
  var g=byIng[i]; if(!g)return;
  var s=wrap.clientWidth/1000, GAP=9;
  var svgTop=sheet.getBoundingClientRect().top-wrap.getBoundingClientRect().top;
  var cx=+g.dataset.x*s, h=+g.dataset.h*s, w=+g.dataset.w*s;
  var top=svgTop+(+g.dataset.y-+g.dataset.h)*s, bot=svgTop+ +g.dataset.y*s;
  var pw=pop.offsetWidth, ph=pop.offsetHeight, W=wrap.clientWidth, H=wrap.clientHeight;
  var x=Math.max(8,Math.min(W-pw-8,cx-pw/2)), y=top-ph-GAP;
  if(y<4){
    /* No room above - which is the normal case for the two tallest bottles once the poster is
       scaled down. Sit beside the mark rather than dropping below it: flipping under sent gin's
       card three hundred pixels down the page, nowhere near the bottle it was describing. */
    var side=Math.max(4,Math.min(H-ph-4, top+h/2-ph/2));
    if(cx+w/2+GAP+pw<=W-8){x=cx+w/2+GAP; y=side}
    else if(cx-w/2-GAP-pw>=8){x=cx-w/2-GAP-pw; y=side}
    else y=bot+GAP;
  }
  pop.style.left=x+'px'; pop.style.top=y+'px';
}
function fade(){var u=pop.querySelector('ul');
  if(u){u.classList.toggle('one-col',u.children.length<7);
        u.classList.toggle('fade',u.scrollHeight>u.clientHeight+1)}}

function showIng(i){
  sheet.classList.add('focus'); lit(only([i]));
  var ds=uses[i]||[], h='<h3>'+cap(ING[i][0])+'</h3>';
  if(ds.length===1){
    var d=DR[ds[0]];
    h+='<div class="sub">Pours one drink. Nothing else.</div>'
      +'<div class="one" data-d="'+ds[0]+'">'+d[0]+'</div>'
      +'<div class="with">Which also needs</div><ul>'
      +d[2].filter(function(j){return j!==i}).map(function(j){
         return '<li data-i="'+j+'">'+cap(ING[j][0])+'</li>'}).join('')+'</ul>';
  } else {
    h+='<div class="sub">'+ds.length+' of the 143 drinks</div><ul>'
      +ds.map(function(di){return '<li data-d="'+di+'">'+dot(DR[di][1])+DR[di][0]+'</li>'}).join('')
      +'</ul>';
  }
  pop.innerHTML=h; pop.classList.add('show'); wire(); fade(); anchor(i);
}

/* the jump back across the graph: a drink lights every bottle it needs */
function showDrink(di){
  var d=DR[di];
  sheet.classList.add('focus'); lit(only(d[2]));
  pop.innerHTML='<h3>'+d[0]+'</h3><div class="sub">'+dot(d[1])+d[2].length
    +' ingredients &#183; '+d[1]+'</div><ul>'
    +d[2].map(function(i){return '<li data-i="'+i+'">'+cap(ING[i][0])+'</li>'}).join('')+'</ul>';
  pop.classList.add('show'); wire(); fade(); anchor(d[2][0]);
}

function wire(){
  pop.querySelectorAll('[data-d]').forEach(function(el){
    el.addEventListener('pointerup',function(e){e.stopPropagation();showDrink(+el.dataset.d)})});
  pop.querySelectorAll('[data-i]').forEach(function(el){
    el.addEventListener('pointerup',function(e){e.stopPropagation();showIng(+el.dataset.i)})});
}
function clear(){sheet.classList.remove('focus');pop.classList.remove('show');lit({})}

function complete(){var m=0;for(var k=0;k<DR.length;k++){
  var d=DR[k][2],ok=1;for(var j=0;j<d.length;j++)if(!owned[d[j]]){ok=0;break}
  if(ok)m++} return m}

function buyRender(){
  lit(owned);
  var m=complete(), n=ownedN;
  countBox.querySelector('.big').innerHTML=n+' bottle'+(n==1?'':'s')+' &#8594; <em>'+m+'</em> of 143';
  countBox.querySelector('.lede').textContent = n===0
    ? 'Your shelf is empty. Tap any bottle to buy it, or let the page pick for you.'
    : m===0 ? 'Still nothing. A drink needs every one of its ingredients, not some of them.'
    : '__SHELF_LINE__';
  var made=DR.filter(function(x){return x[2].every(function(i){return !!owned[i]})});
  pop.innerHTML='<h3>What you can make</h3><div class="sub">'+m+' of the 143</div><ul>'
    +(m?made.map(function(d){return '<li>'+dot(d[1])+d[0]+'</li>'}).join('')
       :'<li style="opacity:.45;cursor:default">Nothing yet</li>')+'</ul>';
  pop.classList.add('show'); fade();
  if(!phone()){pop.style.left=(wrap.clientWidth-pop.offsetWidth-22)+'px';pop.style.top='64px'}
}

/* the greediest bottle available: the one that finishes the most drinks next */
function best(){
  var pick=-1,gain=-1;
  for(var i=0;i<ING.length;i++){
    if(owned[i])continue;
    owned[i]=1; var g=complete(); delete owned[i];
    if(g>gain||(g===gain&&pick>=0&&ING[i][1]>ING[pick][1])){gain=g;pick=i}
  }
  return pick;
}

function setMode(m){
  mode=m; owned={}; ownedN=0; clear();
  sheet.classList.toggle('buy',m==='buy');
  countBox.classList.toggle('show',m==='buy');
  document.getElementById('mRead').classList.toggle('on',m==='read');
  document.getElementById('mBuy').classList.toggle('on',m==='buy');
  var old=document.getElementById('mBest'); if(old)old.remove();
  if(m==='buy'){
    bar.insertAdjacentHTML('beforeend','<button id="mBest">Buy the best next bottle</button>');
    document.getElementById('mBest').addEventListener('pointerup',function(e){
      e.stopPropagation(); var p=best(); if(p>=0){owned[p]=1;ownedN++;buyRender()}});
    buyRender();
  }
}
document.getElementById('mRead').addEventListener('pointerup',
  function(e){e.stopPropagation();setMode('read')});
document.getElementById('mBuy').addEventListener('pointerup',
  function(e){e.stopPropagation();setMode('buy')});

/* Selection is bound to pointerup, never click: on iOS the first tap on a mark whose
   pointerenter mutates the DOM is swallowed, and the piece would need two taps to answer. */
nodes.forEach(function(n){
  var i=+n.dataset.i;
  n.addEventListener('pointerup',function(e){
    e.stopPropagation();
    if(mode==='buy'){
      if(owned[i]){delete owned[i];ownedN--}else{owned[i]=1;ownedN++}
      buyRender();
    } else showIng(i);
  });
});
if(matchMedia('(hover:hover) and (pointer:fine)').matches){
  nodes.forEach(function(n){
    var i=+n.dataset.i;
    n.addEventListener('pointerenter',function(){if(mode==='read')showIng(i)});
  });
  sheet.addEventListener('pointerleave',function(e){
    if(mode==='read'&&!pop.contains(e.relatedTarget))clear()});
}
addEventListener('pointerup',function(){if(mode==='read')clear()});
addEventListener('keydown',function(e){
  if(e.key==='Escape'){if(mode==='buy')setMode('read');else clear()}});

/* the index sends you back to the shelf: find the bottle, flash it, open its card */
document.querySelectorAll('#grid li').forEach(function(li){
  li.addEventListener('pointerup',function(e){
    e.stopPropagation();
    var i=+li.dataset.i, n=byIng[i]; if(!n)return;
    if(mode==='buy')setMode('read');
    n.scrollIntoView({block:'center',behavior:'smooth'});
    n.classList.add('flash'); setTimeout(function(){n.classList.remove('flash')},1200);
    setTimeout(function(){showIng(i)},430);
  });
});
</script></body></html>"""
