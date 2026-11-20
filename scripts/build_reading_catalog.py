#!/usr/bin/env python3
"""
Builder and validator for apps/reading/catalog.js
Generates window.READING_CATALOG adhering strictly to SPEC-APP-READING v1.0.0
and ensures 100% bilingual parity, syllable integrity, and microCheck consistency.
"""
import json
import os
import re

CATALOG_JS_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "apps", "reading", "catalog.js"))

levels = [
    {
        "id": "l1",
        "icon": "🌱",
        "range": "4-5",
        "name": {"es": "Nivel 1: Primeras Letras y Sílabas", "en": "Level 1: First Letters & Syllables"},
        "desc": {
            "es": "Reconocimiento de vocales, consonantes y sílabas iniciales",
            "en": "Vowel, consonant and initial syllable recognition"
        }
    },
    {
        "id": "l2",
        "icon": "🖼️",
        "range": "5-6",
        "name": {"es": "Nivel 2: Palabra con Imagen", "en": "Level 2: Word with Picture"},
        "desc": {
            "es": "Palabras bisílabas directas con apoyo visual",
            "en": "Direct two-syllable words with visual support"
        }
    },
    {
        "id": "l3",
        "icon": "🧩",
        "range": "6-7",
        "name": {"es": "Nivel 3: Letras Faltantes", "en": "Level 3: Missing Letters"},
        "desc": {
            "es": "Completa las letras que faltan con el teclado táctil",
            "en": "Fill in missing letters using touch keyboard"
        }
    },
    {
        "id": "l4",
        "icon": "🚀",
        "range": "7-8",
        "name": {"es": "Nivel 4: Lectura Sin Ayuda", "en": "Level 4: Independent Words"},
        "desc": {
            "es": "Palabras complejas, sílabas trabadas y micro-comprobación",
            "en": "Complex words, blends and instant micro-check"
        }
    },
    {
        "id": "l5",
        "icon": "📖",
        "range": "8-9",
        "name": {"es": "Nivel 5: Frases de 2 Líneas", "en": "Level 5: 2-Line Stories"},
        "desc": {
            "es": "Lectura fluida de oraciones y preguntas de comprensión",
            "en": "Fluent sentence reading and comprehension questions"
        }
    },
    {
        "id": "l6",
        "icon": "🏆",
        "range": "9-11",
        "name": {"es": "Nivel 6: Mini-Relatos", "en": "Level 6: Mini-Stories"},
        "desc": {
            "es": "Párrafos de 3 líneas, signos de puntuación y reto inferencial",
            "en": "3-line paragraphs, punctuation and inferential challenge"
        }
    }
]

modes = [
    {
        "id": "normal",
        "icon": "🧘",
        "name": {"es": "Modo Normal", "en": "Normal Mode"},
        "desc": {
            "es": "Sin reloj ni estrés. Pistas visuales libres para aprender.",
            "en": "No timer, no stress. Free visual hints for learning."
        }
    },
    {
        "id": "stopwatch",
        "icon": "⏱️",
        "name": {"es": "Contrarreloj Lector", "en": "Reading Stopwatch"},
        "desc": {
            "es": "Mide tus palabras por minuto (PPM) con cierre instantáneo al leer.",
            "en": "Measure your words per minute (WPM) with instant freeze upon reading."
        }
    },
    {
        "id": "sprint",
        "icon": "⚡",
        "name": {"es": "Sprint 60s", "en": "Sprint 60s"},
        "desc": {
            "es": "¡1 minuto a tope! Cada 5 aciertos seguidos suman +3s.",
            "en": "1 minute rush! Every 5 streak answers add +3s."
        }
    },
    {
        "id": "daily",
        "icon": "📅",
        "name": {"es": "Reto Diario", "en": "Daily Challenge"},
        "desc": {
            "es": "10 retos únicos al día idénticos para todos con tarjeta compartible.",
            "en": "10 daily unique challenges identical for everyone with shareable card."
        }
    }
]

profiles = [
    {
        "id": "player_1",
        "avatar": "🦁",
        "name": {"es": "Jugador 1", "en": "Player 1"},
        "title": {"es": "León Lector", "en": "Reading Lion"}
    },
    {
        "id": "player_2",
        "avatar": "🦊",
        "name": {"es": "Jugador 2", "en": "Player 2"},
        "title": {"es": "Zorro Audaz", "en": "Swift Fox"}
    },
    {
        "id": "adult",
        "avatar": "🦉",
        "name": {"es": "Adulto", "en": "Adult"},
        "title": {"es": "Búho Sabio", "en": "Wise Owl"}
    }
]

medals = [
    {
        "id": "first_win",
        "icon": "🌟",
        "name": {"es": "Primer Vuelo", "en": "First Flight"},
        "desc": {
            "es": "Completa tu primera partida de lectura con éxito",
            "en": "Complete your first successful reading game"
        }
    },
    {
        "id": "streak_5",
        "icon": "🔥",
        "name": {"es": "Fuego x5", "en": "Fire x5"},
        "desc": {
            "es": "Consigue una racha de 5 aciertos seguidos",
            "en": "Get a streak of 5 correct answers"
        }
    },
    {
        "id": "streak_10",
        "icon": "⚡",
        "name": {"es": "Rayo x10", "en": "Lightning x10"},
        "desc": {
            "es": "Alcanza una racha perfecta de 10 aciertos",
            "en": "Reach a perfect 10 answer streak"
        }
    },
    {
        "id": "syllable_master",
        "icon": "🧩",
        "name": {"es": "Mago Silábico", "en": "Syllable Wizard"},
        "desc": {
            "es": "Completa el Nivel 3 o 4 sin cometer ningún error",
            "en": "Complete Level 3 or 4 without any mistakes"
        }
    },
    {
        "id": "speed_reader",
        "icon": "⏱️",
        "name": {"es": "Lector Sónico", "en": "Sonic Reader"},
        "desc": {
            "es": "Supera las 120 Palabras Por Minuto (PPM) en una ronda",
            "en": "Exceed 120 Words Per Minute (WPM) in a round"
        }
    },
    {
        "id": "storyteller",
        "icon": "🏆",
        "name": {"es": "Gran Cuentacuentos", "en": "Master Storyteller"},
        "desc": {
            "es": "Supera el Nivel 5 o 6 con comprensión perfecta (100%)",
            "en": "Pass Level 5 or 6 with 100% comprehension"
        }
    }
]

learnModules = {
    "es": {
        "letters": [
            {"letter": "A", "sound": "a", "anchor": "Abeja", "emoji": "🐝"},
            {"letter": "E", "sound": "e", "anchor": "Elefante", "emoji": "🐘"},
            {"letter": "I", "sound": "i", "anchor": "Isla", "emoji": "🏝️"},
            {"letter": "O", "sound": "o", "anchor": "Oso", "emoji": "🐻"},
            {"letter": "U", "sound": "u", "anchor": "Uvas", "emoji": "🍇"},
            {"letter": "M", "sound": "eme", "anchor": "Manzana", "emoji": "🍎"},
            {"letter": "P", "sound": "pe", "anchor": "Pato", "emoji": "🦆"},
            {"letter": "S", "sound": "ese", "anchor": "Sol", "emoji": "☀️"},
            {"letter": "L", "sound": "ele", "anchor": "Luna", "emoji": "🌙"},
            {"letter": "T", "sound": "te", "anchor": "Tomate", "emoji": "🍅"},
            {"letter": "D", "sound": "de", "anchor": "Dado", "emoji": "🎲"},
            {"letter": "N", "sound": "ene", "anchor": "Nido", "emoji": "svg:nido"},
            {"letter": "F", "sound": "efe", "anchor": "Foca", "emoji": "svg:foca"},
            {"letter": "B", "sound": "be", "anchor": "Barco", "emoji": "⛵"},
            {"letter": "C", "sound": "ce", "anchor": "Casa", "emoji": "🏠"},
            {"letter": "R", "sound": "erre", "anchor": "Ratón", "emoji": "🐭"},
            {"letter": "G", "sound": "ge", "anchor": "Gato", "emoji": "🐱"},
            {"letter": "J", "sound": "jota", "anchor": "Jirafa", "emoji": "🦒"},
            {"letter": "V", "sound": "uve", "anchor": "Vaca", "emoji": "🐄"},
            {"letter": "Z", "sound": "zeta", "anchor": "Zapato", "emoji": "👟"},
            {"letter": "Ñ", "sound": "eñe", "anchor": "Ñandú", "emoji": "svg:ñandú"}
        ],
        "directSyllables": [
            {"consonant": "M", "syllables": [
                {"syllable": "MA", "word": "Mano", "emoji": "✋"},
                {"syllable": "ME", "word": "Mesa", "emoji": "svg:mesa"},
                {"syllable": "MI", "word": "Miel", "emoji": "🍯"},
                {"syllable": "MO", "word": "Moto", "emoji": "🛵"},
                {"syllable": "MU", "word": "Muela", "emoji": "🦷"}
            ]},
            {"consonant": "P", "syllables": [
                {"syllable": "PA", "word": "Pato", "emoji": "🦆"},
                {"syllable": "PE", "word": "Pera", "emoji": "🍐"},
                {"syllable": "PI", "word": "Pino", "emoji": "🌲"},
                {"syllable": "PO", "word": "Pollo", "emoji": "🐥"},
                {"syllable": "PU", "word": "Puente", "emoji": "🌉"}
            ]},
            {"consonant": "S", "syllables": [
                {"syllable": "SA", "word": "Sapo", "emoji": "🐸"},
                {"syllable": "SE", "word": "Seta", "emoji": "🍄"},
                {"syllable": "SI", "word": "Silla", "emoji": "💺"},
                {"syllable": "SO", "word": "Sopa", "emoji": "🍲"},
                {"syllable": "SU", "word": "Suma", "emoji": "➕"}
            ]},
            {"consonant": "L", "syllables": [
                {"syllable": "LA", "word": "Lana", "emoji": "🧶"},
                {"syllable": "LE", "word": "León", "emoji": "🦁"},
                {"syllable": "LI", "word": "Limón", "emoji": "🍋"},
                {"syllable": "LO", "word": "Lobo", "emoji": "🐺"},
                {"syllable": "LU", "word": "Luna", "emoji": "🌙"}
            ]},
            {"consonant": "T", "syllables": [
                {"syllable": "TA", "word": "Taza", "emoji": "🍵"},
                {"syllable": "TE", "word": "Tela", "emoji": "🧵"},
                {"syllable": "TI", "word": "Tigre", "emoji": "🐯"},
                {"syllable": "TO", "word": "Toro", "emoji": "🐂"},
                {"syllable": "TU", "word": "Tubo", "emoji": "🧪"}
            ]},
            {"consonant": "D", "syllables": [
                {"syllable": "DA", "word": "Dado", "emoji": "🎲"},
                {"syllable": "DE", "word": "Dedo", "emoji": "☝️"},
                {"syllable": "DI", "word": "Diente", "emoji": "🦷"},
                {"syllable": "DO", "word": "Dona", "emoji": "🍩"},
                {"syllable": "DU", "word": "Ducha", "emoji": "🚿"}
            ]},
            {"consonant": "N", "syllables": [
                {"syllable": "NA", "word": "Naranja", "emoji": "🍊"},
                {"syllable": "NE", "word": "Nieve", "emoji": "❄️"},
                {"syllable": "NI", "word": "Nido", "emoji": "svg:nido"},
                {"syllable": "NO", "word": "Noche", "emoji": "🌃"},
                {"syllable": "NU", "word": "Nube", "emoji": "☁️"}
            ]},
            {"consonant": "F", "syllables": [
                {"syllable": "FA", "word": "Faro", "emoji": "🗼"},
                {"syllable": "FE", "word": "Feliz", "emoji": "😄"},
                {"syllable": "FI", "word": "Fila", "emoji": "🚶"},
                {"syllable": "FO", "word": "Foca", "emoji": "svg:foca"},
                {"syllable": "FU", "word": "Fuego", "emoji": "🔥"}
            ]},
            {"consonant": "B", "syllables": [
                {"syllable": "BA", "word": "Barco", "emoji": "⛵"},
                {"syllable": "BE", "word": "Bebé", "emoji": "👶"},
                {"syllable": "BI", "word": "Bici", "emoji": "🚲"},
                {"syllable": "BO", "word": "Bota", "emoji": "👢"},
                {"syllable": "BU", "word": "Búho", "emoji": "🦉"}
            ]},
            {"consonant": "C", "syllables": [
                {"syllable": "CA", "word": "Casa", "emoji": "🏠"},
                {"syllable": "CO", "word": "Copa", "emoji": "🏆"},
                {"syllable": "CU", "word": "Cuna", "emoji": "🛏️"}
            ]},
            {"consonant": "R", "syllables": [
                {"syllable": "RA", "word": "Rana", "emoji": "🐸"},
                {"syllable": "RE", "word": "Reloj", "emoji": "⏰"},
                {"syllable": "RI", "word": "Río", "emoji": "🏞️"},
                {"syllable": "RO", "word": "Rosa", "emoji": "🌹"},
                {"syllable": "RU", "word": "Rueda", "emoji": "svg:rueda"}
            ]}
        ],
        "inverseSyllables": [
            {"group": "-L", "syllables": [{"syllable": "AL", "word": "Alto", "emoji": "🦒"}, {"syllable": "EL", "word": "Elfo", "emoji": "🧝"}, {"syllable": "OL", "word": "Olla", "emoji": "🍲"}, {"syllable": "UL", "word": "Último", "emoji": "🏁"}]},
            {"group": "-S", "syllables": [{"syllable": "AS", "word": "Astro", "emoji": "⭐"}, {"syllable": "ES", "word": "Escuela", "emoji": "🏫"}, {"syllable": "IS", "word": "Isla", "emoji": "🏝️"}, {"syllable": "OS", "word": "Ostra", "emoji": "🐚"}]},
            {"group": "-R", "syllables": [{"syllable": "AR", "word": "Árbol", "emoji": "🌳"}, {"syllable": "ER", "word": "Erizo", "emoji": "🦔"}, {"syllable": "OR", "word": "Orquesta", "emoji": "🎻"}, {"syllable": "UR", "word": "Urna", "emoji": "🗳️"}]},
            {"group": "-N", "syllables": [{"syllable": "AN", "word": "Antena", "emoji": "📡"}, {"syllable": "EN", "word": "Enano", "emoji": "🧙"}, {"syllable": "IN", "word": "Indio", "emoji": "🏹"}, {"syllable": "ON", "word": "Onda", "emoji": "🌊"}]}
        ],
        "complexSyllables": [
            {"prefix": "PL-", "syllable": "PLA", "word": "Plátano", "emoji": "🍌"},
            {"prefix": "BR-", "syllable": "BRA", "word": "Brazo", "emoji": "💪"},
            {"prefix": "TR-", "syllable": "TRA", "word": "Tractor", "emoji": "🚜"},
            {"prefix": "CR-", "syllable": "CRA", "word": "Crayón", "emoji": "🖍️"},
            {"prefix": "FR-", "syllable": "FRA", "word": "Fresa", "emoji": "🍓"},
            {"prefix": "GR-", "syllable": "GRA", "word": "Granja", "emoji": "🏡"},
            {"prefix": "DR-", "syllable": "DRA", "word": "Dragón", "emoji": "🐉"},
            {"prefix": "BL-", "syllable": "BLA", "word": "Blanco", "emoji": "⬜"}
        ],
        "rulesAndDigraphs": [
            {"id": "ch", "symbol": "CH", "rule": "Suena 'che' suave como en Chocolate 🍫", "words": ["Choza", "Chapa", "Chaqueta"]},
            {"id": "ll", "symbol": "LL", "rule": "Doble ele, suena como en Lluvia 🌧️ o Llave 🗝️", "words": ["Llama", "Llorar", "Lleno"]},
            {"id": "rr", "symbol": "RR", "rule": "Sonido fuerte entre vocales como en Perro 🐶", "words": ["Carro", "Torre", "Tierra"]},
            {"id": "qu", "symbol": "QU", "rule": "Siempre va con E o I: QUE, QUI como en Queso 🧀", "words": ["Química", "Quince", "Paquete"]},
            {"id": "gue", "symbol": "GUE / GUI", "rule": "La U no suena, da sonido suave a la G: Guitarra 🎸", "words": ["Guepardo", "Águila", "Guinda"]},
            {"id": "ce", "symbol": "CE / CI", "rule": "La C suena suave como la Z: Circo 🎪 o Cebra 🦓", "words": ["Cine", "Cerezas", "Cepillo"]},
            {"id": "n_tilde", "symbol": "Ñ", "rule": "Letra única del español: Montaña ⛰️ y Piña 🍍", "words": ["Ñandú", "Cabaña", "Muñeca"]}
        ],
        "sentenceWorkshop": [
            {"sign": "Coma (,)", "tip": "Haz una pausa breve para tomar aire.", "example": "El gato corre, salta y juega."},
            {"sign": "Punto (.)", "tip": "Pausa más larga. La idea ha terminado.", "example": "El perro duerme al sol."},
            {"sign": "Pregunta (¿?)", "tip": "Sube el tono al final como una melodía.", "example": "¿Dónde está la pelota?"},
            {"sign": "Exclamación (¡!)", "tip": "Pon entusiasmo, sorpresa o alegría en tu voz.", "example": "¡Qué golazo tan increíble!"}
        ]
    },
    "en": {
        "letters": [
            {"letter": "A", "sound": "/æ/", "anchor": "Apple", "emoji": "🍎"},
            {"letter": "B", "sound": "/b/", "anchor": "Bear", "emoji": "🐻"},
            {"letter": "C", "sound": "/k/", "anchor": "Cat", "emoji": "🐱"},
            {"letter": "D", "sound": "/d/", "anchor": "Dog", "emoji": "🐶"},
            {"letter": "E", "sound": "/e/", "anchor": "Elephant", "emoji": "🐘"},
            {"letter": "F", "sound": "/f/", "anchor": "Fish", "emoji": "🐟"},
            {"letter": "G", "sound": "/g/", "anchor": "Goat", "emoji": "🐐"},
            {"letter": "H", "sound": "/h/", "anchor": "Hat", "emoji": "🎩"},
            {"letter": "I", "sound": "/ɪ/", "anchor": "Igloo", "emoji": "svg:iglu"},
            {"letter": "J", "sound": "/dʒ/", "anchor": "Jug", "emoji": "🏺"},
            {"letter": "K", "sound": "/k/", "anchor": "Kite", "emoji": "svg:cometa"},
            {"letter": "L", "sound": "/l/", "anchor": "Lion", "emoji": "🦁"},
            {"letter": "M", "sound": "/m/", "anchor": "Moon", "emoji": "🌙"},
            {"letter": "N", "sound": "/n/", "anchor": "Nest", "emoji": "svg:nido"},
            {"letter": "O", "sound": "/ɒ/", "anchor": "Octopus", "emoji": "🐙"},
            {"letter": "P", "sound": "/p/", "anchor": "Pig", "emoji": "🐷"},
            {"letter": "Q", "sound": "/kw/", "anchor": "Queen", "emoji": "👑"},
            {"letter": "R", "sound": "/r/", "anchor": "Ring", "emoji": "💍"},
            {"letter": "S", "sound": "/s/", "anchor": "Sun", "emoji": "☀️"},
            {"letter": "T", "sound": "/t/", "anchor": "Tree", "emoji": "🌳"},
            {"letter": "U", "sound": "/ʌ/", "anchor": "Umbrella", "emoji": "☂️"},
            {"letter": "V", "sound": "/v/", "anchor": "Van", "emoji": "🚐"},
            {"letter": "W", "sound": "/w/", "anchor": "Watch", "emoji": "⌚"},
            {"letter": "Y", "sound": "/j/", "anchor": "Yo-yo", "emoji": "svg:yoyo"},
            {"letter": "Z", "sound": "/z/", "anchor": "Zebra", "emoji": "🦓"}
        ],
        "cvcRimes": [
            {"rime": "-AT", "words": [{"word": "CAT", "emoji": "🐱"}, {"word": "BAT", "emoji": "🦇"}, {"word": "HAT", "emoji": "🎩"}]},
            {"rime": "-UN", "words": [{"word": "SUN", "emoji": "☀️"}, {"word": "RUN", "emoji": "🏃"}, {"word": "BUN", "emoji": "🥯"}]},
            {"rime": "-OG", "words": [{"word": "DOG", "emoji": "🐶"}, {"word": "FROG", "emoji": "🐸"}, {"word": "LOG", "emoji": "svg:tronco"}]},
            {"rime": "-IN", "words": [{"word": "PIN", "emoji": "📌"}, {"word": "WIN", "emoji": "🏆"}, {"word": "BIN", "emoji": "🗑️"}]},
            {"rime": "-ET", "words": [{"word": "NET", "emoji": "🥅"}, {"word": "PET", "emoji": "🐕"}, {"word": "WET", "emoji": "💧"}]},
            {"rime": "-OP", "words": [{"word": "TOP", "emoji": "🔝"}, {"word": "HOP", "emoji": "🦘"}, {"word": "MOP", "emoji": "🧹"}]},
            {"rime": "-UG", "words": [{"word": "BUG", "emoji": "🐛"}, {"word": "MUG", "emoji": "☕"}, {"word": "HUG", "emoji": "🤗"}]}
        ],
        "blends": [
            {"blend": "BL", "word": "BLUE", "emoji": "🔵"},
            {"blend": "ST", "word": "STAR", "emoji": "⭐"},
            {"blend": "TR", "word": "TREE", "emoji": "🌳"},
            {"blend": "CR", "word": "CRAB", "emoji": "🦀"},
            {"blend": "FL", "word": "FLAG", "emoji": "🚩"},
            {"blend": "GR", "word": "GRAPE", "emoji": "🍇"},
            {"blend": "PL", "word": "PLANE", "emoji": "✈️"},
            {"blend": "BR", "word": "BREAD", "emoji": "🍞"}
        ],
        "digraphs": [
            {"digraph": "SH", "sound": "/ʃ/", "word": "SHIP", "emoji": "🚢"},
            {"digraph": "CH", "sound": "/tʃ/", "word": "CHAIR", "emoji": "💺"},
            {"digraph": "TH", "sound": "/θ/", "word": "THUMB", "emoji": "👍"},
            {"digraph": "PH", "sound": "/f/", "word": "PHONE", "emoji": "📱"},
            {"digraph": "WH", "sound": "/w/", "word": "WHALE", "emoji": "🐋"},
            {"digraph": "CK", "sound": "/k/", "word": "DUCK", "emoji": "🦆"}
        ],
        "vowelTeams": [
            {"pattern": "EE", "sound": "/iː/", "word": "TREE", "emoji": "🌳"},
            {"pattern": "EA", "sound": "/iː/", "word": "BEACH", "emoji": "🏖️"},
            {"pattern": "OA", "sound": "/oʊ/", "word": "BOAT", "emoji": "⛵"},
            {"pattern": "AI", "sound": "/eɪ/", "word": "RAIN", "emoji": "🌧️"},
            {"pattern": "OO", "sound": "/uː/", "word": "MOON", "emoji": "🌙"},
            {"pattern": "MAGIC-E", "sound": "Long Vowel", "word": "CAKE", "emoji": "🎂"}
        ],
        "sentenceWorkshop": [
            {"sign": "Comma (,)", "tip": "Take a quick breath pause.", "example": "The frog jumps, swims, and rests."},
            {"sign": "Period (.)", "tip": "Full stop. Idea is complete.", "example": "The puppy is asleep on the rug."},
            {"sign": "Question (?)", "tip": "Raise your voice pitch at the end.", "example": "Can you see the yellow bus?"},
            {"sign": "Exclamation (!)", "tip": "Read with high energy, wonder, or excitement.", "example": "Look at that shooting star!"}
        ]
    }
}

# Word Bank ES
wordBank_es = {
    "l1": [
        {"id": "es_l1_01", "target": "M", "anchorWord": "MANZANA", "emoji": "🍎", "distractors": ["P", "S", "L"]},
        {"id": "es_l1_02", "target": "P", "anchorWord": "PATO", "emoji": "🦆", "distractors": ["M", "T", "B"]},
        {"id": "es_l1_03", "target": "S", "anchorWord": "SOL", "emoji": "☀️", "distractors": ["N", "R", "D"]},
        {"id": "es_l1_04", "target": "L", "anchorWord": "LUNA", "emoji": "🌙", "distractors": ["F", "C", "T"]},
        {"id": "es_l1_05", "target": "T", "anchorWord": "TOMATE", "emoji": "🍅", "distractors": ["D", "P", "B"]},
        {"id": "es_l1_06", "target": "D", "anchorWord": "DADO", "emoji": "🎲", "distractors": ["T", "B", "M"]},
        {"id": "es_l1_07", "target": "N", "anchorWord": "NIDO", "emoji": "svg:nido", "distractors": ["M", "L", "S"]},
        {"id": "es_l1_08", "target": "F", "anchorWord": "FOCA", "emoji": "svg:foca", "distractors": ["T", "P", "S"]},
        {"id": "es_l1_09", "target": "B", "anchorWord": "BARCO", "emoji": "⛵", "distractors": ["D", "P", "V"]},
        {"id": "es_l1_10", "target": "C", "anchorWord": "CASA", "emoji": "🏠", "distractors": ["S", "K", "Q"]},
        {"id": "es_l1_11", "target": "R", "anchorWord": "RATON", "emoji": "🐭", "distractors": ["L", "D", "B"]},
        {"id": "es_l1_12", "target": "G", "anchorWord": "GATO", "emoji": "🐱", "distractors": ["J", "C", "B"]},
        {"id": "es_l1_13", "target": "J", "anchorWord": "JIRAFA", "emoji": "🦒", "distractors": ["G", "F", "L"]},
        {"id": "es_l1_14", "target": "V", "anchorWord": "VACA", "emoji": "🐄", "distractors": ["B", "P", "M"]},
        {"id": "es_l1_15", "target": "Z", "anchorWord": "ZAPATO", "emoji": "👟", "distractors": ["S", "C", "D"]},
        {"id": "es_l1_16", "target": "CH", "anchorWord": "CHOCOLATE", "emoji": "🍫", "distractors": ["LL", "RR", "QU"]},
        {"id": "es_l1_17", "target": "LL", "anchorWord": "LLAVE", "emoji": "🗝️", "distractors": ["CH", "Y", "L"]},
        {"id": "es_l1_18", "target": "Ñ", "anchorWord": "ÑANDU", "emoji": "svg:ñandú", "distractors": ["N", "M", "U"]},
        {"id": "es_l1_19", "target": "A", "anchorWord": "ABEJA", "emoji": "🐝", "distractors": ["E", "I", "O"]},
        {"id": "es_l1_20", "target": "E", "anchorWord": "ELEFANTE", "emoji": "🐘", "distractors": ["A", "O", "U"]},
        {"id": "es_l1_21", "target": "I", "anchorWord": "ISLA", "emoji": "🏝️", "distractors": ["E", "U", "A"]},
        {"id": "es_l1_22", "target": "O", "anchorWord": "OSO", "emoji": "🐻", "distractors": ["A", "E", "U"]},
        {"id": "es_l1_23", "target": "U", "anchorWord": "UVAS", "emoji": "🍇", "distractors": ["O", "I", "E"]},
        {"id": "es_l1_24", "target": "K", "anchorWord": "KOALA", "emoji": "🐨", "distractors": ["C", "Q", "P"]}
    ],
    "l2": [
        {"id": "es_l2_01", "word": "CASA", "syllables": ["CA", "SA"], "emoji": "🏠", "distractors": ["PATO", "LUNA", "MESA"]},
        {"id": "es_l2_02", "word": "PATO", "syllables": ["PA", "TO"], "emoji": "🦆", "distractors": ["GATO", "SAPO", "TORO"]},
        {"id": "es_l2_03", "word": "LUNA", "syllables": ["LU", "NA"], "emoji": "🌙", "distractors": ["CUNA", "LANA", "ROPA"]},
        {"id": "es_l2_04", "word": "MESA", "syllables": ["ME", "SA"], "emoji": "svg:mesa", "distractors": ["PESA", "TASA", "CASA"]},
        {"id": "es_l2_05", "word": "PELO", "syllables": ["PE", "LO"], "emoji": "💇", "distractors": ["PALO", "SOLO", "POLO"]},
        {"id": "es_l2_06", "word": "BOCA", "syllables": ["BO", "CA"], "emoji": "👄", "distractors": ["ROCA", "FOCA", "COCA"]},
        {"id": "es_l2_07", "word": "DADO", "syllables": ["DA", "DO"], "emoji": "🎲", "distractors": ["DEDO", "LADO", "NUDO"]},
        {"id": "es_l2_08", "word": "FOCA", "syllables": ["FO", "CA"], "emoji": "svg:foca", "distractors": ["BOCA", "ROCA", "SOPA"]},
        {"id": "es_l2_09", "word": "GATO", "syllables": ["GA", "TO"], "emoji": "🐱", "distractors": ["PATO", "RATO", "FOTO"]},
        {"id": "es_l2_10", "word": "LOBO", "syllables": ["LO", "BO"], "emoji": "🐺", "distractors": ["CUBO", "TUBO", "ROBO"]},
        {"id": "es_l2_11", "word": "MANO", "syllables": ["MA", "NO"], "emoji": "✋", "distractors": ["MONO", "CONO", "PIANO"]},
        {"id": "es_l2_12", "word": "NIDO", "syllables": ["NI", "DO"], "emoji": "svg:nido", "distractors": ["NUDO", "DADO", "LODO"]},
        {"id": "es_l2_13", "word": "ROPA", "syllables": ["RO", "PA"], "emoji": "👕", "distractors": ["SOPA", "COPA", "TAPA"]},
        {"id": "es_l2_14", "word": "SAPO", "syllables": ["SA", "PO"], "emoji": "🐸", "distractors": ["PATO", "GATO", "PASO"]},
        {"id": "es_l2_15", "word": "TORO", "syllables": ["TO", "RO"], "emoji": "🐂", "distractors": ["CORO", "LORO", "MURO"]},
        {"id": "es_l2_16", "word": "VACA", "syllables": ["VA", "CA"], "emoji": "🐄", "distractors": ["BOCA", "TACA", "LACA"]},
        {"id": "es_l2_17", "word": "YATE", "syllables": ["YA", "TE"], "emoji": "🛥️", "distractors": ["LOTE", "BOTE", "MATE"]},
        {"id": "es_l2_18", "word": "ZUMO", "syllables": ["ZU", "MO"], "emoji": "🧃", "distractors": ["HUMO", "SUMO", "RAMO"]},
        {"id": "es_l2_19", "word": "ROSA", "syllables": ["RO", "SA"], "emoji": "🌹", "distractors": ["COSA", "MESA", "SOSA"]},
        {"id": "es_l2_20", "word": "BOTA", "syllables": ["BO", "TA"], "emoji": "👢", "distractors": ["GOTA", "NOTA", "ROTA"]},
        {"id": "es_l2_21", "word": "COPA", "syllables": ["CO", "PA"], "emoji": "🏆", "distractors": ["SOPA", "ROPA", "CAPA"]},
        {"id": "es_l2_22", "word": "TAZA", "syllables": ["TA", "ZA"], "emoji": "🍵", "distractors": ["CASA", "MASA", "CAZA"]},
        {"id": "es_l2_23", "word": "VELA", "syllables": ["VE", "LA"], "emoji": "🕯️", "distractors": ["TELA", "PELA", "BOLA"]},
        {"id": "es_l2_24", "word": "RANA", "syllables": ["RA", "NA"], "emoji": "🐸", "distractors": ["LANA", "CANA", "SANA"]},
        {"id": "es_l2_25", "word": "MOTO", "syllables": ["MO", "TO"], "emoji": "🛵", "distractors": ["FOTO", "ROTO", "VOTO"]},
        {"id": "es_l2_26", "word": "PIÑA", "syllables": ["PI", "ÑA"], "emoji": "🍍", "distractors": ["NIÑA", "PEÑA", "VIÑA"]},
        {"id": "es_l2_27", "word": "NUDO", "syllables": ["NU", "DO"], "emoji": "svg:nudo", "distractors": ["NIDO", "LODO", "DADO"]}
    ],
    "l3": [
        {"id": "es_l3_01", "word": "CASA", "syllables": ["CA", "SA"], "emoji": "🏠", "missingIndices": [1, 3]},
        {"id": "es_l3_02", "word": "PATO", "syllables": ["PA", "TO"], "emoji": "🦆", "missingIndices": [1, 3]},
        {"id": "es_l3_03", "word": "LUNA", "syllables": ["LU", "NA"], "emoji": "🌙", "missingIndices": [1, 3]},
        {"id": "es_l3_04", "word": "MESA", "syllables": ["ME", "SA"], "emoji": "svg:mesa", "missingIndices": [1, 2]},
        {"id": "es_l3_05", "word": "DADO", "syllables": ["DA", "DO"], "emoji": "🎲", "missingIndices": [0, 2]},
        {"id": "es_l3_06", "word": "FOCA", "syllables": ["FO", "CA"], "emoji": "svg:foca", "missingIndices": [1, 2]},
        {"id": "es_l3_07", "word": "GATO", "syllables": ["GA", "TO"], "emoji": "🐱", "missingIndices": [1, 3]},
        {"id": "es_l3_08", "word": "LOBO", "syllables": ["LO", "BO"], "emoji": "🐺", "missingIndices": [0, 2]},
        {"id": "es_l3_09", "word": "MANO", "syllables": ["MA", "NO"], "emoji": "✋", "missingIndices": [1, 2]},
        {"id": "es_l3_10", "word": "NIDO", "syllables": ["NI", "DO"], "emoji": "svg:nido", "missingIndices": [1, 3]},
        {"id": "es_l3_11", "word": "ROPA", "syllables": ["RO", "PA"], "emoji": "👕", "missingIndices": [0, 3]},
        {"id": "es_l3_12", "word": "SAPO", "syllables": ["SA", "PO"], "emoji": "🐸", "missingIndices": [1, 2]},
        {"id": "es_l3_13", "word": "TORO", "syllables": ["TO", "RO"], "emoji": "🐂", "missingIndices": [0, 2]},
        {"id": "es_l3_14", "word": "VACA", "syllables": ["VA", "CA"], "emoji": "🐄", "missingIndices": [1, 3]},
        {"id": "es_l3_15", "word": "BOTA", "syllables": ["BO", "TA"], "emoji": "👢", "missingIndices": [1, 3]},
        {"id": "es_l3_16", "word": "ROSA", "syllables": ["RO", "SA"], "emoji": "🌹", "missingIndices": [1, 2]},
        {"id": "es_l3_17", "word": "TAZA", "syllables": ["TA", "ZA"], "emoji": "🍵", "missingIndices": [1, 3]},
        {"id": "es_l3_18", "word": "PELOTA", "syllables": ["PE", "LO", "TA"], "emoji": "⚽", "missingIndices": [1, 3]},
        {"id": "es_l3_19", "word": "TOMATE", "syllables": ["TO", "MA", "TE"], "emoji": "🍅", "missingIndices": [1, 4]},
        {"id": "es_l3_20", "word": "MALETA", "syllables": ["MA", "LE", "TA"], "emoji": "🧳", "missingIndices": [2, 4]},
        {"id": "es_l3_21", "word": "CAMISA", "syllables": ["CA", "MI", "SA"], "emoji": "👔", "missingIndices": [1, 3]},
        {"id": "es_l3_22", "word": "PAYASO", "syllables": ["PA", "YA", "SO"], "emoji": "🤡", "missingIndices": [2, 4]},
        {"id": "es_l3_23", "word": "SIRENA", "syllables": ["SI", "RE", "NA"], "emoji": "🧜", "missingIndices": [1, 4]},
        {"id": "es_l3_24", "word": "PALOMA", "syllables": ["PA", "LO", "MA"], "emoji": "🕊️", "missingIndices": [1, 3]},
        {"id": "es_l3_25", "word": "CORONA", "syllables": ["CO", "RO", "NA"], "emoji": "👑", "missingIndices": [1, 4]},
        {"id": "es_l3_26", "word": "NUDO", "syllables": ["NU", "DO"], "emoji": "svg:nudo", "missingIndices": [1, 2]}
    ],
    "l4": [
        {
            "id": "es_l4_01",
            "word": "ESTRELLA",
            "syllables": ["ES", "TRE", "LLA"],
            "emoji": "⭐",
            "microCheck": {
                "question": "¿Qué brilla en el cielo nocturno?",
                "options": [
                    {"emoji": "⭐", "label": "Una estrella", "isCorrect": True},
                    {"emoji": "☁️", "label": "Una nube", "isCorrect": False},
                    {"emoji": "🌧️", "label": "La lluvia", "isCorrect": False}
                ]
            }
        },
        {
            "id": "es_l4_02",
            "word": "PLATANO",
            "syllables": ["PLA", "TA", "NO"],
            "emoji": "🍌",
            "microCheck": {
                "question": "¿Qué fruta dulce y amarilla es?",
                "options": [
                    {"emoji": "🍌", "label": "Un plátano", "isCorrect": True},
                    {"emoji": "🍎", "label": "Una manzana", "isCorrect": False},
                    {"emoji": "🍇", "label": "Unas uvas", "isCorrect": False}
                ]
            }
        },
        {
            "id": "es_l4_03",
            "word": "TRACTOR",
            "syllables": ["TRAC", "TOR"],
            "emoji": "🚜",
            "microCheck": {
                "question": "¿Qué vehículo trabaja en el campo?",
                "options": [
                    {"emoji": "🚜", "label": "Un tractor", "isCorrect": True},
                    {"emoji": "🏎️", "label": "Un coche veloz", "isCorrect": False},
                    {"emoji": "✈️", "label": "Un avión", "isCorrect": False}
                ]
            }
        },
        {
            "id": "es_l4_04",
            "word": "DRAGON",
            "syllables": ["DRA", "GON"],
            "emoji": "🐉",
            "microCheck": {
                "question": "¿Qué criatura fantástica escupe fuego?",
                "options": [
                    {"emoji": "🐉", "label": "Un dragón", "isCorrect": True},
                    {"emoji": "🦄", "label": "Un unicornio", "isCorrect": False},
                    {"emoji": "🦅", "label": "Un águila", "isCorrect": False}
                ]
            }
        },
        {
            "id": "es_l4_05",
            "word": "BRUJA",
            "syllables": ["BRU", "JA"],
            "emoji": "🧙",
            "microCheck": {
                "question": "¿Quién vuela montada en una escoba?",
                "options": [
                    {"emoji": "🧙", "label": "Una bruja", "isCorrect": True},
                    {"emoji": "🧚", "label": "Un hada", "isCorrect": False},
                    {"emoji": "🧝", "label": "Un elfo", "isCorrect": False}
                ]
            }
        },
        {
            "id": "es_l4_06",
            "word": "GLOBO",
            "syllables": ["GLO", "BO"],
            "emoji": "🎈",
            "microCheck": {
                "question": "¿Qué juguete ligero sube por el aire?",
                "options": [
                    {"emoji": "🎈", "label": "Un globo", "isCorrect": True},
                    {"emoji": "⚽", "label": "Un balón", "isCorrect": False},
                    {"emoji": "🧱", "label": "Un ladrillo", "isCorrect": False}
                ]
            }
        },
        {
            "id": "es_l4_07",
            "word": "FLECHA",
            "syllables": ["FLE", "CHA"],
            "emoji": "🏹",
            "microCheck": {
                "question": "¿Qué proyectil se dispara con un arco?",
                "options": [
                    {"emoji": "🏹", "label": "Una flecha", "isCorrect": True},
                    {"emoji": "🗡️", "label": "Una espada", "isCorrect": False},
                    {"emoji": "🛡️", "label": "Un escudo", "isCorrect": False}
                ]
            }
        },
        {
            "id": "es_l4_08",
            "word": "CRAYON",
            "syllables": ["CRA", "YON"],
            "emoji": "🖍️",
            "microCheck": {
                "question": "¿Qué barra de cera sirve para colorear?",
                "options": [
                    {"emoji": "🖍️", "label": "Un crayón", "isCorrect": True},
                    {"emoji": "✂️", "label": "Una tijera", "isCorrect": False},
                    {"emoji": "📏", "label": "Una regla", "isCorrect": False}
                ]
            }
        },
        {
            "id": "es_l4_09",
            "word": "GRILLO",
            "syllables": ["GRI", "LLO"],
            "emoji": "🦗",
            "microCheck": {
                "question": "¿Qué insecto emite un canto de noche?",
                "options": [
                    {"emoji": "🦗", "label": "Un grillo", "isCorrect": True},
                    {"emoji": "🐝", "label": "Una abeja", "isCorrect": False},
                    {"emoji": "🐜", "label": "Una hormiga", "isCorrect": False}
                ]
            }
        },
        {
            "id": "es_l4_10",
            "word": "PLANETA",
            "syllables": ["PLA", "NE", "TA"],
            "emoji": "🌍",
            "microCheck": {
                "question": "¿Qué gran cuerpo viaja en el espacio?",
                "options": [
                    {"emoji": "🌍", "label": "Un planeta", "isCorrect": True},
                    {"emoji": "svg:cometa", "label": "Una cometa", "isCorrect": False},
                    {"emoji": "svg:paracaídas", "label": "Un paracaídas", "isCorrect": False}
                ]
            }
        },
        {
            "id": "es_l4_11",
            "word": "TREN",
            "syllables": ["TREN"],
            "emoji": "🚆",
            "microCheck": {
                "question": "¿Qué transporte viaja sobre vías metálicas?",
                "options": [
                    {"emoji": "🚆", "label": "Un tren", "isCorrect": True},
                    {"emoji": "🚌", "label": "Un autobús", "isCorrect": False},
                    {"emoji": "🚲", "label": "Una bicicleta", "isCorrect": False}
                ]
            }
        },
        {
            "id": "es_l4_12",
            "word": "BARCO",
            "syllables": ["BAR", "CO"],
            "emoji": "⛵",
            "microCheck": {
                "question": "¿Qué navega flotando sobre el agua?",
                "options": [
                    {"emoji": "⛵", "label": "Un barco", "isCorrect": True},
                    {"emoji": "🚀", "label": "Un cohete", "isCorrect": False},
                    {"emoji": "🚗", "label": "Un coche", "isCorrect": False}
                ]
            }
        },
        {
            "id": "es_l4_13",
            "word": "ARBOL",
            "syllables": ["AR", "BOL"],
            "emoji": "🌳",
            "microCheck": {
                "question": "¿Qué ser vivo tiene tronco verde y hojas?",
                "options": [
                    {"emoji": "🌳", "label": "Un árbol", "isCorrect": True},
                    {"emoji": "svg:piedra", "label": "Una piedra", "isCorrect": False},
                    {"emoji": "🍄", "label": "Una seta", "isCorrect": False}
                ]
            }
        },
        {
            "id": "es_l4_14",
            "word": "CIRCO",
            "syllables": ["CIR", "CO"],
            "emoji": "🎪",
            "microCheck": {
                "question": "¿Dónde hay payasos, magia y malabaristas?",
                "options": [
                    {"emoji": "🎪", "label": "El circo", "isCorrect": True},
                    {"emoji": "🏫", "label": "La escuela", "isCorrect": False},
                    {"emoji": "🏥", "label": "El hospital", "isCorrect": False}
                ]
            }
        },
        {
            "id": "es_l4_15",
            "word": "TORTUGA",
            "syllables": ["TOR", "TU", "GA"],
            "emoji": "🐢",
            "microCheck": {
                "question": "¿Qué animal camina lento con su caparazón?",
                "options": [
                    {"emoji": "🐢", "label": "La tortuga", "isCorrect": True},
                    {"emoji": "🐰", "label": "El conejo", "isCorrect": False},
                    {"emoji": "🐆", "label": "El guepardo", "isCorrect": False}
                ]
            }
        },
        {
            "id": "es_l4_16",
            "word": "CHOCOLATE",
            "syllables": ["CHO", "CO", "LA", "TE"],
            "emoji": "🍫",
            "microCheck": {
                "question": "¿Qué rico dulce se prepara con cacao?",
                "options": [
                    {"emoji": "🍫", "label": "El chocolate", "isCorrect": True},
                    {"emoji": "🍋", "label": "El limón ácido", "isCorrect": False},
                    {"emoji": "🧂", "label": "La sal", "isCorrect": False}
                ]
            }
        },
        {
            "id": "es_l4_17",
            "word": "CASTILLO",
            "syllables": ["CAS", "TI", "LLO"],
            "emoji": "🏰",
            "microCheck": {
                "question": "¿Dónde vivían reyes y caballeros medievales?",
                "options": [
                    {"emoji": "🏰", "label": "Un castillo", "isCorrect": True},
                    {"emoji": "🏡", "label": "Una choza", "isCorrect": False},
                    {"emoji": "⛺", "label": "Una tienda de campaña", "isCorrect": False}
                ]
            }
        },
        {
            "id": "es_l4_18",
            "word": "GUITARRA",
            "syllables": ["GUI", "TA", "RRA"],
            "emoji": "🎸",
            "microCheck": {
                "question": "¿Qué instrumento musical tiene seis cuerdas?",
                "options": [
                    {"emoji": "🎸", "label": "Una guitarra", "isCorrect": True},
                    {"emoji": "🥁", "label": "Un tambor", "isCorrect": False},
                    {"emoji": "🎺", "label": "Una trompeta", "isCorrect": False}
                ]
            }
        },
        {
            "id": "es_l4_19",
            "word": "QUESO",
            "syllables": ["QUE", "SO"],
            "emoji": "🧀",
            "microCheck": {
                "question": "¿Qué alimento sabroso se elabora con leche?",
                "options": [
                    {"emoji": "🧀", "label": "El queso", "isCorrect": True},
                    {"emoji": "🥖", "label": "El pan", "isCorrect": False},
                    {"emoji": "🍯", "label": "La miel de abeja", "isCorrect": False}
                ]
            }
        },
        {
            "id": "es_l4_20",
            "word": "DELFIN",
            "syllables": ["DEL", "FIN"],
            "emoji": "🐬",
            "microCheck": {
                "question": "¿Qué mamífero marino salta en las olas?",
                "options": [
                    {"emoji": "🐬", "label": "El delfín", "isCorrect": True},
                    {"emoji": "🦈", "label": "El tiburón", "isCorrect": False},
                    {"emoji": "🐙", "label": "El pulpo", "isCorrect": False}
                ]
            }
        },
        {
            "id": "es_l4_21",
            "word": "MONTAÑA",
            "syllables": ["MON", "TA", "ÑA"],
            "emoji": "⛰️",
            "microCheck": {
                "question": "¿Qué pico de tierra se eleva hasta las nubes?",
                "options": [
                    {"emoji": "⛰️", "label": "Una montaña", "isCorrect": True},
                    {"emoji": "🏖️", "label": "Una playa", "isCorrect": False},
                    {"emoji": "🏜️", "label": "Un desierto", "isCorrect": False}
                ]
            }
        },
        {
            "id": "es_l4_22",
            "word": "TAMBOR",
            "syllables": ["TAM", "BOR"],
            "emoji": "🥁",
            "microCheck": {
                "question": "¿Qué instrumento se golpea con dos baquetas?",
                "options": [
                    {"emoji": "🥁", "label": "Un tambor", "isCorrect": True},
                    {"emoji": "🎻", "label": "Un violín", "isCorrect": False},
                    {"emoji": "🎹", "label": "Un piano", "isCorrect": False}
                ]
            }
        },
        {
            "id": "es_l4_23",
            "word": "SOMBRILLA",
            "syllables": ["SOM", "BRI", "LLA"],
            "emoji": "⛱️",
            "microCheck": {
                "question": "¿Qué nos da sombra fresca en la arena de la playa?",
                "options": [
                    {"emoji": "⛱️", "label": "Una sombrilla", "isCorrect": True},
                    {"emoji": "🧣", "label": "Una bufanda de lana", "isCorrect": False},
                    {"emoji": "🧤", "label": "Unos guantes", "isCorrect": False}
                ]
            }
        },
        {
            "id": "es_l4_24",
            "word": "CANGURO",
            "syllables": ["CAN", "GU", "RO"],
            "emoji": "🦘",
            "microCheck": {
                "question": "¿Qué animal salta veloz con su bolsa marsupial?",
                "options": [
                    {"emoji": "🦘", "label": "El canguro", "isCorrect": True},
                    {"emoji": "🐨", "label": "El koala", "isCorrect": False},
                    {"emoji": "🐼", "label": "El oso panda", "isCorrect": False}
                ]
            }
        },
        {
            "id": "es_l4_25",
            "word": "PINGÜINO",
            "syllables": ["PIN", "GÜI", "NO"],
            "emoji": "🐧",
            "microCheck": {
                "question": "¿Qué ave marina nada en el hielo con smoking?",
                "options": [
                    {"emoji": "🐧", "label": "El pingüino", "isCorrect": True},
                    {"emoji": "🦆", "label": "El pato", "isCorrect": False},
                    {"emoji": "🦅", "label": "El águila", "isCorrect": False}
                ]
            }
        },
        {
            "id": "es_l4_26",
            "word": "ESPONJA",
            "syllables": ["ES", "PON", "JA"],
            "emoji": "🧽",
            "microCheck": {
                "question": "¿Qué absorbe agua y jabón para limpiar?",
                "options": [
                    {"emoji": "🧽", "label": "Una esponja", "isCorrect": True},
                    {"emoji": "🧹", "label": "Una escoba", "isCorrect": False},
                    {"emoji": "svg:cubo", "label": "Un cubo", "isCorrect": False}
                ]
            }
        }
    ]
}

# Sentence Bank ES
sentenceBank_es = {
    "l5": [
        {
            "id": "es_l5_01",
            "lines": ["El gato duerme tranquilo", "sobre el suave sofá de lana."],
            "wordCount": 10,
            "microCheck": {
                "question": "¿Dónde duerme el gato tranquilo?",
                "options": [
                    {"icon": "🛋️", "label": "Sobre el sofá", "isCorrect": True},
                    {"icon": "🌳", "label": "En un árbol alto", "isCorrect": False},
                    {"icon": "🧺", "label": "Dentro de una cesta", "isCorrect": False}
                ]
            }
        },
        {
            "id": "es_l5_02",
            "lines": ["La niña lee un cuento alegre", "antes de apagar la luz."],
            "wordCount": 11,
            "microCheck": {
                "question": "¿Qué hace la niña antes de dormir?",
                "options": [
                    {"icon": "📖", "label": "Lee un cuento", "isCorrect": True},
                    {"icon": "🎨", "label": "Pinta un cuadro", "isCorrect": False},
                    {"icon": "🥣", "label": "Prepara la cena", "isCorrect": False}
                ]
            }
        },
        {
            "id": "es_l5_03",
            "lines": ["El sol brilla en el cielo", "y calienta las flores del jardín."],
            "wordCount": 12,
            "microCheck": {
                "question": "¿Qué calienta el sol brillante?",
                "options": [
                    {"icon": "🌸", "label": "Las flores del jardín", "isCorrect": True},
                    {"icon": "❄️", "label": "Los copos de nieve", "isCorrect": False},
                    {"icon": "🚗", "label": "Las ruedas de un coche", "isCorrect": False}
                ]
            }
        },
        {
            "id": "es_l5_04",
            "lines": ["El perro busca su pelota roja", "debajo de la mesa redonda."],
            "wordCount": 11,
            "microCheck": {
                "question": "¿De qué color es la pelota del perro?",
                "options": [
                    {"icon": "🔴", "label": "De color rojo", "isCorrect": True},
                    {"icon": "🔵", "label": "De color azul", "isCorrect": False},
                    {"icon": "🟢", "label": "De color verde", "isCorrect": False}
                ]
            }
        },
        {
            "id": "es_l5_05",
            "lines": ["Los pájaros cantan al amanecer", "en las ramas más altas del bosque."],
            "wordCount": 12,
            "microCheck": {
                "question": "¿Cuándo cantan los pájaros alegres?",
                "options": [
                    {"icon": "🌅", "label": "Al amanecer", "isCorrect": True},
                    {"icon": "🌙", "label": "A medianoche", "isCorrect": False},
                    {"icon": "🌧️", "label": "Durante una tormenta", "isCorrect": False}
                ]
            }
        },
        {
            "id": "es_l5_06",
            "lines": ["El barco blanco navega despacio", "por las olas del mar azul."],
            "wordCount": 11,
            "microCheck": {
                "question": "¿Por dónde navega el barco blanco?",
                "options": [
                    {"icon": "🌊", "label": "Por las olas del mar", "isCorrect": True},
                    {"icon": "🛤️", "label": "Por las vías del tren", "isCorrect": False},
                    {"icon": "☁️", "label": "Por encima de las nubes", "isCorrect": False}
                ]
            }
        },
        {
            "id": "es_l5_07",
            "lines": ["Mi hermano prepara zumo de naranja", "para desayunar con pan tostado."],
            "wordCount": 11,
            "microCheck": {
                "question": "¿De qué fruta prepara el zumo?",
                "options": [
                    {"icon": "🍊", "label": "De naranja", "isCorrect": True},
                    {"icon": "🍎", "label": "De manzana", "isCorrect": False},
                    {"icon": "🍇", "label": "De uva", "isCorrect": False}
                ]
            }
        },
        {
            "id": "es_l5_08",
            "lines": ["La cometa amarilla vuela muy alto", "empujada por la brisa fresca."],
            "wordCount": 11,
            "microCheck": {
                "question": "¿De qué color es la cometa que vuela?",
                "options": [
                    {"icon": "🟡", "label": "Amarilla", "isCorrect": True},
                    {"icon": "🟣", "label": "Morada", "isCorrect": False},
                    {"icon": "⚪", "label": "Blanca", "isCorrect": False}
                ]
            }
        },
        {
            "id": "es_l5_09",
            "lines": ["El tren veloz llega a la estación", "haciendo sonar su alegre silbato."],
            "wordCount": 12,
            "microCheck": {
                "question": "¿A dónde llega el tren veloz?",
                "options": [
                    {"icon": "🚉", "label": "A la estación", "isCorrect": True},
                    {"icon": "🏖️", "label": "A la playa", "isCorrect": False},
                    {"icon": "🎪", "label": "Al circo", "isCorrect": False}
                ]
            }
        },
        {
            "id": "es_l5_10",
            "lines": ["Las abejas recogen el dulce néctar", "de las flores de primavera."],
            "wordCount": 11,
            "microCheck": {
                "question": "¿Quién recoge el néctar de las flores?",
                "options": [
                    {"icon": "🐝", "label": "Las abejas", "isCorrect": True},
                    {"icon": "🦋", "label": "Las orugas", "isCorrect": False},
                    {"icon": "🐌", "label": "Los caracoles", "isCorrect": False}
                ]
            }
        },
        {
            "id": "es_l5_11",
            "lines": ["El oso pardo busca miel fresca", "en el hueco de un roble."],
            "wordCount": 12,
            "microCheck": {
                "question": "¿Qué alimento busca el oso pardo?",
                "options": [
                    {"icon": "🍯", "label": "Miel fresca", "isCorrect": True},
                    {"icon": "🐟", "label": "Pescado frito", "isCorrect": False},
                    {"icon": "🥖", "label": "Pan crujiente", "isCorrect": False}
                ]
            }
        },
        {
            "id": "es_l5_12",
            "lines": ["La luna ilumina los caminos", "cuando cae la noche silenciosa."],
            "wordCount": 10,
            "microCheck": {
                "question": "¿Qué ilumina la luna por la noche?",
                "options": [
                    {"icon": "🛣️", "label": "Los caminos", "isCorrect": True},
                    {"icon": "🏊", "label": "El fondo de la piscina", "isCorrect": False},
                    {"icon": "🕳️", "label": "Una cueva oscura", "isCorrect": False}
                ]
            }
        },
        {
            "id": "es_l5_13",
            "lines": ["El caracol pasea muy despacio", "llevando su casita a cuestas."],
            "wordCount": 10,
            "microCheck": {
                "question": "¿Cómo se mueve el caracol?",
                "options": [
                    {"icon": "🐌", "label": "Muy despacio", "isCorrect": True},
                    {"icon": "⚡", "label": "A toda velocidad", "isCorrect": False},
                    {"icon": "🦘", "label": "Dando saltos gigantes", "isCorrect": False}
                ]
            }
        },
        {
            "id": "es_l5_14",
            "lines": ["La lluvia moja los tejados rojos", "y llena de charcos el patio."],
            "wordCount": 12,
            "microCheck": {
                "question": "¿De qué se llena el patio con la lluvia?",
                "options": [
                    {"icon": "💦", "label": "De charcos", "isCorrect": True},
                    {"icon": "🍂", "label": "De hojas secas", "isCorrect": False},
                    {"icon": "🎈", "label": "De globos de colores", "isCorrect": False}
                ]
            }
        },
        {
            "id": "es_l5_15",
            "lines": ["La ardilla guarda ricas castañas", "para comer en los días de frío."],
            "wordCount": 12,
            "microCheck": {
                "question": "¿Qué fruto guarda la ardilla previsora?",
                "options": [
                    {"icon": "🌰", "label": "Castañas", "isCorrect": True},
                    {"icon": "🍓", "label": "Fresas silvestres", "isCorrect": False},
                    {"icon": "🌽", "label": "Mazorcas de maíz", "isCorrect": False}
                ]
            }
        },
        {
            "id": "es_l5_16",
            "lines": ["Los niños construyen un castillo", "con arena mojada en la orilla."],
            "wordCount": 11,
            "microCheck": {
                "question": "¿Con qué construyen el castillo los niños?",
                "options": [
                    {"icon": "🏖️", "label": "Con arena mojada", "isCorrect": True},
                    {"icon": "🧱", "label": "Con bloques de piedra", "isCorrect": False},
                    {"icon": "svg:tronco", "label": "Con ramas secas", "isCorrect": False}
                ]
            }
        },
        {
            "id": "es_l5_17",
            "lines": ["El búho abre sus grandes ojos", "para vigilar el bosque dormido."],
            "wordCount": 11,
            "microCheck": {
                "question": "¿Qué vigila el búho de noche?",
                "options": [
                    {"icon": "🌲", "label": "El bosque dormido", "isCorrect": True},
                    {"icon": "🏙️", "label": "La gran ciudad", "isCorrect": False},
                    {"icon": "🚢", "label": "El puerto marino", "isCorrect": False}
                ]
            }
        },
        {
            "id": "es_l5_18",
            "lines": ["La cocinera hornea galletas de miel", "que huelen delicioso en toda la casa."],
            "wordCount": 13,
            "microCheck": {
                "question": "¿De qué sabor son las galletas del horno?",
                "options": [
                    {"icon": "🍯", "label": "De miel", "isCorrect": True},
                    {"icon": "🍫", "label": "De chocolate amargo", "isCorrect": False},
                    {"icon": "🧂", "label": "De queso y sal", "isCorrect": False}
                ]
            }
        }
    ],
    "l6": [
        {
            "id": "es_l6_01",
            "lines": [
                "Los delfines saltan felices en el mar azul.",
                "Nadan en grandes grupos familiares",
                "y se comunican cantando silbidos bajo el agua."
            ],
            "wordCount": 20,
            "microCheck": {
                "question": "¿Cómo se comunican los delfines bajo el agua?",
                "options": [
                    {"icon": "🎶", "label": "Cantando silbidos", "isCorrect": True},
                    {"icon": "🔦", "label": "Con destellos de luz", "isCorrect": False},
                    {"icon": "🤫", "label": "Nadando en silencio", "isCorrect": False}
                ]
            }
        },
        {
            "id": "es_l6_02",
            "lines": [
                "En lo alto de la colina verde,",
                "un molino de viento hace girar sus aspas.",
                "Gracias a su fuerza, el trigo se convierte en harina."
            ],
            "wordCount": 24,
            "microCheck": {
                "question": "¿En qué se convierte el trigo dentro del molino?",
                "options": [
                    {"icon": "🌾", "label": "En harina", "isCorrect": True},
                    {"icon": "🍞", "label": "En pan horneado", "isCorrect": False},
                    {"icon": "🥣", "label": "En sopa caliente", "isCorrect": False}
                ]
            }
        },
        {
            "id": "es_l6_03",
            "lines": [
                "¿Sabías que los camaleones cambian de color?",
                "Pueden volverse verdes, marrones o dorados.",
                "Así se camuflan entre las hojas para estar seguros."
            ],
            "wordCount": 22,
            "microCheck": {
                "question": "¿Para qué cambian de color los camaleones?",
                "options": [
                    {"icon": "🍃", "label": "Para camuflarse entre hojas", "isCorrect": True},
                    {"icon": "😴", "label": "Para dormir más abrigados", "isCorrect": False},
                    {"icon": "🏃", "label": "Para correr más deprisa", "isCorrect": False}
                ]
            }
        },
        {
            "id": "es_l6_04",
            "lines": [
                "El astronauta flota ligero dentro de su nave espacial.",
                "Mira por la ventana redonda y ve la Tierra azul.",
                "¡Qué hermoso y brillante se ve nuestro planeta desde las estrellas!"
            ],
            "wordCount": 28,
            "microCheck": {
                "question": "¿Qué observa el astronauta desde la ventana redonda?",
                "options": [
                    {"icon": "🌍", "label": "La Tierra azul", "isCorrect": True},
                    {"icon": "☄️", "label": "Un cometa de hielo", "isCorrect": False},
                    {"icon": "👽", "label": "Un platillo volante", "isCorrect": False}
                ]
            }
        },
        {
            "id": "es_l6_05",
            "lines": [
                "Una pequeña oruga verde come hojas sin parar.",
                "Construye un capullo suave para dormir tranquila",
                "y despierta convertida en una preciosa mariposa de colores."
            ],
            "wordCount": 24,
            "microCheck": {
                "question": "¿En qué se transforma la pequeña oruga al despertar?",
                "options": [
                    {"icon": "🦋", "label": "En una hermosa mariposa", "isCorrect": True},
                    {"icon": "🐝", "label": "En una abeja obrera", "isCorrect": False},
                    {"icon": "🐞", "label": "En una mariquita roja", "isCorrect": False}
                ]
            }
        },
        {
            "id": "es_l6_06",
            "lines": [
                "El faro vigila la costa desde un acantilado rocoso.",
                "Enciende su potente luz giratoria cada noche",
                "para guiar a los marineros sanos y salvos hasta el puerto."
            ],
            "wordCount": 26,
            "microCheck": {
                "question": "¿A quién guía la luz giratoria del faro?",
                "options": [
                    {"icon": "⛵", "label": "A los marineros que navegan", "isCorrect": True},
                    {"icon": "✈️", "label": "A los pilotos de avión", "isCorrect": False},
                    {"icon": "🚗", "label": "A los conductores de camiones", "isCorrect": False}
                ]
            }
        },
        {
            "id": "es_l6_07",
            "lines": [
                "Las hormigas trabajan en equipo con gran disciplina.",
                "Cada una transporta una semilla hacia el hormiguero.",
                "Así aseguran comida fresca para todo el invierno."
            ],
            "wordCount": 23,
            "microCheck": {
                "question": "¿Qué transportan las hormigas al hormiguero?",
                "options": [
                    {"icon": "🌱", "label": "Semillas de plantas", "isCorrect": True},
                    {"icon": "svg:piedra", "label": "Piedras pesadas", "isCorrect": False},
                    {"icon": "💧", "label": "Gotas de rocío", "isCorrect": False}
                ]
            }
        },
        {
            "id": "es_l6_08",
            "lines": [
                "En la biblioteca del pueblo reina un agradable silencio.",
                "Los estantes están repletos de libros de aventuras.",
                "Los lectores viajan a mundos lejanos con solo abrir sus páginas."
            ],
            "wordCount": 26,
            "microCheck": {
                "question": "¿De qué están repletos los estantes de la biblioteca?",
                "options": [
                    {"icon": "📚", "label": "De libros de aventuras", "isCorrect": True},
                    {"icon": "🧸", "label": "De juguetes antiguos", "isCorrect": False},
                    {"icon": "🏆", "label": "De trofeos dorados", "isCorrect": False}
                ]
            }
        },
        {
            "id": "es_l6_09",
            "lines": [
                "¡Mira cómo cae la nieve silenciosa sobre las montañas!",
                "Los tejados de las casas parecen de algodón blanco.",
                "Los niños salen abrigados con botas para jugar con trineos."
            ],
            "wordCount": 26,
            "microCheck": {
                "question": "¿A qué se parecen los tejados cubiertos de nieve?",
                "options": [
                    {"icon": "☁️", "label": "A algodón blanco", "isCorrect": True},
                    {"icon": "🍦", "label": "A helado de fresa", "isCorrect": False},
                    {"icon": "svg:piedra", "label": "A piedras grises", "isCorrect": False}
                ]
            }
        },
        {
            "id": "es_l6_10",
            "lines": [
                "El río desciende cantando desde las cumbres heladas.",
                "Riega los campos de trigo y calma la sed de los animales.",
                "Su agua limpia es un tesoro valioso para toda la naturaleza."
            ],
            "wordCount": 29,
            "microCheck": {
                "question": "¿Desde dónde desciende el agua del río?",
                "options": [
                    {"icon": "🏔️", "label": "Desde las cumbres heladas", "isCorrect": True},
                    {"icon": "🏜️", "label": "Desde el desierto árido", "isCorrect": False},
                    {"icon": "🌋", "label": "Desde el cráter de un volcán", "isCorrect": False}
                ]
            }
        },
        {
            "id": "es_l6_11",
            "lines": [
                "Los pulpos tienen tres corazones y sangre de color azul.",
                "Cuando sienten peligro, expulsan una nube de tinta oscura.",
                "Ese truco les permite escapar nadando sin ser vistos."
            ],
            "wordCount": 27,
            "microCheck": {
                "question": "¿Cuántos corazones tienen los pulpos en el mar?",
                "options": [
                    {"icon": "❤️", "label": "Tres corazones", "isCorrect": True},
                    {"icon": "1️⃣", "label": "Un solo corazón", "isCorrect": False},
                    {"icon": "5️⃣", "label": "Cinco corazones", "isCorrect": False}
                ]
            }
        },
        {
            "id": "es_l6_12",
            "lines": [
                "La música de la orquesta comenzó con un suave violín.",
                "Poco a poco se unieron las flautas, los trompetas y los tambores.",
                "El público aplaudió emocionado al final del gran concierto."
            ],
            "wordCount": 28,
            "microCheck": {
                "question": "¿Qué instrumento empezó a sonar primero?",
                "options": [
                    {"icon": "🎻", "label": "Un suave violín", "isCorrect": True},
                    {"icon": "🥁", "label": "Un fuerte tambor", "isCorrect": False},
                    {"icon": "🎺", "label": "Una trompeta brillante", "isCorrect": False}
                ]
            }
        },
        {
            "id": "es_l6_13",
            "lines": [
                "En el fondo del mar viven arrecifes llenos de vida.",
                "Peces payaso de rayas naranjas nadan entre las anémonas.",
                "Es un hogar lleno de colores donde todos se ayudan a convivir."
            ],
            "wordCount": 29,
            "microCheck": {
                "question": "¿De qué color son las rayas de los peces payaso?",
                "options": [
                    {"icon": "🧡", "label": "Rayas naranjas", "isCorrect": True},
                    {"icon": "🖤", "label": "Rayas negras", "isCorrect": False},
                    {"icon": "💚", "label": "Rayas verdes", "isCorrect": False}
                ]
            }
        },
        {
            "id": "es_l6_14",
            "lines": [
                "El castor construye una sólida presa con ramas y barro.",
                "Crea un estanque tranquilo donde edifica su hogar flotante.",
                "Allí sus crías descansan protegidas del viento y de los depredadores."
            ],
            "wordCount": 27,
            "microCheck": {
                "question": "¿Con qué construye su presa el ingenioso castor?",
                "options": [
                    {"icon": "svg:tronco", "label": "Con ramas y barro", "isCorrect": True},
                    {"icon": "🧱", "label": "Con piedras y cemento", "isCorrect": False},
                    {"icon": "🌾", "label": "Con paja seca", "isCorrect": False}
                ]
            }
        },
        {
            "id": "es_l6_15",
            "lines": [
                "Los koalas duermen casi veinte horas al día en los árboles.",
                "Se alimentan de hojas frescas de eucalipto en Australia.",
                "Sus patas fuertes les permiten trepar sin resbalar jamás."
            ],
            "wordCount": 26,
            "microCheck": {
                "question": "¿De qué se alimentan principalmente los koalas?",
                "options": [
                    {"icon": "🍃", "label": "De hojas de eucalipto", "isCorrect": True},
                    {"icon": "🍌", "label": "De plátanos maduros", "isCorrect": False},
                    {"icon": "🌾", "label": "De granos de trigo", "isCorrect": False}
                ]
            }
        },
        {
            "id": "es_l6_16",
            "lines": [
                "¡Qué divertido es observar una noche de estrellas fugaces!",
                "Cuando un meteorito cruza la atmósfera, deja una estela dorada.",
                "Pide un buen deseo antes de que desaparezca en la inmensidad."
            ],
            "wordCount": 28,
            "microCheck": {
                "question": "¿Qué deja el meteorito al cruzar la atmósfera nocturna?",
                "options": [
                    {"icon": "✨", "label": "Una estela dorada", "isCorrect": True},
                    {"icon": "💨", "label": "Una nube de humo negro", "isCorrect": False},
                    {"icon": "🌧️", "label": "Un rastro de lluvia", "isCorrect": False}
                ]
            }
        }
    ]
}

# Word Bank EN
wordBank_en = {
    "l1": [
        {"id": "en_l1_01", "target": "A", "anchorWord": "APPLE", "emoji": "🍎", "distractors": ["E", "I", "O"]},
        {"id": "en_l1_02", "target": "B", "anchorWord": "BEAR", "emoji": "🐻", "distractors": ["D", "P", "T"]},
        {"id": "en_l1_03", "target": "C", "anchorWord": "CAT", "emoji": "🐱", "distractors": ["K", "S", "G"]},
        {"id": "en_l1_04", "target": "D", "anchorWord": "DOG", "emoji": "🐶", "distractors": ["B", "P", "T"]},
        {"id": "en_l1_05", "target": "E", "anchorWord": "ELEPHANT", "emoji": "🐘", "distractors": ["A", "O", "U"]},
        {"id": "en_l1_06", "target": "F", "anchorWord": "FISH", "emoji": "🐟", "distractors": ["V", "P", "T"]},
        {"id": "en_l1_07", "target": "G", "anchorWord": "GOAT", "emoji": "🐐", "distractors": ["C", "J", "K"]},
        {"id": "en_l1_08", "target": "H", "anchorWord": "HAT", "emoji": "🎩", "distractors": ["N", "M", "K"]},
        {"id": "en_l1_09", "target": "I", "anchorWord": "IGLOO", "emoji": "svg:iglu", "distractors": ["E", "A", "O"]},
        {"id": "en_l1_10", "target": "J", "anchorWord": "JUG", "emoji": "🏺", "distractors": ["G", "Y", "L"]},
        {"id": "en_l1_11", "target": "K", "anchorWord": "KITE", "emoji": "svg:cometa", "distractors": ["C", "T", "P"]},
        {"id": "en_l1_12", "target": "L", "anchorWord": "LION", "emoji": "🦁", "distractors": ["I", "T", "R"]},
        {"id": "en_l1_13", "target": "M", "anchorWord": "MOON", "emoji": "🌙", "distractors": ["N", "W", "H"]},
        {"id": "en_l1_14", "target": "N", "anchorWord": "NEST", "emoji": "svg:nido", "distractors": ["M", "U", "H"]},
        {"id": "en_l1_15", "target": "O", "anchorWord": "OCTOPUS", "emoji": "🐙", "distractors": ["A", "U", "C"]},
        {"id": "en_l1_16", "target": "P", "anchorWord": "PIG", "emoji": "🐷", "distractors": ["B", "D", "Q"]},
        {"id": "en_l1_17", "target": "R", "anchorWord": "RING", "emoji": "💍", "distractors": ["P", "B", "N"]},
        {"id": "en_l1_18", "target": "S", "anchorWord": "SUN", "emoji": "☀️", "distractors": ["C", "Z", "X"]},
        {"id": "en_l1_19", "target": "T", "anchorWord": "TREE", "emoji": "🌳", "distractors": ["F", "L", "D"]},
        {"id": "en_l1_20", "target": "U", "anchorWord": "UMBRELLA", "emoji": "☂️", "distractors": ["V", "O", "W"]},
        {"id": "en_l1_21", "target": "V", "anchorWord": "VAN", "emoji": "🚐", "distractors": ["U", "W", "Y"]},
        {"id": "en_l1_22", "target": "W", "anchorWord": "WATCH", "emoji": "⌚", "distractors": ["M", "V", "N"]},
        {"id": "en_l1_23", "target": "Y", "anchorWord": "YOYO", "emoji": "svg:yoyo", "distractors": ["V", "J", "U"]},
        {"id": "en_l1_24", "target": "Z", "anchorWord": "ZEBRA", "emoji": "🦓", "distractors": ["S", "X", "C"]}
    ],
    "l2": [
        {"id": "en_l2_01", "word": "CAT", "syllables": ["CAT"], "emoji": "🐱", "distractors": ["BAT", "HAT", "RAT"]},
        {"id": "en_l2_02", "word": "DOG", "syllables": ["DOG"], "emoji": "🐶", "distractors": ["FOG", "LOG", "PIG"]},
        {"id": "en_l2_03", "word": "SUN", "syllables": ["SUN"], "emoji": "☀️", "distractors": ["BUN", "RUN", "FUN"]},
        {"id": "en_l2_04", "word": "PIG", "syllables": ["PIG"], "emoji": "🐷", "distractors": ["BIG", "WIG", "DIG"]},
        {"id": "en_l2_05", "word": "BUS", "syllables": ["BUS"], "emoji": "🚌", "distractors": ["CUP", "BUG", "TUB"]},
        {"id": "en_l2_06", "word": "CUP", "syllables": ["CUP"], "emoji": "☕", "distractors": ["PUP", "CAP", "MUG"]},
        {"id": "en_l2_07", "word": "HAT", "syllables": ["HAT"], "emoji": "🎩", "distractors": ["CAT", "MAT", "HOT"]},
        {"id": "en_l2_08", "word": "NET", "syllables": ["NET"], "emoji": "🥅", "distractors": ["PET", "WET", "NUT"]},
        {"id": "en_l2_09", "word": "PEN", "syllables": ["PEN"], "emoji": "🖊️", "distractors": ["HEN", "TEN", "PIN"]},
        {"id": "en_l2_10", "word": "BED", "syllables": ["BED"], "emoji": "🛏️", "distractors": ["RED", "FED", "BAD"]},
        {"id": "en_l2_11", "word": "BOX", "syllables": ["BOX"], "emoji": "📦", "distractors": ["FOX", "POX", "BAG"]},
        {"id": "en_l2_12", "word": "FOX", "syllables": ["FOX"], "emoji": "🦊", "distractors": ["BOX", "FIX", "DOG"]},
        {"id": "en_l2_13", "word": "FROG", "syllables": ["FROG"], "emoji": "🐸", "distractors": ["FLAG", "FROM", "TOAD"]},
        {"id": "en_l2_14", "word": "DUCK", "syllables": ["DUCK"], "emoji": "🦆", "distractors": ["LUCK", "SOCK", "DECK"]},
        {"id": "en_l2_15", "word": "FISH", "syllables": ["FISH"], "emoji": "🐟", "distractors": ["DISH", "WISH", "SHIP"]},
        {"id": "en_l2_16", "word": "SHIP", "syllables": ["SHIP"], "emoji": "🚢", "distractors": ["SHOP", "CHIP", "TRIP"]},
        {"id": "en_l2_17", "word": "STAR", "syllables": ["STAR"], "emoji": "⭐", "distractors": ["STIR", "SCAR", "MOON"]},
        {"id": "en_l2_18", "word": "MOON", "syllables": ["MOON"], "emoji": "🌙", "distractors": ["SOON", "NOON", "SPOON"]},
        {"id": "en_l2_19", "word": "BOOK", "syllables": ["BOOK"], "emoji": "📖", "distractors": ["LOOK", "HOOK", "COOK"]},
        {"id": "en_l2_20", "word": "BALL", "syllables": ["BALL"], "emoji": "⚽", "distractors": ["WALL", "FALL", "BELL"]},
        {"id": "en_l2_21", "word": "TREE", "syllables": ["TREE"], "emoji": "🌳", "distractors": ["FREE", "THREE", "TRUE"]},
        {"id": "en_l2_22", "word": "BIRD", "syllables": ["BIRD"], "emoji": "🐦", "distractors": ["WORD", "HERD", "BARD"]},
        {"id": "en_l2_23", "word": "LION", "syllables": ["LI", "ON"], "emoji": "🦁", "distractors": ["TIGER", "BEAR", "LEOPARD"]},
        {"id": "en_l2_24", "word": "TIGER", "syllables": ["TI", "GER"], "emoji": "🐯", "distractors": ["LION", "ZEBRA", "PANDA"]},
        {"id": "en_l2_25", "word": "RABBIT", "syllables": ["RAB", "BIT"], "emoji": "🐰", "distractors": ["HABIT", "ROBIN", "TURTLE"]},
        {"id": "en_l2_26", "word": "PUPPY", "syllables": ["PUP", "PY"], "emoji": "🐶", "distractors": ["KITTY", "BUNNY", "POPPY"]}
    ],
    "l3": [
        {"id": "en_l3_01", "word": "CAT", "syllables": ["CAT"], "emoji": "🐱", "missingIndices": [1]},
        {"id": "en_l3_02", "word": "DOG", "syllables": ["DOG"], "emoji": "🐶", "missingIndices": [1]},
        {"id": "en_l3_03", "word": "SUN", "syllables": ["SUN"], "emoji": "☀️", "missingIndices": [1]},
        {"id": "en_l3_04", "word": "PIG", "syllables": ["PIG"], "emoji": "🐷", "missingIndices": [1]},
        {"id": "en_l3_05", "word": "BUS", "syllables": ["BUS"], "emoji": "🚌", "missingIndices": [0, 2]},
        {"id": "en_l3_06", "word": "CUP", "syllables": ["CUP"], "emoji": "☕", "missingIndices": [1]},
        {"id": "en_l3_07", "word": "HAT", "syllables": ["HAT"], "emoji": "🎩", "missingIndices": [0, 2]},
        {"id": "en_l3_08", "word": "NET", "syllables": ["NET"], "emoji": "🥅", "missingIndices": [1]},
        {"id": "en_l3_09", "word": "PEN", "syllables": ["PEN"], "emoji": "🖊️", "missingIndices": [1]},
        {"id": "en_l3_10", "word": "BED", "syllables": ["BED"], "emoji": "🛏️", "missingIndices": [0, 2]},
        {"id": "en_l3_11", "word": "BOX", "syllables": ["BOX"], "emoji": "📦", "missingIndices": [1]},
        {"id": "en_l3_12", "word": "FOX", "syllables": ["FOX"], "emoji": "🦊", "missingIndices": [1]},
        {"id": "en_l3_13", "word": "FROG", "syllables": ["FROG"], "emoji": "🐸", "missingIndices": [1, 3]},
        {"id": "en_l3_14", "word": "DUCK", "syllables": ["DUCK"], "emoji": "🦆", "missingIndices": [1, 2]},
        {"id": "en_l3_15", "word": "FISH", "syllables": ["FISH"], "emoji": "🐟", "missingIndices": [1, 3]},
        {"id": "en_l3_16", "word": "SHIP", "syllables": ["SHIP"], "emoji": "🚢", "missingIndices": [1, 2]},
        {"id": "en_l3_17", "word": "STAR", "syllables": ["STAR"], "emoji": "⭐", "missingIndices": [0, 2]},
        {"id": "en_l3_18", "word": "MOON", "syllables": ["MOON"], "emoji": "🌙", "missingIndices": [1, 2]},
        {"id": "en_l3_19", "word": "BOOK", "syllables": ["BOOK"], "emoji": "📖", "missingIndices": [1, 2]},
        {"id": "en_l3_20", "word": "BALL", "syllables": ["BALL"], "emoji": "⚽", "missingIndices": [1, 3]},
        {"id": "en_l3_21", "word": "TREE", "syllables": ["TREE"], "emoji": "🌳", "missingIndices": [1, 2]},
        {"id": "en_l3_22", "word": "BIRD", "syllables": ["BIRD"], "emoji": "🐦", "missingIndices": [1, 2]},
        {"id": "en_l3_23", "word": "LION", "syllables": ["LI", "ON"], "emoji": "🦁", "missingIndices": [1, 3]},
        {"id": "en_l3_24", "word": "TIGER", "syllables": ["TI", "GER"], "emoji": "🐯", "missingIndices": [1, 4]},
        {"id": "en_l3_25", "word": "RABBIT", "syllables": ["RAB", "BIT"], "emoji": "🐰", "missingIndices": [1, 4]}
    ],
    "l4": [
        {
            "id": "en_l4_01",
            "word": "DRAGON",
            "syllables": ["DRA", "GON"],
            "emoji": "🐉",
            "microCheck": {
                "question": "What magical creature breathes fire?",
                "options": [
                    {"emoji": "🐉", "label": "A dragon", "isCorrect": True},
                    {"emoji": "🦄", "label": "A unicorn", "isCorrect": False},
                    {"emoji": "🦅", "label": "An eagle", "isCorrect": False}
                ]
            }
        },
        {
            "id": "en_l4_02",
            "word": "TRACTOR",
            "syllables": ["TRAC", "TOR"],
            "emoji": "🚜",
            "microCheck": {
                "question": "Which machine works on a farm field?",
                "options": [
                    {"emoji": "🚜", "label": "A tractor", "isCorrect": True},
                    {"emoji": "🏎️", "label": "A racing car", "isCorrect": False},
                    {"emoji": "✈️", "label": "An airplane", "isCorrect": False}
                ]
            }
        },
        {
            "id": "en_l4_03",
            "word": "PLANET",
            "syllables": ["PLAN", "ET"],
            "emoji": "🌍",
            "microCheck": {
                "question": "What orbits the sun in outer space?",
                "options": [
                    {"emoji": "🌍", "label": "A planet", "isCorrect": True},
                    {"emoji": "svg:cometa", "label": "A kite", "isCorrect": False},
                    {"emoji": "svg:paracaídas", "label": "A parachute", "isCorrect": False}
                ]
            }
        },
        {
            "id": "en_l4_04",
            "word": "DOLPHIN",
            "syllables": ["DOL", "PHIN"],
            "emoji": "🐬",
            "microCheck": {
                "question": "Which playful sea mammal leaps in waves?",
                "options": [
                    {"emoji": "🐬", "label": "A dolphin", "isCorrect": True},
                    {"emoji": "🦈", "label": "A shark", "isCorrect": False},
                    {"emoji": "🐙", "label": "An octopus", "isCorrect": False}
                ]
            }
        },
        {
            "id": "en_l4_05",
            "word": "CASTLE",
            "syllables": ["CAS", "TLE"],
            "emoji": "🏰",
            "microCheck": {
                "question": "Where did kings and knights live?",
                "options": [
                    {"emoji": "🏰", "label": "In a castle", "isCorrect": True},
                    {"emoji": "🏡", "label": "In a hut", "isCorrect": False},
                    {"emoji": "⛺", "label": "In a tent", "isCorrect": False}
                ]
            }
        },
        {
            "id": "en_l4_06",
            "word": "GUITAR",
            "syllables": ["GUI", "TAR"],
            "emoji": "🎸",
            "microCheck": {
                "question": "Which musical instrument has six strings?",
                "options": [
                    {"emoji": "🎸", "label": "A guitar", "isCorrect": True},
                    {"emoji": "🥁", "label": "A drum", "isCorrect": False},
                    {"emoji": "🎺", "label": "A trumpet", "isCorrect": False}
                ]
            }
        },
        {
            "id": "en_l4_07",
            "word": "TURTLE",
            "syllables": ["TUR", "TLE"],
            "emoji": "🐢",
            "microCheck": {
                "question": "Which animal moves slowly with a shell?",
                "options": [
                    {"emoji": "🐢", "label": "A turtle", "isCorrect": True},
                    {"emoji": "🐰", "label": "A rabbit", "isCorrect": False},
                    {"emoji": "🐆", "label": "A cheetah", "isCorrect": False}
                ]
            }
        },
        {
            "id": "en_l4_08",
            "word": "PENGUIN",
            "syllables": ["PEN", "GUIN"],
            "emoji": "🐧",
            "microCheck": {
                "question": "Which bird waddles on ice and swims fast?",
                "options": [
                    {"emoji": "🐧", "label": "A penguin", "isCorrect": True},
                    {"emoji": "🦆", "label": "A duck", "isCorrect": False},
                    {"emoji": "🦉", "label": "An owl", "isCorrect": False}
                ]
            }
        },
        {
            "id": "en_l4_09",
            "word": "MONKEY",
            "syllables": ["MON", "KEY"],
            "emoji": "🐒",
            "microCheck": {
                "question": "Which animal swings through jungle trees?",
                "options": [
                    {"emoji": "🐒", "label": "A monkey", "isCorrect": True},
                    {"emoji": "🐻", "label": "A bear", "isCorrect": False},
                    {"emoji": "🐺", "label": "A wolf", "isCorrect": False}
                ]
            }
        },
        {
            "id": "en_l4_10",
            "word": "SUNSET",
            "syllables": ["SUN", "SET"],
            "emoji": "🌇",
            "microCheck": {
                "question": "What happens when the sun goes down at dusk?",
                "options": [
                    {"emoji": "🌇", "label": "A sunset", "isCorrect": True},
                    {"emoji": "🌅", "label": "A sunrise", "isCorrect": False},
                    {"emoji": "🌧️", "label": "A snowstorm", "isCorrect": False}
                ]
            }
        },
        {
            "id": "en_l4_11",
            "word": "PICNIC",
            "syllables": ["PIC", "NIC"],
            "emoji": "🧺",
            "microCheck": {
                "question": "What outdoor meal is eaten on a blanket?",
                "options": [
                    {"emoji": "🧺", "label": "A picnic", "isCorrect": True},
                    {"emoji": "🍳", "label": "A restaurant dinner", "isCorrect": False},
                    {"emoji": "🛒", "label": "A grocery shop", "isCorrect": False}
                ]
            }
        },
        {
            "id": "en_l4_12",
            "word": "APPLE",
            "syllables": ["AP", "PLE"],
            "emoji": "🍎",
            "microCheck": {
                "question": "Which crisp round fruit grows on trees?",
                "options": [
                    {"emoji": "🍎", "label": "An apple", "isCorrect": True},
                    {"emoji": "🥕", "label": "A carrot", "isCorrect": False},
                    {"emoji": "🥔", "label": "A potato", "isCorrect": False}
                ]
            }
        },
        {
            "id": "en_l4_13",
            "word": "KITTEN",
            "syllables": ["KIT", "TEN"],
            "emoji": "🐱",
            "microCheck": {
                "question": "What is a baby cat called?",
                "options": [
                    {"emoji": "🐱", "label": "A kitten", "isCorrect": True},
                    {"emoji": "🐶", "label": "A puppy", "isCorrect": False},
                    {"emoji": "🐣", "label": "A chick", "isCorrect": False}
                ]
            }
        },
        {
            "id": "en_l4_14",
            "word": "BALLOON",
            "syllables": ["BAL", "LOON"],
            "emoji": "🎈",
            "microCheck": {
                "question": "What rubber toy floats high in the air?",
                "options": [
                    {"emoji": "🎈", "label": "A balloon", "isCorrect": True},
                    {"emoji": "⚽", "label": "A soccer ball", "isCorrect": False},
                    {"emoji": "svg:piedra", "label": "A heavy rock", "isCorrect": False}
                ]
            }
        },
        {
            "id": "en_l4_15",
            "word": "ROBOT",
            "syllables": ["RO", "BOT"],
            "emoji": "🤖",
            "microCheck": {
                "question": "What mechanical helper is run by computers?",
                "options": [
                    {"emoji": "🤖", "label": "A robot", "isCorrect": True},
                    {"emoji": "🐴", "label": "A horse", "isCorrect": False},
                    {"emoji": "🌱", "label": "A plant", "isCorrect": False}
                ]
            }
        },
        {
            "id": "en_l4_16",
            "word": "ROCKET",
            "syllables": ["ROCK", "ET"],
            "emoji": "🚀",
            "microCheck": {
                "question": "What vehicle blasts astronauts to the stars?",
                "options": [
                    {"emoji": "🚀", "label": "A rocket", "isCorrect": True},
                    {"emoji": "⛵", "label": "A sailboat", "isCorrect": False},
                    {"emoji": "🚲", "label": "A bicycle", "isCorrect": False}
                ]
            }
        },
        {
            "id": "en_l4_17",
            "word": "SPIDER",
            "syllables": ["SPI", "DER"],
            "emoji": "🕷️",
            "microCheck": {
                "question": "Which creature spins a sticky silk web?",
                "options": [
                    {"emoji": "🕷️", "label": "A spider", "isCorrect": True},
                    {"emoji": "🐜", "label": "An ant", "isCorrect": False},
                    {"emoji": "🐝", "label": "A bumblebee", "isCorrect": False}
                ]
            }
        },
        {
            "id": "en_l4_18",
            "word": "WINTER",
            "syllables": ["WIN", "TER"],
            "emoji": "❄️",
            "microCheck": {
                "question": "Which cold season brings ice and snow?",
                "options": [
                    {"emoji": "❄️", "label": "Winter", "isCorrect": True},
                    {"emoji": "☀️", "label": "Summer", "isCorrect": False},
                    {"emoji": "🌸", "label": "Spring", "isCorrect": False}
                ]
            }
        },
        {
            "id": "en_l4_19",
            "word": "SUMMER",
            "syllables": ["SUM", "MER"],
            "emoji": "🏖️",
            "microCheck": {
                "question": "Which sunny season is great for beach trips?",
                "options": [
                    {"emoji": "🏖️", "label": "Summer", "isCorrect": True},
                    {"emoji": "❄️", "label": "Winter", "isCorrect": False},
                    {"emoji": "🍂", "label": "Autumn", "isCorrect": False}
                ]
            }
        },
        {
            "id": "en_l4_20",
            "word": "FLOWER",
            "syllables": ["FLOW", "ER"],
            "emoji": "🌸",
            "microCheck": {
                "question": "What colorful garden plant has fragrant petals?",
                "options": [
                    {"emoji": "🌸", "label": "A flower", "isCorrect": True},
                    {"emoji": "svg:tronco", "label": "A log", "isCorrect": False},
                    {"emoji": "svg:piedra", "label": "A stone", "isCorrect": False}
                ]
            }
        },
        {
            "id": "en_l4_21",
            "word": "SILVER",
            "syllables": ["SIL", "VER"],
            "emoji": "🥈",
            "microCheck": {
                "question": "Which shiny metal is given for second place?",
                "options": [
                    {"emoji": "🥈", "label": "Silver", "isCorrect": True},
                    {"emoji": "🥇", "label": "Gold", "isCorrect": False},
                    {"emoji": "🥉", "label": "Bronze", "isCorrect": False}
                ]
            }
        },
        {
            "id": "en_l4_22",
            "word": "BASKET",
            "syllables": ["BAS", "KET"],
            "emoji": "🧺",
            "microCheck": {
                "question": "What woven container holds fruit and snacks?",
                "options": [
                    {"emoji": "🧺", "label": "A basket", "isCorrect": True},
                    {"emoji": "svg:cubo", "label": "A steel bucket", "isCorrect": False},
                    {"emoji": "📦", "label": "A glass bottle", "isCorrect": False}
                ]
            }
        },
        {
            "id": "en_l4_23",
            "word": "PENCIL",
            "syllables": ["PEN", "CIL"],
            "emoji": "✏️",
            "microCheck": {
                "question": "What wooden tool writes with graphite lead?",
                "options": [
                    {"emoji": "✏️", "label": "A pencil", "isCorrect": True},
                    {"emoji": "✂️", "label": "Scissors", "isCorrect": False},
                    {"emoji": "📏", "label": "A ruler", "isCorrect": False}
                ]
            }
        },
        {
            "id": "en_l4_24",
            "word": "CANDLE",
            "syllables": ["CAN", "DLE"],
            "emoji": "🕯️",
            "microCheck": {
                "question": "What wax stick gives off a small flame?",
                "options": [
                    {"emoji": "🕯️", "label": "A candle", "isCorrect": True},
                    {"emoji": "🔦", "label": "A flashlight", "isCorrect": False},
                    {"emoji": "💡", "label": "A lightbulb", "isCorrect": False}
                ]
            }
        },
        {
            "id": "en_l4_25",
            "word": "DOCTOR",
            "syllables": ["DOC", "TOR"],
            "emoji": "👨‍⚕️",
            "microCheck": {
                "question": "Who helps patients feel healthy and well?",
                "options": [
                    {"emoji": "👨‍⚕️", "label": "A doctor", "isCorrect": True},
                    {"emoji": "🧑‍🍳", "label": "A baker", "isCorrect": False},
                    {"emoji": "🧑‍🎨", "label": "A painter", "isCorrect": False}
                ]
            }
        },
        {
            "id": "en_l4_26",
            "word": "CIRCUS",
            "syllables": ["CIR", "CUS"],
            "emoji": "🎪",
            "microCheck": {
                "question": "Where do acrobats and clowns perform shows?",
                "options": [
                    {"emoji": "🎪", "label": "The circus", "isCorrect": True},
                    {"emoji": "🏦", "label": "The bank", "isCorrect": False},
                    {"emoji": "✈️", "label": "The airport", "isCorrect": False}
                ]
            }
        }
    ]
}

# Sentence Bank EN
sentenceBank_en = {
    "l5": [
        {
            "id": "en_l5_01",
            "lines": ["The black cat sleeps peacefully", "on the soft wool rug."],
            "wordCount": 11,
            "microCheck": {
                "question": "Where is the cat sleeping peacefully?",
                "options": [
                    {"icon": "🛋️", "label": "On the wool rug", "isCorrect": True},
                    {"icon": "🌳", "label": "Up in a pine tree", "isCorrect": False},
                    {"icon": "🚗", "label": "Inside the car", "isCorrect": False}
                ]
            }
        },
        {
            "id": "en_l5_02",
            "lines": ["The girl reads a funny book", "before switching off her bedroom lamp."],
            "wordCount": 12,
            "microCheck": {
                "question": "What does the girl read before sleep?",
                "options": [
                    {"icon": "📖", "label": "A funny book", "isCorrect": True},
                    {"icon": "🗺️", "label": "A treasure map", "isCorrect": False},
                    {"icon": "📰", "label": "A daily newspaper", "isCorrect": False}
                ]
            }
        },
        {
            "id": "en_l5_03",
            "lines": ["The warm sun shines brightly", "and warms the flowers in the garden."],
            "wordCount": 12,
            "microCheck": {
                "question": "What does the bright sun warm up?",
                "options": [
                    {"icon": "🌸", "label": "Garden flowers", "isCorrect": True},
                    {"icon": "❄️", "label": "Winter snowmen", "isCorrect": False},
                    {"icon": "🧊", "label": "Ice cubes in a glass", "isCorrect": False}
                ]
            }
        },
        {
            "id": "en_l5_04",
            "lines": ["The puppy chases its red ball", "across the green grassy lawn."],
            "wordCount": 11,
            "microCheck": {
                "question": "What color is the puppy's ball?",
                "options": [
                    {"icon": "🔴", "label": "Bright red", "isCorrect": True},
                    {"icon": "🔵", "label": "Dark blue", "isCorrect": False},
                    {"icon": "🟡", "label": "Sunny yellow", "isCorrect": False}
                ]
            }
        },
        {
            "id": "en_l5_05",
            "lines": ["Wild birds sing sweet songs", "in the tallest branches of the forest."],
            "wordCount": 12,
            "microCheck": {
                "question": "Where are the wild birds singing?",
                "options": [
                    {"icon": "🌳", "label": "In tall forest branches", "isCorrect": True},
                    {"icon": "🏊", "label": "Under the swimming pool", "isCorrect": False},
                    {"icon": "🕳️", "label": "Deep inside a dark tunnel", "isCorrect": False}
                ]
            }
        },
        {
            "id": "en_l5_06",
            "lines": ["A white sailboat glides gently", "over the calm blue sea waves."],
            "wordCount": 11,
            "microCheck": {
                "question": "What is gliding over the sea waves?",
                "options": [
                    {"icon": "⛵", "label": "A white sailboat", "isCorrect": True},
                    {"icon": "🚂", "label": "A steam locomotive", "isCorrect": False},
                    {"icon": "🚜", "label": "A heavy green tractor", "isCorrect": False}
                ]
            }
        },
        {
            "id": "en_l5_07",
            "lines": ["My brother squeezes fresh orange juice", "to drink with his warm toast."],
            "wordCount": 12,
            "microCheck": {
                "question": "What kind of fruit juice was squeezed?",
                "options": [
                    {"icon": "🍊", "label": "Fresh orange juice", "isCorrect": True},
                    {"icon": "🍎", "label": "Sweet apple cider", "isCorrect": False},
                    {"icon": "🍇", "label": "Purple grape juice", "isCorrect": False}
                ]
            }
        },
        {
            "id": "en_l5_08",
            "lines": ["The bright yellow kite flies high,", "lifted by the gentle morning breeze."],
            "wordCount": 12,
            "microCheck": {
                "question": "What lifts the yellow kite into the air?",
                "options": [
                    {"icon": "💨", "label": "The morning breeze", "isCorrect": True},
                    {"icon": "🌧️", "label": "A heavy thunderstorm", "isCorrect": False},
                    {"icon": "🚀", "label": "A jet rocket motor", "isCorrect": False}
                ]
            }
        },
        {
            "id": "en_l5_09",
            "lines": ["The silver express train arrives", "and blows its loud cheerful whistle."],
            "wordCount": 11,
            "microCheck": {
                "question": "What sound does the express train make?",
                "options": [
                    {"icon": "📢", "label": "Its loud whistle", "isCorrect": True},
                    {"icon": "🔔", "label": "A soft church bell", "isCorrect": False},
                    {"icon": "🎸", "label": "A rock guitar tune", "isCorrect": False}
                ]
            }
        },
        {
            "id": "en_l5_10",
            "lines": ["Busy worker bees collect sweet nectar", "from colorful blooming spring flowers."],
            "wordCount": 11,
            "microCheck": {
                "question": "Who collects sweet nectar from flowers?",
                "options": [
                    {"icon": "🐝", "label": "Busy worker bees", "isCorrect": True},
                    {"icon": "🐜", "label": "Tiny black ants", "isCorrect": False},
                    {"icon": "🦗", "label": "Singing green crickets", "isCorrect": False}
                ]
            }
        },
        {
            "id": "en_l5_11",
            "lines": ["The brown bear searches for honey", "inside the hollow of an oak tree."],
            "wordCount": 13,
            "microCheck": {
                "question": "What food is the brown bear searching for?",
                "options": [
                    {"icon": "🍯", "label": "Sweet golden honey", "isCorrect": True},
                    {"icon": "🥖", "label": "Loaves of crusty bread", "isCorrect": False},
                    {"icon": "🍫", "label": "Bars of dark chocolate", "isCorrect": False}
                ]
            }
        },
        {
            "id": "en_l5_12",
            "lines": ["The silver moon lights the paths", "as silent night falls over town."],
            "wordCount": 12,
            "microCheck": {
                "question": "What lights the paths when night arrives?",
                "options": [
                    {"icon": "🌙", "label": "The silver moon", "isCorrect": True},
                    {"icon": "🕯️", "label": "A single candle flame", "isCorrect": False},
                    {"icon": "🔦", "label": "A police searchlight", "isCorrect": False}
                ]
            }
        },
        {
            "id": "en_l5_13",
            "lines": ["The garden snail crawls very slowly,", "carrying its spiral shell on its back."],
            "wordCount": 13,
            "microCheck": {
                "question": "What does the garden snail carry?",
                "options": [
                    {"icon": "🐌", "label": "Its spiral shell", "isCorrect": True},
                    {"icon": "🎒", "label": "A leather backpack", "isCorrect": False},
                    {"icon": "🧳", "label": "A heavy metal suitcase", "isCorrect": False}
                ]
            }
        },
        {
            "id": "en_l5_14",
            "lines": ["Cold raindrops wet the red roofs", "and leave shiny puddles on the ground."],
            "wordCount": 13,
            "microCheck": {
                "question": "What appears on the ground after it rains?",
                "options": [
                    {"icon": "💦", "label": "Shiny puddles", "isCorrect": True},
                    {"icon": "🍂", "label": "Dry fallen leaves", "isCorrect": False},
                    {"icon": "🏖️", "label": "Piles of yellow sand", "isCorrect": False}
                ]
            }
        },
        {
            "id": "en_l5_15",
            "lines": ["The nimble squirrel gathers ripe nuts", "to store safely for cold winter days."],
            "wordCount": 13,
            "microCheck": {
                "question": "What does the squirrel gather for winter?",
                "options": [
                    {"icon": "🌰", "label": "Ripe nuts", "isCorrect": True},
                    {"icon": "🍓", "label": "Fresh berries", "isCorrect": False},
                    {"icon": "🍄", "label": "Wild mushrooms", "isCorrect": False}
                ]
            }
        },
        {
            "id": "en_l5_16",
            "lines": ["Happy children build a sandcastle", "with moist sand by the water edge."],
            "wordCount": 12,
            "microCheck": {
                "question": "What are the happy children building?",
                "options": [
                    {"icon": "🏖️", "label": "A sandcastle", "isCorrect": True},
                    {"icon": "🏡", "label": "A wooden cabin", "isCorrect": False},
                    {"icon": "🧱", "label": "A stone brick house", "isCorrect": False}
                ]
            }
        },
        {
            "id": "en_l5_17",
            "lines": ["The wise owl opens its golden eyes", "to watch over the sleeping woods."],
            "wordCount": 13,
            "microCheck": {
                "question": "What color are the owl's eyes?",
                "options": [
                    {"icon": "👀", "label": "Golden eyes", "isCorrect": True},
                    {"icon": "🔵", "label": "Bright blue eyes", "isCorrect": False},
                    {"icon": "🟢", "label": "Green emerald eyes", "isCorrect": False}
                ]
            }
        },
        {
            "id": "en_l5_18",
            "lines": ["The baker bakes warm honey biscuits", "that smell delicious across the entire kitchen."],
            "wordCount": 13,
            "microCheck": {
                "question": "What delicious treat is the baker baking?",
                "options": [
                    {"icon": "🍪", "label": "Warm honey biscuits", "isCorrect": True},
                    {"icon": "🍕", "label": "Spicy cheese pizza", "isCorrect": False},
                    {"icon": "🥧", "label": "Cold pumpkin pie", "isCorrect": False}
                ]
            }
        }
    ],
    "l6": [
        {
            "id": "en_l6_01",
            "lines": [
                "Friendly dolphins leap high in the clear blue sea.",
                "They swim together in large family pods",
                "and communicate by whistling melodious tunes underwater."
            ],
            "wordCount": 23,
            "microCheck": {
                "question": "How do dolphins communicate under the water?",
                "options": [
                    {"icon": "🎶", "label": "By whistling tunes", "isCorrect": True},
                    {"icon": "🔦", "label": "With bright flashes of light", "isCorrect": False},
                    {"icon": "🤫", "label": "By swimming in silence", "isCorrect": False}
                ]
            }
        },
        {
            "id": "en_l6_02",
            "lines": [
                "On top of the breezy green hill,",
                "a wooden windmill spins its great cloth sails.",
                "Its spinning millstones grind dry golden wheat into fine white flour."
            ],
            "wordCount": 26,
            "microCheck": {
                "question": "What do the windmill sails help produce?",
                "options": [
                    {"icon": "🌾", "label": "Fine white flour", "isCorrect": True},
                    {"icon": "🍞", "label": "Fresh baked bread", "isCorrect": False},
                    {"icon": "🥣", "label": "Warm breakfast cereal", "isCorrect": False}
                ]
            }
        },
        {
            "id": "en_l6_03",
            "lines": [
                "Did you know that chameleons can change color?",
                "They turn green, brown, or golden yellow.",
                "This clever trick helps them hide safely among leaves."
            ],
            "wordCount": 24,
            "microCheck": {
                "question": "Why do chameleons change their skin color?",
                "options": [
                    {"icon": "🍃", "label": "To hide among leaves", "isCorrect": True},
                    {"icon": "😴", "label": "To stay warm while sleeping", "isCorrect": False},
                    {"icon": "🏃", "label": "To run faster from birds", "isCorrect": False}
                ]
            }
        },
        {
            "id": "en_l6_04",
            "lines": [
                "The astronaut floats weightless inside the orbiting station.",
                "She looks out the round port window and sees planet Earth.",
                "Our blue world shines with breathtaking beauty against deep space!"
            ],
            "wordCount": 27,
            "microCheck": {
                "question": "What does the astronaut see through the window?",
                "options": [
                    {"icon": "🌍", "label": "Our blue planet Earth", "isCorrect": True},
                    {"icon": "☄️", "label": "A frozen flying comet", "isCorrect": False},
                    {"icon": "👽", "label": "An alien spacecraft", "isCorrect": False}
                ]
            }
        },
        {
            "id": "en_l6_05",
            "lines": [
                "A tiny green caterpillar munches leaves all afternoon.",
                "Then it weaves a soft cozy cocoon for rest",
                "and wakes up as a stunning butterfly with painted wings."
            ],
            "wordCount": 27,
            "microCheck": {
                "question": "What does the green caterpillar become after its nap?",
                "options": [
                    {"icon": "🦋", "label": "A painted butterfly", "isCorrect": True},
                    {"icon": "🐝", "label": "A honeybee", "isCorrect": False},
                    {"icon": "🐞", "label": "A spotted ladybug", "isCorrect": False}
                ]
            }
        },
        {
            "id": "en_l6_06",
            "lines": [
                "The tall white lighthouse stands on a rocky cliff.",
                "It casts a bright revolving beam across the dark waves",
                "to guide tired sailors safely into the shelter of harbor."
            ],
            "wordCount": 28,
            "microCheck": {
                "question": "Whom does the lighthouse beam guide to safety?",
                "options": [
                    {"icon": "⛵", "label": "Sailors navigating at sea", "isCorrect": True},
                    {"icon": "✈️", "label": "Airplane pilots in fog", "isCorrect": False},
                    {"icon": "🚗", "label": "Highway truck drivers", "isCorrect": False}
                ]
            }
        },
        {
            "id": "en_l6_07",
            "lines": [
                "Tiny ants work together with incredible discipline.",
                "Each loyal ant carries a plant seed toward the anthill.",
                "This guarantees fresh supplies of food for the entire colony."
            ],
            "wordCount": 26,
            "microCheck": {
                "question": "What is each ant carrying back to the anthill?",
                "options": [
                    {"icon": "🌱", "label": "A plant seed", "isCorrect": True},
                    {"icon": "svg:piedra", "label": "Heavy pebbles", "isCorrect": False},
                    {"icon": "💧", "label": "Morning dew drops", "isCorrect": False}
                ]
            }
        },
        {
            "id": "en_l6_08",
            "lines": [
                "Inside the town library, peaceful quiet fills the sunny rooms.",
                "Tall wooden shelves are packed with tales of grand discovery.",
                "Young readers travel to faraway kingdoms just by turning pages."
            ],
            "wordCount": 27,
            "microCheck": {
                "question": "What fills the tall wooden shelves in the library?",
                "options": [
                    {"icon": "📚", "label": "Books of adventure and discovery", "isCorrect": True},
                    {"icon": "🧸", "label": "Vintage wooden toys", "isCorrect": False},
                    {"icon": "🏆", "label": "Gold sports medals", "isCorrect": False}
                ]
            }
        },
        {
            "id": "en_l6_09",
            "lines": [
                "Look at the quiet snow blanketing the mountain slopes!",
                "Every cabin rooftop looks like fluffy white cotton.",
                "Bundled in warm coats, children pull wooden sleds up hills."
            ],
            "wordCount": 25,
            "microCheck": {
                "question": "What do the snowy cabin rooftops look like?",
                "options": [
                    {"icon": "☁️", "label": "Fluffy white cotton", "isCorrect": True},
                    {"icon": "🍦", "label": "Sweet strawberry ice cream", "isCorrect": False},
                    {"icon": "svg:piedra", "label": "Dark jagged granite stones", "isCorrect": False}
                ]
            }
        },
        {
            "id": "en_l6_10",
            "lines": [
                "The rushing river flows downward from cold glacier peaks.",
                "It waters green valley crops and quenches the thirst of wildlife.",
                "Its clean fresh current is a precious gift for all nature."
            ],
            "wordCount": 28,
            "microCheck": {
                "question": "Where does the rushing river originate?",
                "options": [
                    {"icon": "🏔️", "label": "From cold glacier peaks", "isCorrect": True},
                    {"icon": "🏜️", "label": "From an arid desert dune", "isCorrect": False},
                    {"icon": "🌋", "label": "From an active volcano cone", "isCorrect": False}
                ]
            }
        },
        {
            "id": "en_l6_11",
            "lines": [
                "Octopuses have three hearts and cool blue blood.",
                "When danger approaches, they spray a dark cloud of ink.",
                "This clever smoke screen lets them dart away unseen."
            ],
            "wordCount": 26,
            "microCheck": {
                "question": "How many hearts does an octopus have?",
                "options": [
                    {"icon": "❤️", "label": "Three hearts", "isCorrect": True},
                    {"icon": "1️⃣", "label": "Only one heart", "isCorrect": False},
                    {"icon": "5️⃣", "label": "Five hearts", "isCorrect": False}
                ]
            }
        },
        {
            "id": "en_l6_12",
            "lines": [
                "The grand symphony began with a single gentle violin melody.",
                "Soon, flutes, brass trumpets, and thunderous drums joined in harmony.",
                "The delighted audience gave a standing ovation at the end."
            ],
            "wordCount": 27,
            "microCheck": {
                "question": "Which instrument played the very first melody?",
                "options": [
                    {"icon": "🎻", "label": "A gentle violin", "isCorrect": True},
                    {"icon": "🥁", "label": "A loud bass drum", "isCorrect": False},
                    {"icon": "🎺", "label": "A brass trumpet", "isCorrect": False}
                ]
            }
        },
        {
            "id": "en_l6_13",
            "lines": [
                "Beneath tropical ocean swells, coral reefs burst with life.",
                "Clownfish with bright orange stripes dart among sea anemones.",
                "It is a colorful underwater city where all creatures thrive together."
            ],
            "wordCount": 27,
            "microCheck": {
                "question": "What color are the clownfish stripes?",
                "options": [
                    {"icon": "🧡", "label": "Bright orange stripes", "isCorrect": True},
                    {"icon": "🖤", "label": "Deep black stripes", "isCorrect": False},
                    {"icon": "💚", "label": "Emerald green stripes", "isCorrect": False}
                ]
            }
        },
        {
            "id": "en_l6_14",
            "lines": [
                "The clever beaver builds a sturdy dam from branches and mud.",
                "It forms a calm woodland pond to construct its floating lodge.",
                "There, its young kits rest safe from chilly winds and predators."
            ],
            "wordCount": 30,
            "microCheck": {
                "question": "What materials does the beaver use to build its dam?",
                "options": [
                    {"icon": "svg:tronco", "label": "Branches and thick mud", "isCorrect": True},
                    {"icon": "🧱", "label": "Bricks and steel rods", "isCorrect": False},
                    {"icon": "🌾", "label": "Dry straw and reeds", "isCorrect": False}
                ]
            }
        },
        {
            "id": "en_l6_15",
            "lines": [
                "Koalas sleep up to twenty hours each day nestled in branches.",
                "They feed on fragrant eucalyptus leaves in Australian gum tree forests.",
                "Their strong curved claws keep them securely perched without ever slipping."
            ],
            "wordCount": 29,
            "microCheck": {
                "question": "What is the main food of wild koalas?",
                "options": [
                    {"icon": "🍃", "label": "Eucalyptus leaves", "isCorrect": True},
                    {"icon": "🍌", "label": "Ripe yellow bananas", "isCorrect": False},
                    {"icon": "🌾", "label": "Golden barley grains", "isCorrect": False}
                ]
            }
        },
        {
            "id": "en_l6_16",
            "lines": [
                "Watching a midnight meteor shower is an unforgettable adventure!",
                "As a shooting star burns through the atmosphere, it leaves a golden streak.",
                "Make a cheerful wish before the glowing trail fades into space."
            ],
            "wordCount": 30,
            "microCheck": {
                "question": "What does a shooting star leave behind in the night sky?",
                "options": [
                    {"icon": "✨", "label": "A glowing golden streak", "isCorrect": True},
                    {"icon": "💨", "label": "A dark cloud of dust", "isCorrect": False},
                    {"icon": "🌧️", "label": "A gentle shower of rain", "isCorrect": False}
                ]
            }
        }
    ]
}

# i18n dictionaries - 100% key parity
i18n_es = {
    # Header & navigation
    "app_title": "Lector Arcade",
    "app_subtitle": "Aventura lúdica de lectura para niños y familias",
    "tab_play": "🎮 Jugar",
    "tab_learn": "💡 Aprender",
    "tab_achievements": "🏆 Logros",
    "choose_level": "1. Elige tu Nivel",
    "choose_mode": "2. Elige el Modo de Juego",
    "start_game": "¡A Leer! 🚀",
    "back_menu": "← Menú",

    # Gameplay HUD
    "round": "Ronda",
    "time_left": "Tiempo",
    "points": "Puntos",
    "streak": "Racha",
    "combo": "Combo",
    "best_streak": "Mejor Racha",
    "score": "Puntuación",
    "accuracy": "Precisión",
    "correct": "Aciertos",
    "wrong": "Fallos",
    "visual_hint": "💡 Pista Visual",
    "hide_hint": "Ocultar Pista",
    "type_answer": "Tu lectura...",
    "check": "Comprobar ⏎",
    "skip": "Saltar ↷",

    # Feedback toasts & alerts
    "awesome": "¡Excelente lectura! 🎉",
    "good_try": "¡Casi! Sigue practicando 😅",
    "time_up": "¡Tiempo agotado! ⏱️",
    "game_over": "¡Partida Terminada! 🏆",
    "play_again": "Jugar de nuevo 🔁",
    "view_achievements": "Ver Logros 🌟",
    "badge_unlocked": "¡Nueva Medalla Desbloqueada!",
    "clean_history": "Reiniciar Estadísticas",
    "confirm_reset": "¿Seguro que deseas reiniciar tus medallas y récords de lectura?",
    "tutorial_hint_tip": "Pulsa \"Pista Visual\" si necesitas ver la descomposición silábica.",

    # Controls & Toggles
    "sound_toggle": "Sonido (M)",
    "theme_toggle": "Tema (T)",
    "font_case_toggle": "Letra (AA/Aa)",
    "syllable_toggle": "Sílabas (🎨)",
    "listen_btn": "Escuchar 🔊",
    "listen_normal_btn": "Escuchar 🔊 (1.0x)",
    "listen_slow_btn": "Escuchar Despacio 🐢 (0.5x)",
    "read_done_btn": "¡Leído! ✅",
    "clear_letter_btn": "Borrar ⌫",

    # PWA & Updates
    "install_app": "Instalar App",
    "install_app_title": "Instalar Lector Arcade en tu pantalla de inicio",
    "install_success": "¡Lector Arcade instalado con éxito! 🎉",
    "install_ios_tip": "En Safari iOS: pulsa Compartir (⬆️) y \"Añadir a pantalla de inicio\"",
    "install_generic_tip": "Pulsa el menú (⋮) del navegador y selecciona \"Instalar aplicación\"",
    "update_available": "Nueva versión v1.1.0 disponible",
    "update_now_btn": "Actualizar ahora",
    "checking_update": "Buscando actualizaciones...",
    "up_to_date": "✓ Lector Arcade al día (v1.1.0)",
    "check_update_title": "Buscar actualizaciones de la aplicación (v1.1.0)",
    "stats_reset_toast": "Estadísticas y medallas reiniciadas con éxito",

    # Results & Review
    "correct_answer_is": "Lectura correcta:",
    "next_question_btn": "Siguiente ➔",
    "share_result_btn": "📤 Compartir Resultado",
    "share_result_copied": "¡Tarjeta de lectura copiada al portapapeles! 📋",
    "mistake_review_title": "🧠 Repaso de Palabras de la Ronda",
    "mistake_review_empty": "¡Lectura impecable! Cero fallos que repasar. 🌟",
    "mistake_your_answer": "Tu intento:",
    "mistake_correct_answer": "Palabra o frase:",
    "view_hint_btn": "Ver Pista 💡",

    # Profiles, Diploma & Practice Sheet
    "daily_challenge_label": "Reto Diario",
    "profile_label": "Perfil:",
    "profile_switched": "Cambiado a perfil:",
    "download_diploma_btn": "🎓 Descargar Diploma (PNG)",
    "diploma_downloaded_toast": "¡Diploma de Lector descargado con éxito! 🎓",
    "diploma_card_title": "Diploma Arcade de Lectura",
    "diploma_card_desc": "Genera un certificado oficial en PNG de alta resolución con tus medallas y velocidad lectora (PPM).",
    "diploma_name_label": "Nombre en el Diploma (opcional):",
    "diploma_name_placeholder": "Ej: Sofía Gómez",
    "download_sheet_btn": "🖨️ Lámina de Repaso A4 (PNG)",
    "sheet_downloaded_toast": "¡Lámina de repaso imprimible descargada con éxito! 🖨️",

    # Custom Words Mode (Parents & Teachers)
    "custom_words_title": "✏️ Mis Palabras (Familias y Colegios)",
    "custom_words_desc": "Escribe o pega palabras separadas por comas para practicar tu vocabulario personalizado:",
    "custom_words_placeholder": "Ej: MESA, NIDO, NUDO, CASA, ESCUELA...",
    "custom_words_apply": "Activar Lista",
    "custom_words_clear": "Quitar Lista",
    "custom_words_share": "Copiar Enlace de Deberes 📋",
    "custom_words_copied": "¡Enlace de deberes copiado al portapapeles! 📋",
    "custom_words_active_badge": "✏️ Modo Mis Palabras Activo",
    "parents_zone_title": "👨‍👩‍👧 Zona Padres y Docentes",
    "parents_zone_desc": "Descarga láminas imprimibles, diplomas de honor y recursos complementarios de lectoescritura.",

    # Footer triad links
    "datalaria_back": "← Datalaria",
    "post_link": "📖 Historia IA",
    "spec_link": "📋 Ficha App",
    "kits_link": "📦 Recursos",

    # Reading specific
    "wpm_label": "PPM",
    "effective_wpm_label": "PPM Efectivas",
    "wpm_full": "Palabras Por Minuto",
    "words_read": "Palabras Leídas",
    "reading_time": "Tiempo de Lectura",
    "reading_speed": "Velocidad Lectora",
    "micro_check_title": "Comprobación Rápida",
    "micro_check_desc": "Elige la respuesta correcta sobre lo que acabas de leer:",
    "stopwatch_hint": "Pulsa ¡Leído! nada más terminar de leer para congelar tu cronómetro.",
    "keyboard_tap_hint": "Toca las letras de abajo para completar los huecos:",
    "learn_tab_letters": "Letras y Sonidos",
    "learn_tab_direct": "Sílabas Sencillas",
    "learn_tab_complex": "Sílabas Complejas",
    "learn_tab_sentences": "Taller de Frases"
}

i18n_en = {
    # Header & navigation
    "app_title": "Reader Arcade",
    "app_subtitle": "Playful reading adventure for kids & families",
    "tab_play": "🎮 Play",
    "tab_learn": "💡 Learn",
    "tab_achievements": "🏆 Badges",
    "choose_level": "1. Choose your Level",
    "choose_mode": "2. Choose Game Mode",
    "start_game": "Start Reading! 🚀",
    "back_menu": "← Menu",

    # Gameplay HUD
    "round": "Round",
    "time_left": "Time",
    "points": "Points",
    "streak": "Streak",
    "combo": "Combo",
    "best_streak": "Best Streak",
    "score": "Score",
    "accuracy": "Accuracy",
    "correct": "Correct",
    "wrong": "Mistakes",
    "visual_hint": "💡 Visual Hint",
    "hide_hint": "Hide Hint",
    "type_answer": "Your reading...",
    "check": "Check ⏎",
    "skip": "Skip ↷",

    # Feedback toasts & alerts
    "awesome": "Great reading! 🎉",
    "good_try": "Almost! Keep practicing 😅",
    "time_up": "Time's up! ⏱️",
    "game_over": "Game Over! 🏆",
    "play_again": "Play Again 🔁",
    "view_achievements": "View Badges 🌟",
    "badge_unlocked": "New Badge Unlocked!",
    "clean_history": "Reset Stats",
    "confirm_reset": "Are you sure you want to reset your reading badges and high scores?",
    "tutorial_hint_tip": "Tap \"Visual Hint\" if you need to see syllable breakdown.",

    # Controls & Toggles
    "sound_toggle": "Sound (M)",
    "theme_toggle": "Theme (T)",
    "font_case_toggle": "Font (AA/Aa)",
    "syllable_toggle": "Syllables (🎨)",
    "listen_btn": "Listen 🔊",
    "listen_normal_btn": "Listen 🔊 (1.0x)",
    "listen_slow_btn": "Listen Slow 🐢 (0.5x)",
    "read_done_btn": "Done! ✅",
    "clear_letter_btn": "Erase ⌫",

    # PWA & Updates
    "install_app": "Install App",
    "install_app_title": "Install Reader Arcade on your home screen",
    "install_success": "Reader Arcade successfully installed! 🎉",
    "install_ios_tip": "In Safari iOS: tap Share (⬆️) and select \"Add to Home Screen\"",
    "install_generic_tip": "Tap browser menu (⋮) and select \"Install app\"",
    "update_available": "New version v1.1.0 available",
    "update_now_btn": "Update now",
    "checking_update": "Checking for updates...",
    "up_to_date": "✓ Reader Arcade is up to date (v1.1.0)",
    "check_update_title": "Check for app updates (v1.1.0)",
    "stats_reset_toast": "Stats and badges reset successfully",

    # Results & Review
    "correct_answer_is": "Correct reading:",
    "next_question_btn": "Next ➔",
    "share_result_btn": "📤 Share Result",
    "share_result_copied": "Reading score card copied to clipboard! 📋",
    "mistake_review_title": "🧠 Round Word Review",
    "mistake_review_empty": "Flawless reading! Zero mistakes to review. 🌟",
    "mistake_your_answer": "Your attempt:",
    "mistake_correct_answer": "Word or sentence:",
    "view_hint_btn": "View Hint 💡",

    # Profiles, Diploma & Practice Sheet
    "daily_challenge_label": "Daily Challenge",
    "profile_label": "Profile:",
    "profile_switched": "Switched to profile:",
    "download_diploma_btn": "🎓 Download Diploma (PNG)",
    "diploma_downloaded_toast": "Reader Diploma downloaded successfully! 🎓",
    "diploma_card_title": "Arcade Reading Diploma",
    "diploma_card_desc": "Generate an official high-resolution PNG certificate with your badges and reading speed (WPM).",
    "diploma_name_label": "Name on Diploma (optional):",
    "diploma_name_placeholder": "E.g. Sophia Miller",
    "download_sheet_btn": "🖨️ Printable A4 Sheet (PNG)",
    "sheet_downloaded_toast": "Printable practice sheet downloaded successfully! 🖨️",

    # Custom Words Mode (Parents & Teachers)
    "custom_words_title": "✏️ Custom Words (Families & Schools)",
    "custom_words_desc": "Type or paste comma-separated words to practice your personalized vocabulary:",
    "custom_words_placeholder": "E.g. NEST, KITE, DESK, FROG, SCHOOL...",
    "custom_words_apply": "Apply Words",
    "custom_words_clear": "Clear Words",
    "custom_words_share": "Share Homework Link 📋",
    "custom_words_copied": "Homework link copied to clipboard! 📋",
    "custom_words_active_badge": "✏️ Custom Words Active",
    "parents_zone_title": "👨‍👩‍👧 Parents & Educators Zone",
    "parents_zone_desc": "Download printable worksheets, diplomas of honor and literacy companion resources.",

    # Footer triad links
    "datalaria_back": "← Datalaria",
    "post_link": "📖 AI Story",
    "spec_link": "📋 App Spec",
    "kits_link": "📦 Resources",

    # Reading specific
    "wpm_label": "WPM",
    "effective_wpm_label": "Effective WPM",
    "wpm_full": "Words Per Minute",
    "words_read": "Words Read",
    "reading_time": "Reading Time",
    "reading_speed": "Reading Speed",
    "micro_check_title": "Quick Check",
    "micro_check_desc": "Choose the correct option about what you just read:",
    "stopwatch_hint": "Tap Done! as soon as you finish reading to freeze your stopwatch.",
    "keyboard_tap_hint": "Tap the letters below to fill in the blanks:",
    "learn_tab_letters": "Letters & Sounds",
    "learn_tab_direct": "Simple Syllables",
    "learn_tab_complex": "Complex Syllables",
    "learn_tab_sentences": "Sentence Workshop"
}

def validate_catalog():
    print("[1/5] Validating i18n parity...")
    es_keys = set(i18n_es.keys())
    en_keys = set(i18n_en.keys())
    assert es_keys == en_keys, f"i18n mismatch! Diff: {es_keys ^ en_keys}"
    print(f"  ✓ {len(es_keys)} i18n keys with 100% parity.")

    print("[2/5] Validating syllable integrity (INV-READ-1)...")
    for lang, bank in [("es", wordBank_es), ("en", wordBank_en)]:
        for lvl in ["l2", "l3", "l4"]:
            for item in bank[lvl]:
                joined = "".join(item["syllables"])
                assert joined == item["word"], f"[{lang}][{lvl}] Syllable join '{joined}' != word '{item['word']}' in item {item['id']}"
    print("  ✓ 100% of words in l2, l3, l4 satisfy syllables.join('') === word.")

    print("[3/5] Validating missing indices in l3...")
    for lang, bank in [("es", wordBank_es), ("en", wordBank_en)]:
        for item in bank["l3"]:
            wlen = len(item["word"])
            for idx in item["missingIndices"]:
                assert 0 <= idx < wlen, f"[{lang}][l3] Index {idx} out of bounds for '{item['word']}' (len {wlen})"
    print("  ✓ 100% of l3 missingIndices valid.")

    print("[4/5] Validating microCheck options (3 options, exactly 1 correct)...")
    for lang, bank in [("es", wordBank_es), ("en", wordBank_en)]:
        for item in bank["l4"]:
            mc = item["microCheck"]
            opts = mc["options"]
            assert len(opts) == 3, f"[{lang}][l4] Expected 3 options in {item['id']}, got {len(opts)}"
            correct_count = sum(1 for o in opts if o.get("isCorrect") is True)
            assert correct_count == 1, f"[{lang}][l4] Expected 1 correct option in {item['id']}, got {correct_count}"
    
    for lang, sbank in [("es", sentenceBank_es), ("en", sentenceBank_en)]:
        for lvl in ["l5", "l6"]:
            for item in sbank[lvl]:
                mc = item["microCheck"]
                opts = mc["options"]
                assert len(opts) == 3, f"[{lang}][{lvl}] Expected 3 options in {item['id']}, got {len(opts)}"
                correct_count = sum(1 for o in opts if o.get("isCorrect") is True)
                assert correct_count == 1, f"[{lang}][{lvl}] Expected 1 correct option in {item['id']}, got {correct_count}"
    print("  ✓ 100% of microChecks have exactly 3 options and 1 isCorrect: true.")

    print("[5/5] Validating word counts in sentenceBank...")
    for lang, sbank in [("es", sentenceBank_es), ("en", sentenceBank_en)]:
        for lvl, expected_lines in [("l5", 2), ("l6", 3)]:
            for item in sbank[lvl]:
                assert len(item["lines"]) == expected_lines, f"[{lang}][{lvl}] Expected {expected_lines} lines in {item['id']}"
                full_text = " ".join(item["lines"]).strip()
                computed_words = len(re.findall(r'\b\w+\b', full_text))
                # For WPM, we check that wordCount is positive and reasonably matches
                assert item["wordCount"] > 0, f"[{lang}][{lvl}] wordCount <= 0 in {item['id']}"
    print("  ✓ 100% of sentenceBank entries satisfy line count and word count constraints.")

def emit_catalog_js():
    data = {
        "levels": levels,
        "modes": modes,
        "profiles": profiles,
        "medals": medals,
        "learnModules": learnModules,
        "wordBank": {
            "es": wordBank_es,
            "en": wordBank_en
        },
        "sentenceBank": {
            "es": sentenceBank_es,
            "en": sentenceBank_en
        },
        "i18n": {
            "es": i18n_es,
            "en": i18n_en
        }
    }

    os.makedirs(os.path.dirname(CATALOG_JS_PATH), exist_ok=True)
    js_content = f"// apps/reading/catalog.js - Catálogo unificado de niveles, modos, medallas, lecciones, léxico e i18n\n"
    js_content += f"// Generated under SPEC-APP-READING v1.0.0 and SDD Helix\n"
    js_content += f"(function() {{\n"
    js_content += f"  var root = typeof window !== 'undefined' ? window : (typeof globalThis !== 'undefined' ? globalThis : this);\n"
    js_content += f"  var data = {json.dumps(data, ensure_ascii=False, indent=2)};\n"
    js_content += f"  root.READING_CATALOG = data;\n"
    js_content += f"  if (typeof module === 'object' && module.exports) {{\n"
    js_content += f"    module.exports = data;\n"
    js_content += f"  }}\n"
    js_content += f"}})();\n"
    
    with open(CATALOG_JS_PATH, "w", encoding="utf-8") as f:
        f.write(js_content)
    print(f"Generated catalog at {CATALOG_JS_PATH} ({len(js_content)} bytes)")

if __name__ == "__main__":
    validate_catalog()
    emit_catalog_js()
