# limpar.py — gera a versão sem comentários dentro de docs/
import pathlib, re

ORIGEM  = pathlib.Path(".")
DESTINO = pathlib.Path("docs")
ARQUIVOS = ["index.html", "styles.css", "scripts.js"]

def limpar_html(t):
    t = re.sub(r"<!--.*?-->", "", t, flags=re.S)
    return re.sub(r"\n\s*\n+", "\n\n", t)

def limpar_css(t):
    t = re.sub(r"/\*.*?\*/", "", t, flags=re.S)
    return re.sub(r"\n\s*\n+", "\n\n", t)

def limpar_js(t):
    out, i, n = [], 0, len(t)
    while i < n:
        c = t[i]
        # preserva strings inteiras (não mexe em // dentro delas)
        if c in "'\"`":
            q = c
            out.append(c); i += 1
            while i < n:
                if t[i] == "\\":
                    out.append(t[i:i+2]); i += 2; continue
                out.append(t[i])
                if t[i] == q:
                    i += 1; break
                i += 1
            continue
        # comentário de linha
        if c == "/" and i + 1 < n and t[i+1] == "/":
            while i < n and t[i] != "\n":
                i += 1
            continue
        # comentário de bloco
        if c == "/" and i + 1 < n and t[i+1] == "*":
            i += 2
            while i + 1 < n and not (t[i] == "*" and t[i+1] == "/"):
                i += 1
            i += 2
            continue
        out.append(c); i += 1
    return re.sub(r"\n\s*\n+", "\n\n", "".join(out))

DESTINO.mkdir(exist_ok=True)

for nome in ARQUIVOS:
    origem = ORIGEM / nome
    if not origem.exists():
        print("não encontrado:", nome)
        continue
    texto = origem.read_text(encoding="utf-8")
    if nome.endswith(".html"):   texto = limpar_html(texto)
    elif nome.endswith(".css"):  texto = limpar_css(texto)
    else:                        texto = limpar_js(texto)
    (DESTINO / nome).write_text(texto, encoding="utf-8")
    print("gerado:", nome)

print("Pronto. Versão limpa em:", DESTINO.resolve())