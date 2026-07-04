# Claude Cheatsheets

[![build](https://github.com/manzolo/claude-cheatsheets/actions/workflows/build.yml/badge.svg)](https://github.com/manzolo/claude-cheatsheets/actions/workflows/build.yml)
[![Licenza: CC BY-SA 4.0](https://img.shields.io/badge/licenza-CC%20BY--SA%204.0-d97757)](https://creativecommons.org/licenses/by-sa/4.0/deed.it)

Collana di 8 cheatsheet PDF su **Claude Code** e **Claude.ai**, in **italiano
e inglese**: pagine dense in stile bignami da tenere accanto alla tastiera,
generate da sorgenti HTML+CSS con [WeasyPrint](https://weasyprint.org/) e
verificate sulla documentazione ufficiale Anthropic.

*A series of 8 PDF cheatsheets on Claude Code and Claude.ai, in Italian and
English, built from HTML+CSS sources with WeasyPrint and checked against the
official Anthropic docs.*

## 📥 Scaricare i PDF / Download

- **Ultima versione / latest**: <https://manzolo.github.io/claude-cheatsheets/>
  (rigenerata automaticamente a ogni push / rebuilt on every push)
- **Versioni datate / snapshots**: [Releases](https://github.com/manzolo/claude-cheatsheets/releases)
  — zip completi per lingua, utili perché le funzionalità di Claude cambiano
  spesso

## 📚 I volumi / The volumes

| # | Italiano | English |
|---|----------|---------|
| 1 | Cheatsheet comandi slash | Slash commands cheatsheet |
| 2 | Estendere Claude: skills, subagents, hooks & plugins | Extending Claude: skills, subagents, hooks & plugins |
| 3 | Contesto, memoria e costi | Context, memory and costs |
| 4 | CLI, headless e automazione | CLI, headless and automation |
| 5 | Permessi, sandbox e sicurezza | Permissions, sandbox and security |
| 6 | Lavoro parallelo e cloud | Parallel work and cloud |
| 7 | MCP fatto bene | MCP done right |
| 8 | Claude.ai: l'app oltre il codice | Claude.ai: the app beyond code |

## 🔨 Buildare in locale / Local build

```bash
pip install weasyprint pdf2image --break-system-packages
# pdf2image serve solo per la verifica visiva; richiede poppler-utils

python3 build.py                # tutti i volumi, entrambe le lingue → output/{it,en}/
python3 build.py 05             # solo il volume 05
python3 build.py 05 --lang=en   # solo il volume 05 inglese
python3 build.py --zip          # tutto + zip per lingua
python3 build.py --index        # genera anche output/index.html (GitHub Pages)
```

## 🗂 Struttura del repo / Repo layout

```
src/it/01-*.html … 08-*.html    sorgenti italiani, uno per volume
src/en/01-*.html … 08-*.html    sorgenti inglesi, stessi volumi
src/style.css                   stile condiviso (volumi 03-08; 01-02 hanno CSS inline)
build.py                        genera PDF, zip e indice in output/
.github/workflows/build.yml     CI: build → artifacts, Pages (main), Release (tag v*)
CLAUDE.md                       convenzioni operative per lavorarci con Claude Code
```

I PDF in `output/` sono artefatti generati: **si modificano solo i sorgenti in
`src/`**, mai i PDF, e ogni modifica di contenuto va applicata a entrambe le
lingue. Ogni affermazione sulle funzionalità viene dalla documentazione
ufficiale ([code.claude.com/docs](https://code.claude.com/docs) per Claude
Code, [support.claude.com](https://support.claude.com) per Claude.ai), citata
nel footer di ogni volume.

## 🏷 Pubblicare una nuova versione / Cut a release

```bash
git tag v2026.07 && git push origin v2026.07
```

La Action crea la Release e vi allega gli zip per lingua. /
*The Action creates the Release with the per-language zips attached.*

## Licenza / License

Contenuti rilasciati sotto [CC BY-SA 4.0](LICENSE). Progetto indipendente,
**non affiliato ad Anthropic**; "Claude" è un marchio di Anthropic PBC. /
*Independent project, not affiliated with Anthropic; "Claude" is a trademark
of Anthropic PBC.*
