'''
Project Goal: We want to see the machine code of an assembly 8086 instruction

Project Name: Assembler with python

Author: Ali Rahimi

'''
Value32Bit = {

  "eax" : "000",
  "ecx" : "001",
  "edx" : "010",
  "ebx" : "011",
  "esp" : "100",
  "esi" : "110",
  "edi" : "111",
  "ebp" : "101"

}

Value16Bit = {

  "ax" : "000",
  "cx" : "001",
  "dx" : "010",
  "bx" : "011",
  "sp" : "100",
  "si" : "110",
  "di" : "111",
  "bp" : "101"

}
Value8Bit = {

  "al" : "000",
  "cl" : "001",
  "dl" : "010",
  "bl" : "011",
  "ah" : "100",
  "ch" : "101",
  "dh" : "110",
  "bh" : "111"

}

registers32Bit = ["eax", "ecx", "edx", "ebx", "esp", "esi", "edi", "ebp"]

registers16Bit = ["ax", "cx", "dx", "bx", "sp", "bp", "si", "di"]

registers8Bit = ["al", "cl", "dl", "bl", "ah", "ch", "dh", "bh"]

opCodesRegisters = {

    "add" : "000000",
    "or"  : "000010",
    "and" : "001000",
    "sub" : "001010"  
}

oldOpCodesMemories16and32Bit = {

    "add" : "01",
    "or"  : "09",
    "and" : "21",
    "sub" : "29"
}

oldOpCodesMemory8Bit = {

    "add" : "00",
    "or"  : "08",
    "and" : "20",
    "sub" : "28"
}


opCodesMemories16and32Bit = {

    "add" : "03",
    "or"  : "0b",
    "and" : "23",
    "sub" : "2b"
}

opCodesMemory8Bit = {

    "add" : "02",
    "or"  : "0a",
    "and" : "22",
    "sub" : "2a"
}

def evaluateMod(status):                                                   #evaluate mod by passing 0 or 1
    if status == 0:
        return "00"
    else:
        return "11"

def evaluateInstruction(instruction):                                      #evaluate the instruction 
    if instruction == "add":
        return "add"
    elif instruction == "or":
        return "or"
    elif instruction == "and":
        return "and"
    elif instruction == "sub":
        return "sub"


def isMemory(operator1, operator2, instruction, mod, swap):                #memory function 

    opCode = ""
    newOperator2 = ""
    
    for i in range (len(operator2)):                                       #remove braces from operator
        if(operator2[i] == '[' or operator2[i] == ']'):
            continue
        newOperator2 += operator2[i]


    if(operator1 in registers32Bit and newOperator2 in registers32Bit):    #if both 32 bit 
        if swap == 1:                                                      #check that the swap has been happened or not
            opCode += oldOpCodesMemories16and32Bit[instruction]
        else:
            opCode += opCodesMemories16and32Bit[instruction] 

        mod += Value32Bit[operator1]
        mod += Value32Bit[newOperator2]
        return(printPatter(opCode, mod))
        
    elif(operator1 in registers16Bit and newOperator2 in registers16Bit):  #if both 16 bit(this is not mentioned in this part because of the exceptions)       
        prefix = "\\x66"
        if swap == 1:                                                      #check that the swap has been happened or not
            opCode += oldOpCodesMemories16and32Bit[instruction]
        else:
            opCode += opCodesMemories16and32Bit[instruction] 
        
        mod += Value16Bit[operator1]
        mod += Value16Bit[newOperator2]
        return(prefix + printPatter(opCode, mod))

    elif(operator1 in registers8Bit and newOperator2 in registers8Bit):    #if both 8 bit
        if swap == 1:                                                      #check that the swap has been happened or not
            opCode += oldOpCodesMemory8Bit[instruction]
        else:
            opCode += opCodesMemory8Bit[instruction]
        
        mod += Value8Bit[operator1]        
        mod += Value8Bit[newOperator2]
        return(printPatter(opCode, mod))

    else:
        return("Not available")


    
def printPatter(opCode, mod):                                              #print the patter like \xopcode\xmod
    pattern = "\\x" + opCode + "\\"

    temp = hex(int(mod, 2))[1:]
    
    help = len(temp[1:])
    if help < 2:
        temp = temp[0] + "0" + temp[1:]

    return pattern + temp



def isRegister(operator1, operator2, instruction, mod):                    #memory function 

    opCode = ""
    
    if(operator1 in registers32Bit and operator2 in registers32Bit):       #if both 32 bit 
        opCode += oldOpCodesMemories16and32Bit[instruction] 
        mod += Value32Bit[operator2]
        mod += Value32Bit[operator1]
        return(printPatter(opCode, mod))
        
    elif(operator1 in registers16Bit and operator2 in registers16Bit):     #if both 16 bit(this is not mentioned in this part because of the exceptions)       
        prefix = "\\x66"
        opCode += oldOpCodesMemories16and32Bit[instruction]
        mod += Value16Bit[operator2]
        mod += Value16Bit[operator1]
        return(prefix + printPatter(opCode, mod))

    elif(operator1 in registers8Bit and operator2 in registers8Bit):       #if both 8 bit
        opCode += oldOpCodesMemory8Bit[instruction]
        mod += Value8Bit[operator2]
        mod += Value8Bit[operator1]        
        
        return(printPatter(opCode, mod))

    else:
        return("Not available")

res = ""                                                                   #all outputs


with open('input.txt') as file:                                            #read file and split by lines
    myString = file.read()
    myList = myString.splitlines()

    
    for i in range(len(myList)):                                           #read lines and split by space
        
        splited = myList[i].split(" ")
        
        opCode = opCodesRegisters[splited[0].lower()]                      #convert all cases to lower(not case sensetive)
        
        operators = splited[1].split(",")                                        

        operator1 = operators[0].lower()                                              
        operator2 = operators[1].lower()
        instruction = evaluateInstruction(splited[0].lower())


        if operator1[0] == '[':                                            #check the first operator is memory or not we swap that if it is memory
            operator1, operator2 = operator2, operator1
            mod = evaluateMod(0)                                           #evaluate mod 00
            swap = 1

            res += isMemory(operator1, operator2, instruction, mod, swap)  #call the memory function

        elif operator2[0] == '[':
            mod = evaluateMod(0)
            swap = 0
            res += isMemory(operator1, operator2, instruction, mod, swap)
        else:                                                              #it's register
            mod = evaluateMod(1)                                           #evaluate mod 11
            res += isRegister(operator1, operator2, instruction, mod)      #call the memory function


print(res)
