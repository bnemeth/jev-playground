# Jev

## Mire jó, és mire nem?

A TypeSafe abból indul ki, hogy az AI-t a jövőben nagyrészt nem ember fogja használni, hanem más AI-rendszerek és kód. Ezért nem olvasásra szánt szöveget ad vissza, hanem olyan kimenetet, amit egy alkalmazás közvetlenül feldolgozhat.

A Jev a TypeSafe első 'System One' modellje gyors, strukturált döntéseket ad: osztályoz, pontoz vagy eldönti, hogy egy állítás igaz-e. 

A Jev nem egy reasoning modell, nem LLM, a Jev döntési modell, ami érti a nyelvet és van általános tudása. 

Elsősorban olyan jól definiált kérdésekre ad választ, amelyekhez a rendelkezésre álló kontextus alapján gyors döntés szükséges. A modell legjobb teljesítménye a szűk, egyértelmű, önálló kérdések körében várható.

Nem ügyes bonyolult kérdésekben. Ha a kérdés túl összetett vagy több, egymástól független tényezőt tartalmaz, akkor érdemes azt kisebb, önálló kérdésekre bontani, és a végeredményt a kódban kombinálni.

## System Micsoda?

A 'System One' egy modellkategória. kb kitaláltak egyet pontosan a Jev-hez. Olyan modell, ami "nem szöveget generál, hanem gyors, strukturált döntéseket ad".

Honnan származik: Daniel Kahneman Nobel-díjas pszichológus *Gyors és lassú gondolkodás* című könyvéből. Ő kétféle gondolkodást különít el:

| | Jellemző | Példa |
|---|---|---|
| **System 1** | gyors, automatikus, intuitív | ránézel egy arcra és tudod, hogy dühös; 2+2=4 |
| **System 2** | lassú, tudatos, megerőltető | 17×24 fejben; egy szerződés átolvasása |

## State 

A state az a tartalom, amit a Jev kiértékel: egy tetszőleges JSON (string, objektum vagy tömb). 

**Csak szöveg**, kép, hang vagy videó nem. A Jev-et elsősorban angolra tanították, más nyelven is működik, de gyengébb pontossággal.

A kérdés **nem** ide kerül, ezek csak a tények.

```json
{
  "message": "I was charged twice for order A-104. Please refund the duplicate.",
  "order": { "id": "A-104", "charges": [49, 49] },
  "refund_policy": "Duplicate charges are eligible for a refund."
}
```


## A Jev három kérdéstípusa

- **Noul:** egy állítás igazságát vizsgálja, 0 és 1 közötti valószínűséggel.
- **Choice:** választ az előre megadott lehetőségek közül.
- **Score:** egy leírt, rendezett skálán értékel.

Mindhárom kérdéstípus valószínűséget ad vissza: Noul egy 0–1 értéket, Choice és Score pedig egy teljes eloszlást.

Egy stage-hez több, egymástól függetlenül kiértékelhető kérdést is megadhatunk.

## Noul

Igen/nem kérdés. A neve a Bernoulli-eloszlásból jön: két lehetőség (igen/nem), egyetlen paraméter.

- **Bemenet:** `instructions` (a kérdés vagy egy megítélendő állítás), opcionálisan `criteria` a `true` és `false` jelentésével.
- **Kimenet:** egyetlen szám, `noul`: annak a valószínűsége, hogy a válasz igen. Külön `confidence` nincs, mert a szám maga a bizonytalanság is: 0 vagy 1 közelében biztos, 0.5 körül bizonytalan.
- **Egy Noul = egy kérdés.** Az „és”-sel összekötött feltételeket érdemes két Noulra bontani. A kérdést úgy fogalmazd, hogy a magas érték jelentse az igent.

Notebook: [000_walkthrough_lesson_noul.ipynb](notebooks/000_walkthrough_lesson_noul.ipynb)

## Choice

Egy opció kiválasztása egy előre megadott halmazból.

- **Bemenet:** `instructions` (a kérdés) és `criteria`: opciónév → leírás. A leírás lehet string, objektum vagy üres. A modell az opció nevét és leírását is látja.
- **Kimenet:**
  - `choice`: a legnagyobb valószínűségű opció,
  - `probabilities`: eloszlás az összes opcióra (összege 1),
  - [`confidence`](https://docs.typesafe.ai/confidence): a `probabilities`-ből számolt összegző érték, nem különálló modellkimenet. Egy csúcs esetén magas, szétterülő eloszlásnál alacsony.
- **Legfeljebb 255 opció.** Ha a lista nem fed le minden esetet, érdemes egy `other` / `none` opciót is megadni, különben a modell kénytelen a meglévők közül választani.
- **Az opciók sorrendje számíthat**: a `jev-1.13` hajlamos az elsőként megadott felé húzni.

Notebook: [001_walkthrough_lesson_choice.ipynb](notebooks/001_walkthrough_lesson_choice.ipynb)

## Score

Értékelés egy rendezett, szavakban leírt skálán.

- **Bemenet:** `instructions` (mit értékelünk) és `criteria`: a szintek leírásainak rendezett listája, alulról felfelé, 2–10 szint. A szint száma a listabeli indexe, 0-tól.
- **Kimenet:**
  - `score`: a szintszámok valószínűséggel súlyozott átlaga (Σ szint × p). Ezért lehet tört, például 3.45.
  - `probabilities`: eloszlás a szintekre (összege 1),
  - `legend`: szintszám → leírás,
  - [`confidence`](https://docs.typesafe.ai/confidence): a `probabilities`-ből számolt összegző érték.
- **A `score` önmagában nem elég.** Ugyanaz az érték különböző eloszlásból is kijöhet: az 1.0 jelentheti, hogy minden az 1-es szinten van, de azt is, hogy fele-fele a 0-n és a 2-n. Ezért a `probabilities`-t is érdemes megnézni.
- **Egy Score = egy dimenzió.** A „pontos, okos és tapasztalt” három külön kérdés.

Notebook: [002_walkthrough_lesson_can_monkey.ipynb](notebooks/002_walkthrough_lesson_can_monkey.ipynb)

## Mezőhivatkozás a kérdésben

A kérdés (`instructions`) backtickek között, névvel hivatkozhat a state mezőire, beágyazott mezőnél pont-és-index útvonallal (pl. `order.charges[0]`):

```python
"questions": {
    "refund_requested": {
        "type": "noul",
        "instructions": "Does `message` request a refund?",
    },
    "policy_supports_refund": {
        "type": "noul",
        "instructions": "Does `refund_policy` support the refund requested in `message`, given `order.charges`?",
    },
}
```

Ez nem sablonbehelyettesítés: az API nem írja be az értéket a kérdésbe, a modell maga keresi meg a hivatkozott mezőt. Ezért érdemes beszédes mezőneveket adni, a modell a neveket is látja.

### Ami a kódból jön, az külön mezőbe kerül

Nem így, string-template-tel:

```python
food = "Ice cream sandwich"
payload = {
    "state": {},
    "questions": {
        "is_sandwich": {"type": "noul", "instructions": f"Is {food} a sandwich?"},
    },
}
```

Hanem így, az érték a state-be, a kérdés hivatkozik rá:

```python
payload = {
    "state": {"food": food},
    "questions": {
        "is_sandwich": {"type": "noul", "instructions": "Is `food` a sandwich?"},
    },
}
```

A kérdés így fix, csak az adat változik. Ugyanaz a kérdés több mezőre is feltehető:

```python
"state": {
    "scenario": "Naruto is a Celebes crested macaque ... David Slater ... leaves his camera unattended ...",
    "subject": "Naruto",
    "human": "Slater",
    "creative_work": "the grinning self-portrait",
},
"questions": {
    "take_action_subj": {
        "type": "noul",
        "instructions": "Did `subject` carry out the action that resulted in `creative_work`?",
    },
    "take_action_human": {
        "type": "noul",
        "instructions": "Did `human` carry out the action that resulted in `creative_work`?",
    },
}
```

## Typesafe API

Notebook: [004_typesafe_sdk.ipynb](notebooks/004_typesafe_sdk.ipynb)

## Langchain API

Notebook: [005_langchain_integration.ipynb](notebooks/005_langchain_integration.ipynb)

## API key!

Minimum 5 USD feltöltés, egy évig érvényes. Ha szeretnél egyet, csak írj!
