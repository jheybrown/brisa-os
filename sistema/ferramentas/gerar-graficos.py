"""Gera os gráficos do Brisa 1.0 em SVG: ícones Vidro, versões para a doca e o logótipo.

Uso:  python gerar-graficos.py <pasta de destino usr/share/brisa>
Os fundos vêm de gerar-fundos-opcoes.py (pasta layouts/fundos) e são copiados à parte.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from brisa_icones import ORDEM, icone  # noqa: E402

dest = pathlib.Path(sys.argv[1])
(dest / 'icones' / 'doca').mkdir(parents=True, exist_ok=True)


def escrever(caminho, texto):
    caminho.write_text(texto, encoding='utf-8', newline='\n')


# Ícones Vidro, usados nas aplicações do Brisa e no ecrã de Aplicações
for nome in ORDEM:
    escrever(dest / 'icones' / f'{nome}.svg', icone(nome, 'vidro'))

# Versões para a doca escura: vidro mais opaco, e o ponto de "aberta" à esquerda
for nome in ORDEM:
    interior = icone(nome, 'vidro').replace('fill-opacity=".72"', 'fill-opacity=".92"')
    interior = interior.replace('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 96 96">',
                                '<svg x="12" y="0" width="96" height="96" viewBox="0 0 96 96">')
    for aberto, sufixo in ((False, ''), (True, '-aberto')):
        ponto = '<circle cx="4.5" cy="48" r="3.8" fill="#FFFFFF" fill-opacity=".9"/>' if aberto else ''
        escrever(dest / 'icones' / 'doca' / f'{nome}{sufixo}.svg',
                 f'<svg xmlns="http://www.w3.org/2000/svg" width="108" height="96" viewBox="0 0 108 96">{ponto}{interior}</svg>\n')

# Logótipo: círculo azul com as ondas do Brisa
escrever(dest / 'icones' / 'brisa.svg', '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 96 96">
  <defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5AA2FF"/><stop offset="1" stop-color="#1F5FD0"/></linearGradient></defs>
  <circle cx="48" cy="48" r="44" fill="url(#g)"/>
  <g transform="translate(18 18) scale(2.5)" fill="none" stroke="#FFFFFF" stroke-width="2" stroke-linecap="round">
    <path d="M3 9c3-3 6-3 9 0s6 3 9 0"/><path d="M3 15c3-3 6-3 9 0s6 3 9 0"/>
  </g>
</svg>
''')
print(f'{len(ORDEM)} icones Vidro, versoes da doca e logotipo em {dest}')
