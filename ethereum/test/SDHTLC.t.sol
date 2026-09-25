// SPDX-License-Identifier: MIT
pragma solidity ^0.8.28;
import "forge-std/Test.sol";
import "../src/SwapHTLC.sol";
contract SDHTLCTest is Test {
 SwapHTLC h;
 function setUp() public { h=new SwapHTLC(); }
 function testCreateAndReject() public {
  bytes32 id=keccak256("id"); h.create{value:1 ether}(id,keccak256(abi.encode(bytes32("secret"))),bytes32("policy"),block.timestamp+100,address(this));
  h.setCompliance(id,false); h.refund(id);
 }
 function testFuzzNoEarlyRefund(uint64 wait) public {
  vm.assume(wait<100); bytes32 id=keccak256("id2"); h.create{value:1 ether}(id,keccak256(abi.encode(bytes32("s"))),bytes32("p"),block.timestamp+100,address(this)); h.setCompliance(id,true); vm.warp(block.timestamp+wait);
  vm.expectRevert(); h.refund(id);
 }
}
