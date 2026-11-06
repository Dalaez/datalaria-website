// apps/flashcards/catalog.js
// Catálogo de Mazos Curados, Modos de Juego, Medallas y Diccionarios i18n
// Datalaria Flashcards AI ("Mazo Mágico v2.0")

export const PRESET_DECKS = [
  {
    id: 'body_science',
    tier: 'kids',
    icon: '🦴',
    title: {
      es: 'Ciencias Bilingües: El Cuerpo Humano',
      en: 'Bilingual Science: The Human Body'
    },
    description: {
      es: 'Aprende los huesos, órganos y articulaciones en inglés con fonética clara.',
      en: 'Master bones, organs, and joints in English with phonetic pronunciation.'
    },
    langFront: 'es',
    langBack: 'en',
    cards: [
      { front: 'Articulaciones', back: 'Joints', phonetic: '/dʒɔɪnts/', hint: 'Lugares donde se unen dos huesos' },
      { front: 'Columna vertebral', back: 'Spinal column', phonetic: '/ˈspaɪ.nəl ˈkɒl.əm/', hint: 'Eje central que protege la médula' },
      { front: 'Cráneo', back: 'Skull', phonetic: '/skʌl/', hint: 'Protege el cerebro' },
      { front: 'Costillas', back: 'Ribs', phonetic: '/rɪbz/', hint: 'Protegen el corazón y los pulmones' },
      { front: 'Pulmones', back: 'Lungs', phonetic: '/lʌŋz/', hint: 'Órganos para la respiración' },
      { front: 'Fémur', back: 'Femur', phonetic: '/ˈfiː.mər/', hint: 'El hueso más largo del cuerpo' },
      { front: 'Corazón', back: 'Heart', phonetic: '/hɑːt/', hint: 'Bomba de sangre muscular' },
      { front: 'Cerebro', back: 'Brain', phonetic: '/breɪn/', hint: 'Centro de control del sistema nervioso' },
      { front: 'Músculos', back: 'Muscles', phonetic: '/ˈmʌs.əlz/', hint: 'Permiten el movimiento del esqueleto' },
      { front: 'Hígado', back: 'Liver', phonetic: '/ˈlɪv.ər/', hint: 'Filtra toxinas y produce bilis' }
    ]
  },
  {
    id: 'space_nature',
    tier: 'kids',
    icon: '🪐',
    title: {
      es: 'Exploradores del Espacio & Naturaleza',
      en: 'Space & Nature Explorers'
    },
    description: {
      es: 'Planetas, fenómenos astronómicos y maravillas de la biología.',
      en: 'Planets, astronomical phenomena, and natural wonders.'
    },
    langFront: 'es',
    langBack: 'en',
    cards: [
      { front: 'Fotosíntesis', back: 'Photosynthesis', phonetic: '/ˌfəʊ.təʊˈsɪn.θə.sɪs/', hint: 'Proceso de plantas con luz solar' },
      { front: 'Vía Láctea', back: 'Milky Way', phonetic: '/ˈmɪl.ki weɪ/', hint: 'Nuestra galaxia espiral' },
      { front: 'Gravedad', back: 'Gravity', phonetic: '/ˈɡræv.ə.ti/', hint: 'Fuerza que atrae los cuerpos' },
      { front: 'Agujero negro', back: 'Black hole', phonetic: '/blæk həʊl/', hint: 'Región donde nada escapa, ni la luz' },
      { front: 'Ecosistema', back: 'Ecosystem', phonetic: '/ˈiː.kəʊˌsɪs.təm/', hint: 'Comunidad de seres vivos y su entorno' },
      { front: 'Atmósfera', back: 'Atmosphere', phonetic: '/ˈæt.məs.fɪər/', hint: 'Capa gaseosa protectora del planeta' },
      { front: 'Biodiversidad', back: 'Biodiversity', phonetic: '/ˌbaɪ.əʊ.daɪˈvɜː.sə.ti/', hint: 'Variedad de vida en la Tierra' },
      { front: 'Cometa', back: 'Comet', phonetic: '/ˈkɒm.ɪt/', hint: 'Cuerpo celeste de hielo y polvo con cola' }
    ]
  },
  {
    id: 'world_capitals',
    tier: 'kids',
    icon: '🌍',
    title: {
      es: 'Capitales y Maravillas del Mundo',
      en: 'World Capitals & Wonders'
    },
    description: {
      es: 'Desafío geográfico con pistas culturales de cada rincón del planeta.',
      en: 'Geography challenge with cultural hints from across the globe.'
    },
    langFront: 'es',
    langBack: 'es',
    cards: [
      { front: 'Japón', back: 'Tokio', phonetic: '[To-kio]', hint: 'Metrópolis vanguardista junto al monte Fuji' },
      { front: 'Australia', back: 'Canberra', phonetic: '[Can-be-rra]', hint: 'No es Sídney ni Melbourne, elegida por consenso' },
      { front: 'Canadá', back: 'Ottawa', phonetic: '[O-tta-wa]', hint: 'Ciudad federal entre Quebec y Ontario' },
      { front: 'Brasil', back: 'Brasilia', phonetic: '[Bra-si-lia]', hint: 'Diseñada con forma de avión por Oscar Niemeyer' },
      { front: 'Islandia', back: 'Reikiavik', phonetic: '[Rei-kia-vik]', hint: 'La capital más septentrional del mundo' },
      { front: 'Sudáfrica', back: 'Pretoria (Ejecutiva)', phonetic: '[Pre-to-ria]', hint: 'Tiene 3 capitales: Pretoria, Ciudad del Cabo y Bloemfontein' },
      { front: 'Turquía', back: 'Ankara', phonetic: '[An-ka-ra]', hint: 'Capital política en el corazón de Anatolia, no Estambul' },
      { front: 'Egipto', back: 'El Cairo', phonetic: '[El Cai-ro]', hint: 'La ciudad de los mil minaretes a orillas del Nilo' }
    ]
  },
  {
    id: 'business_english',
    tier: 'adults',
    icon: '💼',
    title: {
      es: 'Business & Tech English (Falsos Amigos)',
      en: 'Business & Tech English (False Friends)'
    },
    description: {
      es: 'Domina los términos en inglés que más inducen a error en entornos profesionales.',
      en: 'Master tricky English terms and false friends in professional settings.'
    },
    langFront: 'en',
    langBack: 'es',
    cards: [
      { front: 'Actually', back: 'En realidad / De hecho (NO actualmente)', phonetic: '/ˈæk.tʃu.ə.li/', hint: 'Usa "currently" para actualmente' },
      { front: 'Embarrassed', back: 'Avergonzado / Incómodo (NO embarazada)', phonetic: '/ɪmˈbær.əst/', hint: 'Usa "pregnant" para embarazada' },
      { front: 'Compromise', back: 'Llegar a un acuerdo / Ceder mutuamente', phonetic: '/ˈkɒm.prə.maɪz/', hint: 'Usa "commitment" para compromiso' },
      { front: 'Sensible', back: 'Sensato / Razonable (NO sensible)', phonetic: '/ˈsen.sə.bəl/', hint: 'Usa "sensitive" para sensible emocional' },
      { front: 'Deliverable', back: 'Entregable del proyecto', phonetic: '/dɪˈlɪv.ər.ə.bəl/', hint: 'Producto final pactado en el contrato' },
      { front: 'Throughput', back: 'Capacidad de procesamiento / Rendimiento', phonetic: '/ˈθruː.pʊt/', hint: 'Volumen de trabajo procesado por unidad de tiempo' },
      { front: 'Stakeholder', back: 'Parte interesada / Actor clave', phonetic: '/ˈsteɪkˌhəʊl.dər/', hint: 'Cualquiera afectado por las decisiones del proyecto' },
      { front: 'Bottleneck', back: 'Cuello de botella / Restricción', phonetic: '/ˈbɒt.əl.nek/', hint: 'Etapa que limita el flujo total según la Teoría de Restricciones' }
    ]
  },
  {
    id: 'ai_concepts',
    tier: 'adults',
    icon: '🤖',
    title: {
      es: 'Conceptos Clave de IA & Data Science',
      en: 'Key Concepts in AI & Data Science'
    },
    description: {
      es: 'Terminología moderna de modelos de lenguaje, agentes y computación cuántica.',
      en: 'Modern terminology for LLMs, agents, and applied data science.'
    },
    langFront: 'es',
    langBack: 'es',
    cards: [
      { front: 'RAG (Retrieval-Augmented Generation)', back: 'Inyección de contexto documental externo en el prompt antes de generar respuesta', phonetic: '[R-A-G]', hint: 'Combina base de datos vectorial y LLM para evitar alucinaciones' },
      { front: 'Alucinación (Hallucination)', back: 'Generación de información falsa con alta confianza sintáctica', phonetic: '[A-lu-ci-na-ción]', hint: 'Riesgo probabilístico inherente al modelo de lenguaje' },
      { front: 'Overfitting (Sobreajuste)', back: 'El modelo memoriza el ruido de entrenamiento y no generaliza ante datos nuevos', phonetic: '[O-ver-fi-tting]', hint: 'Se detecta cuando la pérdida de validación empieza a subir' },
      { front: 'Embeddings', back: 'Vectores matemáticos densos que representan significado semántico en n-dimensiones', phonetic: '[Em-be-ddings]', hint: 'Palabras afines quedan geométricamente cerca (coseno)' },
      { front: 'Spec-Driven Development (SDD)', back: 'Desarrollo donde la especificación inmutable precede y gobierna la generación de código', phonetic: '[S-D-D]', hint: 'Constitución Datalaria vs Vibe Coding sin memoria' },
      { front: 'Ventana de Contexto (Context Window)', back: 'Número máximo de tokens que el modelo puede retener simultáneamente en memoria', phonetic: '[Con-text Win-dow]', hint: 'Límite operativo de tokens de entrada + salida' },
      { front: 'Temperature (Temperatura)', back: 'Parámetro estocástico que controla la aleatoriedad de muestreo (0 = determinista)', phonetic: '[Tem-pe-ra-tu-ra]', hint: '0 para código y aritmética, 0.7 para redacción creativa' },
      { front: 'Quantization (Cuantización)', back: 'Reducción de precisión de pesos (FP16 a INT8/INT4) para inferencia local rápida', phonetic: '[Quan-ti-za-tion]', hint: 'Reduce el consumo de VRAM manteniendo la calidad' }
    ]
  },
  {
    id: 'mba_strategy',
    tier: 'adults',
    icon: '⚡',
    title: {
      es: 'Productividad, Finanzas & Estrategia MBA',
      en: 'Productivity, Finance & MBA Strategy'
    },
    description: {
      es: 'Métricas financieras, modelos cuantitativos y toma de decisiones ejecutivas.',
      en: 'Financial metrics, quantitative models, and executive decision frameworks.'
    },
    langFront: 'es',
    langBack: 'es',
    cards: [
      { front: 'EBITDA', back: 'Resultado operativo bruto antes de intereses, impuestos, depreciaciones y amortizaciones', phonetic: '[E-bit-da]', hint: 'Mide la rentabilidad operativa pura del negocio' },
      { front: 'Punto de Equilibrio (Break-even)', back: 'Volumen de ventas donde los ingresos igualan exactamente a los costes fijos + variables', phonetic: '[Breik-i-ven]', hint: 'Delta V = d / (m - d) ante descuentos comerciales' },
      { front: 'Coste de Oportunidad', back: 'El beneficio al que se renuncia al elegir una alternativa frente a la mejor descartada', phonetic: '[Cos-te O-por-tu-ni-dad]', hint: 'El coste real de cualquier decisión económica' },
      { front: 'Ley de Little', back: 'WIP = Throughput × Tiempo de Ciclo (L = λ × W en colas y procesos)', phonetic: '[Ley de Li-ttle]', hint: 'Fundamento matemático de Lean, Kanban y operaciones' },
      { front: 'Coste Hundido (Sunk Cost Fallacy)', back: 'Coste no recuperable en el pasado que jamás debe influir en decisiones futuras', phonetic: '[Cos-te Hun-di-do]', hint: 'Ignóralo y evalúa solo flujos de caja incrementales' },
      { front: 'Matriz DAR (CMMI)', back: 'Framework formal ponderado para Análisis y Resolución de Decisiones con veto Must-Have', phonetic: '[D-A-R]', hint: 'Elimina el sesgo de la persona mejor pagada (HiPPO)' }
    ]
  }
];

export const STUDY_MODES = [
  {
    id: 'flip',
    icon: '🎴',
    title: { es: 'Modo Giro 3D', en: '3D Flip Mode' },
    subtitle: { es: 'Active recall clásico con 3 cajas Leitner de dominio', en: 'Classic active recall with 3 Leitner mastery boxes' }
  },
  {
    id: 'quiz',
    icon: '🎯',
    title: { es: 'Modo Quiz Arcade', en: 'Quiz Arcade Mode' },
    subtitle: { es: '4 opciones por tarjeta con distractores automáticos', en: '4 options per card with dynamic distractors' }
  },
  {
    id: 'spelling',
    icon: '✍️',
    title: { es: 'Modo Escritura', en: 'Spelling Mode' },
    subtitle: { es: 'Escribe la respuesta exacta con botón de pistas por letras', en: 'Type the exact answer with letter-by-letter hint reveal' }
  }
];

export const MEDALS = [
  {
    id: 'first_session',
    icon: '🌱',
    title: { es: 'Primeros Pasos', en: 'First Steps' },
    description: { es: 'Completa tu primera sesión de estudio.', en: 'Complete your first study session.' }
  },
  {
    id: 'streak_5',
    icon: '🔥',
    title: { es: 'Mente Veloz', en: 'Fast Mind' },
    description: { es: 'Alcanza una racha de 5 aciertos seguidos.', en: 'Reach a streak of 5 consecutive correct answers.' }
  },
  {
    id: 'master_10',
    icon: '👑',
    title: { es: 'Coleccionista de Cartas', en: 'Card Collector' },
    description: { es: 'Domina al menos 10 tarjetas en tu baraja.', en: 'Master at least 10 cards across decks.' }
  },
  {
    id: 'quiz_ace',
    icon: '🎯',
    title: { es: 'Ojo de Halcón', en: 'Hawk Eye' },
    description: { es: 'Termina un Quiz Arcade con más del 80% de aciertos.', en: 'Finish a Quiz Arcade session with 80%+ accuracy.' }
  },
  {
    id: 'spelling_pro',
    icon: '✍️',
    title: { es: 'Maestro de la Ortografía', en: 'Spelling Master' },
    description: { es: 'Acierta 3 tarjetas seguidas en el modo escritura sin pistas.', en: 'Get 3 correct in spelling mode without hints.' }
  },
  {
    id: 'ai_creator',
    icon: '✨',
    title: { es: 'Alquimista Digital', en: 'Digital Alchemist' },
    description: { es: 'Genera o importa un mazo personalizado con éxito.', en: 'Successfully generate or import a custom deck.' }
  }
];

export const I18N = {
  es: {
    appTitle: 'Flashcards Mágico',
    tagline: 'Estudio activo bilingüe, pronunciación por voz y generación con IA',
    backDatalaria: '← Datalaria',
    linkSpec: '📋 Ficha',
    linkPost: '📖 Historia',
    linkKits: '📦 Kits',
    btnInstallPwa: '📲 Instalar App',
    installApp: '📲 Instalar',
    installAppTitle: 'Instalar en pantalla de inicio',
    installSuccessToast: '¡Aplicación instalada con éxito!',
    installIosInstructions: '📲 En iPhone/iPad: pulsa el botón Compartir (↑) y selecciona "Añadir a pantalla de inicio".',
    installGenericInstructions: '📲 Para instalar: abre el menú de tu navegador y pulsa "Instalar aplicación".',
    updateAvailable: 'Nueva versión disponible de Flashcards AI',
    updateNowBtn: 'Actualizar ahora',
    checkingUpdate: 'Buscando actualizaciones...',
    upToDate: '✅ Ya tienes la última versión instalada (v2.1.0)',
    badgeCheckTitle: 'Buscar actualizaciones (v2.1.0)',
    tabStudy: '🎮 Estudiar',
    tabCreator: '✨ Creador Mágico',
    tabStats: '🏆 Logros',
    
    // Vista Selector
    selectDeckTitle: 'Elige tu Mazo de Estudio',
    selectDeckSub: 'Selecciona una baraja curada o crea tus propias tarjetas en segundos:',
    categoryKids: '🎒 Niños & Escolares',
    categoryAdults: '💼 Adultos & Profesionales',
    categoryCustom: '⭐ Tus Mazos Guardados',
    cardsCount: 'tarjetas',
    selectModeTitle: 'Modo de Estudio',
    btnStartStudy: '¡Aprender Ahora! 🚀',
    
    // Vista Estudio
    sessionProgress: 'Tarjeta {current} de {total}',
    masteryBadge: 'Dominio: {percent}%',
    speakNormal: '🔊 Pronunciar',
    speakSlow: '🐢 Modo Lento (0.75x)',
    tapToFlip: 'Toca o pulsa Espacio para voltear 🔄',
    btnRepeat: '🌱 Repetir (+0)',
    btnGood: '👍 Bien (+2)',
    btnMastered: '👑 ¡Dominada! (+3)',
    hintLabel: '💡 Pista:',
    typeAnswerPlaceholder: 'Escribe tu respuesta aquí...',
    btnCheck: 'Comprobar ➔',
    btnRevealLetter: '💡 Revelar Letra',
    feedbackCorrect: '¡Excelente! 🎉',
    feedbackIncorrect: '¡Casi! Repasémosla pronto 🧐',
    btnNext: 'Siguiente ➔',
    
    // Resumen Final
    summaryTitle: '¡Sesión Completada!',
    summaryScore: 'Puntuación: {score} puntos',
    summaryMastered: 'Tarjetas Dominadas: {mastered} de {total}',
    btnStudyAgain: 'Repasar de nuevo 🔁',
    btnStudyFailed: 'Repasar pendientes ({count}) 🎯',
    btnBackHome: 'Elegir otro mazo 🏠',
    
    // Creador
    creatorTitle: 'Creador de Mazos (IA, CSV y Manual)',
    creatorSub: 'Genera mazos enteros con Google Gemini (BYOK), importa desde CSV o añade términos a mano.',
    creatorModeAi: '✨ Modo Mágico (IA Gemini)',
    creatorModeManual: '✍️ Modo Manual / CSV',
    aiApiKeyLabel: 'Tu clave API de Google Gemini (Gratuita en AI Studio):',
    aiApiKeyPlaceholder: 'Pega tu API Key (AIzaSy...)',
    aiApiKeyHint: 'Tu clave se guarda exclusivamente en tu navegador (LocalStorage) y nunca se comparte.',
    aiTargetLang: 'Acción de Generación:',
    optTranslateEn: 'Traducir a Inglés (con fonética)',
    optTranslateEs: 'Traducir a Español',
    optTranslateFr: 'Traducir a Francés',
    optTranslateDe: 'Traducir a Alemán',
    optDefineEs: 'Generar Definición Concisa en Español',
    optDefineEn: 'Generar Definición Concisa en Inglés',
    deckNameLabel: 'Nombre del Mazo:',
    deckNamePlaceholder: 'Ej: Vocabulario Examen Tema 4',
    termsInputLabel: 'Lista de Términos (uno por línea o separados por comas):',
    termsInputPlaceholder: 'Articulación\nColumna vertebral\nCráneo\nCostillas...',
    btnGenerateAi: 'Generar Mazo con IA ⚡',
    btnImportCsv: 'Subir Archivo CSV / TXT 📂',
    btnDownloadTemplate: 'Descargar Plantilla CSV 📥',
    btnExportCurrentDeck: 'Exportar Mazo a CSV 💾',
    btnSaveDeck: 'Guardar Mazo en Biblioteca 💾',
    manualTermHeader: 'Término',
    manualDefHeader: 'Definición / Traducción',
    btnAddRow: '+ Añadir Fila',
    
    // Logros
    statsTitle: 'Tus Logros y Pasaporte de Estudio',
    totalMasteredLabel: 'Tarjetas Dominadas',
    totalDecksLabel: 'Mazos Creados/Estudiados',
    totalSessionsLabel: 'Sesiones Completadas',
    medalsUnlockedLabel: 'Medallas Desbloqueadas: {count} de 6'
  },
  en: {
    appTitle: 'Magic Flashcards',
    tagline: 'Bilingual active recall, speech audio, and AI card generation',
    backDatalaria: '← Datalaria',
    linkSpec: '📋 Spec',
    linkPost: '📖 Story',
    linkKits: '📦 Kits',
    btnInstallPwa: '📲 Install App',
    installApp: '📲 Install',
    installAppTitle: 'Install to home screen',
    installSuccessToast: 'App installed successfully!',
    installIosInstructions: '📲 On iPhone/iPad: tap Share (↑) and select "Add to Home Screen".',
    installGenericInstructions: '📲 To install: open browser menu and tap "Install app".',
    updateAvailable: 'New version of Flashcards AI available',
    updateNowBtn: 'Update now',
    checkingUpdate: 'Checking for updates...',
    upToDate: '✅ You have the latest version installed (v2.1.0)',
    badgeCheckTitle: 'Check for updates (v2.1.0)',
    tabStudy: '🎮 Study',
    tabCreator: '✨ Magic Creator',
    tabStats: '🏆 Medals',
    
    // Deck Selector
    selectDeckTitle: 'Choose Your Study Deck',
    selectDeckSub: 'Select a curated deck or create your own custom flashcards in seconds:',
    categoryKids: '🎒 Kids & Students',
    categoryAdults: '💼 Adults & Professionals',
    categoryCustom: '⭐ Your Saved Decks',
    cardsCount: 'cards',
    selectModeTitle: 'Study Mode',
    btnStartStudy: 'Start Learning Now! 🚀',
    
    // Study View
    sessionProgress: 'Card {current} of {total}',
    masteryBadge: 'Mastery: {percent}%',
    speakNormal: '🔊 Pronounce',
    speakSlow: '🐢 Slow Mode (0.75x)',
    tapToFlip: 'Tap or press Space to flip 🔄',
    btnRepeat: '🌱 Repeat (+0)',
    btnGood: '👍 Good (+2)',
    btnMastered: '👑 Mastered! (+3)',
    hintLabel: '💡 Hint:',
    typeAnswerPlaceholder: 'Type your answer here...',
    btnCheck: 'Check ➔',
    btnRevealLetter: '💡 Reveal Letter',
    feedbackCorrect: 'Great job! 🎉',
    feedbackIncorrect: 'Almost! Let\'s review it soon 🧐',
    btnNext: 'Next ➔',
    
    // Summary
    summaryTitle: 'Session Completed!',
    summaryScore: 'Score: {score} points',
    summaryMastered: 'Mastered Cards: {mastered} of {total}',
    btnStudyAgain: 'Study Again 🔁',
    btnStudyFailed: 'Review Pending ({count}) 🎯',
    btnBackHome: 'Choose Another Deck 🏠',
    
    // Creator
    creatorTitle: 'Deck Creator (AI, CSV & Manual)',
    creatorSub: 'Generate full decks with Google Gemini (BYOK), import standard CSVs, or add cards manually.',
    creatorModeAi: '✨ Magic Mode (Gemini AI)',
    creatorModeManual: '✍️ Manual / CSV Mode',
    aiApiKeyLabel: 'Your Google Gemini API Key (Free on AI Studio):',
    aiApiKeyPlaceholder: 'Paste your API Key (AIzaSy...)',
    aiApiKeyHint: 'Your key is kept strictly in your local browser (LocalStorage) and never shared.',
    aiTargetLang: 'Generation Action:',
    optTranslateEn: 'Translate to English (with phonetics)',
    optTranslateEs: 'Translate to Spanish',
    optTranslateFr: 'Translate to French',
    optTranslateDe: 'Translate to German',
    optDefineEs: 'Generate Concise Spanish Definition',
    optDefineEn: 'Generate Concise English Definition',
    deckNameLabel: 'Deck Name:',
    deckNamePlaceholder: 'E.g., Chapter 4 Vocabulary Review',
    termsInputLabel: 'Terms List (one per line or comma-separated):',
    termsInputPlaceholder: 'Joints\nSpinal column\nSkull\nRibs...',
    btnGenerateAi: 'Generate Deck with AI ⚡',
    btnImportCsv: 'Upload CSV / TXT File 📂',
    btnDownloadTemplate: 'Download CSV Template 📥',
    btnExportCurrentDeck: 'Export Deck to CSV 💾',
    btnSaveDeck: 'Save Deck to Library 💾',
    manualTermHeader: 'Term',
    manualDefHeader: 'Definition / Translation',
    btnAddRow: '+ Add Row',
    
    // Medals
    statsTitle: 'Your Achievements & Study Passport',
    totalMasteredLabel: 'Mastered Cards',
    totalDecksLabel: 'Decks Created/Studied',
    totalSessionsLabel: 'Sessions Completed',
    medalsUnlockedLabel: 'Medals Unlocked: {count} of 6'
  }
};
