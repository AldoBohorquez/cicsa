# CICSA Energy · sitio de propuestas (GitHub Pages)

Se publica en **https://aldobohorquez.github.io/cicsa/** (repositorio `AldoBohorquez/cicsa`, público, sin código fuente: solo los sitios ya compilados).

| Ruta | Qué es | Proyecto de origen |
|---|---|---|
| `/` | Portada con las 4 propuestas (`index.html`, miniaturas en `img/`) | esta carpeta |
| `/1/` | Renovables | `../cicsa-energy-propuesta-solar` |
| `/2/` | Ejecutiva | `../cicsa-energy` |
| `/3/` | Creativa elegante | `../cicsa-energy-propuesta-creativa` |
| `/4/` | Fotográfica | `../cicsa-energy-propuesta-fotos` |

- Cada propuesta lleva abajo una barra «☰ Propuestas · 1 2 3 4» para brincar entre ellas, y la etiqueta `noindex` para que Google no la indexe.
- Las dos cosas las pone `armar.py`, que también recompila las cuatro con `--base-href ./`.
- **Derechos:** © 2026 CosmoSoftWorks, todos los derechos reservados (ver `LICENSE`). Ser público no da permiso de usar el diseño ni el código.
- Ojo: el repositorio es público, así que cualquiera con el enlace puede ver las propuestas. No hay datos privados: todo sale de la constancia fiscal.

## Publicar por primera vez
1. Desde esta carpeta, sube el sitio:
   ```bash
   git init -b main && git add . && git commit -m "Propuestas de sitio web CICSA Energy"
   gh repo create cicsa --public --source=. --push
   ```
2. Activa GitHub Pages desde la rama `main` y la carpeta raíz:
   ```bash
   gh api -X POST repos/AldoBohorquez/cicsa/pages -f "source[branch]=main" -f "source[path]=/"
   ```
3. En uno o dos minutos queda en https://aldobohorquez.github.io/cicsa/.

## Actualizar después de cambiar una propuesta
```bash
python3 -I armar.py
git add . && git commit -m "Actualiza propuestas" && git push
```

## Probar en local
```bash
python3 -m http.server 4310
```
Después abre http://localhost:4310/.
