def prompt_extract_and_describe_frames(frame_number):
    return """<prompt>
  <context>
    Un atleta ha inviato un video della sua performance sportiva. Il frame {frameNumber} è una parte specifica di questo video più ampio. L'obiettivo è analizzare ESCLUSIVAMENTE gli atleti in azione, se presenti.
  </context>
  
  <task>
    Analizzare il frame {frameNumber} del video SOLO per identificare e descrivere atleti in azione. Non fornire ALCUNA informazione sull'ambiente, attrezzature sportive o qualsiasi altro elemento non direttamente correlato agli atleti stessi. Rispondere SEMPRE ED ESCLUSIVAMENTE in italiano.
  </task>
  
  <instructions>
    <step>Verificare la presenza di atleti chiaramente visibili e in azione nell'immagine.</step>
    <step>Se sono presenti atleti in azione:
      <substep>Descrivere SOLO la posizione, postura e movimenti degli atleti.</substep>
      <substep>Analizzare ESCLUSIVAMENTE l'azione o il movimento degli atleti in quel preciso istante.</substep>
      <substep>Menzionare UNICAMENTE espressioni facciali o linguaggio del corpo degli atleti, se rilevanti.</substep>
    </step>
    <step>Se non sono presenti atleti in azione, fornire SOLO la risposta standard specificata in italiano, senza aggiungere alcun dettaglio sull'immagine.</step>
  </instructions>
  
  <output_requirements>
    <format>Testo in prosa, paragrafo unico</format>
    <length>Massimo 5-6 frasi se sono presenti atleti; esattamente 1 frase se non sono presenti</length>
    <style>Descrittivo e focalizzato ESCLUSIVAMENTE sugli atleti se presenti; altrimenti, solo la frase standard di risposta</style>
    <language>ESCLUSIVAMENTE italiano. Non usare MAI altre lingue.</language>
  </output_requirements>
  
  <error_handling>
    <case>
      <condition>Assenza di atleti in azione nell'immagine</condition>
      <response>Rispondere ESCLUSIVAMENTE in italiano con: "L'immagine non contiene atleti visibili in azione. Non è possibile fornire un'analisi della performance sportiva."</response>
    </case>
  </error_handling>
  
  <strict_requirements>
    NON descrivere MAI l'ambiente, le attrezzature sportive, o qualsiasi altro elemento che non sia un atleta in azione.
    NON fornire MAI informazioni su piste, campi, strutture o qualsiasi altro aspetto dell'immagine che non sia direttamente un atleta.
    Se non ci sono atleti in azione, usa SOLO la frase standard fornita in italiano, senza aggiungere alcun dettaglio.
    Rispondere SEMPRE ED ESCLUSIVAMENTE in italiano. Non utilizzare MAI altre lingue nella risposta.
  </strict_requirements>
  
  <language_enforcement>
    Tutte le risposte devono essere formulate ESCLUSIVAMENTE in lingua italiana.
    È VIETATO l'uso di qualsiasi altra lingua, incluso l'inglese, in qualsiasi parte della risposta.
    In caso di dubbi su come esprimere un concetto, utilizzare SEMPRE una formulazione in italiano, anche se meno precisa.
  </language_enforcement>
</prompt>
  """