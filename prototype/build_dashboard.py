"""Builds dashboard.html: self-contained interactive board dashboard (aggregated data embedded)."""
import json, pandas as pd
d = pd.read_csv("duka_sales.csv", parse_dates=["order_date"]); d["revenue"] = d.quantity * d.unit_price
B = ["Nairobi","Mombasa","Nakuru","Kisumu","Eldoret"]; Ch = ["In-store","Online","Phone order"]; P = ["Laptop","Tablet","Phone","Headphones","Charger"]
g = d.groupby([d.order_date.dt.month-1, d.branch.map(B.index), d.channel.map(Ch.index), d["product"].map(P.index)]).agg(r=("revenue","sum"), o=("order_id","count")).reset_index()
g.columns = ["m","b","c","p","r","o"]
rows = json.dumps(g.values.tolist(), separators=(",", ":"))
html = """<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Duka Electronics · H1 2026 dashboard</title>
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<style>
:root{--bg:#fff;--card:#f2f5f9;--ink:#1b2430;--mute:#5b6675;--bar:#b4bcc6;--hi:#1f5fbf;--line:#d9dee5;color-scheme:light dark;box-sizing:border-box;padding:env(safe-area-inset-top,0) 0 env(safe-area-inset-bottom,0)}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#10151c;--card:#1a222d;--ink:#eef2f7;--mute:#9aa6b6;--bar:#4a5666;--hi:#6aa3ff;--line:#2a3442}}
:root[data-theme="dark"]{--bg:#10151c;--card:#1a222d;--ink:#eef2f7;--mute:#9aa6b6;--bar:#4a5666;--hi:#6aa3ff;--line:#2a3442}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.4 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
main{max-width:640px;margin:0 auto;padding:16px}h1{font-size:1.3rem;margin:0 0 2px}p.s{margin:0 0 14px;color:var(--mute);font-size:.85rem}
.f{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:12px}label{font-size:.72rem;color:var(--mute);display:block}
select,button{width:100%;font:inherit;font-size:.9rem;padding:8px;border:1px solid var(--line);border-radius:8px;background:var(--card);color:var(--ink)}
.k{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-bottom:8px}.k div{background:var(--card);border-radius:10px;padding:10px}
.k b{display:block;font-size:1.15rem;color:var(--hi)}.k span{font-size:.72rem;color:var(--mute)}
section{margin:18px 0}h2{font-size:1rem;margin:0 0 2px}h2+p{margin:0 0 8px;font-size:.78rem;color:var(--mute)}
.r{display:grid;grid-template-columns:84px 1fr 62px;align-items:center;gap:8px;margin:5px 0;font-size:.85rem;cursor:pointer;border:0;background:none;color:inherit;width:100%;text-align:left;padding:0}
.t{height:18px;background:transparent}.t i{display:block;height:100%;background:var(--bar);border-radius:3px;min-width:2px}.r.on .t i{background:var(--hi)}.r.on span:first-child{font-weight:700}
.r span:last-child{text-align:right;font-variant-numeric:tabular-nums}.m{display:flex;align-items:flex-end;gap:6px;height:130px;margin-top:4px}
.m div{flex:1;display:flex;flex-direction:column;justify-content:flex-end;align-items:center;height:100%;font-size:.72rem}.m i{display:block;width:100%;background:var(--bar);border-radius:3px 3px 0 0}.m .on i{background:var(--hi)}
.m small{color:var(--mute);margin-top:3px}.n{font-size:.75rem;color:var(--mute);border-top:1px solid var(--line);padding-top:10px}
</style></head><body><main>
<h1>Duka Electronics · H1 2026</h1><p class="s">Sales dashboard, 1 Jan–29 Jun 2026. Tap any bar or use the filters.</p>
<div class="f"><div><label for="fb">Branch</label><select id="fb"></select></div><div><label for="fc">Channel</label><select id="fc"></select></div>
<div><label for="fp">Product</label><select id="fp"></select></div><div><label for="fm">Months</label><select id="fm"></select></div></div>
<button id="rs" style="margin-bottom:12px">Reset filters</button>
<div class="k"><div><b id="k1"></b><span>revenue</span></div><div><b id="k2"></b><span>orders</span></div><div><b id="k3"></b><span>avg order</span></div></div>
<section><h2>Revenue by month</h2><p>KES millions, for the selected branch, channel and product</p><div class="m" id="cm"></div></section>
<section><h2>By branch</h2><p>Revenue, KES millions</p><div id="cb"></div></section>
<section><h2>By product</h2><p>Revenue, KES millions</p><div id="cp"></div></section>
<section><h2>By channel</h2><p>Revenue, KES millions</p><div id="cc"></div></section>
<p class="n">Revenue = quantity × unit price. Each bar ignores its own filter so you can compare alternatives. Branch-level and monthly differences rest on small order counts (see the orders tile), so treat them as signals, not proof.</p>
</main><script>
const D=__DATA__,N={b:__B__,c:__C__,p:__P__},M=["Jan","Feb","Mar","Apr","May","Jun"],S={b:-1,c:-1,p:-1,m:"0-5"};
const $=i=>document.getElementById(i),fm=v=>(v/1e6).toFixed(1);
function opts(id,arr,all){$(id).innerHTML="<option value='-1'>"+all+"</option>"+arr.map((x,i)=>"<option value='"+i+"'>"+x+"</option>").join("")}
opts("fb",N.b,"All branches");opts("fc",N.c,"All channels");opts("fp",N.p,"All products");
$("fm").innerHTML=[["0-5","Jan–Jun"],["0-2","Q1 (Jan–Mar)"],["3-5","Q2 (Apr–Jun)"]].concat(M.map((x,i)=>[i+"-"+i,x])).map(x=>"<option value='"+x[0]+"'>"+x[1]+"</option>").join("");
const ok=(r,skip)=>{const[a,z]=S.m.split("-").map(Number);return(skip=="m"||(r[0]>=a&&r[0]<=z))&&(skip=="b"||S.b<0||r[1]==S.b)&&(skip=="c"||S.c<0||r[2]==S.c)&&(skip=="p"||S.p<0||r[3]==S.p)};
function bars(id,key,idx){const t=Array(N[key].length).fill(0);D.filter(r=>ok(r,key)).forEach(r=>t[r[idx]]+=r[4]);const mx=Math.max(...t,1);
$(id).innerHTML=N[key].map((n,i)=>"<button class='r"+(S[key]==i?" on":"")+"' data-k='"+key+"' data-i='"+i+"'><span>"+n+"</span><span class='t'><i style='width:"+t[i]/mx*100+"%'></i></span><span>"+fm(t[i])+"</span></button>").join("")}
function render(){const x=D.filter(r=>ok(r)),rev=x.reduce((a,r)=>a+r[4],0),o=x.reduce((a,r)=>a+r[5],0);
$("k1").textContent="KES "+fm(rev)+"M";$("k2").textContent=o.toLocaleString();$("k3").textContent=o?"KES "+Math.round(rev/o/1e3)+"K":"–";
const t=Array(6).fill(0);D.filter(r=>ok(r,"m")).forEach(r=>t[r[0]]+=r[4]);const mx=Math.max(...t,1),[a,z]=S.m.split("-").map(Number);
$("cm").innerHTML=t.map((v,i)=>"<div class='"+(i>=a&&i<=z?"on":"")+"'>"+fm(v)+"<i style='height:"+v/mx*90+"px'></i><small>"+M[i]+"</small></div>").join("");
bars("cb","b",1);bars("cp","p",3);bars("cc","c",2)}
["b","c","p"].forEach(k=>$("f"+k).onchange=e=>{S[k]=+e.target.value;sync()});$("fm").onchange=e=>{S.m=e.target.value;sync()};
document.body.addEventListener("click",e=>{const b=e.target.closest(".r");if(b){const k=b.dataset.k,i=+b.dataset.i;S[k]=S[k]==i?-1:i;sync()}});
$("rs").onclick=()=>{S.b=S.c=S.p=-1;S.m="0-5";sync()};
function sync(){$("fb").value=S.b;$("fc").value=S.c;$("fp").value=S.p;$("fm").value=S.m;render()}sync();
</script></body></html>"""
html = html.replace("__DATA__", rows).replace("__B__", json.dumps(B)).replace("__C__", json.dumps(Ch)).replace("__P__", json.dumps(P))
open("prototype/dashboard.html", "w", encoding="utf-8").write(html); print(len(html), "bytes;", len(g), "aggregate rows")
