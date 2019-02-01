class name():
    global namestring, qual
    namestring = []
    qual = []
    def find_name(self):
        namestring = ['ankit', 'avinash', 'harsh']
        print(namestring)

    def quality(self):
        qual = ['good', 'best','better']
        print(qual)
class compare(name):
    #global namestring, qual
    print("working")
    def print_name(self):
        print("working")
        for i in range(len(namestring)):
                print('{} is {}'.format(namestring[i], qual[i]))

objname = name()
objcompare = compare()
objname.find_name()
objname.quality()
objcompare.print_name()
