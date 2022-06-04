from blockchain import Blockchain
from helperFunctions import checklogin, login, logout
import datetime
import streamlit as st
import pandas as pd

# creating the web app

st.set_page_config(
    page_title="plotchain.io",
    page_icon="pics/icon.png",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': None
    }
)
st.image('pics/Banner.png')
st.sidebar.image('pics/Block-Estate.png')
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
    st.caption(
        'Only Authorized employees of The Government Of The United States Of America')

    if checklogin():
        if st.button('Log Out'):
            logout()
            st.success('Logged Out')
    else:
        with st.form("my_form2"):
            upass = st.text_input('Enter Password', type='password')
            submitted = st.form_submit_button("Submit")
            if submitted:
                if upass == 'karan':
                    login()
                    st.success('Logged In')
                elif upass != 'karan':
                    st.error('⚠ Password Incorrect!')

if option == 'Add Block':
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
                new_proof, hash_val = blockchain.proof_of_work(
                    st_0, st_1, st_2, st_3, st_4, 'dummy\n')
                st_5 = str(new_proof)
                st_6 = 'dummy'

                new_str = st_0 + ',' + st_1 + ',' + st_2 + \
                    ',' + st_3 + ','+st_4 + ',' + st_5 + ',' + st_6 + '\n'

                col1, col2 = st.columns(2)
                col1.metric("Hash of the added block is",
                            str(hash_val[:8] + '...' + hash_val[-4:]))
                col2.metric("Nonce of the added block is", str(new_proof), str(
                    int(new_proof) - int(blockchain.chain[-1]['proof'])))

                file.write(new_str)
                st.success('BLOCK ADDED')
                file.close()

    else:
        st.error('⚠ Log In First Please')

if option == 'Health Check':
    st.title('Check Blockchain Health Status')
    blockchain = Blockchain()
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        st.success("Blockchain is currently Healthy")
    else:
        st.error("Data Corruption Detected")
