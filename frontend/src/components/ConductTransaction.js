import React, {useState} from 'react';
import {FormGroup, FormControl, Button} from 'react-bootstrap';
import {API_BASE_URL} from '../config';

function ConductTransaction() {
    const [amount, setAmount] = useState(0);
    const [recipient, setRecipient] = useState('');


    const updateRecipient = event => {
        setRecipient(event.target.value);
    }

    const updateAmount = event => {
        setAmount(event.target.value);
    }

    const submitTransaction = () => {
        fetch(`${API_BASE_URL}/wallet/transact`, 
        {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({recipient, amount})
        })
        .then(response => response.json())
        .then(json => {
            console.log('submitTransaction json', json);
            alert('Success!');
        });
    }

    return (
        <div className="ConductTransaction">
            <h3>Conduct a Transaction</h3>
            <br />
            <FormGroup>
                <FormControl 
                    input="text"
                    placeholder="recipient"
                    value={recipient}
                    onChange={updateRecipient}
                />
            </FormGroup>
            <FormGroup>
                <FormControl 
                    input="number"
                    placeholder="amount"
                    value={amount}
                    onChange={updateAmount}
                />
            </FormGroup>
            <div>
                <Button
                    variant="danger"
                    onClick={submitTransaction}
                >
                    Submit
                </Button>
            </div>
        </div>
    )

}

export default ConductTransaction;