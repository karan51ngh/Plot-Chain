import json
import hashlib


class Blockchain:
    def __init__(self):
        file = open('database.csv', 'r')
        self.chain = []
        for each in file:
            ls = each.split(",")
            if ls[1] == 'land_reg_no':
                continue
            # print(ls)
            block = {'owner': ls[0],
                     'land_reg_no': ls[1],
                     'index': ls[2],
                     'timestamp': ls[3],
                     'previous_hash': ls[4],
                     'proof': ls[5],
                     'dummy': ls[6]
                     }
            self.chain.append(block)

    def display(self):
        for i in self.chain:
            print(i)

    def proof_of_work(self, owner, land_reg_no, index, timestamp, previous_hash, dummy):

        new_proof = 1
        block = {'owner': str(owner),
                 'land_reg_no': str(land_reg_no),
                 'index': str(index),
                 'timestamp': str(timestamp),
                 'previous_hash': str(previous_hash),
                 'proof': str(new_proof),
                 'dummy': dummy
                 }

        print(f'type of block is {type(block)}')
        check_proof = False

        while check_proof is False:
            block['proof'] = str(new_proof)
            print(block)
            encoded_block = json.dumps(block).encode()
            hash_val = hashlib.sha256(encoded_block).hexdigest()
            if hash_val[:4] == '0000':
                print(f'the hash is {hash_val}')
                check_proof = True
            else:
                new_proof += 1

        return new_proof, hash_val

    def hash(self, block):
        # json.dumps makes all the block values into strings
        encoded_block = json.dumps(block).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_idx = 1

        while block_idx < len(chain):
            block = chain[block_idx]

            if block['previous_hash'] != self.hash(previous_block):
                print(f'Hash not same, index of current block is {block_idx}')
                return False

            hash_val = self.hash(block)

            if hash_val[:4] != '0000':
                print(
                    f'Hash doesnt start with 0000, index of current block is {block_idx}')
                return False

            previous_block = block
            block_idx += 1

        return True

    def get_last_block(self):
        return self.chain[-1]
