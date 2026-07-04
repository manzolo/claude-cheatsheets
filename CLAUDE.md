# Claude Cheatsheets — collana di cheatsheet PDF

Collana di 8 PDF su Claude Code e Claude.ai, in italiano e inglese, generati
da sorgenti HTML+CSS con WeasyPrint. Questo repo serve a correggerli,
aggiornarli ed estenderli nel tempo. Pubblicato su
github.com/manzolo/claude-cheatsheets (Pages + Releases).
NOTA NOME: "Bignami" è un marchio registrato — non usarlo nel branding
pubblico (repo, README, zip, indice); al massimo "in stile bignami" minuscolo.

## Struttura

- `src/it/01-*.html` … `08-*.html` — sorgenti italiani, uno per volume
- `src/en/01-*.html` … `08-*.html` — sorgenti inglesi, stessi volumi
  (nomi file tradotti; la corrispondenza vive in VOLUMES in `build.py`)
- `src/style.css` — foglio di stile condiviso da entrambe le lingue (volumi
  03-08); i volumi 01 e 02 hanno il loro `<style>` inline e NON usano
  style.css
- `build.py` — rigenera PDF, zip e indice in `output/{it,en}/`
- `output/` — artefatti generati, in .gitignore; non modificare a mano
- `.github/workflows/build.yml` — CI: build+artifacts su ogni push/PR,
  deploy su GitHub Pages da main, Release con gli zip sui tag `v*`

## Comandi

- Rigenerare tutto (entrambe le lingue): `python3 build.py`
- Un solo volume: `python3 build.py 05` (aggiunge `--lang=en` o `--lang=it`
  per una lingua sola)
- Tutto + zip per lingua: `python3 build.py --zip`
- Indice per Pages: `python3 build.py --index` (genera `output/index.html`
  dalla lista VOLUMES; i titoli dei volumi vivono lì)
- Nuova versione pubblica: `git tag v2026.MM && git push origin v2026.MM`
- Dipendenze: `pip install weasyprint pdf2image --break-system-packages`
  (pdf2image serve solo per la verifica visiva; richiede poppler-utils)

## Workflow per qualsiasi modifica

1. Modifica SOLO i sorgenti in `src/`, mai i PDF. Ogni modifica di contenuto
   va applicata a ENTRAMBE le lingue (`src/it/` e `src/en/`), mantenendo i
   due sorgenti allineati riga per riga come struttura.
2. Rigenera il volume toccato con `python3 build.py NN`.
3. VERIFICA VISIVA OBBLIGATORIA: renderizza le pagine e guardale prima di
   dichiarare finito. Esempio:
   `python3 -c "from pdf2image import convert_from_path; [im.save(f'/tmp/p{i}.png') for i,im in enumerate(convert_from_path('output/<file>.pdf', dpi=60))]"`
   poi apri/leggi le immagini. Controlla: testo tagliato, tabelle che
   sbordano, pagine semivuote, grassetto invisibile su sfondi scuri.
4. Se il numero di pagine cambia molto rispetto a prima, indaga il perché.

## Convenzioni di contenuto

- Lingua: italiano; i termini tecnici (skill, hook, worktree, prompt caching)
  restano in inglese; i nomi di comandi/flag/file sempre in `code`.
- Le affermazioni sulle funzionalità devono venire dalla documentazione
  ufficiale: code.claude.com/docs (indice completo in
  https://code.claude.com/docs/llms.txt) per Claude Code,
  support.claude.com per Claude.ai. In caso di dubbio VERIFICA con una fetch
  della pagina prima di scrivere: le feature cambiano di settimana in
  settimana e la memoria del modello invecchia male su questo dominio.
- Ogni volume chiude con un `.footer-note` che cita le pagine-fonte.
- Densità: pagine piene ma leggibili; meglio tagliare che sbordare. Ogni
  affermazione in una riga, niente paragrafi-fiume nelle tabelle.

## Convenzioni grafiche (WeasyPrint)

- SEMPRE `full_fonts=True` in write_pdf: il font-subsetting di fontTools
  fallisce con certi glifi (errore "expected 0 <= int <= 122").
- NIENTE emoji astrali (U+1F300+): il font DejaVu non le ha e spariscono in
  silenzio. Usa simboli BMP: &#9670; &#9654; &#10003; &#9998; &#8635; &#8644;
  &#8649; &#9733; &#10022; &#9874; &#10010; &#9881; &#9889;
- Grassetto dentro box scuri (`.flowbox`): il colore va forzato
  (`.flowbox td b { color: #f0b393 !important; }` è già in style.css) —
  altrimenti esce scuro-su-scuro e sparisce.
- Palette: sfondo scuro #1f1b16, accento #d97757, carta #faf5ee, capitoli
  colorati con le classi .ch-a … .ch-g. Mantienila per coerenza di collana.
- Il footer di pagina prende il titolo dal primo elemento
  `<span class="doctitle">` del body (string-set): ogni nuovo volume deve
  averlo.
- Evita `page-break-before: always`: lascia fluire e usa `.avoid-break` /
  `page-break-inside: avoid` sui box; i salti forzati creano pagine mezze
  vuote.

## Aggiungere un nuovo volume

1. Copia un sorgente esistente (03-08) come scheletro, aggiorna
   `.doctitle`, hero e capitoli.
2. Aggiungi la tripla (sorgente, pdf, titolo) alla lista VOLUMES in
   `build.py` e la riga corrispondente alla tabella volumi del README.
3. Documentati SOLO da fonti ufficiali (fetch delle pagine .md di
   code.claude.com/docs) e cita le fonti nel footer.
4. Builda, verifica visivamente, aggiorna lo zip con `--zip`.
