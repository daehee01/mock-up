/* 벨루가 장바구니 — localStorage 기반 (목업)
   - 모든 페이지에서 nav 배지 갱신
   - 상품 상세: [data-qty-inc/dec] 수량 조절 + [data-add-cart] 담기
   - cart.html: VLGCart API로 목록/합계 렌더 + 일괄 결제 */
(function () {
  var KEY = "vlg_cart";

  function read() {
    try { return JSON.parse(localStorage.getItem(KEY)) || []; }
    catch (e) { return []; }
  }
  function write(c) { localStorage.setItem(KEY, JSON.stringify(c)); badge(); }
  function count() { return read().reduce(function (n, i) { return n + i.qty; }, 0); }
  function total() { return read().reduce(function (s, i) { return s + i.price * i.qty; }, 0); }
  function won(n) { return (n || 0).toLocaleString("ko-KR") + "원"; }

  function badge() {
    var n = count();
    [].forEach.call(document.querySelectorAll("[data-cart-badge]"), function (b) {
      b.textContent = n;
      b.style.display = n > 0 ? "" : "none";
    });
  }

  function toast(msg) {
    var t = document.querySelector(".toast");
    if (!t) { t = document.createElement("div"); t.className = "toast"; document.body.appendChild(t); }
    t.innerHTML = msg;
    requestAnimationFrame(function () { t.classList.add("show"); });
    clearTimeout(t._h);
    t._h = setTimeout(function () { t.classList.remove("show"); }, 2600);
  }

  // 회원 상태 (데모) — 미설정 시 회원으로 간주(기존 데모 보존). mypage 로그인/로그아웃으로 전환.
  var MKEY = "vlg_member";
  function isMember() { var v = localStorage.getItem(MKEY); return v === null ? true : v === "1"; }
  function setMember(v) { localStorage.setItem(MKEY, v ? "1" : "0"); }

  // 비회원 가입 게이트 모달 (장바구니 담기 클릭 시)
  function showJoinGate(base) {
    var ov = document.querySelector(".gate-overlay");
    if (!ov) {
      ov = document.createElement("div");
      ov.className = "gate-overlay";
      ov.innerHTML =
        '<div class="gate-box" role="dialog" aria-modal="true">' +
          '<div class="gate-ic">🔐</div>' +
          '<div class="gate-t">회원가입이 필요해요!</div>' +
          '<div class="gate-d">장바구니 담기·결제는 벨루가 회원만 이용할 수 있어요. 둘러보기·가격·프로모션은 자유롭게 보실 수 있습니다.</div>' +
          '<div class="gate-warn">🔞 주류는 <b>만 19세 이상</b>만 구매·픽업할 수 있으며, 결제·픽업 시 <b>성인 본인인증</b>이 반드시 필요합니다.</div>' +
          '<a class="btn btn-primary" href="' + base + 'join.html">회원가입 하러 가기 →</a>' +
          '<button type="button" class="gate-close">다음에 할게요</button>' +
        '</div>';
      document.body.appendChild(ov);
      ov.addEventListener("click", function (e) {
        if (e.target === ov || (e.target.closest && e.target.closest(".gate-close"))) closeGate();
      });
    }
    requestAnimationFrame(function () { ov.classList.add("open"); });
    document.body.style.overflow = "hidden";
  }
  function closeGate() {
    var ov = document.querySelector(".gate-overlay");
    if (ov) ov.classList.remove("open");
    document.body.style.overflow = "";
  }
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") closeGate(); });

  var Cart = {
    read: read, write: write, count: count, total: total, won: won, badge: badge,
    isMember: isMember, setMember: setMember,
    add: function (it) {
      var c = read(), f = null, i;
      for (i = 0; i < c.length; i++) { if (c[i].code === it.code) { f = c[i]; break; } }
      if (f) { f.qty += it.qty; } else { c.push(it); }
      write(c);
    },
    setQty: function (code, q) {
      var c = read(), i;
      for (i = 0; i < c.length; i++) { if (c[i].code === code) { c[i].qty = Math.max(1, q); } }
      write(c);
    },
    remove: function (code) { write(read().filter(function (i) { return i.code !== code; })); },
    clear: function () { write([]); }
  };
  window.VLGCart = Cart;

  // 상품 상세 공용: 수량 스테퍼 + 장바구니 담기
  document.addEventListener("click", function (e) {
    if (!e.target.closest) return;
    var inc = e.target.closest("[data-qty-inc]");
    var dec = e.target.closest("[data-qty-dec]");
    var add = e.target.closest("[data-add-cart]");

    if (inc || dec) {
      var wrap = (inc || dec).closest(".qty");
      if (!wrap) return;
      var el = wrap.querySelector("[data-qty]");
      var v = parseInt(el.textContent, 10) || 1;
      el.textContent = inc ? v + 1 : Math.max(1, v - 1);
    }

    if (add) {
      var p = document.querySelector("[data-product]");
      if (!p) return;
      var base = p.getAttribute("data-base") || "";
      if (!isMember()) { showJoinGate(base); return; }  // 비회원: 담기 대신 가입 게이트
      var qel = document.querySelector("[data-qty]");
      var q = qel ? (parseInt(qel.textContent, 10) || 1) : 1;
      Cart.add({
        code: p.getAttribute("data-code"),
        name: p.getAttribute("data-name"),
        img: p.getAttribute("data-img"),
        price: parseInt(p.getAttribute("data-price"), 10) || 0,
        qty: q
      });
      toast('장바구니에 담았어요 · <a href="' + base + 'cart.html">장바구니 보기 →</a>');
    }
  });

  document.addEventListener("DOMContentLoaded", badge);
  badge();
})();
