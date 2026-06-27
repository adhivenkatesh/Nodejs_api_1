
# print("Hello Python Ji")
# variables ="first python"
# https://www.geeksforgeeks.org/python/convert-tuple-to-list-in-python/

# List is a collection which is ordered and changeable. Allows duplicate members.
# Tuple is a collection which is ordered and unchangeable. Allows duplicate members.
# Set is a collection which is unordered, unchangeable*, and unindexed. No duplicate members.
# Dictionary is a collection which is ordered** and changeable. No duplicate members.

# Compilation: When you write Python code and run it, the source code (.py files) 
# is first compiled into an intermediate form called bytecode (.pyc files).
#  This bytecode is a lower-level representation of your code, 
# but it is still not directly machine code. It’s something that 
# the Python Virtual Machine (PVM) can understand and execute.

# Interpretation: After Python code is compiled into bytecode, 
# it is executed by the Python Virtual Machine (PVM), which is an interpreter. 
# The PVM reads the bytecode and executes it line-by-line at runtime, 
# which is why Python is considered an interpreted language in practice.

first = 100;
# def func1():
#     print("Inside Function");
# for num  in range(1,10):
#     if (num%2!=0): 
#         print(num);
#     result=+num
    
# print(func1(),'myresult'.upper());
float_num=float(first);
print(float_num);
print("-- Casting on python --")
int_num=int(4.79);
print(int_num);
str_num=str('s1000');   
print(str_num);
print(type(str_num));   
x = int(1) # x will be 1
y = int(2.8) # y will be 2
z = int("3") # z will be 3
x = float(1) # x will be 1.0
y = float(2.8) # y will be 2.8
z = float("3") # z will be 3.0
w = float("4.2") # w will be 4.2
a = '''Lorem ipsum dolor sit amet,
consectetur adipiscing elit,
sed do eiusmod tempor incididunt
ut labore et dolore magna aliqua.'''
print(a)
#Arrays
arr1 ="Hello, World!"
print(arr1[1].upper())
print(arr1[2:5]);
print('Looping through string');
for x in "banana":
    print(x.upper());   
str1="Python language is a interpreted high-level programming language.";
if 'Python' in str1:
    print("Yes, 'Python' is present.");
elif not '.net' in str1:
    print("No, '.net' is not present.");

print('programming' in str1);
print(str1.split(" "));
b = "Hello, World!"
print(b[:5].upper());
b = "Hello, World!"
print(b[-5:-2]);
print(b.strip());
print(b.replace("H", "J")); 
age = 36
txt = "My name is John, and I am {}"   
print(txt.format(age))
print(f"My name is John, and I am {age}");
price = 59
txt = f"The price is {price:.2f} dollars"
print(txt)
txt = f"The price is {10 * 10} dollars"
print(txt)
def bool_func():
    return True;
if bool_func():
    print("Boolean Function returned True".upper());    
else:
    print("Boolean Function returned False");

x = 200.0
print(isinstance(x, int))

def check_event(num):
    if num % 2 == 0:
        return True
    else:
        return False    
# print(check_event(10))
# type = input("Enter user type: ")
# if type==int(1):
#     print("Hello Admin");
# else:
#     print("Hello User", type);
# print('checking user input complete');
# y=True
# while y == True:
#     x=input("Enter a number: ")
#     try:
#         val=int(x);
#         print(f"You entered: {val}")    
#         y = False
#     except ValueError:
#         print("Invalid input. Please enter a valid integer.")
# print("Loop ended.");

# logical operators

# def logical_ops(a,b):
#     if a > 5 and b > 5:
#         return "Both numbers are greater than 5"
#     elif a > 5 or b > 5:
#         return "At least one number is greater than 5"
#     else:
#         return "Neither number is greater than 5"       
# print(logical_ops(6,6))

arr =['apple', 'banana', 'cherry']
# if arr[0] is 'apple':
#     print("Yes, 'apple' is present in the fruits list.")

#print('cherry' in arr,'yes it is present '+arr[2].upper());
# into_check=10
# if into_check & 10:
#     print("yes, bitwise AND is true");
#list items
list1 = ["apple", "banana", "cherry"]
#list1.append("orange")
# list1[1:2]= ["kiwi",'pineapple']
# list1.insert(3, "orange")
# print(list1)
# list extension
list2=['mango','grape']
# list1.extend(list2)
# # print(list1)

# # del entire list items
# del list2
# print(list1)

# print("Length of list1 is:", len(list1))
# list1.remove("banana")
# print("List after removing banana:", list1)
print (list2)
list2.clear()
print (list2)
#looping through list
# for x in list1:
#     print(x.upper());
# [print ('\n'+x.upper()) for x in list1]
#dictionary
my_dict = {
    "name": "John",
    "age": 30,
    "city": "New York"
}   

# print(my_dict);
# print(my_dict['name'].upper());

# thisdict = dict(name = "John", age = 36, country = "Norway")
# print(thisdict)

# tuple1 = ("apple", "banana", "cherry")
# print(tuple1[1].upper());
# #convert tuple to list
# list_from_tuple = list(tuple1)  
# print (list_from_tuple)

# List Comprehension in Python
a=[1,2,3,4,5]
convert = [val *2 for val in a ]
for v in convert:
    print(v)

# --- Realtime file watcher (simple polling, no extra dependencies) ---
# Watches a target file for changes and prints when it updates.
if __name__ == "__main__":
    import os
    import time
    from pathlib import Path

    # Change this to any file you want to watch
    target = Path(__file__).with_name("watched.txt")

    print("\n-- Realtime File Watcher --")
    print(f"Watching: {target}")
    print("Tip: edit and save the file to see updates. Press Ctrl+C to stop.")

    last_mtime = None
    try:
        while True:
            if target.exists():
                mtime = os.path.getmtime(target)
                if last_mtime is None:
                    last_mtime = mtime
                elif mtime != last_mtime:
                    last_mtime = mtime
                    print(f"Change detected at {time.strftime('%H:%M:%S')}")
            else:
                if last_mtime is not None:
                    last_mtime = None
                    print("File removed. Waiting for it to be created again...")

            time.sleep(1)
    except KeyboardInterrupt:
        print("\nWatcher stopped.")
