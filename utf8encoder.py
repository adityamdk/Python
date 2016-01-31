#program to convert utf 16 to utf 8 encoding for the given input file.
# (limited to converting to utf8 where in utf 8  max 3 bytes are needed in final representation


# Input format example :python anagram.py english_in.txt
# Output will be written to a file called "utf8encoder_out.txt" .



import sys
reload(sys)
sys.setdefaultencoding("UTF-8")
from sys import argv
import binascii
script,filename = argv


# function to convert the characters which need 2 bytes to be represented in utf8
def TwoByteVal(s):
 #print "printing values"
 InterMediateListR = ['1','1','0','0','0','0','0','0','1','0','0','0','0','0','0','0']
 InterMediateList = InterMediateListR[::-1]
 strLen = len(s)
 #reverses the string
 doubleBytes = s[::-1]
 #print doubleBytes
 byteOne = doubleBytes[:6]
 ListByteOne = list(byteOne)
 byteTwo = doubleBytes[6:]
 ListByteTwo = list(byteTwo)
 ZeroToBeFilled = 11 - strLen
 for j in range(ZeroToBeFilled) :
    ListByteTwo.append('0')
 k=0
 for i in range(0,6):
     InterMediateList[k]=ListByteOne[i]
     k+=1
 j =0
 for i in range(8,13):
     InterMediateList[i] =ListByteTwo[j]
     j+=1
 FinalList = "".join(InterMediateList)
 TheFinal = FinalList[::-1]
 return TheFinal

# function to convert the characters which need 3 bytes to be represented in utf8
def ThreeByteVal(s):
     #print"three bytes"
     #1110xxxx 10xxxxxx 10xxxxxx
     InterMediateListR = ['1','1','1','0','0','0','0','0','1','0','0','0','0','0','0','0','1','0','0','0','0','0','0','0']
     InterMediateList = InterMediateListR[::-1]
     strLen = len(s)
     #reverses the string
     doubleBytes = s[::-1]
     #print doubleBytes
     byteOne = doubleBytes[:6]
     ListByteOne = list(byteOne)
     byteTwo = doubleBytes[6:12]
     ListByteTwo = list(byteTwo)

     byteThree = doubleBytes[12:]
     ListByteThree = list(byteThree)

     ZeroToBeFilled = 16 - strLen
     for j in range(ZeroToBeFilled) :
        ListByteThree.append('0')
     k=0
     for i in range(0,6):
         InterMediateList[k]=ListByteOne[i]
         k+=1
     j =0
     for i in range(8,14):
         InterMediateList[i] =ListByteTwo[j]
         j+=1

     j=0
     for i in range(16,20):
         InterMediateList[i] =ListByteThree[j]
         j+=1


     FinalList = "".join(InterMediateList)
     TheFinal = FinalList[::-1]
     return TheFinal




FileContents = []
FinalArray = []
ReadFile = open(filename,"rb")
WriteOutFile = open("utf8encoder_out.txt","w")
Data = ReadFile.read(2)
while Data:
    FileContents.append(Data)
    Data = ReadFile.read(2)

for character in FileContents:
    value = int("".join(map(lambda x:'%02x' %ord(x),character)),16)
    #print value
    charValue = str('{0:08b}'.format(value))
    #print charValue
    flag = 0
    # computes the number of bytes to be used for encoding
    length = 0
    if(value <= 127):
      #print "1 byte"
     # FinalArray = SingleByteFunc(charValue)
      InpLen = len(charValue)
      byteArray = ['0','0','0','0','0','0','0','0']
      ArrayLen = len(byteArray)
      for i in range(ArrayLen-1,0,-1):
        if(i==0):
            continue
        InpLen = InpLen-1
        if(InpLen!=-1):
            byteArray[i]=charValue[InpLen]
            #print
     # byteArray = byteArray.zfill(8)
      FinalArray = "".join(byteArray)
      #print FinalArray



      Out = hex(int(FinalArray,2))
      if((len(Out)%2)==0):
        WriteOutFile.write(binascii.unhexlify(Out[2:]))
      else:
        WriteOutFile.write(binascii.unhexlify('0a'))

    elif(value<=2047):
       #print "2 bytes"
       FinalArray=TwoByteVal(charValue)
       Out = hex(int(FinalArray,2))
       WriteOutFile.write(binascii.unhexlify(Out[2:]))

    else:
      # print "3 bytes"
      FinalArray=ThreeByteVal(charValue)
      Out = hex(int(FinalArray,2))
      WriteOutFile.write(binascii.unhexlify(Out[2:]))
