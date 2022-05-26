from csv import reader

def get_questions():
    return [
        'Ti adatti facilmente alle situazioni e alle aspettative delle persone che ti stanno intorno?',
        'Sei in grado di affrontare situazioni inaspettate che richiedono decisioni rapide e reazioni decise?',
        'Ti capita di nascondere le tue vere intenzioni per manipolare le situazioni in cui ti trovi?',
        'Ti basta poco tempo per fare amicizia o collaborare con gli altri?',
        'Ti capita spesso che le persone ti dicano: “Sei diverso da come ti immaginavo”?',
        'Tendi ad arrabbiarti facilmente in situazioni di stress?',
        'Quando cerchi di aiutare o coinvolgere un amico in qualche attività, ti capita di esagerare e diventare un po’ invadente?',
        'Ti capita di cercare di apparire diverso da quello che sei per sembrare “migliore” o per aderire alle aspettative degli altri?',
        'Quando sei in compagnia, ti capita di sentirti per certi aspetti diverso o fuori luogo?',
        'Ti è facile mantenere la calma e la concentrazione anche sotto pressione?',
        'Quando devi raggiungere un obiettivo, lo fai ad ogni costo, anche se sei consapevole dei tuoi limiti?',
        'Quando subisci un profondo dolore, delusione o lutto, continui a subirne  gli effetti negativi sulle tue capacità di stare nel mondo anche nei mesi successivi?'
        ]

def get_symbols():
    return ["H", "S", "Zn", "N", "Fe", "C", "P", "Ti", "Sn", "Ag", "Pb", "Cd", "U", "As", "K", "Cr", "Ar", "Au", "Ce", "Ni", "Hg", "V"]

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

    
def percentage(totale, n):
    return (n * 100) / totale

def split_line(line: str, max_lenght: int):
    lista = []
    
    testo = ""
    for i in line.split(" "):
        if len(i + " " + testo) <= max_lenght:
            testo = testo + " " + i
        else:
            lista.append(testo.strip())
            testo = ""
            testo = testo + " " + i
    if testo != "":
        lista.append(testo.strip())

    return "\n".join(lista)

def center_text(line: str, line_lenght: int):
    space_number = (line_lenght - len(line))/2
    spaces = " " * int(space_number*1.5)
    return spaces + line

def get_credits_desc():
    return '"Sistema Periodico" è un libro scritto da Primo Levi, l\'opera raccoglie 21 racconti, ciascuno intitolato con il nome di un elemento della tavola periodica, ad esso in qualche modo collegato. I temi sono numerosi, incentrati sulla vita professionale di chimico e contenuti in una cornice autobiografica. La classe 3E dell\'istituto G.B Vico di Napoli durante l\'anno scolastico 2021-2022 ha letto e analizzato questo libro nelle ore di Italiano con la professoressa Soravia. La classe ha inoltre approfondito i vari elementi durante le ore di scienze con il professor Esposito. Poi alcuni studenti hanno collegato ad ogni elemento un personaggio apparso nel capitolo del libro corrispondente in modo da associare un carattere ad ogni elemento. Infine è stata sviluppata un applicazione con Python e Tkinter.\n Alunni che hanno partecipato al progetto: Alessandro Todino, Luca Biasi, Francesco Bocchetti, Enrico Avallone, Giuseppe Fulgione, Giovanni Catalano, Raffaele Mariano, Roberto Ferrigno e Luca Patruno.'