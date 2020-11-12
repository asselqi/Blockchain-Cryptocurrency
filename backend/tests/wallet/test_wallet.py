from backend.wallet.wallet import Wallet

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
