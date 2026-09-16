#!/usr/bin/env python3
"""Rick & Linda 東京5泊(10/3-8)の過ごし方3択ページ。 python3 build.py -> index.html
事実は 2026-09-17 に公式サイトで確認したもののみ。未確認のことは書かない（価格・営業日）。"""
import json, html

PH = json.load(open('photos.json'))
gm = lambda q: 'https://www.google.com/maps/search/?api=1&query=' + q.replace(' ', '+')
emb = lambda q: 'https://maps.google.com/maps?q=' + q.replace(' ', '+') + '&output=embed&z=15'
def route_emb(stops):
    s = [x.replace(' ', '+') for x in stops]
    return 'https://maps.google.com/maps?saddr=' + s[0] + '&daddr=' + '+to:'.join(s[1:]) + '&output=embed'
def route_link(stops):
    s = [x.replace(' ', '+') for x in stops]
    return ('https://www.google.com/maps/dir/?api=1&origin=' + s[0] + '&destination=' + s[-1]
            + ('&waypoints=' + '%7C'.join(s[1:-1]) if len(s) > 2 else '') + '&travelmode=transit')

COURSES = [
 dict(id='A', name='Edo and Hokusai', tag='Course A · Ryogoku, across the river', best='Tuesday or Wednesday',
  why='One train ride east, into the old low city. A museum that rebuilds Edo at full size, a sumo neighbourhood for lunch, a small garden, and Hokusai at the end.',
  steps=[('09:45','Leave the hotel','Shimbashi is 3 minutes on foot. Ryogoku is about 20 minutes by train.'),
         ('10:15','Edo-Tokyo Museum','Reopened in March 2026 after four years of rebuilding. A full-size Nihonbashi bridge you walk across, Edo townhouses you step into, and the city model with thousands of small figures. 800 yen, 400 if you are 65 or over.'),
         ('12:15','Chanko lunch','The sumo stew, in the streets where the wrestlers live. Five minutes from the museum.'),
         ('13:30','Kyu-Yasuda Garden','Free, small, and empty on a weekday. A tidal pond garden from the 1690s.'),
         ('14:00','Sumida Hokusai Museum','Hokusai was born in this neighbourhood. 400 yen, 300 if you are 65 or over. The audio guide is 500 yen and runs on your own phone, so bring earphones.'),
         ('15:45','Back to Ginza','Or ten more minutes east to Tokyo Skytree if you still have legs.')],
  stops=['Edo-Tokyo Museum','Chanko Dojo Ryogoku','Kyu-Yasuda Garden','Sumida Hokusai Museum'],
  moves='Hotel to Ryogoku about 20 minutes by train (Toei Oedo line from Shiodome, or JR from Shimbashi via Akihabara). Everything in Ryogoku is within a 10-minute walk of everything else.',
  food=[('Chanko Dojo Ryogoku-ekimae','Ryogoku · chanko nabe','The sumo hot pot. Lunch 11:30 to 14:30, small pot set from 1,000 yen, the full Ryogoku chanko set 1,700 yen.','Chanko Dojo Ryogoku Ekimae'),
        ('Chanko Kirishima Ryogoku','Ryogoku · chanko nabe','Run by a former ozeki. Lunch is weekdays only and they close on Mondays, so this one works on Tuesday or Wednesday.','Chanko Kirishima Ryogoku')],
  good='Museums, and seeing what Edo actually looked like before it became Tokyo. Mostly indoors, so rain does not matter.',
  mind='Both museums close on Mondays. The Sumida river boats from Ryogoku are suspended at the moment, so we use the train, not the water.',
  links=[('Edo-Tokyo Museum','https://www.edo-tokyo-museum.or.jp/en/'),
         ('Sumida Hokusai Museum','https://hokusai-museum.jp/?lang=en'),
         ('Kyu-Yasuda Garden','https://www.city.sumida.lg.jp/sisetu_info/kouen/kunai_park_annai/sumida_park/park08.html')]),

 dict(id='B', name='A day with your hands', tag='Course B · Tsukiji and Ginza', best='Tuesday for the market, either day for the classes',
  why='The ink painting and the tea ceremony from your list, both close to the hotel. You paint in the morning, eat in Tsukiji, and sit down to tea in the afternoon a minute from the Kabukiza.',
  steps=[('09:30','Tsukiji outer market','15 minutes on foot from the hotel. The selling hours are 9:00 to 14:00. Tuesday is an open day; Wednesday is a market holiday and many shops stay shut.'),
         ('11:00','Sumi-e ink painting','One hour in a teahouse on the second street of Tsukiji, with an English-speaking teacher, eight people at most. You take your paper home.'),
         ('12:30','Lunch in Tsukiji','Tamagoyaki, grilled fish, sushi at a counter. See the picks below.'),
         ('15:00','Tea ceremony, Chazen Ginza','45 minutes, in English, right beside the Kabukiza. 3,500 yen each in a shared room, 5,000 yen each if we take the room privately. On the hour, 10:00 to 17:00, open every day.'),
         ('16:00','Walk back','12 minutes to the hotel, through the back streets of Ginza rather than the main avenue.'),
         ('18:00','Optional: a whisky bar','Bar Doulton in Ginza 6-chome, over a thousand bottles, weekdays 18:00 to midnight. Closed on Sundays.')],
  stops=['Tsukiji Outer Market','Chazen Ginza','Hotel The Celestine Ginza'],
  moves='All of it on foot. Hotel to Tsukiji 15 minutes, Tsukiji to the tea room 10 minutes, tea room to hotel 12 minutes.',
  food=[('Tsukiji outer market','Tsukiji · breakfast and lunch','Eat standing up from the stalls: tamagoyaki, grilled scallops, uni. Selling hours 9:00 to 14:00, and Wednesday is a market holiday.','Tsukiji Outer Market'),
        ('Chazen Ginza','Ginza · tea ceremony','Not food, but the 45 minutes is the point. Next door to the theatre, English, chairs can be arranged if kneeling is not for you.','Chazen Ginza')],
  good='You leave with something you made, and the tea room is one minute from the theatre you are already visiting on Sunday.',
  mind='Both classes are by reservation and I book them, so tell me the day. The ink painting studio in Aoyama I also looked at only runs Friday to Monday, which is why I put the Tsukiji one here.',
  links=[('Sumi-e workshop in a Tsukiji teahouse','https://www.tripadvisor.com/AttractionProductReview-g1066444-d29613388-Sumi_e_Ink_Painting_Suiboku_Ga_Workshop_in_a_Japanese_Teahouse-Chuo_Tokyo_Tokyo_P.html'),
         ('Chazen Ginza','https://teaceremony-tokyo.jp/ginza/'),
         ('Tsukiji outer market','https://www.tsukiji.or.jp/english/'),
         ('Bar Doulton','https://www.ginza-bar-doulton.com/')]),

 dict(id='C', name='Ginza at your own pace', tag='Course C · No trains at all', best='Sunday afternoon after the kabuki, or Wednesday',
  why='A garden by the water, matcha in a teahouse on an island, and the shops of Ginza. Everything inside a 20-minute walk of your room, so you can stop whenever you like.',
  steps=[('09:30','Hamarikyu Garden','A shogun duck-hunting garden with a tidal pond, 15 to 18 minutes on foot from the hotel. 300 yen, 150 if you are 65 or over. Open 9:00 to 17:00.'),
         ('10:30','Matcha on the island','The teahouse in the middle of the pond serves matcha with a sweet. You sit on tatami with the skyline behind the pines.'),
         ('12:00','Lunch in Ginza','Walk back up into the city and pick a floor of a department store, or a counter in a side street.'),
         ('14:00','Ginza on foot','Itoya for paper and pens, the food halls in the basements, Mitsukoshi and Wako on the corner.'),
         ('16:00','Kabukiza without a ticket','The basement floor under the theatre is open to anyone: sweets, fans, prints, a coffee shop. The roof garden on the fifth floor is free as well.'),
         ('17:00','Back at the hotel','Twelve minutes from the theatre, and you are already home.')],
  stops=['Hamarikyu Garden','Ginza Itoya','Kabuki-za Tokyo','Hotel The Celestine Ginza'],
  moves='All on foot. Hotel to Hamarikyu 15 to 18 minutes, Hamarikyu to Ginza 15 minutes, Ginza to the Kabukiza 8 minutes, Kabukiza to the hotel 12 minutes.',
  food=[('Nakajima no Ochaya, Hamarikyu','Hamarikyu · matcha','The teahouse on the island. Matcha with a seasonal sweet, prices on the day.','Nakajima no Ochaya Hamarikyu'),
        ('Ginza Itoya','Ginza · paper and pens','Twelve floors of stationery, with a cafe near the top. Good for presents.','Ginza Itoya')],
  good='A slow day with no train, no timetable, and a bench whenever you want one.',
  mind='On Sunday 4 October the main avenue of Ginza is closed to cars from 12:00 to 17:00, which is why this course fits the afternoon after the kabuki. The garden has free English volunteer guides at 11:00, but only at weekends.',
  links=[('Hamarikyu Garden','https://www.tokyo-park.or.jp/teien/en/hama-rikyu/'),
         ('Kabukiza, Kobikicho Square','https://www.kabuki-za.co.jp/guide/kobikihiroba.html'),
         ('Ginza Itoya','https://www.ito-ya.co.jp/ginza/en/')]),
]

def detail(c):
    ph = ''.join(f'<img src="{x["thumb"]}" alt="{html.escape(x["title"])}" loading="lazy">'
                 for x in [PH[c['id']]['card']] + PH[c['id']]['detail'])
    st = ''.join(f'<li><b>{t}</b><div><strong>{h}</strong><span>{d}</span></div></li>' for t, h, d in c['steps'])
    fd = ''.join(f'<a class="eat" href="{gm(q)}" target="_blank" rel="noopener">'
                 f'<span class="eb"><strong>{n}</strong><em>{a}</em><span>{d}</span>'
                 f'<i>Open in Google Maps ↗</i></span></a>' for (n, a, d, q) in c['food'])
    ln = ' '.join(f'<a href="{u}" target="_blank" rel="noopener">{html.escape(t)} ↗</a>' for t, u in c['links'])
    return f'''<section class="detail" id="course-{c['id']}"><div class="dwrap"><div class="dtop"></div>
<div class="dhead"><div><p class="kicker">{html.escape(c['tag'])}</p><h2><span class="badge">{c['id']}</span>{html.escape(c['name'])}</h2></div></div>
<p class="why">{html.escape(c['why'])}</p>
<div class="photos">{ph}</div>
<div class="dgrid">
<div><h3>The day</h3><ol class="steps">{st}</ol></div>
<div><h3>The route</h3><div class="mapbox"><iframe src="{route_emb(c['stops'])}" loading="lazy" title="Route for course {c['id']}" referrerpolicy="no-referrer-when-downgrade"></iframe></div>
<p class="moves">{c['moves']} <a href="{route_link(c['stops'])}" target="_blank" rel="noopener">Open the route in Google Maps ↗</a></p></div>
</div>
<h3>Where we stop</h3><div class="eats">{fd}</div>
<div class="notes"><p><b>Good for</b> {html.escape(c['good'])}</p><p><b>Keep in mind</b> {html.escape(c['mind'])}</p>
<p><b>Best day</b> {html.escape(c['best'])}</p></div>
<p class="links">{ln}</p>
</div></section>'''

HERO_CSS = """
.hpic{position:relative;background:#111;color:#fff}
.slides{position:absolute;inset:0;overflow:hidden}
.slides img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:0;transform:scale(1.06);transition:opacity 1.1s ease,transform 5s linear}
.slides img.on{opacity:1;transform:scale(1)}
.slides:after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.08) 30%,rgba(0,0,0,.74))}
.hcap{position:relative;z-index:1;min-height:62vh;max-height:600px;display:flex;flex-direction:column;justify-content:flex-end;padding-top:48px;padding-bottom:22px}
.hcap .kicker{color:#f0c9a0}
.fixed{position:relative;z-index:1;display:inline-block;align-self:flex-start;font-size:13.5px;font-weight:600;color:#fff;background:rgba(0,0,0,.42);border:1px solid rgba(255,255,255,.45);border-radius:999px;padding:8px 15px;margin:0 0 14px;backdrop-filter:blur(6px);-webkit-backdrop-filter:blur(6px)}
.hcap h1{color:#fff;margin:0 0 14px;text-shadow:0 2px 14px rgba(0,0,0,.3)}
.snav{display:flex;align-items:center;gap:10px}
.dots{display:flex;gap:7px;flex:none}
.dots button{width:9px;height:9px;padding:0;border:none;border-radius:50%;background:rgba(255,255,255,.45);cursor:pointer}
.dots button.on{background:#fff}
.hbody{padding-top:22px;padding-bottom:26px}
@media(prefers-reduced-motion:reduce){.slides img{transition:none;transform:none}}
"""
HERO_JS = """
 (function(){
  var sl=[].slice.call(document.querySelectorAll('.slides img')),dots=[].slice.call(document.querySelectorAll('.dots button')),i=0,t;
  function show(n){i=n;sl.forEach(function(x,k){x.classList.toggle('on',k===n)});dots.forEach(function(x,k){x.classList.toggle('on',k===n)})}
  function go(){clearInterval(t);if(!matchMedia('(prefers-reduced-motion: reduce)').matches)t=setInterval(function(){show((i+1)%sl.length)},4500)}
  dots.forEach(function(d,k){d.addEventListener('click',function(){show(k);go()})});
  show(0);go();
 })();
"""

credits = '; '.join(html.escape(x['title'].replace('File:', '')) + ' (' + x['lic'] + ')'
                    for x in PH['hero'] + [y for k in 'ABC' for y in [PH[k]['card']] + PH[k]['detail']])

page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Your Tokyo days: October 4 to 7</title><meta name="robots" content="noindex">
<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
:root{{--bg:#fffdf6;--card:#fff;--ink:#111;--mute:#767065;--line:#eae4d6;--acc:#9a2b22;--r:10px}}
*{{box-sizing:border-box;min-width:0}} html,body{{overflow-x:hidden;max-width:100%}} img{{max-width:100%}}
body{{margin:0;font-family:Inter,-apple-system,"Hiragino Sans",sans-serif;color:var(--ink);background:var(--bg);line-height:1.6}}
.wrap{{max-width:1080px;margin:0 auto;padding:0 20px}}
.kicker{{font-size:12px;font-weight:600;letter-spacing:.12em;text-transform:uppercase;color:var(--acc);margin:0 0 10px}}
h1,h2{{text-wrap:balance}} .nb{{white-space:nowrap}}
h1{{font-weight:800;font-size:clamp(34px,5.4vw,54px);line-height:1.06;letter-spacing:-.025em;margin:0 0 16px}}
h2{{font-weight:800;font-size:clamp(28px,4.2vw,42px);line-height:1.06;letter-spacing:-.025em;margin:0;display:flex;align-items:center;gap:12px}}
.badge{{display:inline-flex;align-items:center;justify-content:center;width:44px;height:44px;flex:none;border-radius:50%;background:var(--acc);color:#fff;font-size:22px;line-height:1}}
h3{{font-size:12px;font-weight:600;letter-spacing:.12em;text-transform:uppercase;color:var(--acc);margin:0 0 12px}}
{HERO_CSS}
header p{{font-size:18px;color:var(--mute);margin:0;max-width:640px}}
.facts{{display:flex;flex-wrap:wrap;gap:6px 20px;margin:20px 0 0;padding:0;list-style:none;font-size:14px;color:var(--mute)}} .facts b{{color:var(--ink);font-weight:600}}
.sechead{{display:flex;align-items:baseline;gap:14px;padding:26px 0 16px;border-top:1px solid var(--line)}}
.sechead .n{{font-weight:800;font-size:26px;line-height:1;letter-spacing:-.02em;color:var(--acc)}}
.sechead b{{font-size:19px;font-weight:600}} .sechead span{{font-size:14px;color:var(--mute)}}
.detail{{margin:0 0 20px;position:relative}}
.dwrap{{background:var(--card);border:2px solid var(--ink);border-radius:var(--r);position:relative}}
.dtop{{height:5px;background:var(--acc)}}
.dwrap>*{{margin-left:26px;margin-right:26px}} .dwrap>.dtop{{margin:0}}
.dhead{{padding-top:26px}}
.why{{font-size:17px;color:var(--mute);margin:10px 0 20px;max-width:660px}}
.photos{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px;margin-bottom:26px}}
.photos img{{display:block;width:100%;aspect-ratio:4/3;object-fit:cover;border-radius:8px;background:#f0ebe0}}
.dgrid{{display:grid;grid-template-columns:1fr 1fr;gap:30px;margin-bottom:28px}}
.steps{{list-style:none;padding:0;margin:0;border-top:1px solid var(--line)}}
.steps li{{display:grid;grid-template-columns:60px minmax(0,1fr);gap:12px;padding:11px 0;border-bottom:1px solid var(--line)}}
.steps b{{font-variant-numeric:tabular-nums;color:var(--acc);font-weight:600;font-size:14px}} .steps strong{{display:block;font-weight:600;font-size:16px}} .steps span{{color:var(--mute);font-size:14px}}
.mapbox{{border-radius:8px;overflow:hidden;background:#f0ebe0}} .mapbox iframe{{display:block;width:100%;height:300px;border:0}}
.moves{{font-size:14px;color:var(--mute);margin:12px 0 0}} .moves a{{color:var(--ink);text-decoration:underline;text-underline-offset:3px;white-space:nowrap}}
.eats{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px;margin-bottom:26px}}
.eat{{display:flex;flex-direction:column;text-decoration:none;color:inherit;background:var(--bg);border:1px solid var(--line);border-radius:8px;overflow:hidden}}
.eb{{display:flex;flex-direction:column;flex:1;padding:14px 16px 16px}}
.eat:hover{{border-color:var(--ink)}}
.eat strong{{display:block;font-weight:700;font-size:18px;line-height:1.2;letter-spacing:-.015em}}
.eat em{{display:block;font-style:normal;font-size:11px;color:var(--acc);font-weight:600;letter-spacing:.08em;text-transform:uppercase;margin:5px 0 9px}}
.eb>span{{display:block;font-size:14px;color:var(--mute)}} .eat i{{display:block;font-style:normal;font-size:12px;margin-top:auto;padding-top:10px;text-decoration:underline;text-underline-offset:3px}}
.notes{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px;margin-bottom:20px;font-size:14px}} .notes p{{margin:0;padding:16px 18px;background:var(--bg);border:1px solid var(--line);border-radius:8px}} .notes b{{display:block;font-weight:600;margin-bottom:3px}}
.links{{margin:0 0 22px;font-size:14px;display:flex;flex-wrap:wrap;gap:6px 18px}} .links a{{color:var(--ink);text-decoration:underline;text-underline-offset:3px}}
.kab{{display:grid;grid-template-columns:1fr 1fr;gap:26px;align-items:start;padding-bottom:36px}}
.kab p{{margin:0 0 10px;font-size:16px}} .kab .hint{{color:var(--mute);font-size:15px}}
.tick{{list-style:none;margin:0 0 16px;padding:18px 20px;background:var(--card);border:2px solid var(--ink);border-radius:var(--r);font-size:15px}}
.tick li{{display:grid;grid-template-columns:130px minmax(0,1fr);gap:10px;padding:6px 0}}
.tick b{{color:var(--acc);font-weight:600;font-size:13px;letter-spacing:.04em;text-transform:uppercase}}
.tick li>span{{display:block}} .tick em{{font-style:italic}}
.kab .mapbox iframe{{height:280px}}
.choose{{padding:0 0 44px}}
.choose p{{font-size:16px;margin:0 0 10px;max-width:660px}}
footer.wrap{{padding:26px 20px 60px;font-size:13px;color:var(--mute);border-top:1px solid var(--line)}} footer p{{margin:0 0 6px}}
.cred summary{{cursor:pointer;font-size:12px;color:var(--mute);opacity:.75;list-style:none;display:inline-block;text-decoration:underline;text-underline-offset:3px}}
.cred summary::-webkit-details-marker{{display:none}} .cred p{{margin:8px 0 0;font-size:11.5px;line-height:1.6;opacity:.8}}
@media(max-width:820px){{
 .dgrid,.eats,.notes,.kab,.photos{{grid-template-columns:1fr}}
 .dwrap>*{{margin-left:18px;margin-right:18px}} .mapbox iframe{{height:230px}}
}}
@media(max-width:560px){{
 .wrap{{padding:0 18px}}
 .hcap{{min-height:58vh;padding-bottom:18px}} .hbody{{padding-top:18px;padding-bottom:22px}} .kicker{{margin-bottom:12px}}
 h1{{font-size:33px;line-height:1.08;letter-spacing:-.03em;margin-bottom:14px}}
 header p{{font-size:16px;line-height:1.55;max-width:none}}
 .facts{{display:grid;grid-template-columns:auto 1fr;gap:3px 10px;margin-top:16px;font-size:13px;line-height:1.5}}
 .facts li{{display:contents}} .facts b{{white-space:nowrap}}
 .sechead{{display:block;padding:22px 0 12px}}
 .sechead .n{{font-size:20px;margin-right:8px;display:inline}}
 .sechead b{{font-size:17px}} .sechead span{{display:block;font-size:13px;line-height:1.5;margin-top:2px}}
 h2{{font-size:25px;line-height:1.12;gap:10px}} .badge{{width:36px;height:36px;font-size:18px}}
 .dhead{{padding-top:20px}} .why{{font-size:15.5px;line-height:1.55;margin:8px 0 16px}}
 .dwrap>*{{margin-left:16px;margin-right:16px}}
 .photos{{gap:8px;margin-bottom:20px}} .photos img{{aspect-ratio:3/2}}
 h3{{margin:22px 0 10px}} .dgrid{{gap:0;margin-bottom:0}}
 .steps li{{grid-template-columns:52px minmax(0,1fr);gap:10px;padding:10px 0}}
 .steps strong{{font-size:15.5px}} .steps span{{font-size:13.5px;line-height:1.5}}
 .eats{{gap:10px;margin-bottom:20px}} .eb{{padding:12px 14px 14px}}
 .notes{{gap:10px;margin-bottom:16px}} .notes p{{padding:14px 16px;font-size:13.5px}}
 .links{{font-size:13.5px;gap:4px 14px;margin-bottom:18px}}
 .kab{{gap:16px;padding-bottom:30px}} .kab p{{font-size:15.5px;line-height:1.55}} .kab .hint{{font-size:14px}}
 .tick li{{grid-template-columns:1fr;gap:1px;padding:8px 0;border-bottom:1px solid var(--line)}}
 .mapbox iframe{{height:210px}}
 footer.wrap{{padding:20px 18px 44px;font-size:11.5px;line-height:1.55}}
}}
</style></head><body>
<header class="hero">
<div class="hpic"><div class="slides">{''.join(f'<img src="{x["thumb"]}" alt="{html.escape(x["title"])}">' for x in PH['hero'])}</div>
<div class="wrap hcap">
<p class="kicker">Tokyo · October 3 to 8 · Hotel The Celestine Ginza</p>
<h1>Five nights in Ginza, and <span class="nb">three ways</span> to spend them.</h1>
<p class="fixed">Kabuki is fixed: Sunday 4 October, 11:00. The tickets are in my hands.</p>
<div class="snav"><div class="dots">{''.join(f'<button type="button" aria-label="Photo {k+1}"></button>' for k in range(len(PH['hero'])))}</div></div>
</div></div>
<div class="wrap hbody">
<p>Sunday is the theatre and Monday is Disneyland, so Tuesday and Wednesday are yours. Here are three courses. Read them, pick two, and tell me which day you want each one.</p>
<ul class="facts"><li><b>Fixed</b> Sun 4 Oct, kabuki 11:00</li><li><b>Fixed</b> Mon 5 Oct, Disneyland</li><li><b>Open</b> Tue 6 and Wed 7 Oct</li><li><b>Fly home</b> Thu 8 Oct</li></ul>
</div>
</header>
<div class="wrap">
<div class="sechead"><span class="n">1</span><div><b>Sunday 4 October: the kabuki</b> <span>Kabukiza Theatre, Part 1. Everything you need for that morning.</span></div></div>
<div class="kab">
<div>
<ul class="tick">
<li><b>Programme</b><span>Part 1 of Kinshu October Grand Kabuki: <em>Koi-tsukami</em>, a fight with a giant carp and real water on stage, then the fox-Tadanobu act of <em>Yoshitsune Senbon Zakura</em>. Spectacle rather than dialogue, which is the right first kabuki.</span></li>
<li><b>Time</b><span>Starts 11:00, ends about 13:35. Doors open 30 minutes before.</span></li>
<li><b>Your seats</b><span>Premium, floor 1, row 4, seats 19 and 20. Four rows from the stage, near the centre.</span></li>
<li><b>The tickets</b><span>Paper only, no phone ticket, and the theatre does not post them abroad. I collect them and hand them to you: 10:30 at the front of the theatre, or at your hotel the evening before if you prefer.</span></li>
<li><b>English</b><span>A subtitle tablet, 1,500 yen, cash only, from the counter inside on the first floor. There is no English audio guide at this theatre, so the tablet is the one to get.</span></li>
<li><b>The interval</b><span>A bento eaten at your seat is part of the custom. Sold inside the theatre.</span></li>
<li><b>Manners</b><span>No photographs or recording during the performance. Applause when a famous actor appears and after the big tricks.</span></li>
<li><b>Afterwards</b><span>Ginza is 8 minutes on foot, and on Sundays its main avenue is closed to cars from 12:00 to 17:00. The floor under the theatre and the roof garden are free and need no ticket. Course C below is built for that afternoon.</span></li>
</ul>
</div>
<div><div class="mapbox"><iframe src="{emb('Kabuki-za Tokyo')}" loading="lazy" title="Kabukiza Theatre" referrerpolicy="no-referrer-when-downgrade"></iframe></div>
<p class="moves">The theatre is about 8 minutes on foot from your hotel, and Higashi-Ginza station is directly underneath it. <a href="{gm('Kabuki-za Tokyo')}" target="_blank" rel="noopener">Open in Google Maps ↗</a></p>
<p class="hint">If you would rather have the tickets the evening before, tell me a time and I will bring them to the hotel on Saturday 3 October.</p></div>
</div>
<div class="sechead"><span class="n">2</span><div><b>Tuesday and Wednesday: pick two</b> <span>Any course fits either day, with the notes at the end of each one.</span></div></div>
{''.join(detail(c) for c in COURSES)}
<div class="sechead"><span class="n">3</span><div><b>How to tell me</b> <span>One line on WhatsApp is enough.</span></div></div>
<div class="choose">
<p>Reply with a letter and a day, for example: <b>A on Tuesday, B on Wednesday</b>. If you want Course C on the Sunday afternoon after the theatre, say so and I will send you a short map for it.</p>
<p class="hint">Course B needs me to reserve the ink painting and the tea ceremony, so the sooner I know the day, the better the chance of the hour you want. Everything else needs no booking at all.</p>
<p class="hint">These are suggestions, not a schedule. You are five nights in one hotel with no bags to move, so a morning in the room is also a good answer.</p>
</div>
</div>
<footer class="wrap"><p>Opening hours, prices and market holidays checked on 17 September 2026 against the official sites. Prices are per person and can change; the market and some restaurants close on their own days.</p>
<p>Yuuki Ichihara · Tokyo</p>
<details class="cred"><summary>Photo credits</summary><p>{credits}, via Wikimedia Commons.</p></details></footer>
<script>
{HERO_JS}
</script>
{{DEVBAR}}</body></html>'''

open('index.html', 'w').write(page.replace('{DEVBAR}', ''))
open('preview.html', 'w').write(page.replace(
    '{DEVBAR}',
    '<script>window.DEVBAR_FORCE=1</script><script src="devbar.js?v=3"></script>'))
print('written', len(page), '-> index.html + preview.html')
