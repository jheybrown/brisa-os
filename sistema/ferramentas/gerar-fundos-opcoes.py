"""Gera seis fundos novos do Brisa (três claros, três escuros) e uma página para os comparar.

Uso: python gerar-fundos-opcoes.py <pasta de saída>
Escreve <saída>/fundos/<nome>.svg e <saída>/fundos.html. As prévias PNG (<nome>.png) são
desenhadas à parte com rsvg-convert, para usar a mesma letra que a imagem do sistema.
Tudo é gerado por código com semente fixa: o resultado é sempre igual.
"""
import base64
import math
import pathlib
import random
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from brisa_icones import icone  # noqa: E402

saida = pathlib.Path(sys.argv[1])
(saida / 'fundos').mkdir(parents=True, exist_ok=True)
W, H = 1440, 900
ONDAS = '<path d="M3 9c3-3 6-3 9 0s6 3 9 0"/><path d="M3 15c3-3 6-3 9 0s6 3 9 0"/>'
CAB = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" preserveAspectRatio="xMidYMid slice">'


def marca(x, y, cor, tam=88, op=1):
    e = tam / 92
    return (f'<g opacity="{op}"><g transform="translate({x - 43 * e:.1f} {y - 150 * e:.1f}) scale({3.6 * e:.3f})" fill="none" '
            f'stroke="{cor}" stroke-width="2" stroke-linecap="round">{ONDAS}</g>'
            f'<text x="{x}" y="{y}" text-anchor="middle" font-family="Manrope, sans-serif" font-size="{tam}" '
            f'letter-spacing="{10 * e:.1f}" fill="{cor}"><tspan font-weight="800">BRISA</tspan>'
            f'<tspan font-weight="400" dx="{14 * e:.1f}">OS</tspan></text></g>')


def desfoque(i, d):
    return f'<filter id="{i}" filterUnits="userSpaceOnUse" x="-400" y="-400" width="2240" height="1700"><feGaussianBlur stdDeviation="{d}"/></filter>'


def mistura(a, b, q):
    x = [int(a[i:i + 2], 16) for i in (1, 3, 5)]
    y = [int(b[i:i + 2], 16) for i in (1, 3, 5)]
    return '#' + ''.join(f'{round(u + (v - u) * q):02X}' for u, v in zip(x, y))


r = random.Random(7)
F = {}

# ---------- Claros ----------
# 1. Corrente: manchas suaves e linhas de vento a atravessar o ecrã
linhas = ''
for k in range(16):
    y0 = 180 + k * 34
    a1, a2 = r.uniform(-120, 120), r.uniform(-120, 120)
    linhas += (f'<path d="M-40 {y0} C 380 {y0 + a1} 820 {y0 + a2 - 140} 1480 {y0 - 120 + a1 / 2}" '
               f'opacity="{0.25 + 0.5 * math.sin(k / 15 * math.pi):.2f}"/>')
F['corrente'] = ('Corrente', 'claro', f'''{CAB}
  <defs>{desfoque('f', 120)}<linearGradient id="c" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#F3F7FF"/><stop offset="1" stop-color="#EEEAFE"/></linearGradient></defs>
  <rect width="{W}" height="{H}" fill="url(#c)"/>
  <g filter="url(#f)"><ellipse cx="260" cy="180" rx="420" ry="260" fill="#A9D6FF"/><ellipse cx="1220" cy="300" rx="380" ry="300" fill="#D4C4FF"/>
    <ellipse cx="900" cy="860" rx="520" ry="240" fill="#FFD3C0"/><ellipse cx="120" cy="820" rx="320" ry="200" fill="#B8F0DE"/></g>
  <g fill="none" stroke="#FFFFFF" stroke-width="1.6">{linhas}</g>
  {marca(720, 470, '#1B2A5A', 88, .9)}
</svg>''')

# 2. Dunas: areia em camadas ao fim da tarde
F['dunas'] = ('Dunas', 'claro', f'''{CAB}
  <defs>{desfoque('f', 80)}
    <linearGradient id="ceu" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFF6EC"/><stop offset="1" stop-color="#FFE0C7"/></linearGradient>
    <linearGradient id="d1" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F7D3B3"/><stop offset="1" stop-color="#EDBE97"/></linearGradient>
    <linearGradient id="d2" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#EFB98F"/><stop offset="1" stop-color="#DE9F74"/></linearGradient>
    <linearGradient id="d3" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#E0A076"/><stop offset="1" stop-color="#C9835B"/></linearGradient>
    <linearGradient id="d4" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#C98058"/><stop offset="1" stop-color="#A9643F"/></linearGradient>
  </defs>
  <rect width="{W}" height="{H}" fill="url(#ceu)"/>
  <circle cx="1060" cy="330" r="190" fill="#FFC79A" opacity=".55" filter="url(#f)"/><circle cx="1060" cy="330" r="78" fill="#FFF1E2"/>
  <path d="M0 560 C 260 470 480 520 700 560 S 1160 470 1440 520 V900 H0Z" fill="url(#d1)"/>
  <path d="M0 650 C 300 560 560 700 860 640 S 1260 580 1440 640 V900 H0Z" fill="url(#d2)"/>
  <path d="M0 740 C 220 690 520 800 820 740 S 1240 680 1440 750 V900 H0Z" fill="url(#d3)"/>
  <path d="M0 830 C 300 790 640 880 940 830 S 1300 800 1440 840 V900 H0Z" fill="url(#d4)"/>
  {marca(470, 330, '#6A3A20', 84, .88)}
</svg>''')

# 3. Prisma: triângulos claros em azul e lilás
passo = 120
pts = {}
for i in range(-1, W // passo + 3):
    for j in range(-1, H // passo + 3):
        pts[i, j] = (i * passo + r.uniform(-42, 42), j * passo + r.uniform(-42, 42))
tri = ''
cores = ['#EEF3FF', '#E4ECFF', '#EAE6FF', '#F4F1FF', '#DFE8FF', '#E9EEFF']
for i in range(-1, W // passo + 2):
    for j in range(-1, H // passo + 2):
        a, b, c, d = pts[i, j], pts[i + 1, j], pts[i, j + 1], pts[i + 1, j + 1]
        for t1, t2, t3 in ((a, b, d), (a, d, c)):
            cor = mistura(r.choice(cores), '#C9D7FF', r.uniform(0, .35))
            tri += f'<path d="M{t1[0]:.0f} {t1[1]:.0f}L{t2[0]:.0f} {t2[1]:.0f}L{t3[0]:.0f} {t3[1]:.0f}Z" fill="{cor}"/>'
F['prisma'] = ('Prisma', 'claro', f'''{CAB}
  <defs>{desfoque('f', 70)}</defs>
  <g stroke="#FFFFFF" stroke-opacity=".55" stroke-width="1">{tri}</g>
  <ellipse cx="720" cy="430" rx="420" ry="150" fill="#F4F6FF" opacity=".85" filter="url(#f)"/>
  {marca(720, 470, '#1B2A5A', 88)}
</svg>''')

# ---------- Escuros ----------
estrelas = ''.join(f'<circle cx="{r.uniform(0, W):.0f}" cy="{r.uniform(0, 560):.0f}" r="{r.choice([.6, .8, 1, 1.3, 1.7])}" '
                   f'opacity="{r.uniform(.3, .95):.2f}"/>' for _ in range(170))

# 4. Aurora: faixas de luz suaves sobre montanhas escuras
F['aurora'] = ('Aurora', 'escuro', f'''{CAB}
  <defs>{desfoque('f', 46)}{desfoque('g', 10)}
    <linearGradient id="c" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#060A1E"/><stop offset=".7" stop-color="#0E1A3A"/><stop offset="1" stop-color="#12274A"/></linearGradient>
    <linearGradient id="a1" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#2FE0B9" stop-opacity="0"/><stop offset=".3" stop-color="#2FE0B9"/><stop offset=".7" stop-color="#45B8FF"/><stop offset="1" stop-color="#45B8FF" stop-opacity="0"/></linearGradient>
    <linearGradient id="a2" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#8E7BFF" stop-opacity="0"/><stop offset=".5" stop-color="#8E7BFF"/><stop offset="1" stop-color="#2FE0B9" stop-opacity="0"/></linearGradient>
  </defs>
  <rect width="{W}" height="{H}" fill="url(#c)"/>
  <g fill="#FFFFFF">{estrelas}</g>
  <g filter="url(#f)" opacity=".55">
    <path d="M-60 360 C 260 180 520 380 820 250 S 1260 120 1500 220 L1500 330 C 1240 240 1040 420 800 380 S 280 470 -60 470Z" fill="url(#a1)"/>
    <path d="M-60 250 C 300 110 600 270 900 160 S 1300 90 1500 120 L1500 200 C 1300 160 1080 300 880 260 S 300 330 -60 330Z" fill="url(#a2)"/>
  </g>
  <path d="M-60 380 C 260 200 520 400 820 270 S 1260 140 1500 240" fill="none" stroke="#8CF5DA" stroke-width="2.5" opacity=".45" filter="url(#g)"/>
  <path d="M0 690 L150 610 280 660 420 560 560 640 700 580 850 660 990 590 1130 660 1270 580 1440 650 V900 H0Z" fill="#0B1530"/>
  <path d="M0 780 L200 710 380 770 560 690 760 770 940 720 1120 790 1300 720 1440 770 V900 H0Z" fill="#070D20"/>
  {marca(720, 470, '#FFFFFF', 88, .95)}
</svg>''')

# 5. Horizonte: a orla luminosa de um planeta, com estrelas
F['orbita'] = ('Órbita', 'escuro', f'''{CAB}
  <defs>{desfoque('f', 60)}{desfoque('g', 18)}
    <radialGradient id="c" cx=".5" cy=".35" r=".8"><stop offset="0" stop-color="#1B2252"/><stop offset="1" stop-color="#05071A"/></radialGradient>
    <radialGradient id="p" cx=".5" cy="0" r=".9"><stop offset="0" stop-color="#1A2A66"/><stop offset=".25" stop-color="#0B1236"/><stop offset="1" stop-color="#05071A"/></radialGradient>
  </defs>
  <rect width="{W}" height="{H}" fill="url(#c)"/>
  <g fill="#FFFFFF">{estrelas}</g>
  <ellipse cx="720" cy="1420" rx="1180" ry="780" fill="#3E7BFF" opacity=".55" filter="url(#f)"/>
  <ellipse cx="720" cy="1420" rx="1120" ry="740" fill="url(#p)"/>
  <ellipse cx="720" cy="1420" rx="1120" ry="740" fill="none" stroke="#9CC4FF" stroke-width="3" opacity=".9" filter="url(#g)"/>
  <ellipse cx="720" cy="1420" rx="1120" ry="740" fill="none" stroke="#DCEAFF" stroke-width="1.4"/>
  {marca(720, 400, '#FFFFFF', 88, .96)}
</svg>''')

# 6. Seda: fitas de luz largas e suaves sobre grafite
fitas = ''
for k, (c1, c2, larg, op, y, a) in enumerate([
        ('#5B5BFF', '#C66BFF', 170, .60, 600, 190), ('#2E8BFF', '#6A5BFF', 120, .55, 660, -160),
        ('#C66BFF', '#FF6B9E', 90, .45, 560, 230), ('#29D3C9', '#2E8BFF', 70, .40, 720, -120)]):
    fitas += (f'<linearGradient id="s{k}" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="{W}" y2="0">'
              f'<stop offset="0" stop-color="{c1}" stop-opacity="0"/><stop offset=".25" stop-color="{c1}"/>'
              f'<stop offset=".75" stop-color="{c2}"/><stop offset="1" stop-color="{c2}" stop-opacity="0"/></linearGradient>'
              f'<path d="M-120 {y} C 360 {y - a} 900 {y + a} 1560 {y - a / 2}" fill="none" stroke="url(#s{k})" '
              f'stroke-width="{larg}" stroke-linecap="round" opacity="{op}"/>')
F['seda'] = ('Seda', 'escuro', f'''{CAB}
  <defs>{desfoque('f', 26)}<linearGradient id="c" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0F1117"/><stop offset="1" stop-color="#181B26"/></linearGradient></defs>
  <rect width="{W}" height="{H}" fill="url(#c)"/>
  <g filter="url(#f)">{fitas}</g>
  {marca(720, 330, '#FFFFFF', 88, .95)}
</svg>''')

for nome, (_, _, svg) in F.items():
    (saida / 'fundos' / f'{nome}.svg').write_text(svg, encoding='utf-8', newline='\n')

# ---------- Página de comparação ----------
uri = lambda s: 'data:image/svg+xml;base64,' + base64.b64encode(s.encode()).decode()  # noqa: E731
doca = ''.join(f'<span class="item{" aberta" if n in ("ficheiros", "navegador") else ""}"><img src="{uri(icone(n, "vidro"))}" alt=""></span>'
               for n in ['ficheiros', 'navegador', 'writer', 'calc', 'notas', 'calculadora', 'loja', 'definicoes', 'lancador'])
cartoes = ''
for i, (nome, (titulo, tom, _)) in enumerate(F.items(), 1):
    cartoes += f'''
    <figure class="cartao">
      <div class="cena" style="background-image:url('fundos/{nome}.png')">
        <div class="ilha esq">≋ Brisa</div><div class="ilha meio">sex 13 nov · 10:30</div><div class="ilha dir">97%</div>
        <nav class="doca">{doca}</nav>
      </div>
      <figcaption><b>{i}. {titulo}</b><span>{'Claro' if tom == 'claro' else 'Escuro'}</span></figcaption>
    </figure>'''

(saida / 'fundos.html').write_text(f'''<!doctype html>
<html lang="pt">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Fundos do Brisa</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
  * {{ box-sizing: border-box; }}
  body {{ margin: 0; background: #EEF1F7; color: #141B33; font: 15px/1.5 Inter, system-ui, sans-serif; }}
  main {{ max-width: 1180px; margin: 0 auto; padding: 32px 16px 56px; }}
  h1 {{ font-size: 30px; line-height: 1.15; letter-spacing: -.02em; margin: 0 0 6px; }}
  .intro {{ color: #4A5470; margin: 0 0 24px; max-width: 70ch; }}
  .grelha {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(340px, 1fr)); gap: 20px; }}
  .cartao {{ margin: 0; background: #fff; border: 1px solid #D9DEEA; border-radius: 16px; padding: 10px; }}
  .cena {{ position: relative; aspect-ratio: 16 / 10; border-radius: 10px; overflow: hidden; background: #ccd center / cover; container-type: inline-size; }}
  .ilha {{ position: absolute; top: 2.4cqw; font-size: 2.6cqw; font-weight: 600; padding: .6cqw 2cqw; border-radius: 99px;
    background: rgba(255,255,255,.8); border: 1px solid rgba(255,255,255,.95); white-space: nowrap; color: #1D1D1F; }}
  .ilha.esq {{ left: 2.4cqw; }} .ilha.meio {{ left: 50%; transform: translateX(-50%); }} .ilha.dir {{ right: 2.4cqw; }}
  .doca {{ position: absolute; right: 2.4cqw; top: 55%; transform: translateY(-50%); display: flex; flex-direction: column; gap: .7cqw;
    padding: 1.2cqw 1cqw; border-radius: 3.4cqw; background: rgba(255,255,255,.55); border: 1px solid rgba(255,255,255,.85); }}
  .doca .item {{ position: relative; display: block; }}
  .doca img {{ width: 4.3cqw; height: 4.3cqw; display: block; }}
  .doca .aberta::before {{ content: ""; position: absolute; left: -1cqw; top: 50%; width: .7cqw; height: .7cqw; margin-top: -.35cqw; border-radius: 50%; background: #1D1D1F; }}
  figcaption {{ display: flex; justify-content: space-between; align-items: baseline; padding: 10px 4px 2px; }}
  figcaption b {{ font-size: 16px; }}
  figcaption span {{ color: #4A5470; font-size: 13.5px; }}
</style>
</head>
<body>
<main>
  <h1>Fundos do Brisa</h1>
  <p class="intro">Seis fundos novos com o nome do sistema: três claros e três escuros. Cada um aparece com o layout Ilhas e a doca Vidro por cima, como ficaria no ecrã.</p>
  <div class="grelha">{cartoes}
  </div>
</main>
</body>
</html>
''', encoding='utf-8', newline='\n')
print('6 fundos e a pagina gerados em', saida)
