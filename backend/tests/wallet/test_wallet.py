from os import walk
from backend.config import STARTING_BALANCE
from backend.wallet.wallet import Wallet
from backend.blockchain.blockchain import Blockchain
from backend.wallet.transaction import Transaction
from backend.wallet.transaction_pool import TransactionPool
from backend.config import STARTING_BALANCE

def test_verify_valid_signature():
    data = {'foo' : 'test-data'}
    wallet = Wallet()
    signature = wallet.sign(data)
    assert Wallet.verify(wallet.public_key, data, signature)

def test_verify_invalid_signature():
    data = {'foo' : 'test-data'}
    data1 = {'foo' : 'test-data1'}
    wallet = Wallet()
    signature = wallet.sign(data)
    signature1 = wallet.sign(data1)
    assert not Wallet.verify(Wallet().public_key, data, signature)
    assert not Wallet.verify(wallet.public_key, data1, signature)
    assert not Wallet.verify(wallet.public_key, data, signature1)

def test_calculate_balance():
    blockchain = Blockchain()
    wallet = Wallet()
    assert Wallet.calculate_balance(blockchain, wallet) == STARTING_BALANCE
    amount = 50
    transaction = Transaction(wallet, 'recipient', amount)
    blockchain.add_block([transaction.to_json()])
    assert Wallet.calculate_balance(blockchain, wallet.address) == \
        STARTING_BALANCE - amount
    recieved_amount_1 = 25
    recieved_transaction_1 = Transaction(
        Wallet(),
        wallet.address,
        recieved_amount_1
    )
    recieved_amount_2 = 562
    recieved_transaction_2 = Transaction(
        Wallet(),
        wallet.address,
        recieved_amount_2
    )   
    blockchain.add_block([recieved_transaction_1.to_json(), recieved_transaction_2.to_json()])
    assert Wallet.calculate_balance(blockchain, wallet.address) == \
        STARTING_BALANCE - amount + recieved_amount_1 + recieved_amount_2