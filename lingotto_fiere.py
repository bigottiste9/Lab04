import csv

#classe espositore
class Espositore:
    def __init__(self, codice, nome, cognome):
        #inizializza gli attributi dell'espositore
        self.codice = codice
        self.nome = nome
        self.cognome = cognome

        #all'inizio l'espositore non ha uno stand assegnato
        self.stand= None

    def __eq__(self, other):
        #due espositori sono uguali se hanno lo stesso codice
        if isinstance(other, Espositore):
            return self.codice == other.codice
        return False

    def __str__(self):
        #restituisce una descrizione leggibie dell'espositore
        testo = self.codice + " _ " + self.nome + " " + self.cognome

        #se l'espositore ha uno stand, aggiungiamo il codice
        if self.stand is not None:
            testo = testo + " - Stand assegnato: " + self.stand.codice
        else:
            testo = testo + " - Nessuno stand assegnato"
        return testo

#classe base stand
class Stand:
    def __init__(self, codice, superficie, padiglione, prezzo_base):
        #inizializza le informazioni comuni a tutti gli stand
        self.codice = codice
        self.superficie = superficie
        self.padiglione = padiglione
        self.prezzo_base = prezzo_base

        #all'inizio lo stand è disponibile
        self.disponibile = True

        #nessun espositore è ancora associato allo stand
        self.espositore = None

    def get_prezzo(self):
        #per uno stand standard il prezzo finale è quello base
        return self.prezzo_base

    def __lt__(self, other):
        #permette di confrontare due stand in base al prezzo
        return self.get_prezzo() < other.get_prezzo()

    def __eq__(self, other):
        #due stand sono uguali se hanno lo stesso codice
        if isinstance(other, Stand):
            return self.codice == other.codice
        return False

    def __str__(self):
        #restituisce una descrizione dello stand
        testo = (
            self.codice
            + ": Standard | "
            + str(self.superficie)
            + " mq - Padiglione "
            + str(self.padiglione)
            +" - Prezzo "
            +format(self.get_prezzo(), ".2f")
            + "£" #non ho il simbolo dell'euro sulla tastiera
        )

        #indica se lo stand è disponibile oppure assegnato
        if self.disponibile:
            testo = testo + " - Disponibile"
        else:
            testo = testo + " - Non disponibile"
        return testo

#classe stand con prese elettriche aggiuntive
class StandPreseElettriche(Stand):
    def __init__(self, codice, superficie, padiglione, prezzo_base, numero_prese):
         #richiamo il costruttore della classe Stand
        super().__init__(codice, superficie, padiglione, prezzo_base)

        #memorizza il numero di prese elettriche aggiuntive
        self.numero_prese = numero_prese

    def get_prezzo(self):
        #ogni presa aggiuntiva aumenta il prezzo del 7%
        prezzo_finale = self.prezzo_base * (
            1 + 0.07 * self.numero_prese
        )

        return prezzo_finale

    def __str__(self):
        #descrive lo stand con prese elettriche
        testo = (
            self.codice
            + ": Prese Extra | "
            + str(self.superficie)
            + " mq - Padiglione "
            + str(self.padiglione)
            +" - Prezzo "
            +format(self.get_prezzo(), ".2f")
            +"£ - Prese aggiuntive: "
            +str(self.numero_prese)
        )

        #indica la disponibilità dello stand
        if self.disponibile:
            testo = testo + " - Disponibile"
        else:
            testo = testo + " - Non disponibile"
        return testo

#classe stand premium

class StandPremium(Stand):
    def __init__(self, codice, superficie, padiglione, prezzo_base, posizione):
        #richiama il costruttore della classe stand
        super().__init__(codice, superficie, padiglione, prezzo_base)

        #memorizza la posizione dello Stand premium
        self.posizione = posizione

    def get_prezzo(self):
        #gli stand premium hanno un sovraprezzo fisso del 30%
        prezzo_finale = self.prezzo_base * 1.30
        return prezzo_finale

    def __str__(self):
        #descrive lo stand premium
        testo = (
            +self.codice
            + ": Premium | "
            + str(self.superficie)
            + " mq - Padiglione "
            + str(self.padiglione)
            +" - Prezzo "
            +format(self.get_prezzo(), ".2f")
            + "£ - Posizione: "
            +self.posizione
        )

        #indica la disponibilità dello stand
        if self.disponibile:
            testo = testo + " - Disponibile"
        else:
            testo = testo + " - Non disponibile"
        return testo

#classe principale lingotto fiere

class LingottoFiere:
    def __init__(self, nome):
        #memorizza il nome del centro fieristico
        self.nome = nome

        #lista degli stand presenti nel centro fieristico
        self.stand = []

        #lista degli espositori registrati
        self.espositori = []

    #metodi getter e setter
    def get_nome(self):
        #restituisce il nome del centro fieristico
        return self.nome

    def set_nome(self, nuovo_nome):
        # modifica il nome del centro fieristico
        self.nome = nuovo_nome

    #caricamento dei dati dal file csv
    def carica_file_dati(self, file_path):
        #apre il file csv in modalità lettura
        with open(file_path, "r", encoding= "utf-8") as file:

            #legge le righe del file separando i campi con la virgola
            lettore= csv.reader(file, skipinitialspace=True)

            #svuota le liste prima di caricare i dati
            self.stand = []
            self.espositori = []

            #esamina una riga alla volta
            for riga in lettore:

                #ignora le righe vuote
                if len(riga) == 0:
                    continue

                #elimina eventuali spazi prima e dopo i campi
                for i in range (len(riga)):
                    riga[i] = riga[i].strip()

                #se il codice inizia con ST, la riga riguarda uno stand
                if riga [0].startswith("ST"):

                    #legge le informazioni comuni dello stand
                    codice = riga [0]
                    superficie = int(riga [1])
                    padiglione = int(riga [2])
                    prezzo_base = float(riga [3])

                    #se esiste un quinto campo, identifica la tipologia
                    if len(riga) >= 5:
                        caratteristica = riga[4]

                        #se il campo è numerico, si tratta di prese extra
                        if caratteristica.isdigit():

                            numero_prese = int(caratteristica)

                            #crea un nuovo stand con prese elettriche
                            nuovo_stand = StandPreseElettriche(
                                codice,
                                superficie,
                                padiglione,
                                prezzo_base,
                                numero_prese
                            )
                        else:
                            #se il campo è testuale, si tratta di uno stand Premium
                            posizione = caratteristica

                            #crea uno stand premium
                            nuovo_stand = StandPremium(
                                codice,
                                superficie,
                                padiglione,
                                prezzo_base,
                                posizione
                            )
                    else:
                        #se non esiste il quinto campo, lo stand è Standard
                        nuovo_stand= Stand(
                            codice,
                            superficie,
                            padiglione,
                            prezzo_base
                        )

                    #aggiunge lo stand alla lista degli stand
                    self.stand.append(nuovo_stand)

                #se il codice inizia con ES, la riga riguarda un'espositore
                elif riga [0].startswith("ES"):

                    #legge il codice, il nome, il cognome
                    codice = riga [0]
                    nome = riga [1]
                    cognome = riga [2]

                    #crea il nuovo espositore
                    nuovo_espositore = Espositore(
                        codice,
                        nome,
                        cognome
                    )
                    #aggiunge l'espositore alla lista
                    self.espositori.append(nuovo_espositore)

#assegnazione di uno stand a un espositore
    def assegna_stand_a_espositore(self, codice_stand, codice_espositore):
        #cerca lo stand utilizzando il suo codice
        stand_trovato = None
        for stand in self.stand:
            if stand.codice == codice_stand:
                stand_trovato = stand
                break

        #se lo stand non esiste, genera un'eccezione
        if stand_trovato is None:
            raise ValueError("Lo stand non esiste.")

        #cerca l'espositore utilizzando il suo codice
        espositore_trovato = None
        for espositore in self.espositori:
            if espositore.codice == codice_espositore:
                espositore_trovato = espositore
                break

        #se l'espositore non esiste, genera un'eccezione
        if espositore_trovato is None:
            raise ValueError("Lo stand non esiste.")

        #verifica che lo stand sia ancora disponibile
        if not stand_trovato.disponibile:
            raise ValueError("Lo stand non è disponibile.")

        #verifica che l'espositore non abbia già uno stand
        if espositore_trovato.stand is not None:
            raise ValueError("L'espositore ha già uno stand assegnato.")

        #registra l'associazione tra stand ed espositore
        stand_trovato.espositore = espositore_trovato
        espositore_trovato.stand = stand_trovato

        #o stand non è piu disponibile
        stand_trovato.disponibile = False


#elenco degli espositori
    def elenca_espositori(self):
        #controlla se esistono espositori registrati
        if len(self.espositori) == 0:
            print("Nessun espositore presente")
            return

        #stampa ogni espositore
        for espositore in self.espositori:
            print(espositore)


#stand ordinati per prezzo
    def stand_ordinati_per_prezzo(self):
        #ordina gli stand dal più economico al più costoso
        stand_ordinati = sorted(self.stand)

        #restituisce la lista ordinata
        return stand_ordinati
