import sys
import transfer_to_transfer as ttf

def main():
    print(sys.argv)
    numberOfAgent = int(sys.argv[1])

    # TODO: base station is always in the zero position?
    simpleTtf = ttf.TransferToTransfer(numberOfAgent, 0)
    iteration = 1

    while simpleTtf.is_termination_configuration() != True:
        print(simpleTtf.next_interaction())
        print(iteration)
        iteration += 1
        print(simpleTtf.tokenList)

if __name__ == "__main__":
    main()