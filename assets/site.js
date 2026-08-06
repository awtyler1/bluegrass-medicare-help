/* Bluegrass Medicare Help — end-of-article knowledge check.
   An article defines window.KCHECK = [{q, options:[...], answer:<index>, why:"..."}].
   This renders it into #kcheck with instant, friendly feedback. */
(function(){
  var data = window.KCHECK, mount = document.getElementById('kcheck');
  if(!data || !mount) return;
  var total = data.length, answered = 0, score = 0;
  data.forEach(function(item, qi){
    var q = document.createElement('div'); q.className = 'kc-q';
    var h = document.createElement('p'); h.className = 'kc-qt';
    h.textContent = (qi + 1) + '. ' + item.q; q.appendChild(h);
    var opts = document.createElement('div'); opts.className = 'kc-opts';
    item.options.forEach(function(text, oi){
      var b = document.createElement('button');
      b.type = 'button'; b.className = 'kc-opt'; b.textContent = text;
      b.addEventListener('click', function(){
        if (q.classList.contains('done')) return;
        q.classList.add('done'); answered++;
        var correct = oi === item.answer;
        if (correct){ b.classList.add('right'); score++; }
        else { b.classList.add('wrong'); opts.children[item.answer].classList.add('right'); }
        Array.prototype.forEach.call(opts.children, function(c){ c.disabled = true; });
        var ex = document.createElement('p'); ex.className = 'kc-why';
        ex.innerHTML = (correct ? '<b>Correct.</b> ' : '<b>Not quite.</b> ') + item.why;
        q.appendChild(ex);
        if (answered === total) finish();
      });
      opts.appendChild(b);
    });
    q.appendChild(opts); mount.appendChild(q);
  });
  var result = document.createElement('div'); result.className = 'kc-result';
  result.style.display = 'none'; mount.appendChild(result);
  function finish(){
    var msg = score === total ? "Perfect score — you really know your stuff!"
      : score >= Math.ceil(total * 0.6) ? "Nicely done — you've got a solid handle on this."
      : "Good start — Medicare is genuinely tricky, and now you know a little more.";
    result.innerHTML = '<div class="kc-score">You scored ' + score + ' / ' + total + '</div>'
      + '<p>' + msg + '</p>'
      + '<p>Have a question about your own situation? <a href="/help/">Talk to Austin &rarr;</a>'
      + ' &nbsp;·&nbsp; <a href="/articles/">Keep learning &rarr;</a></p>';
    result.style.display = '';
    if (typeof gtag === 'function') gtag('event', 'knowledge_check_complete', { score: score, total: total });
  }
})();

/* ---- inline glossary terms --------------------------------------------------
   Tapping a marked word opens its meaning under the paragraph it sits in, so a
   reader never has to leave the sentence that confused them. The markup is a
   plain link to the glossary, so this only ever adds to what already works. */
(function () {
  var open = null;

  function close() {
    if (!open) return;
    if (open.panel.parentNode) open.panel.parentNode.removeChild(open.panel);
    open.link.setAttribute('aria-expanded', 'false');
    open = null;
  }

  function panelFor(link) {
    var d = document.createElement('div');
    d.className = 'gtip';
    d.setAttribute('role', 'note');

    var head = document.createElement('div');
    head.className = 'gth';
    var b = document.createElement('b');
    b.textContent = link.getAttribute('data-n');
    var x = document.createElement('button');
    x.type = 'button';
    x.className = 'gtx';
    x.textContent = 'Close';
    x.addEventListener('click', function () { close(); link.focus(); });
    head.appendChild(b);
    head.appendChild(x);

    var p = document.createElement('p');
    p.textContent = link.getAttribute('data-d');

    var more = document.createElement('p');
    more.className = 'gtmore';
    var a = document.createElement('a');
    a.href = link.getAttribute('href');
    a.textContent = 'See an example in the glossary →';
    more.appendChild(a);

    d.appendChild(head);
    d.appendChild(p);
    d.appendChild(more);
    return d;
  }

  document.addEventListener('click', function (e) {
    var link = e.target.closest ? e.target.closest('.gt') : null;
    if (!link) {
      if (open && !(e.target.closest && e.target.closest('.gtip'))) close();
      return;
    }
    e.preventDefault();
    var wasOpen = open && open.link === link;
    close();
    if (wasOpen) return;
    var host = link.closest('p, li, td, blockquote') || link.parentNode;
    var panel = panelFor(link);
    host.parentNode.insertBefore(panel, host.nextSibling);
    link.setAttribute('aria-expanded', 'true');
    open = { link: link, panel: panel };
    if (typeof gtag === 'function') {
      gtag('event', 'glossary_term_opened', { term: link.getAttribute('data-n') });
    }
  });

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && open) { var l = open.link; close(); l.focus(); }
  });
})();
