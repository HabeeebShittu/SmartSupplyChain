// SPDX-License-Identifier: GPL-3.0

pragma solidity >=0.8.0 <0.9.0;

interface SmartSupplyChainDSNInterface {
  function addProductDNS(uint _productId) external;
}

contract SmartSupplyChainDSN {
  struct ProductDSN {
    uint256   productId;
    address   productOwner;
    uint256   materialCount;
    uint256   processCount;
    bytes32[] materials;
    bytes32[] processes;
    bool      exists;
  }
  mapping(uint256 => ProductDSN) internal products;

  event productEvent(
    uint256 indexed productId,
    address indexed productOwner,
    uint256 materialCount,
    uint256 processCount
  );
  event productMaterialEvent(
    uint256 indexed productId,
    address indexed productOwner,
    uint256 materialCount,
    bytes32 materials
  );

  modifier productVerify(
    uint256 _productId
  ) {
    require(products[_productId].exists, "Product Not Found");
    require(msg.sender == products[_productId].productOwner, "Unautorized Product Access");
    _;
  }

  function hash(
    string memory _string
  ) internal pure returns(bytes32) {
    return keccak256(abi.encode(_string));
  }

  function addProductDNS(
    uint256 _productId
  ) external {
    uint256 _materialCount = 0;
    uint256 _processCount = 0;

    ProductDSN memory newProduct = ProductDSN(
      _productId,
      tx.origin,
      _materialCount,
      _processCount,
      new bytes32[](0),
      new bytes32[](0),
      true
    );
    products[_productId] = newProduct;

    emit productEvent(
      newProduct.productId,
      newProduct.productOwner,
      newProduct.materialCount,
      newProduct.processCount
    );
  }

  function addProductDNSMaterial(
    uint256 _productId,
    string memory _singleMaterial
  ) public productVerify(_productId) {
    ProductDSN storage product = products[_productId];
    bytes32 materialHash = hash(_singleMaterial);

    product.materials.push(materialHash);
    product.materialCount++;

    emit productMaterialEvent(
      product.productId,
      product.productOwner,
      product.materialCount,
      materialHash
    );
  }

  function addProductDNSProcess(
    uint256 _productId,
    string memory _singleProcess
  ) public productVerify(_productId) returns (bytes32) {
    ProductDSN storage product = products[_productId];
    bytes32 processHash = hash(_singleProcess);

    product.processes.push(processHash);
    product.processCount++;

    return processHash;
  }

  function readProductDNS(
    uint256 _productId
  ) public view productVerify(_productId) returns(
    uint256 productId,
    address productOwner,
    uint256 materialCount,
    uint256 processCount
  ) {
    ProductDSN storage product = products[_productId];
    return(
      product.productId,
      product.productOwner,
      product.materialCount,
      product.processCount
    );
  }

  function readProductDNSMaterial(
    uint256 _productId,
    uint256 _materialId
  ) public view productVerify(_productId) returns(
    uint256 productId,
    address productOwner,
    bytes32 materialHash
  ) {
    require(_materialId < products[_productId].materialCount, "Product Material Not Found");

    ProductDSN storage product = products[_productId];
    return(
      product.productId,
      product.productOwner,
      product.materials[_materialId]
    );
  }

  function readProductDNSProcess(
    uint256 _productId,
    uint256 _processId
  ) public view productVerify(_productId) returns(
    uint256 productId,
    address productOwner,
    bytes32 processHash
  ) {
    require(_processId < products[_productId].processCount, "Product Manufacturing Process Not Found");

    ProductDSN storage product = products[_productId];
    return(
      product.productId,
      product.productOwner,
      product.processes[_processId]
    );
  }
}