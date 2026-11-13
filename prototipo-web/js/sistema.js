/* Brisa — núcleo do ambiente de trabalho: janelas, barra, doca, lançador e movimento. */
(() => {
  'use strict';

  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];

  const el = (tag, attrs, ...filhos) => {
    const e = document.createElement(tag);
    for (const [k, v] of Object.entries(attrs || {})) {
      if (k === 'class') e.className = v;
      else if (k === 'text') e.textContent = v;
      else if (k === 'html') e.innerHTML = v;
      else if (k.startsWith('on')) e.addEventListener(k.slice(2), v);
      else if (v !== false && v != null) e.setAttribute(k, v === true ? '' : v);
    }
    for (const f of filhos.flat()) if (f != null) e.append(f);
    return e;
  };

  const TRACOS = {
    brisa: '<path d="M3 9c3-3 6-3 9 0s6 3 9 0"/><path d="M3 15c3-3 6-3 9 0s6 3 9 0"/>',
    ficheiros: '<path d="M3 7a2 2 0 0 1 2-2h4l2 2h8a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>',
    notas: '<path d="M6 3h9l4 4v14H6z"/><path d="M9 11h7M9 15h7"/>',
    terminal: '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M7 10l3 2.5L7 15M12.5 15H17"/>',
    definicoes: '<path d="M4 7h9M19 7h1M4 17h1M11 17h9"/><circle cx="16" cy="7" r="2.5"/><circle cx="8" cy="17" r="2.5"/>',
    calculadora: '<rect x="5" y="3" width="14" height="18" rx="2"/><path d="M8.5 7.5h7"/><path d="M9 12h.01M12 12h.01M15 12h.01M9 16h.01M12 16h.01M15 16h.01" stroke-width="2.4"/>',
    monitor: '<path d="M3 12h4l2-6 4 12 2-6h6"/>',
    grelha: '<rect x="4" y="4" width="6.5" height="6.5" rx="1.5"/><rect x="13.5" y="4" width="6.5" height="6.5" rx="1.5"/><rect x="4" y="13.5" width="6.5" height="6.5" rx="1.5"/><rect x="13.5" y="13.5" width="6.5" height="6.5" rx="1.5"/>',
    fechar: '<path d="M6 6l12 12M18 6L6 18" stroke-width="3"/>',
    minimizar: '<path d="M5 12h14" stroke-width="3"/>',
    maximizar: '<rect x="5" y="5" width="14" height="14" rx="2" stroke-width="3"/>',
    voltar: '<path d="M14 6l-6 6 6 6"/>',
  };
  const icone = (nome) =>
    `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${TRACOS[nome] || ''}</svg>`;

  const B = (window.Brisa = {
    $, $$, el, icone,
    apps: new Map(),
    janelas: new Map(),
    z: 10,
    ativa: null,
    MEM_BASE: 286,
    MEM_TOTAL: 2048,
  });

  const avisar = () => document.dispatchEvent(new CustomEvent('brisa:mudou'));
  const area = () => $('#area');

  /* ---------- Definições guardadas ---------- */
  const PADRAO = { tema: 'auto', acento: 'azul', fundo: 'vidro', animacoes: true };
  const ACENTOS = ['azul', 'mar', 'sol', 'buganvilia'];
  const FUNDOS = ['vidro', 'mare', 'duna', 'noite'];
  const defs = { ...PADRAO };
  try { Object.assign(defs, JSON.parse(localStorage.getItem('brisa.defs') || '{}')); } catch {}
  const escuroSistema = window.matchMedia('(prefers-color-scheme: dark)');
  const menosMovimento = window.matchMedia('(prefers-reduced-motion: reduce)');

  B.defs = defs;
  B.aplicarDefs = (mudancas) => {
    Object.assign(defs, mudancas || {});
    // Valores guardados por versões anteriores do protótipo voltam ao padrão
    if (!ACENTOS.includes(defs.acento)) defs.acento = PADRAO.acento;
    if (!FUNDOS.includes(defs.fundo)) defs.fundo = PADRAO.fundo;
    try { localStorage.setItem('brisa.defs', JSON.stringify(defs)); } catch {}
    const tema = defs.tema === 'auto' ? (escuroSistema.matches ? 'escuro' : 'claro') : defs.tema;
    const h = document.documentElement;
    h.dataset.tema = tema;
    h.dataset.acento = defs.acento;
    h.dataset.fundo = defs.fundo;
    h.dataset.anim = defs.animacoes ? 'sim' : 'nao';
    $$('#rapido-tema button').forEach((b) => b.setAttribute('aria-pressed', String(b.dataset.tema === tema)));
    avisar();
  };
  escuroSistema.addEventListener('change', () => B.aplicarDefs());

  /* ---------- Movimento ---------- */
  const CURVA = 'cubic-bezier(.2, .8, .2, 1)';
  const comMovimento = () => defs.animacoes && !menosMovimento.matches;

  // Anima um elemento; aoFim só corre se a animação chegar ao fim (não se for cancelada)
  const animar = (alvo, quadros, ms, aoFim, manter) => {
    if (!comMovimento()) { aoFim?.(); return; }
    const an = alvo.animate(quadros, { duration: ms, easing: CURVA, fill: manter ? 'forwards' : 'none' });
    an.finished.then(() => { aoFim?.(); if (manter) an.cancel(); }, () => {});
  };

  // Transformação que leva a janela até ao seu ícone na doca
  const ateDoca = (id, janela) => {
    const alvo = $(`#doca [data-app="${id}"] .mosaico`) || $('#btn-lancador .mosaico');
    const a = alvo.getBoundingClientRect(), r = janela.getBoundingClientRect();
    const dx = a.left + a.width / 2 - (r.left + r.width / 2);
    const dy = a.top + a.height / 2 - (r.top + r.height / 2);
    return `translate(${dx}px, ${dy}px) scale(${Math.max(.06, a.width / r.width)})`;
  };
  const surgirDaDoca = (id, janela, ms) =>
    animar(janela, [{ transform: ateDoca(id, janela), opacity: 0 }, { opacity: 1, offset: .5 }, { transform: 'none', opacity: 1 }], ms);

  const saltar = (id) => {
    const b = $(`#doca [data-app="${id}"]`);
    if (!b) return;
    b.classList.remove('a-saltar');
    void b.offsetWidth;
    b.classList.add('a-saltar');
  };

  // Liga a transição de posição e tamanho durante uma mudança de geometria
  const comGeometria = (janela, mudar) => {
    if (comMovimento()) {
      janela.classList.add('a-geo');
      clearTimeout(janela._geo);
      janela._geo = setTimeout(() => janela.classList.remove('a-geo'), 300);
    }
    mudar();
  };

  /* ---------- Aplicações e janelas ---------- */
  B.registar = (app) => B.apps.set(app.id, app);

  B.memoria = () => {
    let m = B.MEM_BASE;
    for (const id of B.janelas.keys()) m += B.apps.get(id).mem || 20;
    return m;
  };

  const visiveis = () => [...B.janelas.values()].filter((j) => !j.oculta)
    .sort((a, b) => (+a.el.style.zIndex || 0) - (+b.el.style.zIndex || 0));

  B.focar = (id) => {
    B.ativa = id;
    for (const [jid, j] of B.janelas) j.el.classList.toggle('ativa', jid === id);
    const j = B.janelas.get(id);
    if (j) j.el.style.zIndex = ++B.z;
    $('#barra-app').textContent = j ? j.app.nome : 'Ambiente de trabalho';
    avisar();
  };

  const focarSeguinte = () => B.focar(visiveis().pop()?.id ?? null);

  B.fechar = (id) => {
    const j = B.janelas.get(id);
    if (!j) return;
    j.aoFechar?.();
    B.janelas.delete(id);
    j.el.style.pointerEvents = 'none';
    animar(j.el, [{ transform: 'none', opacity: 1 }, { transform: 'scale(.9)', opacity: 0 }], 180, () => j.el.remove(), true);
    focarSeguinte();
  };

  B.minimizar = (id) => {
    const j = B.janelas.get(id);
    if (!j || j.oculta) return;
    j.oculta = true;
    animar(j.el, [{ transform: 'none', opacity: 1 }, { opacity: 1, offset: .5 }, { transform: ateDoca(id, j.el), opacity: 0 }], 300,
      () => { if (j.oculta) j.el.classList.add('minimizada'); }, true);
    focarSeguinte();
  };

  B.maximizar = (id, ligar) => {
    const j = B.janelas.get(id);
    if (j) comGeometria(j.el, () => j.el.classList.toggle('maximizada', ligar));
  };

  /* ---------- Organização das janelas ---------- */
  // Espaço útil: a área de janelas menos a faixa da doca
  const util = () => {
    const a = area();
    const doca = parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--doca-alt')) || 0;
    return { w: a.clientWidth, h: a.clientHeight - doca };
  };
  const MARGEM = 8;
  const zona = (nome) => {
    const { w, h } = util(), g = MARGEM;
    if (nome === 'esq') return { x: g, y: g, w: w / 2 - g * 1.5, h: h - g * 2 };
    if (nome === 'dir') return { x: w / 2 + g / 2, y: g, w: w / 2 - g * 1.5, h: h - g * 2 };
    return { x: g, y: g, w: w - g * 2, h: h - g * 2 };
  };
  const colocar = (j, r, lembrar = true) => {
    if (lembrar && !j.antes) j.antes = { w: j.el.offsetWidth, h: j.el.offsetHeight };
    comGeometria(j.el, () => {
      j.el.classList.remove('maximizada');
      Object.assign(j.el.style, { left: r.x + 'px', top: r.y + 'px', width: r.w + 'px', height: r.h + 'px' });
    });
  };

  let fantasma = null;
  const mostrarEncaixe = (nome) => {
    if (!fantasma) area().append((fantasma = el('div', { class: 'encaixe', hidden: true })));
    fantasma.hidden = !nome;
    if (!nome) return;
    const r = zona(nome);
    Object.assign(fantasma.style, { left: r.x + 'px', top: r.y + 'px', width: r.w + 'px', height: r.h + 'px', zIndex: B.z - 1 });
  };

  B.ladoALado = () => {
    const js = visiveis().reverse();
    const n = js.length;
    if (!n) return;
    const { w, h } = util(), g = MARGEM;
    const colunas = Math.ceil(Math.sqrt(n)), linhas = Math.ceil(n / colunas);
    const alt = (h - g * (linhas + 1)) / linhas;
    js.forEach((j, i) => {
      const linha = Math.floor(i / colunas), col = i % colunas;
      const naLinha = linha === linhas - 1 ? n - colunas * (linhas - 1) : colunas; // a última linha estica
      const larg = (w - g * (naLinha + 1)) / naLinha;
      colocar(j, { x: g + col * (larg + g), y: g + linha * (alt + g), w: larg, h: alt });
    });
  };

  B.cascata = () => {
    const { w, h } = util();
    visiveis().forEach((j, i) => {
      const d = i * 34;
      colocar(j, { x: 24 + d, y: 16 + d, w: Math.min(j.app.largura || 640, w - 48 - d), h: Math.min(j.app.altura || 440, h - 32 - d) }, false);
      j.antes = null;
    });
  };

  B.mostrarAmbiente = () => visiveis().forEach((j) => B.minimizar(j.id));

  // Vista geral: todas as janelas encolhidas numa grelha, para escolher uma
  B.vista = (ligar) => {
    const A = area();
    const js = [...B.janelas.values()];
    if (ligar === undefined) ligar = !A.classList.contains('vista');
    if (ligar && !js.length) return;
    B.fecharPaineis();
    A.classList.toggle('vista', ligar);
    js.forEach((j) => { clearTimeout(j._vista); j.el.classList.add('a-vista'); });
    if (!ligar) {
      js.forEach((j) => {
        j.el.style.transform = '';
        j._vista = setTimeout(() => j.el.classList.remove('a-vista'), 340);
      });
      return;
    }
    const { w, h } = util();
    const n = js.length, lado = 40, topo = 56, g = 30;
    const colunas = Math.ceil(Math.sqrt(n)), linhas = Math.ceil(n / colunas);
    const cw = (w - lado * 2 - g * (colunas - 1)) / colunas;
    const ch = (h - topo - 24 - g * (linhas - 1)) / linhas;
    js.forEach((j, i) => {
      const e = j.el;
      const cx = lado + (i % colunas) * (cw + g) + cw / 2;
      const cy = topo + Math.floor(i / colunas) * (ch + g) + ch / 2;
      const s = Math.min(cw / e.offsetWidth, ch / e.offsetHeight, 1);
      e.style.transform = `translate(${cx - (e.offsetLeft + e.offsetWidth / 2)}px, ${cy - (e.offsetTop + e.offsetHeight / 2)}px) scale(${s})`;
    });
  };

  /* ---------- Abrir uma aplicação ---------- */
  B.abrir = (id, args) => {
    const app = B.apps.get(id);
    if (!app) return null;
    B.fecharPaineis();

    let j = B.janelas.get(id);
    if (j) {
      if (j.oculta) {
        j.oculta = false;
        j.el.getAnimations().forEach((a) => a.cancel());
        j.el.classList.remove('minimizada');
        surgirDaDoca(id, j.el, 280);
      }
      B.focar(id);
      if (args) j.receber?.(args);
      return j;
    }

    const A = area();
    const livre = util();
    const w = Math.min(app.largura || 640, livre.w - 24);
    const h = Math.min(app.altura || 440, livre.h - 20);
    const n = B.janelas.size;
    const x = Math.max(12, Math.min((livre.w - w) / 2 + (n % 5) * 30 - 45, livre.w - w - 12));
    const y = Math.max(10, Math.min((livre.h - h) / 2 + (n % 5) * 26 - 20, livre.h - h));

    const corpo = el('div', { class: 'jan-corpo' });
    const titulo = el('span', { class: 'jan-titulo', text: app.nome });
    const topo = el('div', { class: 'jan-topo' },
      el('div', { class: 'jan-controlos' },
        el('button', { class: 'c-fechar', 'aria-label': 'Fechar', html: icone('fechar'), onclick: () => B.fechar(id) }),
        el('button', { 'aria-label': 'Minimizar', html: icone('minimizar'), onclick: () => B.minimizar(id) }),
        el('button', { 'aria-label': 'Maximizar', html: icone('maximizar'), onclick: () => B.maximizar(id) }),
      ),
      titulo,
    );
    const pega = el('div', { class: 'jan-pega' });
    const janela = el('section', { class: 'janela', role: 'dialog', 'aria-label': app.nome, 'data-app': id }, topo, corpo, pega);
    Object.assign(janela.style, { left: x + 'px', top: y + 'px', width: w + 'px', height: h + 'px' });

    j = { id, app, el: janela, corpo, oculta: false, antes: null, titulo: (t) => { titulo.textContent = t; } };

    janela.addEventListener('pointerdown', () => { if (B.ativa !== id) B.focar(id); }, true);
    topo.addEventListener('dblclick', (e) => { if (!e.target.closest('button')) B.maximizar(id); });

    // Arrastar; largar junto a uma margem encaixa a janela
    arrasto(topo, (e) => {
      if (e.target.closest('button') || janela.classList.contains('maximizada')) return null;
      const ar = A.getBoundingClientRect();
      let x0 = janela.offsetLeft - e.clientX;
      const y0 = janela.offsetTop - e.clientY;
      let alvo = null, moveu = false;
      return {
        mover(m) {
          if (!moveu) {
            moveu = true;
            janela.classList.remove('a-geo');
            janela.classList.add('a-arrastar');
            if (j.antes) { // sai do encaixe: recupera o tamanho que tinha
              const fr = (e.clientX - ar.left - janela.offsetLeft) / janela.offsetWidth;
              janela.style.width = j.antes.w + 'px';
              janela.style.height = j.antes.h + 'px';
              x0 = -ar.left - j.antes.w * fr;
              j.antes = null;
            }
          }
          janela.style.left = Math.max(80 - janela.offsetWidth, Math.min(x0 + m.clientX, A.clientWidth - 80)) + 'px';
          janela.style.top = Math.max(0, Math.min(y0 + m.clientY, A.clientHeight - 40)) + 'px';
          const novo = m.clientX <= 12 ? 'esq' : m.clientX >= window.innerWidth - 12 ? 'dir' : m.clientY <= ar.top + 6 ? 'max' : null;
          if (novo !== alvo) mostrarEncaixe((alvo = novo));
        },
        fim() {
          janela.classList.remove('a-arrastar');
          mostrarEncaixe(null);
          if (alvo === 'max') B.maximizar(id, true);
          else if (alvo) colocar(j, zona(alvo));
        },
      };
    });
    // Redimensionar
    arrasto(pega, (e) => {
      const w0 = janela.offsetWidth - e.clientX, h0 = janela.offsetHeight - e.clientY;
      j.antes = null;
      return {
        mover(m) {
          janela.style.width = Math.max(260, w0 + m.clientX) + 'px';
          janela.style.height = Math.max(160, h0 + m.clientY) + 'px';
        },
      };
    });

    B.janelas.set(id, j);
    A.append(janela);
    app.criar(j, args);
    B.focar(id);
    surgirDaDoca(id, janela, 320);
    saltar(id);
    return j;
  };

  function arrasto(alvo, iniciar) {
    alvo.addEventListener('pointerdown', (e) => {
      if (e.button !== 0) return;
      const gesto = iniciar(e);
      if (!gesto) return;
      e.preventDefault();
      alvo.setPointerCapture(e.pointerId);
      const fim = () => {
        alvo.removeEventListener('pointermove', gesto.mover);
        alvo.removeEventListener('pointerup', fim);
        alvo.removeEventListener('pointercancel', fim);
        gesto.fim?.();
      };
      alvo.addEventListener('pointermove', gesto.mover);
      alvo.addEventListener('pointerup', fim);
      alvo.addEventListener('pointercancel', fim);
    });
  }

  /* ---------- Painéis (menus, painel rápido, lançador) ---------- */
  B.fecharPaineis = () => {
    $$('.painel').forEach((p) => { p.hidden = true; });
    $$('[data-abre]').forEach((b) => b.setAttribute('aria-expanded', 'false'));
  };
  B.alternarPainel = (idPainel, botao) => {
    const p = $('#' + idPainel);
    const abrir = p.hidden;
    B.fecharPaineis();
    if (!abrir) return false;
    if (botao && p.classList.contains('menu')) p.style.left = Math.max(8, botao.getBoundingClientRect().left) + 'px';
    p.hidden = false;
    botao?.setAttribute('aria-expanded', 'true');
    return true;
  };

  const abrirLancador = (botao) => {
    if (!B.alternarPainel('lancador', botao)) return;
    const busca = $('#lancador-busca');
    busca.value = '';
    filtrarLancador();
    busca.focus();
  };

  const semAcentos = (s) => s.normalize('NFD').replace(/\p{M}/gu, '').toLowerCase();
  const filtrarLancador = () => {
    const q = semAcentos($('#lancador-busca').value.trim());
    let n = 0;
    $$('#lancador-grelha button').forEach((b) => {
      const mostra = semAcentos(b.dataset.nome).includes(q);
      b.hidden = !mostra;
      if (mostra) n++;
    });
    $('#lancador-vazio').hidden = n > 0;
  };

  /* ---------- Doca ---------- */
  const desenharDoca = () => {
    $('#doca').replaceChildren(
      el('button', { class: 'doca-item', id: 'btn-lancador', 'data-abre': 'lancador', title: 'Todas as aplicações (Ctrl+Espaço)', 'aria-label': 'Todas as aplicações', 'aria-expanded': 'false', onclick: (e) => abrirLancador(e.currentTarget) },
        el('span', { class: 'mosaico neutro', html: icone('grelha') })),
      el('span', { class: 'doca-sep' }),
      ...[...B.apps.values()].filter((a) => a.naDoca !== false).map((a) =>
        el('button', { class: 'doca-item', 'data-app': a.id, title: a.nome, 'aria-label': a.nome, onclick: () => {
          const j = B.janelas.get(a.id);
          if (j && B.ativa === a.id && !j.oculta) B.minimizar(a.id);
          else B.abrir(a.id);
        } }, el('span', { class: 'mosaico', style: `--cor:${a.cor}`, html: icone(a.icone) }))),
    );
    $('#lancador-grelha').replaceChildren(
      ...[...B.apps.values()].map((a) =>
        el('button', { 'data-nome': a.nome, onclick: () => B.abrir(a.id) },
          el('span', { class: 'mosaico', style: `--cor:${a.cor}`, html: icone(a.icone) }),
          el('span', { text: a.nome }))),
    );
  };

  const atualizarEstado = () => {
    $$('#doca [data-app]').forEach((b) => {
      b.classList.toggle('aberta', B.janelas.has(b.dataset.app));
      b.classList.toggle('ativa', B.ativa === b.dataset.app);
    });
    const mem = B.memoria();
    $('#barra-mem').textContent = `${mem} MB`;
    $('#rapido-mem').textContent = `${mem} MB de ${B.MEM_TOTAL / 1024} GB`;
    $('#rapido-mem-barra').style.width = (mem / B.MEM_TOTAL) * 100 + '%';
  };

  const relogio = () => {
    const agora = new Date();
    const dia = agora.toLocaleDateString('pt-PT', { weekday: 'short', day: 'numeric', month: 'short' }).replace(/\./g, '');
    const hora = agora.toLocaleTimeString('pt-PT', { hour: '2-digit', minute: '2-digit' });
    $('#btn-relogio').textContent = `${dia}  ${hora}`;
    $('#rapido-data').textContent = agora.toLocaleDateString('pt-PT', { weekday: 'long', day: 'numeric', month: 'long' });
  };

  /* ---------- Arranque ---------- */
  const ACOES = {
    'fechar-tudo': () => [...B.janelas.keys()].forEach(B.fechar),
    'lado-a-lado': () => B.ladoALado(),
    cascata: () => B.cascata(),
    ambiente: () => B.mostrarAmbiente(),
    vista: () => B.vista(true),
  };

  B.iniciar = () => {
    $('#marca-icone').innerHTML = icone('brisa');
    desenharDoca();
    B.aplicarDefs();
    relogio();
    setInterval(relogio, 15000);
    document.addEventListener('brisa:mudou', atualizarEstado);
    atualizarEstado();

    $$('.barra [data-abre]').forEach((b) => b.addEventListener('click', () => B.alternarPainel(b.dataset.abre, b)));
    $$('.menu').forEach((m) => m.addEventListener('click', (e) => {
      const b = e.target.closest('button');
      if (!b) return;
      B.fecharPaineis();
      if (b.dataset.app) B.abrir(b.dataset.app);
      ACOES[b.dataset.acao]?.();
    }));
    $('#rapido-tema').addEventListener('click', (e) => {
      const b = e.target.closest('button');
      if (b) B.aplicarDefs({ tema: b.dataset.tema });
    });
    $('#lancador-busca').addEventListener('input', filtrarLancador);
    $('#lancador-busca').addEventListener('keydown', (e) => {
      if (e.key === 'Enter') $('#lancador-grelha button:not([hidden])')?.click();
    });

    // Na vista geral, um clique escolhe a janela (ou sai, se for no vazio)
    area().addEventListener('click', (e) => {
      if (!area().classList.contains('vista')) return;
      e.stopPropagation();
      const id = e.target.closest('.janela')?.dataset.app;
      B.vista(false);
      if (id) B.abrir(id);
    }, true);

    document.addEventListener('pointerdown', (e) => {
      if (!e.target.closest('.painel, [data-abre]')) B.fecharPaineis();
    });
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') { B.fecharPaineis(); B.vista(false); }
      if (e.ctrlKey && e.code === 'Space') { e.preventDefault(); abrirLancador($('#btn-lancador')); }
    });
  };
})();
