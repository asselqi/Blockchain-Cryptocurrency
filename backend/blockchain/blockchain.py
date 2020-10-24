from backend.blockchain.block import Block


class Blockchain:
    """
    Blovkchain: a public ledger of transaction.
    Implemented as a list of blocks - data sets of transactions
    """
    def __init__(self):
        self.chain = [Block.genesis()]

    def add_block(self, data):
        self.chain.append(Block.mine_block(self.chain[-1], data))

    def __repr__(self):
        return f'Blockchain: {self.chain}'

blockchain = Blockchain()
blockchain.add_block('one')
blockchain.add_block('two')
print(blockchain)