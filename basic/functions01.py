def my_function():
    print("my_function")

my_function()

def my_function02(argument01):
    print("my_function", argument01)
    
my_function02("This is 1st argument ")
    
def my_function03(arg01, arg02):
    print("In my_function03 \n arg01:\n", arg01 , "\n arg02:\n", arg02)
    
my_function03("1st", "2nd")

def my_function04(*args):
    print("Ths arg at index 0 is:", args[0])

my_function04("some one")    