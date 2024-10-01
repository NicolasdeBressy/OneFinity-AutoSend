import os
import time
from dotenv import load_dotenv
from web3 import Web3
import requests  # Importing the requests library to handle HTTP requests to the faucet API

# Load environment variables from the .env file
load_dotenv()

# Retrieve the necessary environment variables
WEB3_PROVIDER_URI = os.getenv("WEB3_PROVIDER_URI")  # The URI for connecting to the Ethereum network
CHECKSUM_ADDRESS = os.getenv("CHECKSUM_ADDRESS")  # Load the sender's Ethereum address from .env
PRIVATE_KEY = os.getenv("PRIVATE_KEY")  # Load the private key for signing transactions
AMOUNT = float(os.getenv("AMOUNT"))  # Amount of ONE tokens to send
RECEIVER_ADDRESS = os.getenv("RECEIVER_ADDRESS")  # Load the receiver's Ethereum address from .env

def get_faucet():
    """Function to request tokens from the faucet."""
    url = "https://testnet-api.onefinity.network/faucet"  # API endpoint for the faucet
    data = {
        'address': CHECKSUM_ADDRESS,  # Include the sender's address in the request data
        # You can add additional parameters if required by the faucet API
    }
    response = requests.post(url, json=data)  # Send a POST request to the faucet API
    if response.status_code == 200:  # Check if the request was successful
        print("Faucet successfully retrieved!")  # Confirmation message for successful retrieval
    else:
        # Print error message if the request failed
        print(f"Error retrieving faucet: {response.status_code} - {response.text}")

def send_transaction(w3, sender_address):
    """Function to send a transaction from the sender to the receiver."""
    # Get the current balance of the sender's address
    balance = w3.eth.get_balance(sender_address)  
    balance_in_one = w3.from_wei(balance, 'ether')  # Convert balance from Wei to ONE
    print(f"Current balance of the sender: {balance_in_one} $ONE")  # Display the balance

    # Check if the sender has enough funds to send the specified amount
    if balance_in_one < AMOUNT:
        print("Insufficient funds to make this transaction.")  # Alert for insufficient funds
        return  # Exit the function if funds are insufficient

    # Print the details of the transaction
    print(f"Sending {AMOUNT} $ONE from {sender_address} to {RECEIVER_ADDRESS}...")

    # Build the transaction details
    nonce = w3.eth.get_transaction_count(sender_address)  # Get the transaction count for the sender
    gas_price = w3.to_wei('1', 'gwei')  # Set the gas price (cost of processing the transaction)
    
    # Create a transaction dictionary containing all necessary details
    transaction = {
        'to': RECEIVER_ADDRESS,  # Set the recipient's address
        'value': w3.to_wei(AMOUNT, 'ether'),  # Convert the amount to Wei for the transaction
        'gas': 2000000,  # Specify the gas limit for the transaction
        'gasPrice': gas_price,  # Set the gas price for the transaction
        'nonce': nonce,  # Set the nonce for the transaction to prevent replay attacks
        'chainId': 999987  # Specify the chain ID for the OneFinity Testnet
    }

    # Attempt to sign the transaction
    try:
        signed_txn = w3.eth.account.sign_transaction(transaction, private_key=PRIVATE_KEY)  # Sign the transaction with the private key
        
        # Send the signed transaction to the network
        tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)  # Send the raw signed transaction
        print(f"Transaction sent! Transaction hash: {tx_hash.hex()}")  # Print the transaction hash for tracking
    except Exception as e:
        # Print any errors encountered during the transaction signing or sending process
        print(f"Error sending transaction: {e}")

def main():
    """Main function to control the flow of the script."""
    # Connect to the Ethereum network using Web3
    w3 = Web3(Web3.HTTPProvider(WEB3_PROVIDER_URI))

    # Check if the connection to Web3 was successful
    if not w3.is_connected():
        print("Failed to connect to Web3.")  # Alert if connection fails
        return  # Exit the main function if unable to connect

    # Display the sender's address after converting to checksum format
    sender_address = w3.to_checksum_address(CHECKSUM_ADDRESS)
    print(f"Sender's address: {sender_address}")

    last_faucet_time = 0  # Variable to track the last time tokens were retrieved from the faucet
    start_time = time.time()  # Variable to track the start time for sending transactions

    # Infinite loop to continuously send transactions and request from the faucet
    while True:
        current_time = time.time()  # Get the current time

        # Send the transaction every 10 seconds
        if current_time - start_time >= 10:
            send_transaction(w3, sender_address)  # Call the send_transaction function
            start_time = current_time  # Reset the start time for the next transaction

        # Retrieve tokens from the faucet every 5 minutes and 10 seconds
        if current_time - last_faucet_time >= 310:  # 5 minutes and 10 seconds
            get_faucet()  # Call the get_faucet function to request tokens
            last_faucet_time = current_time  # Reset the last faucet retrieval time

        time.sleep(1)  # Wait for a short duration to avoid a too fast loop

if __name__ == "__main__":
    main()  # Call the main function to start the script
