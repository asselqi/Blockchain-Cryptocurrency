class Block:
    """
    Block: a data storage unit.
    Store transactions in a blockchain that supports a cryptocurrency
    """
    def __init__(self, data):
        self.data = data

    def __repr__(self):
        return f'Block: data - {self.data}'