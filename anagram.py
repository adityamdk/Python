#program which takes a string from user and writes the anagrams of the string to an output file.
__author__ = 'Aditya'

#Function to swap two elements
def swap(array,index1,index2):
    temp = array[index1]
    array[index1] = array[index2]
    array[index2] = temp
    return array

#function to print the final string
def output(str,list):
    string =''
    r = string.join(str)
    list.append(r)
    return list

#function to print anagrams of a string
def anagram(array,start,end,list):
    if(start==end):
     list = output(array,list)
    else:
        for j in range(start,end+1):
            array = swap(array,start,j)
            anagram(array,start+1,end,list)
            array = swap(array,start,j)
    return list
#main

from sys import argv
inputFile = open("anagram_out.txt",'w')
script, input = argv
len1 = len(input)
mylist = []
array = list(input)
anagram(array,0,len1-1,mylist)
mylist.sort()
ll= len(mylist)

for i in range(ll):
    inputFile.writelines(mylist[i]+"\n")
  #  if(i!=ll-1):
      # inputFile.writelines("\n")
inputFile.close()