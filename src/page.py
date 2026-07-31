# The shell the interactive piece lives in: markup, style and behaviour, kept apart from the
# drawing so src/site.py stays about the drawing. __SVG__ / __ING__ / __DR__ are filled by site.py.

PAGE = r"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Half the shelf pours one drink</title>
<meta name="description" content="143 classic cocktails call for 177 ingredients. Ninety of them appear in exactly one drink and nothing else. Point at any bottle.">
<meta name="theme-color" content="#ffffff">
<link rel="icon" href="data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20viewBox%3D%220%200%2032%2032%22%3E%3Cpath%20d%3D%22M11%2030%20L11%2014%20L13.5%2010.5%20L13.5%203%20L18.5%203%20L18.5%2010.5%20L21%2014%20L21%2030%20Z%22%20fill%3D%22%231F9E8E%22%2F%3E%3Cpath%20d%3D%22M16%2030%20L16%203%20L18.5%203%20L18.5%2010.5%20L21%2014%20L21%2030%20Z%22%20fill%3D%22%2317786B%22%2F%3E%3Cpath%20d%3D%22M13%205.4%20L19%205.4%20L19%203%20L13%203%20Z%22%20fill%3D%22%230F5A50%22%2F%3E%3C%2Fsvg%3E">
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#E9E7E2;font-family:'Century Gothic',Questrial,Futura,sans-serif;color:#2E2A24;
     -webkit-text-size-adjust:100%}
#wrap{position:relative;width:min(100vw,1000px);margin:0 auto;background:#fff;
      box-shadow:0 1px 24px rgba(0,0,0,.13)}
svg{display:block;width:100%;height:auto}
.o{cursor:pointer}
.o .hit{fill:transparent}
.o>*{transition:opacity .16s ease}
/* pointing at one bottle ghosts the other 176 - the relationship the paper cannot show */
#sheet.focus .o:not(.on)>*:not(.hit){opacity:.10}
#sheet.buy .o:not(.on)>*:not(.hit){opacity:.09}

#panel{position:absolute;left:62.4%;top:5.6%;width:30%;background:#fff;
       border-left:calc(2px * var(--s)) solid #B23A26;padding:calc(9px * var(--s));
       display:none;z-index:3}
#panel.show{display:block}
#panel h3{font-size:calc(15px * var(--s));font-weight:400;line-height:1.15}
#panel .sub{font-size:calc(10px * var(--s));opacity:.55;margin-top:calc(3px * var(--s));
            letter-spacing:calc(.6px * var(--s))}
#panel ul{list-style:none;margin-top:calc(7px * var(--s));max-height:calc(290px * var(--s));
          overflow:auto;scrollbar-width:thin}
/* a long list is scrolled, not truncated; the fade says so instead of a cut-off row */
#panel ul{-webkit-mask-image:linear-gradient(#000 calc(100% - 22px),transparent);
          mask-image:linear-gradient(#000 calc(100% - 22px),transparent)}
#panel ul.short{-webkit-mask-image:none;mask-image:none}
#panel li{font-size:calc(10.5px * var(--s));line-height:1.65;opacity:.82;cursor:pointer;
          white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
#panel li:hover{opacity:1;color:#B23A26}
#panel li b{font-weight:400;opacity:.45;font-size:calc(9px * var(--s))}

#bar{position:absolute;left:7.6%;top:24.5%;display:flex;gap:calc(7px * var(--s));z-index:4}
button{font:inherit;font-size:calc(9.5px * var(--s));letter-spacing:calc(1.3px * var(--s));
       text-transform:uppercase;padding:calc(6px * var(--s)) calc(11px * var(--s));
       background:#fff;color:#2E2A24;border:calc(1px * var(--s)) solid rgba(46,42,36,.30);
       cursor:pointer;line-height:1;white-space:nowrap}
button:hover{border-color:#B23A26;color:#B23A26}
button.on{background:#B23A26;border-color:#B23A26;color:#fff}
#count{position:absolute;left:7.6%;top:17.2%;width:52%;display:none;z-index:3}
#sheet .deck{transition:opacity .2s ease}
#sheet.buy .deck{opacity:0}
/* the how-to-read block has done its job once the panel is open */
#sheet .teach{transition:opacity .2s ease}
#sheet.buy .teach,#sheet.focus .teach{opacity:0}
#count.show{display:block}
/* the ninety are ~7px wide on a phone: say how to get into them rather than pretend otherwise */
#hint{display:none;padding:0 12px 10px;font-size:11px;letter-spacing:.5px;opacity:.5;
      text-transform:uppercase;background:#fff}
#count .big{font-size:calc(31px * var(--s));line-height:1.15}
#count em{font-style:normal;color:#B23A26}
#count .lede{font-size:calc(12px * var(--s));opacity:.62;margin-top:calc(7px * var(--s));
             line-height:1.5;max-width:calc(430px * var(--s))}

@media (max-width:719px){
  #panel{position:fixed;left:0;top:auto;bottom:0;width:100%;max-height:54vh;overflow:auto;
         border-left:0;border-top:3px solid #B23A26;padding:13px 15px 18px;
         box-shadow:0 -2px 18px rgba(0,0,0,.16)}
  #panel h3{font-size:19px}#panel .sub{font-size:11.5px;letter-spacing:.6px}
  #panel ul{max-height:34vh}#panel li{font-size:13.5px;line-height:1.9}
  #panel li b{font-size:11px}
  #bar{position:static;display:flex;flex-wrap:wrap;padding:10px 12px;background:#fff;
       border-bottom:1px solid rgba(46,42,36,.14);gap:7px}
  button{font-size:11px;padding:9px 12px;border-width:1px}
  #count{position:static;width:auto;padding:13px 15px 3px}
  #hint{display:block}
  #count .big{font-size:29px}#count .lede{font-size:13px;max-width:none}
}
</style></head><body>
<div id="wrap">
  <div id="bar">
    <button id="mRead" class="on">Point at a bottle</button>
    <button id="mBuy">Buy the shelf</button>
  </div>
  <div id="hint">Pinch to zoom · tap any bottle</div>
  <div id="count"><div class="big"></div><div class="lede"></div></div>
  <div id="panel"></div>
  __SVG__
</div>
<script>
var ING=__ING__, DR=__DR__;
var sheet=document.getElementById('sheet'), panel=document.getElementById('panel'),
    wrap=document.getElementById('wrap'), countBox=document.getElementById('count'),
    bar=document.getElementById('bar');
var nodes=Array.prototype.slice.call(sheet.querySelectorAll('.o'));
var uses={}; DR.forEach(function(d,di){d[2].forEach(function(i){(uses[i]=uses[i]||[]).push(di)})});

var mode='read', owned={}, ownedN=0;

/* keeps the overlay measured in the poster's own units at any width */
function rescale(){wrap.style.setProperty('--s', wrap.clientWidth/1000)}
addEventListener('resize',rescale); rescale();

function cap(s){return s.charAt(0).toUpperCase()+s.slice(1)}
function lit(on){nodes.forEach(function(n){
  if(on[+n.dataset.i]) n.classList.add('on'); else n.classList.remove('on');})}
function only(list){var o={};list.forEach(function(i){o[i]=1});return o}

function showIng(i){
  sheet.classList.add('focus'); lit(only([i]));
  var ds=uses[i]||[];
  panel.innerHTML='<h3>'+cap(ING[i][0])+'</h3><div class="sub">IN '+ING[i][1]
    +' OF THE 143 DRINK'+(ING[i][1]==1?'':'S')+'</div><ul>'
    +ds.map(function(di){return '<li data-d="'+di+'">'+DR[di][0]+' <b>'+DR[di][1]+'</b></li>'}).join('')
    +'</ul>';
  panel.classList.add('show'); wire(); fade();
}

/* the jump back across the graph: a drink lights every bottle it needs */
function showDrink(di){
  var d=DR[di];
  sheet.classList.add('focus'); lit(only(d[2]));
  panel.innerHTML='<h3>'+d[0]+'</h3><div class="sub">'+d[2].length+' INGREDIENTS &#183; '
    +d[1].toUpperCase()+'</div><ul>'
    +d[2].map(function(i){return '<li data-i="'+i+'">'+cap(ING[i][0])+' <b>'+ING[i][1]
      +(ING[i][1]==1?' drink':' drinks')+'</b></li>'}).join('')+'</ul>';
  panel.classList.add('show'); wire(); fade();
}

/* only fade a list that actually overflows */
function fade(){var u=panel.querySelector('ul');
  if(u)u.classList.toggle('short',u.scrollHeight<=u.clientHeight+1)}

function wire(){
  panel.querySelectorAll('li[data-d]').forEach(function(li){
    li.addEventListener('pointerup',function(e){e.stopPropagation();showDrink(+li.dataset.d)})});
  panel.querySelectorAll('li[data-i]').forEach(function(li){
    li.addEventListener('pointerup',function(e){e.stopPropagation();showIng(+li.dataset.i)})});
}

function clear(){sheet.classList.remove('focus');panel.classList.remove('show');lit({})}

function complete(){var m=0;for(var k=0;k<DR.length;k++){
  var d=DR[k][2],ok=1;for(var j=0;j<d.length;j++)if(!owned[d[j]]){ok=0;break}
  if(ok)m++} return m}
function madeList(){return DR.filter(function(x){
  return x[2].every(function(i){return !!owned[i]})})}

function buyRender(){
  lit(owned);
  var m=complete(), n=ownedN;
  countBox.querySelector('.big').innerHTML=n+' bottle'+(n==1?'':'s')
    +' &#8594; <em>'+m+'</em> of 143';
  countBox.querySelector('.lede').textContent = n===0
    ? 'Your shelf is empty. Tap any bottle to buy it, or let the page pick for you.'
    : m===0 ? 'Still nothing. A drink needs every one of its ingredients, not some of them.'
    : '__SHELF_LINE__';
  var made=madeList();
  panel.innerHTML='<h3>What you can make</h3><div class="sub">'+m+' OF THE 143</div><ul>'
    +(m?made.map(function(d){return '<li>'+d[0]+' <b>'+d[1]+'</b></li>'}).join('')
       :'<li style="opacity:.45;cursor:default">Nothing yet</li>')+'</ul>';
  panel.classList.add('show'); fade();
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

/* Selection is bound to pointerup, never to click: on iOS the first tap on a mark whose
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
  sheet.addEventListener('pointerleave',function(){if(mode==='read')clear()});
}
addEventListener('pointerup',function(){if(mode==='read')clear()});
addEventListener('keydown',function(e){
  if(e.key==='Escape'){if(mode==='buy')setMode('read');else clear()}});
</script></body></html>"""
