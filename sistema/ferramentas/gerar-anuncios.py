"""Gera três anúncios do Brisa OS em SVG, a partir de uma captura real e dos ícones do sistema.

Uso: python gerar-anuncios.py <captura.png> <pasta dos ícones> <pasta de saída>
"""
import base64
import pathlib
import sys

captura, icones, saida = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]), pathlib.Path(sys.argv[3])
saida.mkdir(parents=True, exist_ok=True)

ECRA = 'data:image/png;base64,' + base64.b64encode(captura.read_bytes()).decode()


def icone(nome):
    return 'data:image/svg+xml;base64,' + base64.b64encode((icones / f'{nome}.svg').read_bytes()).decode()


FONTE = 'font-family="Manrope, sans-serif"'
ONDAS = '<path d="M3 9c3-3 6-3 9 0s6 3 9 0"/><path d="M3 15c3-3 6-3 9 0s6 3 9 0"/>'


def logo(x, y, cor, tam=26):
    """Símbolo e nome BRISA OS alinhados à esquerda em (x, y = linha de base)."""
    e = tam / 26
    return (f'<g transform="translate({x} {y - 22 * e}) scale({1.25 * e})" fill="none" stroke="{cor}" stroke-width="2.2" stroke-linecap="round">{ONDAS}</g>'
            f'<text x="{x + 38 * e}" y="{y}" {FONTE} font-size="{tam}" letter-spacing="{3 * e}" fill="{cor}">'
            f'<tspan font-weight="800">BRISA</tspan><tspan font-weight="400" dx="{5 * e}">OS</tspan></text>')


def linhas(x, y, textos, tam, cor, peso=800, entre=1.12, ancora='start'):
    out = f'<text x="{x}" y="{y}" {FONTE} font-size="{tam}" font-weight="{peso}" fill="{cor}" text-anchor="{ancora}" letter-spacing="{-tam * 0.02:.1f}">'
    for i, t in enumerate(textos):
        out += f'<tspan x="{x}" dy="{0 if i == 0 else tam * entre:.0f}">{t}</tspan>'
    return out + '</text>'


def portatil(x, y, larg):
    """Um portátil simples com a captura real no ecrã. (x, y) é o canto superior esquerdo da tampa."""
    alt = larg * 0.655
    m = larg * 0.03
    ecr_l, ecr_a = larg - 2 * m, (larg - 2 * m) * 800 / 1280
    base_y = y + alt
    return f'''<g>
    <ellipse cx="{x + larg / 2}" cy="{base_y + larg * 0.05}" rx="{larg * 0.6}" ry="{larg * 0.035}" fill="#0A1030" opacity=".22" filter="url(#sombra)"/>
    <rect x="{x}" y="{y}" width="{larg}" height="{alt}" rx="{larg * 0.025}" fill="#1B2130"/>
    <image href="{ECRA}" x="{x + m}" y="{y + m}" width="{ecr_l}" height="{ecr_a}" preserveAspectRatio="xMidYMid slice"/>
    <path d="M{x - larg * 0.08} {base_y} H{x + larg * 1.08} l{-larg * 0.03} {larg * 0.035} H{x - larg * 0.05}Z" fill="#C9CFDC"/>
    <rect x="{x + larg * 0.42}" y="{base_y}" width="{larg * 0.16}" height="{larg * 0.012}" rx="{larg * 0.006}" fill="#A7AEC0"/>
  </g>'''


def botao(x, y, texto, tam=22, fundo='#2F7BF6', cor='#FFFFFF'):
    larg = len(texto) * tam * 0.56 + tam * 2.2
    return (f'<rect x="{x}" y="{y}" width="{larg:.0f}" height="{tam * 2.5:.0f}" rx="{tam * 1.25:.0f}" fill="{fundo}"/>'
            f'<text x="{x + larg / 2:.0f}" y="{y + tam * 1.6:.0f}" {FONTE} font-size="{tam}" font-weight="700" fill="{cor}" text-anchor="middle">{texto}</text>')


DEFS = '''<defs>
    <filter id="sombra" x="-20%" y="-200%" width="140%" height="500%"><feGaussianBlur stdDeviation="14"/></filter>
    <filter id="halo" filterUnits="userSpaceOnUse" x="-500" y="-500" width="3000" height="3000"><feGaussianBlur stdDeviation="90"/></filter>
  </defs>'''

# ---------- 1. Banner 1200x628: o portátil antigo ----------
a1 = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="628" viewBox="0 0 1200 628">
  {DEFS}
  <rect width="1200" height="628" fill="#EEF2FF"/>
  <g filter="url(#halo)">
    <ellipse cx="180" cy="80" rx="380" ry="240" fill="#BFD8FF"/>
    <ellipse cx="1050" cy="560" rx="420" ry="260" fill="#FFD9C4"/>
    <ellipse cx="900" cy="90" rx="300" ry="200" fill="#DCCBFF"/>
  </g>
  {logo(64, 92, '#17357A', 24)}
  {linhas(64, 190, ['O teu portátil', 'antigo ainda tem', 'muito para dar.'], 50, '#141B33')}
  {linhas(64, 380, ['Um sistema leve e bonito, com Office', 'incluído e capaz de abrir muitos', 'programas do Windows.'], 21, '#3F4860', 500, 1.45)}
  {botao(64, 488, 'Experimenta grátis numa pen USB', 20)}
  {portatil(612, 132, 520)}
</svg>
'''

# ---------- 2. Quadrado 1080x1080: leve, bonito, em português ----------
nomes = ['ficheiros', 'navegador', 'escritorio', 'notas', 'loja', 'definicoes']
fila = ''.join(f'<image href="{icone(n)}" x="{258 + i * 98}" y="402" width="88" height="88"/>' for i, n in enumerate(nomes))
a2 = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1080" viewBox="0 0 1080 1080">
  {DEFS}
  <defs><linearGradient id="fd" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0B1433"/><stop offset="1" stop-color="#18245A"/></linearGradient></defs>
  <rect width="1080" height="1080" fill="url(#fd)"/>
  <g filter="url(#halo)"><ellipse cx="540" cy="900" rx="520" ry="200" fill="#3A5BE0" opacity=".55"/><ellipse cx="900" cy="120" rx="300" ry="200" fill="#8A4FE0" opacity=".45"/></g>
  <g transform="translate(540 120)">{logo(-118, 0, '#FFFFFF', 30)}</g>
  {linhas(540, 250, ['Leve. Bonito.', 'Em português.'], 76, '#FFFFFF', 800, 1.08, 'middle').replace('<tspan x="540"', '<tspan x="540"')}
  {fila}
  {portatil(250, 560, 580)}
  <text x="540" y="1032" {FONTE} font-size="24" font-weight="600" fill="#BFCBF2" text-anchor="middle">Gratuito, sem licenças. Experimenta numa pen USB.</text>
</svg>
'''

# ---------- 3. Vertical 1080x1920 (stories): o que traz ----------
cartoes = [
    ('escritorio', 'Office incluído', 'Documentos, folhas de cálculo e apresentações.'),
    ('windows', 'Programas do Windows', 'Abre muitos .exe com um duplo clique.'),
    ('loja', 'Loja simples', 'Chrome, Zoom, Spotify e mais, com um clique.'),
]
bloco = ''
for i, (ic, tit, txt) in enumerate(cartoes):
    y = 560 + i * 196
    bloco += (f'<rect x="90" y="{y}" width="900" height="168" rx="34" fill="#FFFFFF" fill-opacity=".82"/>'
              f'<image href="{icone(ic)}" x="124" y="{y + 30}" width="108" height="108"/>'
              f'<text x="266" y="{y + 72}" {FONTE} font-size="38" font-weight="800" fill="#141B33">{tit}</text>'
              f'<text x="266" y="{y + 120}" {FONTE} font-size="27" font-weight="500" fill="#3F4860">{txt}</text>')
a3 = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1920" viewBox="0 0 1080 1920">
  {DEFS}
  <defs><linearGradient id="fa" x1="0" y1="1" x2="1" y2="0"><stop offset="0" stop-color="#FFD9B8"/><stop offset=".4" stop-color="#FFC4D8"/><stop offset=".75" stop-color="#CDB8FF"/><stop offset="1" stop-color="#9CC6FF"/></linearGradient></defs>
  <rect width="1080" height="1920" fill="url(#fa)"/>
  {logo(90, 170, '#17357A', 34)}
  {linhas(90, 300, ['Tudo o que precisas.', 'Nada que te atrase.'], 72, '#141B33', 800, 1.1)}
  {bloco}
  {portatil(170, 1240, 740)}
  {botao(250, 1790, 'Descarrega e experimenta grátis', 28)}
</svg>
'''

for nome, svg in (('anuncio-1-banner', a1), ('anuncio-2-quadrado', a2), ('anuncio-3-vertical', a3)):
    (saida / f'{nome}.svg').write_text(svg, encoding='utf-8', newline='\n')
print('3 anuncios gerados')
