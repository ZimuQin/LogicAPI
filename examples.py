from LogicAPI import Term, Var, query, Cut, _, Func, BoolFunc, Object

# Example code
class f(Term): pass # define predicates
class g(Term): pass
class h(Term): pass
X = Var('X') # define variables
Y = Var('Y')
Z = Var('Z')
+f(1) # define facts
+f(2)
+g(4)
+g(5)
+g(6)
+h(4)
f(X) <= g(X) & h(X) # define rules
print 'query f(X):\n\t', list(query(f(X))) # lists all solutions to the query
print 'query f(X) & Cut():\n\t', list(query(f(X) & Cut()))


A = Var('A')
B = Var('B')
C = Var('C')
D = Var('D')
E = Var('E')
F = Var('F')
+f(A, C, C, E, E, 0)
print 'query f(B, C, F, E, 0, 0):\n\t', list(query(f(B, C, F, E, 0, 0)))


class path(Term): pass
class arc(Term): pass
From = Var('From')
To = Var('To')
I = Var('I')
L = Var('L')
L2 = Var('L2')

path(From, To) <= arc(From, To)
path(From, To) <= arc(From, I) & path(I, To)
+arc('a', 'b')
+arc('b', 'c')
+arc('c', 'd')
+arc('b', 'e')
+arc('c', 'f')
print 'query path(From, To):\n\t', list(query(path(From, To)))


class parent(Term): pass

class grandparent(Term): pass

X = Var('X')
Y = Var('Y')
Z = Var('Z')

+parent('pete','ian')
+parent('ian','peter')
+parent('ian','lucy')
+parent('lou','pete')
+parent('lou','pauline')
+parent('cathy','ian')

grandparent(X, Y) <= parent(X, Z) & parent(Z, Y)
print 'query grandparent(X, Y):\n\t', list(query(grandparent(X, Y)))


class append(Term): pass
L2 = Var('L2')
L3 = Var('L3')
H = Var('H')
T = Var('T')

+append([], L, L)
append([H]+T, L2, [H]+L3) <= append(T, L2, L3)
print 'query append([1,2], [4,6], L):\n\t', list(query(append([1,2], [4,6], L)))

class reverse(Term): pass
+reverse([], L, L)
reverse([H]+T, L, L2) <= reverse(T, L, [H]+L2)
reverse(L, L2) <= reverse(L, L2, [])
print 'query reverse([4,5,6,\'a\'], L):\n\t', list(query(reverse([4,5,6,'a'], L)))

class reverse2(Term): pass
+reverse2([], [])
reverse2([H]+T, L) <= reverse2(T, L2) & (L == L2+[H])
print 'query reverse2([4,5,6,\'a\'], L):\n\t', list(query(reverse2([4,5,6,'a'], L)))

class reverseFunc(Func): # define functions
    def function(self, l):
        return l[::-1]

class reverse3(Term): pass
+reverse3(L, reverseFunc(L))
print 'query reverse3([4,5,6,\'a\'], L):\n\t', list(query(reverse3([4,5,6,'a'], L)))


class member(Term): pass
+member(X, [X]+_)
member(X, [Y]+T) <= member(X, T)
print 'query member(X,[1,2,3]) & ~member(X, [1,4,5]):\n\t', list(query(member(X,[1,2,3]) & ~member(X, [1,4,5])))

class not_in(Term): pass
+not_in([], L, [])
not_in([X]+Y, L, [X]+L2) <= (~member(X, L)) & Cut() & not_in(Y, L, L2)
not_in([X]+Y, L, L2) <= not_in(Y, L, L2)
print 'query not_in([1,2,3,4], [1], L):\n\t', list(query(not_in([1,2,3,4], [1], L)))

class write(Func):
    def function(self, form, *args):
        print(str(form) % args)
l = list(query(f(X) & ~(X >= 3) & write('%s is written.', X)))
print 'query f(X) & ~(X >= 3) & write(\'%s is written.\', X):\n\t', l


class is_prime(BoolFunc): # define boolean functions
    def function(self, n):
        if n == 2:
            return True
        if n < 2 or n % 2 == 0:
            return False
        for i in range(3, int(n**0.5) + 1, 2):
            if n % i == 0:
                return False
        return True

class primes(Term): pass
primes(X, []) <= (X <= 1) & Cut()
primes(X, L) <= is_prime(X) & Cut() & primes(X - 1, L2) & (L == L2+[X])
primes(X, L) <= primes(X - 1, L)

print 'query primes(100, L):\n\t', list(query(primes(100, L)))


class Person(Object): # enables object-oriented paradigm
    class age(Term): pass # define predicate in class
    def __init__(self, name, age):
        self.name = name
        +self.age(self, age)
    def __repr__(self):
        return self.name

a = Person('a', 15)
b = Person('b', 19)
c = Person('c', 13)
d = Person('d', 24)
e = Person('e', 16)
f = Person('f', 17)

print 'query Person.age(X, A) & (A <= 18):\n\t', list(query(Person.age(X, A) & (A <= 18)))