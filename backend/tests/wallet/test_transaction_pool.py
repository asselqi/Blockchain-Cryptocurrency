from backend.wallet.wallet import Wallet
from backend.wallet.transaction import Transaction
from backend.wallet.transaction_pool import TransactionPool
from backend.blockchain.blockchain import Blockchain

def test_set_transction():
    transaction_pool = TransactionPool()
    transaction = Transaction(Wallet(), 'recipient', 1)
    transaction_pool.set_transaction(transaction)
    assert transaction_pool.transaction_map[transaction.id] == transaction

def test_clear_blockchain_transactions():
    transaction_pool = TransactionPool()
    transaction_1 = Transaction(Wallet(), 'recipient', 1)
    transaction_2 = Transaction(Wallet(), 'recipient', 2)
    transaction_3 = Transaction(Wallet(), 'recipient', 3)
    transaction_4 = Transaction(Wallet(), 'recipient', 4)
    transaction_pool.set_transaction(transaction_1)
    transaction_pool.set_transaction(transaction_2)
    transaction_pool.set_transaction(transaction_3)
    transaction_pool.set_transaction(transaction_4)

    blockchain = Blockchain()
    blockchain.add_block([transaction_1.to_json(), transaction_2.to_json(), transaction_3.to_json(), transaction_4.to_json()])

    assert transaction_1.id in transaction_pool.transaction_map    
    assert transaction_2.id in transaction_pool.transaction_map    
    assert transaction_3.id in transaction_pool.transaction_map    
    assert transaction_4.id in transaction_pool.transaction_map
        
    transaction_pool.clear_blockchain_transactions(blockchain)

    assert not transaction_1.id in transaction_pool.transaction_map
    assert not transaction_2.id in transaction_pool.transaction_map
    assert not transaction_3.id in transaction_pool.transaction_map
    assert not transaction_4.id in transaction_pool.transaction_map
