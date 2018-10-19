import re
import pprint

def Remove(duplicate): 
    final_list = [] 
    for num in duplicate: 
        if num not in final_list: 
            final_list.append(num) 
    return final_list 
    
#bible = open("bible11.txt", "r")
#regex = re.compile(r'\b\w{18}\b')
#regexJesus = re.compile(r'(?i)jesus')
#memoryBible = bible.read()
#result = regex.findall(memoryBible)
#resultJesus = regexJesus.findall(memoryBible)

#print(len(result))
#print(result)
#print(Remove(resultJesus))
#print('"Jesus" is mentioned {0} times.'.format(len(resultJesus)))

ccg = open('CCG_AVL_DATA.txt','r')
#regexCCG = re.compile(r'TVL.*\'')
memoryCCG = ccg.read()




# resultCCG = regexCCG.findall(memoryCCG)
# # (?s) = re.findall(r'regexString',data,re.DOTALL)
# resultIFT = re.findall(r"(?s)(?m)IFT\+.*?\+(.*?)'",memoryCCG)
# print(Remove(resultCCG))
# print('Found {0}'.format(len(resultCCG)))
pp = pprint.PrettyPrinter(indent=4)
# pp.pprint(Remove(resultIFT))
# print('Found {0}'.format(len(resultIFT)))
# pp.pprint(resultIFT)


resultIFT2 = re.findall(r'(?s)(?m)IFT\+.*?\+(.*?)\'P', memoryCCG)
pp.pprint(resultIFT2)
for i,x in enumerate(resultIFT2):
    print('[{0}]\t{1}'.format(str(i).rjust(3),re.sub(r'\n \d*? ','',x)))
print('Found {0}'.format(len(resultIFT2)))
#print(resultIFT2)


resultTFF = re.findall(r'(?s)(?m)(TFF\+.*?\')', memoryCCG)
for i,x in enumerate(resultTFF):
    print('[{0}]\t{1}'.format(str(i).rjust(3),re.sub(r'\s*\d{1,2} ','',x)))
print('Found {0}'.format(len(resultTFF)))
