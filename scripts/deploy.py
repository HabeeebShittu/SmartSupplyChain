# Import config, accounts and Smart Contract object
from brownie import config, accounts, SupplyChainV2

# Begin MAIN function
def main():
  # Declare a string that retrives the .env PRIVATE KEY
  privateKey = config["wallets"]["from_key"]
  # Declare an object that stores the Kovan account from the privateKey
  account = accounts.add(privateKey)
  # Run .deploy METHOD to deploy the smart contract using the account
  deployResult = SupplyChainV2.deploy({'from': account})
  # Record Contract Address for the scanner script (demo.py)
  ContractInfo = open("contract_info.txt", "w")
  ContractInfo.write(deployResult.address)
  ContractInfo.close()