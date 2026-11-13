"""Gera três estilos novos de ícones para a doca e uma página HTML para os comparar.

Uso: python gerar-icones-opcoes.py <pasta usr/share/brisa> <ficheiro html de saída>
Os símbolos são formas preenchidas em duas camadas (classe p = principal, s = secundária),
o que permite pintar o mesmo desenho em estilos diferentes.
"""
import base64
import math
import pathlib
import sys

brisa, saida = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])


sys.path.insert(0, str(pathlib.Path(__file__).parent))
from brisa_icones import ORDEM, SIMBOLOS, icone  # noqa: E402


def uri(svg_texto):
    return 'data:image/svg+xml;base64,' + base64.b64encode(svg_texto.encode()).decode()


ATUAL = {'ficheiros': 'ficheiros', 'navegador': 'navegador', 'writer': 'writer', 'calc': 'calc', 'notas': 'notas',
         'calculadora': 'calculadora', 'loja': 'loja', 'definicoes': 'definicoes', 'lancador': 'lancador'}

ESTILOS = [
    ('pastel', '1. Pastel', 'Mosaico de cor suave com o símbolo em dois tons da mesma cor. Calmo e legível; combina com o vidro das ilhas.'),
    ('vidro', '2. Vidro', 'Círculo de vidro claro com o símbolo colorido. O mais discreto: o fundo continua a ver-se.'),
    ('solido', '3. Sólido', 'Círculo de cor viva com o símbolo branco. O mais forte e o mais fácil de distinguir de longe.'),
    ('atual', 'Atual', 'Mosaico 3D com traço fino, para comparar.'),
]

fundo = uri((brisa / 'fundos' / 'rede.svg').read_text(encoding='utf-8'))
blocos = []
for chave, titulo, texto in ESTILOS:
    icones = []
    for n in ORDEM:
        if chave == 'atual':
            u = uri((brisa / 'icones' / f'{ATUAL[n]}.svg').read_text(encoding='utf-8'))
        else:
            u = uri(icone(n, chave))
        icones.append((n, u))
    doca = ''.join(f'<span class="item{" aberta" if n in ("ficheiros", "navegador") else ""}"><img src="{u}" alt=""></span>' for n, u in icones)
    fila = ''.join(f'<figure><img src="{u}" alt=""><figcaption>{SIMBOLOS[n][0]}</figcaption></figure>' for n, u in icones)
    blocos.append(f'''
  <section class="estilo" aria-labelledby="t-{chave}">
    <div class="cena">
      <div class="ilha">sex 13 nov · 10:30</div>
      <nav class="doca" aria-label="Doca no estilo {titulo}">{doca}</nav>
    </div>
    <div class="texto">
      <h2 id="t-{chave}">{titulo}</h2>
      <p>{texto}</p>
      <div class="fila">{fila}</div>
    </div>
  </section>''')

html = f'''<!doctype html>
<html lang="pt">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Ícones da doca</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
  * {{ box-sizing: border-box; }}
  body {{ margin: 0; background: #EEF1F7; color: #141B33; font: 15px/1.5 Inter, system-ui, sans-serif; }}
  main {{ max-width: 1100px; margin: 0 auto; padding: 32px 16px 56px; }}
  h1 {{ font-size: 30px; line-height: 1.15; letter-spacing: -.02em; margin: 0 0 6px; }}
  .intro {{ color: #4A5470; margin: 0 0 26px; max-width: 70ch; }}
  .estilo {{ display: grid; grid-template-columns: 300px minmax(0, 1fr); gap: 24px; align-items: center;
    background: #fff; border: 1px solid #D9DEEA; border-radius: 16px; padding: 18px; margin-bottom: 18px; }}
  .cena {{ position: relative; height: 420px; border-radius: 12px; overflow: hidden; background: url('{fundo}') 70% center / cover; }}
  .ilha {{ position: absolute; top: 12px; left: 50%; transform: translateX(-50%); white-space: nowrap; font-weight: 600; font-size: 13px;
    padding: 5px 14px; border-radius: 999px; background: rgba(255,255,255,.8); border: 1px solid rgba(255,255,255,.95); }}
  .doca {{ position: absolute; right: 14px; top: 50%; transform: translateY(-50%); display: flex; flex-direction: column; gap: 6px;
    padding: 10px 8px; border-radius: 26px; background: rgba(255,255,255,.58); border: 1px solid rgba(255,255,255,.85);
    box-shadow: 0 6px 20px rgba(20,27,51,.12); }}
  .doca img {{ width: 40px; height: 40px; display: block; position: relative; transition: transform .14s ease-out; }}
  .doca img:hover {{ transform: scale(1.18) translateX(-4px); }}
  .doca .item {{ position: relative; display: block; }}
  .doca .aberta::before {{ content: ""; position: absolute; left: -6px; top: 50%; width: 4px; height: 4px; margin-top: -2px;
    border-radius: 50%; background: #1D1D1F; }}
  .texto h2 {{ font-size: 21px; margin: 0 0 4px; letter-spacing: -.01em; }}
  .texto p {{ color: #4A5470; margin: 0 0 16px; max-width: 60ch; }}
  .fila {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(88px, 1fr)); gap: 14px 8px; }}
  figure {{ margin: 0; text-align: center; }}
  figure img {{ width: 64px; height: 64px; display: block; margin: 0 auto 6px; }}
  figcaption {{ font-size: 12.5px; color: #3A3F4F; }}
  @media (max-width: 760px) {{ .estilo {{ grid-template-columns: 1fr; }} .cena {{ height: 380px; }} }}
</style>
</head>
<body>
<main>
  <h1>Ícones da doca</h1>
  <p class="intro">Três estilos novos para os ícones, já na doca vertical do layout Ilhas. Os símbolos foram redesenhados com formas
  preenchidas, mais fáceis de reconhecer do que os traços finos atuais. O último bloco mostra os ícones de agora, para comparar.
  Passe o rato pela doca para ver o efeito de ampliação.</p>
  {''.join(blocos)}
</main>
</body>
</html>
'''
saida.write_text(html, encoding='utf-8', newline='\n')
print('pagina gerada:', saida, len(html) // 1024, 'KB')
