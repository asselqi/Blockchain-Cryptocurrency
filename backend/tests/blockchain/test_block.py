import pytest
import time

from backend.blockchain.block import Block, GENESIS_DATA
from backend.config import MINE_RATE, SECONDS
from backend.util.hex_to_binary import hex_to_binary

def test_mine_block():
    last_block = Block.genesis()
    data = 'test-data'
    block = Block.mine_block(last_block, data)

    assert isinstance(block, Block)
    assert block.data == data
    assert block.last_hash == last_block.hash
    assert hex_to_binary(block.hash)[0:block.difficulty] == '0' * block.difficulty

def test_genesis():
    genesis = Block.genesis()

    assert isinstance(genesis, Block)
    for key, value in GENESIS_DATA.items():
        getattr(genesis, key) == value

def test_quickly_mined_block():
    last_block = Block.mine_block(Block.genesis(), 'foo')
    mined_block = Block.mine_block(last_block, 'bar')

    assert mined_block.difficulty == last_block.difficulty + 1

def test_slowly_mined_block():
    last_block = Block.mine_block(Block.genesis(), 'foo')
    time.sleep(MINE_RATE / SECONDS) #time.sleep(/*param*/) recieves seconds as a parameter, our MINE_RATE is in NANOSECONDS
    mined_block = Block.mine_block(last_block, 'bar')

    assert mined_block.difficulty == last_block.difficulty - 1

def test_mined_block_difficulty_limit(): 
    last_block = Block.mine_block(Block.genesis(), 'foo')
    last_block.difficulty = 1
    time.sleep(MINE_RATE / SECONDS)
    mined_block = Block.mine_block(last_block, 'bar')

    assert mined_block.difficulty == 1

def test_is_valid_block():
    last_block = Block.genesis()
    block = Block.mine_block(last_block, 'foo')
    Block.is_valid_block(last_block, block)

def test_is_valid_block_last_hash_err():
    last_block = Block.genesis()
    block = Block.mine_block(last_block, 'foo')
    block.last_hash = 'new evil hash'
    with pytest.raises(Exception, match = 'The block last_hash must be correct'):
        Block.is_valid_block(last_block, block)

def test_is_valid_block_proof_of_work():
    last_block = Block.genesis()
    block = Block.mine_block(last_block, 'foo')
    block.hash = 'fffffff'
    with pytest.raises(Exception, match = 'The proof of work requirement was not met'):
        Block.is_valid_block(last_block, block)

def test_is_valid_block_difficulty_adjustment():
    last_block = Block.genesis()
    block = Block.mine_block(last_block, 'foo')
    block.difficulty = 1
    with pytest.raises(Exception, match = 'The block difficulty must only adjust by 1'):
        Block.is_valid_block(last_block, block)

def test_is_valid_block_hash():
    last_block = Block.genesis()
    block = Block.mine_block(last_block, 'foo')
    block.hash = '00000000000000000000000000000000cabd'
    with pytest.raises(Exception, match = 'The block hash is not valid'):
        Block.is_valid_block(last_block, block)