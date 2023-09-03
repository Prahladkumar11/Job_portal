from django.test import TestCase

a='name_1.jpg'
b,c=a.rsplit('_',1)
d,e=c.rsplit('.',1)
print(e,'jjf',d)
print(type(d))
f=int(d)+1
print(f)