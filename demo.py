#=======================LIBRARY IMPORT DECLARATIONS===============
import os
import json
import datetime
from array import *
import RPi.GPIO as GPIO
from dotenv import load_dotenv
from mfrc522 import SimpleMFRC522
from web3 import Web3, HTTPProvider

load_dotenv()

#====================GLOBAL VARIABLE DECLARATIONS#====================
# Declare and initiate a transaction stage variable
reader = SimpleMFRC522()

# Declare and connect to Kovan Infura Network with Web3
privateKey = os.getenv('PRIVATE_KEY')
infuraID = os.getenv('WEB3_INFURA_PROJECT_ID')
kovanUri = f"https://kovan.infura.io/v3/{infuraID}"
w3 = Web3(Web3.HTTPProvider(kovanUri))

# Declare and attach connected account to Web3 using PRIVATE_KEY
account = w3.eth.account.from_key(privateKey)
w3.eth.defaultAccount = account.address

# Declare contract abi and fetch active contract address
contractAbi = json.loads('[{"anonymous": false,"inputs":[{"indexed": true,"name": "uId","type": "uint256"},{"indexed": false,"name": "stage","type": "uint256"},{"indexed": false, "name": "humidity","type": "string"},{"indexed": false,"name": "temperature","type": "string"},{"indexed": false,"name": "createdAt","type": "uint256"},{"indexed": false,"name": "updatedAt","type": "uint256"}],"name": "ProductEvent","type": "event"},{"inputs": [{"name": "_uId","type": "uint256"}],"name": "writeProduct","outputs": [{"name": "status","type": "bool"}],"stateMutability": "nonpayable","type": "function"},{"inputs": [{"name": "_uId","type": "uint256"}],"name": "readProduct","outputs": [{"name": "uId","type": "uint256"},{"name": "stage","type": "uint256"},{"name": "createdAt","type": "uint256"},{"name": "updatedAt","type": "uint256"}],"stateMutability": "view","type": "function"}]')
ContractInfo = open("contract_info.txt", "r")
contractAddress = (ContractInfo.readline())
ContractInfo.close()

# Decalre and initiate SmartSupplyChain contract instance
Contract = w3.eth.contract(address=contractAddress, abi=contractAbi)

#=======================BEGIN SPI COMMUNICATION#=======================
try:
  # Read RFID tag
  print("Put RFID tag on sensor")
  id, text = reader.read()
  
  # Print the received productID to terminal
  productID = id
  print(f"Scanned Product ID is: {productID}")

  # Record Product ID
  RFID_FILE = open("rfid_info.txt", "w")
  productIDStr = repr(productID)
  RFID_FILE.write(productIDStr)
  RFID_FILE.close()

  # Declare key product transaction parameters
  txObject = Contract.functions.writeProduct(productID).buildTransaction({
    'from': account.address,
    'nonce': w3.eth.get_transaction_count(account.address)
  })

  # Push scanned product to Blockchain
  signedTx = account.signTransaction(txObject)
  tx_hash = w3.eth.sendRawTransaction(signedTx.rawTransaction)
  w3.eth.waitForTransactionReceipt(tx_hash)

  # Record Transaction details
  LogFile = open("trans_log.txt", "a")
  transHashStr = repr(tx_hash)
  print(f"Blockchain Transaction Hash: {transHashStr}")
  LogFile.write(transHashStr + "\n")
  LogFile.close()

  # Print the scanned product details to terminal
  productArray = array('L',[0,0,0,0])
  productArray = Contract.functions.readProduct(productID).call()
  createdAt = datetime.datetime.fromtimestamp(productArray[2])
  updatedAt = datetime.datetime.fromtimestamp(productArray[3])

  print(f"Processed Product ID is: {productArray[0]}")
  print(f"Current Product Stage is: {productArray[1]}")
  print("Product Humidity is: 20%")
  print("Product Temperature is: 20°C")
  print(f"Product was created at: {createdAt}")
  print(f"Product Last update was at: {updatedAt}")
# Reassign (empty) GPIO ports
finally:
  GPIO.cleanup()