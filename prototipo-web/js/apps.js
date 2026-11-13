/* Brisa — aplicações incluídas no protótipo. */
(() => {
  'use strict';
  const B = window.Brisa;
  const { el, icone } = B;

  /* ---------- Sistema de ficheiros de demonstração (vive só em memória) ---------- */
  const pasta = (filhos = {}) => ({ tipo: 'pasta', filhos });
  const txt = (texto) => ({ tipo: 'txt', texto });
  const raiz = pasta({
    Documentos: pasta({
      'Bem-vindo ao Brisa.txt': txt(
        'Este é um protótipo do ambiente de trabalho Brisa.\n\n' +
        'Experimente:\n' +
        '- arrastar as janelas pela barra de título\n' +
        '- redimensionar pelo canto inferior direito\n' +
        '- Ctrl+Espaço para procurar uma aplicação\n' +
        '- mudar o tema, a cor e o fundo nas Definições\n'),
      'Ideias.txt': txt('O que falta ao Brisa?\n\n'),
    }),
    Imagens: pasta(),
    Música: pasta(),
    Transferências: pasta(),
  });
  const resolver = (caminho) => {
    let no = raiz;
    for (const nome of caminho) {
      no = no.filhos?.[nome];
      if (!no) return null;
    }
    return no;
  };
  const textoCaminho = (c) => '~' + (c.length ? '/' + c.join('/') : '');

  const I_PASTA = '<svg class="i-pasta" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M2 7a2 2 0 0 1 2-2h5l2 2h9a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2z"/></svg>';
  const I_TXT = '<svg class="i-txt" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round" stroke-linecap="round" aria-hidden="true"><path d="M6 3h9l4 4v14H6z"/><path d="M9 11h7M9 14.5h7M9 18h4"/></svg>';

  /* ---------- Ficheiros ---------- */
  B.registar({
    id: 'ficheiros', nome: 'Ficheiros', icone: 'ficheiros', cor: '#1F6F78', mem: 38, largura: 660, altura: 430,
    criar(j, args) {
      let caminho = args?.caminho || [];
      const lado = el('nav', { class: 'fic-lado', 'aria-label': 'Locais' });
      const rotulo = el('span', { class: 'fic-caminho' });
      const lista = el('div', { class: 'fic-lista' });
      const voltar = el('button', { class: 'botao', 'aria-label': 'Pasta anterior', html: icone('voltar'), onclick: () => ir(caminho.slice(0, -1)) });
      voltar.firstChild.style.cssText = 'width:16px;height:16px;display:block';

      const abrirItem = (nome, no) => {
        if (no.tipo === 'pasta') ir([...caminho, nome]);
        else B.abrir('notas', { caminho: [...caminho, nome] });
      };
      const novaNota = () => {
        const dir = resolver(caminho);
        let nome = 'Nova nota.txt', n = 2;
        while (dir.filhos[nome]) nome = `Nova nota ${n++}.txt`;
        dir.filhos[nome] = txt('');
        ir(caminho);
        B.abrir('notas', { caminho: [...caminho, nome] });
      };

      function ir(novo) {
        caminho = novo;
        const dir = resolver(caminho);
        rotulo.textContent = caminho.length ? caminho[caminho.length - 1] : 'Início';
        voltar.disabled = !caminho.length;
        voltar.style.opacity = caminho.length ? 1 : .4;
        lado.replaceChildren(
          el('button', { text: 'Início', 'aria-current': String(!caminho.length), onclick: () => ir([]) }),
          ...Object.keys(raiz.filhos).map((n) =>
            el('button', { text: n, 'aria-current': String(caminho[0] === n), onclick: () => ir([n]) })),
        );
        const nomes = Object.keys(dir.filhos).sort((a, b) =>
          (dir.filhos[b].tipo === 'pasta') - (dir.filhos[a].tipo === 'pasta') || a.localeCompare(b, 'pt'));
        lista.replaceChildren(
          ...(nomes.length
            ? nomes.map((n) => {
                const no = dir.filhos[n];
                return el('button', { class: 'fic-item', html: no.tipo === 'pasta' ? I_PASTA : I_TXT,
                  ondblclick: () => abrirItem(n, no),
                  onkeydown: (e) => { if (e.key === 'Enter') abrirItem(n, no); } },
                  el('span', { text: n }));
              })
            : [el('p', { class: 'fic-vazio', text: 'Esta pasta está vazia. Use "Nova nota" para criar aqui um ficheiro.' })]),
        );
      }

      j.corpo.append(el('div', { class: 'fic' }, lado,
        el('div', { class: 'fic-main' },
          el('div', { class: 'fic-topo' }, voltar, rotulo, el('button', { class: 'botao principal', text: 'Nova nota', onclick: novaNota })),
          lista,
          el('div', { class: 'fic-dica nota-rodape', text: 'Duplo clique para abrir.' }))));
      j.receber = (a) => a.caminho && ir(a.caminho);
      ir(caminho);
    },
  });

  /* ---------- Notas ---------- */
  B.registar({
    id: 'notas', nome: 'Notas', icone: 'notas', cor: '#D9912B', mem: 24, largura: 520, altura: 400,
    criar(j, args) {
      const area = el('textarea', { spellcheck: 'false', 'aria-label': 'Texto da nota', placeholder: 'Escreva aqui.' });
      const estado = el('span', { class: 'nota-rodape' });
      const conta = el('span', { class: 'nota-rodape' });
      let no = null;

      const contar = () => {
        const p = area.value.trim() ? area.value.trim().split(/\s+/).length : 0;
        conta.textContent = p === 1 ? '1 palavra' : `${p} palavras`;
      };
      const carregar = (a) => {
        no = a?.caminho ? resolver(a.caminho) : null;
        if (no) {
          area.value = no.texto;
          j.titulo(a.caminho[a.caminho.length - 1]);
          estado.textContent = 'Guardado em ' + textoCaminho(a.caminho.slice(0, -1));
        } else {
          let rascunho = '';
          try { rascunho = localStorage.getItem('brisa.nota') || ''; } catch {}
          area.value = rascunho;
          j.titulo('Notas — rascunho');
          estado.textContent = 'O rascunho guarda-se sozinho';
        }
        contar();
        area.focus();
      };
      area.addEventListener('input', () => {
        if (no) no.texto = area.value;
        else { try { localStorage.setItem('brisa.nota', area.value); } catch {} }
        contar();
      });

      j.corpo.append(el('div', { class: 'notas' }, area, el('div', { class: 'notas-rodape' }, estado, conta)));
      j.receber = carregar;
      carregar(args);
    },
  });

  /* ---------- Terminal ---------- */
  B.registar({
    id: 'terminal', nome: 'Terminal', icone: 'terminal', cor: '#3A4F58', mem: 18, largura: 580, altura: 360,
    criar(j) {
      let cwd = [];
      const historico = [];
      let pos = 0;
      const saida = el('div');
      const prompt = el('span');
      const entrada = el('input', { 'aria-label': 'Comando', autocomplete: 'off', autocapitalize: 'off', spellcheck: 'false' });
      const caixa = el('div', { class: 'term' }, saida, el('div', { class: 'term-linha' }, prompt, entrada));

      const escrever = (texto, classe) => saida.append(el('pre', { class: classe || '', text: texto }));
      const atualizarPrompt = () => { prompt.textContent = `brisa:${textoCaminho(cwd)}$`; };

      const comandos = {
        ajuda: () => escrever(
          'ajuda            mostra esta lista\n' +
          'ls               lista a pasta atual\n' +
          'cd <pasta>       muda de pasta (cd .. sobe, cd volta ao início)\n' +
          'cat <ficheiro>   mostra um ficheiro de texto\n' +
          'abrir <app>      abre uma aplicação (ex.: abrir notas)\n' +
          'eco <texto>      repete o texto\n' +
          'data             data e hora\n' +
          'sistema          resumo do sistema\n' +
          'limpar           limpa o ecrã'),
        ls: () => {
          const f = resolver(cwd).filhos;
          const nomes = Object.keys(f).map((n) => (f[n].tipo === 'pasta' ? n + '/' : n));
          escrever(nomes.length ? nomes.join('\n') : '(pasta vazia)');
        },
        cd: (arg) => {
          if (!arg || arg === '~') cwd = [];
          else if (arg === '..') cwd = cwd.slice(0, -1);
          else {
            const alvo = [...cwd, arg.replace(/\/$/, '')];
            if (resolver(alvo)?.tipo === 'pasta') cwd = alvo;
            else escrever(`cd: a pasta "${arg}" não existe aqui. Use ls para ver o que há.`, 't-erro');
          }
        },
        cat: (arg) => {
          const no = arg && resolver([...cwd, arg]);
          if (no?.tipo === 'txt') escrever(no.texto || '(ficheiro vazio)');
          else escrever(`cat: "${arg || ''}" não é um ficheiro de texto desta pasta.`, 't-erro');
        },
        abrir: (arg) => {
          const id = [...B.apps.keys()].find((k) => k === (arg || '').toLowerCase());
          if (id) B.abrir(id);
          else escrever(`abrir: aplicações disponíveis: ${[...B.apps.keys()].join(', ')}`, 't-erro');
        },
        eco: (arg) => escrever(arg || ''),
        data: () => escrever(new Date().toLocaleString('pt-PT', { dateStyle: 'full', timeStyle: 'short' })),
        sistema: () => escrever(
          'Brisa 0.1 (protótipo)\n' +
          `Janelas abertas: ${B.janelas.size}\n` +
          `Memória em uso:  ${B.memoria()} MB de ${B.MEM_TOTAL} MB (simulada)\n` +
          `Tema:            ${document.documentElement.dataset.tema}`),
        limpar: () => saida.replaceChildren(),
      };

      entrada.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
          const linha = entrada.value.trim();
          escrever(`${prompt.textContent} ${linha}`, 't-cmd');
          entrada.value = '';
          if (linha) {
            historico.push(linha);
            pos = historico.length;
            const [nome, ...resto] = linha.split(/\s+/);
            const cmd = comandos[nome.toLowerCase()];
            if (cmd) cmd(resto.join(' '));
            else escrever(`Comando desconhecido: ${nome}. Escreva "ajuda" para ver os comandos.`, 't-erro');
          }
          atualizarPrompt();
          caixa.scrollTop = caixa.scrollHeight;
        } else if (e.key === 'ArrowUp' || e.key === 'ArrowDown') {
          e.preventDefault();
          pos = Math.max(0, Math.min(historico.length, pos + (e.key === 'ArrowUp' ? -1 : 1)));
          entrada.value = historico[pos] || '';
        }
      });
      caixa.addEventListener('click', () => { if (!String(getSelection())) entrada.focus(); });

      escrever('Terminal do Brisa. Escreva "ajuda" para ver os comandos.');
      atualizarPrompt();
      j.corpo.append(caixa);
      entrada.focus();
    },
  });

  /* ---------- Calculadora ---------- */
  B.registar({
    id: 'calculadora', nome: 'Calculadora', icone: 'calculadora', cor: '#B8336A', mem: 12, largura: 280, altura: 400,
    criar(j) {
      let atual = '0', acum = null, op = null, novo = true;
      const visor = el('div', { class: 'calc-visor', 'aria-live': 'polite' });
      const mostrar = () => { visor.textContent = atual.replace('.', ','); };
      const formatar = (n) => (Number.isFinite(n) ? String(parseFloat(n.toPrecision(10))) : 'Erro');
      const calcular = () => {
        const a = acum, b = parseFloat(atual);
        const r = op === '+' ? a + b : op === '−' ? a - b : op === '×' ? a * b : a / b;
        atual = formatar(r);
        acum = Number.isFinite(r) ? r : null;
      };
      const premir = (t) => {
        if (atual === 'Erro' && t !== 'C') return;
        if (/^\d$/.test(t)) {
          if (novo) { atual = t; novo = false; }
          else if (atual.replace(/\D/g, '').length < 12) atual = atual === '0' ? t : atual + t;
        } else if (t === ',') {
          if (novo) { atual = '0.'; novo = false; }
          else if (!atual.includes('.')) atual += '.';
        } else if (t === 'C') { atual = '0'; acum = null; op = null; novo = true; }
        else if (t === '±') { if (atual !== '0') atual = atual.startsWith('-') ? atual.slice(1) : '-' + atual; }
        else if (t === '%') { atual = formatar(parseFloat(atual) / 100); novo = true; }
        else if (t === '=') { if (op) { calcular(); op = null; } novo = true; }
        else { // operador
          if (op && !novo) calcular(); else acum = parseFloat(atual);
          op = t; novo = true;
        }
        mostrar();
      };
      const teclas = ['C', '±', '%', '÷', '7', '8', '9', '×', '4', '5', '6', '−', '1', '2', '3', '+', '0', ',', '='];
      const grelha = el('div', { class: 'calc-teclas' }, teclas.map((t) =>
        el('button', {
          text: t,
          class: t === '=' ? 't-ig' : '÷×−+'.includes(t) ? 't-op' : t === '0' ? 't-largo' : '',
          onclick: () => premir(t),
        })));
      const corpo = el('div', { class: 'calc', tabindex: '0', 'aria-label': 'Calculadora' }, visor, grelha);
      const MAPA = { '/': '÷', '*': '×', '-': '−', '+': '+', Enter: '=', '=': '=', '.': ',', ',': ',', Escape: 'C', '%': '%' };
      corpo.addEventListener('keydown', (e) => {
        const t = /^\d$/.test(e.key) ? e.key : MAPA[e.key];
        if (!t) return;
        e.preventDefault();
        e.stopPropagation();
        premir(t);
      });
      j.corpo.append(corpo);
      mostrar();
      corpo.focus();
    },
  });

  /* ---------- Definições ---------- */
  const G = {
    vidro: 'radial-gradient(60% 60% at 20% 25%, #8FC3FF, transparent), radial-gradient(50% 60% at 85% 20%, #CDB4FF, transparent), radial-gradient(60% 60% at 75% 85%, #FFC4A3, transparent), #EEF2FF',
    mare: 'linear-gradient(#BFE3DF 0 45%, #3F9296 45% 70%, #174F5A 70%)',
    duna: 'linear-gradient(#F3CFA8 0 45%, #D9AE74 45% 70%, #9C6B43 70%)',
    noite: 'linear-gradient(#0F1B22 0 45%, #18393F 45% 70%, #0D1F24 70%)',
  };
  const ACENTOS = [['azul', 'Azul', '#2F7BF6'], ['mar', 'Mar', '#1F6F78'], ['sol', 'Sol', '#F2B33D'], ['buganvilia', 'Buganvília', '#B8336A']];
  const FUNDOS = [['vidro', 'Vidro'], ['mare', 'Maré'], ['duna', 'Duna'], ['noite', 'Noite']];
  const grad = (v) => G[v];
  B.registar({
    id: 'definicoes', nome: 'Definições', icone: 'definicoes', cor: '#55666D', mem: 22, largura: 480, altura: 520,
    criar(j) {
      const corpo = el('div', { class: 'defs' });
      const desenhar = () => {
        const d = B.defs;
        corpo.replaceChildren(
          el('h2', { text: 'Tema' }),
          el('p', { text: 'Automático segue a preferência do computador.' }),
          el('div', { class: 'segmentos' }, [['auto', 'Automático'], ['claro', 'Claro'], ['escuro', 'Escuro']].map(([v, n]) =>
            el('button', { text: n, 'aria-pressed': String(d.tema === v), onclick: () => B.aplicarDefs({ tema: v }) }))),
          el('h2', { text: 'Animações' }),
          el('p', { text: 'Transições ao abrir, fechar e organizar janelas. Desligue em computadores mais fracos.' }),
          el('div', { class: 'segmentos' }, [[true, 'Ligadas'], [false, 'Desligadas']].map(([v, n]) =>
            el('button', { text: n, 'aria-pressed': String(d.animacoes === v), onclick: () => B.aplicarDefs({ animacoes: v }) }))),
          el('h2', { text: 'Cor de destaque' }),
          el('p', { text: 'Usada em botões, seleções e na aplicação ativa da doca.' }),
          el('div', { class: 'amostras' }, ACENTOS.map(([v, n, cor]) =>
            el('button', { class: 'amostra', 'aria-pressed': String(d.acento === v), onclick: () => B.aplicarDefs({ acento: v }) },
              el('i', { style: `background:${cor}` }), el('span', { text: n })))),
          el('h2', { text: 'Fundo' }),
          el('p', { text: 'Os fundos são desenhados pelo sistema, sem ficheiros de imagem, para poupar memória.' }),
          el('div', { class: 'amostras' }, FUNDOS.map(([v, n]) =>
            el('button', { class: 'amostra fundo-op', 'aria-pressed': String(d.fundo === v), onclick: () => B.aplicarDefs({ fundo: v }) },
              el('i', { style: `background:${grad(v)}` }), el('span', { text: n })))),
        );
      };
      const ouvir = () => desenhar();
      document.addEventListener('brisa:mudou', ouvir);
      j.aoFechar = () => document.removeEventListener('brisa:mudou', ouvir);
      j.corpo.append(corpo);
      desenhar();
    },
  });

  /* ---------- Monitor do sistema ---------- */
  B.registar({
    id: 'monitor', nome: 'Monitor', icone: 'monitor', cor: '#3B7A57', mem: 16, largura: 400, altura: 400,
    criar(j) {
      const corpo = el('div', { class: 'mon' });
      const desenhar = () => {
        const mem = B.memoria();
        const barra = el('i');
        barra.style.width = (mem / B.MEM_TOTAL) * 100 + '%';
        corpo.replaceChildren(
          el('div', { class: 'mon-grande' }, `${mem} MB `, el('small', { text: `de ${B.MEM_TOTAL / 1024} GB em uso` })),
          el('div', { class: 'medidor' }, barra),
          el('table', null,
            el('thead', null, el('tr', null, el('th', { text: 'Processo' }), el('th', { text: 'Memória' }))),
            el('tbody', null,
              el('tr', null, el('td', { text: 'Sistema e ambiente de trabalho' }), el('td', { text: `${B.MEM_BASE} MB` })),
              [...B.janelas.keys()].map((id) => {
                const a = B.apps.get(id);
                return el('tr', null, el('td', { text: a.nome }), el('td', { text: `${a.mem} MB` }));
              }))),
          el('p', { class: 'nota-rodape', text: 'Valores simulados: mostram o objetivo de consumo do Brisa, não medições reais.' }),
        );
      };
      const ouvir = () => desenhar();
      document.addEventListener('brisa:mudou', ouvir);
      j.aoFechar = () => document.removeEventListener('brisa:mudou', ouvir);
      j.corpo.append(corpo);
      desenhar();
    },
  });

  /* ---------- Sobre ---------- */
  B.registar({
    id: 'sobre', nome: 'Sobre o Brisa', icone: 'brisa', cor: '#1F6F78', mem: 8, largura: 340, altura: 300, naDoca: false,
    criar(j) {
      j.corpo.append(el('div', { class: 'sobre' },
        el('span', { class: 'mosaico', html: icone('brisa') }),
        el('h2', { text: 'Brisa' }),
        el('p', { text: 'Versão 0.1, protótipo do ambiente de trabalho.' }),
        el('p', { text: 'Um sistema leve para computadores com pouca memória.' })));
    },
  });

  B.iniciar();
  B.abrir('ficheiros');
})();
