#!/usr/bin/env python3
"""Arma el sitio de propuestas de CICSA Energy para GitHub Pages (repo «cicsa» → https://aldobohorquez.github.io/cicsa/).

Uso (desde esta carpeta):  python3 -I armar.py
1. Compila las 4 propuestas con base-href relativo («./»), para que funcionen dentro de /1/, /2/, /3/ y /4/.
2. Copia cada compilación a su carpeta y le agrega:
   - la barra «Propuestas · 1 2 3 4» para brincar entre ellas;
   - <meta name="robots" content="noindex"> para que Google no las indexe.
La portada (index.html) y las miniaturas (img/) se editan a mano; este script no las toca.
"""
import pathlib, re, shutil, subprocess, sys

AQUI = pathlib.Path(__file__).resolve().parent
GITHUB = AQUI.parent
PROPUESTAS = [  # (carpeta del sitio, proyecto Angular, nombre corto)
    ('1', 'cicsa-energy-propuesta-solar', 'Renovables'),
    ('2', 'cicsa-energy', 'Ejecutiva'),
    ('3', 'cicsa-energy-propuesta-creativa', 'Creativa'),
    ('4', 'cicsa-energy-propuesta-fotos', 'Referencias'),
]

ESTILO = """<style id="cicsa-prop-css">
#cicsa-prop{position:fixed;left:50%;bottom:14px;transform:translateX(-50%);z-index:2147483000;display:flex;align-items:center;gap:2px;padding:5px;border-radius:999px;background:rgba(14,17,26,.9);-webkit-backdrop-filter:blur(10px);backdrop-filter:blur(10px);box-shadow:0 12px 30px -12px rgba(0,0,0,.6);font:600 12.5px/1 system-ui,-apple-system,'Segoe UI',sans-serif;color:#fff}
#cicsa-prop a{display:inline-flex;align-items:center;justify-content:center;min-width:34px;height:34px;padding:0 11px;border-radius:999px;color:rgba(255,255,255,.78);text-decoration:none;transition:background .2s,color .2s}
#cicsa-prop a:hover{background:rgba(255,255,255,.12);color:#fff}
#cicsa-prop a.on{background:#fff;color:#0e111a}
#cicsa-prop .sep{width:1px;height:18px;background:rgba(255,255,255,.2);margin:0 4px}
#cicsa-prop .nom{display:none;padding:0 10px 0 4px;color:rgba(255,255,255,.6);font-weight:500}
@media (min-width:700px){#cicsa-prop .nom{display:inline}}
@media (max-width:700px){.notas-btn{bottom:66px!important}.wa-fab{bottom:66px!important}}
@media print{#cicsa-prop{display:none}}
</style>"""


def barra(actual: str, nombre: str) -> str:
    on = ' class="on" aria-current="page"'
    nums = ''.join(f'<a href="../{n}/"{on if n == actual else ""} title="Propuesta {n} · {nom}">{n}</a>'
                   for n, _, nom in PROPUESTAS)
    return (f'<nav id="cicsa-prop" aria-label="Propuestas de diseño"><a href="../" title="Ver todas las propuestas">☰ Propuestas</a>'
            f'<span class="sep"></span>{nums}<span class="nom">{nombre}</span></nav>')


def main():
    for carpeta, proyecto, nombre in PROPUESTAS:
        src = GITHUB / proyecto
        print(f'→ Propuesta {carpeta} · {nombre} ({proyecto})', flush=True)
        r = subprocess.run(['npx', 'ng', 'build', '--base-href', './'], cwd=src, capture_output=True, text=True)
        if r.returncode != 0:
            print(r.stdout[-2000:], r.stderr[-2000:]); sys.exit(f'Falló la compilación de {proyecto}')
        dist = src / 'dist' / 'cicsa-energy' / 'browser'
        dest = AQUI / carpeta
        if dest.exists():
            shutil.rmtree(dest)
        shutil.copytree(dist, dest)
        idx = dest / 'index.html'
        html = idx.read_text(encoding='utf-8')
        html = html.replace('<meta charset="utf-8">', '<meta charset="utf-8">\n  <meta name="robots" content="noindex, nofollow">', 1)
        html = re.sub(r'<title>(.*?)</title>', lambda m: f'<title>Propuesta {carpeta} · {m.group(1)}</title>', html, count=1)
        html = html.replace('</head>', ESTILO + '\n</head>', 1)
        html = html.replace('</body>', barra(carpeta, nombre) + '\n</body>', 1)
        idx.write_text(html, encoding='utf-8')
    (AQUI / '.nojekyll').write_text('')
    print('Listo. Revisa con:  python3 -m http.server 4310  (y abre http://localhost:4310/)')


if __name__ == '__main__':
    main()
