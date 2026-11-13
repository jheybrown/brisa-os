"""Gera a maqueta do ecrã do Brisa com o layout Ilhas, a doca Vidro e um fundo à escolha.

Uso: python gerar-maqueta.py <fundo.png relativo à página> <ficheiro html de saída>
A página tem duas variantes, escolhidas com ?tema=claro ou ?tema=escuro.
"""
import base64
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from brisa_icones import icone  # noqa: E402

fundo, saida = sys.argv[1], pathlib.Path(sys.argv[2])
uri = lambda s: 'data:image/svg+xml;base64,' + base64.b64encode(s.encode()).decode()  # noqa: E731
ic = {n: uri(icone(n, 'vidro')) for n in ['ficheiros', 'navegador', 'writer', 'calc', 'notas', 'calculadora', 'loja', 'definicoes', 'lancador']}
NOMES = {'ficheiros': 'Ficheiros', 'navegador': 'Navegador', 'writer': 'Writer', 'calc': 'Calc', 'notas': 'Notas',
         'calculadora': 'Calculadora', 'loja': 'Loja', 'definicoes': 'Definições', 'lancador': 'Aplicações'}
doca = ''.join(f'<span class="item{" aberta" if n in ("ficheiros", "navegador") else ""}" title="{NOMES[n]}"><img src="{u}" alt=""></span>'
               for n, u in ic.items())

pasta = '<svg viewBox="0 0 48 40"><path d="M2 8a5 5 0 0 1 5-5h10l4 4h20a5 5 0 0 1 5 5v2H2z" fill="#5FA2F8"/><path d="M2 12h44v21a5 5 0 0 1-5 5H7a5 5 0 0 1-5-5z" fill="#3D8BF0"/></svg>'
pastas = ''.join(f'<div class="ficheiro">{pasta}<span>{n}</span></div>' for n in ['Escola', 'Trabalho', 'Faturas', 'Viagens', 'Fotografias', 'Receitas'])
glifo = lambda d: f'<svg class="glifo" viewBox="0 0 24 24">{d}</svg>'  # noqa: E731
WIFI = glifo('<path d="M2 9a15 15 0 0 1 20 0M5 12.5a10 10 0 0 1 14 0M8.5 16a5 5 0 0 1 7 0"/><circle cx="12" cy="19.5" r=".7"/>')
SOM = glifo('<path d="M4 9h4l5-4v14l-5-4H4z"/><path d="M16 9a4 4 0 0 1 0 6M18.5 6.5a8 8 0 0 1 0 11"/>')
BAT = glifo('<rect x="2.5" y="7" width="17" height="10" rx="2.5"/><path d="M22 10.5v3"/><rect x="5" y="9.5" width="11" height="5" rx="1" fill="currentColor" stroke="none"/>')

html = f'''<!doctype html>
<html lang="pt">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Brisa com o fundo Aurora</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
  * {{ box-sizing: border-box; }}
  html, body {{ margin: 0; height: 100%; background: #05070F; }}
  .ecra {{
    --vidro: rgba(255, 255, 255, .78); --vidro-borda: rgba(255, 255, 255, .92); --texto: #1D1D1F; --texto-2: #4A5470;
    --janela: #FFFFFF; --janela-topo: #FFFFFF; --janela-lado: #F6F7F9; --linha: rgba(0, 0, 0, .08); --doca: rgba(255, 255, 255, .55);
    --ponto: #1D1D1F; --selecao: rgba(10, 132, 255, .14); --selecao-texto: #0A5BC4;
    position: relative; width: 100vw; height: 100vh; overflow: hidden; container-type: inline-size;
    background: #0B1026 url("{fundo}") center / cover; font: 1cqw/1.45 Inter, system-ui, sans-serif; color: var(--texto);
  }}
  .ecra.escuro {{
    --vidro: rgba(22, 28, 52, .62); --vidro-borda: rgba(255, 255, 255, .14); --texto: #F2F4FA; --texto-2: #A9B2CC;
    --janela: #1A2036; --janela-topo: #1F2640; --janela-lado: #161B2E; --linha: rgba(255, 255, 255, .08); --doca: rgba(22, 28, 52, .5);
    --ponto: #F2F4FA; --selecao: rgba(90, 160, 255, .2); --selecao-texto: #9CC8FF;
  }}
  .vidro {{ background: var(--vidro); border: .07cqw solid var(--vidro-borda); box-shadow: 0 .5cqw 1.6cqw rgba(0, 0, 0, .25);
    -webkit-backdrop-filter: blur(20px) saturate(1.4); backdrop-filter: blur(20px) saturate(1.4); }}
  .glifo {{ width: 1.15cqw; height: 1.15cqw; fill: none; stroke: currentColor; stroke-width: 2; stroke-linecap: round; stroke-linejoin: round; }}

  .ilha {{ position: absolute; top: .8cqw; height: 2.4cqw; border-radius: 1.2cqw; display: flex; align-items: center; gap: 1.1cqw; padding: 0 1.1cqw; font-weight: 600; }}
  .ilha.esq {{ left: .9cqw; }} .ilha.meio {{ left: 50%; transform: translateX(-50%); }} .ilha.dir {{ right: .9cqw; }}
  .ilha .marca {{ font-weight: 800; }}
  .ilha .pilula {{ padding: .2cqw .7cqw; border-radius: .9cqw; background: var(--selecao); color: var(--selecao-texto); }}
  .ilha .fraco {{ color: var(--texto-2); font-weight: 500; }}

  .widget {{ position: absolute; left: 2cqw; border-radius: 1.4cqw; padding: 1.3cqw 1.5cqw; }}
  .relogio {{ top: 5.6cqw; width: 18cqw; }}
  .relogio .h {{ font-size: 4.8cqw; font-weight: 800; letter-spacing: -.04em; line-height: 1; }}
  .relogio .d {{ color: var(--texto-2); margin-top: .4cqw; font-weight: 500; }}
  .recentes {{ top: 17.4cqw; width: 18cqw; }}
  .recentes h3 {{ margin: 0 0 .7cqw; font-size: 1cqw; }}
  .recentes div {{ display: flex; align-items: center; gap: .7cqw; padding: .35cqw 0; font-size: .95cqw; }}
  .recentes img {{ width: 2.1cqw; height: 2.1cqw; }}

  .janela {{ position: absolute; left: 24%; top: 9%; width: 54%; height: 68%; border-radius: 1.3cqw; overflow: hidden; background: var(--janela);
    box-shadow: 0 2cqw 4.5cqw rgba(0, 0, 0, .45), 0 0 0 .07cqw rgba(255, 255, 255, .08); }}
  .jan-topo {{ height: 3.2cqw; display: flex; align-items: center; padding: 0 1.2cqw; background: var(--janela-topo); border-bottom: .07cqw solid var(--linha); font-weight: 600; }}
  .jan-topo .titulo {{ flex: 1; }}
  .fechar {{ width: 1.7cqw; height: 1.7cqw; border-radius: 50%; display: grid; place-items: center; background: var(--linha); font-size: .85cqw; font-weight: 700; }}
  .jan-corpo {{ display: flex; height: calc(100% - 3.2cqw); }}
  .jan-lado {{ width: 24%; background: var(--janela-lado); padding: 1cqw .8cqw; border-right: .07cqw solid var(--linha); color: var(--texto-2); }}
  .jan-lado div {{ padding: .4cqw .7cqw; border-radius: .5cqw; }}
  .jan-lado .ativo {{ background: var(--selecao); color: var(--selecao-texto); font-weight: 600; }}
  .grelha {{ flex: 1; display: grid; grid-template-columns: repeat(4, 1fr); gap: 1.6cqw 1cqw; padding: 1.8cqw; align-content: start; text-align: center; font-size: .95cqw; }}
  .ficheiro svg {{ width: 4.2cqw; height: 3.5cqw; display: block; margin: 0 auto .5cqw; }}

  .doca {{ position: absolute; right: .9cqw; top: 50%; transform: translateY(-50%); display: flex; flex-direction: column; gap: .55cqw;
    padding: .8cqw .65cqw; border-radius: 2cqw; background: var(--doca); border: .07cqw solid var(--vidro-borda);
    -webkit-backdrop-filter: blur(20px); backdrop-filter: blur(20px); box-shadow: 0 .6cqw 2cqw rgba(0, 0, 0, .3); }}
  .doca .item {{ position: relative; display: block; }}
  .doca img {{ width: 3.4cqw; height: 3.4cqw; display: block; transition: transform .14s ease-out; }}
  .doca .item:hover img {{ transform: scale(1.2) translateX(-.4cqw); }}
  .doca .aberta::before {{ content: ""; position: absolute; left: -.5cqw; top: 50%; width: .32cqw; height: .32cqw; margin-top: -.16cqw; border-radius: 50%; background: var(--ponto); }}
</style>
</head>
<body>
<div class="ecra" id="ecra">
  <div class="ilha esq vidro"><span class="marca">≋ Brisa</span><span class="pilula">Aplicações</span><span class="fraco">Janelas</span></div>
  <div class="ilha meio vidro">sex 13 nov · 10:30</div>
  <div class="ilha dir vidro">{WIFI}{SOM}{BAT}<span>97%</span></div>

  <div class="widget relogio vidro"><div class="h">10:30</div><div class="d">Sexta-feira, 13 de novembro</div></div>
  <div class="widget recentes vidro"><h3>Continuar onde ficou</h3>
    <div><img src="{ic['writer']}" alt="">Carta à escola.odt</div>
    <div><img src="{ic['calc']}" alt="">Orçamento de novembro.ods</div>
    <div><img src="{ic['notas']}" alt="">Lista de compras.txt</div>
  </div>

  <div class="janela">
    <div class="jan-topo"><span class="titulo">Documentos</span><span class="fechar">✕</span></div>
    <div class="jan-corpo">
      <div class="jan-lado"><div>Início</div><div class="ativo">Documentos</div><div>Imagens</div><div>Música</div><div>Vídeos</div><div>Transferências</div></div>
      <div class="grelha">{pastas}</div>
    </div>
  </div>

  <nav class="doca" aria-label="Doca">{doca}</nav>
</div>
<script>
  const tema = new URLSearchParams(location.search).get('tema');
  if (tema === 'escuro') document.getElementById('ecra').classList.add('escuro');
  if (new URLSearchParams(location.search).get('janela') === 'nao') document.querySelector('.janela').remove();
</script>
</body>
</html>
'''
saida.write_text(html, encoding='utf-8', newline='\n')
print('maqueta gerada:', saida)
