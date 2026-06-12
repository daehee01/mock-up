#!/usr/bin/env python3
# 벨루가 B2C 랜딩 v2 — 정적 페이지 빌더 (뼈대 v3)
#
# 구조: 메인(한정 이벤트·인플루언서·위신싸 미리보기·SOLD OUT 아카이브)
#       / 전체상품(레인+주종 필터) / 위신싸관(떨이) / events(단일 컨테이너)
# 메커닉(mech): crowd(공동 예약·차오름 bar) / preorder(사전 예약·잔여 bar·입고일)
#               / stock(선착순·잔여 bar·즉시 픽업)
# 레인(lane):  limited(→ 이벤트 상세가 곧 상품 페이지) / wisinssa(떨이) / normal
# ※ 보틀 이미지는 검증된 벨루가 CDN 4종만 사용(외부 URL 추측 금지) — 한정 SKU는
#   탐나불린 패밀리 가상 데이터 + 기존 이미지 placeholder.
import os, json, re
from urllib.parse import quote

ROOT = os.path.dirname(os.path.abspath(__file__))
VERSION = "1"  # 캐시버스팅 — 디자인 변경 시 +1

SETTINGS_PATH = os.path.normpath(os.path.join(ROOT, "..", "..", "ops-drink", "settings.json"))
CATEGORIES_FALLBACK = ["국산 맥주", "수입 맥주", "소주", "와인", "위스키", "일반 증류주",
                       "탁주", "과실주", "중국술", "사케", "청주", "약주", "리큐르", "브랜디",
                       "기타 주류", "논알콜"]


def load_categories():
    try:
        with open(SETTINGS_PATH, encoding="utf-8") as f:
            data = json.load(f)
        cats = [k for k in data["주종별_스타일_값"].keys() if k and k != "주종"]
        return cats or CATEGORIES_FALLBACK
    except Exception:
        return CATEGORIES_FALLBACK


CATEGORIES = load_categories()

IMG = {
    "sherry": "https://cdn.veluga.kr/drinks/pv/31081.png",
    "double": "https://cdn.veluga.kr/drinks/pv/31253.png",
    "sb":     "https://cdn.veluga.kr/drinks/pv/31244.png",
    "pinot":  "https://cdn.veluga.kr/drinks/30879/pv/main/be6df03a84774220bdb94eac1f7089d5_%E1%84%90%E1%85%A1%E1%86%B7%E1%84%82%E1%85%A1%E1%84%87%E1%85%AE%E1%86%AF%E1%84%85%E1%85%B5%E1%86%AB_%E1%84%8C%E1%85%A5%E1%84%86%E1%85%A5%E1%86%AB_%E1%84%91%E1%85%B5%E1%84%82%E1%85%A9_%E1%84%82%E1%85%AE%E1%84%8B%E1%85%A1.png",
}

FONT = ('<link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin />\n'
        '<link rel="stylesheet" as="style" crossorigin '
        'href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css" />')

SHARED = {
    "region": "스페이사이드, 스코틀랜드",
    "producer": "Whyte & Mackay",
    "flag": "🥃",
    "foods": [("🧀", "숙성 치즈 · 견과"), ("🦪", "차가운 해산물"), ("🍫", "다크 초콜릿")],
    "story": [
        "스코틀랜드 스페이사이드의 탐나불린 증류소는 <b>부드럽고 달콤한 싱글몰트</b> 스타일로 알려져 있습니다.",
        "같은 원액에서도 셰리 · 쇼비뇽 블랑 · 피노 누아 등 <b>캐스크 피니시</b>에 따라 전혀 다른 개성을 끌어냅니다.",
    ],
}

# ---------------- PRODUCTS — lane: limited / wisinssa / normal ----------------
PRODUCTS = [
    # 한정 (이벤트 연동 — 카드 클릭 시 이벤트 상세로)
    {"code":"1001","lane":"limited","event":"0101","name":"탐나불린 18년 싱글 캐스크","img":IMG["sherry"],
     "now":"219,000원","was":"","off":"","vol":"700mL","abv":"54.2%","cat":"위스키",
     "badge":"공동 예약 80%","badge_kind":"deal",
     "search":"탐나불린 18년 싱글 캐스크 셰리 벗 고연산 한정 공동 예약",
     "why":"18년 셰리 벗 싱글 캐스크 원액 그대로. 캐스크 스트렝스 54.2%의 진한 셰리·건과일 풍미입니다.",
     "aroma":"건포도 · 무화과 · 다크초콜릿","palate":"셰리 · 호두 · 흑설탕","finish":"길고 묵직한 건과일 여운"},
    {"code":"1002","lane":"limited","event":"0102","name":"탐나불린 21년 캐스크 스트렝스","img":IMG["double"],
     "now":"329,000원","was":"","off":"","vol":"700mL","abv":"57.1%","cat":"위스키",
     "badge":"사전 예약","badge_kind":"",
     "search":"탐나불린 21년 캐스크 스트렝스 고연산 사전 예약 얼로케이션",
     "why":"21년 고연산 캐스크 스트렝스. 국내 배정 60병이 확정된 1차 선적분입니다.",
     "aroma":"오크 · 꿀 · 잘 익은 배","palate":"토피 · 견과 · 오렌지 필","finish":"스파이시하고 긴 오크 여운"},
    {"code":"0004","lane":"limited","event":"0103","name":"탐나불린 피노 누아","img":IMG["pinot"],
     "now":"94,000원","was":"","off":"","vol":"700mL","abv":"40%","cat":"위스키",
     "badge":"6병 남음","badge_kind":"deal",
     "search":"탐나불린 저먼 피노 누아 캐스크 레드와인 한정 레어 선착순",
     "why":"피노 누아의 향이 피어오르는 레드와인 캐스크. 진한 로즈우드 컬러와 우아한 단맛이 특징입니다.",
     "aroma":"체리 · 사과파이","palate":"바닐라 · 무화과 · 터키쉬 딜라이트","finish":"복숭아 · 오렌지 · 감초"},

    # 일반
    {"code":"0001","lane":"normal","name":"탐나불린 셰리 캐스크","img":IMG["sherry"],
     "now":"89,000원","was":"","off":"","vol":"700mL","abv":"40%","cat":"위스키","badge":"","badge_kind":"",
     "search":"탐나불린 셰리 캐스크 스페이사이드 싱글몰트",
     "why":"글로벌 위스키 콘테스트 4년 연속 골드. 달콤하고 부드러워 위스키가 처음인 분도 편하게 즐깁니다.",
     "aroma":"구운 빵 · 바닐라 · 생강 · 오렌지","palate":"천도복숭아 · 케이크 · 토피넛","finish":"과일 · 살구의 복합미"},
    {"code":"0002","lane":"normal","name":"탐나불린 더블 캐스크","img":IMG["double"],
     "now":"59,000원","was":"","off":"","vol":"700mL","abv":"40%","cat":"위스키","badge":"","badge_kind":"",
     "search":"탐나불린 더블 캐스크 스페이사이드 싱글몰트 입문",
     "why":"가성비·가심비를 모두 잡은 공식 라인업의 첫 위스키. 두 캐스크의 균형감이 특징입니다.",
     "aroma":"사과 · 토피 · 마지팬 · 스파이스","palate":"배 · 복숭아 · 구운 파인애플","finish":"깔끔 · 스파이시 · 달콤"},
    {"code":"0006","lane":"normal","name":"탐나불린 기프트 세트","img":IMG["double"],
     "now":"69,000원","was":"","off":"","vol":"700mL + 전용잔","abv":"40%","cat":"위스키","badge":"선물","badge_kind":"",
     "search":"탐나불린 더블 캐스크 기프트 세트 선물 전용잔",
     "why":"탐나불린 더블 캐스크에 브랜드 전용잔을 더한 선물 세트. 위스키 입문 선물로 안성맞춤입니다.",
     "aroma":"사과 · 토피 · 마지팬","palate":"배 · 복숭아 · 흑설탕","finish":"깔끔 · 달콤"},
    {"code":"0008","lane":"normal","name":"셰리·더블 2종 세트","img":IMG["sherry"],
     "now":"139,000원","was":"","off":"","vol":"700mL x 2","abv":"40%","cat":"위스키","badge":"테이스팅","badge_kind":"",
     "search":"탐나불린 셰리 더블 캐스크 2종 테이스팅 세트 비교",
     "why":"셰리와 더블 캐스크를 한 번에 비교 시음할 수 있는 2종 세트. 캐스크별 개성을 즐기기 좋습니다.",
     "aroma":"두 캐스크의 향을 한자리에","palate":"셰리의 달콤 · 더블의 균형","finish":"각기 다른 여운"},

    # 위신싸 (가성비·떨이·임박)
    {"code":"0003","lane":"wisinssa","reason":"과잉 재고 떨이","name":"탐나불린 쇼비뇽 블랑","img":IMG["sb"],
     "now":"49,900원","was":"72,000","off":"31%","vol":"700mL","abv":"40%","cat":"위스키","badge":"31%","badge_kind":"deal",
     "search":"탐나불린 쇼비뇽 블랑 캐스크 화이트와인 여름 떨이 특가",
     "why":"여름을 상징하는 화이트와인 캐스크 싱글몰트. 여름 물량이 많이 들어와 통 크게 풉니다.",
     "aroma":"청사과 · 파인애플 · 멜론 · 자스민","palate":"레몬 · 라임 · 사과파이","finish":"과일 · 크리미한 코코넛"},
    {"code":"0007","lane":"wisinssa","reason":"시즌 마감 임박","name":"쇼비뇽 블랑 하이볼팩","img":IMG["sb"],
     "now":"59,900원","was":"79,000","off":"24%","vol":"700mL + 토닉","abv":"40%","cat":"위스키","badge":"24%","badge_kind":"deal",
     "search":"탐나불린 쇼비뇽 블랑 하이볼 패키지 토닉 여름 임박 특가",
     "why":"쇼비뇽 블랑에 토닉을 더한 여름 하이볼 패키지. 시즌 구성품 소진 시 종료됩니다.",
     "aroma":"청사과 · 파인애플 · 멜론","palate":"레몬 · 라임 · 진저","finish":"청량 · 코코넛"},
    {"code":"0005","lane":"wisinssa","reason":"가성비 입문","name":"탐나불린 셰리 200mL","img":IMG["sherry"],
     "now":"24,900원","was":"29,000","off":"14%","vol":"200mL","abv":"40%","cat":"위스키","badge":"14%","badge_kind":"deal",
     "search":"탐나불린 셰리 캐스크 미니어처 200ml 입문 가성비",
     "why":"부담 없이 셰리 캐스크를 맛볼 수 있는 미니 사이즈. 선물이나 입문용으로 좋습니다.",
     "aroma":"구운 빵 · 바닐라 · 오렌지","palate":"천도복숭아 · 토피넛","finish":"과일 · 살구"},
]
PMAP = {p["code"]: p for p in PRODUCTS}

# ---------------- EVENTS — type: limited / wisinssa / promo ----------------
# mech: crowd(공동 예약) / preorder(사전 예약) / stock(선착순)
EVENTS = [
    {"code":"0101","type":"limited","mech":"crowd","status":"live","product":"1001",
     "title":"탐나불린 18년 싱글 캐스크 공동 예약","img":IMG["sherry"],
     "period":"2026.06.09 – 06.19","deadline":"2026-06-19T20:00:00+09:00",
     "goal":30,"sold":24,"eta":"2026.07.03",
     "desc":"단 한 통의 셰리 벗에서 나온 18년 원액. 30병이 모이면 벨루가가 직접 들여옵니다.",
     "inf":{"handle":"@위스키한모금","comment":"캐스크 스트렝스 셰리는 이 가격에 다시 만나기 어렵습니다. 같이 모아서 엽시다."},
     "specs":[("연산","<b>18</b>년"),("캐스크","셰리 벗 #4012"),("국내 배정","30병 한정"),("도수","54.2% C/S")],
     "source":[
        "이 보틀은 매장 진열대에서 살 수 없습니다. 증류소가 한 통 단위로만 내놓는 <b>싱글 캐스크 원액</b>이라, 수입사도 주문이 모여야 들여올 수 있습니다.",
        "벨루가는 전국 <b>13,000개 매장에 술을 공급하는 주류 도매상</b>입니다. 그 공급망 덕분에 일반 소매가 접근하지 못하는 캐스크 단위 물량을 직접 협상할 수 있습니다.",
        "30병의 예약이 모이면 벨루가가 캐스크를 확정 매입하고, 7월 초 입고 후 가까운 픽업 매장에서 받아보실 수 있습니다.",
     ]},

    {"code":"0102","type":"limited","mech":"preorder","status":"live","product":"1002",
     "title":"탐나불린 21년 캐스크 스트렝스 사전 예약","img":IMG["double"],
     "period":"2026.06.05 – 06.28","deadline":"2026-06-28T23:59:00+09:00",
     "alloc":60,"left":14,"eta":"2026.07.03",
     "desc":"국내 배정 60병이 이미 확정된 1차 선적분. 입고 전 사전 예약으로 먼저 잡으세요.",
     "specs":[("연산","<b>21</b>년"),("물량","1차 선적분"),("국내 배정","60병 확정"),("도수","57.1% C/S")],
     "source":[
        "21년 캐스크 스트렝스는 증류소가 국가별로 수량을 배정하는 <b>얼로케이션 보틀</b>입니다. 한국 배정분은 60병 — 추가 입고는 다음 배정을 기다려야 합니다.",
        "벨루가는 도매 공급망의 직거래 라인으로 이번 1차 선적분 60병 전량을 확보했습니다. 이미 46병이 예약되어 <b>14병 남았습니다</b>.",
        "7월 3일 입고 예정이며, 입고 즉시 픽업 코드가 발급됩니다.",
     ]},

    {"code":"0103","type":"limited","mech":"stock","status":"live","product":"0004",
     "title":"피노 누아 캐스크 선착순 20병","img":IMG["pinot"],
     "period":"2026.06.10 – 소진 시","deadline":"2026-06-17T23:59:00+09:00",
     "total":20,"left":6,
     "desc":"레드와인 캐스크 피니시 레어 보틀. 창고에 있는 20병이 전부 — 결제 즉시 오늘 픽업 가능합니다.",
     "inf":{"handle":"@위스키한모금","comment":"피노 누아 피니시는 호불호 없이 선물용으로도 좋아요. 남은 수량 보고 서두르세요."},
     "specs":[("캐스크","저먼 피노 누아"),("물량","보유 재고 20병"),("남은 수량","<b>6</b>병"),("도수","40%")],
     "source":[
        "수입사 마지막 재고 20병을 벨루가가 통째로 가져왔습니다. 이 물량이 끝나면 국내 정식 유통분은 없습니다.",
        "보유 재고라 <b>결제 즉시 픽업 코드가 발급</b>되고, 가까운 매장에서 당일 픽업할 수 있습니다.",
     ]},

    {"code":"0104","type":"wisinssa","mech":"stock","status":"live",
     "title":"여름 떨이 — 쇼비뇽 블랑 과잉 재고","img":IMG["sb"],
     "period":"2026.06.10 – 06.30","deadline":"2026-06-30T23:59:00+09:00",
     "total":40,"left":18,
     "desc":"여름 물량이 너무 많이 들어왔습니다. 창고 비울 때까지 최대 31% — 싸니까 빨리 가져가세요.",
     "products":["0003","0007","0005"],
     "features":[
        ("📦 과잉 재고 정리","수요 예측보다 물량이 많이 들어왔어요. 도매상 창고를 비우는 동안만 이 가격입니다."),
        ("🧊 여름에 제일 맛있는 술","화이트와인 캐스크 특유의 청량감. 칠링하거나 하이볼로 마시기 좋은 계절입니다."),
        ("🏪 오늘 결제, 오늘 픽업","보유 재고라 결제 즉시 픽업 코드 발급. 가까운 매장에서 바로 받아가세요."),
     ]},

    {"code":"0105","type":"promo","status":"live",
     "title":"위스키 입문자 기획전","img":IMG["double"],
     "period":"상시",
     "desc":"'뭐부터 마셔야 할지 모르겠다'는 분들을 위해. 부담 없는 가격·용량·선물 구성으로 첫 보틀을 골라드려요.",
     "products":["0002","0005","0006"],
     "features":[
        ("🍯 달콤·부드러운 입문용","탐나불린은 셰리 단맛이 부드러워 위스키가 처음인 분도 거부감이 없어요."),
        ("🥃 작게 시작하는 미니어처","200mL 미니로 부담 없이 맛만 먼저 보고, 마음에 들면 풀보틀로."),
        ("🎁 선물로도 딱","전용잔을 더한 기프트 세트는 위스키 입문 선물로 안성맞춤이에요."),
     ]},

    # 오픈 예정 — 허브·메인에 알림 받기 배너
    {"code":"0106","type":"limited","mech":"crowd","status":"upcoming",
     "title":"시크릿 캐스크 공동 예약","img":IMG["pinot"],
     "open_at":"2026.06.27 (토) 20:00 오픈",
     "desc":"연산 비공개. 오픈과 동시에 스펙이 공개되는 단 한 통의 캐스크. 알림을 걸어두세요."},

    # 종료 — SOLD OUT 아카이브 (희소성 증명)
    {"code":"0107","type":"limited","mech":"crowd","status":"ended","img":IMG["sherry"],
     "title":"5월 공동 예약 · 셰리 싱글 캐스크","result":"24병 · 3시간 만에 목표 달성"},
    {"code":"0108","type":"limited","mech":"stock","status":"ended","img":IMG["double"],
     "title":"4월 선착순 · 더블 캐스크 매그넘","result":"40병 · 이틀 만에 완판"},
]
EMAP = {e["code"]: e for e in EVENTS}

MECH_LABEL = {"crowd": "공동 예약", "preorder": "사전 예약", "stock": "선착순"}
LANE_LABEL = {"limited": "한정 이벤트", "wisinssa": "위신싸", "normal": "일반"}


# ---------------- 공통 조각 ----------------
def header(base):
    return f'''  <header class="hdr">
    <a href="{base}index.html" class="logo mark">벨루<b>가</b></a>
    <nav class="nav">
      <a href="{base}products.html">전체상품</a>
      <a href="{base}wisinssa.html">위신싸</a>
      <a href="{base}about.html">About</a>
      <a class="ico cart-ico" href="{base}cart.html" aria-label="장바구니"><svg width="21" height="21" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 2 3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"/><path d="M3 6h18"/><path d="M16 10a4 4 0 0 1-8 0"/></svg><span class="cart-badge" data-cart-badge style="display:none">0</span></a>
      <a class="ico" href="{base}mypage.html" aria-label="마이페이지"><svg width="21" height="21" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="8" r="4"/><path d="M4 21c0-4 4-6 8-6s8 2 8 6"/></svg></a>
    </nav>
  </header>'''


def footer():
    return '''  <footer class="ft">
    <div class="fl mark">벨루<b>가</b></div>
    <div style="margin-bottom:4px;">구하기 어려운 술을, 동네 매장에서 — 벨루가 B2C</div>
    <span class="age">19+ 청소년 보호</span>
    <div>주류는 만 19세 이상만 구매·픽업할 수 있습니다.</div>
    <div style="margin-top:10px;"><b>(주)벨루가</b> · 사업자/통신판매업/주류통신판매 승인 정보 (확정 후 기재)</div>
  </footer>'''


def page(title, body, base=""):
    return f'''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{title}</title>
{FONT}
<link rel="stylesheet" href="{base}style.css?v={VERSION}" />
<link rel="stylesheet" href="{base}v2.css?v={VERSION}" />
</head>
<body>
<div class="wrap">
{body}
</div>
<script src="{base}cart.js?v={VERSION}"></script>
</body>
</html>
'''


def price_html(p):
    out = ""
    if p.get("off"):
        out += f'<span class="off">{p["off"]}</span>'
    out += f'<span class="now">{p["now"]}</span>'
    if p.get("was"):
        out += f' <span class="was">{p["was"]}</span>'
    return out


def price_num(p):
    return int(re.sub(r"[^0-9]", "", p["now"]) or 0)


def card(p, base):
    badge = ""
    if p.get("badge"):
        cls = "badge deal" if p.get("badge_kind") == "deal" else "badge"
        badge = f'<span class="{cls}">{p["badge"]}</span>'
    # 한정 단일 보틀: 이벤트 상세가 곧 상품 페이지 (3홉 방지)
    href = f'{base}events/{p["event"]}/' if p.get("lane") == "limited" else f'{base}product/{p["code"]}/'
    return f'''      <a class="prod" href="{href}" data-name="{p['search']}" data-cat="{p.get('cat','위스키')}" data-lane="{p['lane']}">
        {badge}
        <img src="{p['img']}" alt="" />
        <div class="nm">{p['name']}</div>
        <div class="meta">{p['vol']} · {p['abv']}</div>
        <div class="price">{price_html(p)}</div>
      </a>'''


def mbar(e, dark=False):
    """메커닉별 진행 바. crowd=달성률(차오름·앰버) / preorder·stock=잔여(소진·그린)"""
    if e["mech"] == "crowd":
        pct = round(e["sold"] / e["goal"] * 100)
        return f'''<div class="mbar mbar--crowd"><div class="track"><div class="fill" style="width:{pct}%;"></div></div>
        <div class="lbl"><span><b>{e["sold"]}병</b> / 목표 {e["goal"]}병</span><span><b>{pct}%</b> 달성</span></div></div>'''
    total = e.get("alloc") or e.get("total")
    sold = total - e["left"]
    pct = round(sold / total * 100)
    unit = "배정" if e["mech"] == "preorder" else "한정"
    return f'''<div class="mbar"><div class="track"><div class="fill" style="width:{pct}%;"></div></div>
        <div class="lbl"><span>{unit} {total}병 중 <b>{e["left"]}병 남음</b></span><span>{pct}% 소진</span></div></div>'''


def mech_chip(e):
    return f'<span class="mech mech--{e["mech"]}">{MECH_LABEL[e["mech"]]}</span>'


COUNTDOWN_JS = '''  <script>
    (function(){
      var el=document.getElementById('cd'); if(!el) return;
      var t=new Date(el.getAttribute('data-deadline')).getTime();
      function f(){
        var d=t-Date.now();
        if(d<=0){ el.textContent='마감되었습니다'; return; }
        var dd=Math.floor(d/864e5), hh=Math.floor(d%864e5/36e5), mm=Math.floor(d%36e5/6e4);
        el.textContent='⏳ 마감까지 '+(dd>0?dd+'일 ':'')+hh+'시간 '+mm+'분';
        setTimeout(f, 3e4);
      }
      f();
    })();
  </script>'''

STORE_SCRIPT = '''  <script>
    function naverSearch(){
      var v=(document.getElementById('storeq').value||'').trim();
      var q=encodeURIComponent((v?v+' ':'')+'벨루가 픽업 주류');
      window.open('https://map.naver.com/p/search/'+q,'_blank');
    }
  </script>'''


def stores_html():
    stores = [("강남점", "서울 강남구 테헤란로 ··", "0.4km"),
              ("역삼점", "서울 강남구 논현로 ··", "0.9km"),
              ("선릉점", "서울 강남구 선릉로 ··", "1.3km")]
    return "\n    ".join(
        f'<a class="store" href="https://map.naver.com/p/search/{quote("벨루가 픽업 " + nm)}" target="_blank" rel="noopener">'
        f'<div><div class="nm">벨루가 픽업 · {nm}</div><div class="ad">{ad}</div></div><div class="dist">{d} ›</div></a>'
        for nm, ad, d in stores)


def pickup_section(note):
    return f'''  <section class="sec sec--tight" style="padding-top:40px;">
    <div class="eyebrow">PICKUP STORES</div>
    <div class="h2">내 주변 픽업 매장.</div>
    <p class="lead">{note}</p>
    <div class="store-find">
      <input id="storeq" type="text" placeholder="동·지하철역으로 검색" />
      <button onclick="naverSearch()">검색</button>
    </div>
    {stores_html()}
  </section>'''


LAW_BOX = ('<div class="law" style="margin-top:18px;">📌 <b>왜 배송이 아니라 픽업인가요?</b> '
           '주류는 법적으로 온라인 배송이 불가합니다(전통주 제외). 온라인 결제 후 매장에서 받는 '
           '<b>스마트오더</b>가 합법적인 유일한 방법이에요.</div>')


# ---------------- index.html (메인) ----------------
def build_index():
    hero_e = EMAP["0101"]  # 최우선 이벤트 = 공동 예약 콜라보
    live_limited = [e for e in EVENTS if e["type"] == "limited" and e["status"] == "live"]
    ended = [e for e in EVENTS if e["status"] == "ended"]
    upcoming = [e for e in EVENTS if e["status"] == "upcoming"]
    wss = [p for p in PRODUCTS if p["lane"] == "wisinssa"]

    ev_cards = ""
    for e in live_limited:
        p = PMAP[e["product"]]
        sub = {"crowd": f'목표 달성 시 {e.get("eta","")} 입고', "preorder": f'{e.get("eta","")} 입고 예정',
               "stock": "결제 즉시 당일 픽업"}[e["mech"]]
        ev_cards += f'''      <a class="evcard" href="events/{e['code']}/">
        <div class="top">
          <img src="{e['img']}" alt="" />
          <div style="flex:1;min-width:0;">
            {mech_chip(e)}
            <div class="tt">{e['title']}</div>
            <div class="ds">{p['now']} · {sub}</div>
          </div>
        </div>
        {mbar(e)}
      </a>\n'''

    inf_cards = ""
    for e in live_limited:
        if not e.get("inf"):
            continue
        inf_cards += f'''      <a class="evcard" href="events/{e['code']}/">
        <div class="top">
          <img src="{e['img']}" alt="" />
          <div style="flex:1;min-width:0;">
            <span class="lockup"><span class="hd">{e['inf']['handle']}</span><span class="x">×</span><span>벨루가</span></span>
            <div class="tt">{e['title']}</div>
            <div class="ds">"{e['inf']['comment'][:38]}…"</div>
          </div>
        </div>
      </a>\n'''

    wss_cards = "\n".join(card(p, "") for p in wss[:3])
    arch = "\n".join(
        f'''      <div class="arch"><img src="{e['img']}" alt="" />
        <div><div class="tt">{e['title']}</div><div class="ds">{e['result']}</div></div>
        <span class="stamp">SOLD OUT</span></div>''' for e in ended)
    soon = "\n".join(
        f'''      <div class="pbanner pbanner--soon">
        <div class="pb-body">
          <div class="soon-badge">OPEN 예정</div>
          <div class="ptt">{e['title']}</div>
          <div class="pperiod">🕒 {e['open_at']}</div>
          <div class="pdesc">{e['desc']}</div>
          <a class="btn btn-ghost" style="margin-top:14px;padding:12px;font-size:14px;" href="join.html">🔔 오픈 알림 받기</a>
        </div>
        <img src="{e['img']}" alt="" />
      </div>''' for e in upcoming)

    pct = round(hero_e["sold"] / hero_e["goal"] * 100)
    body = f'''{header("")}

  <!-- HERO — 지금 최우선 이벤트 (공동 예약 콜라보) -->
  <section class="hero hero--dark hero-ev">
    <img class="bottle rise d3" src="{hero_e['img']}" alt="" />
    <div class="inner" style="flex:1;display:flex;flex-direction:column;">
      <span class="lockup rise d1"><span class="hd">{hero_e['inf']['handle']}</span><span class="x">×</span><span>벨루<b style="color:var(--amber);">가</b></span></span>
      <div class="ttl rise d2">탐나불린 18년<br />싱글 캐스크</div>
      <p class="sub rise d2">단 한 통, 국내 배정 {hero_e['goal']}병. {hero_e['goal']}병이 모이면 벨루가가 직접 들여옵니다.</p>
      <div class="barwrap rise d3">{mbar(hero_e)}
        <span class="cdown" id="cd" data-deadline="{hero_e['deadline']}">⏳ 마감 {hero_e['period'].split("–")[1].strip()}</span>
      </div>
      <div class="rise d4" style="margin-top:22px;"><a href="events/{hero_e['code']}/" class="btn btn-primary btn-inline" style="background:var(--amber);color:var(--amber-ink);">공동 예약 참여하기 →</a></div>
      <div class="foot-row"><span class="scroll-hint">SCROLL<br />▾</span></div>
    </div>
  </section>

  <!-- 1) 진행 중 한정 이벤트 -->
  <section class="sec" id="now">
    <div class="row-head"><div class="t">진행 중 한정 이벤트</div><a class="more" href="events/">전체 →</a></div>
{ev_cards}  </section>

  <!-- 2) 인플루언서 픽 -->
  <section class="sec sec--tight">
    <div class="row-head"><div class="t">인플루언서 픽</div></div>
{inf_cards}  </section>

  <!-- 3) 위신싸 미리보기 -->
  <section class="sec sec--tight">
    <div class="row-head"><div class="t">위신<b style="color:var(--amber);">싸</b> — 신발보다 싸다</div><a class="more" href="wisinssa.html">떨이 전체 →</a></div>
    <div class="carousel">
{wss_cards}
    </div>
  </section>

  <!-- 4) SOLD OUT 아카이브 — 희소성 증명 -->
  <section class="sec sec--tight">
    <div class="row-head"><div class="t">지난 이벤트</div></div>
{arch}
    <div style="font-size:12.5px;color:var(--ink-48);margin-top:10px;letter-spacing:-0.01em;">놓치셨나요? 다음 이벤트 알림을 받아보세요.</div>
  </section>

  <!-- 5) 오픈 예정 -->
  <section class="sec sec--tight">
    <div class="row-head"><div class="t">오픈 예정</div></div>
{soon}
  </section>

  <!-- 가입 유도 -->
  <section class="join-cta">
    <div class="jt">회원가입하고<br /><b>한정 이벤트 알림</b>까지.</div>
    <div class="jd">공동 예약 오픈 알림부터 첫 픽업 혜택까지, 30초 가입으로 받아가세요.</div>
    <a href="join.html" class="btn">벨루가 가입하기 →</a>
  </section>

{footer()}
{COUNTDOWN_JS}'''
    return page("벨루가 — 구하기 어려운 술을, 동네 매장에서", body)


# ---------------- products.html (전체상품 — 레인 + 주종 필터) ----------------
def build_products():
    cards = "\n".join(card(p, "") for p in PRODUCTS)
    lane_chips = "\n".join(
        f'      <button type="button" class="fchip" data-lane="{k}">{v}</button>'
        for k, v in LANE_LABEL.items())
    cat_chips = "\n".join(
        f'      <button type="button" class="fchip" data-cat2="{c}">{c}</button>'
        for c in CATEGORIES)
    body = f'''{header("")}

  <div class="ptop">
    <h1>전체 상품</h1>
    <div class="cnt"><span id="count">{len(PRODUCTS)}</span>개 상품 · 픽업 가능 전체</div>
  </div>

  <div class="searchbar">
    <div class="searchbox">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#7a7a7a" stroke-width="2.2" stroke-linecap="round"><circle cx="11" cy="11" r="7"/><path d="M21 21l-4.3-4.3"/></svg>
      <input id="q" type="text" placeholder="상품명·증류소·캐스크 검색" autocomplete="off" />
    </div>
    <!-- 1차: 레인 필터 (한정/위신싸/일반) -->
    <div class="filterbar" id="lanebar">
      <button type="button" class="fchip on" data-lane="">전체</button>
{lane_chips}
    </div>
    <!-- 2차: 주종 필터 (벨루가 settings.json 기준) -->
    <div class="filterbar" id="catbar" style="margin-top:8px;">
      <button type="button" class="fchip on" data-cat2="">모든 주종</button>
{cat_chips}
    </div>
  </div>

  <div class="grid" id="grid">
{cards}
  </div>
  <div class="empty" id="empty">조건에 맞는 상품이 없어요.</div>

{footer()}

  <script>
    var q=document.getElementById('q'),cards=[].slice.call(document.querySelectorAll('#grid .prod')),
        countEl=document.getElementById('count'),emptyEl=document.getElementById('empty'),
        activeLane='',activeCat='';
    function norm(s){{return (s||'').toLowerCase().replace(/\\s+/g,'');}}
    function apply(){{
      var t=norm(q.value),n=0;
      cards.forEach(function(c){{
        var hay=norm(c.getAttribute('data-name')+' '+c.querySelector('.nm').textContent);
        var ok=(t===''||hay.indexOf(t)!==-1)
          &&(activeLane===''||c.getAttribute('data-lane')===activeLane)
          &&(activeCat===''||c.getAttribute('data-cat')===activeCat);
        c.style.display=ok?'':'none'; if(ok)n++;
      }});
      countEl.textContent=n; emptyEl.style.display=n===0?'block':'none';
    }}
    q.addEventListener('input',apply);
    function bindChips(barId,attr,set){{
      var chips=[].slice.call(document.querySelectorAll('#'+barId+' .fchip'));
      chips.forEach(function(ch){{
        ch.addEventListener('click',function(){{
          chips.forEach(function(x){{x.classList.remove('on');}});
          ch.classList.add('on'); set(ch.getAttribute(attr)||'');
          ch.scrollIntoView({{inline:'center',block:'nearest',behavior:'smooth'}}); apply();
        }});
      }});
    }}
    bindChips('lanebar','data-lane',function(v){{activeLane=v;}});
    bindChips('catbar','data-cat2',function(v){{activeCat=v;}});
  </script>'''
    return page("벨루가 — 전체 상품", body)


# ---------------- wisinssa.html (위신싸관 — 가성비·떨이·임박) ----------------
def build_wisinssa():
    wss_events = [e for e in EVENTS if e["type"] == "wisinssa" and e["status"] == "live"]
    banners = ""
    for e in wss_events:
        banners += f'''      <a class="pbanner" href="events/{e['code']}/">
        <div class="pb-body">
          <div class="ptag">위신싸 떨이</div>
          <div class="ptt">{e['title']}</div>
          <div class="pperiod">{e['period']}</div>
          <div class="pdesc">{e['desc']}</div>
          {mbar(e)}
          <div class="pcta">떨이 보러 가기 →</div>
        </div>
        <img src="{e['img']}" alt="" />
      </a>\n'''
    wss = [p for p in PRODUCTS if p["lane"] == "wisinssa"]
    cards = ""
    for p in wss:
        c = card(p, "")
        c = c.replace('<div class="nm">', f'<span class="reason">{p["reason"]}</span>\n        <div class="nm">')
        cards += c + "\n"
    body = f'''{header("")}

  <!-- 위신싸 히어로 — 가성비 레인 전용 톤 -->
  <section class="wss-hero">
    <div class="mark rise d1">위신<b>싸</b></div>
    <div class="pun rise d2">앗! <b>위</b>스키가 <b>신</b>발보다 <b>싸</b>다!</div>
    <div class="d rise d2">도매상 창고의 과잉 재고·시즌 임박분을 통 크게 풉니다.<br />싸니까 빨리 — 소진되면 끝나요.</div>
  </section>

  <!-- 진행 중 떨이 이벤트 -->
  <section class="sec sec--tight" style="padding-top:30px;">
    <div class="row-head"><div class="t">진행 중 떨이</div></div>
{banners}  </section>

  <!-- 가성비 그리드 -->
  <section class="sec sec--tight">
    <div class="row-head"><div class="t">위신싸 상품</div><a class="more" href="products.html">전체상품 →</a></div>
  </section>
  <div class="grid" style="padding-top:0;">
{cards}
  </div>

{footer()}'''
    return page("위신싸 — 신발보다 싸다 · 벨루가 떨이관", body)


# ---------------- events/ (허브) ----------------
def build_events_hub():
    base = "../"
    live = [e for e in EVENTS if e["status"] == "live"]
    soon = [e for e in EVENTS if e["status"] == "upcoming"]
    ended = [e for e in EVENTS if e["status"] == "ended"]
    banners = ""
    for e in live:
        tag = MECH_LABEL.get(e.get("mech", ""), "기획전") if e["type"] != "promo" else "기획전"
        bar = mbar(e) if e["type"] != "promo" else ""
        banners += f'''      <a class="pbanner" href="{base}events/{e['code']}/">
        <div class="pb-body">
          <div class="ptag">{("위신싸 떨이" if e["type"]=="wisinssa" else tag)}</div>
          <div class="ptt">{e['title']}</div>
          <div class="pperiod">{e['period']}</div>
          <div class="pdesc">{e['desc']}</div>
          {bar}
          <div class="pcta">자세히 보기 →</div>
        </div>
        <img src="{e['img']}" alt="" />
      </a>\n'''
    if soon:
        banners += '      <div class="hub-divider">오픈 예정</div>\n'
        for e in soon:
            banners += f'''      <div class="pbanner pbanner--soon">
        <div class="pb-body">
          <div class="soon-badge">OPEN 예정</div>
          <div class="ptt">{e['title']}</div>
          <div class="pperiod">🕒 {e['open_at']}</div>
          <div class="pdesc">{e['desc']}</div>
          <a class="btn btn-ghost" style="margin-top:14px;padding:12px;font-size:14px;" href="{base}join.html">🔔 오픈 알림 받기</a>
        </div>
        <img src="{e['img']}" alt="" />
      </div>\n'''
    if ended:
        banners += '      <div class="hub-divider">종료된 이벤트</div>\n'
        for e in ended:
            banners += f'''      <div class="arch"><img src="{e['img']}" alt="" />
        <div><div class="tt">{e['title']}</div><div class="ds">{e['result']}</div></div>
        <span class="stamp">SOLD OUT</span></div>\n'''
    body = f'''{header(base)}

  <div class="ev-top">
    <div class="eyebrow eyebrow--amber">EVENTS</div>
    <h1>이벤트</h1>
    <div class="desc">공동 예약 · 사전 예약 · 선착순 한정과 위신싸 떨이까지 — 벨루가의 모든 이벤트.</div>
  </div>

  <div class="promo-hub">
{banners}  </div>

{footer()}'''
    return page("벨루가 — 이벤트", body, base=base)


# ---------------- events/<code>/ (이벤트 상세 — 단일 템플릿 + mech 분기) ----------------
CROWD_MODAL = '''
<div class="pay-overlay" id="payModal" onclick="if(event.target===this)closePay()">
  <div class="pay-sheet" role="dialog" aria-modal="true" aria-label="공동 예약">
    <div class="pay-grab"></div>
    <div class="pay-head"><span>공동 예약 결제</span><button class="pay-x" onclick="closePay()" aria-label="닫기">✕</button></div>
    <div class="pay-scroll">
      <div class="pay-order">
        <img src="__IMG__" alt="" />
        <div class="pay-order-info"><div class="t">__NAME__</div><div class="d">공동 예약 1병 · 목표 달성 시 __ETA__ 입고</div></div>
        <div class="pay-order-amt">__PRICE__</div>
      </div>
      <div class="crowd-note"><b>공동 예약 안내</b> — 지금 결제하면 예약이 확정됩니다. 마감일까지 목표 수량이 모이지 않으면 <b>전액 자동 환불</b>되며, 달성 시 입고 후 픽업 코드가 발급됩니다.</div>
      <div class="pay-sec">픽업 매장 선택</div>
      <div class="pay-store">
        <label class="ps"><input type="radio" name="ps" checked /><span>벨루가 픽업 · 강남점</span><span class="d">0.4km</span></label>
        <label class="ps"><input type="radio" name="ps" /><span>벨루가 픽업 · 역삼점</span><span class="d">0.9km</span></label>
        <label class="ps"><input type="radio" name="ps" /><span>벨루가 픽업 · 선릉점</span><span class="d">1.3km</span></label>
      </div>
      <div class="pay-sec">결제 수단</div>
      <div class="pay-easy">
        <button class="easy sel"><span class="tosspay">toss pay</span></button>
        <button class="easy"><span style="color:#03c75a;font-weight:800;">N</span> Pay</button>
        <button class="easy"><span style="color:#ffcd00;font-weight:900;">kakao</span> pay</button>
      </div>
      <label class="pay-agree-all"><input type="checkbox" id="agreeAll" /><span>전체 동의하기</span></label>
      <div class="pay-agree-sub">
        <label><input type="checkbox" class="agsub" /><span>(필수) 만 19세 이상이며 본인이 픽업합니다</span><i>›</i></label>
        <label><input type="checkbox" class="agsub" /><span>(필수) 목표 미달 시 자동 환불에 동의합니다</span><i>›</i></label>
        <label><input type="checkbox" class="agsub" /><span>(필수) 결제 서비스 이용약관, 개인정보 처리 동의</span><i>›</i></label>
      </div>
    </div>
    <div class="pay-foot"><button class="pay-cta" onclick="reserveDemo()">__PRICE__ 예약 결제</button></div>
  </div>
</div>
<script>
  function openPay(){ document.getElementById('payModal').classList.add('open'); document.body.style.overflow='hidden'; }
  function closePay(){ document.getElementById('payModal').classList.remove('open'); document.body.style.overflow=''; }
  function reserveDemo(){
    alert('공동 예약 결제는 데모입니다.\\n실연동 시: 결제 보관 → 목표 달성 시 확정·입고 → 픽업 코드 발급, 미달 시 전액 자동 환불.');
    closePay();
  }
  document.addEventListener('change',function(e){
    if(e.target.id==='agreeAll'){ document.querySelectorAll('.agsub').forEach(function(c){c.checked=e.target.checked;}); }
    if(e.target.classList&&e.target.classList.contains('agsub')){
      var all=document.querySelectorAll('.agsub'),on=document.querySelectorAll('.agsub:checked');
      document.getElementById('agreeAll').checked=all.length===on.length;
    }
  });
  document.addEventListener('keydown',function(e){ if(e.key==='Escape') closePay(); });
</script>'''


def mech_steps(e):
    if e["mech"] == "crowd":
        steps = [("예약 결제", "지금 결제하면 예약 확정. 달성 현황은 마이페이지에서 확인."),
                 ("목표 달성 → 입고", f'{e["goal"]}병이 모이면 벨루가가 확정 매입, {e.get("eta","")} 입고. 미달 시 전액 자동 환불.'),
                 ("픽업 (성인인증)", "입고 알림과 함께 픽업 코드 발급. 선택한 매장에서 신분증 확인 후 수령.")]
        notice = ('<div class="notice" style="margin-top:16px;">⚠️ <b>목표 미달 시 전액 자동 환불됩니다.</b> '
                  "공동 예약은 수량이 모여야 진행되는 방식이라, 마감일까지 목표에 못 미치면 결제가 자동 취소돼요.</div>")
    elif e["mech"] == "preorder":
        steps = [("사전 예약 결제", "국내 배정분이 확정된 물량이라 결제 즉시 구매가 확정됩니다."),
                 (f'{e.get("eta","")} 입고', "입고 즉시 알림과 함께 픽업 코드가 발급됩니다."),
                 ("픽업 (성인인증)", "선택한 매장에서 신분증 확인 후 수령.")]
        notice = (f'<div class="notice" style="margin-top:16px;">📦 <b>{e.get("eta","")} 입고 예정 상품입니다.</b> '
                  "결제는 지금, 픽업은 입고 이후에 가능해요. 입고되면 바로 알림을 드립니다.</div>")
    else:
        steps = [("결제", "보유 재고라 결제 즉시 픽업 코드가 발급됩니다."),
                 ("가까운 매장 선택", "내 주변 벨루가 픽업 매장 중 편한 곳을 고릅니다."),
                 ("당일 픽업 (성인인증)", "신분증 확인 후 바로 수령. 오늘 결제, 오늘 픽업.")]
        notice = ""
    html = "".join(
        f'<div class="step"><div class="n">{i+1}</div><div><div class="t">{t}</div><div class="d">{d}</div></div></div>'
        for i, (t, d) in enumerate(steps))
    return html, notice


def build_event_limited(e):
    base = "../../"
    p = PMAP[e["product"]]
    specs = "".join(f'<div class="sp"><div class="l">{l}</div><div class="v">{v}</div></div>' for l, v in e["specs"])
    source = "".join(f"<p>{s}</p>" for s in e["source"])
    inf = ""
    if e.get("inf"):
        inf = f'''
  <section class="sec sec--tight" style="padding-top:34px;">
    <div class="inf">
      <div class="ava">🥃</div>
      <div>
        <div class="who"><span class="lockup"><span class="hd">{e['inf']['handle']}</span><span class="x">×</span><span>벨루가</span></span></div>
        <div class="cmt">"{e['inf']['comment']}"</div>
      </div>
    </div>
  </section>'''
    steps_html, notice = mech_steps(e)
    others = [q for q in PRODUCTS if q["code"] != p["code"]][:4]
    cross = "\n".join(card(q, base) for q in others)

    # mech별 CTA / FAQ 첫 문항
    if e["mech"] == "crowd":
        cta_bar = (f'<div class="cta-bar"><div class="price"><div class="now">{p["now"]}</div></div>'
                   '<button type="button" class="btn btn-primary" style="background:var(--amber);color:var(--amber-ink);" '
                   'onclick="openPay()">공동 예약 참여하기</button></div>')
        faq1 = ('<details class="qa"><summary><span>목표에 못 미치면 어떻게 되나요?</span></summary>'
                '<p>마감일까지 목표 수량이 모이지 않으면 결제하신 금액 전액이 자동 환불됩니다. 별도 신청은 필요 없어요.</p></details>')
        tail_modal = (CROWD_MODAL.replace("__IMG__", e["img"]).replace("__NAME__", p["name"])
                      .replace("__PRICE__", p["now"]).replace("__ETA__", e.get("eta", "")))
    elif e["mech"] == "preorder":
        cta_bar = (f'''<div class="cta-bar"><div class="qty">
    <button type="button" data-qty-dec aria-label="수량 감소">−</button><span data-qty>1</span>
    <button type="button" data-qty-inc aria-label="수량 증가">+</button></div>
  <button type="button" class="btn btn-primary" data-add-cart>사전 예약 담기</button></div>''')
        faq1 = (f'<details class="qa"><summary><span>언제 받을 수 있나요?</span></summary>'
                f'<p>{e.get("eta","")} 입고 예정입니다. 입고되면 알림과 함께 픽업 코드가 발급되고, 그때부터 매장 픽업이 가능합니다.</p></details>')
        tail_modal = ""
    else:
        cta_bar = ('''<div class="cta-bar"><div class="qty">
    <button type="button" data-qty-dec aria-label="수량 감소">−</button><span data-qty>1</span>
    <button type="button" data-qty-inc aria-label="수량 증가">+</button></div>
  <button type="button" class="btn btn-primary" data-add-cart>장바구니 담기</button></div>''')
        faq1 = ('<details class="qa"><summary><span>오늘 바로 받을 수 있나요?</span></summary>'
                '<p>네. 보유 재고라 결제 즉시 픽업 코드가 발급되고, 매장 영업시간 내 당일 픽업이 가능합니다.</p></details>')
        tail_modal = ""

    pickup_note = ("결제 시 픽업 매장을 선택합니다. 매장을 누르면 네이버 지도에서 위치를 확인할 수 있어요."
                   if e["mech"] != "stock" else "매장을 누르면 네이버 지도에서 위치를 확인할 수 있어요. 당일 픽업 가능.")
    cart_data = (f'<div data-product data-code="{p["code"]}" data-name="{p["name"]}'
                 + (f' (사전 예약·{e.get("eta","")} 입고)' if e["mech"] == "preorder" else "")
                 + f'" data-img="{p["img"]}" data-price="{price_num(p)}" data-base="{base}" hidden></div>')

    body = f'''{header(base)}

  {cart_data}

  <!-- 이벤트 히어로 -->
  <section class="ev-hero">
    <div class="eh-in">
      <img src="{e['img']}" alt="" />
      <div style="flex:1;min-width:0;">
        {mech_chip(e)}
        <h1>{e['title']}</h1>
        <div class="pperiod">{e['period']}</div>
        <div class="price-line">{p['now']}</div>
      </div>
    </div>
    {mbar(e)}
    <span class="cdown" id="cd" data-deadline="{e['deadline']}"></span>
    <div class="ehdesc">{e['desc']}</div>
  </section>
{inf}

  <!-- 희소성 스펙 -->
  <section class="sec sec--tight" style="padding-top:36px;">
    <div class="eyebrow eyebrow--amber">WHY SO RARE</div>
    <div class="h2" style="font-size:21px;margin-bottom:14px;">이 보틀이 귀한 이유</div>
    <div class="specs">{specs}</div>
  </section>

  <!-- 소싱 스토리 -->
  <section class="sec sec--parchment">
    <div class="eyebrow">THE SOURCE</div>
    <div class="h2" style="font-size:21px;">이 보틀이 여기 있는 이유</div>
    <div class="story">{source}</div>
  </section>

  <!-- 테이스팅 노트 -->
  <section class="sec sec--tight" style="padding-top:38px;">
    <div class="eyebrow">TASTING NOTES</div>
    <p class="lead">{p['why']}</p>
    <div class="chips">
      <span class="chip">싱글몰트 스카치</span>
      <span class="chip">{SHARED['region'].split(',')[0]}</span>
      <span class="chip">{p['vol']} · {p['abv']}</span>
    </div>
    <div class="notes">
      <div class="row"><div class="k">AROMA</div><div>{p['aroma']}</div></div>
      <div class="row"><div class="k">PALATE</div><div>{p['palate']}</div></div>
      <div class="row"><div class="k">FINISH</div><div>{p['finish']}</div></div>
    </div>
  </section>

  <!-- 진행 방식 (mech 분기) -->
  <section class="sec sec--parchment">
    <div class="eyebrow">HOW IT WORKS</div>
    <div class="h2">{MECH_LABEL[e['mech']]}, 이렇게 진행돼요.</div>
    <div style="margin-top:8px;">{steps_html}</div>
    {notice}
    {LAW_BOX}
  </section>

{pickup_section(pickup_note)}

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
    {faq1}
    <details class="qa"><summary><span>성인인증은 어떻게 하나요?</span></summary><p>픽업 시 신분증으로 만 19세 이상 본인 확인 후 수령합니다.</p></details>
    <details class="qa"><summary><span>배송은 정말 안 되나요?</span></summary><p>네. 위스키 등은 주류법상 온라인 배송이 불가하며 매장 픽업만 가능합니다.</p></details>
    <details class="qa"><summary><span>환불되나요?</span></summary><p>픽업 전 결제 취소가 가능합니다. 공동 예약은 목표 미달 시 자동 환불됩니다. (세부 정책 추후 확정)</p></details>
  </section>

{footer()}'''
    tail = f'\n{cta_bar}\n{tail_modal}\n{STORE_SCRIPT}\n{COUNTDOWN_JS}'
    html = page(e["title"] + " — 벨루가", body, base=base)
    html = html.replace('<div class="wrap">', '<div class="wrap pad-cta">')
    html = html.replace('</div>\n<script src=', '</div>\n' + tail + '\n<script src=')
    return html


def build_event_listing(e):
    """wisinssa 떨이 / promo 기획전 — 상품 모음형 이벤트 상세"""
    base = "../../"
    prods = [PMAP[c] for c in e["products"] if c in PMAP]
    cards = "\n".join(card(q, base) for q in prods)
    feats = "\n".join(
        f'      <div class="step"><div class="n">{i+1}</div><div><div class="t">{t}</div><div class="d">{d}</div></div></div>'
        for i, (t, d) in enumerate(e["features"]))
    bar = mbar(e) if e.get("mech") else ""
    tag = "위신싸 떨이" if e["type"] == "wisinssa" else "기획전"
    body = f'''{header(base)}

  <section class="ev-hero">
    <div class="eh-in">
      <img src="{e['img']}" alt="" />
      <div style="flex:1;min-width:0;">
        <div class="ptag">{tag}</div>
        <h1>{e['title']}</h1>
        <div class="pperiod">{e['period']}</div>
      </div>
    </div>
    {bar}
    <div class="ehdesc">{e['desc']}</div>
  </section>

  <section class="sec sec--tight" style="padding-top:34px;">
    <div class="eyebrow eyebrow--amber">WHY</div>
    <div class="h2" style="font-size:21px;margin-bottom:6px;">이래서 좋아요</div>
    <div style="margin-top:8px;">
{feats}
    </div>
  </section>

  <section class="sec sec--tight">
    <div class="row-head"><div class="t">이벤트 상품</div><a class="more" href="{base}products.html">전체 →</a></div>
  </section>
  <div class="grid" style="padding-top:0;">
{cards}
  </div>

{footer()}'''
    return page(e["title"] + " — 벨루가", body, base=base)


# ---------------- product/<code>/ (일반·위신싸 상품 상세) ----------------
def build_product(p):
    base = "../../"
    others = [q for q in PRODUCTS if q["code"] != p["code"]][:4]
    cross = "\n".join(card(q, base) for q in others)
    foods_html = "".join(f'<div class="food"><div class="ic">{i}</div><div class="t">{t}</div></div>' for i, t in SHARED["foods"])
    story_html = "".join(f"<p>{s}</p>" for s in SHARED["story"])
    reason = f'<span class="reason">{p["reason"]}</span>' if p.get("reason") else ""
    kicker = "위신싸 · <b>떨이</b>" if p["lane"] == "wisinssa" else "벨루가 · 픽업 가능"
    body = f'''{header(base)}

  <div data-product data-code="{p['code']}" data-name="{p['name']}" data-img="{p['img']}" data-price="{price_num(p)}" data-base="{base}" hidden></div>

  <section class="pdp-media"><img src="{p['img']}" alt="{p['name']}" /></section>
  <section class="pdp-info">
    <div class="pdp-kicker">{kicker}</div>
    {reason}
    <h1 class="pdp-name">{p['name']}</h1>
    <div class="pdp-price">{price_html(p)}</div>
  </section>

  <!-- 원산지 -->
  <section class="sec sec--tight" style="padding-top:34px;">
    <div class="origin">
      <div>
        <div class="o"><span>🏞️</span><span>{SHARED['region']}</span></div>
        <div class="o"><span>🏛️</span><span>{SHARED['producer']}</span></div>
      </div>
      <div class="flag">{SHARED['flag']}</div>
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
    <div class="story">{story_html}</div>
  </section>

  <!-- 픽업 3단계 -->
  <section class="sec sec--tight" style="padding-top:38px;">
    <div class="eyebrow">HOW IT WORKS</div>
    <div class="h2">집 근처에서 3분이면 픽업.</div>
    <div style="margin-top:8px;">
      <div class="step"><div class="n">1</div><div><div class="t">온라인으로 결제</div><div class="d">결제하면 픽업 코드가 발급됩니다.</div></div></div>
      <div class="step"><div class="n">2</div><div><div class="t">가까운 픽업 매장 선택</div><div class="d">내 주변 벨루가 픽업 매장 중 편한 곳을 고릅니다.</div></div></div>
      <div class="step"><div class="n">3</div><div><div class="t">방문해서 픽업 (성인인증)</div><div class="d">신분증 확인 후 보틀을 받아갑니다. 끝!</div></div></div>
    </div>
    {LAW_BOX}
  </section>

{pickup_section("매장을 누르면 네이버 지도에서 위치를 확인할 수 있어요.")}

  <!-- 신뢰 -->
  <section class="sec sec--tight">
    <div class="trust-line">
      <span class="i">✅ <b>100% 정품</b></span>
      <span class="i">🏪 <b>동네 픽업</b></span>
      <span class="i">🔞 <b>성인 픽업</b></span>
    </div>
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
    <details class="qa"><summary><span>픽업 기한이 있나요?</span></summary><p>결제 후 7일 이내 선택한 매장에서 픽업해 주세요.</p></details>
    <details class="qa"><summary><span>성인인증은 어떻게 하나요?</span></summary><p>픽업 시 신분증으로 만 19세 이상 본인 확인 후 수령합니다.</p></details>
    <details class="qa"><summary><span>배송은 정말 안 되나요?</span></summary><p>네. 위스키 등은 주류법상 온라인 배송이 불가하며 매장 픽업만 가능합니다.</p></details>
  </section>

{footer()}'''
    tail = '''
<div class="cta-bar">
  <div class="qty">
    <button type="button" data-qty-dec aria-label="수량 감소">−</button>
    <span data-qty>1</span>
    <button type="button" data-qty-inc aria-label="수량 증가">+</button>
  </div>
  <button type="button" class="btn btn-primary" data-add-cart>장바구니 담기</button>
</div>
''' + STORE_SCRIPT
    html = page(p["name"] + " — 벨루가", body, base=base)
    html = html.replace('<div class="wrap">', '<div class="wrap pad-cta">')
    html = html.replace('</div>\n<script src=', '</div>\n' + tail + '\n<script src=')
    return html


# ---------------- about.html — 소싱 권위 ----------------
def build_about():
    body = f'''{header("")}

  <section class="hero hero--dark" style="padding:72px var(--pad);text-align:center;min-height:70vh;display:flex;flex-direction:column;justify-content:center;">
    <div class="inner">
      <div class="mark rise d1" style="font-size:clamp(64px,22vw,110px);">벨루<b>가</b></div>
      <div class="rise d2" style="font-size:17px;color:rgba(255,255,255,.82);margin-top:20px;line-height:1.72;letter-spacing:-0.015em;">
        전국 13,000개 매장에 술을 대는 도매상이<br /><em style="color:var(--amber);font-style:normal;font-weight:700;">직접 엽니다.</em>
      </div>
    </div>
  </section>

  <section class="sec">
    <div class="eyebrow eyebrow--amber">THE SOURCE</div>
    <div class="h2">왜 벨루가에만<br />이 보틀이 있을까요?</div>
    <p class="lead">캐스크 단위 물량, 국가별 배정 보틀, 수입사 마지막 재고 — 이런 술은 소매 매장 진열대에 오르기 전에 사라집니다. 벨루가는 <b style="color:var(--ink);">전국 13,000개 매장에 23,000종의 술을 공급하는 주류 도매상</b>이라, 그 물량을 공급망에서 직접 가져옵니다.</p>
  </section>

  <section class="sec sec--tight">
    <div style="margin-top:6px;">
      <div class="step"><div class="n">1</div><div><div class="t">공동 예약 — 모이면 엽니다</div><div class="d">아직 들여오지 않은 캐스크를 예약이 모이면 직접 매입. 목표 미달 시 전액 자동 환불.</div></div></div>
      <div class="step"><div class="n">2</div><div><div class="t">사전 예약 — 확보했습니다</div><div class="d">국내 배정이 확정된 얼로케이션 보틀을 입고 전에 먼저. 결제 즉시 구매 확정.</div></div></div>
      <div class="step"><div class="n">3</div><div><div class="t">선착순 — 지금 있습니다</div><div class="d">보유 재고 한정 수량. 결제 즉시 픽업 코드 발급, 오늘 픽업.</div></div></div>
    </div>
  </section>

  <section class="sec sec--parchment">
    <div class="eyebrow">HOW IT WORKS</div>
    <div class="h2">받는 방법은 하나, 픽업.</div>
    <div style="margin-top:8px;">
      <div class="step"><div class="n">1</div><div><div class="t">온라인 결제</div><div class="d">원하는 보틀을 결제하면 픽업 코드 발급 (이벤트 유형별 발급 시점 상이).</div></div></div>
      <div class="step"><div class="n">2</div><div><div class="t">가까운 매장 선택</div><div class="d">내 주변 벨루가 픽업 매장 중 편한 곳 선택.</div></div></div>
      <div class="step"><div class="n">3</div><div><div class="t">방문 픽업 (성인인증)</div><div class="d">신분증 확인 후 수령. 배송 기다릴 필요 없어요.</div></div></div>
    </div>
    <div class="law" style="margin-top:18px;">📌 주류는 법상 온라인 배송이 불가합니다(전통주 제외). 온라인 결제 후 매장에서 받는 <b>스마트오더</b>가 합법적인 방식이며, 벨루가는 이 방식을 따릅니다.</div>
  </section>

  <section class="sec">
    <div class="eyebrow">TRUST</div>
    <div class="h2">도매상이 파니까, 전부 정품.</div>
    <p class="lead">벨루가의 모든 보틀은 정식 수입·유통 경로를 거친 <b style="color:var(--ink);">100% 정품</b>입니다. 결제·픽업 전 과정에서 만 19세 이상 성인인증을 거치며, 미성년자에게는 판매하지 않습니다.</p>
  </section>

  <section class="sec sec--tight">
    <a href="events/" class="btn btn-primary" style="margin-bottom:10px;">진행 중 이벤트 보기 →</a>
    <a href="join.html" class="btn btn-ghost">벨루가 회원가입 →</a>
  </section>

{footer()}'''
    return page("벨루가 — 도매상이 직접 엽니다", body)


# ---------------- mypage.html (5단계 진행바) ----------------
def build_mypage():
    body = f'''{header("")}

  <!-- 비회원(게스트) 뷰 -->
  <div id="guestView" style="display:none;">
    <div class="guest-hero">
      <div class="avt"><svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="8" r="4"/><path d="M4 21c0-4 4-6 8-6s8 2 8 6"/></svg></div>
      <div class="gt">로그인하고<br /><b>벨루가 혜택</b>을 받아보세요.</div>
      <div class="gd">비회원도 가격·이벤트는 자유롭게 둘러볼 수 있어요. 예약·픽업 코드 관리와 장바구니·결제는 회원만 이용할 수 있습니다.</div>
      <a href="join.html" class="btn btn-primary">회원가입 →</a>
      <a href="#" class="btn btn-ghost" id="loginBtn">이미 회원이에요 · 로그인(데모)</a>
    </div>
    <section class="sec sec--tight" style="padding-top:28px;">
      <div class="guest-warn">🔞 <div><b>만 19세 이상</b>만 구매·픽업할 수 있어요. 결제·픽업 시 신분증으로 <b>성인 본인인증</b>을 거칩니다.</div></div>
    </section>
    <section class="sec sec--tight">
      <a href="events/" class="btn btn-ghost" style="margin-bottom:10px;">진행 중 이벤트 보기 →</a>
      <a href="products.html" class="btn btn-ghost">전체 상품 둘러보기 →</a>
    </section>
  </div>

  <!-- 회원 뷰 -->
  <div id="memberView">
  <div class="prof">
    <div class="avt">벨</div>
    <div>
      <div class="nm">위스키러버 님</div>
      <div class="sub">010-••••-1234 · 일반 회원</div>
    </div>
  </div>

  <!-- 진행 중 주문 — 공동 예약 (5단계: 예약·주문 → 목표 달성 → 입고 → 픽업 가능 → 완료) -->
  <section class="sec sec--tight">
    <div class="row-head"><div class="t">진행 중</div></div>
    <div class="waitwrap" style="margin-bottom:13px;">
      <a class="waitcard" href="events/0101/">
        <img src="{IMG['sherry']}" alt="" />
        <div>
          <div class="t">탐나불린 18년 싱글 캐스크</div>
          <div class="d">공동 예약 중 · 24/30병 달성 · 마감 6/19</div>
        </div>
        <div class="code"><div class="lbl">상태</div><div class="v" style="color:#9a6a14;">예약 중</div></div>
      </a>
      <div class="pickup-prog">
        <div class="pp-track pp-5">
          <div class="pp-fill" style="width:0%;"></div>
          <div class="pp-step curr"><span class="pp-dot"></span><span class="pp-lbl">예약 완료</span></div>
          <div class="pp-step"><span class="pp-dot"></span><span class="pp-lbl">목표 달성</span></div>
          <div class="pp-step"><span class="pp-dot"></span><span class="pp-lbl">입고</span></div>
          <div class="pp-step"><span class="pp-dot"></span><span class="pp-lbl">픽업 가능</span></div>
          <div class="pp-step"><span class="pp-dot"></span><span class="pp-lbl">픽업 완료</span></div>
        </div>
      </div>
    </div>

    <!-- 선착순 주문 — 픽업 가능 -->
    <div class="waitwrap">
      <a class="waitcard" href="events/0103/">
        <img src="{IMG['pinot']}" alt="" />
        <div>
          <div class="t">탐나불린 피노 누아</div>
          <div class="d">벨루가 픽업 · 강남점 · ~6/18까지</div>
        </div>
        <div class="code"><div class="lbl">픽업코드</div><div class="v">VLG-4821</div></div>
      </a>
      <div class="pickup-prog">
        <div class="pp-track pp-5">
          <div class="pp-fill" style="width:60%;"></div>
          <div class="pp-step done"><span class="pp-dot"></span><span class="pp-lbl">주문</span></div>
          <div class="pp-step done"><span class="pp-dot"></span><span class="pp-lbl">—</span></div>
          <div class="pp-step done"><span class="pp-dot"></span><span class="pp-lbl">재고 확보</span></div>
          <div class="pp-step curr"><span class="pp-dot"></span><span class="pp-lbl">픽업 가능</span></div>
          <div class="pp-step"><span class="pp-dot"></span><span class="pp-lbl">픽업 완료</span></div>
        </div>
      </div>
    </div>
  </section>

  <!-- 찜한 보틀 -->
  <section class="sec sec--tight">
    <div class="row-head"><div class="t">찜한 보틀</div><a class="more" href="products.html">전체 →</a></div>
    <div class="carousel">
{card(PMAP["1002"], "")}
{card(PMAP["0003"], "")}
{card(PMAP["0008"], "")}
    </div>
  </section>

  <!-- 메뉴 -->
  <section class="sec sec--tight">
    <a class="mrow" href="events/0101/">주문 · 예약 내역<span class="r">3건</span></a>
    <a class="mrow" href="events/">오픈 알림<span class="r">2개</span></a>
    <a class="mrow" href="#">알림 설정<span class="r"></span></a>
    <div class="mrow">본인인증 정보<span class="r">인증완료</span></div>
    <a class="mrow" href="https://pf.kakao.com/_veluga/chat" target="_blank" rel="noopener">고객센터<span class="r">카카오 채널</span></a>
    <a class="mrow" href="#" id="logoutBtn" style="color:var(--ink-48);">로그아웃<span class="r" style="font-size:0;"></span></a>
  </section>
  </div><!-- /memberView -->

{footer()}

  <script>
    (function () {{
      var guest = document.getElementById('guestView'), member = document.getElementById('memberView');
      function render() {{
        var m = VLGCart.isMember();
        guest.style.display = m ? 'none' : '';
        member.style.display = m ? '' : 'none';
      }}
      render();
      var lo = document.getElementById('logoutBtn');
      if (lo) lo.addEventListener('click', function (e) {{ e.preventDefault(); VLGCart.setMember(false); location.reload(); }});
      var li = document.getElementById('loginBtn');
      if (li) li.addEventListener('click', function (e) {{ e.preventDefault(); VLGCart.setMember(true); location.reload(); }});
    }})();
  </script>'''
    return page("벨루가 — 마이페이지", body)


# ---------------- cart.html ----------------
CART_SCRIPT = '''  <script>
  function renderCart(){
    var items=VLGCart.read();
    var wrap=document.getElementById('cartWrap'), empty=document.getElementById('cartEmpty'),
        bar=document.getElementById('checkoutBar'), list=document.getElementById('cartList');
    if(!items.length){
      wrap.style.display='none'; bar.style.display='none'; empty.style.display='block';
      document.getElementById('sumCount').textContent='0';
      return;
    }
    wrap.style.display=''; bar.style.display='flex'; empty.style.display='none';
    list.innerHTML=items.map(function(i){
      return '<div class="citem" data-code="'+i.code+'">'
        +'<img src="'+i.img+'" alt="" />'
        +'<div class="ci-info">'
          +'<span class="ci-nm">'+i.name+'</span>'
          +'<div class="ci-pr">'+VLGCart.won(i.price)+'</div>'
          +'<span class="ci-rm" data-rm>삭제</span>'
        +'</div>'
        +'<div class="qty"><button type="button" data-cdec aria-label="수량 감소">−</button>'
          +'<span data-qty>'+i.qty+'</span>'
          +'<button type="button" data-cinc aria-label="수량 증가">+</button></div>'
      +'</div>';
    }).join('');
    var c=VLGCart.count(), tot=VLGCart.won(VLGCart.total());
    document.getElementById('sumCount').textContent=c;
    document.getElementById('sumSubtotal').textContent=tot;
    document.getElementById('sumTotal').textContent=tot;
    document.getElementById('barTotal').textContent=tot;
    document.getElementById('payTotal').textContent=tot;
    document.getElementById('payCount').textContent=c;
    document.getElementById('payCta').textContent=tot+' 결제하기';
  }
  document.addEventListener('click',function(e){
    var row=e.target.closest && e.target.closest('.citem');
    if(!row) return;
    var code=row.getAttribute('data-code');
    if(e.target.closest('[data-rm]')){ VLGCart.remove(code); renderCart(); return; }
    var cur=VLGCart.read().filter(function(i){return i.code===code;})[0];
    if(!cur) return;
    if(e.target.closest('[data-cinc]')){ VLGCart.setQty(code,cur.qty+1); renderCart(); }
    else if(e.target.closest('[data-cdec]')){ VLGCart.setQty(code,cur.qty-1); renderCart(); }
  });
  function openPay(){ document.getElementById('payModal').classList.add('open'); document.body.style.overflow='hidden'; }
  function closePay(){ document.getElementById('payModal').classList.remove('open'); document.body.style.overflow=''; }
  function payDemo(){
    alert('결제는 데모입니다. 실연동 시 토스페이먼츠 결제위젯 SDK로 대체됩니다.\\n선착순 상품은 즉시, 사전 예약 상품은 입고 시 픽업 코드가 발급됩니다.');
    VLGCart.clear(); closePay(); renderCart();
  }
  document.addEventListener('change',function(e){
    if(e.target.id==='agreeAll'){ document.querySelectorAll('.agsub').forEach(function(c){c.checked=e.target.checked;}); }
    if(e.target.classList.contains('agsub')){
      var all=document.querySelectorAll('.agsub'),on=document.querySelectorAll('.agsub:checked');
      document.getElementById('agreeAll').checked=all.length===on.length;
    }
  });
  document.addEventListener('keydown',function(e){ if(e.key==='Escape') closePay(); });
  renderCart();
  </script>'''


def build_cart():
    body = f'''{header("")}

  <div class="cart-top">
    <h1>장바구니</h1>
    <div class="cnt"><span id="sumCount">0</span>병 담김 · 한 번에 결제</div>
  </div>

  <div id="cartWrap" style="display:none;">
    <div class="cart-list" id="cartList"></div>
    <div class="cart-sum">
      <div class="row"><span>상품 합계</span><span id="sumSubtotal">0원</span></div>
      <div class="row"><span>픽업 수수료</span><span>0원</span></div>
      <div class="row total"><span>결제 예정 금액</span><span class="amt" id="sumTotal">0원</span></div>
    </div>
    <div class="cart-note">📌 주류는 온라인 배송이 불가합니다. 결제 후 선택한 벨루가 픽업 매장에서 신분증 확인(만 19세 이상) 후 직접 픽업해 주세요. <b>사전 예약 상품은 입고 후 픽업 코드가 발급됩니다.</b> 공동 예약은 장바구니 없이 이벤트 페이지에서 단독 결제됩니다.</div>
  </div>

  <div class="cart-empty" id="cartEmpty" style="display:none;">
    <div class="ce-ic">🛒</div>
    <div class="ce-t">장바구니가 비어 있어요</div>
    <div class="ce-d">담아둔 보틀이 아직 없어요. 진행 중인 한정 이벤트를 둘러보세요.</div>
    <a href="events/" class="btn btn-primary btn-inline">이벤트 보기 →</a>
  </div>

{footer()}'''
    tail = '''
<div class="cta-bar" id="checkoutBar" style="display:none;">
  <div class="price"><div class="now" id="barTotal">0원</div></div>
  <button type="button" class="btn btn-primary" onclick="openPay()">결제하기</button>
</div>

<div class="pay-overlay" id="payModal" onclick="if(event.target===this)closePay()">
  <div class="pay-sheet" role="dialog" aria-modal="true" aria-label="결제하기">
    <div class="pay-grab"></div>
    <div class="pay-head"><span>주문 / 결제</span><button class="pay-x" onclick="closePay()" aria-label="닫기">✕</button></div>
    <div class="pay-scroll">
      <div class="pay-order">
        <div class="pay-order-info"><div class="t"><span id="payCount">0</span>개 상품</div><div class="d">벨루가 픽업 · 강남점</div></div>
        <div class="pay-order-amt" id="payTotal">0원</div>
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
    <div class="pay-foot"><button class="pay-cta" id="payCta" onclick="payDemo()">결제하기</button></div>
  </div>
</div>
''' + CART_SCRIPT
    html = page("벨루가 — 장바구니", body)
    html = html.replace('<div class="wrap">', '<div class="wrap pad-cta">')
    html = html.replace('</div>\n<script src=', '</div>\n' + tail + '\n<script src=')
    return html


# ---------------- join.html ----------------
def build_join():
    body = f'''{header("")}

  <section class="sec">
    <div class="eyebrow eyebrow--amber">JOIN</div>
    <div class="h2">벨루가 가입하기</div>
    <p class="lead" style="margin-bottom:26px;">30초면 끝. 가입하고 한정 이벤트 오픈 알림과 첫 픽업 혜택을 받아보세요.</p>

    <div class="field">
      <label>이름</label>
      <input class="inp" type="text" placeholder="이름을 입력하세요" />
    </div>
    <div class="field">
      <label>휴대폰 번호</label>
      <div class="row">
        <input class="inp" type="tel" inputmode="numeric" placeholder="010-0000-0000" />
        <button onclick="alert('인증번호를 전송했어요. (데모)')">인증요청</button>
      </div>
    </div>
    <div class="field">
      <label>인증번호</label>
      <div class="row">
        <input class="inp" type="text" inputmode="numeric" placeholder="6자리 입력" />
        <button onclick="alert('인증되었어요. (데모)')">확인</button>
      </div>
    </div>

    <div class="join-agree">
      <label class="all"><input type="checkbox" id="agreeAll" /><span>전체 동의하기</span></label>
      <label><input type="checkbox" class="agsub" /><span>(필수) 만 19세 이상이며 본인이 픽업합니다</span></label>
      <label><input type="checkbox" class="agsub" /><span>(필수) 이용약관 및 개인정보 처리 동의</span></label>
      <label><input type="checkbox" class="agsub" /><span>(선택) 한정 이벤트 오픈 · 혜택 알림 수신</span></label>
    </div>

    <a href="#" class="btn btn-primary" onclick="joinDemo();return false;">가입하기</a>
  </section>

{footer()}

  <script>
    document.addEventListener('change', function(e){{
      if(e.target.id==='agreeAll'){{ document.querySelectorAll('.agsub').forEach(function(c){{c.checked=e.target.checked;}}); }}
      if(e.target.classList.contains('agsub')){{
        var all=document.querySelectorAll('.agsub'),on=document.querySelectorAll('.agsub:checked');
        document.getElementById('agreeAll').checked=all.length===on.length;
      }}
    }});
    function joinDemo(){{ try{{ localStorage.setItem('vlg_member','1'); }}catch(e){{}} alert('가입 완료! (데모) 마이페이지로 이동합니다.'); location.href='mypage.html'; }}
  </script>'''
    return page("벨루가 — 회원가입", body)


# ---------------- 빌드 ----------------
def write(path, html):
    full = os.path.join(ROOT, path)
    if os.path.dirname(full) != ROOT:
        os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(html)
    print("  wrote", path)


def main():
    print("building 벨루가 B2C v2 pages…")
    write("index.html", build_index())
    write("products.html", build_products())
    write("wisinssa.html", build_wisinssa())
    write("about.html", build_about())
    write("mypage.html", build_mypage())
    write("cart.html", build_cart())
    write("join.html", build_join())
    write("events/index.html", build_events_hub())
    for e in EVENTS:
        if e["status"] != "live":
            continue  # upcoming·ended: 허브/메인 배너만, 상세 없음
        if e["type"] == "limited":
            write(f"events/{e['code']}/index.html", build_event_limited(e))
        else:
            write(f"events/{e['code']}/index.html", build_event_listing(e))
    for p in PRODUCTS:
        if p["lane"] == "limited":
            continue  # 한정 단일 보틀: 이벤트 상세가 곧 상품 페이지
        write(f"product/{p['code']}/index.html", build_product(p))
    print("done.")


if __name__ == "__main__":
    main()
