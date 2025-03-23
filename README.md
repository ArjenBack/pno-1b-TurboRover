# Probleemoplossen en ontwerpen - deel 1b
Groepswerk voor probleemoplossen en ontwerpen, deel 1b in bachelor 1, semester 2 aan KULeuven 2024-2025.

In samenwerking met: Ward Geens, Pieter-Jan Bossuyt, Casper Caers, Zidane Castermans, Daan Coletti, Elias Dezittere en Mauro Berden.

## Inhoud
Deze repository bevat zowel het besturingsalgoritme van de wagen, circuitpython code voor de microcontroller (pico).
Ook bevat het de code voor de browserapplicatie.

## Structuur
```bash
.
├── besturingsalgoritme             # Python code op de pico voor besturing van de wagen
│   └── besturingsalgoritme.py
├── browserapplicatie               # Code en markupbestanden van de browserapplicatie
│   ├── browserapplicatie.css
│   ├── browserapplicatie.html
│   └── browserapplicatie.js
├── extra-code                      # extra code voor experimenten en testen
│   ├── analyse_LDR.py
│   └── motor-test.py
├── LICENSE
└── README.md
```

## Experimenten
 - Bepalen van LDR-waarden bij lijn verschil: `./extra-code/analyse_LDR.py`

## Testen
 - Motor test: `./extra-code/motor-test.py`
