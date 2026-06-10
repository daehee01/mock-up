/* 위신싸 장바구니 — localStorage 기반 (목업)
   - 모든 페이지에서 nav 배지 갱신
   - 상품 상세: [data-qty-inc/dec] 수량 조절 + [data-add-cart] 담기
   - cart.html: WSSCart API로 목록/합계 렌더 + 일괄 결제 */
(function () {
  var KEY = "wss_cart";

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

  var Cart = {
    read: read, write: write, count: count, total: total, won: won, badge: badge,
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
  window.WSSCart = Cart;

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
      var qel = document.querySelector("[data-qty]");
      var q = qel ? (parseInt(qel.textContent, 10) || 1) : 1;
      Cart.add({
        code: p.getAttribute("data-code"),
        name: p.getAttribute("data-name"),
        img: p.getAttribute("data-img"),
        price: parseInt(p.getAttribute("data-price"), 10) || 0,
        qty: q
      });
      var base = p.getAttribute("data-base") || "";
      toast('장바구니에 담았어요 · <a href="' + base + 'cart.html">장바구니 보기 →</a>');
    }
  });

  document.addEventListener("DOMContentLoaded", badge);
  badge();
})();
