# Import accounts and Smart Contract object
from brownie import accounts, SupplyChainV2
# Import module that supplies classes for manipulating environment variables
import os

# Begin MAIN function
def main():
  # Declare a string that retrives the .env PRIVATE KEY
  privateKey = os.getenv("PRIVATE_KEY")
  # Declare an object that stores the Kovan account from the privateKey
  account = accounts.add(privateKey)
  # Run .deploy METHOD to deploy the smart contract using the account
  deployResult = SupplyChainV2.deploy({'from': account})
  # Record Contract Address for the scanner script (demo.py)
  ContractInfo = open("contract_info.txt", "w")
  ContractInfo.write(deployResult.address)
  ContractInfo.close()