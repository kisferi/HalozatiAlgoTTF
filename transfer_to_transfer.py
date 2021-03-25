import random
import numpy

class TransferToTransfer:
    def __init__(self, numberOfAgent, baseStationPosition):
        self.numberOfAgent = numberOfAgent
        self.probabilityList = [0 for i in range(self.numberOfAgent*self.numberOfAgent)]
        self.optionsForRandomChoice = [i for i in range(self.numberOfAgent*self.numberOfAgent)]
        self.coverTimeList = [1 for i in range(self.numberOfAgent)]
        self.baseStationPosition = baseStationPosition
        self.generate_random_probabilty_matrix()
        self.probabilityMatrix = numpy.reshape(self.probabilityList, (self.numberOfAgent, self.numberOfAgent))
        self.tokenList = [1 for i in range(self.numberOfAgent)]
        self.tokenList[self.baseStationPosition] = 0
        self.calculate_cover_time()
        print('TransferToTransfer object is created!')
        print('Probability list:')
        print(self.probabilityList)
        print('Probability matrix:')
        print(self.probabilityMatrix)
        print('Cover time list:')
        print(self.coverTimeList)

    def calculate_cover_time(self):
        for currentAgent in range(self.numberOfAgent):
            for i in range(self.numberOfAgent):
                for j in range(self.numberOfAgent):
                    if (i == currentAgent) != (j == currentAgent):
                        # TODO: this calculation is not the appropriate, just similar, but is it good for us? (Page 5 / cover time)
                        self.coverTimeList[currentAgent] *= self.probabilityMatrix[i][j]

            self.coverTimeList[currentAgent] = 1 - self.coverTimeList[currentAgent]

    def generate_random_probabilty_matrix(self):
        diagonal = 0
        generatedNumbersSum = 0
        for i in range(len(self.probabilityList)):
            if i != diagonal:
                self.probabilityList[i] = random.randint(1, 1000)
                generatedNumbersSum += self.probabilityList[i]
            else:
                diagonal += self.numberOfAgent + 1

        probabilitySum = 0
        for i in range(len(self.probabilityList)):
            self.probabilityList[i] = self.probabilityList[i] / generatedNumbersSum
            probabilitySum += self.probabilityList[i]

        if probabilitySum != 1:
            self.probabilityList[1] += 1 - probabilitySum

    def calculate_index(self, numberOflabel):
        return (numberOflabel % self.numberOfAgent, int(numberOflabel / self.numberOfAgent))

    def make_transaction(self, sender, receiver):
        self.tokenList[receiver] += self.tokenList[sender]
        self.tokenList[sender] = 0

    def cover_time_greater(self, sender, receiver):
        if self.coverTimeList[sender] > self.coverTimeList[receiver]:
            return True
        return False

    def token_transaction(self, interactionPair):
        # TODO: is there a direction of a transaction?
        if interactionPair[0] == self.baseStationPosition or interactionPair[1] == self.baseStationPosition:
            if interactionPair[0] == self.baseStationPosition:
                self.make_transaction(interactionPair[1], self.baseStationPosition)
            else:
                self.make_transaction(interactionPair[0], self.baseStationPosition)
            return True

        if self.cover_time_greater(interactionPair[0], interactionPair[1]):
            self.make_transaction(interactionPair[0], interactionPair[1])
            return True

        if self.cover_time_greater(interactionPair[1], interactionPair[0]):
            self.make_transaction(interactionPair[1], interactionPair[0])
            return True

        return False

    def next_interaction(self):
        currentInteraction = self.calculate_index(numpy.random.choice(self.optionsForRandomChoice, p=self.probabilityList))
        return [currentInteraction, self.token_transaction(currentInteraction)]

    def is_termination_configuration(self):
        return self.tokenList[self.baseStationPosition] == self.numberOfAgent - 1
