#!/usr/bin/env python3
"""Rigenera i PDF della collana "Claude Cheatsheets" a partire dai sorgenti HTML.

Uso:
    python3 build.py                # tutti i volumi, entrambe le lingue → output/{it,en}/
    python3 build.py 03             # solo il volume 03 (entrambe le lingue)
    python3 build.py 03 --lang=en   # solo il volume 03 inglese
    python3 build.py --zip          # tutto + claude-cheatsheets-{it,en}.zip
    python3 build.py --index        # genera anche output/index.html (per GitHub Pages)

Requisiti: weasyprint (pip install weasyprint --break-system-packages).
Su alcuni sistemi il font-subsetting di weasyprint fallisce con certi glifi:
per questo write_pdf usa full_fonts=True (file un po' più grandi, zero errori).
"""
import datetime
import sys
import zipfile
from pathlib import Path

from weasyprint import HTML, CSS

ROOT = Path(__file__).parent
SRC = ROOT / "src"
OUT = ROOT / "output"

# Per lingua: (sorgente HTML in src/<lang>/, nome del PDF in output/<lang>/,
# titolo per l'indice). Stessi volumi, stesso ordine nelle due liste.
VOLUMES = {
    "it": [
        ("01-comandi-slash.html",                  "claude-code-1-comandi-slash-cheatsheet.pdf",
         "Cheatsheet comandi slash"),
        ("02-skills-subagents-hooks-plugins.html", "claude-code-2-skills-subagents-hooks-plugins.pdf",
         "Estendere Claude: skills, subagents, hooks & plugins"),
        ("03-contesto-memoria-costi.html",         "claude-code-3-contesto-memoria-costi.pdf",
         "Contesto, memoria e costi"),
        ("04-cli-headless-automazione.html",       "claude-code-4-cli-headless-automazione.pdf",
         "CLI, headless e automazione"),
        ("05-permessi-sandbox-sicurezza.html",     "claude-code-5-permessi-sandbox-sicurezza.pdf",
         "Permessi, sandbox e sicurezza"),
        ("06-parallelo-e-cloud.html",              "claude-code-6-parallelo-e-cloud.pdf",
         "Lavoro parallelo e cloud"),
        ("07-mcp.html",                            "claude-code-7-mcp.pdf",
         "MCP fatto bene"),
        ("08-claude-ai-app.html",                  "claude-ai-8-app-projects-artifacts.pdf",
         "Claude.ai: l'app oltre il codice"),
        ("09-skills-in-pratica.html",              "claude-code-9-skills-in-pratica.pdf",
         "Extra · Skills in pratica: tre esempi completi"),
        ("10-subagents-in-pratica.html",           "claude-code-10-subagents-in-pratica.pdf",
         "Extra · Subagents in pratica: tre esempi completi"),
        ("11-comandi-custom-in-pratica.html",      "claude-code-11-comandi-custom-in-pratica.pdf",
         "Extra · Comandi custom in pratica: tre esempi completi"),
        ("12-mcp-in-pratica.html",                 "claude-code-12-mcp-in-pratica.pdf",
         "Extra · MCP in pratica: tre integrazioni reali"),
    ],
    "en": [
        ("01-slash-commands.html",                 "claude-code-1-slash-commands-cheatsheet.pdf",
         "Slash commands cheatsheet"),
        ("02-skills-subagents-hooks-plugins.html", "claude-code-2-skills-subagents-hooks-plugins.pdf",
         "Extending Claude: skills, subagents, hooks & plugins"),
        ("03-context-memory-costs.html",           "claude-code-3-context-memory-costs.pdf",
         "Context, memory and costs"),
        ("04-cli-headless-automation.html",        "claude-code-4-cli-headless-automation.pdf",
         "CLI, headless and automation"),
        ("05-permissions-sandbox-security.html",   "claude-code-5-permissions-sandbox-security.pdf",
         "Permissions, sandbox and security"),
        ("06-parallel-and-cloud.html",             "claude-code-6-parallel-and-cloud.pdf",
         "Parallel work and cloud"),
        ("07-mcp.html",                            "claude-code-7-mcp.pdf",
         "MCP done right"),
        ("08-claude-ai-app.html",                  "claude-ai-8-app-projects-artifacts.pdf",
         "Claude.ai: the app beyond code"),
        ("09-skills-in-practice.html",             "claude-code-9-skills-in-practice.pdf",
         "Extra · Skills in practice: three complete examples"),
        ("10-subagents-in-practice.html",          "claude-code-10-subagents-in-practice.pdf",
         "Extra · Subagents in practice: three complete examples"),
        ("11-custom-commands-in-practice.html",    "claude-code-11-custom-commands-in-practice.pdf",
         "Extra · Custom commands in practice: three complete examples"),
        ("12-mcp-in-practice.html",                "claude-code-12-mcp-in-practice.pdf",
         "Extra · MCP in practice: three real integrations"),
    ],
}

LANG_LABELS = {"it": "Italiano", "en": "English"}
ZIP_NAMES = {"it": "claude-cheatsheets-it.zip", "en": "claude-cheatsheets-en.zip"}
REPO = "manzolo/claude-cheatsheets"

INDEX_TEMPLATE = """<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Claude Cheatsheets — PDF italiano / English</title>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: "DejaVu Sans", "Verdana", sans-serif; background: #faf5ee;
         color: #2b2620; line-height: 1.5; }}
  .hero {{ background: #1f1b16; color: #faf5ee; padding: 2.5rem 1.5rem; }}
  .hero .inner, main {{ max-width: 46rem; margin: 0 auto; }}
  .hero h1 {{ font-size: 1.8rem; }}
  .hero h1 span {{ color: #d97757; }}
  .hero p {{ color: #c9c2b8; margin-top: .5rem; font-size: .95rem; }}
  main {{ padding: 1.5rem; }}
  h2 {{ margin: 1.6rem 0 .4rem; font-size: 1.1rem; color: #1f1b16;
       border-bottom: 2px solid #d97757; padding-bottom: .2rem; }}
  h2:first-child {{ margin-top: 0; }}
  ol {{ list-style: none; counter-reset: vol; }}
  ol li {{ counter-increment: vol; margin: .6rem 0; }}
  ol li a {{ display: block; background: #fff; border: 1px solid #e4dcd0;
            border-left: 4px solid #d97757; border-radius: 6px;
            padding: .7rem 1rem .7rem 3.2rem; position: relative;
            color: #2b2620; text-decoration: none; font-weight: bold; }}
  ol li a:hover {{ border-color: #d97757; background: #fdf0e7; }}
  ol li a::before {{ content: counter(vol); position: absolute; left: .9rem;
            top: 50%; transform: translateY(-50%); color: #d97757;
            font-size: 1.3rem; }}
  ol li a small {{ display: block; font-weight: normal; color: #7a736a;
            font-size: .8rem; }}
  .zip {{ display: inline-block; margin-top: .8rem; background: #d97757;
         color: #fff; padding: .6rem 1.2rem; border-radius: 6px;
         text-decoration: none; font-weight: bold; }}
  .zip:hover {{ background: #c2603f; }}
  footer {{ margin-top: 2rem; padding-top: 1rem; border-top: 1px solid #e4dcd0;
           color: #9a938c; font-size: .8rem; }}
  footer a {{ color: #d97757; }}
</style>
</head>
<body>
<div class="hero"><div class="inner">
  <h1>Claude <span>/</span> Cheatsheets</h1>
  <p>Collana di {count} PDF su Claude Code e Claude.ai, in italiano e inglese,
     generati dalla documentazione ufficiale Anthropic.<br>
     {count} PDF cheatsheets on Claude Code and Claude.ai, in Italian and
     English, built from the official Anthropic docs.</p>
</div></div>
<main>
{sections}
  <footer>
    Aggiornato il / updated on {date} · Sorgenti e versioni / sources and releases:
    <a href="{repo_url}">github.com/{repo}</a> ·
    Licenza <a href="https://creativecommons.org/licenses/by-sa/4.0/deed.it">CC BY-SA 4.0</a>
    · Progetto non affiliato ad Anthropic / not affiliated with Anthropic.
  </footer>
</main>
</body>
</html>
"""

SECTION_TEMPLATE = """  <h2>{label}</h2>
  <ol>
{items}
  </ol>
  <a class="zip" href="{zip_name}">&#8681; {zip_label} ({zip_name})</a>
"""


# style.css scrive il footer di pagina in italiano ("pag. X di Y"): per i
# volumi inglesi che lo condividono va sovrascritta la sola stringa content.
EN_FOOTER_CSS = CSS(string=(
    '@page { @bottom-center { content: string(doctitle)'
    ' " — page " counter(page) " of " counter(pages); } }'
))


def build(volume_filter: str | None = None, langs: list[str] | None = None) -> list[Path]:
    produced = []
    shared_css = CSS(str(SRC / "style.css"))
    for lang in langs or list(VOLUMES):
        out_dir = OUT / lang
        out_dir.mkdir(parents=True, exist_ok=True)
        for src_name, pdf_name, _title in VOLUMES[lang]:
            if volume_filter and not src_name.startswith(volume_filter):
                continue
            src = SRC / lang / src_name
            # I volumi 01 e 02 sono autosufficienti (hanno <style> inline);
            # gli altri usano il foglio di stile condiviso src/style.css.
            if "<style" in src.read_text(encoding="utf-8"):
                stylesheets = []
            else:
                stylesheets = [shared_css] + ([EN_FOOTER_CSS] if lang == "en" else [])
            out = out_dir / pdf_name
            HTML(str(src)).write_pdf(str(out), stylesheets=stylesheets, full_fonts=True)
            print(f"ok  {out.relative_to(ROOT)}")
            produced.append(out)
    if not produced:
        sys.exit(f"Nessun volume corrisponde a '{volume_filter}'")
    return produced


def make_zips(langs: list[str] | None = None) -> None:
    for lang in langs or list(VOLUMES):
        zpath = OUT / ZIP_NAMES[lang]
        with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
            for _, pdf_name, _title in VOLUMES[lang]:
                z.write(OUT / lang / pdf_name, pdf_name)
        print(f"zip {zpath.relative_to(ROOT)}")


def make_index() -> None:
    sections = []
    for lang in VOLUMES:
        serie_label = {"it": "Claude.ai", "en": "Claude.ai"}
        items = []
        for _src, pdf_name, title in VOLUMES[lang]:
            serie = "Claude.ai" if pdf_name.startswith("claude-ai") else "Claude Code"
            items.append(
                f'    <li><a href="{lang}/{pdf_name}">{title}'
                f'<small>{serie} &middot; {pdf_name}</small></a></li>'
            )
        sections.append(SECTION_TEMPLATE.format(
            label=LANG_LABELS[lang],
            items="\n".join(items),
            zip_name=ZIP_NAMES[lang],
            zip_label="Scarica tutto" if lang == "it" else "Download all",
        ))
    html = INDEX_TEMPLATE.format(
        count=len(VOLUMES["it"]),
        sections="\n".join(sections),
        date=datetime.date.today().strftime("%d/%m/%Y"),
        repo=REPO,
        repo_url=f"https://github.com/{REPO}",
    )
    OUT.mkdir(exist_ok=True)
    ipath = OUT / "index.html"
    ipath.write_text(html, encoding="utf-8")
    print(f"idx {ipath.relative_to(ROOT)}")


if __name__ == "__main__":
    args = sys.argv[1:]
    want_zip = "--zip" in args
    want_index = "--index" in args
    langs = [a.split("=", 1)[1] for a in args if a.startswith("--lang=")] or None
    if langs and (bad := [l for l in langs if l not in VOLUMES]):
        sys.exit(f"Lingua sconosciuta: {bad[0]} (disponibili: {', '.join(VOLUMES)})")
    filters = [a for a in args if not a.startswith("--")]
    build(filters[0] if filters else None, langs)
    if want_zip:
        make_zips(langs)
    if want_index:
        make_index()
