#=======================LIBRARY IMPORT DECLARATIONS===============
import os
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from brownie import accounts, SupplyChainV2

#====================GLOBAL VARIABLE DECLARATIONS#====================
# Declare and initiate a transaction stage variable
reader = SimpleMFRC522()

#=======================BEGIN SPI COMMUNICATION#=======================
try:
  # Read RFID tag
  print("Put RFID tag on sensor")
  id = reader.read()
  
  # Print the received productID to terminal
  productID = id
  print(productID)

  # Record Product ID
  RFID_FILE = open("rfid_info.txt", "w")
  productIDStr = repr(productID)
  RFID_FILE.write(productIDStr)
  RFID_FILE.close()

  # Declare key parameters
  account = accounts.add(os.getenv("PRIVATE_KEY"))
  Contract = SupplyChainV2[len(SupplyChainV2) - 1]

  # Push product to Blockchain
  writeResult = Contract.writeProduct(productID, {'from': account})

  # Record Transaction details
  LogFile = open("trans_log.txt", "a")
  transHashStr = repr(writeResult.txid)
  LogFile.write(transHashStr + "\n")
  LogFile.close()

  # Print the blockchain transaction hash to terminal
  print(f"Blockchain Transaction Hash: {writeResult.txid}")
# Reassign (empty) GPIO ports
finally:
  GPIO.cleanup()