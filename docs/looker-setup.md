# Looker — come arrivare a "qual è l'acceptance rate payins per MCC 2123 in Bulgaria?" → un numero

## La verità
**Non esiste un connettore Looker attivo** in questa configurazione. Quindi oggi non posso interrogare Looker
in linguaggio naturale. Ma è fattibile: il blocco non è Claude, è (a) l'accesso e (b) sapere in quale
"Explore" di Looker vivono quei dati. Due strade, dalla più semplice.

---

## Path B — Fallback che funziona SUBITO (zero setup tecnico) ✅
Se sai già arrivare a un report che contiene acceptance rate per MCC/paese (anche imperfetto):
1. In Looker, apri quel Look/dashboard → **Download → CSV** (con le colonne: MCC, Country, Payin acceptance rate, periodo).
2. Metti il CSV in **Google Drive** (già collegato).
3. Chiedimi: *"qual è l'acceptance rate payins per MCC 2123 in Bulgaria?"* → leggo il CSV e ti do il numero,
   e te lo trasformo in frase da pitch.

Limite: è una foto statica (aggiorni ri-esportando). Ma ti toglie subito dal "non capisco come navigare Looker".

---

## Path A — La versione "magica" NL→numero live (richiede setup una tantum)
Per interrogare Looker dal vivo servono 3 cose, che chiedi al **team Data/Analytics o all'admin Looker**:

1. **Credenziali API** (Looker API3): `base_url` dell'istanza + `client_id` + `client_secret`.
   → vanno messe come variabili d'ambiente / secret, MAI nel repo.
2. **La mappa semantica** (la parte che ti manca oggi): per l'acceptance rate payins, chiedi loro:
   - Nome del **model** e dell'**Explore** che contiene questi dati.
   - I nomi esatti dei campi per: `acceptance rate payin`, `MCC`, `country`, `date/period`, `transaction type`.
   - Un esempio di query che restituisce il numero che ti serve (così lo replico).
3. **Abilitazione MCP/tool**: aggiungere un **Looker MCP server** ai connettori (Google ne offre uno ufficiale),
   oppure farmi costruire un piccolo tool Python con `looker_sdk` (`run_inline_query`) alimentato dalle credenziali sopra.

Una volta che ho questi 3 elementi, costruisco il comando `/looker` in cui scrivi la domanda in italiano e io:
tradurre → query Looker → numero reale → frase di pitch pronta. Esempio di output:
> *"MCC 2123 in Bulgaria: acceptance payin 82% vs media checkout.com 91% → ~9 punti di transato recuperabili."*

## Messaggio pronto per il team Data
> Ciao, sto costruendo un assistente per pitchare con dati reali di acceptance. Mi servono: (1) credenziali
> API3 di Looker (client_id/secret + base_url), (2) model + Explore dove sta l'acceptance rate payin, e i nomi
> dei campi per acceptance rate, MCC, country, periodo, transaction type, (3) un esempio di query che dà quel
> numero. Le credenziali le gestiamo come secret, non finiscono in nessun repo.
