import datetime
import hashlib
import json
import streamlit as st
import pandas as pd

# structuring the blockchain


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
                col1, col2 = st.columns(2)
                col1.metric("Hash of the added block is",str(hash_val[:12] + '...'))
                col2.metric("Nonce of the added block is", str(new_proof),str(new_proof - self.chain[-1]['proof']))
                check_proof = True
            else:
                new_proof += 1

        return new_proof

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

# creating the web app


def checklogin():
    file2 = open('loginstate.txt', 'r')

    if file2.read()[-1] == '1':
        file2.close()
        return True

    else:
        file2.close()
        return False


st.sidebar.image('Block-Estate2.png')
# st.sidebar.markdown("#### Contents:")
option = st.sidebar.selectbox(
    '',
    ('Home',
     'View Blockchain',
     'Health Check',
     'Admin Access',
     'Add Block'
     )
)

if option == 'Home':
    st.image('Banner.png')
    st.markdown("<h1 style = 'text-align: center'>Welcome</h1>",
                unsafe_allow_html=True)
    # st.markdown('### WELCOME')
    st.markdown('Land & property can be identified as one of the core assets in any county in the world.\
        Governments spend significant amount of money to identify, define, manage and maintain the \
        transactional information around land and property in a country. Creating a proper \
        mechanism to make this information available to the public users can be considered\
        as one of the key indications that shows the development of a country.\
        We at **PLOT-CHAIN** provide banks, businesses, and governments **BLOCKCHAIN SOLUTIONS** to _track and investigate and manage Real-Estate_.')
if option == 'View Blockchain':
    st.image('Banner.png')
    # st.title('View the Blockchain')
    st.markdown("<h1 style = 'text-align: center'>View the Blockchain</h1>",
                unsafe_allow_html=True)
    blockchain = Blockchain()
    blockchain.display()
    df = pd.read_csv('database.csv')
    df.rename(columns={"owner": "Owner", "land_reg_no": "Land Registration Number", "index": "Index",
              "timestamp": "Timestamp", "previous_hash": "Previous Hash", "proof": "Proof", "dummy": "Dummy"}, inplace=True)
    df = df[["Index", "Owner", "Land Registration Number",
             "Timestamp",  "Previous Hash", "Proof", "Dummy"]]
    df = df.iloc[:, 1:-1]  # to hide dummy
    st.table(data=df)
    # st.dataframe(data=df)

if option == 'Admin Access':
    st.image('admin.png')
    # st.title('ADMINSTRATION ACCESS')
    # st.markdown("<h1 style = 'text-align: center'>ADMINSTRATION ACCESS</h1>",
    # unsafe_allow_html=True)
    # st.image('emblem.png')
    st.caption(
        'Only Authorized employees of The Government Of The United States Of America')

    if checklogin():
        if st.button('Log Out'):
            file2 = open('loginstate.txt', 'a')
            file2.write('0')
            st.success('Logged Out')
            file2.close()
    else:
        with st.form("my_form2"):
            upass = st.text_input('Enter Password', type='password')
            submitted = st.form_submit_button("Submit")
            if submitted:
                if upass == 'karan':
                    file2 = open('loginstate.txt', 'a')
                    file2.write('1')
                    st.success('Logged In')
                    file2.close()
                elif upass != 'karan':
                    st.error('⚠ Password Incorrect!')
#         upass = st.text_input('Enter Password', type='password')
#         if upass == 'karan':
#             file2 = open('loginstate.txt', 'a')
#             file2.write('1')
#             st.success('Logged In')
#             file2.close()
#         # else:
#         #     st.error('⚠ Password Incorrect!')
#         elif upass != 'karan':
#             st.error('⚠ Password Incorrect!')


if option == 'Add Block':
    st.image('Banner.png')
    st.title('ADD A NEW BLOCK')
    if checklogin():
        blockchain = Blockchain()
        previous_block = blockchain.get_last_block()
        print(previous_block)
        file = open('database.csv', 'a')
        with st.form("my_form"):
            st.markdown("### Enter Details Of The User")
            st_0 = str(st.text_input('Enter Owner Name:'))
            st_1 = str(st.text_input('Enter Registration Number:'))
            submitted = st.form_submit_button("Submit")
            if submitted:
                file = open('database.csv', 'a')
                st_2 = str(len(blockchain.chain))
                st_3 = str(datetime.datetime.now())
                st_4 = str(blockchain.hash(previous_block))
                st_5 = str(blockchain.proof_of_work(
                    st_0, st_1, st_2, st_3, st_4, 'dummy\n'))
                st_6 = 'dummy'

                new_str = st_0 + ',' + st_1 + ',' + st_2 + \
                    ',' + st_3 + ','+st_4 + ',' + st_5 + ',' + st_6 + '\n'

                # with st.spinner(text='MINING THR BLOCK'):
                file.write(new_str)
                st.success('BLOCK ADDED')
                file.close()
    else:
        st.error('⚠ Log In First Please')

if option == 'Health Check':
    st.image('Banner.png')
    st.title('Check Blockchain Health Status')
    blockchain = Blockchain()
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        st.success("Blockchain is currently Healthy")
    else:
        st.error("Data Corruption Detected")
