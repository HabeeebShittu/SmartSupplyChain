# @version ^0.3.3

# Contract SupplyChainV2

# Storage variables
struct Product:
  uId: uint256
  stage: uint256
  humidity: String[100]
  temperature: String[100]
  createdAt: uint256
  updatedAt: uint256
  exists: bool

# Main storage array
products: HashMap[uint256, Product]

# Product info broadcaster
event ProductEvent:
  uId: indexed(uint256)
  stage: uint256
  humidity: String[100]
  temperature: String[100]
  createdAt: uint256
  updatedAt: uint256

# Constant variables
STAGE: constant(uint256) = 0
HUMIDITY: constant(String[100]) = "20%"
TEMPERATURE: constant(String[100]) = "20°C"

# Create (POST) function addProduct. 
# Inputs: UID from RFID Tag
# Log: object of six mixed variables: uId, stage, humidity, temperature, createdAt, & updatedAt
# Internal calls: timestamp to record the time of creation
@internal #is made internal to be hidden and accessible only by the contract
def addProduct(_uId: uint256):
  newProduct: Product = Product({
    uId: _uId,
    stage: STAGE,
    humidity: HUMIDITY,
    temperature: TEMPERATURE,
    createdAt: block.timestamp,
    updatedAt: block.timestamp,
    exists: True
  })
  self.products[_uId] = newProduct

  log ProductEvent(
    newProduct.uId,
    newProduct.stage,
    newProduct.humidity,
    newProduct.temperature,
    newProduct.createdAt,
    newProduct.updatedAt
  )

# Update (PUT) function updateProduct. 
# Inputs: UID from RFID Tag
# Log: object of six mixed variables: uId, stage, humidity, temperature, createdAt, & updatedAt
# Internal calls: timestamp to record the time of update
@internal #is made internal to be hidden and accessible only by the contract
def updateProduct(_uId: uint256):
  assert self.products[_uId].stage < 6, "Product fully delivered"
  
  self.products[_uId].stage += 1
  self.products[_uId].updatedAt = block.timestamp
  product: Product = self.products[_uId]

  log ProductEvent(
    product.uId,
    product.stage,
    product.humidity,
    product.temperature,
    product.createdAt,
    product.updatedAt
  )

# Write (POST/PUT) function writeProduct. 
# Inputs: UID from RFID Tag
# Output: Boolean True
# Internal calls: Creates new Product if not found or updates created product if found
@external #is made external to be visible / editible
def writeProduct(_uId: uint256) -> bool:
  if self.products[_uId].exists:
    self.updateProduct(_uId)
  else:
    self.addProduct(_uId)

  return True

# Read (GET) function readProduct. 
# Inputs: UID from RFID Tag
# Output: object of four uint256 variables: uId, stage, createdAt, & updatedAt
@external #is made external to be visible / editible
@view
def readProduct(_uId: uint256) -> (uint256, uint256, uint256, uint256):
  assert self.products[_uId].exists, "Product Not Found"
  
  product: Product = self.products[_uId]
  return(
    product.uId,
    product.stage,
    product.createdAt,
    product.updatedAt
  )