"""Símbolos e estilos dos ícones da doca do Brisa (partilhado pelos geradores)."""
import math


def mistura(cor, alvo, quanto):
    a = [int(cor[i:i + 2], 16) for i in (1, 3, 5)]
    b = [int(alvo[i:i + 2], 16) for i in (1, 3, 5)]
    return '#' + ''.join(f'{round(x + (y - x) * quanto):02X}' for x, y in zip(a, b))


def roda_dentada():
    pts = []
    for k in range(8):
        base = k * math.pi / 4
        for ang, r in ((-0.30, 7.2), (-0.17, 9.6), (0.17, 9.6), (0.30, 7.2)):
            pts.append((12 + r * math.cos(base + ang), 12 + r * math.sin(base + ang)))
    return 'M' + 'L'.join(f'{x:.2f} {y:.2f}' for x, y in pts) + 'Z'


# Símbolos num quadro de 24x24. p = camada principal, s = secundária, l = traço principal
SIMBOLOS = {
    'ficheiros': ('Ficheiros', '#2F7BF6',
                  '<path class="s" d="M3 7.5A2.5 2.5 0 0 1 5.5 5h3.7l2 2h7.3A2.5 2.5 0 0 1 21 9.5V12H3z"/>'
                  '<path class="p" d="M3 10.5h18v7a2.5 2.5 0 0 1-2.5 2.5h-13A2.5 2.5 0 0 1 3 17.5z"/>'),
    'navegador': ('Navegador', '#F0683C',
                  '<circle class="s" cx="12" cy="12" r="9"/>'
                  '<path class="p" d="M16.2 7.8l-2.6 5.8-5.8 2.6 2.6-5.8z"/><circle class="s" cx="12" cy="12" r="1.3"/>'),
    'writer': ('Writer', '#2B6FD6',
               '<path class="s" d="M6.5 3h7.5l4.5 4.5v12A1.5 1.5 0 0 1 17 21H6.5A1.5 1.5 0 0 1 5 19.5v-15A1.5 1.5 0 0 1 6.5 3z"/>'
               '<path class="p" d="M14 3v3a1.5 1.5 0 0 0 1.5 1.5h3z"/>'
               '<rect class="p" x="8" y="11" width="7.5" height="1.7" rx=".85"/><rect class="p" x="8" y="14.2" width="7.5" height="1.7" rx=".85"/>'
               '<rect class="p" x="8" y="17.4" width="4.6" height="1.7" rx=".85"/>'),
    'calc': ('Calc', '#1E9E5A',
             '<rect class="s" x="3.5" y="3.5" width="17" height="17" rx="3"/>'
             '<path class="p" d="M3.5 6.5a3 3 0 0 1 3-3h11a3 3 0 0 1 3 3v2.8h-17z"/>'
             '<path class="l" d="M3.5 14.6h17M9.6 9.3v11.2"/>'),
    'notas': ('Notas', '#F2A93B',
              '<rect class="s" x="4.5" y="3" width="15" height="18" rx="2.5"/>'
              '<path class="p" d="M4.5 5.5A2.5 2.5 0 0 1 7 3h10a2.5 2.5 0 0 1 2.5 2.5V7h-15z"/>'
              '<rect class="p" x="7.5" y="10" width="9" height="1.7" rx=".85"/><rect class="p" x="7.5" y="13.4" width="9" height="1.7" rx=".85"/>'
              '<rect class="p" x="7.5" y="16.8" width="5.5" height="1.7" rx=".85"/>'),
    'calculadora': ('Calculadora', '#B8336A',
                    '<rect class="s" x="5" y="2.5" width="14" height="19" rx="3"/>'
                    '<rect class="p" x="7.5" y="5" width="9" height="4.2" rx="1.2"/>'
                    + ''.join(f'<circle class="p" cx="{x}" cy="{y}" r="1.25"/>' for y in (12.6, 16.8) for x in (9, 12, 15))),
    'loja': ('Loja', '#7A45F0',
             '<path class="s" d="M5 8.5h14l-1.1 11.1A1.6 1.6 0 0 1 16.3 21H7.7a1.6 1.6 0 0 1-1.6-1.4z"/>'
             '<path class="l" d="M9 10V7.5a3 3 0 0 1 6 0V10"/>'),
    'definicoes': ('Definições', '#64748B',
                   f'<path class="p" d="{roda_dentada()}"/><circle class="s" cx="12" cy="12" r="3.4"/>'),
    'lancador': ('Aplicações', '#5B6478',
                 '<rect class="p" x="4" y="4" width="7" height="7" rx="2"/><rect class="p" x="13" y="4" width="7" height="7" rx="2"/>'
                 '<rect class="p" x="4" y="13" width="7" height="7" rx="2"/><rect class="s" x="13" y="13" width="7" height="7" rx="2"/>'),
}
ORDEM = ['ficheiros', 'navegador', 'writer', 'calc', 'notas', 'calculadora', 'loja', 'definicoes', 'lancador']


def icone(nome, estilo):
    _, cor, desenho = SIMBOLOS[nome]
    if estilo == 'pastel':
        fundo = f'<rect x="4" y="4" width="88" height="88" rx="24" fill="{mistura(cor, "#FFFFFF", .84)}"/>' \
                f'<rect x="4.5" y="4.5" width="87" height="87" rx="23.5" fill="none" stroke="{mistura(cor, "#FFFFFF", .6)}" stroke-width="1"/>'
        p, s = mistura(cor, '#000000', .08), mistura(cor, '#FFFFFF', .48)
    elif estilo == 'vidro':
        fundo = ('<circle cx="48" cy="48" r="44" fill="#FFFFFF" fill-opacity=".72"/>'
                 '<circle cx="48" cy="48" r="43.5" fill="none" stroke="#FFFFFF" stroke-width="1.5"/>'
                 '<circle cx="48" cy="48" r="44" fill="none" stroke="#141B33" stroke-opacity=".08"/>')
        p, s = cor, mistura(cor, '#FFFFFF', .62)
    else:  # solido
        fundo = (f'<defs><linearGradient id="g-{nome}" x1="0" y1="0" x2="0" y2="1">'
                 f'<stop offset="0" stop-color="{mistura(cor, "#FFFFFF", .18)}"/><stop offset="1" stop-color="{mistura(cor, "#000000", .12)}"/></linearGradient></defs>'
                 f'<circle cx="48" cy="48" r="44" fill="url(#g-{nome})"/>')
        p, s = '#FFFFFF', mistura(cor, '#FFFFFF', .55)
    simbolo = desenho.replace('class="p"', f'fill="{p}"').replace('class="s"', f'fill="{s}"') \
                     .replace('class="l"', f'fill="none" stroke="{p}" stroke-width="1.9" stroke-linecap="round"')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 96 96">{fundo}'
            f'<g transform="translate(18 18) scale(2.5)">{simbolo}</g></svg>')
