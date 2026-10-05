/* Oryzz · inyecta cabecera y pie en cada .page (salvo .portada / .sin-marco).
   Atributos en <body>: data-doc="Texto de la cabecera", data-pie="texto izquierdo del pie" */
(function () {
  var LOGO_CLARO = '../../../02_Logos/01_Horizontal/SVG/oryzz-logo-horizontal_color-sobre-claro.svg';
  var LOGO_OSCURO = '../../../02_Logos/01_Horizontal/SVG/oryzz-logo-horizontal_color-sobre-oscuro.svg';
  function pad(n) { return (n < 10 ? '0' : '') + n; }
  function run() {
    var pages = Array.prototype.slice.call(document.querySelectorAll('.page'));
    var total = pages.length;
    var doc = document.body.getAttribute('data-doc') || '';
    var pie = document.body.getAttribute('data-pie') || 'oryzz.com';
    pages.forEach(function (p, i) {
      if (p.classList.contains('portada') || p.classList.contains('sin-marco')) return;
      var dark = p.classList.contains('oscura');
      var h = document.createElement('div');
      h.className = 'run-head';
      h.innerHTML = '<img src="' + (dark ? LOGO_OSCURO : LOGO_CLARO) + '" alt="oryzz"><span>' + doc + '</span>';
      var f = document.createElement('div');
      f.className = 'run-foot';
      f.innerHTML = '<span>' + pie + '</span><span class="folio">' + pad(i + 1) + ' / ' + pad(total) + '</span>';
      p.insertBefore(h, p.firstChild);
      p.appendChild(f);
    });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', run); else run();
})();
