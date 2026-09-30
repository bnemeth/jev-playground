# Jev

## Mire jó, és mire nem?

 A Jev a TypeSafe első 'System One' modellje. Nem szöveget generál, hanem gyors, strukturált döntéseket ad: osztályoz, pontoz vagy eldönti, hogy egy állítás igaz-e. 

 A 'System One' egy modellkategória, kb kitaláltak egy model kategóriát pontosan a Jev hez. Egy olyan model család ami gyors struktúrált döntéseket hoz.

 A Jev nem egy reasoning, vagy hatalmas korpuszon tanított rendszer. Elsősorban olyan jól definiált kérdésekre ad választ, amelyekhez a rendelkezésre álló kontextus alapján gyors döntés szükséges. A modell legjobb teljesítménye a szűk, egyértelmű, önálló kérdések körében várható.

 Ha a kérdés túl összetett vagy több, egymástól független tényezőt tartalmaz, akkor érdemes azt kisebb, önálló kérdésekre bontani, és a végeredményt a kódban kombinálni.

## A Jev három kérdéstípusa

- **Noul:** egy állítás igazságát vizsgálja, 0 és 1 közötti valószínűséggel.
- **Choice:** választ az előre megadott lehetőségek közül.
- **Score:** egy leírt, rendezett skálán értékel.

Mindhárom kérdéstípus valószínűséget ad vissza: Noul egy 0–1 értéket, Choice és Score pedig egy teljes eloszlást. A 'confidence' ezekből számolt összegző érték, nem különálló modellkimenet.