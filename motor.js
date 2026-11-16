/* Motor del sitio de Fernanda Ramos. Sin dependencias.
   Un solo requestAnimationFrame: el scroll sólo levanta una bandera y el trabajo ocurre una vez por
   fotograma. Si algo falla al arrancar se quita .js y el sitio queda entero y quieto: nunca a medias.
   Con «reducir movimiento» todo se mueve, pero sin paralaje ni imán (ver el final de estilo.css). */
(function () {
  'use strict';
  var raiz = document.documentElement;
  var suave = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };
  var limita = function (v, a, b) { return v < a ? a : v > b ? b : v; };
  var T0 = raiz.classList.contains('sin-telon') ? 0 : 1500;

  try { arrancar(); } catch (e) { raiz.classList.remove('js'); if (window.console) console.error(e); }

  function arrancar() {
    /* ───────── revelados ─────────
       Sin IntersectionObserver: un elemento tapado por su propio clip-path, o desplazado fuera de una
       máscara con overflow oculto, tiene intersección cero y el observador nunca avisa. Se mide la caja
       (que el recorte no cambia) desde el mismo bucle del scroll. */
    var porRevelar = $$('.rv, .rv-ln, .dibuja').map(function (el) {
      return { el: el, sensor: el.classList.contains('rv-ln') ? el.parentNode : el };
    });
    function revelar(vh) {
      if (!porRevelar.length) return;
      var lote = 0, quedan = [];
      for (var i = 0; i < porRevelar.length; i++) {
        var it = porRevelar[i], r = it.sensor.getBoundingClientRect();
        if (r.top < vh * 0.88 && r.bottom > -40) {
          it.el.style.setProperty('--r', (Math.min(lote++, 10) * 0.06) + 's');
          it.el.classList.add('visto');
        } else quedan.push(it);
      }
      porRevelar = quedan;
    }

    /* ───────── el fondo: una escena por sección ─────────
       Un lienzo fijo detrás de toda la página. Cada sección tiene su escena y, al bajar, la que entra se
       funde con la que sale: anillos moleculares en la portada (se encienden cerca del cursor), hojas que
       caen en el perfil, el trazo de un cromatograma en la trayectoria, burbujas en las certificaciones,
       moléculas que giran en la formación y polen dorado en el contacto. La tabla de ámbitos, en marfil,
       lleva su propio lienzo con una retícula de celdas que se encienden.
       ~30 fps, se pausa con la pestaña oculta; con «reducir movimiento» todo va a un tercio y sin paralaje. */
    var VEL = suave ? 0.35 : 1;
    var fondo = $('#fondo'), fx = fondo ? fondo.getContext('2d') : null;
    var FD = { w: 0, h: 0, dpr: 1, px: 0.66, py: 0.42, tx: 0.66, ty: 0.42, cursor: false };
    var sem = 11; function azar() { sem = (sem * 9301 + 49297) % 233280; return sem / 233280; }
    function capa(w, h) { var c = document.createElement('canvas'); c.width = w; c.height = h; return c; }
    var LAT = null, HOJAS = [], TRAZOS = [], BURB = [], MOLS = [], POLEN = [];
    var IDS = ['inicio', 'perfil', 'ambitos', 'trayectoria', 'certificaciones', 'formacion', 'contacto'];
    var SECC = IDS.map(function (id) { return document.getElementById(id); }), PESO = IDS.map(function (_, i) { return i ? 0 : 1; });

    function armarRed() {
      var w = FD.w, h = FD.h, dpr = FD.dpr, s = 34 * dpr, dx = s * Math.sqrt(3), dy = s * 1.5;
      LAT = { tenue: capa(w + 40 * dpr, h + 40 * dpr), viva: capa(w + 40 * dpr, h + 40 * dpr), puntos: [], R: 300 * dpr };
      LAT.luz = capa(LAT.R * 2, LAT.R * 2);
      var a = LAT.tenue.getContext('2d'), b = LAT.viva.getContext('2d');
      [a, b].forEach(function (g, k) { g.strokeStyle = k ? 'rgba(159,203,178,.6)' : 'rgba(159,203,178,.085)'; g.lineWidth = dpr; g.beginPath(); });
      sem = 7;
      for (var fila = -1; fila * dy < h + 40 * dpr + s; fila++) for (var col = -1; col * dx < w + 40 * dpr + dx; col++) {
        var cx = col * dx + (fila % 2 ? dx / 2 : 0), cy = fila * dy;
        for (var k = 0; k < 6; k++) {
          var a1 = Math.PI / 3 * k + Math.PI / 6, a2 = a1 + Math.PI / 3;
          [a, b].forEach(function (g) { g.moveTo(cx + s * Math.cos(a1), cy + s * Math.sin(a1)); g.lineTo(cx + s * Math.cos(a2), cy + s * Math.sin(a2)); });
        }
        var z = azar();
        if (z < 0.07) {   // un doble enlace de vez en cuando: el guiño químico
          var b1 = Math.PI / 3 * Math.floor(azar() * 6) + Math.PI / 6, f = 0.78;
          [a, b].forEach(function (g) { g.moveTo(cx + s * f * Math.cos(b1), cy + s * f * Math.sin(b1)); g.lineTo(cx + s * f * Math.cos(b1 + Math.PI / 3), cy + s * f * Math.sin(b1 + Math.PI / 3)); });
        }
        if (z > 0.9) LAT.puntos.push({ x: cx + s * Math.cos(Math.PI / 6), y: cy + s * Math.sin(Math.PI / 6), f: azar() * 6.28, v: 0.6 + azar() * 0.8 });
      }
      a.stroke(); b.stroke();
    }
    function armarParticulas() {
      var w = FD.w, h = FD.h, d = FD.dpr; sem = 23;
      HOJAS = []; for (var i = 0; i < 24; i++) HOJAS.push({ x: azar() * w, y: azar() * h, L: (14 + azar() * 22) * d, r: azar() * 6.28, vr: (azar() - 0.5) * 0.6, vy: (10 + azar() * 16) * d, f: azar() * 6.28 });
      TRAZOS = [0.3, 0.52, 0.72, 0.88].map(function (y, k) {
        var picos = []; for (var j = 0; j < 7; j++) picos.push({ x: azar() * 1.7 * w, a: (0.03 + azar() * (k === 1 ? 0.16 : 0.09)) * h, s: (6 + azar() * 22) * d });
        return { y: y * h, picos: picos, P: 1.7 * w, v: (14 + k * 6) * d, col: k === 1 ? '201,168,106' : '159,203,178', al: k === 1 ? 0.32 : 0.18 };
      });
      BURB = []; for (var m = 0; m < 40; m++) BURB.push({ x: azar() * w, y: azar() * h, r: (2 + Math.pow(azar(), 2) * 16) * d, vy: (12 + azar() * 22) * d, f: azar() * 6.28 });
      var anillo = []; for (var q = 0; q < 6; q++) anillo.push([Math.cos(q * Math.PI / 3), Math.sin(q * Math.PI / 3), 0]);
      var plantillas = [
        { at: anillo.concat(anillo.map(function (p) { return [p[0] * 1.75, p[1] * 1.75, 0]; })), en: [[0,1],[1,2],[2,3],[3,4],[4,5],[5,0],[0,6],[1,7],[2,8],[3,9],[4,10],[5,11]], hetero: [6, 9] },
        { at: [[0,0,0],[0,1.1,0],[1.04,-.37,0],[-.52,-.37,.9],[-.52,-.37,-.9]], en: [[0,1],[0,2],[0,3],[0,4]], hetero: [1] },
        { at: [[-2,0,0],[-1,.6,0],[0,0,0],[1,.6,0],[2,0,0],[1,1.6,.3],[-1,1.6,-.3]], en: [[0,1],[1,2],[2,3],[3,4],[3,5],[1,6]], hetero: [5, 0] }
      ];
      MOLS = []; for (var n = 0; n < 6; n++) MOLS.push({ m: plantillas[n % 3], x: (0.1 + azar() * 0.8) * w, y: (0.12 + azar() * 0.76) * h, e: (26 + azar() * 34) * d, ax: azar() * 6.28, ay: azar() * 6.28, vx: (azar() - 0.5) * 0.5, vy: 0.2 + azar() * 0.4, dy: (azar() - 0.5) * 6 * d });
      POLEN = []; for (var o = 0; o < 70; o++) POLEN.push({ x: azar() * w, y: azar() * h, r: (0.8 + azar() * 2.4) * d, vy: (6 + azar() * 14) * d, f: azar() * 6.28 });
    }
    function medirFondo() {
      var dpr = Math.min(window.devicePixelRatio || 1, 1.25), w = Math.round(window.innerWidth * dpr), h = Math.round(window.innerHeight * dpr);
      if (w === FD.w && h === FD.h) return;
      FD.w = w; FD.h = h; FD.dpr = dpr; fondo.width = w; fondo.height = h; armarRed(); armarParticulas();
    }

    var ESCENAS = [
      function red(g, a, t) {
        var d = FD.dpr, ox = (suave ? 0 : (FD.px - 0.5) * -16 * d) - 20 * d, oy = (suave ? 0 : (FD.py - 0.5) * -12 * d) - 20 * d;
        g.globalAlpha = a; g.drawImage(LAT.tenue, ox, oy);
        var R = LAT.R, lx = FD.px * FD.w, ly = FD.py * FD.h, l = LAT.luz.getContext('2d');
        l.globalCompositeOperation = 'source-over'; l.clearRect(0, 0, R * 2, R * 2); l.drawImage(LAT.viva, ox - (lx - R), oy - (ly - R));
        l.globalCompositeOperation = 'destination-in'; var gr = l.createRadialGradient(R, R, 0, R, R, R); gr.addColorStop(0, 'rgba(0,0,0,.9)'); gr.addColorStop(1, 'rgba(0,0,0,0)'); l.fillStyle = gr; l.fillRect(0, 0, R * 2, R * 2);
        g.drawImage(LAT.luz, lx - R, ly - R);
        for (var i = 0; i < LAT.puntos.length; i++) {
          var p = LAT.puntos[i], v = 0.5 + 0.5 * Math.sin(t * 0.0012 * p.v * VEL + p.f);
          g.fillStyle = 'rgba(201,168,106,' + (0.12 + v * 0.5).toFixed(3) + ')'; g.beginPath(); g.arc(p.x + ox, p.y + oy, (1.4 + v * 1.8) * d, 0, 6.2832); g.fill();
        }
      },
      function hojas(g, a, t, dt) {
        g.globalAlpha = a; g.lineWidth = 1.1 * FD.dpr; g.strokeStyle = 'rgba(159,203,178,.34)';
        for (var i = 0; i < HOJAS.length; i++) {
          var o = HOJAS[i]; o.y += o.vy * dt * VEL; o.r += o.vr * dt * VEL; o.x += Math.sin(t * 0.0005 * VEL + o.f) * 0.5 * FD.dpr;
          if (o.y > FD.h + 40) { o.y = -40; o.x = azar() * FD.w; }
          var c = Math.cos(o.r), s = Math.sin(o.r), L = o.L;
          g.setTransform(c, s, -s, c, o.x, o.y); g.beginPath();
          g.moveTo(0, 0); g.quadraticCurveTo(L * 0.5, -L * 0.34, L, 0); g.quadraticCurveTo(L * 0.5, L * 0.34, 0, 0); g.moveTo(0, 0); g.lineTo(L * 0.86, 0); g.stroke();
        }
        g.setTransform(1, 0, 0, 1, 0, 0);
      },
      null,
      function cromatograma(g, a, t) {
        g.globalAlpha = a; g.lineWidth = 1.3 * FD.dpr; var paso = 5 * FD.dpr;
        for (var k = 0; k < TRAZOS.length; k++) {
          var tr = TRAZOS[k], off = (t * 0.001 * tr.v * VEL) % tr.P;
          g.strokeStyle = 'rgba(' + tr.col + ',' + tr.al + ')'; g.beginPath();
          for (var x = 0; x <= FD.w + paso; x += paso) {
            var y = tr.y;
            for (var j = 0; j < tr.picos.length; j++) { var p = tr.picos[j], dd = ((x + off - p.x) % tr.P + tr.P) % tr.P; if (dd > tr.P / 2) dd -= tr.P; if (dd > -p.s * 4 && dd < p.s * 4) y -= p.a * Math.exp(-(dd * dd) / (2 * p.s * p.s)); }
            if (x) g.lineTo(x, y); else g.moveTo(x, y);
          }
          g.stroke();
        }
      },
      function burbujas(g, a, t, dt) {
        g.globalAlpha = a; g.lineWidth = FD.dpr;
        for (var i = 0; i < BURB.length; i++) {
          var b = BURB[i]; b.y -= b.vy * dt * VEL; var x = b.x + Math.sin(t * 0.0011 * VEL + b.f) * 8 * FD.dpr;
          if (b.y < -30) { b.y = FD.h + 30; b.x = azar() * FD.w; }
          g.beginPath(); g.arc(x, b.y, b.r, 0, 6.2832);
          if (b.r < 4 * FD.dpr) { g.fillStyle = 'rgba(201,168,106,.42)'; g.fill(); } else { g.strokeStyle = 'rgba(159,203,178,.4)'; g.stroke(); g.beginPath(); g.arc(x - b.r * 0.35, b.y - b.r * 0.35, b.r * 0.18, 0, 6.2832); g.fillStyle = 'rgba(238,241,230,.16)'; g.fill(); }
        }
      },
      function moleculas(g, a, t, dt) {
        g.globalAlpha = a;
        for (var i = 0; i < MOLS.length; i++) {
          var M = MOLS[i]; M.ax += M.vx * dt * VEL; M.ay += M.vy * dt * VEL;
          var ca = Math.cos(M.ay), sa = Math.sin(M.ay), cb = Math.cos(M.ax), sb = Math.sin(M.ax), cy = M.y + Math.sin(t * 0.0004 * VEL + i) * M.dy * 3;
          var pr = M.m.at.map(function (p) { var x = p[0] * ca + p[2] * sa, z = -p[0] * sa + p[2] * ca, y = p[1] * cb - z * sb; z = p[1] * sb + z * cb; var f = 1 / (1 + z * 0.22); return [M.x + x * M.e * f, cy + y * M.e * f, f]; });
          g.lineWidth = 1.2 * FD.dpr; g.strokeStyle = 'rgba(159,203,178,.28)'; g.beginPath();
          M.m.en.forEach(function (e) { g.moveTo(pr[e[0]][0], pr[e[0]][1]); g.lineTo(pr[e[1]][0], pr[e[1]][1]); }); g.stroke();
          pr.forEach(function (p, k) { g.beginPath(); g.arc(p[0], p[1], (M.m.hetero.indexOf(k) >= 0 ? 4.6 : 3.2) * p[2] * FD.dpr, 0, 6.2832); g.fillStyle = M.m.hetero.indexOf(k) >= 0 ? 'rgba(201,168,106,.6)' : 'rgba(159,203,178,.5)'; g.fill(); });
        }
      },
      function polen(g, a, t, dt) {
        g.globalAlpha = a;
        for (var i = 0; i < POLEN.length; i++) {
          var p = POLEN[i]; p.y -= p.vy * dt * VEL; var x = p.x + Math.sin(t * 0.0007 * VEL + p.f) * 14 * FD.dpr, v = 0.5 + 0.5 * Math.sin(t * 0.002 * VEL + p.f * 3);
          if (p.y < -10) { p.y = FD.h + 10; p.x = azar() * FD.w; }
          g.fillStyle = 'rgba(226,200,147,' + (0.22 + v * 0.6).toFixed(3) + ')'; g.beginPath(); g.arc(x, p.y, p.r, 0, 6.2832); g.fill();
          if (p.r > 2.4 * FD.dpr) { g.fillStyle = 'rgba(226,200,147,' + (0.04 + v * 0.08).toFixed(3) + ')'; g.beginPath(); g.arc(x, p.y, p.r * 4, 0, 6.2832); g.fill(); }
        }
      }
    ];
    function pintarFondo(t, dt, vh) {
      for (var i = 0; i < SECC.length; i++) {
        var r = SECC[i] ? SECC[i].getBoundingClientRect() : null, meta = r ? limita((Math.min(r.bottom, vh) - Math.max(r.top, 0)) / vh, 0, 1) : 0;
        PESO[i] += (meta - PESO[i]) * 0.14;
      }
      var g = fx; g.setTransform(1, 0, 0, 1, 0, 0); g.globalAlpha = 1; g.clearRect(0, 0, FD.w, FD.h);
      for (var k = 0; k < ESCENAS.length; k++) if (ESCENAS[k] && PESO[k] > 0.015) ESCENAS[k](g, Math.min(1, PESO[k] * 1.15), t, dt);
      g.globalAlpha = 1;
      pintarReticula(t);
    }

    /* la tabla de ámbitos, en marfil: retícula de celdas que se encienden, en su propio lienzo */
    var lienzoA = $('#fondoAmbitos'), gA = lienzoA ? lienzoA.getContext('2d') : null, RA = { w: 0, h: 0, celdas: [] };
    function pintarReticula(t) {
      if (!gA) return;
      var r = lienzoA.parentNode.getBoundingClientRect();
      if (r.bottom < 0 || r.top > window.innerHeight) return;
      var d = Math.min(window.devicePixelRatio || 1, 1.25), w = Math.round(r.width * d), h = Math.round(r.height * d), c = 72 * d;
      if (w !== RA.w || h !== RA.h) {
        RA.w = w; RA.h = h; lienzoA.width = w; lienzoA.height = h; sem = 31; RA.celdas = [];
        for (var n = 0; n < 26; n++) RA.celdas.push({ x: Math.floor(azar() * w / c), y: Math.floor(azar() * h / c), f: azar() * 6.28, v: 0.4 + azar() * 0.8 });
      }
      gA.clearRect(0, 0, w, h);
      for (var i = 0; i < RA.celdas.length; i++) { var q = RA.celdas[i], v = Math.max(0, Math.sin(t * 0.0009 * q.v * VEL + q.f)); if (v > 0.02) { gA.fillStyle = 'rgba(201,168,106,' + (v * 0.16).toFixed(3) + ')'; gA.fillRect(q.x * c + 1, q.y * c + 1, c - 2, c - 2); } }
      gA.strokeStyle = 'rgba(13,42,33,.07)'; gA.lineWidth = d; gA.beginPath();
      for (var x = 0; x <= w; x += c) { gA.moveTo(x + 0.5, 0); gA.lineTo(x + 0.5, h); }
      for (var y = 0; y <= h; y += c) { gA.moveTo(0, y + 0.5); gA.lineTo(w, y + 0.5); }
      gA.stroke();
      var barre = ((t * 0.00006 * VEL) % 1.4 - 0.2) * w;   // una línea que barre, como un lector
      var gr = gA.createLinearGradient(barre - 120 * d, 0, barre + 120 * d, 0); gr.addColorStop(0, 'rgba(201,168,106,0)'); gr.addColorStop(0.5, 'rgba(201,168,106,.12)'); gr.addColorStop(1, 'rgba(201,168,106,0)');
      gA.fillStyle = gr; gA.fillRect(barre - 120 * d, 0, 240 * d, h);
    }

    /* ───────── la enredadera del margen: crece con la lectura ───────── */
    var enr = $('#enredadera'), tallo = null, largo = 0, hojasEnr = [], altoDoc = 0;
    function armarEnredadera() {
      if (!enr || getComputedStyle(enr).display === 'none') return;
      altoDoc = document.documentElement.scrollHeight;
      enr.setAttribute('height', altoDoc); enr.style.height = altoDoc + 'px';
      enr.setAttribute('viewBox', '0 0 70 ' + altoDoc);
      var pts = [], paso = 210, x0 = 30;
      for (var y = 120; y < altoDoc - 60; y += paso) pts.push([x0 + Math.sin(y * 0.0062) * 13, y]);
      if (pts.length < 2) return;
      var d = 'M' + pts[0][0].toFixed(1) + ' ' + pts[0][1];
      for (var i = 0; i < pts.length - 1; i++) {   // Catmull-Rom a Bézier: curva suave por todos los puntos
        var p0 = pts[i - 1] || pts[i], p1 = pts[i], p2 = pts[i + 1], p3 = pts[i + 2] || p2;
        d += ' C' + (p1[0] + (p2[0] - p0[0]) / 6).toFixed(1) + ' ' + (p1[1] + (p2[1] - p0[1]) / 6).toFixed(1) + ' ' + (p2[0] - (p3[0] - p1[0]) / 6).toFixed(1) + ' ' + (p2[1] - (p3[1] - p1[1]) / 6).toFixed(1) + ' ' + p2[0].toFixed(1) + ' ' + p2[1];
      }
      var h = '<path class="enr-tallo" d="' + d + '" stroke-width="1.3"/>';
      for (var j = 0; j < pts.length; j++) {
        for (var k = 0; k < 2; k++) {
          var lado = (j + k) % 2 ? 1 : -1, yy = pts[j][1] + k * paso * 0.5, xx = x0 + Math.sin(yy * 0.0062) * 13;
          var ang = lado > 0 ? -28 - (j % 3) * 8 : 208 + (j % 3) * 8, L = 15 + ((j * 7 + k * 3) % 9);
          h += '<g transform="translate(' + xx.toFixed(1) + ' ' + yy.toFixed(1) + ') rotate(' + ang + ')"><path class="enr-hoja" data-y="' + yy.toFixed(0) + '" d="M0 0 Q ' + (L * 0.5) + ' ' + (-L * 0.32) + ' ' + L + ' 0 Q ' + (L * 0.5) + ' ' + (L * 0.32) + ' 0 0" stroke-width="1"/></g>';
        }
      }
      enr.innerHTML = h;
      tallo = $('.enr-tallo', enr); largo = tallo.getTotalLength();
      tallo.style.strokeDasharray = largo; tallo.style.strokeDashoffset = largo;
      hojasEnr = $$('.enr-hoja', enr).map(function (el) { return { el: el, y: +el.getAttribute('data-y') }; });
    }
    function crecer(sy, vh) {
      if (!tallo) return;
      var hasta = sy + vh * 0.82, p = limita(hasta / altoDoc, 0, 1);
      tallo.style.strokeDashoffset = (largo * (1 - p)).toFixed(1);
      for (var i = 0; i < hojasEnr.length; i++) hojasEnr[i].el.classList.toggle('brota', hojasEnr[i].y < hasta - 30);
    }

    /* ───────── trayectoria: el año grande y el hilo ───────── */
    var puestos = $$('.puesto'), anio = $('#anio'), hilo = $('#hilo'), lista = $('.puestos'), anioActual = anio ? anio.textContent : '';
    function seguirAnio(vh) {
      if (!anio || !puestos.length) return;
      var actual = puestos[0];
      for (var i = 0; i < puestos.length; i++) if (puestos[i].getBoundingClientRect().top < vh * 0.55) actual = puestos[i];
      var a = actual.getAttribute('data-anio');
      if (a !== anioActual) {
        anioActual = a; anio.textContent = a;
        anio.classList.remove('cambia'); void anio.offsetWidth; anio.classList.add('cambia');
      }
      var r = lista.getBoundingClientRect();
      if (hilo) hilo.style.setProperty('--p', limita((vh * 0.55 - r.top) / r.height, 0, 1).toFixed(3));
    }

    /* ───────── barra e índice ───────── */
    var barra = $('#barra'), enlaces = $$('.indice a'), secciones = enlaces.map(function (a) { return $(a.getAttribute('href')); });

    /* ───────── bucle ───────── */
    var sucio = true, ultimo = 0;
    window.addEventListener('scroll', function () { sucio = true; }, { passive: true });
    function cuadro(t) {
      requestAnimationFrame(cuadro);
      var sy = window.pageYOffset, vh = window.innerHeight;
      if (sucio) {
        sucio = false;
        barra.classList.toggle('barra--llena', sy > 10);
        revelar(vh); crecer(sy, vh); seguirAnio(vh);
        var act = -1;
        for (var s = 0; s < secciones.length; s++) if (secciones[s] && secciones[s].getBoundingClientRect().top < vh * 0.45) act = s;
        enlaces.forEach(function (el, j) { el.classList.toggle('activo', j === act); });
      }
      // el fondo: ~30 fps; sin cursor (teléfono) la luz camina sola
      if (fx && !document.hidden && t - ultimo > 32) {
        var dt = Math.min(0.064, (t - ultimo) / 1000); ultimo = t;
        if (!FD.cursor) { FD.tx = 0.66 + Math.sin(t * 0.00023) * 0.2; FD.ty = 0.42 + Math.cos(t * 0.00031) * 0.22; }
        FD.px += (FD.tx - FD.px) * 0.07; FD.py += (FD.ty - FD.py) * 0.07;
        pintarFondo(t, dt, vh);
      }
    }

    /* ───────── puntero: luz, red e imán ───────── */
    var luz = $('#luz'), fino = window.matchMedia('(hover: hover) and (pointer: fine)').matches;
    if (fino) {
      window.addEventListener('pointermove', function (e) {
        if (luz) { luz.style.setProperty('--lx', e.clientX + 'px'); luz.style.setProperty('--ly', e.clientY + 'px'); luz.classList.add('luz--on'); }
        FD.cursor = true; FD.tx = e.clientX / window.innerWidth; FD.ty = e.clientY / window.innerHeight;
      }, { passive: true });
      if (!suave) $$('.boton, .ficha-dl').forEach(function (b) {
        b.addEventListener('pointermove', function (e) { var r = b.getBoundingClientRect(); b.style.translate = ((e.clientX - r.left - r.width / 2) * 0.14).toFixed(1) + 'px ' + ((e.clientY - r.top - r.height / 2) * 0.24).toFixed(1) + 'px'; });
        b.addEventListener('pointerleave', function () { b.style.translate = ''; });
      });
    }

    /* ───────── cifras que cuentan, cuando sube el telón ───────── */
    setTimeout(function () {
      $$('[data-cuenta]').forEach(function (b) {
        var n = +b.getAttribute('data-cuenta'), t0 = performance.now(), dura = 900 + n * 60;
        (function paso(t) { var k = limita((t - t0) / dura, 0, 1); b.textContent = Math.round(n * (1 - Math.pow(1 - k, 3))); if (k < 1) requestAnimationFrame(paso); })(t0);
      });
    }, T0 + 1100);

    /* ───────── idioma: un barrido verde cruza y el texto cambia cuando lo tapa ───────── */
    var traducibles = $$('[data-en]'), conAttr = $$('*').filter(function (el) {
      for (var i = 0; i < el.attributes.length; i++) if (el.attributes[i].name.indexOf('data-en-') === 0) return true; return false;
    });
    var titulos = { es: document.title, en: 'Fernanda Ramos · Regulatory Affairs' };
    function poner(l) {
      traducibles.forEach(function (el) {
        if (el.dataset.es === undefined) el.dataset.es = el.innerHTML;
        el.innerHTML = l === 'en' ? el.dataset.en : el.dataset.es;
      });
      conAttr.forEach(function (el) {
        Array.prototype.slice.call(el.attributes).forEach(function (at) {
          if (at.name.indexOf('data-en-') !== 0) return;
          var destino = at.name.slice(8), guarda = 'data-es-' + destino;
          if (!el.hasAttribute(guarda)) el.setAttribute(guarda, el.getAttribute(destino) || '');
          el.setAttribute(destino, l === 'en' ? at.value : el.getAttribute(guarda));
        });
      });
      raiz.lang = l; document.title = titulos[l];
      try { localStorage.setItem('fr-idioma', l); } catch (e) {}
      sucio = true; setTimeout(armarEnredadera, 50);
    }
    var barrido = null;
    function cambiar() {
      var l = raiz.lang === 'en' ? 'es' : 'en';
      if (!document.body.animate) { poner(l); return; }
      if (!barrido) { barrido = document.createElement('div'); barrido.setAttribute('aria-hidden', 'true'); barrido.style.cssText = 'position:fixed;inset:0;z-index:70;background:#11322A;transform:translateX(-101%);pointer-events:none;border-right:2px solid #C9A86A'; document.body.appendChild(barrido); }
      var an = barrido.animate([{ transform: 'translateX(-101%)' }, { transform: 'translateX(0)', offset: 0.5 }, { transform: 'translateX(101%)' }], { duration: suave ? 600 : 900, easing: 'cubic-bezier(.7,0,.3,1)' });
      setTimeout(function () { poner(l); }, suave ? 300 : 450);
      an.onfinish = function () { barrido.style.transform = 'translateX(-101%)'; };
    }
    var boton = $('.idioma'); if (boton) boton.addEventListener('click', cambiar);
    var guardado = null; try { guardado = localStorage.getItem('fr-idioma'); } catch (e) {}
    if (guardado === 'en') poner('en');

    /* ───────── copiar el correo ───────── */
    $$('.copiar').forEach(function (b) {
      b.addEventListener('click', function () {
        var txt = b.getAttribute('data-copiar'), et = $('span', b), antes = et.innerHTML;
        function listo() { b.classList.add('hecho'); et.textContent = b.getAttribute('data-ok'); setTimeout(function () { b.classList.remove('hecho'); et.innerHTML = antes; }, 1700); }
        if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(txt).then(listo, listo);
        else { var t = document.createElement('textarea'); t.value = txt; document.body.appendChild(t); t.select(); try { document.execCommand('copy'); } catch (e) {} t.remove(); listo(); }
      });
    });

    /* ───────── arranque ───────── */
    if (fondo) medirFondo(); armarEnredadera();
    window.addEventListener('resize', function () { if (fondo) medirFondo(); clearTimeout(window.__fr); window.__fr = setTimeout(armarEnredadera, 200); sucio = true; });
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(function () { armarEnredadera(); sucio = true; });
    window.addEventListener('load', function () { armarEnredadera(); sucio = true; });
    requestAnimationFrame(cuadro);
  }
})();
