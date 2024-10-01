# OneFinity AutoSend

**OneFinity AutoSend** is a Python script that automates the process of sending cryptocurrency on the OneFinity Testnet. It interacts with the OneFinity faucet to replenish the sender's balance and periodically sends a specified amount of cryptocurrency to a designated recipient address.

## Features

- Automatically retrieves tokens from the OneFinity faucet.
- Sends a specified amount of cryptocurrency to a receiver address.
- Configurable parameters via a `.env` file to ensure sensitive information is kept secure.
- Easy to set up and run with minimal configuration.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- **Python 3.x** installed on your machine.
- Basic knowledge of Python programming.
- Access to the OneFinity Testnet.
- A valid **Web3** provider URI.
- Create an account on OneFinity and obtain an address to use.

## Installation

1. **Clone the repository** to your local machine:

   ```bash
   git clone https://github.com/yourusername/OneFinity-AutoSend.git
   cd OneFinity-AutoSend
   ```

2. **Set up a virtual environment** (optional but recommended):

   ```bash
   python -m venv mon_environnement
   source mon_environnement/bin/activate  # On Windows use `mon_environnement\Scripts\activate`
   ```

3. **Install the required packages**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Create a `.env` file** in the root directory of your project with the following content:

   ```env
   WEB3_PROVIDER_URI=https://testnet-rpc.onefinity.network
   CHECKSUM_ADDRESS=0xYOUR_ADDRESS_HERE  # Replace with your address
   PRIVATE_KEY=YOUR_PRIVATE_KEY_HERE  # Replace with your private key
   AMOUNT=0.15  # Amount to send
   RECEIVER_ADDRESS=0xRECEIVER_ADDRESS_HERE  # Replace with the receiver's address
   ```

## Usage

1. **Run the script** using Python:

   ```bash
   python auto_send.py
   ```

2. **Stopping the script**:

   - To stop the script, you can use `CTRL + C` in your terminal.

3. The script will:
   - Check your current balance.
   - Retrieve tokens from the faucet every 5 minutes and 10 seconds.
   - Send the specified amount to the receiver every 10 seconds.

## Code Explanation

### Main Components

- **Environment Variables**: All sensitive information is stored in the `.env` file, which is loaded at runtime using the `dotenv` library.
- **Faucet Functionality**: The script interacts with the OneFinity faucet to automatically replenish your balance.
- **Transaction Logic**: It checks if there are sufficient funds and sends transactions accordingly.

### Important Functions

- `get_faucet()`: Requests tokens from the OneFinity faucet.
- `send_transaction(w3, sender_address)`: Sends a specified amount of cryptocurrency to the receiver address.
- `main()`: Connects to the Web3 provider and manages the execution flow.

## Contributing

Contributions are welcome! If you have suggestions for improvements or bug fixes, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgements

- [Web3.py](https://web3py.readthedocs.io/en/stable/) for interacting with Ethereum blockchain.
- [Python Dotenv](https://pypi.org/project/python-dotenv/) for loading environment variables from `.env` files.
