import pytest

from backend.blockchain.block import GENESIS_DATA
from backend.blockchain.blockchain import Blockchain
from backend.blockchain.block import Block

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
        blockchain.add_block(i)
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