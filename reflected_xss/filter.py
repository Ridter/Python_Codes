import re
def sort():
    f=open("urllist","r")
    arr=f.readlines()
    f.close()
    a1=set(arr)
    a2=[i for i in a1]
    f=open("urllist","w")
    for i in a2:
        f.write(i)
    f.close()
def filter():
    f=open("urllist","r")
    a=f.readlines()
    dellist=[]
    for i in a:
        if i.find("?")==-1:
           dellist.append(i) 
    for i in dellist:
        a.remove(i)
    f.close()
    f=open("urllist","w")
    for i in a:
        f.write(i)
    f.close()
    sort()
if __name__=="__main__":
    filter()
