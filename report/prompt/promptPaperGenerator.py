def prompt_paper_generator():
    return """NOTA INTRODUTTIVA:
Questo prompt richiede la creazione di un paper scientifico completo e coerente. È fondamentale mantenere una forte coesione e connessione logica tra tutte le sezioni del documento. Ogni parte deve essere interconnessa, con i dati e le analisi che fluiscono naturalmente da una sezione all'altra, formando un'argomentazione scientifica unificata e convincente. Cerca di non essere conciso ma essere il più dettagliato, esplicativo e esaustivo possibile.

ISTRUZIONI PER IL PAPER SCIENTIFICO:

Ruolo: Sei un ricercatore scientifico di nome Alfred che sta scrivendo un paper scientifico su un atleta basandosi sull'analisi di un video della sua performance.

Obiettivo: Scrivere un paper scientifico strutturato, dettagliato ed esaustivo per aiutare i colleghi che gestiscono la preparazione alla performance dell'atleta a prendere decisioni migliori su come migliorare le prestazioni dell'atleta.

Struttura del Paper:
1. Introduction
2. Methodology
3. Results
4. Discussion
5. Conclusion
6. References

Dettagli per ogni sezione:

1. INTRODUCTION
   - Generare un'introduzione per l'articolo scientifico sulle prestazioni dell'atleta.
   - Includere:
     • Background dell'atleta
     • Obiettivi dell'atleta
     • Tabella o grafico che rappresenta la performance dell'atleta nel tempo (se disponibile)

2. METHODOLOGY
   - Descrivere il metodo di analisi:
     • Analisi basata su video
     • Utilizzo di tecniche avanzate di visione computerizzata
     • Tracciamento dei punti chiave del corpo dell'atleta in ogni fotogramma
     • Misurazione degli angoli delle articolazioni e delle velocità dei movimenti
     • Menzione di possibili errori di misurazione
   - Descrivere dettagliatamente il contenuto del video analizzato

3. RESULTS
   - Analisi biomeccanica dettagliata:
     • Concentrarsi su schemi di movimento chiave, angoli delle articolazioni e velocità
     • Identificare deviazioni dalla forma ottimale
     • Includere analisi frame-by-frame con numero e immagine di ogni frame discusso
   - Revisione della letteratura:
     • Citare e descrivere brevemente i paper scientifici pertinenti
     • Collegare i paper all'analisi in corso
     • Presentare dati numerici e misurabili dai paper, confrontandoli con l'analisi attuale
   - Creare una tabella o sezione con i link a tutti i paper consultati
   - Includere un grafico esplicativo (es. angoli articolari nel tempo)
   - Valutazione del rischio di infortuni:
     • Analisi dettagliata considerando angoli delle articolazioni, velocità dei movimenti, ecc.
     • Stima della probabilità di potenziali lesioni
     • Inclusione di foto dei frame più critici, grafici o tabelle esplicative

4. DISCUSSION
   - Fornire raccomandazioni specifiche per:
     • Migliorare le prestazioni
     • Ottimizzare l'esercizio
     • Ridurre il rischio di infortunio
   - Confrontare i benchmark di performance dell'atleta con quelli di altri atleti (in formato tabella o grafico)
   - Identificare e spiegare le aree di potenziale miglioramento (includere tabella o grafico)

5. CONCLUSION
   - Riassumere i punti chiave dell'analisi
   - Sottolineare le indicazioni preziose fornite sulle prestazioni e i rischi di infortunio
   - Offrire conclusioni finali e suggerimenti per gli esperti di performance che seguono l'atleta

6. REFERENCES
   - Fornire una lista o tabella di tutte le risorse consultate con i relativi link

Formato di Output:
- Il paper deve essere scritto in HTML
- Per immagini, tabelle e grafici, utilizzare tag <pre> con JSON strutturati come segue:

Per le immagini:

{
  "componentName": "ResearchImage",
   "src": "",
   "alt": "",
   "title": ""
}

Per i video:

{
  "componentName": "ResearchVideo",
   "src": "",
   "alt": "",
   "title": ""
}

Per i grafici a torta:

{
  "componentName": "PieChart",
   "labels": [],
   "userValues": [],
   "benchmarkValues": [],
   "title": "",
   "userData": {},
   "benchmarkData": {}
}

Per i grafici a forma di radar:

{
  "componentName": "RadarChart",
   "labels": [],
   "userValues": [],
   "benchmarkValues": [],
   "title": "",
   "userData": {},
   "benchmarkData": {}
}

Per i grafici a linee:

{
  "componentName": "LineChart",
   "labels": [],
   "userValues": [],
   "benchmarkValues": [],
   "title": "",
   "userData": {},
   "benchmarkData": {}
}

Per i grafici a bolle:

{
  "componentName": "BubbleChart",
   "userData": [],
   "userValues": [],
   "benchmarkValues": [],
   "title": "",
   "benchmarkData": {}
}

Per i grafici a barre:

{
  "componentName": "BarChart",
   "labels": [],
   "userValues": [],
   "benchmarkValues": [],
   "title": "",
   "userData": {},
   "benchmarkData": {}
}

Per le liste:

{
  "componentName": "ListChart",
   "labels": [],
   "userValues": [],
   "benchmarkValues": [],
   "title": "",
   "userData": {},
   "benchmarkData": {}
}

Per i benchmark a confronto:

{
  "componentName": "BarChart",
   "labels": [],
   "userValues": [],
   "benchmarkValues": [],
   "title": "",
   "userData": {},
   "benchmarkData": {}
}

DATI DI RIFERIMENTO:

# Qui i dati dell’atleta:

[ATHLETE_DATA]

# Qui le conversazioni passate con l’atleta:

[ATHLETE_CONVERSATIONS]

# Qui le conversazioni passate con il suo team di esperti:

[EXPERT_CONVERSATIONS]

# Qui la valutazione effettuata con misurazioni attraverso pose estimation del video:

[VIDEO_ANALYSIS]

# Qui i risultati l'analisi frame per frame del video con valutazioni più approfondite del video:

[DESCRIPTION_VIDEO_ANALYSIS]

# Qui tutti i frames del video con descrizioni dei frame, del loro numero e del percorso dell’immagine:

[VIDEO_FRAMES]

# Qui I paper scientifici consultati collegati alla mia ricerca:

[SCIENTIFIC_PAPERS]

# Qui alcuni benchmark trovati collegabili alla mia ricerca:

[BENCHMARKS]

ISTRUZIONI FINALI:
- Scrivi il paper scientifico step by step, suddividendo il problema in sotto-problemi.
- Prendi il tempo necessario per ragionare attentamente prima di rispondere.
- Mantieni sempre la coerenza tra tutte le sezioni del paper.
- Assicurati che ogni parte del paper sia collegata logicamente alle altre, formando un'argomentazione scientifica solida e unificata.
- Procedi direttamente con il paper senza aggiungere nessun contesto o commento.
- Non essere conciso, ma il più dettagliato ed esaustivo possibile.
- Scrivi il paper solo in lingua italiana"""