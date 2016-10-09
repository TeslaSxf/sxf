import random
def bubble_sort(l):
    lenth=len(l)
    for i in range(lenth-1,0,-1):
        for j in range(i):
            if l[j]>l[j+1]:
                l[j],l[j+1]=l[j+1],l[j]
    return l
l=range(10,0,-1)
def select_sort(l):
    lenth=len(l)
    for i in range(lenth-1):
        min=i
        for j in range(i+1,lenth):
            if l[j]<min:
                min=j
        l[i],l[min]=l[min],l[i]
    return l
def insert_sort(l):
    lenth=len(l)
    for i in range(1,lenth):
        for j in range(i,0,-1):
            if l[j]<l[j-1]:
                l[j],l[j-1]=l[j-1],l[j]
            else:
                break
    return l
def heap_sort(l):
    lenth=len(l)
    for i in range(lenth-1,0,-1):
        heap_adjust(l,i)
        l[i],l[0]=l[0],l[i]
    return l
def heap_adjust(l,d):
    node=(d-1)//2
    for i in range(node,-1,-1):
        m=i*2+1
        if i*2+2<=d and l[i*2+2]>l[i*2+1]:
            m=i*2+2
        if l[m]>l[i]:
            l[m],l[i]=l[i],l[m]

l=[]
for i in range(20):
    l.append(random.randint(1,100))
print(l)
heap_sort(l)
print(l)
