from backend.blockchain.block import GENESIS_DATA
from backend.blockchain.blockchain import Blockchain

def test_blockchain_instance():
    blockchain = Blockchain()

    assert blockchain.chain[0].hash == GENESIS_DATA['hash']

def test_add_block():
    blockchain = Blockchain()
    data = 'test-data'
    blockchain.add_block(data)

    assert blockchain.chain[-1].last_hash == GENESIS_DATA['hash']
    assert blockchain.chain[-1].data == data
