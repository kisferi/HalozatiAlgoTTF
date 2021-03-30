import random
import numpy

class TransferToTransfer:
    def parse_json(self, json):
        print('Input json data:')
        print(json)

        self.probabilityList = []
        for item in json['agents_probability']:
            for i in item:
                self.probabilityList.append(i)

        self.numberOfAgents = int((len(self.probabilityList) + 1)**(0.5))

        if json['type'] == 'lazyttf':
            self.isLazy = True
            self.pVector = []
            for item in json['p_vector']:
                self.pVector.append(item)

            probabilitiesSum = 0
            for i in range(len(self.probabilityList)):
                self.probabilityList[i] = self.probabilityList[i] * self.pVector[i % self.numberOfAgents]
                probabilitiesSum += self.probabilityList[i]

            self.helperProbabilityList = []
            if probabilitiesSum != 1:
                self.helperProbabilityList =  [self.probabilityList[i] for i in range(len(self.probabilityList))]
                self.helperProbabilityList.append(1 - probabilitiesSum)

    def __init__(self, numberOfAgents, json = '', baseStationPosition = 0):
        self.isLazy = False

        if json:
            self.parse_json(json)
        else:
            self.numberOfAgents = numberOfAgents
            self.probabilityList = [0 for i in range(self.numberOfAgents*self.numberOfAgents)]
            self.generate_random_probabilty_matrix()

        self.baseStationPosition = baseStationPosition
        self.probabilityMatrix = numpy.reshape(self.probabilityList, (self.numberOfAgents, self.numberOfAgents))

        self.coverTimeList = [1 for i in range(self.numberOfAgents)]
        self.calculate_cover_time()
        self.make_categories()

        self.tokenList = [1 for i in range(self.numberOfAgents)]
        self.tokenList[self.baseStationPosition] = 0

        self.optionsForRandomChoice = [i for i in range(self.numberOfAgents*self.numberOfAgents)]
        if self.isLazy and self.helperProbabilityList:
            self.optionsForRandomChoice.append(self.numberOfAgents*self.numberOfAgents)

        if self.isLazy:
            print('Lazy TransferToTransfer object is created!')
        else:
            print('TransferToTransfer object is created!')

        print('Probability list:')
        print(self.probabilityList)
        print('Probability matrix:')
        print(self.probabilityMatrix)
        print('Cover time list:')
        print(self.coverTimeList)
        print('Cover time categories:')
        print(self.coverTimeCategories)

        if self.isLazy:
            print('p vector:')
            print(self.pVector)

    def make_categories(self):
        self.coverTimeCategories = dict()
        for coverTime in self.coverTimeList:
            if coverTime not in self.coverTimeCategories:
                sum = 0
                for currentTime in self.coverTimeList:
                    if coverTime == currentTime:
                        sum += 1

                self.coverTimeCategories[coverTime] = sum

    def calculate_cover_time(self):
        for currentAgent in range(self.numberOfAgents):
            for i in range(self.numberOfAgents):
                for j in range(i, self.numberOfAgents):
                    if (i == currentAgent) != (j == currentAgent):
                        self.coverTimeList[currentAgent] *= 1 - (2 ** -(self.probabilityMatrix[i][j] + self.probabilityMatrix[j][i])) + 0.00001
                        # 0.00001 magic number is needed because if both of the probabilities are zero then both of the cover times are one

            self.coverTimeList[currentAgent] = 1 - self.coverTimeList[currentAgent]

    def generate_random_probabilty_matrix(self):
        diagonal = 0
        generatedNumbersSum = 0
        for i in range(len(self.probabilityList)):
            if i != diagonal:
                self.probabilityList[i] = random.randint(1, 1000)
                generatedNumbersSum += self.probabilityList[i]
            else:
                diagonal += self.numberOfAgents + 1

        probabilitySum = 0
        for i in range(len(self.probabilityList)):
            self.probabilityList[i] = self.probabilityList[i] / generatedNumbersSum
            probabilitySum += self.probabilityList[i]

        if probabilitySum != 1:
            self.probabilityList[1] += 1 - probabilitySum

    def calculate_index(self, numberOflabel):
        return (numberOflabel % self.numberOfAgents, int(numberOflabel / self.numberOfAgents))

    def make_transaction(self, sender, receiver):
        if self.tokenList[sender] == 0:
            return False

        self.tokenList[receiver] += self.tokenList[sender]
        self.tokenList[sender] = 0
        return True

    def cover_time_greater(self, sender, receiver):
        if self.coverTimeList[sender] > self.coverTimeList[receiver]:
            return True
        return False

    def token_transaction(self, interactionPair):
        # interactionPair is a pair like (i,j). There is a direction and it means that i makes an interaction
        # and j can send its tokens to i if i is faster than j.
        # If i is the base station then j always sends its tokens if j has any tokens.
        if interactionPair[0] == self.baseStationPosition:
            return self.make_transaction(interactionPair[1], self.baseStationPosition)

        # If j is the base station then there are no tokens sending.
        if interactionPair[1] == self.baseStationPosition:
            return False

        if self.cover_time_greater(interactionPair[1], interactionPair[0]):
            return self.make_transaction(interactionPair[1], interactionPair[0])

        return False

    def next_interaction(self):
        if self.isLazy and self.helperProbabilityList:
            randomChoice = self.numberOfAgents*self.numberOfAgents
            while randomChoice == self.numberOfAgents*self.numberOfAgents:
                randomChoice = numpy.random.choice(self.optionsForRandomChoice, p=self.helperProbabilityList)

            currentInteraction = self.calculate_index(randomChoice)
        else:
            currentInteraction = self.calculate_index(numpy.random.choice(self.optionsForRandomChoice, p=self.probabilityList))

        return [currentInteraction, self.token_transaction(currentInteraction)]

    def is_termination_configuration(self):
        return self.tokenList[self.baseStationPosition] == self.numberOfAgents - 1
