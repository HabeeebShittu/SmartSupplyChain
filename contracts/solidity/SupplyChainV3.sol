// SPDX-License-Identifier: GPL-3.0

pragma solidity >=0.8.0 <0.9.0;

import './SupplyChainV3DSN.sol';

contract SmartSupplyChain {
  struct Product {
    uint256 uId;
    uint256 stage;
    string  humidity;
    string  temperature;
    uint256 createdAt;
    uint256 updatedAt;
    bool    exists;
  }

  SmartSupplyChainDSNInterface DSNContract;
  mapping(uint256 => Product) internal products;

  event productEvent(
    uint256 indexed uId,
    uint256 stage,
    string  humidity,
    string  temperature,
    uint256 createdAt,
    uint256 updatedAt
  );

  constructor(
    address dsnContractAddress
  ) {
    DSNContract = SmartSupplyChainDSNInterface(dsnContractAddress);
  }

  function addProduct(
    uint256 _uId
  ) internal {
    uint256 _stage = 0;
    string memory _humidity = "20%";
    string memory _temperature = "20 C";

    Product memory newProduct = Product(
      _uId,
      _stage,
      _humidity,
      _temperature,
      block.timestamp,
      block.timestamp,
      true
    );
    products[_uId] = newProduct;

    DSNContract.addProductDNS(_uId);

    emit productEvent(
      newProduct.uId,
      newProduct.stage,
      newProduct.humidity,
      newProduct.temperature,
      newProduct.createdAt,
      newProduct.updatedAt
    );
  }

  function updateProduct(
    uint256 _uId
  ) internal {
    require(products[_uId].stage < 6, "Product fully delivered");

    Product storage product = products[_uId];
    product.stage++;
    product.updatedAt = block.timestamp;

    emit productEvent(
      product.uId,
      product.stage,
      product.humidity,
      product.temperature,
      product.createdAt,
      product.updatedAt
    );
  }

  function writeProduct(
    uint256 _uId
  ) public returns(
    bool status
  ) {
    if (products[_uId].exists) {
      updateProduct(_uId);
    } else {
      addProduct(_uId);
    }

    return true;
  }

  function readProduct(
    uint256 _uId
  ) public view returns(
    uint256 uId,
    uint256 stage,
    string memory humidity,
    string memory temperature,
    uint256 createdAt,
    uint256 updatedAt
  ) {
    require(products[_uId].exists, "Product Not Found");

    Product storage product = products[_uId];
    return(
      product.uId,
      product.stage,
      product.humidity,
      product.temperature,
      product.createdAt,
      product.updatedAt
    );
  }
}