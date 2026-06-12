#!/usr/bin/env python3
# 벨루가 B2C 랜딩 v3 — 정적 페이지 빌더 (뼈대 v4)
#
# 컨셉: "인플루언서가 말아주는 익스클루시브 술 큐레이션 서비스(앱)"
#   - IA = 스포티파이: 큐레이터(인플루언서)=아티스트, PICK=트랙리스트,
#     홈(HOT·팔로우·추천 레일) / 상설할인 / 마이(라이브러리), 하단 탭바.
#   - 비주얼 = 루트 DESIGN.md(Apple 분석): Action Blue(#0066cc) 단일 액센트,
#     화이트/파치먼트 ↔ 니어블랙 타일 교차, 필 CTA, 헤어라인 카드(18px),
#     보틀 이미지에만 단일 드롭섀도, 타이트 자간, active scale(0.95).
#
# 상품: vel.kr(api.veluga.kr) 실데이터 — pv_id·상품명·용량·이미지 URL은
#   /drinks/pv/<id>/card/ 응답에서 가져와 전수 HTTP 200 검증함(추측 금지).
#   가격은 API 미제공(B2B 견적제)이라 시중가 수준의 "목업 가격"임.
# 인플루언서: 실명 채널 6곳 — 데모 목업 전용. 실서비스 전 초상권·계약 필수.
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
VERSION = "2"  # 캐시버스팅 — 디자인 변경 시 +1

FONT = ('<link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin />\n'
        '<link rel="stylesheet" as="style" crossorigin '
        'href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css" />')

# ---------------- PRODUCTS — vel.kr 실데이터 10종 (가격만 목업) ----------------
# img: /drinks/pv/<id>/card/ 응답의 main_image_url을 percent-encoding한 최종형.
# ※ CDN 한글 경로는 NFC/NFD가 파일별로 혼재(대부분 NFD) — 사람이 다시 타이핑하면
#   NFC로 정규화돼 404가 남. 반드시 API 응답 원문을 인코딩한 아래 문자열 그대로 쓸 것.
PRODUCTS = [
    {"pv":9215,"name":"글렌피딕 12년","vol":"700mL","abv":"40%",
     "img":"https://cdn.veluga.kr/files/supplier/undefined/drinks/1.%E1%84%8B%E1%85%B1%E1%86%AF%E1%84%85%E1%85%B5%E1%84%8B%E1%85%A5%E1%86%B7%E1%84%80%E1%85%B3%E1%84%85%E1%85%A2%E1%86%AB%E1%84%90%E1%85%B3_%E1%84%80%E1%85%B3%E1%86%AF%E1%84%85%E1%85%A6%E1%86%AB%E1%84%91%E1%85%B5%E1%84%83%E1%85%B5%E1%86%A812%E1%84%82%E1%85%A7%E1%86%AB.png",
     "now":"65,000원","was":"","off":"",
     "note":"세계에서 가장 많이 팔린 싱글몰트"},
    {"pv":9229,"name":"발베니 12년 더블 우드","vol":"700mL","abv":"40%",
     "img":"https://cdn.veluga.kr/files/supplier/undefined/drinks/13.%E1%84%8B%E1%85%B1%E1%86%AF%E1%84%85%E1%85%B5%E1%84%8B%E1%85%A5%E1%86%B7%E1%84%80%E1%85%B3%E1%84%85%E1%85%A2%E1%86%AB%E1%84%90%E1%85%B3_%E1%84%87%E1%85%A1%E1%86%AF%E1%84%87%E1%85%A6%E1%84%82%E1%85%B512%E1%84%82%E1%85%A7%E1%86%AB%E1%84%83%E1%85%A5%E1%84%87%E1%85%B3%E1%86%AF%E1%84%8B%E1%85%AE%E1%84%83%E1%85%B3.png",
     "now":"128,000원","was":"","off":"",
     "note":"꿀·바닐라 — 데이트 위스키의 대명사"},
    {"pv":19904,"name":"맥캘란 12년 셰리 오크","vol":"700mL","abv":"40%",
     "img":"https://cdn.veluga.kr/files/supplier/217/drinks/%EB%A7%A5%EC%BA%98%EB%9E%80_12%EB%85%84_%EC%85%B0%EB%A6%AC_%EC%98%A4%ED%81%AC_The_Macallan_12yo_Sherry_Oak_%EB%94%94%EC%95%A4%ED%94%BC%EC%8A%A4%ED%94%BC%EB%A6%AC%EC%B8%A0.png",
     "now":"158,000원","was":"","off":"",
     "note":"셰리 캐스크의 교과서"},
    {"pv":2962,"name":"글렌알라키 12년","vol":"700mL","abv":"46%",
     "img":"https://assets.business.veluga.kr/media/public/GlenAllachie_12Y.png",
     "now":"119,000원","was":"","off":"",
     "note":"빌리 워커의 역작 — 셰리 폭탄"},
    {"pv":5229,"name":"더 글렌리벳 12년","vol":"700mL","abv":"40%",
     "img":"https://cdn.veluga.kr/files/supplier/undefined/drinks/4._%E1%84%91%E1%85%A6%E1%84%85%E1%85%B3%E1%84%82%E1%85%A9%E1%84%85%E1%85%B5%E1%84%8F%E1%85%A1%E1%84%8F%E1%85%A9%E1%84%85%E1%85%B5%E1%84%8B%E1%85%A1_%E1%84%83%E1%85%A5_%E1%84%80%E1%85%B3%E1%86%AF%E1%84%85%E1%85%A6%E1%86%AB%E1%84%85%E1%85%B5%E1%84%87%E1%85%A6%E1%86%BA_12%E1%84%82%E1%85%A7%E1%86%AB.png",
     "now":"69,000원","was":"","off":"",
     "note":"싱글몰트 입문의 정석"},
    {"pv":8019,"name":"라프로익 10년","vol":"750mL","abv":"43%",
     "img":"https://cdn.veluga.kr/files/supplier/undefined/drinks/7.%E1%84%87%E1%85%B5%E1%86%B7%E1%84%89%E1%85%A1%E1%86%AB%E1%84%90%E1%85%A9%E1%84%85%E1%85%B5_%E1%84%85%E1%85%A1%E1%84%91%E1%85%B3%E1%84%85%E1%85%A9%E1%84%8B%E1%85%B5%E1%86%A8-10%E1%84%82%E1%85%A7%E1%86%AB.png",
     "now":"98,000원","was":"","off":"",
     "note":"아일라 피트 — 호불호의 왕"},
    {"pv":3194,"name":"와일드 터키 101","vol":"750mL","abv":"50.5%",
     "img":"https://assets.business.veluga.kr/media/public/Wild_Turkey_101.png",
     "now":"52,000원","was":"","off":"",
     "note":"하이 프루프 버번의 기준점"},
    {"pv":3304,"name":"버팔로 트레이스","vol":"750mL","abv":"45%",
     "img":"https://stage-cdn.veluga.kr/files/supplier/97/package_variation/3304.png",
     "now":"45,000원","was":"","off":"",
     "note":"가성비 버번 1순위"},
    {"pv":5390,"name":"산토리 가쿠빈","vol":"700mL","abv":"40%",
     "img":"https://cdn.veluga.kr/files/supplier/undefined/drinks/134.%E1%84%87%E1%85%B5%E1%86%B7%E1%84%89%E1%85%A1%E1%86%AB%E1%84%90%E1%85%A9%E1%84%85%E1%85%B5_%E1%84%80%E1%85%A1%E1%84%8F%E1%85%AE%E1%84%87%E1%85%B5%E1%86%AB.png",
     "now":"38,000원","was":"","off":"",
     "note":"하이볼의 원조 — 가쿠하이볼"},
    {"pv":31081,"name":"탐나불린 셰리 캐스크","vol":"700mL","abv":"40%",
     "img":"https://cdn.veluga.kr/drinks/pv/31081.png",
     "now":"89,000원","was":"","off":"",
     "note":"벨루가 단독 소싱 스페이사이드"},
]
PMAP = {p["pv"]: p for p in PRODUCTS}

# 상설 할인(떨이) — 동일 상품에 떨이 가격·사유만 오버라이드
SALE = [
    {"pv":3304,"now":"34,900원","was":"45,000","off":"22%","reason":"과잉 재고 정리"},
    {"pv":5390,"now":"29,900원","was":"38,000","off":"21%","reason":"하이볼 시즌 물량"},
    {"pv":5229,"now":"54,900원","was":"69,000","off":"20%","reason":"라벨 변경 전 재고"},
]

# ---------------- INFLUENCERS — 1급 객체 (hot: 메인 HOT 레일 노출) ----------------
# 실명 채널 — 데모 목업 전용(소개·코멘트·팔로워 수 전부 가상). 실서비스 전 계약 필수.
INFLUENCERS = [
    {"code":"chimchakman","handle":"@침착맨","name":"침착맨","hot":True,
     "ava":"🧀","col":"#3a3a3c","tags":["편안한 술","예능"],"followers":"285만",
     "oneliner":"술은 편하게 마시는 게 제일 맛있습니다.",
     "bio":"설명이 필요 없는 그 분. 어려운 위스키 용어 없이 '그냥 맛있는 술'을 골라드립니다. "
           "침착하게 한 잔, 부담 없이 한 잔.",
     "comment":"비싼 술이 꼭 맛있는 건 아니에요. 근데 맛있는 술이 가끔 비싸긴 합니다. "
               "오늘은 안 비싸고 맛있는 걸로 가져왔어요.",
     "picks":[
        (5390,"하이볼 만들어 먹으면 치킨이 두 마리 됩니다."),
        (3194,"이름이 와일드 터키인데 맛은 순합니다. 사람도 그런 사람 있잖아요."),
        (9215,"제일 많이 팔렸다는 건 제일 덜 망한다는 뜻입니다."),
     ]},
    {"code":"ppanibottle","handle":"@빠니보틀","name":"빠니보틀","hot":True,
     "ava":"🎒","col":"#8a5a2b","tags":["여행","로컬 술"],"followers":"198만",
     "oneliner":"현지에서 마셔본 술만 추천합니다.",
     "bio":"전 세계를 떠돌며 그 동네 술을 마셔온 여행 유튜버. 스코틀랜드 증류소부터 "
           "켄터키 버번 트레일, 도쿄 골목 하이볼 바까지 — 현지에서 직접 마셔본 술만 픽합니다.",
     "comment":"아일라 섬에서 라프로익 마시고 '이게 뭐야' 했는데, 한국 와서 또 찾게 되더라고요. "
               "여행은 술맛으로 기억됩니다.",
     "picks":[
        (8019,"아일라 섬의 그 바닷바람 맛. 한 번 빠지면 못 나옵니다."),
        (3194,"켄터키에서 마신 그대로. 콜라 섞으면 미국이 됩니다."),
        (5390,"도쿄 골목 어느 바에서나 이걸로 하이볼을 말아줍니다."),
     ]},
    {"code":"jurakworld","handle":"@주락이월드","name":"주락이월드","hot":True,
     "ava":"🥃","col":"#41643f","tags":["위스키 리뷰","싱글몰트"],"followers":"34만",
     "oneliner":"마셔보고 솔직하게, 위스키 리뷰의 기준.",
     "bio":"국내 대표 주류 리뷰 채널. 광고와 리뷰를 분리하는 원칙으로 신뢰를 쌓아왔습니다. "
           "벨루가에서는 직접 블라인드 시음을 거친 보틀만 큐레이션합니다.",
     "comment":"셰리 캐스크 유행이 한참인데, 결국 기본기가 좋은 증류소가 이깁니다. "
               "맥캘란과 글렌알라키를 나란히 마셔보세요 — 답이 나옵니다.",
     "picks":[
        (19904,"셰리 오크의 교과서. 기준이 있어야 비교가 됩니다."),
        (2962,"같은 셰리인데 절반 가격에 도수는 46%. 요즘 제일 바쁜 증류소."),
        (8019,"피트 입문은 쿼터캐스크보다 10년부터. 정석대로 가세요."),
     ]},
    {"code":"sulsuno","handle":"@술수노","name":"술수노","hot":False,
     "ava":"🍸","col":"#5b3a6e","tags":["꿀조합","입문"],"followers":"42만",
     "oneliner":"술알못도 따라 하는 꿀조합 레시피.",
     "bio":"'이렇게 마시면 맛있어요'를 가장 쉽게 알려주는 채널. 편의점 재료로 만드는 "
           "꿀조합부터 입문용 위스키까지, 술이 어려운 분들의 첫 가이드.",
     "comment":"위스키 입문은 거창할 필요 없어요. 6만 원대에서 시작해서 "
               "내 입맛을 찾은 다음에 올라가도 늦지 않습니다.",
     "picks":[
        (9215,"입문 1순위. 청사과 향이라 '술 냄새'가 안 무서워요."),
        (5229,"부드럽고 꽃향기. 글렌피딕이랑 비교하며 마셔보세요."),
        (5390,"토닉워터 4 : 가쿠빈 1 + 레몬. 이게 꿀조합의 시작."),
     ]},
    {"code":"newsulletter","handle":"@뉴술레터","name":"뉴술레터","hot":False,
     "ava":"📮","col":"#2f5d62","tags":["트렌드","뉴스레터"],"followers":"11만",
     "oneliner":"이번 주 술 트렌드, 메일함보다 먼저.",
     "bio":"매주 술 트렌드를 큐레이션하는 뉴스레터. 지금 바·보틀숍에서 무엇이 팔리는지, "
           "다음 유행은 무엇인지 — 데이터와 현장 취재로 픽합니다.",
     "comment":"올해 키워드는 '버번 리바이벌'과 '하이 프루프'예요. "
               "싱글몰트만 보던 분들이 버번 코너로 돌아오고 있습니다.",
     "picks":[
        (3304,"버번 리바이벌의 중심. 이 가격대에 적이 없습니다."),
        (3194,"하이 프루프 유행의 시작점. 칵테일 베이스로도 만점."),
        (9229,"'발베니는 항상 옳다'는 밈이 괜히 나온 게 아니에요."),
     ]},
    {"code":"veluga","handle":"@벨루가","name":"벨루가 공식","hot":False,
     "ava":"🐳","col":"#0066cc","tags":["데이터 픽","단독 소싱"],"followers":"공식",
     "oneliner":"13,000개 매장의 도매 데이터가 고른 술.",
     "bio":"국내 유일의 주류 도매 유통 플랫폼 벨루가의 공식 큐레이션. 전국 13,000개 매장에서 "
           "오가는 도매 거래 데이터를 AI로 분석해, 지금 가장 빠르게 움직이는 보틀과 "
           "단독 소싱 물량을 픽합니다.",
     "comment":"데이터는 거짓말을 하지 않습니다. 이번 주 전국 매장 발주가 가장 빠르게 "
               "늘어난 보틀과, 벨루가만 들여온 단독 물량을 모았습니다.",
     "picks":[
        (31081,"벨루가 단독 소싱. 콘테스트 4년 연속 골드의 스페이사이드."),
        (9229,"이번 주 전국 발주 증가율 1위 — 데이터가 고른 픽."),
        (3304,"재발주율(다시 시키는 비율) 최상위권. 매장이 증명한 맛."),
     ]},
]
IMAP = {i["code"]: i for i in INFLUENCERS}

# ---------------- EVENTS — 한정판 판매 이벤트 (인플루언서 종속) ----------------
# mech: crowd(공동구매·달성률 bar) / preorder(예약·잔여 bar) / stock(선착순·잔여 bar)
# status: live(진행 중) / upcoming(예정) / ended(마감 — SOLD OUT 아카이브)
# 메인의 모든 이벤트 카드는 클릭 시 해당 인플루언서 페이지로 이동.
EVENTS = [
    {"id":"e1","inf":"chimchakman","pv":2962,"mech":"crowd","status":"live",
     "title":"글렌알라키 12년 공동구매","goal":60,"sold":49,
     "ends":"06.19(금) 20:00 마감","note":"60병 모이면 확정 매입 — 미달 시 전액 환불"},
    {"id":"e2","inf":"jurakworld","pv":19904,"mech":"preorder","status":"live",
     "title":"맥캘란 12년 셰리 오크 예약","alloc":40,"left":7,
     "ends":"07.03 입고 — 입고 후 픽업","note":"국내 배정 40병 확정분"},
    {"id":"e3","inf":"ppanibottle","pv":8019,"mech":"stock","status":"live",
     "title":"라프로익 10년 선착순","total":30,"left":6,
     "ends":"소진 시 종료 — 결제 즉시 픽업","note":"보유 재고 30병이 전부"},
    {"id":"e4","inf":"sulsuno","status":"upcoming",
     "title":"시크릿 하이볼 세트 공동구매","open_at":"06.20(토) 20:00 오픈",
     "note":"오픈과 동시에 구성 공개 — 알림을 걸어두세요"},
    {"id":"e5","inf":"newsulletter","status":"upcoming",
     "title":"버번 리바이벌 컬렉션","open_at":"06.27(토) 20:00 오픈",
     "note":"이번 주 뉴술레터에서 다룬 그 버번들"},
    {"id":"e6","inf":"veluga","pv":31081,"status":"ended",
     "title":"탐나불린 셰리 캐스크 단독 소싱","result":"30병 · 3시간 만에 완판"},
    {"id":"e7","inf":"chimchakman","pv":5390,"status":"ended",
     "title":"가쿠빈 하이볼 공동구매","result":"200병 · 이틀 만에 완판"},
]
MECH_LABEL = {"crowd": "공동구매", "preorder": "예약", "stock": "선착순"}


def ev_bar(e):
    """진행 바 — crowd: 차오름(달성률) / preorder·stock: 소진(잔여)."""
    if e["mech"] == "crowd":
        pct = round(e["sold"] / e["goal"] * 100)
        lbl = f'<span><b>{e["sold"]}병</b> / 목표 {e["goal"]}병</span><span><b>{pct}%</b> 달성</span>'
    else:
        total = e.get("alloc") or e.get("total")
        pct = round((total - e["left"]) / total * 100)
        lbl = f'<span><b>{e["left"]}병 남음</b> / {total}병</span><span>{pct}% 소진</span>'
    return f'''<div class="bar"><div class="track-bg"><div class="fill" style="width:{pct}%;"></div></div>
        <div class="lbl">{lbl}</div></div>'''


def ev_live_card(e, base, link=True):
    """진행 중 이벤트 카드. link=True(메인) → 인플루언서 페이지로 /
       link=False(인플루언서 페이지) → 행 클릭 = 결제 시트."""
    p, i = PMAP[e["pv"]], IMAP[e["inf"]]
    head = (f'<a class="evcard" href="{base}influencer/{i["code"]}/">' if link
            else f'<div class="evcard" {pay_attrs(p)} onclick="VLG3.openPay(this)">')
    tail = "</a>" if link else "</div>"
    return f'''      {head}
        <span class="cover"><img src="{p["img"]}" alt="" loading="lazy" /></span>
        <div class="ei">
          <div class="top"><span class="mech">{MECH_LABEL[e["mech"]]}</span><span class="who">{i["handle"]}</span></div>
          <div class="nm">{e["title"]}</div>
          {ev_bar(e)}
          <div class="ends">⏳ {e["ends"]}</div>
        </div>
      {tail}'''


def ev_upcoming_card(e, base, link=True):
    i = IMAP[e["inf"]]
    inner = f'''        <div class="ei">
          <div class="top"><span class="mech soon">OPEN 예정</span><span class="who">{i["handle"]}</span></div>
          <div class="nm">{e["title"]}</div>
          <div class="ends">🕒 {e["open_at"]} — {e["note"]}</div>
        </div>
        <button type="button" class="notify" onclick="event.preventDefault();event.stopPropagation();VLG3.notify('{e["title"]}')">알림 받기</button>'''
    if link:
        return f'      <a class="evcard up" href="{base}influencer/{i["code"]}/">\n{inner}\n      </a>'
    return f'      <div class="evcard up">\n{inner}\n      </div>'


def ev_ended_card(e, base, link=True):
    p, i = PMAP[e["pv"]], IMAP[e["inf"]]
    inner = f'''        <span class="cover dim"><img src="{p["img"]}" alt="" loading="lazy" /></span>
        <div class="ei">
          <div class="top"><span class="mech out">SOLD OUT</span><span class="who">{i["handle"]}</span></div>
          <div class="nm">{e["title"]}</div>
          <div class="ends ok">✓ {e["result"]}</div>
        </div>'''
    if link:
        return f'      <a class="evcard end" href="{base}influencer/{i["code"]}/">\n{inner}\n      </a>'
    return f'      <div class="evcard end">\n{inner}\n      </div>'


def events_of(code, status):
    return [e for e in EVENTS if e["inf"] == code and e["status"] == status]


# ---------------- 공통 조각 ----------------
def gnav(base):
    """Apple식 초슬림 트루블랙 글로벌 나브(44px)."""
    return f'''  <header class="gnav">
    <a href="{base}index.html" class="logo">벨루<b>가</b></a>
    <nav>
      <a href="{base}sale.html">상설할인</a>
      <a href="{base}library.html">내 라이브러리</a>
      <a href="{base}about.html">About</a>
      <a href="{base}mypage.html">마이</a>
      <a class="cartico" href="{base}cart.html" aria-label="장바구니"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M6 2 3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"/><path d="M3 6h18"/><path d="M16 10a4 4 0 0 1-8 0"/></svg><span class="cartbadge" data-cart-badge style="display:none">0</span></a>
    </nav>
  </header>'''


def tabbar(base, active):
    def t(href, key, label, icon):
        on = ' class="on"' if key == active else ''
        return f'<a href="{href}"{on}>{icon}<span>{label}</span></a>'
    home = t(f"{base}index.html", "home", "홈",
             '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="m3 10 9-7 9 7v10a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><path d="M9 22V12h6v10"/></svg>')
    sale = t(f"{base}sale.html", "sale", "상설할인",
             '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M19 5 5 19"/><circle cx="6.5" cy="6.5" r="2.5"/><circle cx="17.5" cy="17.5" r="2.5"/></svg>')
    lib = t(f"{base}library.html", "lib", "내 라이브러리",
            '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M4 3v18"/><path d="M9 3v18"/><path d="m14 4 5 17"/></svg>')
    my = t(f"{base}mypage.html", "my", "마이",
           '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="8" r="4"/><path d="M4 21c0-4 4-6 8-6s8 2 8 6"/></svg>')
    return f'''  <nav class="tabbar">
    {home}
    {sale}
    {lib}
    {my}
  </nav>'''


def footer(base=""):
    return f'''  <footer class="ft">
    <div class="fl">벨루<b>가</b></div>
    <div>인플루언서가 말아주는 익스클루시브 술 큐레이션</div>
    <nav class="ftnav">
      <a href="{base}index.html">홈</a><a href="{base}sale.html">상설할인</a><a href="{base}library.html">내 라이브러리</a><a href="{base}about.html">About</a><a href="{base}mypage.html">마이</a>
    </nav>
    <div class="legal"><span class="age">19+</span> 주류는 만 19세 이상만 구매·픽업할 수 있습니다.<br/>
    (주)벨루가 · 사업자/통신판매업/주류통신판매 승인 정보 (확정 후 기재)<br/>
    본 페이지는 데모 목업입니다 — 가격·팔로워 수·코멘트는 가상이며 인플루언서와의 제휴는 체결 전입니다.</div>
  </footer>'''


def page(title, body, base="", tail="", active="home"):
    # tail(모달·인라인 스크립트)은 반드시 app.js 로드 "뒤"에 둠 — v2의
    # cart.js ReferenceError 버그 재발 방지.
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
{gnav(base)}
<main class="page">
{body}
</main>
{tabbar(base, active)}
<div class="toast" id="toast"></div>
<script src="{base}app.js?v={VERSION}"></script>
{tail}
</body>
</html>
'''


def price_html(p):
    out = ""
    if p.get("off"):
        out += f'<span class="off">{p["off"]}</span> '
    out += f'<span class="now">{p["now"]}</span>'
    if p.get("was"):
        out += f' <span class="was">{p["was"]}원</span>'
    return out


def ava(i, size=""):
    cls = f"ava {size}".strip()
    return f'<span class="{cls}" style="background:{i["col"]};">{i["ava"]}</span>'


def follow_btn(i, small=False):
    cls = "follow sm" if small else "follow"
    return (f'<button type="button" class="{cls}" data-follow="{i["code"]}" '
            f'onclick="event.preventDefault();event.stopPropagation();VLG3.toggle(\'{i["code"]}\')">팔로우</button>')


def inf_search_attr(i):
    return f'{i["handle"]} {i["name"]} {" ".join(i["tags"])}'


def rail_card(i, base):
    """스포티파이 플레이리스트 카드 문법 — 흰 카드 + 헤어라인 + 18px."""
    return f'''      <a class="rcard" href="{base}influencer/{i["code"]}/" data-inf-search="{inf_search_attr(i)}">
        {ava(i, "lg")}
        <div class="nm">{i["handle"]}</div>
        <div class="ds">{i["oneliner"]}</div>
        <div class="mt">{" · ".join(i["tags"])} · {i["followers"]}</div>
      </a>'''


def inf_row(i, base, data_attr=""):
    return f'''      <div class="irow" {data_attr} data-inf-search="{inf_search_attr(i)}">
        <a class="go" href="{base}influencer/{i["code"]}/">
          {ava(i)}
          <div class="who">
            <div class="hd">{i["handle"]}</div>
            <div class="sub">{" · ".join(i["tags"])} · 팔로워 {i["followers"]}</div>
          </div>
        </a>
        {follow_btn(i, small=True)}
      </div>'''


def pay_attrs(p, override=None):
    o = override or {}
    return (f'data-code="{p["pv"]}" data-name="{p["name"]}" data-img="{p["img"]}" '
            f'data-price="{o.get("now", p["now"])}" data-vol="{p["vol"]}"')


SAVE_BTN = ('<button type="button" class="save" data-save aria-label="라이브러리에 저장" '
            'onclick="event.stopPropagation();VLG3.toggleLib(this)">♡</button>')
CART_BTN = ('<button type="button" class="buy" '
            'onclick="event.stopPropagation();VLG3.addCart(this)">담기</button>')


def track_row(n, pv, cmt, i):
    """PICK = 스포티파이 트랙 행. 행 클릭 = 바로 결제, ♡ = 저장, 담기 = 장바구니."""
    p = PMAP[pv]
    return f'''      <div class="track" {pay_attrs(p)} onclick="VLG3.openPay(this)">
        <div class="no">{n:02d}</div>
        <span class="cover"><img src="{p["img"]}" alt="" loading="lazy" /></span>
        <div class="ti">
          <div class="nm">{p["name"]}</div>
          <div class="mt">{p["vol"]} · {p["abv"]} · {p["note"]}</div>
          <div class="cmt">“{cmt}”</div>
        </div>
        <div class="tr">
          <div class="price">{price_html(p)}</div>
          <div class="acts">{SAVE_BTN}{CART_BTN}</div>
        </div>
      </div>'''


PAY_MODAL = '''  <div class="pay-overlay" id="pay" onclick="if(event.target===this)VLG3.closePay()">
    <div class="pay-sheet" role="dialog" aria-modal="true">
      <div class="pay-grab"></div>
      <div class="pay-head"><span>주문서</span><button class="pay-x" onclick="VLG3.closePay()" aria-label="닫기">✕</button></div>
      <div class="pay-scroll">
        <div class="pay-order">
          <img id="pay-img" src="" alt="" />
          <div class="pay-order-info"><div class="t" id="pay-name"></div><div class="d" id="pay-vol"></div></div>
          <div class="pay-order-amt" id="pay-price"></div>
        </div>
        <div class="pay-sec">픽업 매장 <small>(온라인 결제 후 매장에서 수령)</small></div>
        <div class="pay-store">
          <label class="ps"><input type="radio" name="pstore" value="강남점" checked /><div><div>벨루가 픽업 · 강남점</div><div class="d">서울 강남구 테헤란로 ·· (0.4km)</div></div></label>
          <label class="ps"><input type="radio" name="pstore" value="역삼점" /><div><div>벨루가 픽업 · 역삼점</div><div class="d">서울 강남구 논현로 ·· (0.9km)</div></div></label>
          <label class="ps"><input type="radio" name="pstore" value="선릉점" /><div><div>벨루가 픽업 · 선릉점</div><div class="d">서울 강남구 선릉로 ·· (1.3km)</div></div></label>
        </div>
        <div class="pay-sec">결제 수단</div>
        <div class="pay-easy">
          <button type="button" class="easy sel" onclick="VLG3.selEasy(this)">toss pay</button>
          <button type="button" class="easy" onclick="VLG3.selEasy(this)">N Pay</button>
          <button type="button" class="easy" onclick="VLG3.selEasy(this)">kakao pay</button>
        </div>
        <label class="pay-agree-all"><input type="checkbox" id="pay-all" onchange="VLG3.agreeAll(this)" /> 약관 전체 동의</label>
        <div class="pay-agree-sub">
          <label><input type="checkbox" class="pay-req" /> [필수] 만 19세 이상이며, 픽업 시 성인 인증에 동의</label>
          <label><input type="checkbox" class="pay-req" /> [필수] 주문자 본인이 매장에서 직접 수령</label>
          <label><input type="checkbox" class="pay-req" /> [필수] 구매 주류의 미성년자 양도 금지 확인</label>
        </div>
        <div class="law">📌 주류는 온라인 배송이 불가합니다(전통주 제외). 결제 후 <b>매장 픽업(스마트오더)</b>만 가능해요.</div>
      </div>
      <div class="pay-foot"><button class="pay-cta" onclick="VLG3.payNow()">결제하기</button></div>
    </div>
  </div>'''


# ---------------- index.html (홈 — 이벤트 + 큐레이션 피드) ----------------
# 브랜드 카피·신뢰 지표·법 고지는 about.html로 이전 (2026-06-12 오퍼레이터).
def build_index():
    hot = [i for i in INFLUENCERS if i["hot"]]
    rest = [i for i in INFLUENCERS if not i["hot"]]

    hot_html = "\n".join(rail_card(i, "") for i in hot)
    follow_rows = "\n".join(inf_row(i, "", f'data-inf="{i["code"]}" style="display:none"') for i in INFLUENCERS)
    rec_rows = "\n".join(inf_row(i, "") for i in rest + hot)

    live = "\n".join(ev_live_card(e, "") for e in EVENTS if e["status"] == "live")
    upcoming = "\n".join(ev_upcoming_card(e, "") for e in EVENTS if e["status"] == "upcoming")
    ended = "\n".join(ev_ended_card(e, "") for e in EVENTS if e["status"] == "ended")

    body = f'''  <section class="sec sec--first">
    <div class="searchbox">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="11" cy="11" r="7"/><path d="m21 21-4.3-4.3"/></svg>
      <input id="infq" type="text" placeholder="인플루언서 검색 (@핸들·주종)" oninput="VLG3.search(this.value)" />
    </div>
  </section>

  <section class="sec" id="sec-live">
    <div class="row-head"><h2>🔴 진행 중인 한정판</h2></div>
{live}
  </section>

  <section class="sec" id="sec-hot">
    <div class="row-head"><h2>지금 HOT한 큐레이터</h2></div>
    <div class="rail">
{hot_html}
    </div>
  </section>

  <section class="sec" id="feed-follow">
    <div class="row-head"><h2>내가 팔로우한 큐레이터</h2></div>
    <div id="follow-empty" class="empty">
      아직 팔로우한 큐레이터가 없어요.<br/>
      <span>마음에 드는 큐레이터를 팔로우하면 여기에 모아드려요.</span>
    </div>
{follow_rows}
  </section>

  <section class="sec" id="sec-rec">
    <div class="row-head"><h2>이런 큐레이터는 어때요</h2></div>
{rec_rows}
    <div id="inf-empty" class="empty" style="display:none">검색 결과가 없어요. 다른 키워드로 찾아보세요.</div>
  </section>

  <section class="sec" id="sec-upcoming">
    <div class="row-head"><h2>오픈 예정</h2></div>
{upcoming}
  </section>

  <section class="sec" id="sec-ended">
    <div class="row-head"><h2>지난 한정판 — 전부 완판</h2></div>
{ended}
  </section>

{footer()}'''
    return page("벨루가 — 인플루언서 술 큐레이션", body, base="", active="home")


# ---------------- about.html (브랜드 — 메인에서 이전한 소개·신뢰·법 고지) ----------------
def build_about():
    body = f'''  <section class="hero">
    <div class="eyebrow">EXCLUSIVE CURATION</div>
    <h1>인플루언서가 말아주는<br/>익스클루시브 술 큐레이션.</h1>
    <p class="lead">국내 유일의 주류 도매 유통 플랫폼이 데이터로 소싱한 술을,
    믿고 보는 큐레이터가 직접 골라드립니다.</p>
  </section>

  <section class="sec">
    <div class="row-head"><h2>벨루가는 어떻게 술을 구하나요</h2></div>
    <p class="bio">벨루가는 전국 13,000개 매장의 주류 도매 거래가 오가는 <b>국내 유일의 주류 도매
    유통 플랫폼</b>입니다. 23,000종이 넘는 SKU의 도매 거래 데이터를 AI로 분석하기 때문에,
    어떤 보틀이 언제 어디서 풀리는지 가장 먼저 알고 직접 협상할 수 있습니다.
    큐레이터의 안목과 벨루가의 데이터가 만나 — 다른 곳에 없는 술이 여기 모입니다.</p>
  </section>

  <section class="band">
    <div class="trust">
      <div class="i"><b>13,000</b><span>매장 유통망</span></div>
      <div class="i"><b>23,000+</b><span>SKU 데이터</span></div>
      <div class="i"><b>AI</b><span>소싱 분석</span></div>
    </div>
  </section>

  <section class="sec">
    <div class="row-head"><h2>픽업은 이렇게</h2></div>
    <div class="steps">
      <div class="step"><div class="n">1</div><div><b>온라인에서 결제</b><br/>큐레이터 PICK에서 고르고 픽업 매장을 선택해요.</div></div>
      <div class="step"><div class="n">2</div><div><b>픽업 코드 발급</b><br/>결제 즉시 코드가 발급돼요. 입고 상품은 입고일 이후부터.</div></div>
      <div class="step"><div class="n">3</div><div><b>매장에서 수령</b><br/>신분증으로 성인 인증 후 바로 받아가세요.</div></div>
    </div>
    <div class="law">📌 <b>왜 배송이 아니라 픽업인가요?</b> 주류는 법적으로 온라인 배송이 불가합니다(전통주 제외).
    온라인 결제 후 매장에서 받는 <b>스마트오더</b>가 합법적인 유일한 방법이에요. 픽업 시 성인 인증이 필요합니다.</div>
  </section>

{footer()}'''
    return page("About — 벨루가", body, base="", active="home")


# ---------------- influencer/<code>/ (큐레이터 상세 — 아티스트 페이지) ----------------
def build_influencer(i):
    base = "../../"
    tracks = "\n".join(track_row(n + 1, pv, cmt, i) for n, (pv, cmt) in enumerate(i["picks"]))
    tags = "".join(f'<span class="chip">{t}</span>' for t in i["tags"])

    # 이벤트 3단 — 진행 중(행 클릭=결제)·오픈 예정·지난 이벤트
    live = events_of(i["code"], "live")
    upcoming = events_of(i["code"], "upcoming")
    ended = events_of(i["code"], "ended")
    ev_html = ""
    if live:
        cards = "\n".join(ev_live_card(e, base, link=False) for e in live)
        ev_html += f'''
  <section class="sec">
    <div class="row-head"><h2>🔴 진행 중인 한정판</h2></div>
{cards}
  </section>
'''
    if upcoming:
        cards = "\n".join(ev_upcoming_card(e, base, link=False) for e in upcoming)
        ev_html += f'''
  <section class="sec">
    <div class="row-head"><h2>오픈 예정</h2></div>
{cards}
  </section>
'''
    body = f'''  <section class="artist">
    {ava(i, "xl")}
    <div class="eyebrow on-dark">CURATOR</div>
    <h1>{i["handle"]}</h1>
    <div class="sub">팔로워 {i["followers"]}</div>
    <div class="chips">{tags}</div>
    {follow_btn(i)}
  </section>

  <section class="sec">
    <div class="row-head"><h2>소개</h2></div>
    <p class="bio">{i["bio"]}</p>
    <div class="quote">
      <div class="by">{ava(i)}<span>{i["handle"]}의 코멘트</span></div>
      <p>“{i["comment"]}”</p>
    </div>
  </section>
{ev_html}
  <section class="sec">
    <div class="row-head"><h2>{i["name"]}의 PICK</h2><span class="cnt">{len(i["picks"])}</span></div>
    <div class="tracklist">
{tracks}
    </div>
    <div class="law">📌 결제 즉시 픽업 코드가 발급됩니다. 가까운 매장에서 <b>본인 확인(성인 인증)</b> 후 수령하세요.</div>
  </section>
{f"""
  <section class="sec">
    <div class="row-head"><h2>지난 한정판 — 전부 완판</h2></div>
{chr(10).join(ev_ended_card(e, base, link=False) for e in ended)}
  </section>
""" if ended else ""}
{footer(base)}'''
    return page(f"{i['handle']} PICK — 벨루가", body, base=base, tail=PAY_MODAL, active="home")


# ---------------- sale.html (상설 할인 — 떨이 전용) ----------------
def build_sale():
    rows = []
    for n, s in enumerate(SALE):
        p = PMAP[s["pv"]]
        merged = {**p, **s}
        rows.append(f'''      <div class="track" {pay_attrs(p, s)} onclick="VLG3.openPay(this)">
        <div class="no">{n + 1:02d}</div>
        <span class="cover"><img src="{p["img"]}" alt="" loading="lazy" /></span>
        <div class="ti">
          <div class="nm">{p["name"]}</div>
          <div class="mt">{p["vol"]} · {p["abv"]} · {p["note"]}</div>
          <div class="cmt reason">🏷️ {s["reason"]}</div>
        </div>
        <div class="tr">
          <div class="price">{price_html(merged)}</div>
          <div class="acts">{SAVE_BTN}{CART_BTN}</div>
        </div>
      </div>''')
    grid = "\n".join(rows)

    body = f'''  <section class="hero hero--sale">
    <div class="eyebrow">상설 할인 — 떨이 전용</div>
    <h1>앗! 위스키가<br/>신발보다 싸다.</h1>
    <p class="lead">과잉 재고·시즌 물량·라벨 변경 재고만 모았습니다.
    창고를 비우는 동안만 이 가격 — 떨이 사유는 정직하게 적어둡니다.</p>
  </section>

  <section class="sec">
    <div class="row-head"><h2>지금 떨이 중</h2><span class="cnt">{len(SALE)}</span></div>
    <div class="tracklist">
{grid}
    </div>
    <div class="law">📌 떨이 상품도 동일하게 <b>매장 픽업(스마트오더)</b>으로 받습니다. 수량 소진 시 예고 없이 종료돼요.</div>
  </section>

{footer()}'''
    return page("상설 할인 — 벨루가", body, base="", tail=PAY_MODAL, active="sale")


def inf_json():
    import json as _json
    return _json.dumps(
        [{"code": i["code"], "handle": i["handle"], "tags": i["tags"],
          "followers": i["followers"], "ava": i["ava"], "col": i["col"]} for i in INFLUENCERS],
        ensure_ascii=False)


# ---------------- library.html (내 라이브러리 — 스포티파이 Your Library) ----------------
def build_library():
    body = f'''  <section class="sec sec--first">
    <div class="row-head"><h2>내 라이브러리</h2></div>
    <p class="bio" style="margin-bottom:6px;">저장한 보틀과 팔로우한 큐레이터를 한곳에 모아드려요.</p>
  </section>

  <section class="sec">
    <div class="row-head"><h2>저장한 보틀</h2><span class="cnt" id="lib-cnt"></span></div>
    <div class="tracklist" id="lib-bottles"></div>
    <div id="lib-bottles-empty" class="empty" style="display:none">
      저장한 보틀이 없어요.<br/><span>PICK 목록에서 ♡를 누르면 여기에 모아드려요.</span>
    </div>
  </section>

  <section class="sec">
    <div class="row-head"><h2>팔로우한 큐레이터</h2></div>
    <div id="my-follows"></div>
    <div id="my-follows-empty" class="empty" style="display:none">
      팔로우한 큐레이터가 없어요.<br/><span>홈에서 마음에 드는 큐레이터를 팔로우해 보세요.</span>
    </div>
  </section>

{footer()}'''
    tail = f'''{PAY_MODAL}
  <script>
    VLG3.renderLibrary({inf_json()});
  </script>'''
    return page("내 라이브러리 — 벨루가", body, base="", tail=tail, active="lib")


# ---------------- cart.html (장바구니 — 여러 상품 일괄 결제) ----------------
def build_cart():
    body = f'''  <section class="sec sec--first">
    <div class="row-head"><h2>장바구니</h2><span class="cnt" id="cart-cnt"></span></div>
    <div class="tracklist" id="cart-list"></div>
    <div id="cart-empty" class="empty" style="display:none">
      장바구니가 비어 있어요.<br/><span>큐레이터 PICK에서 "담기"를 누르면 여기에 모여요.</span>
    </div>
  </section>

  <section class="sec" id="cart-foot" style="display:none">
    <div class="total"><span>합계</span><b id="cart-total"></b></div>
    <button type="button" class="checkout" onclick="VLG3.checkoutCart()">전체 결제하기</button>
    <div class="law">📌 전 상품 <b>매장 픽업(스마트오더)</b>입니다. 픽업 매장은 결제 단계에서 선택해요.</div>
  </section>

{footer()}'''
    tail = f'''{PAY_MODAL}
  <script>
    VLG3.renderCart();
  </script>'''
    return page("장바구니 — 벨루가", body, base="", tail=tail, active="home")


# ---------------- mypage.html (마이 — 프로필·주문·설정) ----------------
def build_mypage():
    body = f'''  <section class="sec sec--first">
    <div class="prof">
      <span class="ava lg" style="background:#000;">🐳</span>
      <div>
        <div class="nm">벨루가 회원님</div>
        <div class="sub">010-****-1234 · 성인 인증 완료 ✓</div>
      </div>
    </div>
  </section>

  <section class="sec">
    <div class="row-head"><h2>주문 · 픽업</h2></div>
    <div id="my-orders"></div>
    <div id="my-orders-empty" class="empty" style="display:none">
      아직 주문이 없어요.<br/><span>큐레이터 PICK에서 첫 보틀을 골라보세요.</span>
    </div>
  </section>

  <section class="sec">
    <div class="mrow" onclick="location.href='library.html'"><div>내 라이브러리</div><div class="r"></div></div>
    <div class="mrow"><div>재입고 · 오픈 알림</div><div class="r"></div></div>
    <div class="mrow"><div>알림 설정</div><div class="r"></div></div>
    <div class="mrow" onclick="alert('카카오 채널 데모 — 실서비스에서 연결됩니다.')"><div>고객센터 (카카오 채널)</div><div class="r"></div></div>
    <div class="mrow" onclick="VLG3.resetDemo()"><div class="warn">데모 데이터 초기화</div><div class="r"></div></div>
  </section>

{footer()}'''
    tail = '''  <script>
    VLG3.renderMypage();
  </script>'''
    return page("마이 — 벨루가", body, base="", tail=tail, active="my")


# ---------------- 빌드 ----------------
def write(path, html):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full) or ROOT, exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  + {path}")


def main():
    print("벨루가 B2C v3 빌드 (뼈대 v4 — 인플루언서 큐레이션 / Apple 디자인 / 스포티파이 IA)")
    write("index.html", build_index())
    write("about.html", build_about())
    write("sale.html", build_sale())
    write("library.html", build_library())
    write("cart.html", build_cart())
    write("mypage.html", build_mypage())
    for i in INFLUENCERS:
        write(f"influencer/{i['code']}/index.html", build_influencer(i))
    print(f"완료 — 큐레이터 {len(INFLUENCERS)}명 · 상품 {len(PRODUCTS)}종 · v={VERSION}")


if __name__ == "__main__":
    main()
