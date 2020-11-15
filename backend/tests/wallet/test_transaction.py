import pytest

from backend.wallet.transaction import Transaction
from backend.wallet.wallet import Wallet
from backend.config import MINING_REWARD, MINING_REWARD_INPUT, STARTING_BALANCE


def test_transaction():
    sender_wallet = Wallet()
    recipient = 'recipient'
    amount = 50 
    transaction = Transaction(sender_wallet, recipient, amount)
    assert transaction.output[recipient] == amount
    assert transaction.output[sender_wallet.address] == \
        sender_wallet.balance - amount
    assert 'timestamp' in transaction.input
    assert transaction.input['amount'] == sender_wallet.balance
    assert transaction.input['address'] == sender_wallet.address
    assert transaction.input['public_key'] == sender_wallet.public_key
    assert sender_wallet.verify(
        transaction.input['public_key'],
        transaction.output,
        transaction.input['signature']
    )

def test_transaction_exceeds():
    with pytest.raises(Exception, match = 'Amount exceeds balance'):
        Transaction(Wallet(), 'recipient', 1500)

def test_transaction_update_exceeds_balance():
    sender_wallet = Wallet()
    transaction = Transaction(sender_wallet, 'recipient', 50)
    with pytest.raises(Exception, match = 'Amount exceeds balance'):
        transaction.update(sender_wallet, 'new-recipient', 1500)

def test_transaction_update():
    sender_wallet = Wallet()
    first_recipient = 'first-recipient'
    first_amount = 50
    transaction = Transaction(sender_wallet, first_recipient, first_amount)
    next_recipient = 'next-recipient'
    next_amount = 75
    transaction.update(sender_wallet, next_recipient, next_amount)
    assert transaction.output[next_recipient] == next_amount
    assert transaction.output[sender_wallet.address] == \
        sender_wallet.balance - first_amount - next_amount
    assert sender_wallet.verify(
        transaction.input['public_key'],
        transaction.output,
        transaction.input['signature']
    )
    transaction.update(sender_wallet, first_recipient, first_amount)
    assert transaction.output[first_recipient] == first_amount * 2
    assert transaction.output[sender_wallet.address] == \
        sender_wallet.balance - first_amount - next_amount - first_amount
    assert sender_wallet.verify(
        transaction.input['public_key'],
        transaction.output,
        transaction.input['signature']
    )

def test_is_valid_transaction():
    Transaction.is_valid_transaction(Transaction(Wallet(), 'recipient', 50))

def test_valid_transaction_with_invalid_outputs():
    sender_wallet = Wallet()
    transaction = Transaction(sender_wallet, 'recipient', 50)
    transaction.output[sender_wallet.address] = 9001
    with pytest.raises(Exception, match='Invalid transaction output values'):
        Transaction.is_valid_transaction(transaction)

def test_valid_transaction_with_invalid_signature():
    sender_wallet = Wallet()
    transaction = Transaction(sender_wallet, 'recipient', 50)
    transaction.input['signature'] = Wallet().sign(transaction.output)
    with pytest.raises(Exception, match='Invalid signature'):
        Transaction.is_valid_transaction(transaction)

def test_reward_transaction():
    miner_wallet = Wallet()
    transaction = Transaction.reward_transaction(miner_wallet)
    assert transaction.input == MINING_REWARD_INPUT
    assert transaction.output[miner_wallet.address] == MINING_REWARD

def test_valid_reward_transaction():
    reward_transaction = Transaction.reward_transaction(Wallet())
    Transaction.is_valid_transaction(reward_transaction)

def test_invalid_reward_transaction_extra_recipient():
    reward_transaction = Transaction.reward_transaction(Wallet())
    reward_transaction.output['extra_recipient'] = 500
    with pytest.raises(Exception, match = 'Invalid mining reward'):
        Transaction.is_valid_transaction(reward_transaction)
    
def test_invalid_reward_transaction_invalid_amount():
    miner_wallet = Wallet()
    reward_transaction = Transaction.reward_transaction(miner_wallet)
    reward_transaction.output[miner_wallet.address] = 23451
    with pytest.raises(Exception, match = 'Invalid mining reward'):
        Transaction.is_valid_transaction(reward_transaction)