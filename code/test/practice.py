string = "length of string: 20"

# print the length of string
print("length of the string is", len(string) )

# print the first occurance of t
print("the first occurence of t is", string.index("t") )

# print the no. of t's
print("t occurs {} times".format(string.count("t")))

# slicing the string into bits
print("the first five characters are '{}'".format(string[:5]))

print("the next five characters are '{}'".format(string[5:10]))

print("the chacters at odd index are '{}'".format(string[1::2]))

print("the last five characters are '{}'".format(string[-5:]))

print("the uppercase string is '{}'".format(string.upper()))

print("the lowercase string is '{}'".format(string.lower()))

if string.startswith("length"):
    print("this string starts with 'length'")

if string.endswith("20"):
    print("this string ends with '20'")

print("split the words of the string: {}".format(string.split()))

