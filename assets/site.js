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
