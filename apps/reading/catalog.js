// apps/reading/catalog.js - Catálogo unificado de niveles, modos, medallas, lecciones, léxico e i18n
// Generated under SPEC-APP-READING v1.0.0 and SDD Helix
window.READING_CATALOG = {
  "levels": [
    {
      "id": "l1",
      "icon": "🌱",
      "range": "4-5",
      "name": {
        "es": "Nivel 1: Primeras Letras y Sílabas",
        "en": "Level 1: First Letters & Syllables"
      },
      "desc": {
        "es": "Reconocimiento de vocales, consonantes y sílabas iniciales",
        "en": "Vowel, consonant and initial syllable recognition"
      }
    },
    {
      "id": "l2",
      "icon": "🖼️",
      "range": "5-6",
      "name": {
        "es": "Nivel 2: Palabra con Imagen",
        "en": "Level 2: Word with Picture"
      },
      "desc": {
        "es": "Palabras bisílabas directas con apoyo visual",
        "en": "Direct two-syllable words with visual support"
      }
    },
    {
      "id": "l3",
      "icon": "🧩",
      "range": "6-7",
      "name": {
        "es": "Nivel 3: Letras Faltantes",
        "en": "Level 3: Missing Letters"
      },
      "desc": {
        "es": "Completa las letras que faltan con el teclado táctil",
        "en": "Fill in missing letters using touch keyboard"
      }
    },
    {
      "id": "l4",
      "icon": "🚀",
      "range": "7-8",
      "name": {
        "es": "Nivel 4: Lectura Sin Ayuda",
        "en": "Level 4: Independent Words"
      },
      "desc": {
        "es": "Palabras complejas, sílabas trabadas y micro-comprobación",
        "en": "Complex words, blends and instant micro-check"
      }
    },
    {
      "id": "l5",
      "icon": "📖",
      "range": "8-9",
      "name": {
        "es": "Nivel 5: Frases de 2 Líneas",
        "en": "Level 5: 2-Line Stories"
      },
      "desc": {
        "es": "Lectura fluida de oraciones y preguntas de comprensión",
        "en": "Fluent sentence reading and comprehension questions"
      }
    },
    {
      "id": "l6",
      "icon": "🏆",
      "range": "9-11",
      "name": {
        "es": "Nivel 6: Mini-Relatos",
        "en": "Level 6: Mini-Stories"
      },
      "desc": {
        "es": "Párrafos de 3 líneas, signos de puntuación y reto inferencial",
        "en": "3-line paragraphs, punctuation and inferential challenge"
      }
    }
  ],
  "modes": [
    {
      "id": "normal",
      "icon": "🧘",
      "name": {
        "es": "Modo Normal",
        "en": "Normal Mode"
      },
      "desc": {
        "es": "Sin reloj ni estrés. Pistas visuales libres para aprender.",
        "en": "No timer, no stress. Free visual hints for learning."
      }
    },
    {
      "id": "stopwatch",
      "icon": "⏱️",
      "name": {
        "es": "Contrarreloj Lector",
        "en": "Reading Stopwatch"
      },
      "desc": {
        "es": "Mide tus palabras por minuto (PPM) con cierre instantáneo al leer.",
        "en": "Measure your words per minute (WPM) with instant freeze upon reading."
      }
    },
    {
      "id": "sprint",
      "icon": "⚡",
      "name": {
        "es": "Sprint 60s",
        "en": "Sprint 60s"
      },
      "desc": {
        "es": "¡1 minuto a tope! Cada 5 aciertos seguidos suman +3s.",
        "en": "1 minute rush! Every 5 streak answers add +3s."
      }
    },
    {
      "id": "daily",
      "icon": "📅",
      "name": {
        "es": "Reto Diario",
        "en": "Daily Challenge"
      },
      "desc": {
        "es": "10 retos únicos al día idénticos para todos con tarjeta compartible.",
        "en": "10 daily unique challenges identical for everyone with shareable card."
      }
    }
  ],
  "profiles": [
    {
      "id": "player_1",
      "avatar": "🦁",
      "name": {
        "es": "Jugador 1",
        "en": "Player 1"
      },
      "title": {
        "es": "León Lector",
        "en": "Reading Lion"
      }
    },
    {
      "id": "player_2",
      "avatar": "🦊",
      "name": {
        "es": "Jugador 2",
        "en": "Player 2"
      },
      "title": {
        "es": "Zorro Audaz",
        "en": "Swift Fox"
      }
    },
    {
      "id": "adult",
      "avatar": "🦉",
      "name": {
        "es": "Adulto",
        "en": "Adult"
      },
      "title": {
        "es": "Búho Sabio",
        "en": "Wise Owl"
      }
    }
  ],
  "medals": [
    {
      "id": "first_win",
      "icon": "🌟",
      "name": {
        "es": "Primer Vuelo",
        "en": "First Flight"
      },
      "desc": {
        "es": "Completa tu primera partida de lectura con éxito",
        "en": "Complete your first successful reading game"
      }
    },
    {
      "id": "streak_5",
      "icon": "🔥",
      "name": {
        "es": "Fuego x5",
        "en": "Fire x5"
      },
      "desc": {
        "es": "Consigue una racha de 5 aciertos seguidos",
        "en": "Get a streak of 5 correct answers"
      }
    },
    {
      "id": "streak_10",
      "icon": "⚡",
      "name": {
        "es": "Rayo x10",
        "en": "Lightning x10"
      },
      "desc": {
        "es": "Alcanza una racha perfecta de 10 aciertos",
        "en": "Reach a perfect 10 answer streak"
      }
    },
    {
      "id": "syllable_master",
      "icon": "🧩",
      "name": {
        "es": "Mago Silábico",
        "en": "Syllable Wizard"
      },
      "desc": {
        "es": "Completa el Nivel 3 o 4 sin cometer ningún error",
        "en": "Complete Level 3 or 4 without any mistakes"
      }
    },
    {
      "id": "speed_reader",
      "icon": "⏱️",
      "name": {
        "es": "Lector Sónico",
        "en": "Sonic Reader"
      },
      "desc": {
        "es": "Supera las 120 Palabras Por Minuto (PPM) en una ronda",
        "en": "Exceed 120 Words Per Minute (WPM) in a round"
      }
    },
    {
      "id": "storyteller",
      "icon": "🏆",
      "name": {
        "es": "Gran Cuentacuentos",
        "en": "Master Storyteller"
      },
      "desc": {
        "es": "Supera el Nivel 5 o 6 con comprensión perfecta (100%)",
        "en": "Pass Level 5 or 6 with 100% comprehension"
      }
    }
  ],
  "learnModules": {
    "es": {
      "letters": [
        {
          "letter": "A",
          "sound": "a",
          "anchor": "Abeja",
          "emoji": "🐝"
        },
        {
          "letter": "E",
          "sound": "e",
          "anchor": "Elefante",
          "emoji": "🐘"
        },
        {
          "letter": "I",
          "sound": "i",
          "anchor": "Isla",
          "emoji": "🏝️"
        },
        {
          "letter": "O",
          "sound": "o",
          "anchor": "Oso",
          "emoji": "🐻"
        },
        {
          "letter": "U",
          "sound": "u",
          "anchor": "Uvas",
          "emoji": "🍇"
        },
        {
          "letter": "M",
          "sound": "eme",
          "anchor": "Manzana",
          "emoji": "🍎"
        },
        {
          "letter": "P",
          "sound": "pe",
          "anchor": "Pato",
          "emoji": "🦆"
        },
        {
          "letter": "S",
          "sound": "ese",
          "anchor": "Sol",
          "emoji": "☀️"
        },
        {
          "letter": "L",
          "sound": "ele",
          "anchor": "Luna",
          "emoji": "🌙"
        },
        {
          "letter": "T",
          "sound": "te",
          "anchor": "Tomate",
          "emoji": "🍅"
        },
        {
          "letter": "D",
          "sound": "de",
          "anchor": "Dado",
          "emoji": "🎲"
        },
        {
          "letter": "N",
          "sound": "ene",
          "anchor": "Nido",
          "emoji": "🪺"
        },
        {
          "letter": "F",
          "sound": "efe",
          "anchor": "Foca",
          "emoji": "🦭"
        },
        {
          "letter": "B",
          "sound": "be",
          "anchor": "Barco",
          "emoji": "⛵"
        },
        {
          "letter": "C",
          "sound": "ce",
          "anchor": "Casa",
          "emoji": "🏠"
        },
        {
          "letter": "R",
          "sound": "erre",
          "anchor": "Ratón",
          "emoji": "🐭"
        },
        {
          "letter": "G",
          "sound": "ge",
          "anchor": "Gato",
          "emoji": "🐱"
        },
        {
          "letter": "J",
          "sound": "jota",
          "anchor": "Jirafa",
          "emoji": "🦒"
        },
        {
          "letter": "V",
          "sound": "uve",
          "anchor": "Vaca",
          "emoji": "🐄"
        },
        {
          "letter": "Z",
          "sound": "zeta",
          "anchor": "Zapato",
          "emoji": "👟"
        },
        {
          "letter": "Ñ",
          "sound": "eñe",
          "anchor": "Ñandú",
          "emoji": "🦤"
        }
      ],
      "directSyllables": [
        {
          "consonant": "M",
          "syllables": [
            {
              "syllable": "MA",
              "word": "Mano",
              "emoji": "✋"
            },
            {
              "syllable": "ME",
              "word": "Mesa",
              "emoji": "🪑"
            },
            {
              "syllable": "MI",
              "word": "Miel",
              "emoji": "🍯"
            },
            {
              "syllable": "MO",
              "word": "Moto",
              "emoji": "🛵"
            },
            {
              "syllable": "MU",
              "word": "Muela",
              "emoji": "🦷"
            }
          ]
        },
        {
          "consonant": "P",
          "syllables": [
            {
              "syllable": "PA",
              "word": "Pato",
              "emoji": "🦆"
            },
            {
              "syllable": "PE",
              "word": "Pelo",
              "emoji": "💇"
            },
            {
              "syllable": "PI",
              "word": "Pino",
              "emoji": "🌲"
            },
            {
              "syllable": "PO",
              "word": "Pozo",
              "emoji": "🪣"
            },
            {
              "syllable": "PU",
              "word": "Puente",
              "emoji": "🌉"
            }
          ]
        },
        {
          "consonant": "S",
          "syllables": [
            {
              "syllable": "SA",
              "word": "Sapo",
              "emoji": "🐸"
            },
            {
              "syllable": "SE",
              "word": "Seta",
              "emoji": "🍄"
            },
            {
              "syllable": "SI",
              "word": "Silla",
              "emoji": "🪑"
            },
            {
              "syllable": "SO",
              "word": "Sopa",
              "emoji": "🍲"
            },
            {
              "syllable": "SU",
              "word": "Suma",
              "emoji": "➕"
            }
          ]
        },
        {
          "consonant": "L",
          "syllables": [
            {
              "syllable": "LA",
              "word": "Lana",
              "emoji": "🧶"
            },
            {
              "syllable": "LE",
              "word": "León",
              "emoji": "🦁"
            },
            {
              "syllable": "LI",
              "word": "Limón",
              "emoji": "🍋"
            },
            {
              "syllable": "LO",
              "word": "Lobo",
              "emoji": "🐺"
            },
            {
              "syllable": "LU",
              "word": "Luna",
              "emoji": "🌙"
            }
          ]
        },
        {
          "consonant": "T",
          "syllables": [
            {
              "syllable": "TA",
              "word": "Taza",
              "emoji": "🍵"
            },
            {
              "syllable": "TE",
              "word": "Tela",
              "emoji": "🧵"
            },
            {
              "syllable": "TI",
              "word": "Tigre",
              "emoji": "🐯"
            },
            {
              "syllable": "TO",
              "word": "Toro",
              "emoji": "🐂"
            },
            {
              "syllable": "TU",
              "word": "Tubo",
              "emoji": "🧪"
            }
          ]
        },
        {
          "consonant": "D",
          "syllables": [
            {
              "syllable": "DA",
              "word": "Dado",
              "emoji": "🎲"
            },
            {
              "syllable": "DE",
              "word": "Dedo",
              "emoji": "☝️"
            },
            {
              "syllable": "DI",
              "word": "Diente",
              "emoji": "🦷"
            },
            {
              "syllable": "DO",
              "word": "Dominó",
              "emoji": "🁛"
            },
            {
              "syllable": "DU",
              "word": "Ducha",
              "emoji": "🚿"
            }
          ]
        },
        {
          "consonant": "N",
          "syllables": [
            {
              "syllable": "NA",
              "word": "Naranja",
              "emoji": "🍊"
            },
            {
              "syllable": "NE",
              "word": "Nieve",
              "emoji": "❄️"
            },
            {
              "syllable": "NI",
              "word": "Nido",
              "emoji": "🪺"
            },
            {
              "syllable": "NO",
              "word": "Noche",
              "emoji": "🌃"
            },
            {
              "syllable": "NU",
              "word": "Nube",
              "emoji": "☁️"
            }
          ]
        },
        {
          "consonant": "F",
          "syllables": [
            {
              "syllable": "FA",
              "word": "Faro",
              "emoji": "🗼"
            },
            {
              "syllable": "FE",
              "word": "Feliz",
              "emoji": "😄"
            },
            {
              "syllable": "FI",
              "word": "Fila",
              "emoji": "🚶"
            },
            {
              "syllable": "FO",
              "word": "Foca",
              "emoji": "🦭"
            },
            {
              "syllable": "FU",
              "word": "Fuego",
              "emoji": "🔥"
            }
          ]
        },
        {
          "consonant": "B",
          "syllables": [
            {
              "syllable": "BA",
              "word": "Barco",
              "emoji": "⛵"
            },
            {
              "syllable": "BE",
              "word": "Bebé",
              "emoji": "👶"
            },
            {
              "syllable": "BI",
              "word": "Bici",
              "emoji": "🚲"
            },
            {
              "syllable": "BO",
              "word": "Bota",
              "emoji": "👢"
            },
            {
              "syllable": "BU",
              "word": "Búho",
              "emoji": "🦉"
            }
          ]
        },
        {
          "consonant": "C",
          "syllables": [
            {
              "syllable": "CA",
              "word": "Casa",
              "emoji": "🏠"
            },
            {
              "syllable": "CO",
              "word": "Copa",
              "emoji": "🏆"
            },
            {
              "syllable": "CU",
              "word": "Cuna",
              "emoji": "🛏️"
            }
          ]
        },
        {
          "consonant": "R",
          "syllables": [
            {
              "syllable": "RA",
              "word": "Rana",
              "emoji": "🐸"
            },
            {
              "syllable": "RE",
              "word": "Reloj",
              "emoji": "⏰"
            },
            {
              "syllable": "RI",
              "word": "Río",
              "emoji": "🏞️"
            },
            {
              "syllable": "RO",
              "word": "Rosa",
              "emoji": "🌹"
            },
            {
              "syllable": "RU",
              "word": "Rueda",
              "emoji": "🛞"
            }
          ]
        }
      ],
      "inverseSyllables": [
        {
          "group": "-L",
          "syllables": [
            {
              "syllable": "AL",
              "word": "Alto",
              "emoji": "🦒"
            },
            {
              "syllable": "EL",
              "word": "Elfo",
              "emoji": "🧝"
            },
            {
              "syllable": "OL",
              "word": "Olla",
              "emoji": "🍲"
            },
            {
              "syllable": "UL",
              "word": "Último",
              "emoji": "🏁"
            }
          ]
        },
        {
          "group": "-S",
          "syllables": [
            {
              "syllable": "AS",
              "word": "Astro",
              "emoji": "⭐"
            },
            {
              "syllable": "ES",
              "word": "Escuela",
              "emoji": "🏫"
            },
            {
              "syllable": "IS",
              "word": "Isla",
              "emoji": "🏝️"
            },
            {
              "syllable": "OS",
              "word": "Ostra",
              "emoji": "🦪"
            }
          ]
        },
        {
          "group": "-R",
          "syllables": [
            {
              "syllable": "AR",
              "word": "Árbol",
              "emoji": "🌳"
            },
            {
              "syllable": "ER",
              "word": "Erizo",
              "emoji": "🦔"
            },
            {
              "syllable": "OR",
              "word": "Orquesta",
              "emoji": "🎻"
            },
            {
              "syllable": "UR",
              "word": "Urna",
              "emoji": "🗳️"
            }
          ]
        },
        {
          "group": "-N",
          "syllables": [
            {
              "syllable": "AN",
              "word": "Antena",
              "emoji": "📡"
            },
            {
              "syllable": "EN",
              "word": "Enano",
              "emoji": "🧙"
            },
            {
              "syllable": "IN",
              "word": "Indio",
              "emoji": "🏹"
            },
            {
              "syllable": "ON",
              "word": "Onda",
              "emoji": "🌊"
            }
          ]
        }
      ],
      "complexSyllables": [
        {
          "prefix": "PL-",
          "syllable": "PLA",
          "word": "Plátano",
          "emoji": "🍌"
        },
        {
          "prefix": "BR-",
          "syllable": "BRA",
          "word": "Brazo",
          "emoji": "💪"
        },
        {
          "prefix": "TR-",
          "syllable": "TRA",
          "word": "Tractor",
          "emoji": "🚜"
        },
        {
          "prefix": "CR-",
          "syllable": "CRA",
          "word": "Crayón",
          "emoji": "🖍️"
        },
        {
          "prefix": "FR-",
          "syllable": "FRA",
          "word": "Fresa",
          "emoji": "🍓"
        },
        {
          "prefix": "GR-",
          "syllable": "GRA",
          "word": "Granja",
          "emoji": "🚜"
        },
        {
          "prefix": "DR-",
          "syllable": "DRA",
          "word": "Dragón",
          "emoji": "🐉"
        },
        {
          "prefix": "BL-",
          "syllable": "BLA",
          "word": "Blanco",
          "emoji": "⬜"
        }
      ],
      "rulesAndDigraphs": [
        {
          "id": "ch",
          "symbol": "CH",
          "rule": "Suena 'che' suave como en Chocolate 🍫",
          "words": [
            "Choza",
            "Chapa",
            "Chaqueta"
          ]
        },
        {
          "id": "ll",
          "symbol": "LL",
          "rule": "Doble ele, suena como en Lluvia 🌧️ o Llave 🗝️",
          "words": [
            "Llama",
            "Llorar",
            "Lleno"
          ]
        },
        {
          "id": "rr",
          "symbol": "RR",
          "rule": "Sonido fuerte entre vocales como en Perro 🐶",
          "words": [
            "Carro",
            "Torre",
            "Tierra"
          ]
        },
        {
          "id": "qu",
          "symbol": "QU",
          "rule": "Siempre va con E o I: QUE, QUI como en Queso 🧀",
          "words": [
            "Química",
            "Quince",
            "Paquete"
          ]
        },
        {
          "id": "gue",
          "symbol": "GUE / GUI",
          "rule": "La U no suena, da sonido suave a la G: Guitarra 🎸",
          "words": [
            "Guepardo",
            "Águila",
            "Guinda"
          ]
        },
        {
          "id": "ce",
          "symbol": "CE / CI",
          "rule": "La C suena suave como la Z: Circo 🎪 o Cebra 🦓",
          "words": [
            "Cine",
            "Cerezas",
            "Cepillo"
          ]
        },
        {
          "id": "n_tilde",
          "symbol": "Ñ",
          "rule": "Letra única del español: Montaña ⛰️ y Piña 🍍",
          "words": [
            "Ñandú",
            "Cabaña",
            "Muñeca"
          ]
        }
      ],
      "sentenceWorkshop": [
        {
          "sign": "Coma (,)",
          "tip": "Haz una pausa breve para tomar aire.",
          "example": "El gato corre, salta y juega."
        },
        {
          "sign": "Punto (.)",
          "tip": "Pausa más larga. La idea ha terminado.",
          "example": "El perro duerme al sol."
        },
        {
          "sign": "Pregunta (¿?)",
          "tip": "Sube el tono al final como una melodía.",
          "example": "¿Dónde está la pelota?"
        },
        {
          "sign": "Exclamación (¡!)",
          "tip": "Pon entusiasmo, sorpresa o alegría en tu voz.",
          "example": "¡Qué golazo tan increíble!"
        }
      ]
    },
    "en": {
      "letters": [
        {
          "letter": "A",
          "sound": "/æ/",
          "anchor": "Apple",
          "emoji": "🍎"
        },
        {
          "letter": "B",
          "sound": "/b/",
          "anchor": "Bear",
          "emoji": "🐻"
        },
        {
          "letter": "C",
          "sound": "/k/",
          "anchor": "Cat",
          "emoji": "🐱"
        },
        {
          "letter": "D",
          "sound": "/d/",
          "anchor": "Dog",
          "emoji": "🐶"
        },
        {
          "letter": "E",
          "sound": "/e/",
          "anchor": "Elephant",
          "emoji": "🐘"
        },
        {
          "letter": "F",
          "sound": "/f/",
          "anchor": "Fish",
          "emoji": "🐟"
        },
        {
          "letter": "G",
          "sound": "/g/",
          "anchor": "Goat",
          "emoji": "🐐"
        },
        {
          "letter": "H",
          "sound": "/h/",
          "anchor": "Hat",
          "emoji": "🎩"
        },
        {
          "letter": "I",
          "sound": "/ɪ/",
          "anchor": "Igloo",
          "emoji": "🛖"
        },
        {
          "letter": "J",
          "sound": "/dʒ/",
          "anchor": "Jug",
          "emoji": "🏺"
        },
        {
          "letter": "K",
          "sound": "/k/",
          "anchor": "Kite",
          "emoji": "🪁"
        },
        {
          "letter": "L",
          "sound": "/l/",
          "anchor": "Lion",
          "emoji": "🦁"
        },
        {
          "letter": "M",
          "sound": "/m/",
          "anchor": "Moon",
          "emoji": "🌙"
        },
        {
          "letter": "N",
          "sound": "/n/",
          "anchor": "Nest",
          "emoji": "🪺"
        },
        {
          "letter": "O",
          "sound": "/ɒ/",
          "anchor": "Octopus",
          "emoji": "🐙"
        },
        {
          "letter": "P",
          "sound": "/p/",
          "anchor": "Pig",
          "emoji": "🐷"
        },
        {
          "letter": "Q",
          "sound": "/kw/",
          "anchor": "Queen",
          "emoji": "👑"
        },
        {
          "letter": "R",
          "sound": "/r/",
          "anchor": "Ring",
          "emoji": "💍"
        },
        {
          "letter": "S",
          "sound": "/s/",
          "anchor": "Sun",
          "emoji": "☀️"
        },
        {
          "letter": "T",
          "sound": "/t/",
          "anchor": "Tree",
          "emoji": "🌳"
        },
        {
          "letter": "U",
          "sound": "/ʌ/",
          "anchor": "Umbrella",
          "emoji": "☂️"
        },
        {
          "letter": "V",
          "sound": "/v/",
          "anchor": "Van",
          "emoji": "🚐"
        },
        {
          "letter": "W",
          "sound": "/w/",
          "anchor": "Watch",
          "emoji": "⌚"
        },
        {
          "letter": "Y",
          "sound": "/j/",
          "anchor": "Yo-yo",
          "emoji": "🪀"
        },
        {
          "letter": "Z",
          "sound": "/z/",
          "anchor": "Zebra",
          "emoji": "🦓"
        }
      ],
      "cvcRimes": [
        {
          "rime": "-AT",
          "words": [
            {
              "word": "CAT",
              "emoji": "🐱"
            },
            {
              "word": "BAT",
              "emoji": "🦇"
            },
            {
              "word": "HAT",
              "emoji": "🎩"
            }
          ]
        },
        {
          "rime": "-UN",
          "words": [
            {
              "word": "SUN",
              "emoji": "☀️"
            },
            {
              "word": "RUN",
              "emoji": "🏃"
            },
            {
              "word": "BUN",
              "emoji": "🥯"
            }
          ]
        },
        {
          "rime": "-OG",
          "words": [
            {
              "word": "DOG",
              "emoji": "🐶"
            },
            {
              "word": "FROG",
              "emoji": "🐸"
            },
            {
              "word": "LOG",
              "emoji": "🪵"
            }
          ]
        },
        {
          "rime": "-IN",
          "words": [
            {
              "word": "PIN",
              "emoji": "📌"
            },
            {
              "word": "WIN",
              "emoji": "🏆"
            },
            {
              "word": "BIN",
              "emoji": "🗑️"
            }
          ]
        },
        {
          "rime": "-ET",
          "words": [
            {
              "word": "NET",
              "emoji": "🥅"
            },
            {
              "word": "PET",
              "emoji": "🐕"
            },
            {
              "word": "WET",
              "emoji": "💧"
            }
          ]
        },
        {
          "rime": "-OP",
          "words": [
            {
              "word": "TOP",
              "emoji": "🔝"
            },
            {
              "word": "HOP",
              "emoji": "🦘"
            },
            {
              "word": "MOP",
              "emoji": "🧹"
            }
          ]
        },
        {
          "rime": "-UG",
          "words": [
            {
              "word": "BUG",
              "emoji": "🐛"
            },
            {
              "word": "MUG",
              "emoji": "☕"
            },
            {
              "word": "HUG",
              "emoji": "🤗"
            }
          ]
        }
      ],
      "blends": [
        {
          "blend": "BL",
          "word": "BLUE",
          "emoji": "🔵"
        },
        {
          "blend": "ST",
          "word": "STAR",
          "emoji": "⭐"
        },
        {
          "blend": "TR",
          "word": "TREE",
          "emoji": "🌳"
        },
        {
          "blend": "CR",
          "word": "CRAB",
          "emoji": "🦀"
        },
        {
          "blend": "FL",
          "word": "FLAG",
          "emoji": "🚩"
        },
        {
          "blend": "GR",
          "word": "GRAPE",
          "emoji": "🍇"
        },
        {
          "blend": "PL",
          "word": "PLANE",
          "emoji": "✈️"
        },
        {
          "blend": "BR",
          "word": "BREAD",
          "emoji": "🍞"
        }
      ],
      "digraphs": [
        {
          "digraph": "SH",
          "sound": "/ʃ/",
          "word": "SHIP",
          "emoji": "🚢"
        },
        {
          "digraph": "CH",
          "sound": "/tʃ/",
          "word": "CHAIR",
          "emoji": "🪑"
        },
        {
          "digraph": "TH",
          "sound": "/θ/",
          "word": "THUMB",
          "emoji": "👍"
        },
        {
          "digraph": "PH",
          "sound": "/f/",
          "word": "PHONE",
          "emoji": "📱"
        },
        {
          "digraph": "WH",
          "sound": "/w/",
          "word": "WHALE",
          "emoji": "🐋"
        },
        {
          "digraph": "CK",
          "sound": "/k/",
          "word": "DUCK",
          "emoji": "🦆"
        }
      ],
      "vowelTeams": [
        {
          "pattern": "EE",
          "sound": "/iː/",
          "word": "TREE",
          "emoji": "🌳"
        },
        {
          "pattern": "EA",
          "sound": "/iː/",
          "word": "BEACH",
          "emoji": "🏖️"
        },
        {
          "pattern": "OA",
          "sound": "/oʊ/",
          "word": "BOAT",
          "emoji": "⛵"
        },
        {
          "pattern": "AI",
          "sound": "/eɪ/",
          "word": "RAIN",
          "emoji": "🌧️"
        },
        {
          "pattern": "OO",
          "sound": "/uː/",
          "word": "MOON",
          "emoji": "🌙"
        },
        {
          "pattern": "MAGIC-E",
          "sound": "Long Vowel",
          "word": "CAKE",
          "emoji": "🎂"
        }
      ],
      "sentenceWorkshop": [
        {
          "sign": "Comma (,)",
          "tip": "Take a quick breath pause.",
          "example": "The frog jumps, swims, and rests."
        },
        {
          "sign": "Period (.)",
          "tip": "Full stop. Idea is complete.",
          "example": "The puppy is asleep on the rug."
        },
        {
          "sign": "Question (?)",
          "tip": "Raise your voice pitch at the end.",
          "example": "Can you see the yellow bus?"
        },
        {
          "sign": "Exclamation (!)",
          "tip": "Read with high energy, wonder, or excitement.",
          "example": "Look at that shooting star!"
        }
      ]
    }
  },
  "wordBank": {
    "es": {
      "l1": [
        {
          "id": "es_l1_01",
          "target": "M",
          "anchorWord": "MANZANA",
          "emoji": "🍎",
          "distractors": [
            "P",
            "S",
            "L"
          ]
        },
        {
          "id": "es_l1_02",
          "target": "P",
          "anchorWord": "PATO",
          "emoji": "🦆",
          "distractors": [
            "M",
            "T",
            "B"
          ]
        },
        {
          "id": "es_l1_03",
          "target": "S",
          "anchorWord": "SOL",
          "emoji": "☀️",
          "distractors": [
            "N",
            "R",
            "D"
          ]
        },
        {
          "id": "es_l1_04",
          "target": "L",
          "anchorWord": "LUNA",
          "emoji": "🌙",
          "distractors": [
            "F",
            "C",
            "T"
          ]
        },
        {
          "id": "es_l1_05",
          "target": "T",
          "anchorWord": "TOMATE",
          "emoji": "🍅",
          "distractors": [
            "D",
            "P",
            "B"
          ]
        },
        {
          "id": "es_l1_06",
          "target": "D",
          "anchorWord": "DADO",
          "emoji": "🎲",
          "distractors": [
            "T",
            "B",
            "M"
          ]
        },
        {
          "id": "es_l1_07",
          "target": "N",
          "anchorWord": "NIDO",
          "emoji": "🪺",
          "distractors": [
            "M",
            "L",
            "S"
          ]
        },
        {
          "id": "es_l1_08",
          "target": "F",
          "anchorWord": "FOCA",
          "emoji": "🦭",
          "distractors": [
            "T",
            "P",
            "S"
          ]
        },
        {
          "id": "es_l1_09",
          "target": "B",
          "anchorWord": "BARCO",
          "emoji": "⛵",
          "distractors": [
            "D",
            "P",
            "V"
          ]
        },
        {
          "id": "es_l1_10",
          "target": "C",
          "anchorWord": "CASA",
          "emoji": "🏠",
          "distractors": [
            "S",
            "K",
            "Q"
          ]
        },
        {
          "id": "es_l1_11",
          "target": "R",
          "anchorWord": "RATON",
          "emoji": "🐭",
          "distractors": [
            "L",
            "D",
            "B"
          ]
        },
        {
          "id": "es_l1_12",
          "target": "G",
          "anchorWord": "GATO",
          "emoji": "🐱",
          "distractors": [
            "J",
            "C",
            "B"
          ]
        },
        {
          "id": "es_l1_13",
          "target": "J",
          "anchorWord": "JIRAFA",
          "emoji": "🦒",
          "distractors": [
            "G",
            "F",
            "L"
          ]
        },
        {
          "id": "es_l1_14",
          "target": "V",
          "anchorWord": "VACA",
          "emoji": "🐄",
          "distractors": [
            "B",
            "P",
            "M"
          ]
        },
        {
          "id": "es_l1_15",
          "target": "Z",
          "anchorWord": "ZAPATO",
          "emoji": "👟",
          "distractors": [
            "S",
            "C",
            "D"
          ]
        },
        {
          "id": "es_l1_16",
          "target": "CH",
          "anchorWord": "CHOCOLATE",
          "emoji": "🍫",
          "distractors": [
            "LL",
            "RR",
            "QU"
          ]
        },
        {
          "id": "es_l1_17",
          "target": "LL",
          "anchorWord": "LLAVE",
          "emoji": "🗝️",
          "distractors": [
            "CH",
            "Y",
            "L"
          ]
        },
        {
          "id": "es_l1_18",
          "target": "Ñ",
          "anchorWord": "ÑANDU",
          "emoji": "🦤",
          "distractors": [
            "N",
            "M",
            "U"
          ]
        },
        {
          "id": "es_l1_19",
          "target": "A",
          "anchorWord": "ABEJA",
          "emoji": "🐝",
          "distractors": [
            "E",
            "I",
            "O"
          ]
        },
        {
          "id": "es_l1_20",
          "target": "E",
          "anchorWord": "ELEFANTE",
          "emoji": "🐘",
          "distractors": [
            "A",
            "O",
            "U"
          ]
        },
        {
          "id": "es_l1_21",
          "target": "I",
          "anchorWord": "ISLA",
          "emoji": "🏝️",
          "distractors": [
            "E",
            "U",
            "A"
          ]
        },
        {
          "id": "es_l1_22",
          "target": "O",
          "anchorWord": "OSO",
          "emoji": "🐻",
          "distractors": [
            "A",
            "E",
            "U"
          ]
        },
        {
          "id": "es_l1_23",
          "target": "U",
          "anchorWord": "UVAS",
          "emoji": "🍇",
          "distractors": [
            "O",
            "I",
            "E"
          ]
        },
        {
          "id": "es_l1_24",
          "target": "K",
          "anchorWord": "KOALA",
          "emoji": "🐨",
          "distractors": [
            "C",
            "Q",
            "P"
          ]
        }
      ],
      "l2": [
        {
          "id": "es_l2_01",
          "word": "CASA",
          "syllables": [
            "CA",
            "SA"
          ],
          "emoji": "🏠",
          "distractors": [
            "PATO",
            "LUNA",
            "MESA"
          ]
        },
        {
          "id": "es_l2_02",
          "word": "PATO",
          "syllables": [
            "PA",
            "TO"
          ],
          "emoji": "🦆",
          "distractors": [
            "GATO",
            "SAPO",
            "TORO"
          ]
        },
        {
          "id": "es_l2_03",
          "word": "LUNA",
          "syllables": [
            "LU",
            "NA"
          ],
          "emoji": "🌙",
          "distractors": [
            "CUNA",
            "LANA",
            "ROPA"
          ]
        },
        {
          "id": "es_l2_04",
          "word": "MESA",
          "syllables": [
            "ME",
            "SA"
          ],
          "emoji": "🪑",
          "distractors": [
            "PESA",
            "TASA",
            "CASA"
          ]
        },
        {
          "id": "es_l2_05",
          "word": "PELO",
          "syllables": [
            "PE",
            "LO"
          ],
          "emoji": "💇",
          "distractors": [
            "PALO",
            "SOLO",
            "POLO"
          ]
        },
        {
          "id": "es_l2_06",
          "word": "BOCA",
          "syllables": [
            "BO",
            "CA"
          ],
          "emoji": "👄",
          "distractors": [
            "ROCA",
            "FOCA",
            "COCA"
          ]
        },
        {
          "id": "es_l2_07",
          "word": "DADO",
          "syllables": [
            "DA",
            "DO"
          ],
          "emoji": "🎲",
          "distractors": [
            "DEDO",
            "LADO",
            "NUDO"
          ]
        },
        {
          "id": "es_l2_08",
          "word": "FOCA",
          "syllables": [
            "FO",
            "CA"
          ],
          "emoji": "🦭",
          "distractors": [
            "BOCA",
            "ROCA",
            "SOPA"
          ]
        },
        {
          "id": "es_l2_09",
          "word": "GATO",
          "syllables": [
            "GA",
            "TO"
          ],
          "emoji": "🐱",
          "distractors": [
            "PATO",
            "RATO",
            "FOTO"
          ]
        },
        {
          "id": "es_l2_10",
          "word": "LOBO",
          "syllables": [
            "LO",
            "BO"
          ],
          "emoji": "🐺",
          "distractors": [
            "CUBO",
            "TUBO",
            "ROBO"
          ]
        },
        {
          "id": "es_l2_11",
          "word": "MANO",
          "syllables": [
            "MA",
            "NO"
          ],
          "emoji": "✋",
          "distractors": [
            "MONO",
            "CONO",
            "PIANO"
          ]
        },
        {
          "id": "es_l2_12",
          "word": "NIDO",
          "syllables": [
            "NI",
            "DO"
          ],
          "emoji": "🪺",
          "distractors": [
            "NUDO",
            "DADO",
            "LODO"
          ]
        },
        {
          "id": "es_l2_13",
          "word": "ROPA",
          "syllables": [
            "RO",
            "PA"
          ],
          "emoji": "👕",
          "distractors": [
            "SOPA",
            "COPA",
            "TAPA"
          ]
        },
        {
          "id": "es_l2_14",
          "word": "SAPO",
          "syllables": [
            "SA",
            "PO"
          ],
          "emoji": "🐸",
          "distractors": [
            "PATO",
            "GATO",
            "PASO"
          ]
        },
        {
          "id": "es_l2_15",
          "word": "TORO",
          "syllables": [
            "TO",
            "RO"
          ],
          "emoji": "🐂",
          "distractors": [
            "CORO",
            "LORO",
            "MURO"
          ]
        },
        {
          "id": "es_l2_16",
          "word": "VACA",
          "syllables": [
            "VA",
            "CA"
          ],
          "emoji": "🐄",
          "distractors": [
            "BOCA",
            "TACA",
            "LACA"
          ]
        },
        {
          "id": "es_l2_17",
          "word": "YATE",
          "syllables": [
            "YA",
            "TE"
          ],
          "emoji": "🛥️",
          "distractors": [
            "LOTE",
            "BOTE",
            "MATE"
          ]
        },
        {
          "id": "es_l2_18",
          "word": "ZUMO",
          "syllables": [
            "ZU",
            "MO"
          ],
          "emoji": "🧃",
          "distractors": [
            "HUMO",
            "SUMO",
            "RAMO"
          ]
        },
        {
          "id": "es_l2_19",
          "word": "ROSA",
          "syllables": [
            "RO",
            "SA"
          ],
          "emoji": "🌹",
          "distractors": [
            "COSA",
            "MESA",
            "SOSA"
          ]
        },
        {
          "id": "es_l2_20",
          "word": "BOTA",
          "syllables": [
            "BO",
            "TA"
          ],
          "emoji": "👢",
          "distractors": [
            "GOTA",
            "NOTA",
            "ROTA"
          ]
        },
        {
          "id": "es_l2_21",
          "word": "COPA",
          "syllables": [
            "CO",
            "PA"
          ],
          "emoji": "🏆",
          "distractors": [
            "SOPA",
            "ROPA",
            "CAPA"
          ]
        },
        {
          "id": "es_l2_22",
          "word": "TAZA",
          "syllables": [
            "TA",
            "ZA"
          ],
          "emoji": "🍵",
          "distractors": [
            "CASA",
            "MASA",
            "CAZA"
          ]
        },
        {
          "id": "es_l2_23",
          "word": "VINO",
          "syllables": [
            "VI",
            "NO"
          ],
          "emoji": "🍷",
          "distractors": [
            "PINO",
            "LINO",
            "TINO"
          ]
        },
        {
          "id": "es_l2_24",
          "word": "RANA",
          "syllables": [
            "RA",
            "NA"
          ],
          "emoji": "🐸",
          "distractors": [
            "LANA",
            "CANA",
            "SANA"
          ]
        },
        {
          "id": "es_l2_25",
          "word": "MOTO",
          "syllables": [
            "MO",
            "TO"
          ],
          "emoji": "🛵",
          "distractors": [
            "FOTO",
            "ROTO",
            "VOTO"
          ]
        },
        {
          "id": "es_l2_26",
          "word": "PIÑA",
          "syllables": [
            "PI",
            "ÑA"
          ],
          "emoji": "🍍",
          "distractors": [
            "NIÑA",
            "PEÑA",
            "VIÑA"
          ]
        }
      ],
      "l3": [
        {
          "id": "es_l3_01",
          "word": "CASA",
          "syllables": [
            "CA",
            "SA"
          ],
          "emoji": "🏠",
          "missingIndices": [
            1,
            3
          ]
        },
        {
          "id": "es_l3_02",
          "word": "PATO",
          "syllables": [
            "PA",
            "TO"
          ],
          "emoji": "🦆",
          "missingIndices": [
            1,
            3
          ]
        },
        {
          "id": "es_l3_03",
          "word": "LUNA",
          "syllables": [
            "LU",
            "NA"
          ],
          "emoji": "🌙",
          "missingIndices": [
            1,
            3
          ]
        },
        {
          "id": "es_l3_04",
          "word": "MESA",
          "syllables": [
            "ME",
            "SA"
          ],
          "emoji": "🪑",
          "missingIndices": [
            1,
            2
          ]
        },
        {
          "id": "es_l3_05",
          "word": "DADO",
          "syllables": [
            "DA",
            "DO"
          ],
          "emoji": "🎲",
          "missingIndices": [
            0,
            2
          ]
        },
        {
          "id": "es_l3_06",
          "word": "FOCA",
          "syllables": [
            "FO",
            "CA"
          ],
          "emoji": "🦭",
          "missingIndices": [
            1,
            2
          ]
        },
        {
          "id": "es_l3_07",
          "word": "GATO",
          "syllables": [
            "GA",
            "TO"
          ],
          "emoji": "🐱",
          "missingIndices": [
            1,
            3
          ]
        },
        {
          "id": "es_l3_08",
          "word": "LOBO",
          "syllables": [
            "LO",
            "BO"
          ],
          "emoji": "🐺",
          "missingIndices": [
            0,
            2
          ]
        },
        {
          "id": "es_l3_09",
          "word": "MANO",
          "syllables": [
            "MA",
            "NO"
          ],
          "emoji": "✋",
          "missingIndices": [
            1,
            2
          ]
        },
        {
          "id": "es_l3_10",
          "word": "NIDO",
          "syllables": [
            "NI",
            "DO"
          ],
          "emoji": "🪺",
          "missingIndices": [
            1,
            3
          ]
        },
        {
          "id": "es_l3_11",
          "word": "ROPA",
          "syllables": [
            "RO",
            "PA"
          ],
          "emoji": "👕",
          "missingIndices": [
            0,
            3
          ]
        },
        {
          "id": "es_l3_12",
          "word": "SAPO",
          "syllables": [
            "SA",
            "PO"
          ],
          "emoji": "🐸",
          "missingIndices": [
            1,
            2
          ]
        },
        {
          "id": "es_l3_13",
          "word": "TORO",
          "syllables": [
            "TO",
            "RO"
          ],
          "emoji": "🐂",
          "missingIndices": [
            0,
            2
          ]
        },
        {
          "id": "es_l3_14",
          "word": "VACA",
          "syllables": [
            "VA",
            "CA"
          ],
          "emoji": "🐄",
          "missingIndices": [
            1,
            3
          ]
        },
        {
          "id": "es_l3_15",
          "word": "BOTA",
          "syllables": [
            "BO",
            "TA"
          ],
          "emoji": "👢",
          "missingIndices": [
            1,
            3
          ]
        },
        {
          "id": "es_l3_16",
          "word": "ROSA",
          "syllables": [
            "RO",
            "SA"
          ],
          "emoji": "🌹",
          "missingIndices": [
            1,
            2
          ]
        },
        {
          "id": "es_l3_17",
          "word": "TAZA",
          "syllables": [
            "TA",
            "ZA"
          ],
          "emoji": "🍵",
          "missingIndices": [
            1,
            3
          ]
        },
        {
          "id": "es_l3_18",
          "word": "PELOTA",
          "syllables": [
            "PE",
            "LO",
            "TA"
          ],
          "emoji": "⚽",
          "missingIndices": [
            1,
            3
          ]
        },
        {
          "id": "es_l3_19",
          "word": "TOMATE",
          "syllables": [
            "TO",
            "MA",
            "TE"
          ],
          "emoji": "🍅",
          "missingIndices": [
            1,
            4
          ]
        },
        {
          "id": "es_l3_20",
          "word": "MALETA",
          "syllables": [
            "MA",
            "LE",
            "TA"
          ],
          "emoji": "🧳",
          "missingIndices": [
            2,
            4
          ]
        },
        {
          "id": "es_l3_21",
          "word": "CAMISA",
          "syllables": [
            "CA",
            "MI",
            "SA"
          ],
          "emoji": "👔",
          "missingIndices": [
            1,
            3
          ]
        },
        {
          "id": "es_l3_22",
          "word": "PAYASO",
          "syllables": [
            "PA",
            "YA",
            "SO"
          ],
          "emoji": "🤡",
          "missingIndices": [
            2,
            4
          ]
        },
        {
          "id": "es_l3_23",
          "word": "SIRENA",
          "syllables": [
            "SI",
            "RE",
            "NA"
          ],
          "emoji": "🧜",
          "missingIndices": [
            1,
            4
          ]
        },
        {
          "id": "es_l3_24",
          "word": "PALOMA",
          "syllables": [
            "PA",
            "LO",
            "MA"
          ],
          "emoji": "🕊️",
          "missingIndices": [
            1,
            3
          ]
        },
        {
          "id": "es_l3_25",
          "word": "CORONA",
          "syllables": [
            "CO",
            "RO",
            "NA"
          ],
          "emoji": "👑",
          "missingIndices": [
            1,
            4
          ]
        }
      ],
      "l4": [
        {
          "id": "es_l4_01",
          "word": "ESTRELLA",
          "syllables": [
            "ES",
            "TRE",
            "LLA"
          ],
          "emoji": "⭐",
          "microCheck": {
            "question": "¿Qué brilla en el cielo nocturno?",
            "options": [
              {
                "emoji": "⭐",
                "label": "Una estrella",
                "isCorrect": true
              },
              {
                "emoji": "☁️",
                "label": "Una nube",
                "isCorrect": false
              },
              {
                "emoji": "🌧️",
                "label": "La lluvia",
                "isCorrect": false
              }
            ]
          }
        },
        {
          "id": "es_l4_02",
          "word": "PLATANO",
          "syllables": [
            "PLA",
            "TA",
            "NO"
          ],
          "emoji": "🍌",
          "microCheck": {
            "question": "¿Qué fruta dulce y amarilla es?",
            "options": [
              {
                "emoji": "🍌",
                "label": "Un plátano",
                "isCorrect": true
              },
              {
                "emoji": "🍎",
                "label": "Una manzana",
                "isCorrect": false
              },
              {
                "emoji": "🍇",
                "label": "Unas uvas",
                "isCorrect": false
              }
            ]
          }
        },
        {
          "id": "es_l4_03",
          "word": "TRACTOR",
          "syllables": [
            "TRAC",
            "TOR"
          ],
          "emoji": "🚜",
          "microCheck": {
            "question": "¿Qué vehículo trabaja en el campo?",
            "options": [
              {
                "emoji": "🚜",
                "label": "Un tractor",
                "isCorrect": true
              },
              {
                "emoji": "🏎️",
                "label": "Un coche veloz",
                "isCorrect": false
              },
              {
                "emoji": "✈️",
                "label": "Un avión",
                "isCorrect": false
              }
            ]
          }
        },
        {
          "id": "es_l4_04",
          "word": "DRAGON",
          "syllables": [
            "DRA",
            "GON"
          ],
          "emoji": "🐉",
          "microCheck": {
            "question": "¿Qué criatura fantástica escupe fuego?",
            "options": [
              {
                "emoji": "🐉",
                "label": "Un dragón",
                "isCorrect": true
              },
              {
                "emoji": "🦄",
                "label": "Un unicornio",
                "isCorrect": false
              },
              {
                "emoji": "🦅",
                "label": "Un águila",
                "isCorrect": false
              }
            ]
          }
        },
        {
          "id": "es_l4_05",
          "word": "BRUJA",
          "syllables": [
            "BRU",
            "JA"
          ],
          "emoji": "🧙",
          "microCheck": {
            "question": "¿Quién vuela montada en una escoba?",
            "options": [
              {
                "emoji": "🧙",
                "label": "Una bruja",
                "isCorrect": true
              },
              {
                "emoji": "🧚",
                "label": "Un hada",
                "isCorrect": false
              },
              {
                "emoji": "🧝",
                "label": "Un elfo",
                "isCorrect": false
              }
            ]
          }
        },
        {
          "id": "es_l4_06",
          "word": "GLOBO",
          "syllables": [
            "GLO",
            "BO"
          ],
          "emoji": "🎈",
          "microCheck": {
            "question": "¿Qué juguete ligero sube por el aire?",
            "options": [
              {
                "emoji": "🎈",
                "label": "Un globo",
                "isCorrect": true
              },
              {
                "emoji": "⚽",
                "label": "Un balón",
                "isCorrect": false
              },
              {
                "emoji": "🧱",
                "label": "Un ladrillo",
                "isCorrect": false
              }
            ]
          }
        },
        {
          "id": "es_l4_07",
          "word": "FLECHA",
          "syllables": [
            "FLE",
            "CHA"
          ],
          "emoji": "🏹",
          "microCheck": {
            "question": "¿Qué proyectil se dispara con un arco?",
            "options": [
              {
                "emoji": "🏹",
                "label": "Una flecha",
                "isCorrect": true
              },
              {
                "emoji": "🗡️",
                "label": "Una espada",
                "isCorrect": false
              },
              {
                "emoji": "🛡️",
                "label": "Un escudo",
                "isCorrect": false
              }
            ]
          }
        },
        {
          "id": "es_l4_08",
          "word": "CRAYON",
          "syllables": [
            "CRA",
            "YON"
          ],
          "emoji": "🖍️",
          "microCheck": {
            "question": "¿Qué barra de cera sirve para colorear?",
            "options": [
              {
                "emoji": "🖍️",
                "label": "Un crayón",
                "isCorrect": true
              },
              {
                "emoji": "✂️",
                "label": "Una tijera",
                "isCorrect": false
              },
              {
                "emoji": "📏",
                "label": "Una regla",
                "isCorrect": false
              }
            ]
          }
        },
        {
          "id": "es_l4_09",
          "word": "GRILLO",
          "syllables": [
            "GRI",
            "LLO"
          ],
          "emoji": "🦗",
          "microCheck": {
            "question": "¿Qué insecto emite un canto de noche?",
            "options": [
              {
                "emoji": "🦗",
                "label": "Un grillo",
                "isCorrect": true
              },
              {
                "emoji": "🐝",
                "label": "Una abeja",
                "isCorrect": false
              },
              {
                "emoji": "🐜",
                "label": "Una hormiga",
                "isCorrect": false
              }
            ]
          }
        },
        {
          "id": "es_l4_10",
          "word": "PLANETA",
          "syllables": [
            "PLA",
            "NE",
            "TA"
          ],
          "emoji": "🪐",
          "microCheck": {
            "question": "¿Qué gran cuerpo viaja en el espacio?",
            "options": [
              {
                "emoji": "🪐",
                "label": "Un planeta",
                "isCorrect": true
              },
              {
                "emoji": "🪁",
                "label": "Una cometa",
                "isCorrect": false
              },
              {
                "emoji": "🪂",
                "label": "Un paracaídas",
                "isCorrect": false
              }
            ]
          }
        },
        {
          "id": "es_l4_11",
          "word": "TREN",
          "syllables": [
            "TREN"
          ],
          "emoji": "🚆",
          "microCheck": {
            "question": "¿Qué transporte viaja sobre vías metálicas?",
            "options": [
              {
                "emoji": "🚆",
                "label": "Un tren",
                "isCorrect": true
              },
              {
                "emoji": "🚌",
                "label": "Un autobús",
                "isCorrect": false
              },
              {
                "emoji": "🚲",
                "label": "Una bicicleta",
                "isCorrect": false
              }
            ]
          }
        },
        {
          "id": "es_l4_12",
          "word": "BARCO",
          "syllables": [
            "BAR",
            "CO"
          ],
          "emoji": "⛵",
          "microCheck": {
            "question": "¿Qué navega flotando sobre el agua?",
            "options": [
              {
                "emoji": "⛵",
                "label": "Un barco",
                "isCorrect": true
              },
              {
                "emoji": "🚀",
                "label": "Un cohete",
                "isCorrect": false
              },
              {
                "emoji": "🚗",
                "label": "Un coche",
                "isCorrect": false
              }
            ]
          }
        },
        {
          "id": "es_l4_13",
          "word": "ARBOL",
          "syllables": [
            "AR",
            "BOL"
          ],
          "emoji": "🌳",
          "microCheck": {
            "question": "¿Qué ser vivo tiene tronco verde y hojas?",
            "options": [
              {
                "emoji": "🌳",
                "label": "Un árbol",
                "isCorrect": true
              },
              {
                "emoji": "🪨",
                "label": "Una piedra",
                "isCorrect": false
              },
              {
                "emoji": "🍄",
                "label": "Una seta",
                "isCorrect": false
              }
            ]
          }
        },
        {
          "id": "es_l4_14",
          "word": "CIRCO",
          "syllables": [
            "CIR",
            "CO"
          ],
          "emoji": "🎪",
          "microCheck": {
            "question": "¿Dónde hay payasos, magia y malabaristas?",
            "options": [
              {
                "emoji": "🎪",
                "label": "El circo",
                "isCorrect": true
              },
              {
                "emoji": "🏫",
                "label": "La escuela",
                "isCorrect": false
              },
              {
                "emoji": "🏥",
                "label": "El hospital",
                "isCorrect": false
              }
            ]
          }
        },
        {
          "id": "es_l4_15",
          "word": "TORTUGA",
          "syllables": [
            "TOR",
            "TU",
            "GA"
          ],
          "emoji": "🐢",
          "microCheck": {
            "question": "¿Qué animal camina lento con su caparazón?",
            "options": [
              {
                "emoji": "🐢",
                "label": "La tortuga",
                "isCorrect": true
              },
              {
                "emoji": "🐰",
                "label": "El conejo",
                "isCorrect": false
              },
              {
                "emoji": "🐆",
                "label": "El guepardo",
                "isCorrect": false
              }
            ]
          }
        },
        {
          "id": "es_l4_16",
          "word": "CHOCOLATE",
          "syllables": [
            "CHO",
            "CO",
            "LA",
            "TE"
          ],
          "emoji": "🍫",
          "microCheck": {
            "question": "¿Qué rico dulce se prepara con cacao?",
            "options": [
              {
                "emoji": "🍫",
                "label": "El chocolate",
                "isCorrect": true
              },
              {
                "emoji": "🍋",
                "label": "El limón ácido",
                "isCorrect": false
              },
              {
                "emoji": "🧂",
                "label": "La sal",
                "isCorrect": false
              }
            ]
          }
        },
        {
          "id": "es_l4_17",
          "word": "CASTILLO",
          "syllables": [
            "CAS",
            "TI",
            "LLO"
          ],
          "emoji": "🏰",
          "microCheck": {
            "question": "¿Dónde vivían reyes y caballeros medievales?",
            "options": [
              {
                "emoji": "🏰",
                "label": "Un castillo",
                "isCorrect": true
              },
              {
                "emoji": "🛖",
                "label": "Una choza",
                "isCorrect": false
              },
              {
                "emoji": "⛺",
                "label": "Una tienda de campaña",
                "isCorrect": false
              }
            ]
          }
        },
        {
          "id": "es_l4_18",
          "word": "GUITARRA",
          "syllables": [
            "GUI",
            "TA",
            "RRA"
          ],
          "emoji": "🎸",
          "microCheck": {
            "question": "¿Qué instrumento musical tiene seis cuerdas?",
            "options": [
              {
                "emoji": "🎸",
                "label": "Una guitarra",
                "isCorrect": true
              },
              {
                "emoji": "🥁",
                "label": "Un tambor",
                "isCorrect": false
              },
              {
                "emoji": "🎺",
                "label": "Una trompeta",
                "isCorrect": false
              }
            ]
          }
        },
        {
          "id": "es_l4_19",
          "word": "QUESO",
          "syllables": [
            "QUE",
            "SO"
          ],
          "emoji": "🧀",
          "microCheck": {
            "question": "¿Qué alimento sabroso se elabora con leche?",
            "options": [
              {
                "emoji": "🧀",
                "label": "El queso",
                "isCorrect": true
              },
              {
                "emoji": "🥖",
                "label": "El pan",
                "isCorrect": false
              },
              {
                "emoji": "🍯",
                "label": "La miel de abeja",
                "isCorrect": false
              }
            ]
          }
        },
        {
          "id": "es_l4_20",
          "word": "DELFIN",
          "syllables": [
            "DEL",
            "FIN"
          ],
          "emoji": "🐬",
          "microCheck": {
            "question": "¿Qué mamífero marino salta en las olas?",
            "options": [
              {
                "emoji": "🐬",
                "label": "El delfín",
                "isCorrect": true
              },
              {
                "emoji": "🦈",
                "label": "El tiburón",
                "isCorrect": false
              },
              {
                "emoji": "🐙",
                "label": "El pulpo",
                "isCorrect": false
              }
            ]
          }
        },
        {
          "id": "es_l4_21",
          "word": "MONTAÑA",
          "syllables": [
            "MON",
            "TA",
            "ÑA"
          ],
          "emoji": "⛰️",
          "microCheck": {
            "question": "¿Qué pico de tierra se eleva hasta las nubes?",
            "options": [
              {
                "emoji": "⛰️",
                "label": "Una montaña",
                "isCorrect": true
              },
              {
                "emoji": "🏖️",
                "label": "Una playa",
                "isCorrect": false
              },
              {
                "emoji": "🏜️",
                "label": "Un desierto",
                "isCorrect": false
              }
            ]
          }
        },
        {
          "id": "es_l4_22",
          "word": "TAMBOR",
          "syllables": [
            "TAM",
            "BOR"
          ],
          "emoji": "🥁",
          "microCheck": {
            "question": "¿Qué instrumento se golpea con dos baquetas?",
            "options": [
              {
                "emoji": "🥁",
                "label": "Un tambor",
                "isCorrect": true
              },
              {
                "emoji": "🎻",
                "label": "Un violín",
                "isCorrect": false
              },
              {
                "emoji": "🎹",
                "label": "Un piano",
                "isCorrect": false
              }
            ]
          }
        },
        {
          "id": "es_l4_23",
          "word": "SOMBRILLA",
          "syllables": [
            "SOM",
            "BRI",
            "LLA"
          ],
          "emoji": "⛱️",
          "microCheck": {
            "question": "¿Qué nos da sombra fresca en la arena de la playa?",
            "options": [
              {
                "emoji": "⛱️",
                "label": "Una sombrilla",
                "isCorrect": true
              },
              {
                "emoji": "🧣",
                "label": "Una bufanda de lana",
                "isCorrect": false
              },
              {
                "emoji": "🧤",
                "label": "Unos guantes",
                "isCorrect": false
              }
            ]
          }
        },
        {
          "id": "es_l4_24",
          "word": "CANGURO",
          "syllables": [
            "CAN",
            "GU",
            "RO"
          ],
          "emoji": "🦘",
          "microCheck": {
            "question": "¿Qué animal salta veloz con su bolsa marsupial?",
            "options": [
              {
                "emoji": "🦘",
                "label": "El canguro",
                "isCorrect": true
              },
              {
                "emoji": "🐨",
                "label": "El koala",
                "isCorrect": false
              },
              {
                "emoji": "🐼",
                "label": "El oso panda",
                "isCorrect": false
              }
            ]
          }
        },
        {
          "id": "es_l4_25",
          "word": "PINGÜINO",
          "syllables": [
            "PIN",
            "GÜI",
            "NO"
          ],
          "emoji": "🐧",
          "microCheck": {
            "question": "¿Qué ave marina nada en el hielo con smoking?",
            "options": [
              {
                "emoji": "🐧",
                "label": "El pingüino",
                "isCorrect": true
              },
              {
                "emoji": "🦆",
                "label": "El pato",
                "isCorrect": false
              },
              {
                "emoji": "🦅",
                "label": "El águila",
                "isCorrect": false
              }
            ]
          }
        },
        {
          "id": "es_l4_26",
          "word": "ESPONJA",
          "syllables": [
            "ES",
            "PON",
            "JA"
          ],
          "emoji": "🧽",
          "microCheck": {
            "question": "¿Qué absorbe agua y jabón para limpiar?",
            "options": [
              {
                "emoji": "🧽",
                "label": "Una esponja",
                "isCorrect": true
              },
              {
                "emoji": "🧹",
                "label": "Una escoba",
                "isCorrect": false
              },
              {
                "emoji": "🪣",
                "label": "Un cubo",
                "isCorrect": false
              }
            ]
          }
        }
      ]
    },
    "en": {
      "l1": [
        {
          "id": "en_l1_01",
          "target": "A",
          "anchorWord": "APPLE",
          "emoji": "🍎",
          "distractors": [
            "E",
            "I",
            "O"
          ]
        },
        {
          "id": "en_l1_02",
          "target": "B",
          "anchorWord": "BEAR",
          "emoji": "🐻",
          "distractors": [
            "D",
            "P",
            "T"
          ]
        },
        {
          "id": "en_l1_03",
          "target": "C",
          "anchorWord": "CAT",
          "emoji": "🐱",
          "distractors": [
            "K",
            "S",
            "G"
          ]
        },
        {
          "id": "en_l1_04",
          "target": "D",
          "anchorWord": "DOG",
          "emoji": "🐶",
          "distractors": [
            "B",
            "P",
            "T"
          ]
        },
        {
          "id": "en_l1_05",
          "target": "E",
          "anchorWord": "ELEPHANT",
          "emoji": "🐘",
          "distractors": [
            "A",
            "O",
            "U"
          ]
        },
        {
          "id": "en_l1_06",
          "target": "F",
          "anchorWord": "FISH",
          "emoji": "🐟",
          "distractors": [
            "V",
            "P",
            "T"
          ]
        },
        {
          "id": "en_l1_07",
          "target": "G",
          "anchorWord": "GOAT",
          "emoji": "🐐",
          "distractors": [
            "C",
            "J",
            "K"
          ]
        },
        {
          "id": "en_l1_08",
          "target": "H",
          "anchorWord": "HAT",
          "emoji": "🎩",
          "distractors": [
            "N",
            "M",
            "K"
          ]
        },
        {
          "id": "en_l1_09",
          "target": "I",
          "anchorWord": "IGLOO",
          "emoji": "🛖",
          "distractors": [
            "E",
            "A",
            "O"
          ]
        },
        {
          "id": "en_l1_10",
          "target": "J",
          "anchorWord": "JUG",
          "emoji": "🏺",
          "distractors": [
            "G",
            "Y",
            "L"
          ]
        },
        {
          "id": "en_l1_11",
          "target": "K",
          "anchorWord": "KITE",
          "emoji": "🪁",
          "distractors": [
            "C",
            "T",
            "P"
          ]
        },
        {
          "id": "en_l1_12",
          "target": "L",
          "anchorWord": "LION",
          "emoji": "🦁",
          "distractors": [
            "I",
            "T",
            "R"
          ]
        },
        {
          "id": "en_l1_13",
          "target": "M",
          "anchorWord": "MOON",
          "emoji": "🌙",
          "distractors": [
            "N",
            "W",
            "H"
          ]
        },
        {
          "id": "en_l1_14",
          "target": "N",
          "anchorWord": "NEST",
          "emoji": "🪺",
          "distractors": [
            "M",
            "U",
            "H"
          ]
        },
        {
          "id": "en_l1_15",
          "target": "O",
          "anchorWord": "OCTOPUS",
          "emoji": "🐙",
          "distractors": [
            "A",
            "U",
            "C"
          ]
        },
        {
          "id": "en_l1_16",
          "target": "P",
          "anchorWord": "PIG",
          "emoji": "🐷",
          "distractors": [
            "B",
            "D",
            "Q"
          ]
        },
        {
          "id": "en_l1_17",
          "target": "R",
          "anchorWord": "RING",
          "emoji": "💍",
          "distractors": [
            "P",
            "B",
            "N"
          ]
        },
        {
          "id": "en_l1_18",
          "target": "S",
          "anchorWord": "SUN",
          "emoji": "☀️",
          "distractors": [
            "C",
            "Z",
            "X"
          ]
        },
        {
          "id": "en_l1_19",
          "target": "T",
          "anchorWord": "TREE",
          "emoji": "🌳",
          "distractors": [
            "F",
            "L",
            "D"
          ]
        },
        {
          "id": "en_l1_20",
          "target": "U",
          "anchorWord": "UMBRELLA",
          "emoji": "☂️",
          "distractors": [
            "V",
            "O",
            "W"
          ]
        },
        {
          "id": "en_l1_21",
          "target": "V",
          "anchorWord": "VAN",
          "emoji": "🚐",
          "distractors": [
            "U",
            "W",
            "Y"
          ]
        },
        {
          "id": "en_l1_22",
          "target": "W",
          "anchorWord": "WATCH",
          "emoji": "⌚",
          "distractors": [
            "M",
            "V",
            "N"
          ]
        },
        {
          "id": "en_l1_23",
          "target": "Y",
          "anchorWord": "YOYO",
          "emoji": "🪀",
          "distractors": [
            "V",
            "J",
            "U"
          ]
        },
        {
          "id": "en_l1_24",
          "target": "Z",
          "anchorWord": "ZEBRA",
          "emoji": "🦓",
          "distractors": [
            "S",
            "X",
            "C"
          ]
        }
      ],
      "l2": [
        {
          "id": "en_l2_01",
          "word": "CAT",
          "syllables": [
            "CAT"
          ],
          "emoji": "🐱",
          "distractors": [
            "BAT",
            "HAT",
            "RAT"
          ]
        },
        {
          "id": "en_l2_02",
          "word": "DOG",
          "syllables": [
            "DOG"
          ],
          "emoji": "🐶",
          "distractors": [
            "FOG",
            "LOG",
            "PIG"
          ]
        },
        {
          "id": "en_l2_03",
          "word": "SUN",
          "syllables": [
            "SUN"
          ],
          "emoji": "☀️",
          "distractors": [
            "BUN",
            "RUN",
            "FUN"
          ]
        },
        {
          "id": "en_l2_04",
          "word": "PIG",
          "syllables": [
            "PIG"
          ],
          "emoji": "🐷",
          "distractors": [
            "BIG",
            "WIG",
            "DIG"
          ]
        },
        {
          "id": "en_l2_05",
          "word": "BUS",
          "syllables": [
            "BUS"
          ],
          "emoji": "🚌",
          "distractors": [
            "CUP",
            "BUG",
            "TUB"
          ]
        },
        {
          "id": "en_l2_06",
          "word": "CUP",
          "syllables": [
            "CUP"
          ],
          "emoji": "☕",
          "distractors": [
            "PUP",
            "CAP",
            "MUG"
          ]
        },
        {
          "id": "en_l2_07",
          "word": "HAT",
          "syllables": [
            "HAT"
          ],
          "emoji": "🎩",
          "distractors": [
            "CAT",
            "MAT",
            "HOT"
          ]
        },
        {
          "id": "en_l2_08",
          "word": "NET",
          "syllables": [
            "NET"
          ],
          "emoji": "🥅",
          "distractors": [
            "PET",
            "WET",
            "NUT"
          ]
        },
        {
          "id": "en_l2_09",
          "word": "PEN",
          "syllables": [
            "PEN"
          ],
          "emoji": "🖊️",
          "distractors": [
            "HEN",
            "TEN",
            "PIN"
          ]
        },
        {
          "id": "en_l2_10",
          "word": "BED",
          "syllables": [
            "BED"
          ],
          "emoji": "🛏️",
          "distractors": [
            "RED",
            "FED",
            "BAD"
          ]
        },
        {
          "id": "en_l2_11",
          "word": "BOX",
          "syllables": [
            "BOX"
          ],
          "emoji": "📦",
          "distractors": [
            "FOX",
            "POX",
            "BAG"
          ]
        },
        {
          "id": "en_l2_12",
          "word": "FOX",
          "syllables": [
            "FOX"
          ],
          "emoji": "🦊",
          "distractors": [
            "BOX",
            "FIX",
            "DOG"
          ]
        },
        {
          "id": "en_l2_13",
          "word": "FROG",
          "syllables": [
            "FROG"
          ],
          "emoji": "🐸",
          "distractors": [
            "FLAG",
            "FROM",
            "TOAD"
          ]
        },
        {
          "id": "en_l2_14",
          "word": "DUCK",
          "syllables": [
            "DUCK"
          ],
          "emoji": "🦆",
          "distractors": [
            "LUCK",
            "SOCK",
            "DECK"
          ]
        },
        {
          "id": "en_l2_15",
          "word": "FISH",
          "syllables": [
            "FISH"
          ],
          "emoji": "🐟",
          "distractors": [
            "DISH",
            "WISH",
            "SHIP"
          ]
        },
        {
          "id": "en_l2_16",
          "word": "SHIP",
          "syllables": [
            "SHIP"
          ],
          "emoji": "🚢",
          "distractors": [
            "SHOP",
            "CHIP",
            "TRIP"
          ]
        },
        {
          "id": "en_l2_17",
          "word": "STAR",
          "syllables": [
            "STAR"
          ],
          "emoji": "⭐",
          "distractors": [
            "STIR",
            "SCAR",
            "MOON"
          ]
        },
        {
          "id": "en_l2_18",
          "word": "MOON",
          "syllables": [
            "MOON"
          ],
          "emoji": "🌙",
          "distractors": [
            "SOON",
            "NOON",
            "SPOON"
          ]
        },
        {
          "id": "en_l2_19",
          "word": "BOOK",
          "syllables": [
            "BOOK"
          ],
          "emoji": "📖",
          "distractors": [
            "LOOK",
            "HOOK",
            "COOK"
          ]
        },
        {
          "id": "en_l2_20",
          "word": "BALL",
          "syllables": [
            "BALL"
          ],
          "emoji": "⚽",
          "distractors": [
            "WALL",
            "FALL",
            "BELL"
          ]
        },
        {
          "id": "en_l2_21",
          "word": "TREE",
          "syllables": [
            "TREE"
          ],
          "emoji": "🌳",
          "distractors": [
            "FREE",
            "THREE",
            "TRUE"
          ]
        },
        {
          "id": "en_l2_22",
          "word": "BIRD",
          "syllables": [
            "BIRD"
          ],
          "emoji": "🐦",
          "distractors": [
            "WORD",
            "HERD",
            "BARD"
          ]
        },
        {
          "id": "en_l2_23",
          "word": "LION",
          "syllables": [
            "LI",
            "ON"
          ],
          "emoji": "🦁",
          "distractors": [
            "TIGER",
            "BEAR",
            "LEOPARD"
          ]
        },
        {
          "id": "en_l2_24",
          "word": "TIGER",
          "syllables": [
            "TI",
            "GER"
          ],
          "emoji": "🐯",
          "distractors": [
            "LION",
            "ZEBRA",
            "PANDA"
          ]
        },
        {
          "id": "en_l2_25",
          "word": "RABBIT",
          "syllables": [
            "RAB",
            "BIT"
          ],
          "emoji": "🐰",
          "distractors": [
            "HABIT",
            "ROBIN",
            "TURTLE"
          ]
        },
        {
          "id": "en_l2_26",
          "word": "PUPPY",
          "syllables": [
            "PUP",
            "PY"
          ],
          "emoji": "🐶",
          "distractors": [
            "KITTY",
            "BUNNY",
            "POPPY"
          ]
        }
      ],
      "l3": [
        {
          "id": "en_l3_01",
          "word": "CAT",
          "syllables": [
            "CAT"
          ],
          "emoji": "🐱",
          "missingIndices": [
            1
          ]
        },
        {
          "id": "en_l3_02",
          "word": "DOG",
          "syllables": [
            "DOG"
          ],
          "emoji": "🐶",
          "missingIndices": [
            1
          ]
        },
        {
          "id": "en_l3_03",
          "word": "SUN",
          "syllables": [
            "SUN"
          ],
          "emoji": "☀️",
          "missingIndices": [
            1
          ]
        },
        {
          "id": "en_l3_04",
          "word": "PIG",
          "syllables": [
            "PIG"
          ],
          "emoji": "🐷",
          "missingIndices": [
            1
          ]
        },
        {
          "id": "en_l3_05",
          "word": "BUS",
          "syllables": [
            "BUS"
          ],
          "emoji": "🚌",
          "missingIndices": [
            0,
            2
          ]
        },
        {
          "id": "en_l3_06",
          "word": "CUP",
          "syllables": [
            "CUP"
          ],
          "emoji": "☕",
          "missingIndices": [
            1
          ]
        },
        {
          "id": "en_l3_07",
          "word": "HAT",
          "syllables": [
            "HAT"
          ],
          "emoji": "🎩",
          "missingIndices": [
            0,
            2
          ]
        },
        {
          "id": "en_l3_08",
          "word": "NET",
          "syllables": [
            "NET"
          ],
          "emoji": "🥅",
          "missingIndices": [
            1
          ]
        },
        {
          "id": "en_l3_09",
          "word": "PEN",
          "syllables": [
            "PEN"
          ],
          "emoji": "🖊️",
          "missingIndices": [
            1
          ]
        },
        {
          "id": "en_l3_10",
          "word": "BED",
          "syllables": [
            "BED"
          ],
          "emoji": "🛏️",
          "missingIndices": [
            0,
            2
          ]
        },
        {
          "id": "en_l3_11",
          "word": "BOX",
          "syllables": [
            "BOX"
          ],
          "emoji": "📦",
          "missingIndices": [
            1
          ]
        },
        {
          "id": "en_l3_12",
          "word": "FOX",
          "syllables": [
            "FOX"
          ],
          "emoji": "🦊",
          "missingIndices": [
            1
          ]
        },
        {
          "id": "en_l3_13",
          "word": "FROG",
          "syllables": [
            "FROG"
          ],
          "emoji": "🐸",
          "missingIndices": [
            1,
            3
          ]
        },
        {
          "id": "en_l3_14",
          "word": "DUCK",
          "syllables": [
            "DUCK"
          ],
          "emoji": "🦆",
          "missingIndices": [
            1,
            2
          ]
        },
        {
          "id": "en_l3_15",
          "word": "FISH",
          "syllables": [
            "FISH"
          ],
          "emoji": "🐟",
          "missingIndices": [
            1,
            3
          ]
        },
        {
          "id": "en_l3_16",
          "word": "SHIP",
          "syllables": [
            "SHIP"
          ],
          "emoji": "🚢",
          "missingIndices": [
            1,
            2
          ]
        },
        {
          "id": "en_l3_17",
          "word": "STAR",
          "syllables": [
            "STAR"
          ],
          "emoji": "⭐",
          "missingIndices": [
            0,
            2
          ]
        },
        {
          "id": "en_l3_18",
          "word": "MOON",
          "syllables": [
            "MOON"
          ],
          "emoji": "🌙",
          "missingIndices": [
            1,
            2
          ]
        },
        {
          "id": "en_l3_19",
          "word": "BOOK",
          "syllables": [
            "BOOK"
          ],
          "emoji": "📖",
          "missingIndices": [
            1,
            2
          ]
        },
        {
          "id": "en_l3_20",
          "word": "BALL",
          "syllables": [
            "BALL"
          ],
          "emoji": "⚽",
          "missingIndices": [
            1,
            3
          ]
        },
        {
          "id": "en_l3_21",
          "word": "TREE",
          "syllables": [
            "TREE"
          ],
          "emoji": "🌳",
          "missingIndices": [
            1,
            2
          ]
        },
        {
          "id": "en_l3_22",
          "word": "BIRD",
          "syllables": [
            "BIRD"
          ],
          "emoji": "🐦",
          "missingIndices": [
            1,
            2
          ]
        },
        {
          "id": "en_l3_23",
          "word": "LION",
          "syllables": [
            "LI",
            "ON"
          ],
          "emoji": "🦁",
          "missingIndices": [
            1,
            3
          ]
        },
        {
          "id": "en_l3_24",
          "word": "TIGER",
          "syllables": [
            "TI",
            "GER"
          ],
          "emoji": "🐯",
          "missingIndices": [
            1,
            4
          ]
        },
        {
          "id": "en_l3_25",
          "word": "RABBIT",
          "syllables": [
            "RAB",
            "BIT"
          ],
          "emoji": "🐰",
          "missingIndices": [
            1,
            4
          ]
        }
      ],
      "l4": [
        {
          "id": "en_l4_01",
          "word": "DRAGON",
          "syllables": [
            "DRA",
            "GON"
          ],
          "emoji": "🐉",
          "microCheck": {
            "question": "What magical creature breathes fire?",
            "options": [
              {
                "emoji": "🐉",
                "label": "A dragon",
                "isCorrect": true
              },
              {
                "emoji": "🦄",
                "label": "A unicorn",
                "isCorrect": false
              },
              {
                "emoji": "🦅",
                "label": "An eagle",
                "isCorrect": false
              }
            ]
          }
        },
        {
          "id": "en_l4_02",
          "word": "TRACTOR",
          "syllables": [
            "TRAC",
            "TOR"
          ],
          "emoji": "🚜",
          "microCheck": {
            "question": "Which machine works on a farm field?",
            "options": [
              {
                "emoji": "🚜",
                "label": "A tractor",
                "isCorrect": true
              },
              {
                "emoji": "🏎️",
                "label": "A racing car",
                "isCorrect": false
              },
              {
                "emoji": "✈️",
                "label": "An airplane",
                "isCorrect": false
              }
            ]
          }
        },
        {
          "id": "en_l4_03",
          "word": "PLANET",
          "syllables": [
            "PLAN",
            "ET"
          ],
          "emoji": "🪐",
          "microCheck": {
            "question": "What orbits the sun in outer space?",
            "options": [
              {
                "emoji": "🪐",
                "label": "A planet",
                "isCorrect": true
              },
              {
                "emoji": "🪁",
                "label": "A kite",
                "isCorrect": false
              },
              {
                "emoji": "🪂",
                "label": "A parachute",
                "isCorrect": false
              }
            ]
          }
        },
        {
          "id": "en_l4_04",
          "word": "DOLPHIN",
          "syllables": [
            "DOL",
            "PHIN"
          ],
          "emoji": "🐬",
          "microCheck": {
            "question": "Which playful sea mammal leaps in waves?",
            "options": [
              {
                "emoji": "🐬",
                "label": "A dolphin",
                "isCorrect": true
              },
              {
                "emoji": "🦈",
                "label": "A shark",
                "isCorrect": false
              },
              {
                "emoji": "🐙",
                "label": "An octopus",
                "isCorrect": false
              }
            ]
          }
        },
        {
          "id": "en_l4_05",
          "word": "CASTLE",
          "syllables": [
            "CAS",
            "TLE"
          ],
          "emoji": "🏰",
          "microCheck": {
            "question": "Where did kings and knights live?",
            "options": [
              {
                "emoji": "🏰",
                "label": "In a castle",
                "isCorrect": true
              },
              {
                "emoji": "🛖",
                "label": "In a hut",
                "isCorrect": false
              },
              {
                "emoji": "⛺",
                "label": "In a tent",
                "isCorrect": false
              }
            ]
          }
        },
        {
          "id": "en_l4_06",
          "word": "GUITAR",
          "syllables": [
            "GUI",
            "TAR"
          ],
          "emoji": "🎸",
          "microCheck": {
            "question": "Which musical instrument has six strings?",
            "options": [
              {
                "emoji": "🎸",
                "label": "A guitar",
                "isCorrect": true
              },
              {
                "emoji": "🥁",
                "label": "A drum",
                "isCorrect": false
              },
              {
                "emoji": "🎺",
                "label": "A trumpet",
                "isCorrect": false
              }
            ]
          }
        },
        {
          "id": "en_l4_07",
          "word": "TURTLE",
          "syllables": [
            "TUR",
            "TLE"
          ],
          "emoji": "🐢",
          "microCheck": {
            "question": "Which animal moves slowly with a shell?",
            "options": [
              {
                "emoji": "🐢",
                "label": "A turtle",
                "isCorrect": true
              },
              {
                "emoji": "🐰",
                "label": "A rabbit",
                "isCorrect": false
              },
              {
                "emoji": "🐆",
                "label": "A cheetah",
                "isCorrect": false
              }
            ]
          }
        },
        {
          "id": "en_l4_08",
          "word": "PENGUIN",
          "syllables": [
            "PEN",
            "GUIN"
          ],
          "emoji": "🐧",
          "microCheck": {
            "question": "Which bird waddles on ice and swims fast?",
            "options": [
              {
                "emoji": "🐧",
                "label": "A penguin",
                "isCorrect": true
              },
              {
                "emoji": "🦆",
                "label": "A duck",
                "isCorrect": false
              },
              {
                "emoji": "🦉",
                "label": "An owl",
                "isCorrect": false
              }
            ]
          }
        },
        {
          "id": "en_l4_09",
          "word": "MONKEY",
          "syllables": [
            "MON",
            "KEY"
          ],
          "emoji": "🐒",
          "microCheck": {
            "question": "Which animal swings through jungle trees?",
            "options": [
              {
                "emoji": "🐒",
                "label": "A monkey",
                "isCorrect": true
              },
              {
                "emoji": "🐻",
                "label": "A bear",
                "isCorrect": false
              },
              {
                "emoji": "🐺",
                "label": "A wolf",
                "isCorrect": false
              }
            ]
          }
        },
        {
          "id": "en_l4_10",
          "word": "SUNSET",
          "syllables": [
            "SUN",
            "SET"
          ],
          "emoji": "🌇",
          "microCheck": {
            "question": "What happens when the sun goes down at dusk?",
            "options": [
              {
                "emoji": "🌇",
                "label": "A sunset",
                "isCorrect": true
              },
              {
                "emoji": "🌅",
                "label": "A sunrise",
                "isCorrect": false
              },
              {
                "emoji": "🌧️",
                "label": "A snowstorm",
                "isCorrect": false
              }
            ]
          }
        },
        {
          "id": "en_l4_11",
          "word": "PICNIC",
          "syllables": [
            "PIC",
            "NIC"
          ],
          "emoji": "🧺",
          "microCheck": {
            "question": "What outdoor meal is eaten on a blanket?",
            "options": [
              {
                "emoji": "🧺",
                "label": "A picnic",
                "isCorrect": true
              },
              {
                "emoji": "🍳",
                "label": "A restaurant dinner",
                "isCorrect": false
              },
              {
                "emoji": "🛒",
                "label": "A grocery shop",
                "isCorrect": false
              }
            ]
          }
        },
        {
          "id": "en_l4_12",
          "word": "APPLE",
          "syllables": [
            "AP",
            "PLE"
          ],
          "emoji": "🍎",
          "microCheck": {
            "question": "Which crisp round fruit grows on trees?",
            "options": [
              {
                "emoji": "🍎",
                "label": "An apple",
                "isCorrect": true
              },
              {
                "emoji": "🥕",
                "label": "A carrot",
                "isCorrect": false
              },
              {
                "emoji": "🥔",
                "label": "A potato",
                "isCorrect": false
              }
            ]
          }
        },
        {
          "id": "en_l4_13",
          "word": "KITTEN",
          "syllables": [
            "KIT",
            "TEN"
          ],
          "emoji": "🐱",
          "microCheck": {
            "question": "What is a baby cat called?",
            "options": [
              {
                "emoji": "🐱",
                "label": "A kitten",
                "isCorrect": true
              },
              {
                "emoji": "🐶",
                "label": "A puppy",
                "isCorrect": false
              },
              {
                "emoji": "🐣",
                "label": "A chick",
                "isCorrect": false
              }
            ]
          }
        },
        {
          "id": "en_l4_14",
          "word": "BALLOON",
          "syllables": [
            "BAL",
            "LOON"
          ],
          "emoji": "🎈",
          "microCheck": {
            "question": "What rubber toy floats high in the air?",
            "options": [
              {
                "emoji": "🎈",
                "label": "A balloon",
                "isCorrect": true
              },
              {
                "emoji": "⚽",
                "label": "A soccer ball",
                "isCorrect": false
              },
              {
                "emoji": "🪨",
                "label": "A heavy rock",
                "isCorrect": false
              }
            ]
          }
        },
        {
          "id": "en_l4_15",
          "word": "ROBOT",
          "syllables": [
            "RO",
            "BOT"
          ],
          "emoji": "🤖",
          "microCheck": {
            "question": "What mechanical helper is run by computers?",
            "options": [
              {
                "emoji": "🤖",
                "label": "A robot",
                "isCorrect": true
              },
              {
                "emoji": "🐴",
                "label": "A horse",
                "isCorrect": false
              },
              {
                "emoji": "🌱",
                "label": "A plant",
                "isCorrect": false
              }
            ]
          }
        },
        {
          "id": "en_l4_16",
          "word": "ROCKET",
          "syllables": [
            "ROCK",
            "ET"
          ],
          "emoji": "🚀",
          "microCheck": {
            "question": "What vehicle blasts astronauts to the stars?",
            "options": [
              {
                "emoji": "🚀",
                "label": "A rocket",
                "isCorrect": true
              },
              {
                "emoji": "⛵",
                "label": "A sailboat",
                "isCorrect": false
              },
              {
                "emoji": "🚲",
                "label": "A bicycle",
                "isCorrect": false
              }
            ]
          }
        },
        {
          "id": "en_l4_17",
          "word": "SPIDER",
          "syllables": [
            "SPI",
            "DER"
          ],
          "emoji": "🕷️",
          "microCheck": {
            "question": "Which creature spins a sticky silk web?",
            "options": [
              {
                "emoji": "🕷️",
                "label": "A spider",
                "isCorrect": true
              },
              {
                "emoji": "🐜",
                "label": "An ant",
                "isCorrect": false
              },
              {
                "emoji": "🐝",
                "label": "A bumblebee",
                "isCorrect": false
              }
            ]
          }
        },
        {
          "id": "en_l4_18",
          "word": "WINTER",
          "syllables": [
            "WIN",
            "TER"
          ],
          "emoji": "❄️",
          "microCheck": {
            "question": "Which cold season brings ice and snow?",
            "options": [
              {
                "emoji": "❄️",
                "label": "Winter",
                "isCorrect": true
              },
              {
                "emoji": "☀️",
                "label": "Summer",
                "isCorrect": false
              },
              {
                "emoji": "🌸",
                "label": "Spring",
                "isCorrect": false
              }
            ]
          }
        },
        {
          "id": "en_l4_19",
          "word": "SUMMER",
          "syllables": [
            "SUM",
            "MER"
          ],
          "emoji": "🏖️",
          "microCheck": {
            "question": "Which sunny season is great for beach trips?",
            "options": [
              {
                "emoji": "🏖️",
                "label": "Summer",
                "isCorrect": true
              },
              {
                "emoji": "❄️",
                "label": "Winter",
                "isCorrect": false
              },
              {
                "emoji": "🍂",
                "label": "Autumn",
                "isCorrect": false
              }
            ]
          }
        },
        {
          "id": "en_l4_20",
          "word": "FLOWER",
          "syllables": [
            "FLOW",
            "ER"
          ],
          "emoji": "🌸",
          "microCheck": {
            "question": "What colorful garden plant has fragrant petals?",
            "options": [
              {
                "emoji": "🌸",
                "label": "A flower",
                "isCorrect": true
              },
              {
                "emoji": "🪵",
                "label": "A log",
                "isCorrect": false
              },
              {
                "emoji": "🪨",
                "label": "A stone",
                "isCorrect": false
              }
            ]
          }
        },
        {
          "id": "en_l4_21",
          "word": "SILVER",
          "syllables": [
            "SIL",
            "VER"
          ],
          "emoji": "🥈",
          "microCheck": {
            "question": "Which shiny metal is given for second place?",
            "options": [
              {
                "emoji": "🥈",
                "label": "Silver",
                "isCorrect": true
              },
              {
                "emoji": "🥇",
                "label": "Gold",
                "isCorrect": false
              },
              {
                "emoji": "🥉",
                "label": "Bronze",
                "isCorrect": false
              }
            ]
          }
        },
        {
          "id": "en_l4_22",
          "word": "BASKET",
          "syllables": [
            "BAS",
            "KET"
          ],
          "emoji": "🧺",
          "microCheck": {
            "question": "What woven container holds fruit and snacks?",
            "options": [
              {
                "emoji": "🧺",
                "label": "A basket",
                "isCorrect": true
              },
              {
                "emoji": "🪣",
                "label": "A steel bucket",
                "isCorrect": false
              },
              {
                "emoji": "📦",
                "label": "A glass bottle",
                "isCorrect": false
              }
            ]
          }
        },
        {
          "id": "en_l4_23",
          "word": "PENCIL",
          "syllables": [
            "PEN",
            "CIL"
          ],
          "emoji": "✏️",
          "microCheck": {
            "question": "What wooden tool writes with graphite lead?",
            "options": [
              {
                "emoji": "✏️",
                "label": "A pencil",
                "isCorrect": true
              },
              {
                "emoji": "✂️",
                "label": "Scissors",
                "isCorrect": false
              },
              {
                "emoji": "📏",
                "label": "A ruler",
                "isCorrect": false
              }
            ]
          }
        },
        {
          "id": "en_l4_24",
          "word": "CANDLE",
          "syllables": [
            "CAN",
            "DLE"
          ],
          "emoji": "🕯️",
          "microCheck": {
            "question": "What wax stick gives off a small flame?",
            "options": [
              {
                "emoji": "🕯️",
                "label": "A candle",
                "isCorrect": true
              },
              {
                "emoji": "🔦",
                "label": "A flashlight",
                "isCorrect": false
              },
              {
                "emoji": "💡",
                "label": "A lightbulb",
                "isCorrect": false
              }
            ]
          }
        },
        {
          "id": "en_l4_25",
          "word": "DOCTOR",
          "syllables": [
            "DOC",
            "TOR"
          ],
          "emoji": "🩺",
          "microCheck": {
            "question": "Who helps patients feel healthy and well?",
            "options": [
              {
                "emoji": "🩺",
                "label": "A doctor",
                "isCorrect": true
              },
              {
                "emoji": "🧑‍🍳",
                "label": "A baker",
                "isCorrect": false
              },
              {
                "emoji": "🧑‍🎨",
                "label": "A painter",
                "isCorrect": false
              }
            ]
          }
        },
        {
          "id": "en_l4_26",
          "word": "CIRCUS",
          "syllables": [
            "CIR",
            "CUS"
          ],
          "emoji": "🎪",
          "microCheck": {
            "question": "Where do acrobats and clowns perform shows?",
            "options": [
              {
                "emoji": "🎪",
                "label": "The circus",
                "isCorrect": true
              },
              {
                "emoji": "🏦",
                "label": "The bank",
                "isCorrect": false
              },
              {
                "emoji": "✈️",
                "label": "The airport",
                "isCorrect": false
              }
            ]
          }
        }
      ]
    }
  },
  "sentenceBank": {
    "es": {
      "l5": [
        {
          "id": "es_l5_01",
          "lines": [
            "El gato duerme tranquilo",
            "sobre el suave sofá de lana."
          ],
          "wordCount": 10,
          "microCheck": {
            "question": "¿Dónde duerme el gato tranquilo?",
            "options": [
              {
                "icon": "🛋️",
                "label": "Sobre el sofá",
                "isCorrect": true
              },
              {
                "icon": "🌳",
                "label": "En un árbol alto",
                "isCorrect": false
              },
              {
                "icon": "🧺",
                "label": "Dentro de una cesta",
                "isCorrect": false
              }
            ]
          }
        },
        {
          "id": "es_l5_02",
          "lines": [
            "La niña lee un cuento alegre",
            "antes de apagar la luz."
          ],
          "wordCount": 11,
          "microCheck": {
            "question": "¿Qué hace la niña antes de dormir?",
            "options": [
              {
                "icon": "📖",
                "label": "Lee un cuento",
                "isCorrect": true
              },
              {
                "icon": "🎨",
                "label": "Pinta un cuadro",
                "isCorrect": false
              },
              {
                "icon": "🥣",
                "label": "Prepara la cena",
                "isCorrect": false
              }
            ]
          }
        },
        {
          "id": "es_l5_03",
          "lines": [
            "El sol brilla en el cielo",
            "y calienta las flores del jardín."
          ],
          "wordCount": 12,
          "microCheck": {
            "question": "¿Qué calienta el sol brillante?",
            "options": [
              {
                "icon": "🌸",
                "label": "Las flores del jardín",
                "isCorrect": true
              },
              {
                "icon": "❄️",
                "label": "Los copos de nieve",
                "isCorrect": false
              },
              {
                "icon": "🚗",
                "label": "Las ruedas de un coche",
                "isCorrect": false
              }
            ]
          }
        },
        {
          "id": "es_l5_04",
          "lines": [
            "El perro busca su pelota roja",
            "debajo de la mesa redonda."
          ],
          "wordCount": 11,
          "microCheck": {
            "question": "¿De qué color es la pelota del perro?",
            "options": [
              {
                "icon": "🔴",
                "label": "De color rojo",
                "isCorrect": true
              },
              {
                "icon": "🔵",
                "label": "De color azul",
                "isCorrect": false
              },
              {
                "icon": "🟢",
                "label": "De color verde",
                "isCorrect": false
              }
            ]
          }
        },
        {
          "id": "es_l5_05",
          "lines": [
            "Los pájaros cantan al amanecer",
            "en las ramas más altas del bosque."
          ],
          "wordCount": 12,
          "microCheck": {
            "question": "¿Cuándo cantan los pájaros alegres?",
            "options": [
              {
                "icon": "🌅",
                "label": "Al amanecer",
                "isCorrect": true
              },
              {
                "icon": "🌙",
                "label": "A medianoche",
                "isCorrect": false
              },
              {
                "icon": "🌧️",
                "label": "Durante una tormenta",
                "isCorrect": false
              }
            ]
          }
        },
        {
          "id": "es_l5_06",
          "lines": [
            "El barco blanco navega despacio",
            "por las olas del mar azul."
          ],
          "wordCount": 11,
          "microCheck": {
            "question": "¿Por dónde navega el barco blanco?",
            "options": [
              {
                "icon": "🌊",
                "label": "Por las olas del mar",
                "isCorrect": true
              },
              {
                "icon": "🛤️",
                "label": "Por las vías del tren",
                "isCorrect": false
              },
              {
                "icon": "☁️",
                "label": "Por encima de las nubes",
                "isCorrect": false
              }
            ]
          }
        },
        {
          "id": "es_l5_07",
          "lines": [
            "Mi hermano prepara zumo de naranja",
            "para desayunar con pan tostado."
          ],
          "wordCount": 11,
          "microCheck": {
            "question": "¿De qué fruta prepara el zumo?",
            "options": [
              {
                "icon": "🍊",
                "label": "De naranja",
                "isCorrect": true
              },
              {
                "icon": "🍎",
                "label": "De manzana",
                "isCorrect": false
              },
              {
                "icon": "🍇",
                "label": "De uva",
                "isCorrect": false
              }
            ]
          }
        },
        {
          "id": "es_l5_08",
          "lines": [
            "La cometa amarilla vuela muy alto",
            "empujada por la brisa fresca."
          ],
          "wordCount": 11,
          "microCheck": {
            "question": "¿De qué color es la cometa que vuela?",
            "options": [
              {
                "icon": "🟡",
                "label": "Amarilla",
                "isCorrect": true
              },
              {
                "icon": "🟣",
                "label": "Morada",
                "isCorrect": false
              },
              {
                "icon": "⚪",
                "label": "Blanca",
                "isCorrect": false
              }
            ]
          }
        },
        {
          "id": "es_l5_09",
          "lines": [
            "El tren veloz llega a la estación",
            "haciendo sonar su alegre silbato."
          ],
          "wordCount": 12,
          "microCheck": {
            "question": "¿A dónde llega el tren veloz?",
            "options": [
              {
                "icon": "🚉",
                "label": "A la estación",
                "isCorrect": true
              },
              {
                "icon": "🏖️",
                "label": "A la playa",
                "isCorrect": false
              },
              {
                "icon": "🎪",
                "label": "Al circo",
                "isCorrect": false
              }
            ]
          }
        },
        {
          "id": "es_l5_10",
          "lines": [
            "Las abejas recogen el dulce néctar",
            "de las flores de primavera."
          ],
          "wordCount": 11,
          "microCheck": {
            "question": "¿Quién recoge el néctar de las flores?",
            "options": [
              {
                "icon": "🐝",
                "label": "Las abejas",
                "isCorrect": true
              },
              {
                "icon": "🦋",
                "label": "Las orugas",
                "isCorrect": false
              },
              {
                "icon": "🐌",
                "label": "Los caracoles",
                "isCorrect": false
              }
            ]
          }
        },
        {
          "id": "es_l5_11",
          "lines": [
            "El oso pardo busca miel fresca",
            "en el hueco de un roble."
          ],
          "wordCount": 12,
          "microCheck": {
            "question": "¿Qué alimento busca el oso pardo?",
            "options": [
              {
                "icon": "🍯",
                "label": "Miel fresca",
                "isCorrect": true
              },
              {
                "icon": "🐟",
                "label": "Pescado frito",
                "isCorrect": false
              },
              {
                "icon": "🥖",
                "label": "Pan crujiente",
                "isCorrect": false
              }
            ]
          }
        },
        {
          "id": "es_l5_12",
          "lines": [
            "La luna ilumina los caminos",
            "cuando cae la noche silenciosa."
          ],
          "wordCount": 10,
          "microCheck": {
            "question": "¿Qué ilumina la luna por la noche?",
            "options": [
              {
                "icon": "🛣️",
                "label": "Los caminos",
                "isCorrect": true
              },
              {
                "icon": "🏊",
                "label": "El fondo de la piscina",
                "isCorrect": false
              },
              {
                "icon": "🕳️",
                "label": "Una cueva oscura",
                "isCorrect": false
              }
            ]
          }
        },
        {
          "id": "es_l5_13",
          "lines": [
            "El caracol pasea muy despacio",
            "llevando su casita a cuestas."
          ],
          "wordCount": 10,
          "microCheck": {
            "question": "¿Cómo se mueve el caracol?",
            "options": [
              {
                "icon": "🐌",
                "label": "Muy despacio",
                "isCorrect": true
              },
              {
                "icon": "⚡",
                "label": "A toda velocidad",
                "isCorrect": false
              },
              {
                "icon": "🦘",
                "label": "Dando saltos gigantes",
                "isCorrect": false
              }
            ]
          }
        },
        {
          "id": "es_l5_14",
          "lines": [
            "La lluvia moja los tejados rojos",
            "y llena de charcos el patio."
          ],
          "wordCount": 12,
          "microCheck": {
            "question": "¿De qué se llena el patio con la lluvia?",
            "options": [
              {
                "icon": "💦",
                "label": "De charcos",
                "isCorrect": true
              },
              {
                "icon": "🍂",
                "label": "De hojas secas",
                "isCorrect": false
              },
              {
                "icon": "🎈",
                "label": "De globos de colores",
                "isCorrect": false
              }
            ]
          }
        },
        {
          "id": "es_l5_15",
          "lines": [
            "La ardilla guarda ricas castañas",
            "para comer en los días de frío."
          ],
          "wordCount": 12,
          "microCheck": {
            "question": "¿Qué fruto guarda la ardilla previsora?",
            "options": [
              {
                "icon": "🌰",
                "label": "Castañas",
                "isCorrect": true
              },
              {
                "icon": "🍓",
                "label": "Fresas silvestres",
                "isCorrect": false
              },
              {
                "icon": "🌽",
                "label": "Mazorcas de maíz",
                "isCorrect": false
              }
            ]
          }
        },
        {
          "id": "es_l5_16",
          "lines": [
            "Los niños construyen un castillo",
            "con arena mojada en la orilla."
          ],
          "wordCount": 11,
          "microCheck": {
            "question": "¿Con qué construyen el castillo los niños?",
            "options": [
              {
                "icon": "🏖️",
                "label": "Con arena mojada",
                "isCorrect": true
              },
              {
                "icon": "🧱",
                "label": "Con bloques de piedra",
                "isCorrect": false
              },
              {
                "icon": "🪵",
                "label": "Con ramas secas",
                "isCorrect": false
              }
            ]
          }
        },
        {
          "id": "es_l5_17",
          "lines": [
            "El búho abre sus grandes ojos",
            "para vigilar el bosque dormido."
          ],
          "wordCount": 11,
          "microCheck": {
            "question": "¿Qué vigila el búho de noche?",
            "options": [
              {
                "icon": "🌲",
                "label": "El bosque dormido",
                "isCorrect": true
              },
              {
                "icon": "🏙️",
                "label": "La gran ciudad",
                "isCorrect": false
              },
              {
                "icon": "🚢",
                "label": "El puerto marino",
                "isCorrect": false
              }
            ]
          }
        },
        {
          "id": "es_l5_18",
          "lines": [
            "La cocinera hornea galletas de miel",
            "que huelen delicioso en toda la casa."
          ],
          "wordCount": 13,
          "microCheck": {
            "question": "¿De qué sabor son las galletas del horno?",
            "options": [
              {
                "icon": "🍯",
                "label": "De miel",
                "isCorrect": true
              },
              {
                "icon": "🍫",
                "label": "De chocolate amargo",
                "isCorrect": false
              },
              {
                "icon": "🧂",
                "label": "De queso y sal",
                "isCorrect": false
              }
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
              {
                "icon": "🎶",
                "label": "Cantando silbidos",
                "isCorrect": true
              },
              {
                "icon": "🔦",
                "label": "Con destellos de luz",
                "isCorrect": false
              },
              {
                "icon": "🤫",
                "label": "Nadando en silencio",
                "isCorrect": false
              }
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
              {
                "icon": "🌾",
                "label": "En harina",
                "isCorrect": true
              },
              {
                "icon": "🍞",
                "label": "En pan horneado",
                "isCorrect": false
              },
              {
                "icon": "🥣",
                "label": "En sopa caliente",
                "isCorrect": false
              }
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
              {
                "icon": "🍃",
                "label": "Para camuflarse entre hojas",
                "isCorrect": true
              },
              {
                "icon": "😴",
                "label": "Para dormir más abrigados",
                "isCorrect": false
              },
              {
                "icon": "🏃",
                "label": "Para correr más deprisa",
                "isCorrect": false
              }
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
              {
                "icon": "🌍",
                "label": "La Tierra azul",
                "isCorrect": true
              },
              {
                "icon": "☄️",
                "label": "Un cometa de hielo",
                "isCorrect": false
              },
              {
                "icon": "👽",
                "label": "Un platillo volante",
                "isCorrect": false
              }
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
              {
                "icon": "🦋",
                "label": "En una hermosa mariposa",
                "isCorrect": true
              },
              {
                "icon": "🐝",
                "label": "En una abeja obrera",
                "isCorrect": false
              },
              {
                "icon": "🐞",
                "label": "En una mariquita roja",
                "isCorrect": false
              }
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
              {
                "icon": "⛵",
                "label": "A los marineros que navegan",
                "isCorrect": true
              },
              {
                "icon": "✈️",
                "label": "A los pilotos de avión",
                "isCorrect": false
              },
              {
                "icon": "🚗",
                "label": "A los conductores de camiones",
                "isCorrect": false
              }
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
              {
                "icon": "🌱",
                "label": "Semillas de plantas",
                "isCorrect": true
              },
              {
                "icon": "🪨",
                "label": "Piedras pesadas",
                "isCorrect": false
              },
              {
                "icon": "💧",
                "label": "Gotas de rocío",
                "isCorrect": false
              }
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
              {
                "icon": "📚",
                "label": "De libros de aventuras",
                "isCorrect": true
              },
              {
                "icon": "🧸",
                "label": "De juguetes antiguos",
                "isCorrect": false
              },
              {
                "icon": "🏆",
                "label": "De trofeos dorados",
                "isCorrect": false
              }
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
              {
                "icon": "☁️",
                "label": "A algodón blanco",
                "isCorrect": true
              },
              {
                "icon": "🍦",
                "label": "A helado de fresa",
                "isCorrect": false
              },
              {
                "icon": "🪨",
                "label": "A piedras grises",
                "isCorrect": false
              }
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
              {
                "icon": "🏔️",
                "label": "Desde las cumbres heladas",
                "isCorrect": true
              },
              {
                "icon": "🏜️",
                "label": "Desde el desierto árido",
                "isCorrect": false
              },
              {
                "icon": "🌋",
                "label": "Desde el cráter de un volcán",
                "isCorrect": false
              }
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
              {
                "icon": "❤️",
                "label": "Tres corazones",
                "isCorrect": true
              },
              {
                "icon": "1️⃣",
                "label": "Un solo corazón",
                "isCorrect": false
              },
              {
                "icon": "5️⃣",
                "label": "Cinco corazones",
                "isCorrect": false
              }
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
              {
                "icon": "🎻",
                "label": "Un suave violín",
                "isCorrect": true
              },
              {
                "icon": "🥁",
                "label": "Un fuerte tambor",
                "isCorrect": false
              },
              {
                "icon": "🎺",
                "label": "Una trompeta brillante",
                "isCorrect": false
              }
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
              {
                "icon": "🧡",
                "label": "Rayas naranjas",
                "isCorrect": true
              },
              {
                "icon": "🖤",
                "label": "Rayas negras",
                "isCorrect": false
              },
              {
                "icon": "💚",
                "label": "Rayas verdes",
                "isCorrect": false
              }
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
              {
                "icon": "🪵",
                "label": "Con ramas y barro",
                "isCorrect": true
              },
              {
                "icon": "🧱",
                "label": "Con piedras y cemento",
                "isCorrect": false
              },
              {
                "icon": "🌾",
                "label": "Con paja seca",
                "isCorrect": false
              }
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
              {
                "icon": "🍃",
                "label": "De hojas de eucalipto",
                "isCorrect": true
              },
              {
                "icon": "🍌",
                "label": "De plátanos maduros",
                "isCorrect": false
              },
              {
                "icon": "🌾",
                "label": "De granos de trigo",
                "isCorrect": false
              }
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
              {
                "icon": "✨",
                "label": "Una estela dorada",
                "isCorrect": true
              },
              {
                "icon": "💨",
                "label": "Una nube de humo negro",
                "isCorrect": false
              },
              {
                "icon": "🌧️",
                "label": "Un rastro de lluvia",
                "isCorrect": false
              }
            ]
          }
        }
      ]
    },
    "en": {
      "l5": [
        {
          "id": "en_l5_01",
          "lines": [
            "The black cat sleeps peacefully",
            "on the soft wool rug."
          ],
          "wordCount": 11,
          "microCheck": {
            "question": "Where is the cat sleeping peacefully?",
            "options": [
              {
                "icon": "🛋️",
                "label": "On the wool rug",
                "isCorrect": true
              },
              {
                "icon": "🌳",
                "label": "Up in a pine tree",
                "isCorrect": false
              },
              {
                "icon": "🚗",
                "label": "Inside the car",
                "isCorrect": false
              }
            ]
          }
        },
        {
          "id": "en_l5_02",
          "lines": [
            "The girl reads a funny book",
            "before switching off her bedroom lamp."
          ],
          "wordCount": 12,
          "microCheck": {
            "question": "What does the girl read before sleep?",
            "options": [
              {
                "icon": "📖",
                "label": "A funny book",
                "isCorrect": true
              },
              {
                "icon": "🗺️",
                "label": "A treasure map",
                "isCorrect": false
              },
              {
                "icon": "📰",
                "label": "A daily newspaper",
                "isCorrect": false
              }
            ]
          }
        },
        {
          "id": "en_l5_03",
          "lines": [
            "The warm sun shines brightly",
            "and warms the flowers in the garden."
          ],
          "wordCount": 12,
          "microCheck": {
            "question": "What does the bright sun warm up?",
            "options": [
              {
                "icon": "🌸",
                "label": "Garden flowers",
                "isCorrect": true
              },
              {
                "icon": "❄️",
                "label": "Winter snowmen",
                "isCorrect": false
              },
              {
                "icon": "🧊",
                "label": "Ice cubes in a glass",
                "isCorrect": false
              }
            ]
          }
        },
        {
          "id": "en_l5_04",
          "lines": [
            "The puppy chases its red ball",
            "across the green grassy lawn."
          ],
          "wordCount": 11,
          "microCheck": {
            "question": "What color is the puppy's ball?",
            "options": [
              {
                "icon": "🔴",
                "label": "Bright red",
                "isCorrect": true
              },
              {
                "icon": "🔵",
                "label": "Dark blue",
                "isCorrect": false
              },
              {
                "icon": "🟡",
                "label": "Sunny yellow",
                "isCorrect": false
              }
            ]
          }
        },
        {
          "id": "en_l5_05",
          "lines": [
            "Wild birds sing sweet songs",
            "in the tallest branches of the forest."
          ],
          "wordCount": 12,
          "microCheck": {
            "question": "Where are the wild birds singing?",
            "options": [
              {
                "icon": "🌳",
                "label": "In tall forest branches",
                "isCorrect": true
              },
              {
                "icon": "🏊",
                "label": "Under the swimming pool",
                "isCorrect": false
              },
              {
                "icon": "🕳️",
                "label": "Deep inside a dark tunnel",
                "isCorrect": false
              }
            ]
          }
        },
        {
          "id": "en_l5_06",
          "lines": [
            "A white sailboat glides gently",
            "over the calm blue sea waves."
          ],
          "wordCount": 11,
          "microCheck": {
            "question": "What is gliding over the sea waves?",
            "options": [
              {
                "icon": "⛵",
                "label": "A white sailboat",
                "isCorrect": true
              },
              {
                "icon": "🚂",
                "label": "A steam locomotive",
                "isCorrect": false
              },
              {
                "icon": "🚜",
                "label": "A heavy green tractor",
                "isCorrect": false
              }
            ]
          }
        },
        {
          "id": "en_l5_07",
          "lines": [
            "My brother squeezes fresh orange juice",
            "to drink with his warm toast."
          ],
          "wordCount": 12,
          "microCheck": {
            "question": "What kind of fruit juice was squeezed?",
            "options": [
              {
                "icon": "🍊",
                "label": "Fresh orange juice",
                "isCorrect": true
              },
              {
                "icon": "🍎",
                "label": "Sweet apple cider",
                "isCorrect": false
              },
              {
                "icon": "🍇",
                "label": "Purple grape juice",
                "isCorrect": false
              }
            ]
          }
        },
        {
          "id": "en_l5_08",
          "lines": [
            "The bright yellow kite flies high,",
            "lifted by the gentle morning breeze."
          ],
          "wordCount": 12,
          "microCheck": {
            "question": "What lifts the yellow kite into the air?",
            "options": [
              {
                "icon": "💨",
                "label": "The morning breeze",
                "isCorrect": true
              },
              {
                "icon": "🌧️",
                "label": "A heavy thunderstorm",
                "isCorrect": false
              },
              {
                "icon": "🚀",
                "label": "A jet rocket motor",
                "isCorrect": false
              }
            ]
          }
        },
        {
          "id": "en_l5_09",
          "lines": [
            "The silver express train arrives",
            "and blows its loud cheerful whistle."
          ],
          "wordCount": 11,
          "microCheck": {
            "question": "What sound does the express train make?",
            "options": [
              {
                "icon": "📢",
                "label": "Its loud whistle",
                "isCorrect": true
              },
              {
                "icon": "🔔",
                "label": "A soft church bell",
                "isCorrect": false
              },
              {
                "icon": "🎸",
                "label": "A rock guitar tune",
                "isCorrect": false
              }
            ]
          }
        },
        {
          "id": "en_l5_10",
          "lines": [
            "Busy worker bees collect sweet nectar",
            "from colorful blooming spring flowers."
          ],
          "wordCount": 11,
          "microCheck": {
            "question": "Who collects sweet nectar from flowers?",
            "options": [
              {
                "icon": "🐝",
                "label": "Busy worker bees",
                "isCorrect": true
              },
              {
                "icon": "🐜",
                "label": "Tiny black ants",
                "isCorrect": false
              },
              {
                "icon": "🦗",
                "label": "Singing green crickets",
                "isCorrect": false
              }
            ]
          }
        },
        {
          "id": "en_l5_11",
          "lines": [
            "The brown bear searches for honey",
            "inside the hollow of an oak tree."
          ],
          "wordCount": 13,
          "microCheck": {
            "question": "What food is the brown bear searching for?",
            "options": [
              {
                "icon": "🍯",
                "label": "Sweet golden honey",
                "isCorrect": true
              },
              {
                "icon": "🥖",
                "label": "Loaves of crusty bread",
                "isCorrect": false
              },
              {
                "icon": "🍫",
                "label": "Bars of dark chocolate",
                "isCorrect": false
              }
            ]
          }
        },
        {
          "id": "en_l5_12",
          "lines": [
            "The silver moon lights the paths",
            "as silent night falls over town."
          ],
          "wordCount": 12,
          "microCheck": {
            "question": "What lights the paths when night arrives?",
            "options": [
              {
                "icon": "🌙",
                "label": "The silver moon",
                "isCorrect": true
              },
              {
                "icon": "🕯️",
                "label": "A single candle flame",
                "isCorrect": false
              },
              {
                "icon": "🔦",
                "label": "A police searchlight",
                "isCorrect": false
              }
            ]
          }
        },
        {
          "id": "en_l5_13",
          "lines": [
            "The garden snail crawls very slowly,",
            "carrying its spiral shell on its back."
          ],
          "wordCount": 13,
          "microCheck": {
            "question": "What does the garden snail carry?",
            "options": [
              {
                "icon": "🐌",
                "label": "Its spiral shell",
                "isCorrect": true
              },
              {
                "icon": "🎒",
                "label": "A leather backpack",
                "isCorrect": false
              },
              {
                "icon": "🧳",
                "label": "A heavy metal suitcase",
                "isCorrect": false
              }
            ]
          }
        },
        {
          "id": "en_l5_14",
          "lines": [
            "Cold raindrops wet the red roofs",
            "and leave shiny puddles on the ground."
          ],
          "wordCount": 13,
          "microCheck": {
            "question": "What appears on the ground after it rains?",
            "options": [
              {
                "icon": "💦",
                "label": "Shiny puddles",
                "isCorrect": true
              },
              {
                "icon": "🍂",
                "label": "Dry fallen leaves",
                "isCorrect": false
              },
              {
                "icon": "🏖️",
                "label": "Piles of yellow sand",
                "isCorrect": false
              }
            ]
          }
        },
        {
          "id": "en_l5_15",
          "lines": [
            "The nimble squirrel gathers ripe nuts",
            "to store safely for cold winter days."
          ],
          "wordCount": 13,
          "microCheck": {
            "question": "What does the squirrel gather for winter?",
            "options": [
              {
                "icon": "🌰",
                "label": "Ripe nuts",
                "isCorrect": true
              },
              {
                "icon": "🍓",
                "label": "Fresh berries",
                "isCorrect": false
              },
              {
                "icon": "🍄",
                "label": "Wild mushrooms",
                "isCorrect": false
              }
            ]
          }
        },
        {
          "id": "en_l5_16",
          "lines": [
            "Happy children build a sandcastle",
            "with moist sand by the water edge."
          ],
          "wordCount": 12,
          "microCheck": {
            "question": "What are the happy children building?",
            "options": [
              {
                "icon": "🏖️",
                "label": "A sandcastle",
                "isCorrect": true
              },
              {
                "icon": "🛖",
                "label": "A wooden cabin",
                "isCorrect": false
              },
              {
                "icon": "🧱",
                "label": "A stone brick house",
                "isCorrect": false
              }
            ]
          }
        },
        {
          "id": "en_l5_17",
          "lines": [
            "The wise owl opens its golden eyes",
            "to watch over the sleeping woods."
          ],
          "wordCount": 13,
          "microCheck": {
            "question": "What color are the owl's eyes?",
            "options": [
              {
                "icon": "👀",
                "label": "Golden eyes",
                "isCorrect": true
              },
              {
                "icon": "🔵",
                "label": "Bright blue eyes",
                "isCorrect": false
              },
              {
                "icon": "🟢",
                "label": "Green emerald eyes",
                "isCorrect": false
              }
            ]
          }
        },
        {
          "id": "en_l5_18",
          "lines": [
            "The baker bakes warm honey biscuits",
            "that smell delicious across the entire kitchen."
          ],
          "wordCount": 13,
          "microCheck": {
            "question": "What delicious treat is the baker baking?",
            "options": [
              {
                "icon": "🍪",
                "label": "Warm honey biscuits",
                "isCorrect": true
              },
              {
                "icon": "🍕",
                "label": "Spicy cheese pizza",
                "isCorrect": false
              },
              {
                "icon": "🥧",
                "label": "Cold pumpkin pie",
                "isCorrect": false
              }
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
              {
                "icon": "🎶",
                "label": "By whistling tunes",
                "isCorrect": true
              },
              {
                "icon": "🔦",
                "label": "With bright flashes of light",
                "isCorrect": false
              },
              {
                "icon": "🤫",
                "label": "By swimming in silence",
                "isCorrect": false
              }
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
              {
                "icon": "🌾",
                "label": "Fine white flour",
                "isCorrect": true
              },
              {
                "icon": "🍞",
                "label": "Fresh baked bread",
                "isCorrect": false
              },
              {
                "icon": "🥣",
                "label": "Warm breakfast cereal",
                "isCorrect": false
              }
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
              {
                "icon": "🍃",
                "label": "To hide among leaves",
                "isCorrect": true
              },
              {
                "icon": "😴",
                "label": "To stay warm while sleeping",
                "isCorrect": false
              },
              {
                "icon": "🏃",
                "label": "To run faster from birds",
                "isCorrect": false
              }
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
              {
                "icon": "🌍",
                "label": "Our blue planet Earth",
                "isCorrect": true
              },
              {
                "icon": "☄️",
                "label": "A frozen flying comet",
                "isCorrect": false
              },
              {
                "icon": "👽",
                "label": "An alien spacecraft",
                "isCorrect": false
              }
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
              {
                "icon": "🦋",
                "label": "A painted butterfly",
                "isCorrect": true
              },
              {
                "icon": "🐝",
                "label": "A honeybee",
                "isCorrect": false
              },
              {
                "icon": "🐞",
                "label": "A spotted ladybug",
                "isCorrect": false
              }
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
              {
                "icon": "⛵",
                "label": "Sailors navigating at sea",
                "isCorrect": true
              },
              {
                "icon": "✈️",
                "label": "Airplane pilots in fog",
                "isCorrect": false
              },
              {
                "icon": "🚗",
                "label": "Highway truck drivers",
                "isCorrect": false
              }
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
              {
                "icon": "🌱",
                "label": "A plant seed",
                "isCorrect": true
              },
              {
                "icon": "🪨",
                "label": "Heavy pebbles",
                "isCorrect": false
              },
              {
                "icon": "💧",
                "label": "Morning dew drops",
                "isCorrect": false
              }
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
              {
                "icon": "📚",
                "label": "Books of adventure and discovery",
                "isCorrect": true
              },
              {
                "icon": "🧸",
                "label": "Vintage wooden toys",
                "isCorrect": false
              },
              {
                "icon": "🏆",
                "label": "Gold sports medals",
                "isCorrect": false
              }
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
              {
                "icon": "☁️",
                "label": "Fluffy white cotton",
                "isCorrect": true
              },
              {
                "icon": "🍦",
                "label": "Sweet strawberry ice cream",
                "isCorrect": false
              },
              {
                "icon": "🪨",
                "label": "Dark jagged granite stones",
                "isCorrect": false
              }
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
              {
                "icon": "🏔️",
                "label": "From cold glacier peaks",
                "isCorrect": true
              },
              {
                "icon": "🏜️",
                "label": "From an arid desert dune",
                "isCorrect": false
              },
              {
                "icon": "🌋",
                "label": "From an active volcano cone",
                "isCorrect": false
              }
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
              {
                "icon": "❤️",
                "label": "Three hearts",
                "isCorrect": true
              },
              {
                "icon": "1️⃣",
                "label": "Only one heart",
                "isCorrect": false
              },
              {
                "icon": "5️⃣",
                "label": "Five hearts",
                "isCorrect": false
              }
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
              {
                "icon": "🎻",
                "label": "A gentle violin",
                "isCorrect": true
              },
              {
                "icon": "🥁",
                "label": "A loud bass drum",
                "isCorrect": false
              },
              {
                "icon": "🎺",
                "label": "A brass trumpet",
                "isCorrect": false
              }
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
              {
                "icon": "🧡",
                "label": "Bright orange stripes",
                "isCorrect": true
              },
              {
                "icon": "🖤",
                "label": "Deep black stripes",
                "isCorrect": false
              },
              {
                "icon": "💚",
                "label": "Emerald green stripes",
                "isCorrect": false
              }
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
              {
                "icon": "🪵",
                "label": "Branches and thick mud",
                "isCorrect": true
              },
              {
                "icon": "🧱",
                "label": "Bricks and steel rods",
                "isCorrect": false
              },
              {
                "icon": "🌾",
                "label": "Dry straw and reeds",
                "isCorrect": false
              }
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
              {
                "icon": "🍃",
                "label": "Eucalyptus leaves",
                "isCorrect": true
              },
              {
                "icon": "🍌",
                "label": "Ripe yellow bananas",
                "isCorrect": false
              },
              {
                "icon": "🌾",
                "label": "Golden barley grains",
                "isCorrect": false
              }
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
              {
                "icon": "✨",
                "label": "A glowing golden streak",
                "isCorrect": true
              },
              {
                "icon": "💨",
                "label": "A dark cloud of dust",
                "isCorrect": false
              },
              {
                "icon": "🌧️",
                "label": "A gentle shower of rain",
                "isCorrect": false
              }
            ]
          }
        }
      ]
    }
  },
  "i18n": {
    "es": {
      "app_title": "Lector Arcade",
      "app_subtitle": "Aventura lúdica de lectura para niños y familias",
      "tab_play": "🎮 Jugar",
      "tab_learn": "💡 Aprender",
      "tab_achievements": "🏆 Logros",
      "choose_level": "1. Elige tu Nivel",
      "choose_mode": "2. Elige el Modo de Juego",
      "start_game": "¡A Leer! 🚀",
      "back_menu": "← Menú",
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
      "sound_toggle": "Sonido (M)",
      "theme_toggle": "Tema (T)",
      "font_case_toggle": "Letra (AA/Aa)",
      "syllable_toggle": "Sílabas (🎨)",
      "listen_btn": "Escuchar 🔊",
      "listen_slow_btn": "Escuchar Despacio 🐢",
      "read_done_btn": "¡Leído! ✅",
      "clear_letter_btn": "Borrar ⌫",
      "install_app": "Instalar App",
      "install_app_title": "Instalar Lector Arcade en tu pantalla de inicio",
      "install_success": "¡Lector Arcade instalado con éxito! 🎉",
      "install_ios_tip": "En Safari iOS: pulsa Compartir (⬆️) y \"Añadir a pantalla de inicio\"",
      "install_generic_tip": "Pulsa el menú (⋮) del navegador y selecciona \"Instalar aplicación\"",
      "update_available": "Nueva versión v1.0.0 disponible",
      "update_now_btn": "Actualizar ahora",
      "checking_update": "Buscando actualizaciones...",
      "up_to_date": "✓ Lector Arcade al día (v1.0.0)",
      "check_update_title": "Buscar actualizaciones de la aplicación (v1.0.0)",
      "stats_reset_toast": "Estadísticas y medallas reiniciadas con éxito",
      "correct_answer_is": "Lectura correcta:",
      "next_question_btn": "Siguiente ➔",
      "share_result_btn": "📤 Compartir Resultado",
      "share_result_copied": "¡Tarjeta de lectura copiada al portapapeles! 📋",
      "mistake_review_title": "🧠 Repaso de Palabras de la Ronda",
      "mistake_review_empty": "¡Lectura impecable! Cero fallos que repasar. 🌟",
      "mistake_your_answer": "Tu intento:",
      "mistake_correct_answer": "Palabra o frase:",
      "view_hint_btn": "Ver Pista 💡",
      "daily_challenge_label": "Reto Diario",
      "profile_label": "Perfil:",
      "profile_switched": "Cambiado a perfil:",
      "download_diploma_btn": "🎓 Descargar Diploma (PNG)",
      "diploma_downloaded_toast": "¡Diploma de Lector descargado con éxito! 🎓",
      "diploma_card_title": "Diploma Arcade de Lectura",
      "diploma_card_desc": "Genera un certificado oficial en PNG de alta resolución con tus medallas y velocidad lectora (PPM).",
      "datalaria_back": "← Datalaria",
      "post_link": "📖 Historia IA",
      "spec_link": "📋 Ficha App",
      "kits_link": "📦 Recursos",
      "wpm_label": "PPM",
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
    },
    "en": {
      "app_title": "Reader Arcade",
      "app_subtitle": "Playful reading adventure for kids & families",
      "tab_play": "🎮 Play",
      "tab_learn": "💡 Learn",
      "tab_achievements": "🏆 Badges",
      "choose_level": "1. Choose your Level",
      "choose_mode": "2. Choose Game Mode",
      "start_game": "Start Reading! 🚀",
      "back_menu": "← Menu",
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
      "sound_toggle": "Sound (M)",
      "theme_toggle": "Theme (T)",
      "font_case_toggle": "Font (AA/Aa)",
      "syllable_toggle": "Syllables (🎨)",
      "listen_btn": "Listen 🔊",
      "listen_slow_btn": "Listen Slow 🐢",
      "read_done_btn": "Done! ✅",
      "clear_letter_btn": "Erase ⌫",
      "install_app": "Install App",
      "install_app_title": "Install Reader Arcade on your home screen",
      "install_success": "Reader Arcade successfully installed! 🎉",
      "install_ios_tip": "In Safari iOS: tap Share (⬆️) and select \"Add to Home Screen\"",
      "install_generic_tip": "Tap browser menu (⋮) and select \"Install app\"",
      "update_available": "New version v1.0.0 available",
      "update_now_btn": "Update now",
      "checking_update": "Checking for updates...",
      "up_to_date": "✓ Reader Arcade is up to date (v1.0.0)",
      "check_update_title": "Check for app updates (v1.0.0)",
      "stats_reset_toast": "Stats and badges reset successfully",
      "correct_answer_is": "Correct reading:",
      "next_question_btn": "Next ➔",
      "share_result_btn": "📤 Share Result",
      "share_result_copied": "Reading score card copied to clipboard! 📋",
      "mistake_review_title": "🧠 Round Word Review",
      "mistake_review_empty": "Flawless reading! Zero mistakes to review. 🌟",
      "mistake_your_answer": "Your attempt:",
      "mistake_correct_answer": "Word or sentence:",
      "view_hint_btn": "View Hint 💡",
      "daily_challenge_label": "Daily Challenge",
      "profile_label": "Profile:",
      "profile_switched": "Switched to profile:",
      "download_diploma_btn": "🎓 Download Diploma (PNG)",
      "diploma_downloaded_toast": "Reader Diploma downloaded successfully! 🎓",
      "diploma_card_title": "Arcade Reading Diploma",
      "diploma_card_desc": "Generate an official high-resolution PNG certificate with your badges and reading speed (WPM).",
      "datalaria_back": "← Datalaria",
      "post_link": "📖 AI Story",
      "spec_link": "📋 App Spec",
      "kits_link": "📦 Resources",
      "wpm_label": "WPM",
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
  }
};
