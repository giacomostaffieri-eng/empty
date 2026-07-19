# Cosa chiedere ad Account Manager / Solutions Engineer per alimentare il Tech Resolver

Il Tech Resolver è forte solo quanto la conoscenza che gli dai. Confluence ha la teoria, ma il "no-dipende"
azionabile vive nella testa di chi gestisce i merchant ogni giorno. Manda a 2–3 AM/SE questo questionario
(bastano risposte brevi). Ogni risposta diventa una voce nella knowledge base (`docs/knowledge-base/`).

## Il questionario (copia-incolla)

> Sto costruendo un assistente che mi aiuta a risolvere/pitchare problemi di pagamento senza rimbalzare tra
> Glean e voi. Mi dai una mano con qualche risposta secca?

**1. Top problemi ricorrenti**
- Quali sono i **10 problemi/domande** che ti arrivano più spesso dai merchant?
- Per ognuno: causa reale in 1 frase + **la fix concreta** (dove clicca il merchant, quale flag, quale endpoint).

**2. Codici errore / decline**
- I **decline code / error code** che vedi più spesso: cosa significano DAVVERO (non la definizione da doc) e cosa si fa.
- Ci sono codici la cui doc ufficiale è fuorviante o incompleta? Quali e perché.

**3. Gotcha per mercato**
- Per i mercati chiave (FR, DE, IT, UK, NL, BR…): quali sono le trappole specifiche?
  (es. PSD2/SCA exemption in FR, mandati locali, schemi di carte particolari, APM must-have).

**4. Navigazione Dashboard**
- Per le 5 fix più comuni: la **sequenza di click** esatta nel Dashboard checkout.com (o la chiamata API).

**5. Underwriting / go-live**
- Quali sono le cause più frequenti per cui un deal **non va live** dopo l'approvazione del prevet (MAF)?
- Per MCC/settori rischiosi: cosa fa cadere il MAF? Come lo si anticipa?

**6. Acceptance rate / performance** (il ponte verso il pitch)
- Quando un merchant ha un calo di acceptance, quali sono le **3 cause più frequenti** in ordine?
  (es. 3DS/SCA mal configurato, no local acquiring, routing subottimale, carte estere).
- Quali leve di checkout.com recuperano di più? (retry logic, network tokens, local acquiring, exemptions).

**7. Dove NON fidarsi**
- Su quali temi devo SEMPRE coinvolgere un SE invece di rispondere da solo?

## Come si trasforma in knowledge base

Ogni risposta va in `docs/knowledge-base/` come file markdown, es:
- `decline-codes.md`, `market-france.md`, `underwriting-gotchas.md`, `acceptance-playbook.md`.

Formato di ogni voce (così il resolver la cita con precisione):

```
## <Problema / codice / tema>
**Causa reale:** ...
**Fix azionabile:** 1) ... 2) ...
**Dashboard/API:** <percorso esatto>
**Mercato:** <se specifico>
**Fonte:** <nome AM/SE + data> oppure <link Confluence>
**Confidenza:** ALTA / MEDIA / coinvolgi SE
```

Il Tech Resolver legge PRIMA questa cartella (conoscenza pratica verificata), POI Confluence, e non usa altro.
Man mano che raccogli risposte, la copertura cresce e i "dipende" spariscono.
