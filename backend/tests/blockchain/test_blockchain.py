import pytest

from backend.blockchain.block import GENESIS_DATA
from backend.blockchain.blockchain import Blockchain
from backend.blockchain.block import Block
from backend.wallet.wallet import Wallet
from backend.wallet.transaction import Transaction

def test_blockchain_instance():
    blockchain = Blockchain()

    assert blockchain.chain[0].hash == GENESIS_DATA['hash']

def test_add_block():
    blockchain = Blockchain()
    data = 'test-data'
    blockchain.add_block(data)

    assert blockchain.chain[-1].last_hash == GENESIS_DATA['hash']
    assert blockchain.chain[-1].data == data

@pytest.fixture
def blockchain_ten_blocks():
    blockchain = Blockchain()
    for i in range(10):
        blockchain.add_block([Transaction(Wallet(), 'recipient', i).to_json()])
    return blockchain    

def test_is_valid_chain(blockchain_ten_blocks):
    blockchain_ten_blocks.is_valid_chain(blockchain_ten_blocks.chain)

def test_is_valid_chain_bad_genesis(blockchain_ten_blocks):
    blockchain_ten_blocks.chain[0] = Block.mine_block(blockchain_ten_blocks.chain[-1], 'testing-data')
    with pytest.raises(Exception, match = 'The genesis block must be valid'):
        blockchain_ten_blocks.is_valid_chain(blockchain_ten_blocks.chain)

def test_replace_chain(blockchain_ten_blocks):
    blockchain = Blockchain()
    blockchain.replace_chain(blockchain_ten_blocks.chain)
    assert blockchain.chain == blockchain_ten_blocks.chain

def test_replace_chain_bad_length(blockchain_ten_blocks):
    blockchain1 = Blockchain()
    for i in range(10):
        blockchain1.add_block(i)
    blockchain2 = Blockchain()
    with pytest.raises(Exception, match = 'Cannot replace. The incoming chain must be longer.'):
        blockchain1.replace_chain(blockchain_ten_blocks.chain)
    with pytest.raises(Exception, match = 'Cannot replace. The incoming chain must be longer.'):
        blockchain_ten_blocks.replace_chain(blockchain1.chain)
    with pytest.raises(Exception, match = 'Cannot replace. The incoming chain must be longer.'):
        blockchain_ten_blocks.replace_chain(blockchain2.chain)

def test_replace_chain_invalid(blockchain_ten_blocks):
    blockchain_five_blocks = Blockchain()
    for i in range(5):
        blockchain_five_blocks.add_block(i)
    blockchain_ten_blocks.chain[3].data = 'test-data'
    blockchain = Blockchain()
    blockchain1 = Blockchain()
    try:
        blockchain.replace_chain(blockchain_ten_blocks.chain)
    except Exception as e:
        assert str(e) == 'Cannot replace. The incoming chain is invalid: The block hash is not valid'          
    try:
        blockchain1.replace_chain(blockchain_five_blocks.chain)
    except Exception as e:
        assert str(e) == 'Cannot replace. The incoming chain is invalid: The genesis block must be valid'

def test_valid_transaction_chain(blockchain_ten_blocks):
    Blockchain.is_valid_transaction_chain(blockchain_ten_blocks.chain)

def test_is_valid_transaction_chain_duplicate_transactions(blockchain_ten_blocks):
    transaction = Transaction(Wallet(), 'recipient', 1).to_json()
    blockchain_ten_blocks.add_block([transaction, transaction])
    with pytest.raises(Exception, match = 'is not unique'):
        Blockchain.is_valid_transaction_chain(blockchain_ten_blocks.chain)

def test_is_valid_transaction_chain_multiple_rewards(blockchain_ten_blocks):
    reward_1 = Transaction.reward_transaction(Wallet())
    reward_2 = Transaction.reward_transaction(Wallet())
    blockchain_ten_blocks.add_block([reward_1.to_json(), reward_2.to_json()])
    with pytest.raises(Exception, match='one mining reward per block'):
        Blockchain.is_valid_transaction_chain(blockchain_ten_blocks.chain)

def test_is_valid_transaction_chain_bad_transaction(blockchain_ten_blocks):
    bad_transaction = Transaction(Wallet(), 'recipent', 1)
    bad_transaction.input['signature'] = Wallet().sign(bad_transaction.output)
    blockchain_ten_blocks.add_block([bad_transaction.to_json()])
    with pytest.raises(Exception):
        Blockchain.is_valid_transaction_chain(blockchain_ten_blocks.chain)

def test_is_valid_transaction_chain_bad_historic_balance(blockchain_ten_blocks):
    wallet = Wallet()
    bad_transaction = Transaction(wallet, 'recipient', 1)
    bad_transaction.output[wallet.address] = 9000
    bad_transaction.input['amount'] = 9001
    bad_transaction.input['signature'] = wallet.sign(bad_transaction.output)
    blockchain_ten_blocks.add_block([bad_transaction.to_json()])
    with pytest.raises(Exception, match = 'has an invalid input amount'):
        Blockchain.is_valid_transaction_chain(blockchain_ten_blocks.chain)