from csv import reader

class Tree:

    def __init__(self, index: str, question: str, ans1: str, ans2: str):
        self.main_node = Node(index, question, ans1, ans2)

    def add_node(self, index: str, question: str, ans1: str, ans2: str):
        self.main_node.add(Node(index, question, ans1, ans2))

    def draw(self):
        self.main_node.draw()


# classe nodo
class Node:

    def __init__(self, index: str, question: str, answer1: str, answer2: str):
        
        # left e right sono i due nodi che si trovano subordinati al nodo originale
        self.left = None
        self.right = None
        
        self.index = index
        self.val = int(index, 2)
        self.question = question
        self.answers = {"answer-1" : answer1, "answer-2" : answer2}

    # Si svolge ricrsivamente per disegnare tutti i nodi
    def draw(self, level=0, yes_or_no=""):
        
        # disegma tutti i nodi a destra del nodo originale ricorsivamente
        if self.left != None:
            self.left.draw(level + 1, "Si")
            print("")
        
        # disegna il nodo originale
        print(' ' * 8 * level + yes_or_no + '-> ' + str(self.val))
        
        # disegna tutti i nodi a sinistra del nodo originale ricorsivamente
        if self.left != None:
            print("")
            self.right.draw(level + 1, "No")

    def add(self, new_node):
        
        assert type(new_node) == Node

        # Serve a capire se il nodo che sta venendo aggiunto è figlio diretto o no del nodo attuale
        if (len(new_node.index) - len(self.index)) == 1:

            # imposta il nuovo nodo come figlio diretto
            if new_node.index[-1] == '0':
                self.left = new_node
            elif new_node.index[-1] == '1':
                self.right = new_node
        else:

            # serve a capire se il nuovo nodo è figlio del nodo a destra o di quello a sinistra
            if new_node.index[len(self.index)] == '0':
                self.left.add(new_node)
            elif new_node.index[len(self.index)] == '1':
                self.right.add(new_node)


def extract_csv(filename):
    with open(filename, 'r') as read_obj:
        return list(reader(read_obj))


if __name__ == "__main__":
    
    table = extract_csv("table.csv")
    
    # crea il nodo base
    albero = Tree(table[1][0], table[1][1], table[1][2], table[1][3])

    # itera attraverso tutti gli elementi della tabella e li aggiunge come figli del nodo base
    for index, quest, ans1, ans2 in table[2:]:
        albero.add_node(index, quest, ans1, ans2)
    
    #albero.draw()
    
    current_node = albero.main_node
    print("Benvenuto nel test!\n")
    
    while True:
        if current_node.left is None or current_node.right is None:
            print(f"Congratulations! You finished the test! Your element is {current_node.index}")
            break
        answer = input(current_node.question.strip("' ") + " (Y/N)  -->  ")
        if answer.lower() in ["yes", "y"]:
            current_node = current_node.left
        elif answer.lower() in ["no", "n"]:
            current_node = current_node.right
        else:
            print(f"Sorry, {answer} is not a valid answer. Try with 'yes' or 'no'")
