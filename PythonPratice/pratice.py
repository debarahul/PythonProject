'''from collections import namedtuple
a = namedtuple('course', 'name, usedTech')
b = a('datascience', 'python')
c = a('datascience', 'ml')
d = a._make(['langu', 'c'])
print(b)
print(c)
print(d) '''
#deque --> deque is pronounced as 'deck' is an optimised list to perform insertion and deletion easily.
"""from collections import deque
a = ['d', 'e', 'b', 'a', 's', 'i', 's', 'h']
print(a)
a.append('na')
print(a)
a.insert(0, 'm')
print(a)
b = deque(a)
print (b)
b.append('yak')
print(b)
b.insert(1, 'r.')
print(b)
b.remove('yak')
print(b)
b.appendleft('Hello')
print(b)
b.pop()
print(b)
b.popleft()
print(b)
"""
#Chainmap -> chainmap is a dictionary like class for creating a single view of multiple mappings
'''from collections import ChainMap
a = {1: 'python' ,2: 'java'}
b = {3: 'c' ,4: 'linux'}
c = {5:"c++"}
d = ChainMap(a,b,c)
print(d)'''
#Counter --> Counter is a dictionary subclass for counting hashable objects...
'''from collections import Counter
a=[1,2,3,4,5,6,7,8,9,0,1,3,5,5,3,4,2,6,2,2,5,2,2,6,6,78,4]
b = Counter(a)
print(b)
print(list(b.elements()))
print(b.most_common())
sub={2:1, 5:2}
print(b.subtract(sub))
print(b.most_common()) '''
#OrderDict --> OrderDict is dictionary subclass which remembers the order in which the entires were done.
'''from collections import OrderedDict

d = OrderedDict()
d[1] = 'd'
d[2] = 'e'
d[3] = 'b'
d[4] = 'a'
d[5] = 's'
d[6] = 'i'
d[7] = 's'
d[8] = 'h'

print(d)
print(d.keys())
print(d.values())
print(d.items())
print(d.popitem())
d[1] = 'a'
print(d)  '''
#defaultDict --> Defaultdict is a dictionary subclass which calls a factory function to supply missing values.
'''from collections import defaultdict
d = defaultdict(str)
d[1] = 'debasish'
d[2] = 'asish'
print(d[3])
#simple distonary , if we use then throw error so that we can use default dict instate of normal dict.
a= {1: 'sahil', 2:'rahul'}
print(a[3])  '''
#UserDict --> its a wrapper around dictionary objects for easier dictionary sub-classing.
#UserList --> Its a wrapper around list objects for easier list sub-classing.
#UserString--> Its a wrapper around string objects for easier string sub-classing.
#Array --> An a array a basically data structure which can hold more than one value at a time. its collection or ordered series of element of the same type.
#Python List and array have the same way store data, where List can store anytype of data type but array take only a single data type element.
#ValueError: bad typecode (must be b, B, u, h, H, i, I, l, L, q, Q, f or d)
'''print('1st method to create array')
import array
a = array.array('i',[0,1,2,3,4,5,6,7,8,9])
print(a)
print('2nd Method')
import array as arr
b = arr.array('l',[0,9,8,7,6,5,4,3,2,1])
print(b)
print("3rd Method")
from array import *
c = array('d',[0,2,3,5,7,9])
print(c)
print(a[8])
print(a[-4])
print(len(c))

d=arr.array('d',[1,2,4,5.6,2,5,2,2,1])
d.append(7.9)
print("Array a\d=",d)
e=arr.array('i',[1,2,3,4,31,1,13,4])
e.extend([1,5,7,3,2])
print('extend value=', e)
f=arr.array('d',[4,12.3,2.1,1.2,1.2,1.1,1.2,1.2])
f.insert(0,4.56)
f.insert(3,21.4)
print("after insert=",f)
#pop() -> function used when u want to remove an element and return it.
#remove() --> function used when to remove an element with a specific value without returning it.
import array as arr
g=arr.array('d',[1,2,3,4,5,6,7,8,9,0])
print("poping without specified, that poping last element",g.pop())
print("poping 4th values", g.pop(3))
print("poping with '-'", g.pop(-3))
i=arr.array('d',[1,2,3,4,5,6,7,8,9,0])
i.remove(3)
print(i)
#Concatenation and slicing(symbol - :)
import array as arr
j=arr.array('i',[2,3,4,5,6,2,1,1])
k=arr.array('i',[3,5,2,1,45])
#l=arr.array('i')
l=j+k
print('Concat',l)
#slicing function
print(l[0:8])
print(l[::-1])
print(l[0:-2]) '''
#looping in array
