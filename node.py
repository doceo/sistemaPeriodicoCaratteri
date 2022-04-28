from csv import reader

# classe nodo
class Node:
    
    def __init__(self, index, question, answer1, answer2):
        
        # left e right sono i due nodi che si trovano subordinati al nodo originale
        self.left = None
        self.right = None
        
        self.val = index
        self.question = question
        self.answers = {"answer-1" : answer1, "answer-2" : answer2}
    
    # Si svolge ricrsivamente per disegnare tutti i nodi
    def draw(self, level=0, yes_or_no=""):
        
        # disegma tutti i nodi a destra del nodo originale ricorsivamente
        if self.left != None:
            self.left.draw(level + 1, "Si")
            print("")
        
        # disegna il nodo originale
        print(' ' * 8 * level + yes_or_no + '-> ' + self.val)
        
        # disegna tutti i nodi a sinistra del nodo originale ricorsivamente
        if self.left != None:
            print("")
            self.right.draw(level + 1, "No")

def csv_to_node(filename):
    
    nodes = {}
    
    # estrae il file csv in una lista di liste
    with open(filename, 'r') as read_obj:
        table = list(reader(read_obj))

    # crea un nodo corrispondente ad ogni riga del file csv e lo aggiunge al dizionario
    for index, quest, ans1, ans2 in table[1:]:
        nodes[index] = Node(index, quest, ans1, ans2)
    print(nodes)

    # ripercorre la lista di liste in ordine opposto
    for index, quest, ans1, ans2 in reversed(table[1:]):
        
        # non esegue il codice se l'indice è 1 perchè esso è il nodo genitore di tutti gli altri
        if index != "1":
            # trova il nodo genitore del nodo a cui il ciclo attualmente si trova
            parent = ".".join(index.split(".")[:-1])
            
            # aggiunge il nodo figlio come attributo del nodo genitore posizionandolo a sinistra o destra in base al suo indice
            if index[-1] == "1":
                nodes[parent].left = nodes[index]
            else:
                nodes[parent].right = nodes[index]
    
    # ritorna in output solo il nodo con indice 1 in quanto è il nodo genitore degli altri 
    return nodes["1"]

if __name__ == "__main__":
    node = csv_to_node("table.csv")
    node.draw()

