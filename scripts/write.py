# Import config, accounts and Smart Contract object
from brownie import config, accounts, SupplyChainV2

# Begin MAIN function
def main():
  # ========RFID SMART CONTRACT VARIABLES TO BE ADDED/UPDATED========
  # Step 1:
  # Retrieve productID variables from RFID RC522
  RFID_INFO = open("rfid_info.txt", "r")
  productID = (RFID_INFO.readline())
  RFID_INFO.close()
  # ============SET KEY PARAMETERS FOR THIS PYTHON SCRIPT============
  # Step 2:
  # Get PRIVATE KEY of the account to be charged Transaction Gas Fees for “writing” into Smart Contract
  privateKey = config["wallets"]["from_key"]
  account = accounts.add(privateKey)
  # Step 3:
  # Create an object used to identify the latest deployment
  Contract = SupplyChainV2[len(SupplyChainV2) - 1]
  # ===RUN FUNCTION TO ADD/UPDATE PRODUCT BASED ON THE RFID VARIABLES===
  # Step 4:
  writeResult = Contract.writeProduct(productID, {'from': account})
  # =====================RECORD TRANSACTION DETAILS=====================
  # Step 5
  # Add the transaction hash to the log file
  # Open the log file
  LogFile = open("trans_log.txt", "a")
  # Convert values to string type
  transHashStr = repr(writeResult.txid)
  #  Write with elimination 
  LogFile.write(transHashStr + "\n")
  # Close the log file
  LogFile.close()
   # ======================DISPLAY TRANSACTION HASH======================
  # Step 6:
  # Return transaction hash on console
  print(f"Blockchain Transaction Hash: {writeResult.txid}")