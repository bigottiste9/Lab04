#importa la classe principale dal file lingotto_fiere.py
from lingotto_fiere import LingottoFiere

#funzione che visualizza il menu
def menu():

    #stampa il menù del programma
    print(f'\n--- MENU LINGOTTO FIERE ---')
    print("1. Modifica nome del centro fieristico")
    print("2. Carica dati da file")
    print("3. Assegna stand a espositore")
    print("4. Visualizza elenco espositori")
    print("5. Visualizza stand ordinati per prezzo")
    print("6. Esci")

    #chiede all'utente di scegliere un'opzione
    return input("Scegli un'opzione >> ")

#funzione principale
def main():
    #crea l'oggetto che rappresenta il centro fieristico
    lingotto = LingottoFiere("Lingotto Fiere")

    #ripete il menu finchè l'utente non sceglie di uscire
    while True:
        #mostra il menù ed acquisisce la scelta
        scelta = menu()

        #opzione 1 : midifica del nome
        if scelta == "1":
            #chiede il nuovo nome del centro fioristico
            nuovo_nome = input("Inserisci il nuovo nome del centro fieristico: ")

            #modifico il nome usando il metodo setter
            lingotto.set_nome(nuovo_nome)

            #conferma l'operazione
            print("Nome del centro fieristico aggiornato.")

            #mostra il nuovo nome
            print("Nuovo nome:", lingotto.get_nome())


        #opzione 2 : caricamento del file
        elif scelta == "2":

            #nome del file CSV contenente gli stand e gli espositori
            file_path = "dati_lingotto.csv"
            try:

                #carica i dati del file
                lingotto.carica_file_dati(file_path)

                #conferma il caricamento
                print("Dati caricati correttamente.")

                #mostra quanti elementi sono stati caricati
                print("Numero stand:", len(lingotto.stand))
                print("Numero espositori:", len(lingotto.espositori))

            except FileNotFoundError:

                #gestisce il caso in cui il file non esista
                print("File non trovato.")

            except (ValueError, IndexError) as e:
                #gestisce eventuali dati non validi o righe incomplete
                print("Errore nei dati del file: ", e)


#opzione 3: assegnazione di uno stand
        elif scelta == "3":

            #chiede il codice dello stand
            codice_stand = input("Codice stand: ")

            #chiede il codice dell'espositore
            codice_espositore = input("Codice espositore: ")
            try:

                #tenta di assegnare lo stand all'espositore
                lingotto.assegna_stand_a_espositore(codice_stand, codice_espositore)

                #se non si verificano errori, l'assegnazione è riuscita
                print("Stand assegnato con successo.")
            except Exception as e:

                #mostra il motivo del perchè l'assegnazione non è riuscita
                print(f"Errore: {e}")


#opzione 4: elenco espositori
        elif scelta == "4":

            #stampa il titolo della sezione
            print("\n--- Elenco espositori ---")

            #mostra gli espositori e gli eventuali stand assegnati
            lingotto.elenca_espositori()


#opzione 5: stan ordinati per prezzo
        elif scelta == "5":

            #ottiene la lista degi stand ordinati per prezzo
            stand_ordinati = lingotto.stand_ordinati_per_prezzo()

            #stampa il titolo della sezione
            print("\n--- Stand ordinati per prezzo ---")

            #controlla se sono presenti stand
            if len(stand_ordinati) == 0:
                print("Nessuno stand presente.")
            else:

                #stampa gli stand dal piu economico al piu costoso
                for stand in stand_ordinati:
                    print(stand)


#opzione 6: uscita
        elif scelta == "6":

            #comunica che il proramma sta terminando
            print("Uscita dal programma.")

           #interrompe il ciclo while
            break


#scelta non valida
        else:

            #gestisce una scelta diversa da quelle previste
            print("Scelta non valida.")


#avvio del programma
if __name__ == "__main__":
    main()
