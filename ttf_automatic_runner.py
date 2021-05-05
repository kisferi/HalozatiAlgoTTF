import json
import transfer_to_transfer as ttf

files = ['sample1.json', 'sample2.json','sample3.json', 'sample4_1.json','sample4_2.json', 'sample5.json','sample6.json']
f=open("test_ttf_generated.txt", "a+")
for file in files:
    for i in range(0,1000):
        inputFile = open(file)
        jsonArray = json.load(inputFile)
        ttfObject = ttf.TransferToTransfer(0, jsonArray)
        # running_ttf(simpleTtf)
        index = 0
        while ttfObject.is_termination_configuration() != True:
            current = ttfObject.next_interaction()
            index += 1
        
        f.write(file+";" + str(index) + ";" + str(ttfObject.numberOfDataTransitions) + '\n')
        print(file+";" + str(index) + ";" + str(ttfObject.numberOfDataTransitions) + '\n')

f.close()