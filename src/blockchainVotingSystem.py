import matplotlib.pyplot as plt
from numpy import invert

from blockchain import *
from hashlib import sha256
import random
import json


class Election():
    def __init__(self, blockchain, candidates, voters):
        self.blockchain = blockchain
        self.candidates = candidates
        self.voters = voters
        self.authorizeVoters()

    # A voter cant vote more than one time since we
    # give voters only one choice.

    def authorizeVoters(self):
        for voter in voters:
            self.blockchain.forceTransaction(transaction("null", voter, 1))

        self.blockchain.handleTransaction("null")

    def vote(self, voter, candidate):
        self.blockchain.addTransaction(transaction(voter, candidate, 1))

    def countVotes(self):
        results = {}
        for candidate in self.candidates:
            results[candidate] = self.blockchain.getBalance(candidate)

        return results


class ElectionHelper():
    def __init__(self, blockchain, candidates, voters):
        self.blockchain = blockchain
        self.candidates = candidates.copy()
        self.voters = voters.copy()
        self.newElection = Election(
            self.blockchain, self.candidates, self.voters)

    # Election
    def startElection(self):
        electionSize = len(self.voters)
        for i in range(electionSize):
            rand = random.randint(0, len(self.candidates) - 1)
            self.newElection.vote(self.voters[i], self.candidates[rand])

        self.blockchain.handleTransaction("null")

        print("Election is over! Now we count the votes.\nResults:")
        self.showResults()

    def showResults(self):
        results = self.newElection.countVotes()
        print(json.dumps(results, sort_keys=True, indent=3))

        candidates = results.keys()
        votes = results.values()

        winner = max(votes)
        winnerName = ""

        for key, value in results.items():
            if value == winner:
                winnerName = key
                break

        print(
            f"{winnerName} is won the election with {winner} votes.")

        plt.bar(candidates, votes)
        plt.show()

#-----------------------------------#

# Generating random voters.


def randomWordGenerator():
    randomWord = ""
    for j in range(50):
        randomWord += random.choice(string.ascii_lowercase)
    return sha256(randomWord.encode('utf-8')).hexdigest()


# An election with 4 candidates and 10000 voters

block1 = blockchain(0, 0.1)

electionSize = 10000
candidates = ["berk", "alice", "bob", "unnamed"]

voters = []
for i in range(electionSize):
    randomVoter = randomWordGenerator()
    voters.append(randomVoter)


election = ElectionHelper(block1, candidates, voters)
election.startElection()
