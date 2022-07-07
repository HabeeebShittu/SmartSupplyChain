# Import Smart Contract (SC)
from brownie import SupplyChainV2
# Import module that enables processing of arrays
from array import *
# Import module that supplies classes for manipulating dates and times.
import datetime

#Declare global variable array of unsigned long values
productArray = array('L',[0,0,0,0])

# Begin MAIN function
def main():
  # ===========RFID SMART CONTRACT VARIABLES TO BE SEARCHED===========
  # Step 1:
  # Retrieve productID variables from RFID RC522
  RFID_INFO = open("rfid_info.txt", "r")
  productID = (RFID_INFO.readline())
  RFID_INFO.close()
  # ============SET KEY PARAMETERS FOR THIS PYTHON SCRIPT============
  # Step 2:
  # Create an object used to identify the latest deployment
  Contract = SupplyChainV2[len(SupplyChainV2) - 1]
  # =============RUN FUNCTION TO READ RFID VARIABLES=================
  # Step 3:
  # Return the searched product details as values for the productArray 
  productArray = Contract.readProduct(productID)
  # ================PERFORM VARIABLE CONVERSIONS=====================
  # Step 4:
  # Convert received createdAt & updatedAt timestamp to human readable date
  createdAt = datetime.datetime.fromtimestamp(productArray[2])
  updatedAt = datetime.datetime.fromtimestamp(productArray[3])
  # ================DISPLAY PRODUCT INFORMATION======================
  # Step 5:
  # Return Product Information on console if found on the blockchain
  print(f"Searched Product ID is: {productArray[0]}")
  print(f"Current Product Stage is: {productArray[1]}")
  print("Product Humidity is: 20%")
  print("Product Temperature is: 20°C")
  print(f"Product was created at: {createdAt}")
  print(f"Product Last update was at: {updatedAt}")