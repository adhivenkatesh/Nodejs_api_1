#Python 3.14.2 (tags/v3.14.2:df79316, Dec  5 2025, 17:18:21) [MSC v.1944 64 bit (AMD64)] on win32
#Enter "help" below or click "Help" above for more information.
 
f = open("demofile.txt")
Traceback (most recent call last):
  File "<pyshell#1>", line 1, in <module>
    f = open("demofile.txt")
FileNotFoundError: [Errno 2] No such file or directory: 'demofile.txt'
f=open("d:\justtextfile.txt")
f=open("d:\justtextfile.txt")
f = open("justtextfile.txt", "rt")
Traceback (most recent call last):
  File "<pyshell#4>", line 1, in <module>
    f = open("justtextfile.txt", "rt")
FileNotFoundError: [Errno 2] No such file or directory: 'justtextfile.txt'
print(1)
f = open("d:\justtextfile.txt", "rt")
python --version
Traceback (most recent call last):
  File "<pyshell#6>", line 1, in <module>
    python --version
NameError: name 'python' is not defined
print("s");
s
x="John"
print x
SyntaxError: Missing parentheses in call to 'print'. Did you mean print(...)?
print (x)
John
x=1234
print (x)
1234
x=str("John")
x=1
print (x)
1
x=.str("John")
SyntaxError: invalid syntax
x=str("John")
print (x)
John
print (x+1)
Traceback (most recent call last):
  File "<pyshell#19>", line 1, in <module>
    print (x+1)
TypeError: can only concatenate str (not "int") to str
print(type(x))
<class 'str'>
x,y,j = 'apple',"Orange","Banana"
print (x)
apple
print (j)
Banana
x=y=j='Orange'
print (j)
Orange
fruits =['apple',"Banana","Pinnaple"]
print(fruits(1))
Traceback (most recent call last):
  File "<pyshell#27>", line 1, in <module>
    print(fruits(1))
TypeError: 'list' object is not callable
print(fruits[1])
Banana
p="Python'
SyntaxError: unterminated string literal (detected at line 1)
p="Python"
def func(): print(p)
func()
SyntaxError: invalid syntax
def func():
    print(p)
    .
    
SyntaxError: invalid syntax
def func():
    print(p)
return
SyntaxError: invalid syntax
def func():
    print(p)
def func():
    print(p)
return ("")
SyntaxError: invalid syntax
def add_numbers(a, b):
    sum_result = a + b
    return sum_result

add_numbers(1,2)
3
def func():
    print(p)

    
func()
Python
dict1 = {'class":4,"school":'government'}
         
SyntaxError: unterminated string literal (detected at line 1)
dict1 = {"class":4,"school":'government'}
         
print (dict1)
         
{'class': 4, 'school': 'government'}
b="Python Learning"
         
print(b[2.4])
         
Traceback (most recent call last):
  File "<pyshell#49>", line 1, in <module>
    print(b[2.4])
TypeError: string indices must be integers, not 'float'
print(b[2:4])
         
th
b="Python"
         
print(b[2:4])
         
th
b="Python Learning"
         
b="Python, Learning"
         
print(b[2:4])
         
th
b = "Hello, World!"
         
print(b[2:4])
         
ll
print(b[1])
         
e
print(b[5])
         
,
print(b[5,2])
         
Traceback (most recent call last):
  File "<pyshell#60>", line 1, in <module>
    print(b[5,2])
TypeError: string indices must be integers, not 'tuple'
print(b[5:2])
         

print(b[2:2])
         

for x in 'banana'
         
SyntaxError: expected ':'
for x in 'banana':
         print (x)

         
b
a
n
a
n
a

# Initialize an accumulator variable
total_sum = 0
# Iterate over a range of numbers (1 to 5 inclusive)
for number in range(1, 6):
    total_sum += number # Add the current number to the running total
    print(f"Current sum after adding {number}: {total_sum}")

print(f"The final total sum is: {total_sum}")

SyntaxError: multiple statements found while compiling a single statement

# Initialize an accumulator variable
total_sum = 0
# Iterate over a range of numbers (1 to 5 inclusive)
for number in range(1, 6):
    total_sum += number # Add the current number to the running total
    print(f"Current sum after adding {number}: {total_sum}")

print(f"The final total sum is: {total_sum}")
         
SyntaxError: multiple statements found while compiling a single statement
total_sum = 0
         
for number in range(1, 6):
    total_sum += number # Add the current number to the running total
    print(f"Current sum after adding {number}: {total_sum}")

print(f"The final total sum is: {total_sum}")
         
SyntaxError: invalid syntax
for number in range(1, 6):
    total_sum += number # Add the current number to the running total
    print(f"Current sum after adding {number}: {total_sum}")

Current sum after adding 1: 1
Current sum after adding 2: 3
Current sum after adding 3: 6
Current sum after adding 4: 10
Current sum after adding 5: 15
for num in range(0,10):
         print(num)

         
0
1
2
3
4
5
6
7
8
9
print(b)
         
Hello, World!
for txt in b:
         print (txt)

         
H
e
l
l
o
,
 
W
o
r
l
d
!
for txt in b:
         print (txt\n)
         
SyntaxError: unexpected character after line continuation character
for txt in b:
         print (txt+'\n')

         
H

e

l

l

o

,

 

W

o

r

l

d

!

for txt in range(1,20):
         print (txt+'\n')

         
Traceback (most recent call last):
  File "<pyshell#85>", line 2, in <module>
    print (txt+'\n')
TypeError: unsupported operand type(s) for +: 'int' and 'str'
a='good'
         
b='GOOD'
         
if a==b: print('yes')

         


if a==b: print('yes')
         else:print('no')
         
SyntaxError: unexpected indent
if a==b: print('yes')
         else: print('no')
         
SyntaxError: unexpected indent
if a==b: print('yes')
else: print('no')

no
a='GOOD'
if a==b: print('yes')
else: print('no')

yes
day=5
match day:
    case 1:
    print ("Monday")
    
SyntaxError: expected an indented block after 'case' statement on line 2
match day:
case 1:
print ("Monday")
SyntaxError: expected an indented block after 'match' statement on line 1
match day:
  case 1:
  print ("Monday")
  
SyntaxError: expected an indented block after 'case' statement on line 2
match day:
  case 1:
  print("Monday")
  
SyntaxError: expected an indented block after 'case' statement on line 2
match day:
  case 1:
  print("Monday")
  
SyntaxError: expected an indented block after 'case' statement on line 2
match day:
  case 1:
    print("Monday")
  case 2:
    print("Tuesday")
  case 3:
    print("Wednesday")
  case 4:
    print("Thursday")
  case 5:
    print("Friday")
  case 6:
    print("Saturday")
  case 7:
    print("Sunday")
SyntaxError: invalid non-printable character U+00A0
match day:
case 1:
    print("Monday")
case 2:
    print("Tuesday")
case 3:
    print("Wednesday")
case 4:
    print("Thursday")
case 5:
    print("Friday")

SyntaxError: invalid non-printable character U+00A0

match day:
case 1: print("Monday")
case 2: print("Tuesday")
case 3: print("Wednesday")
case 4: print("Thursday")
case 5: print("Friday")
         
SyntaxError: expected an indented block after 'match' statement on line 1
def http_error(status):
    match(status):
        case 201:
        return "created"
    
SyntaxError: expected an indented block after 'case' statement on line 3
def http_error(status):
    match(status):
         case 201:
        return "created"
    
SyntaxError: unindent does not match any outer indentation level
def http_error(status):
    match status:
        case 400:
            return "Bad request"
        case 404 | 405 | 406:
            return "Not found, method not allowed, or unacceptable"
        case _:
            return "Something else went wrong"

print(http_error(404))
# Output: Not found, method not allowed, or unacceptable
def http_error(status):
    match(status):
         case 201:
            return "created"
        
SyntaxError: invalid syntax
def http_error(status):
    match status:
        case 400:
            return "Bad request"
        case 404 | 405 | 406:
            return "Not found, method not allowed, or unacceptable"
        case _:
            return "Something else went wrong"

print(http_error(404))
# Output: Not found, method not allowed, or unacceptable
def http_error(status):
    match(status):
         case 201:
             return "created"
            
SyntaxError: invalid syntax
def http_error(status):
    match status:
        case 400:
            return "Bad request"
        case 404 | 405 | 406:
            return "Not found, method not allowed, or unacceptable"
        case _:
            return "Something else went wrong"

print(http_error(404))
# Output: Not found, method not allowed, or unacceptable
def http_error(status):
    match status:
         case 201:
             return "created"
            
SyntaxError: invalid syntax
def http_error(status):
    match status:
        case 400:
            return "Bad request"
        case 404 | 405 | 406:
            return "Not found, method not allowed, or unacceptable"
        case _:
            return "Something else went wrong"

print(http_error(404))
# Output: Not found, method not allowed, or unacceptable
def http_error(status):
    match status:
        case 201:
             return "created"
            
SyntaxError: invalid syntax
def http_error(status):
    match status:
        case 400:
            return "Bad request"
        case 404 | 405 | 406:
            return "Not found, method not allowed, or unacceptable"
        case _:
            return "Something else went wrong"

print(http_error(404))
# Output: Not found, method not allowed, or unacceptable
def http_error(status):
    match status:
        case 404:
             return "created"
            
SyntaxError: invalid syntax
def http_error(status):
    match status:
        case 400:
            return "Bad request"
        case 404 | 405 | 406:
            return "Not found, method not allowed, or unacceptable"
	case 201:
	    return "New value created"
        case _:
            return "Something else went wrong"

SyntaxError: inconsistent use of tabs and spaces in indentation
def http_error(status):
    match status:
        case 201:
	    return "New value created"
        case 400:
            return "Bad request"
        case 404 | 405 | 406:
            return "Not found, method not allowed, or unacceptable"
        case _:
            return "Something else went wrong"
        
SyntaxError: inconsistent use of tabs and spaces in indentation
>>> def http_error(status):
...     match status:
...         case 400:
...             return "Bad request"
...         case 404 | 405 | 406:
...             return "Not found, method not allowed, or unacceptable"
...         case _:
...             return "Something else went wrong"
... 
...         
>>> 
>>> 
>>> 
>>> 
>>> 
>>> http_error(405)
'Not found, method not allowed, or unacceptable'
>>> def http_error(status):
...     match status:
...         case 400:
...             return "Bad request"
...         case 404 | 405 | 406:
...             return "Not found, method not allowed, or unacceptable"
...         case 201:
...             return "Created"
...         case _:
...             return "Something else went wrong"
... 
...         
>>> 
>>> 
>>> 
>>> http_error(201)
'Created'
