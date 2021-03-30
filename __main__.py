import argparse
import json
import transfer_to_transfer as ttf

parser = argparse.ArgumentParser(description='Transfer to tranfer')
parser.add_argument('-agents', dest='numberOfAgents', type=int, default=3,
                    help='number of agents with generated probability matrix (default:3)')
parser.add_argument('-json', dest='jsonFile',
                    help='input json file path')

args = parser.parse_args()

def running_ttf(ttfObject):
    numberOfInteractions = 0
    while ttfObject.is_termination_configuration() != True:
        print('Current interaction: ', ttfObject.next_interaction())
        numberOfInteractions += 1
        print('Number of interactions: ', numberOfInteractions)
        print('TokenList: ', ttfObject.tokenList)

    print('Result number of interaction: ', numberOfInteractions)

def test_with_generating_probability(numberOfAgents):
    simpleTtf = ttf.TransferToTransfer(numberOfAgents)
    running_ttf(simpleTtf)


def test_with_json_file(jsonFile):
    inputFile = open(jsonFile)
    jsonArray = json.load(inputFile)
    simpleTtf = ttf.TransferToTransfer(0, jsonArray)
    running_ttf(simpleTtf)

def main():
    if args.numberOfAgents and not args.jsonFile:
        test_with_generating_probability(args.numberOfAgents)

    if args.jsonFile:
        test_with_json_file(args.jsonFile)

if __name__ == "__main__":
    main()
