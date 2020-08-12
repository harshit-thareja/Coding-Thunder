from random import shuffle
def generater():
     list = [0,1,2,3,4,5,6,7,8,9]
     shuffle(list)
     slist = list[0:4]
     print("Your OTP is:",end=" ")
     for i in slist:
          print(i,end="")
generater()