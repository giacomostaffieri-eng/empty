# Sales Toolkit per checkout.com — come attivarlo

Questo kit trasforma Claude (già collegato al tuo stack) nel tuo co-pilota di prevendita/vendita.
**Non è un'app da sviluppare**: sono 3 comandi riutilizzabili che orchestrano i connettori che hai già.

## I 3 comandi

| Comando | Cosa fa | Dolore che risolve |
|---|---|---|
| `/precall-brief <dominio>` | Brief di 1 pagina: chi chiamare, 3 leve, script cold call. Fonde Salesforce+6sense, Lusha, Slack, Confluence. | Il ping-pong Glean↔Gemini in prep discovery. |
| `/account-prioritizer [filtro]` | Ordina i ~400 account per priorità di chiamata usando i segnali 6sense (via SF) + Lusha. | "Busso a tutti", non scalabile. Chiami solo al momento giusto. |
| `/tech-resolver <problema>` | Risposta tecnica ancorata SOLO ai doc checkout.com, zero "dipende", + mail pronta. | Fare tu il Data Scientist/Support sotto i 12.5k MMB. |

## Come si attiva (una tantum)

Questi comandi girano in una **sessione interattiva** di Claude Code (terminale/IDE) o via claude.ai,
dove i connettori sono autorizzati. In una sessione non-interattiva i prompt di permesso non si possono approvare.

1. **Autorizza i connettori** (impostazioni connettori claude.ai oppure `/mcp` in sessione interattiva):
   - ✅ **Salesforce** — account, opportunità, e **campi 6sense sincronizzati** (Buying Stage, Intent, Profile Fit…)
   - ✅ **Lusha** — decision maker, segnali, enrichment (sostituto operativo di 6sense per il prospecting)
   - ✅ **Atlassian/Confluence** — knowledge base checkout.com (fonte accurata, citata)
   - ✅ **Slack** — contesto interno account
   - ✅ **Google Calendar** — task e follow-up
   - ⚠️ **Gmail** — richiede autorizzazione a parte; finché non è autorizzato, Claude **scrive** le bozze ma non le invia.
2. Apri Claude Code in questa cartella e digita, es.: `/precall-brief acme.com`

## 6sense: cosa si può e cosa no

- ✅ **Leggibile**: tutto ciò che 6sense **sincronizza in Salesforce** (campi custom su Account/Lead).
  Il comando scopre i nomi reali dei campi al primo run (`getObjectSchema`).
- ❌ **Non leggibile**: ciò che vive **solo** nella dashboard 6sense (es. visitatori anonimi del sito),
  a meno che non venga esportato o 6sense non venga collegato direttamente.

## Limiti onesti (leggi prima di fidarti dei numeri)

- **Looker NON è collegato** → i calcoli tipo "stai perdendo $800k di false declines" e i benchmark di
  acceptance rate su dati reali **non sono alimentabili** oggi. Senza dati veri sarebbero inventati: i comandi
  li marcano come `STIMA` o `⚠️ da verificare`. Per renderli reali: collega Looker o esporta un CSV dei clienti.
- **MMB viability** nel prioritizer è **euristica** (mix cross-border/APM), non basata sulle performance reali.
- **Fingerprint del checkout** (che PSP usano, APM mancanti) è **inferenza dal sito**, non certezza.

## Prossimi passi possibili
- Collegare **Looker** (o import CSV) per attivare il vero "money-lost calculator" del pitch.
- Salvare gli output ricorrenti come **canvas Slack** o file **Drive** condivisi col team.
- Automatizzare la coda giornaliera con un task ricorrente (`/account-prioritizer` ogni mattina).
