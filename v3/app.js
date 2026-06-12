// 벨루가 B2C v3 — 공용 스크립트 (팔로우 · 라이브러리 저장 · 검색 · 결제 시트 · 마이)
// localStorage 키는 v1/v2와 분리: vlg3_follow / vlg3_lib / vlg3_orders
var VLG3 = (function () {
  var FKEY = 'vlg3_follow', LKEY = 'vlg3_lib', OKEY = 'vlg3_orders';

  function read(k) { try { return JSON.parse(localStorage.getItem(k)) || []; } catch (e) { return []; } }
  function save(k, v) { localStorage.setItem(k, JSON.stringify(v)); }

  // ---- 팔로우 ----
  function follows() { return read(FKEY); }
  function isF(c) { return follows().indexOf(c) >= 0; }

  function toggle(c) {
    var a = follows(), i = a.indexOf(c);
    if (i >= 0) a.splice(i, 1); else a.push(c);
    save(FKEY, a); sync();
    toast(i >= 0 ? '팔로우를 취소했어요' : '팔로우했어요 — 라이브러리에 모아드려요');
  }

  function sync() {
    document.querySelectorAll('[data-follow]').forEach(function (b) {
      var on = isF(b.getAttribute('data-follow'));
      b.classList.toggle('on', on);
      b.textContent = on ? '팔로잉' : '팔로우';
    });
    var sec = document.getElementById('feed-follow');
    if (sec) {
      var any = false;
      sec.querySelectorAll('[data-inf]').forEach(function (c) {
        var show = isF(c.getAttribute('data-inf'));
        c.style.display = show ? '' : 'none';
        if (show) any = true;
      });
      var em = document.getElementById('follow-empty');
      if (em) em.style.display = any ? 'none' : '';
    }
    syncSaves();
  }

  // ---- 라이브러리 (저장한 보틀) ----
  function lib() { return read(LKEY); }
  function inLib(code) { return lib().some(function (b) { return b.code === code; }); }

  function toggleLib(btn) {
    var t = btn.closest('.track');
    if (!t) return;
    var code = t.getAttribute('data-code');
    var a = lib(), idx = a.findIndex(function (b) { return b.code === code; });
    if (idx >= 0) { a.splice(idx, 1); toast('라이브러리에서 뺐어요'); }
    else {
      a.unshift({
        code: code,
        name: t.getAttribute('data-name'),
        img: t.getAttribute('data-img'),
        price: t.getAttribute('data-price'),
        vol: t.getAttribute('data-vol')
      });
      toast('라이브러리에 저장했어요 ♥');
    }
    save(LKEY, a); syncSaves();
  }

  function syncSaves() {
    document.querySelectorAll('.track [data-save]').forEach(function (b) {
      var t = b.closest('.track');
      var on = t && inLib(t.getAttribute('data-code'));
      b.classList.toggle('on', !!on);
      b.textContent = on ? '♥' : '♡';
    });
  }

  // ---- 인플루언서 검색 (홈) ----
  function search(q) {
    q = (q || '').trim().toLowerCase();
    var any = false;
    document.querySelectorAll('#sec-rec [data-inf-search]').forEach(function (el) {
      var hit = !q || el.getAttribute('data-inf-search').toLowerCase().indexOf(q) >= 0;
      el.style.display = hit ? '' : 'none';
      if (hit) any = true;
    });
    document.querySelectorAll('#sec-hot [data-inf-search]').forEach(function (el) {
      el.style.display = (!q || el.getAttribute('data-inf-search').toLowerCase().indexOf(q) >= 0) ? '' : 'none';
    });
    var em = document.getElementById('inf-empty');
    if (em) em.style.display = any ? 'none' : '';
  }

  // ---- 결제 시트 ----
  var cur = null;
  function openPay(el) {
    cur = {
      code: el.getAttribute('data-code'),
      name: el.getAttribute('data-name'),
      img: el.getAttribute('data-img'),
      price: el.getAttribute('data-price'),
      vol: el.getAttribute('data-vol')
    };
    document.getElementById('pay-img').src = cur.img;
    document.getElementById('pay-name').textContent = cur.name;
    document.getElementById('pay-vol').textContent = cur.vol + ' · 1병 · 매장 픽업';
    document.getElementById('pay-price').textContent = cur.price;
    document.getElementById('pay').classList.add('open');
    document.body.style.overflow = 'hidden';
  }
  function closePay() {
    document.getElementById('pay').classList.remove('open');
    document.body.style.overflow = '';
  }
  function selEasy(btn) {
    btn.parentElement.querySelectorAll('.easy').forEach(function (b) { b.classList.remove('sel'); });
    btn.classList.add('sel');
  }
  function agreeAll(box) {
    document.querySelectorAll('.pay-req').forEach(function (c) { c.checked = box.checked; });
  }
  function payNow() {
    var all = Array.prototype.every.call(document.querySelectorAll('.pay-req'), function (c) { return c.checked; });
    if (!all) { toast('필수 약관에 모두 동의해 주세요'); return; }
    var store = (document.querySelector('input[name="pstore"]:checked') || {}).value || '강남점';
    var code = 'VLG-' + String(Math.floor(1000 + Math.random() * 9000));
    var a = read(OKEY);
    a.unshift({ code: cur.code, name: cur.name, img: cur.img, price: cur.price, store: store, pickup: code });
    save(OKEY, a);
    closePay();
    toast('결제 완료(데모) — 픽업 코드 ' + code);
  }

  // ---- 내 라이브러리 페이지 ----
  function trackRow(b) {
    return '<div class="track" data-code="' + b.code + '" data-name="' + b.name + '" data-img="' + b.img +
      '" data-price="' + b.price + '" data-vol="' + b.vol + '" onclick="VLG3.openPay(this)">' +
      '<span class="cover"><img src="' + b.img + '" alt="" loading="lazy" /></span>' +
      '<div class="ti"><div class="nm">' + b.name + '</div><div class="mt">' + b.vol + '</div></div>' +
      '<div class="tr"><div class="price"><span class="now">' + b.price + '</span></div>' +
      '<div class="acts"><button type="button" class="save on" data-save aria-label="라이브러리에서 빼기" ' +
      'onclick="event.stopPropagation();VLG3.toggleLib(this);VLG3.renderLibrary(window.__infs||[])">♥</button>' +
      '<button type="button" class="buy">구매</button></div></div></div>';
  }

  function renderLibrary(infs) {
    window.__infs = infs;
    var bs = lib();
    var bw = document.getElementById('lib-bottles');
    if (bw) {
      bw.innerHTML = bs.map(trackRow).join('');
      document.getElementById('lib-bottles-empty').style.display = bs.length ? 'none' : '';
      var cnt = document.getElementById('lib-cnt');
      if (cnt) cnt.textContent = bs.length || '';
    }
    var fw = document.getElementById('my-follows');
    if (fw) {
      var fl = follows();
      fw.innerHTML = infs.filter(function (i) { return fl.indexOf(i.code) >= 0; }).map(function (i) {
        return '<a class="irow" href="influencer/' + i.code + '/" style="display:flex;">' +
          '<span class="go"><span class="ava" style="background:' + i.col + ';">' + i.ava + '</span>' +
          '<span class="who"><span class="hd" style="display:block;">' + i.handle + '</span>' +
          '<span class="sub">' + i.tags.join(' · ') + ' · 팔로워 ' + i.followers + '</span></span></span></a>';
      }).join('');
      document.getElementById('my-follows-empty').style.display = fl.length ? 'none' : '';
    }
  }

  // ---- 마이 ----
  function renderMypage() {
    var os = read(OKEY);
    var ow = document.getElementById('my-orders');
    if (ow) {
      ow.innerHTML = os.map(function (o) {
        return '<div class="ordercard"><span class="cover sm"><img src="' + o.img + '" alt="" /></span>' +
          '<div><div class="t">' + o.name + '</div><div class="d">' + o.store + ' · 픽업 가능 · ' + o.price + '</div></div>' +
          '<div class="code"><div class="lbl">픽업 코드</div><div class="v">' + o.pickup + '</div></div></div>';
      }).join('');
      document.getElementById('my-orders-empty').style.display = os.length ? 'none' : '';
    }
  }

  function resetDemo() {
    [FKEY, LKEY, OKEY].forEach(function (k) { localStorage.removeItem(k); });
    toast('데모 데이터를 초기화했어요'); sync();
    setTimeout(function () { location.reload(); }, 600);
  }

  // ---- 토스트 ----
  var tt = null;
  function toast(msg) {
    var el = document.getElementById('toast');
    if (!el) return;
    el.textContent = msg;
    el.classList.add('show');
    clearTimeout(tt);
    tt = setTimeout(function () { el.classList.remove('show'); }, 2200);
  }

  sync();
  return { toggle: toggle, sync: sync, search: search, toggleLib: toggleLib,
           openPay: openPay, closePay: closePay, selEasy: selEasy, agreeAll: agreeAll,
           payNow: payNow, renderLibrary: renderLibrary, renderMypage: renderMypage,
           resetDemo: resetDemo };
})();
