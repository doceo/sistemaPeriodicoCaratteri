from csv import reader


def extract_csv(filename):
    with open(filename, 'r') as read_obj:
        return list(reader(read_obj))


#calcolo il punteggio per ogni elemento caratteristica per caratteristica
def get_points(elemento, risposte):
    assert len(elemento) == len(risposte)
    
    punteggio = 0
    for i in range(len(elemento)):
        if elemento[i] == 5 and risposte[i] == 5:
            punteggio += 1000
        elif elemento[i] == 1 and risposte[i] == 1:
            punteggio += 250
        elif elemento[i] == risposte[i]:
            punteggio += 50
        else:
            punteggio += 5 * (4 - abs(elemento[i] - risposte[i]))
    
    return punteggio
    
def percentuale(totale, n):
    return (n * 100) / totale

#ottengo in input dall'utente le risposte e le salvo come lista
def get_answer(domande):
    risposte = []
    for i in domande:
        while True:
            try:
                answer = int(input(f"\n{i}? (1 - 5))  -->  "))
                if answer in [1, 2, 3, 4, 5]:
                    risposte.append(answer)
                    break
                else:
                    raise Exception
            except:
                print("\n Inserisci un numero compreso tra 1 e 5")
    
    return risposte

if __name__ == "__main__":
        
    table = extract_csv("sistema_periodico.csv")
    #le domande sono la prima riga del file csv
    domande = table[0][1:]
    
    #creo un dizionario con chiave il nome dell'elemento e come valore la lista dei punteggi
    elementi = {i[0]: [int(i) for i in i[1:]] for i in table[1:]}
    risposte = [2, 3, 2, 2, 4, 5, 3, 2, 5, 3, 5, 2]#get_answer(domande)
    
    #creo un dizionario con chiave il nome dell'elemento e come valore il punteggio dell'elemento
    punteggi = {elemento: get_points(elementi[elemento], risposte) for elemento in elementi.keys()}
    totale_punti = sum(list(punteggi.values()))
    
    #creo un dizionario con chiave il nome dell'elemento e come valore la percentuale dei punti fatti dall'elemento sul totale
    percentuali = {elemento: percentuale(totale_punti, punteggi[elemento]) for elemento in elementi.keys()}

    #crea una lista ordinata degli elementi in base alla percentuale
    ordine_elementi = [i[0] for i in reversed(sorted(punteggi.items(), key=lambda item: item[1]))]
    
    for elemento in ordine_elementi:
        print(f"{elemento} - {punteggi[elemento]} - {percentuali[elemento]}")
