#importing required libraries
import hashlib
import datetime
import random
import time

#predefined constants
GENERATOR = 4
PRIME = 1101
DIFFICULTY = 4

#function to hash data wrt SHA256
def hash_block(block):
    sha = hashlib.sha256()
    #hash the data from all the tuples of the block
    sha.update(str(block[0]).encode('utf-8') + str(block[1]).encode('utf-8') + str(block[2]).encode('utf-8')  + str(block[3]).encode('utf-8') + str(block[4]).encode('utf-8'))
    return sha.hexdigest()

#function to add the first block to the blockchain 
def genesis_block():
    data = random.randint(1, PRIME - 1)
    # b = random.randint(0,1)
    carID = random.randint(1, 1000000000)
    new_block = [0, carID, datetime.datetime.now(),0, data]
    hash_of_block = hash_block(new_block)
    new_block.append(hash_of_block)
    return new_block

#function to create a new block
def createBlock(index, carID, previous_hash, data):
    block = [index, carID, datetime.datetime.now(), previous_hash,data]
    hash_of_block = hash_block(block)
    block.append(hash_of_block)
    return block

#function to verify if the blockchain is valid
def verifyChain(blockchain):
    for i in range(1,len(blockchain)):
        #current block's previous hash
        current = blockchain[i][3]
        #previous block's current hash
        previous = blockchain[i-1][5]
        #check if the block itself has been tampered with
        if(blockchain[i][5] != hash_block(blockchain[i])):
            return False
        #check  if the hashes are in orderly fashion in the chain
        if(previous != current):
            return False
    return True

#function to mine new blocks to add to the chain
def mine(index, blockchain):
    #start time to mine blocks
    start = time.time()
    #get the carID for the previous block
    carID = blockchain[index - 1][1]
    #calculate y
    y = (GENERATOR ** carID) % PRIME
    #bruteforce values of r and b to solve for the ZKP
    while(int(blockchain[index-1][5][0:2], 16)):
        #calculate h
        # h = (GENERATOR ** i) % PRIME
        # #calculate s
        # s = (i + j * carID) % (PRIME - 1)
        # #calculate the first_proof and the second_proof
        # first = (GENERATOR ** s) % PRIME
        # second = (h * (y ** j)) % PRIME
        #check if both are equal
        blockchain[index - 1][4] = blockchain[index - 1][4] + 1
        blockchain[index - 1][5] = hash_block(blockchain[index-1])
        # print("mined hash", blockchain[index - 1][5])
    # if first == second:
    duration = time.time() - start
    print("mined hash ---", blockchain[index - 1][5])
    #return the [r,b] tuple and the time it took to mine the block
    return blockchain[index - 1][4], duration

'''
    Structure of the Blockchain list:
        0th index -- index
        1st index -- CarID
        2nd index -- Timestamp
        3rd index -- Previous block's hash
        4th index -- data corresponding to ZKP
        5th index -- Current block's hash
        6th index -- link to the navigational data for the autonomous cars
'''
#function to print the blockchain in a readable manner
def print_chain(blockchain, index):
    if index < len(blockchain):
        print("Index -- ",blockchain[index][0])
        print("CarID -- ", blockchain[index][1])
        print("Timestamp -- ", blockchain[index][2])
        print("Hash -- ", blockchain[index][5])
        print("Previous Hash -- ", blockchain[index][3])
        print()

#main function
def main():
    index = 1
    #initialize the blockchain
    blockchain = []
    #add the genesis block
    blockchain.append(genesis_block())
    #loop to continuosly verify, mine and add new blocks to the chain
    while True:
        #boolean function to verify if chain is valid
        print("Is chain valid -- ", verifyChain(blockchain))
        #random CarID generator to act as secret data stored on the chain
        carID = random.randint(1, 1000000000)
        #mine and get the time required to mine new blocks
        data, duration = mine(index, blockchain)
        print("Time to mine -- ", duration, " seconds", "hash", data)
        #add the new block to the chain
        blockchain.append(createBlock(index, carID,blockchain[len(blockchain) - 1][5],data))
        #print the new block
        print_chain(blockchain, index)
        index = index + 1

if __name__ == "__main__":
    main()
    
