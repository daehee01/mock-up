#!/usr/bin/env python3
# 위신싸 랜딩 정적 페이지 빌더
# 데이터(PRODUCTS / EVENTS) → 코드별 페이지 생성:
#   products.html               전체 상품 + 검색
#   product/<code>/index.html   상품 상세 (히어로 없이 대표 이미지 우선) + Toss 결제 모달
#   events/<code>/index.html    프로모션관
# index.html / about.html 은 수기 유지 (브랜드 페이지).
import os, json
from urllib.parse import quote

ROOT = os.path.dirname(os.path.abspath(__file__))
VERSION = "4"  # style.css 캐시버스팅 — 디자인 변경 시 +1

# 탐나불린 공통 정보 (브랜드 단위 — 캐스크별 제품이 공유)
SHARED = {
    "region": "스페이사이드, 스코틀랜드",
    "producer": "Whyte & Mackay",
    "flag": "🥃",
    "foods": [("🧀", "숙성 치즈 · 견과"), ("🦪", "차가운 해산물"), ("🍫", "다크 초콜릿")],
    "pron_ko": "탐나불린", "pron_ipa": "tæmnəˈvuːlɪn",
    "quote": "게일어로 ‘언덕 위의 방앗간’.",
    "story": [
        "스코틀랜드 스페이사이드의 탐나불린 증류소는 <b>부드럽고 달콤한 싱글몰트</b> 스타일로 알려져 있습니다. 위스키를 처음 접하는 분도 편하게 즐길 수 있는 접근성이 강점입니다.",
        "같은 원액에서도 셰리 · 쇼비뇽 블랑 · 피노 누아 등 <b>캐스크 피니시</b>에 따라 전혀 다른 개성을 끌어냅니다. 한 브랜드 안에서 취향대로 고르는 재미가 있습니다.",
        "그중 셰리 캐스크는 글로벌 위스키 콘테스트에서 <b>4년 연속 골드 메달</b>을 받으며 품질을 인정받았습니다.",
    ],
    "strengths": [
        "글로벌 콘테스트 4년 연속 골드 — 검증된 품질",
        "달콤하고 부드러워 위스키 입문자도 부담 없이",
        "셰리 · 쇼비뇽 블랑 · 피노 누아 등 캐스크별 개성",
    ],
    "reviews": [
        "<b>입문용으로 강추.</b> 셰리 특유의 단맛이 부담스럽지 않고 깔끔해서 위스키 처음인 친구도 잘 마셨어요.",
        "하이볼로 말면 청량하고, 니트로 마시면 토피·견과 풍미가 살아나요. <b>가성비가 미쳤다.</b>",
        "선물했더니 라벨이 예쁘다고 좋아하더라고요. 맛도 무난해서 <b>실패 없는 선택.</b>",
    ],
}

# 제품별 ChatGPT 요약(캐스크별)
SUMMARIES = {
    "0001": "탐나불린은 스코틀랜드 스페이사이드의 싱글몰트예요. <b>부드럽고 달콤한 스타일</b>이라 위스키가 처음인 분도 거부감 없이 즐깁니다. 그중 셰리 캐스크는 <b>글로벌 콘테스트 4년 연속 골드</b>를 받은 탐나불린의 얼굴이에요.",
    "0002": "두 가지 캐스크의 균형감이 특징인 공식 라인업의 첫 위스키예요. <b>가성비·가심비</b>를 모두 잡아, 데일리로 부담 없이 즐기기 좋습니다.",
    "0003": "화이트와인(쇼비뇽 블랑) 캐스크로 마무리한 <b>여름용 싱글몰트</b>예요. 칠링하거나 하이볼로 즐기면 청량감이 한층 살아납니다.",
    "0004": "레드와인(피노 누아) 캐스크로 마무리한 <b>레어 보틀</b>이에요. 진한 로즈우드 컬러와 우아한 단맛이 매력입니다.",
}
DEFAULT_SUMMARY = SUMMARIES["0001"]
FONT = ('<link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin />\n'
        '<link rel="stylesheet" as="style" crossorigin '
        'href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css" />')

IMG = {
    "sherry": "https://cdn.veluga.kr/drinks/pv/31081.png",
    "double": "https://cdn.veluga.kr/drinks/pv/31253.png",
    "sb":     "https://cdn.veluga.kr/drinks/pv/31244.png",
    "pinot":  "https://cdn.veluga.kr/drinks/30879/pv/main/be6df03a84774220bdb94eac1f7089d5_%E1%84%90%E1%85%A1%E1%86%B7%E1%84%82%E1%85%A1%E1%84%87%E1%85%AE%E1%86%AF%E1%84%85%E1%85%B5%E1%86%AB_%E1%84%8C%E1%85%A5%E1%84%86%E1%85%A5%E1%86%AB_%E1%84%91%E1%85%B5%E1%84%82%E1%85%A9_%E1%84%82%E1%85%AE%E1%84%8B%E1%85%A1.png",
}

PRODUCTS = [
    {"code":"0001","name":"탐나불린 셰리 캐스크","img":IMG["sherry"],"now":"89,000원","was":"110,000","off":"19%",
     "vol":"700mL","abv":"40%","badge":"12병 남음","badge_kind":"","kicker":"위신싸 · <b>LIMITED DROP</b>",
     "limited":True,"qty_left":"12","qty_total":"30","dday":"D-3","promo":True,"promo_tag":"WEEKLY DROP · D-3",
     "search":"탐나불린 셰리 캐스크 스페이사이드 싱글몰트 한정",
     "why":"글로벌 위스키 콘테스트 4년 연속 골드. 달콤하고 부드러워 위스키가 처음인 분도 편하게 즐깁니다.",
     "aroma":"구운 빵 · 바닐라 · 생강 · 오렌지","palate":"천도복숭아 · 케이크 · 토피넛","finish":"과일 · 살구의 복합미",
     "inf":{"handle":"@위스키한모금","comment":"입문자도 거부감 없는 셰리. 이 가격에 이 퀄이면 무조건 쟁여두세요."}},

    {"code":"0002","name":"탐나불린 더블 캐스크","img":IMG["double"],"now":"59,000원","was":"","off":"",
     "vol":"700mL","abv":"40%","badge":"단독","badge_kind":"deal","kicker":"위신싸 · <b>단독 입점</b>",
     "limited":False,"promo":False,"search":"탐나불린 더블 캐스크 스페이사이드 싱글몰트 단독",
     "why":"가성비·가심비를 모두 잡은 공식 라인업의 첫 위스키. 두 캐스크의 균형감이 특징입니다.",
     "aroma":"사과 · 토피 · 마지팬 · 스파이스","palate":"배 · 복숭아 · 구운 파인애플","finish":"깔끔 · 스파이시 · 달콤"},

    {"code":"0003","name":"탐나불린 쇼비뇽 블랑","img":IMG["sb"],"now":"72,000원","was":"","off":"",
     "vol":"700mL","abv":"40%","badge":"여름","badge_kind":"","kicker":"위신싸 · <b>여름 한정</b>",
     "limited":False,"promo":True,"promo_tag":"여름 시즌","search":"탐나불린 쇼비뇽 블랑 캐스크 화이트와인 여름",
     "why":"여름을 상징하는 화이트와인 캐스크 싱글몰트. 칠링하거나 얼려 마시면 청량감이 더 살아납니다.",
     "aroma":"청사과 · 파인애플 · 멜론 · 자스민","palate":"레몬 · 라임 · 사과파이","finish":"과일 · 크리미한 코코넛"},

    {"code":"0004","name":"탐나불린 피노 누아","img":IMG["pinot"],"now":"94,000원","was":"","off":"",
     "vol":"700mL","abv":"40%","badge":"한정","badge_kind":"","kicker":"위신싸 · <b>레어 캐스크</b>",
     "limited":True,"qty_left":"6","qty_total":"20","dday":"D-5","promo":True,"promo_tag":"LIMITED",
     "search":"탐나불린 저먼 피노 누아 캐스크 레드와인 한정 레어",
     "why":"피노 누아의 향이 피어오르는 레드와인 캐스크. 진한 로즈우드 컬러와 우아한 단맛이 특징입니다.",
     "aroma":"체리 · 사과파이","palate":"바닐라 · 무화과 · 터키쉬 딜라이트","finish":"복숭아 · 오렌지 · 감초"},

    {"code":"0005","name":"탐나불린 셰리 200mL","img":IMG["sherry"],"now":"29,000원","was":"","off":"",
     "vol":"200mL","abv":"40%","badge":"","badge_kind":"","kicker":"위신싸 · <b>미니어처</b>",
     "limited":False,"promo":False,"search":"탐나불린 셰리 캐스크 미니어처 200ml 입문",
     "why":"부담 없이 셰리 캐스크를 맛볼 수 있는 미니 사이즈. 선물이나 입문용으로 좋습니다.",
     "aroma":"구운 빵 · 바닐라 · 오렌지","palate":"천도복숭아 · 토피넛","finish":"과일 · 살구"},

    {"code":"0006","name":"탐나불린 기프트 세트","img":IMG["double"],"now":"69,000원","was":"","off":"",
     "vol":"700mL + 전용잔","abv":"40%","badge":"선물","badge_kind":"deal","kicker":"위신싸 · <b>기프트</b>",
     "limited":False,"promo":False,"search":"탐나불린 더블 캐스크 기프트 세트 선물 전용잔",
     "why":"탐나불린 더블 캐스크에 브랜드 전용잔을 더한 선물 세트. 위스키 입문 선물로 안성맞춤입니다.",
     "aroma":"사과 · 토피 · 마지팬","palate":"배 · 복숭아 · 흑설탕","finish":"깔끔 · 달콤"},

    {"code":"0007","name":"쇼비뇽 블랑 하이볼팩","img":IMG["sb"],"now":"79,000원","was":"","off":"",
     "vol":"700mL + 토닉","abv":"40%","badge":"여름","badge_kind":"","kicker":"위신싸 · <b>여름 패키지</b>",
     "limited":False,"promo":False,"search":"탐나불린 쇼비뇽 블랑 하이볼 패키지 토닉 분다버그 여름",
     "why":"쇼비뇽 블랑에 토닉을 더한 여름 하이볼 패키지. 집에서 바로 시그니처 하이볼을 만들 수 있어요.",
     "aroma":"청사과 · 파인애플 · 멜론","palate":"레몬 · 라임 · 진저","finish":"청량 · 코코넛"},

    {"code":"0008","name":"셰리·더블 2종 세트","img":IMG["sherry"],"now":"139,000원","was":"","off":"",
     "vol":"700mL x 2","abv":"40%","badge":"테이스팅","badge_kind":"deal","kicker":"위신싸 · <b>테이스팅 세트</b>",
     "limited":False,"promo":True,"promo_tag":"세트 할인","search":"탐나불린 셰리 더블 캐스크 2종 테이스팅 세트 비교",
     "why":"셰리와 더블 캐스크를 한 번에 비교 시음할 수 있는 2종 세트. 캐스크별 개성을 즐기기 좋습니다.",
     "aroma":"두 캐스크의 향을 한자리에","palate":"셰리의 달콤 · 더블의 균형","finish":"각기 다른 여운"},
]

EVENTS = [
    {"code":"0001","title":"위스키한모금 PICK 위크","period":"2026.06.09 – 06.15",
     "desc":"어디서도 쉽게 못 구하던 한정·단독 보틀을, 이번 주 위신싸에서만 특가로. 풀리면 끝납니다.",
     "products":["0001","0004","0003","0008"]},
]

PMAP = {p["code"]: p for p in PRODUCTS}


def header(base):
    return f'''  <header class="hdr">
    <a href="{base}index.html" class="logo mark">위신<b>싸</b></a>
    <nav class="nav">
      <a href="{base}products.html">전체상품</a>
      <a href="{base}events/0001/">프로모션관</a>
      <a href="{base}about.html">About</a>
      <a class="ico" href="{base}mypage.html" aria-label="마이페이지"><svg width="21" height="21" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="8" r="4"/><path d="M4 21c0-4 4-6 8-6s8 2 8 6"/></svg></a>
    </nav>
  </header>'''


def footer():
    return '''  <footer class="ft">
    <div class="fl mark">위신<b>싸</b></div>
    <div style="margin-bottom:4px;">위스키가 신발보다 싸다 — by 벨루가</div>
    <span class="age">19+ 청소년 보호</span>
    <div>주류는 만 19세 이상만 구매·픽업할 수 있습니다.</div>
    <div style="margin-top:10px;"><b>(주)벨루가</b> · 사업자/통신판매업/주류통신판매 승인 정보 (확정 후 기재)</div>
  </footer>'''


def price_html(p):
    out = ""
    if p.get("off"):
        out += f'<span class="off">{p["off"]}</span>'
    out += f'<span class="now">{p["now"]}</span>'
    if p.get("was"):
        out += f' <span class="was">{p["was"]}</span>'
    return out


def card(p, base):
    badge = ""
    if p.get("badge"):
        cls = "badge deal" if p.get("badge_kind") == "deal" else "badge"
        badge = f'<span class="{cls}">{p["badge"]}</span>'
    return f'''      <a class="prod" href="{base}product/{p['code']}/" data-name="{p['search']}">
        {badge}
        <img src="{p['img']}" alt="" />
        <div class="nm">{p['name']}</div>
        <div class="meta">{p['vol']} · {p['abv']}</div>
        <div class="price">{price_html(p)}</div>
      </a>'''


def page(title, body, base=""):
    return f'''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{title}</title>
{FONT}
<link rel="stylesheet" href="{base}style.css?v={VERSION}" />
</head>
<body>
<div class="wrap">
{body}
</div>
</body>
</html>
'''


# ---------- products.html ----------
def build_products():
    cards = "\n".join(card(p, "") for p in PRODUCTS)
    body = f'''{header("")}

  <div class="ptop">
    <h1>전체 상품</h1>
    <div class="cnt"><span id="count">{len(PRODUCTS)}</span>개 상품 · 지금 픽업 가능</div>
  </div>

  <div class="searchbar">
    <div class="searchbox">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#7a7a7a" stroke-width="2.2" stroke-linecap="round"><circle cx="11" cy="11" r="7"/><path d="M21 21l-4.3-4.3"/></svg>
      <input id="q" type="text" placeholder="상품명·증류소·캐스크 검색" autocomplete="off" />
    </div>
  </div>

  <div class="grid" id="grid">
{cards}
  </div>
  <div class="empty" id="empty">검색 결과가 없어요.</div>

{footer()}

  <script>
    var q=document.getElementById('q'),cards=[].slice.call(document.querySelectorAll('#grid .prod')),
        countEl=document.getElementById('count'),emptyEl=document.getElementById('empty');
    function norm(s){{return (s||'').toLowerCase().replace(/\\s+/g,'');}}
    q.addEventListener('input',function(){{
      var t=norm(q.value),n=0;
      cards.forEach(function(c){{
        var hay=norm(c.getAttribute('data-name')+' '+c.querySelector('.nm').textContent);
        var m=t===''||hay.indexOf(t)!==-1; c.style.display=m?'':'none'; if(m)n++;
      }});
      countEl.textContent=n; emptyEl.style.display=n===0?'block':'none';
    }});
  </script>'''
    return page("위신싸 — 전체 상품", body, base="")


# ---------- product/<code>/index.html ----------
PAY_SCRIPT = '''  <script>
    function openPay(){ document.getElementById('payModal').classList.add('open'); document.body.style.overflow='hidden'; }
    function closePay(){ document.getElementById('payModal').classList.remove('open'); document.body.style.overflow=''; }
    function payDemo(){ alert('결제는 데모입니다. 실제 연동 시 토스페이먼츠 결제위젯 SDK로 대체됩니다.'); closePay(); }
    function naverSearch(){
      var v=(document.getElementById('storeq').value||'').trim();
      var q=encodeURIComponent((v?v+' ':'')+'위신싸 픽업 주류');
      window.open('https://map.naver.com/p/search/'+q,'_blank');
    }
    document.addEventListener('change',function(e){
      if(e.target.id==='agreeAll'){ document.querySelectorAll('.agsub').forEach(function(c){c.checked=e.target.checked;}); }
      if(e.target.classList.contains('agsub')){
        var all=document.querySelectorAll('.agsub'),on=document.querySelectorAll('.agsub:checked');
        document.getElementById('agreeAll').checked=all.length===on.length;
      }
    });
    document.addEventListener('keydown',function(e){ if(e.key==='Escape') closePay(); });
  </script>'''


def pay_modal(p):
    return f'''<div class="pay-overlay" id="payModal" onclick="if(event.target===this)closePay()">
  <div class="pay-sheet" role="dialog" aria-modal="true" aria-label="결제하기">
    <div class="pay-grab"></div>
    <div class="pay-head"><span>주문 / 결제</span><button class="pay-x" onclick="closePay()" aria-label="닫기">✕</button></div>
    <div class="pay-scroll">
      <div class="pay-order">
        <img src="{p['img']}" alt="" />
        <div class="pay-order-info"><div class="t">{p['name']}</div><div class="d">위신싸 픽업 · 강남점</div></div>
        <div class="pay-order-amt">{p['now']}</div>
      </div>
      <div class="pay-sec">결제 수단</div>
      <div class="pay-easy">
        <button class="easy sel"><span class="tosspay">toss pay</span></button>
        <button class="easy"><span style="color:#03c75a;font-weight:800;">N</span> Pay</button>
        <button class="easy"><span style="color:#ffcd00;font-weight:900;">kakao</span> pay</button>
      </div>
      <div class="pay-methods">
        <label class="pm"><input type="radio" name="pm" /><span>신용 · 체크카드</span></label>
        <label class="pm"><input type="radio" name="pm" /><span>계좌이체</span></label>
        <label class="pm"><input type="radio" name="pm" /><span>가상계좌</span></label>
        <label class="pm"><input type="radio" name="pm" /><span>휴대폰</span></label>
      </div>
      <label class="pay-agree-all"><input type="checkbox" id="agreeAll" /><span>전체 동의하기</span></label>
      <div class="pay-agree-sub">
        <label><input type="checkbox" class="agsub" /><span>(필수) 결제 서비스 이용약관, 개인정보 처리 동의</span><i>›</i></label>
        <label><input type="checkbox" class="agsub" /><span>(필수) 만 19세 이상이며 본인이 픽업합니다</span><i>›</i></label>
      </div>
    </div>
    <div class="pay-foot"><button class="pay-cta" onclick="payDemo()">{p['now']} 결제하기</button></div>
  </div>
</div>'''


def build_product(p):
    base = "../../"
    statbar = ""
    if p.get("limited"):
        statbar = f'''
  <div class="statbar">
    <div class="s"><div class="l">남은 수량</div><div class="v"><b>{p['qty_left']}</b> / {p['qty_total']}병</div></div>
    <div class="s"><div class="l">드롭 마감</div><div class="v">{p['dday']}</div></div>
  </div>'''
    inf = ""
    if p.get("inf"):
        inf = f'''
  <section class="sec sec--tight" style="padding-top:40px;">
    <div class="inf">
      <div class="ava">🥃</div>
      <div>
        <div class="who"><span>{p['inf']['handle']}</span> 님이 함께 고른 보틀</div>
        <div class="cmt">"{p['inf']['comment']}"</div>
      </div>
    </div>
  </section>'''
    others = [q for q in PRODUCTS if q["code"] != p["code"]][:4]
    cross = "\n".join(card(q, base) for q in others)
    foods_html = "".join(f'<div class="food"><div class="ic">{i}</div><div class="t">{t}</div></div>' for i, t in SHARED["foods"])
    story_html = "".join(f"<p>{para}</p>" for para in SHARED["story"])
    strengths_html = "".join(f'<div class="st"><span class="chk">✔</span><span>{s}</span></div>' for s in SHARED["strengths"])
    reviews_html = "\n    ".join(f'<div class="rv">{r}</div>' for r in SHARED["reviews"])
    summary = SUMMARIES.get(p["code"], DEFAULT_SUMMARY)
    stores = [("강남점", "서울 강남구 테헤란로 ··", "0.4km"),
              ("역삼점", "서울 강남구 논현로 ··", "0.9km"),
              ("선릉점", "서울 강남구 선릉로 ··", "1.3km")]
    stores_html = "\n    ".join(
        f'<a class="store" href="https://map.naver.com/p/search/{quote("위신싸 픽업 " + nm)}" target="_blank" rel="noopener">'
        f'<div><div class="nm">위신싸 픽업 · {nm}</div><div class="ad">{ad}</div></div><div class="dist">{d} ›</div></a>'
        for nm, ad, d in stores)
    body = f'''{header(base)}

  <!-- 대표 이미지 (히어로 없음 / 이미지 하단 구매버튼 없음) -->
  <section class="pdp-media"><img src="{p['img']}" alt="{p['name']}" /></section>
  <section class="pdp-info">
    <div class="pdp-kicker">{p['kicker']}</div>
    <h1 class="pdp-name">{p['name']}</h1>
    <div class="pdp-price">{price_html(p)}</div>
  </section>
{statbar}
{inf}

  <!-- 원산지 + ChatGPT 요약 -->
  <section class="sec sec--tight" style="padding-top:38px;">
    <div class="origin">
      <div>
        <div class="o"><span>🏞️</span><span>{SHARED['region']}</span></div>
        <div class="o"><span>🏛️</span><span>{SHARED['producer']}</span></div>
      </div>
      <div class="flag">{SHARED['flag']}</div>
    </div>
    <div class="gpt">
      <div class="gh"><span class="ico">🤖</span><span>ChatGPT로 요약했어요!</span></div>
      <div class="gt">{summary}</div>
    </div>
  </section>

  <!-- 테이스팅 노트 -->
  <section class="sec sec--tight">
    <div class="eyebrow">TASTING NOTES</div>
    <p class="lead">{p['why']}</p>
    <div class="chips">
      <span class="chip">싱글몰트 스카치</span>
      <span class="chip">스페이사이드</span>
      <span class="chip">{p['vol']} · {p['abv']}</span>
    </div>
    <div class="notes">
      <div class="row"><div class="k">AROMA</div><div>{p['aroma']}</div></div>
      <div class="row"><div class="k">PALATE</div><div>{p['palate']}</div></div>
      <div class="row"><div class="k">FINISH</div><div>{p['finish']}</div></div>
    </div>
  </section>

  <!-- 잘 어울리는 안주 -->
  <section class="sec sec--tight">
    <div class="h2" style="font-size:21px;">잘 어울리는 안주</div>
    <div class="foods">{foods_html}</div>
  </section>

  <!-- 브랜드 스토리 -->
  <section class="sec sec--parchment">
    <div class="eyebrow">THE STORY</div>
    <div class="pron">{SHARED['pron_ko']} <span class="ipa">: [ {SHARED['pron_ipa']} ]</span></div>
    <div class="quote">“{SHARED['quote']}”</div>
    <div class="story">{story_html}</div>
  </section>

  <!-- 이 위스키의 강점 -->
  <section class="sec sec--tight" style="padding-top:38px;">
    <div class="eyebrow">WHY TAMNAVULIN</div>
    <div class="h2" style="font-size:21px;margin-bottom:14px;">홈바·여름 메뉴에 두기 좋은 이유</div>
    <div class="strengths">{strengths_html}</div>
  </section>

  <!-- 픽업 3단계 -->
  <section class="sec sec--parchment">
    <div class="eyebrow">HOW IT WORKS</div>
    <div class="h2">집 근처에서 3분이면 픽업.</div>
    <div style="margin-top:8px;">
      <div class="step"><div class="n">1</div><div><div class="t">온라인으로 결제</div><div class="d">결제하면 픽업 코드가 발급됩니다.</div></div></div>
      <div class="step"><div class="n">2</div><div><div class="t">가까운 픽업 매장 선택</div><div class="d">내 주변 위신싸 매장 중 편한 곳을 고릅니다.</div></div></div>
      <div class="step"><div class="n">3</div><div><div class="t">방문해서 픽업 (성인인증)</div><div class="d">신분증 확인 후 보틀을 받아갑니다. 끝!</div></div></div>
    </div>
    <div class="law" style="margin-top:18px;">📌 <b>왜 배송이 아니라 픽업인가요?</b> 주류는 법적으로 온라인 배송이 불가합니다(전통주 제외). 온라인 결제 후 매장에서 받는 <b>스마트오더</b>가 합법적인 유일한 방법이에요.</div>
  </section>

  <!-- 픽업 매장 (네이버 지도 연결) -->
  <section class="sec sec--tight" style="padding-top:40px;">
    <div class="eyebrow">PICKUP STORES</div>
    <div class="h2">내 주변 픽업 매장.</div>
    <p class="lead">매장을 누르면 네이버 지도에서 위치를 확인할 수 있어요.</p>
    <div class="store-find">
      <input id="storeq" type="text" placeholder="동·지하철역으로 검색" />
      <button onclick="naverSearch()">검색</button>
    </div>
    {stores_html}
  </section>

  <!-- 구매 + 신뢰 -->
  <section class="sec sec--tight">
    <a href="#" class="btn btn-primary" style="margin-bottom:10px;" onclick="openPay();return false;">지금 구매하기 →</a>
    <a href="#" class="btn btn-ghost" style="margin-bottom:20px;">품절됐어요 · 재입고 알림 받기</a>
    <div class="trust-line">
      <span class="i">✅ <b>100% 정품</b></span>
      <span class="i">💸 <b>신발보다 싸게</b></span>
      <span class="i">🔞 <b>성인 픽업</b></span>
    </div>
  </section>

  <!-- 리뷰 -->
  <section class="sec sec--tight reviews">
    <div class="eyebrow">REVIEW</div>
    <div class="h2" style="font-size:21px;margin-bottom:14px;">🙂 마셔본 사람들 한 줄 평</div>
    {reviews_html}
  </section>

  <!-- 크로스셀 -->
  <section class="sec sec--tight">
    <div class="row-head"><div class="t">이 상품도 픽업 가능해요</div><a class="more" href="{base}products.html">전체 →</a></div>
    <div class="carousel">
{cross}
    </div>
  </section>

  <!-- FAQ -->
  <section class="sec faq sec--tight">
    <div class="eyebrow">FAQ</div>
    <details class="qa"><summary><span>픽업 기한이 있나요?</span></summary><p>결제 후 7일 이내 선택한 매장에서 픽업해 주세요. (드롭마다 상이)</p></details>
    <details class="qa"><summary><span>성인인증은 어떻게 하나요?</span></summary><p>픽업 시 신분증으로 만 19세 이상 본인 확인 후 수령합니다.</p></details>
    <details class="qa"><summary><span>배송은 정말 안 되나요?</span></summary><p>네. 위스키 등은 주류법상 온라인 배송이 불가하며 매장 픽업만 가능합니다.</p></details>
    <details class="qa"><summary><span>환불되나요?</span></summary><p>픽업 전 결제 취소가 가능합니다. (세부 정책 추후 확정)</p></details>
  </section>

{footer()}'''
    # 스티키 CTA + 모달은 .wrap 밖
    tail = f'''
<div class="cta-bar" id="pay">
  <div class="price"><div class="now">{p['now']}</div>{f'<div class="was">정가 {p["was"]}</div>' if p.get("was") else ''}</div>
  <a href="#" class="btn btn-primary" onclick="openPay();return false;">구매하기</a>
</div>

{pay_modal(p)}
{PAY_SCRIPT}'''
    html = page(p['name'] + " — 위신싸", body, base=base)
    # .wrap에 pad-cta 부여 + tail 삽입 (</body> 앞)
    html = html.replace('<div class="wrap">', '<div class="wrap pad-cta">')
    html = html.replace('</div>\n</body>', '</div>\n' + tail + '\n</body>')
    return html


# ---------- events/<code>/index.html ----------
def build_event(e):
    base = "../../"
    prods = [PMAP[c] for c in e["products"] if c in PMAP]
    cards = "\n".join(card(p, base) for p in prods)
    body = f'''{header(base)}

  <div class="ev-top">
    <div class="eyebrow eyebrow--amber">PROMOTION</div>
    <h1>{e['title']}</h1>
    <div class="period">{e['period']}</div>
    <div class="desc">{e['desc']}</div>
  </div>

  <div class="grid">
{cards}
  </div>

{footer()}'''
    return page(e['title'] + " — 위신싸 프로모션관", body, base=base)


def write(path, html):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True) if os.path.dirname(full) != ROOT else None
    with open(full, "w", encoding="utf-8") as f:
        f.write(html)
    print("  wrote", path)


def main():
    print("building 위신싸 pages…")
    write("products.html", build_products())
    for p in PRODUCTS:
        write(f"product/{p['code']}/index.html", build_product(p))
    for e in EVENTS:
        write(f"events/{e['code']}/index.html", build_event(e))
    print("done.")


if __name__ == "__main__":
    main()
