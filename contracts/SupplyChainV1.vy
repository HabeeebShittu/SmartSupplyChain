# @version ^0.3.3

# Contract SupplyChainV1

#Storage Variables
# Main storage array
ids: public(uint256[3])


# Functions
# Write (update) function updateStage. 
# Inputs: new UID, new Stage from RFID Tag
# Output: Boolean True
# Internal calls: timestamp to record the time of update
@external #is made external to be visible / editible
def updateStage(new_product_ID: uint256, new_Stage: uint256) -> bool:
    self.ids[0]= new_product_ID
    self.ids[1] = new_Stage
    self.ids[2] = block.timestamp
    return True

# Read (get) function readStage. 
# Inputs: none
# Output: array of three uint256 variables: UID, Stage, Time
@external #is made external to be visible / editible
@view
def readStage() -> uint256[3]:
    return self.ids