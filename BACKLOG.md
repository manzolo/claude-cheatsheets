# Backlog

Lavori futuri e manutenzione della collana. Spuntare e committare man mano;
le convenzioni operative stanno in CLAUDE.md.

## Manutenzione ricorrente

- [ ] **Revisione mensile dei contenuti** contro la documentazione ufficiale
      (code.claude.com/docs, indice in `/docs/llms.txt`): le feature cambiano
      di settimana in settimana. Aggiornare la riga "Aggiornato: mese anno"
      nei volumi toccati e taggare una release `v2026.MM`.
- [ ] Controllare periodicamente le versioni delle GitHub Actions nel
      workflow (major native sul Node corrente, niente workaround).
- [ ] Ricontrollare i volumi extra 9-12 quando cambia la sintassi di
      frontmatter di skills/subagents o i comandi `claude mcp`.

## Idee per nuovi volumi

- [ ] Extra · Hooks in pratica: esempi reali completi (lint automatico su
      PostToolUse, guardrail PreToolUse, notifiche) — fonte: docs/hooks.
- [ ] Extra · Plugin in pratica: creare e distribuire un plugin che
      impacchetta skill + subagent + server MCP — fonte: docs/plugins.
- [ ] Volume su agent teams / background agents quando escono dallo stato
      sperimentale.

## Migliorie sito e distribuzione

- [ ] Favicon e meta Open Graph nella pagina indice di Pages.
- [ ] Link dinamico all'ultima release nell'indice.
- [ ] Valutare una variante stampabile in A5 o fronte-retro.
