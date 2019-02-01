class parent():
    global parent1,parent2
    parent1 = 'father'
    #parent2 = 'mother'

    def print_parent(self):
        global parent2
        parent2 = 'mother'
        print("your parents are {} and {}".format(parent1,parent2))

class mother(parent):
    def print_mother(self):
        print("your mother's name is {}".format(parent2))

ankit = parent()
ankit_mother = mother()
ankit.print_parent()
ankit_mother.print_mother()
