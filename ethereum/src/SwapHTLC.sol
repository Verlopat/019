// SPDX-License-Identifier: MIT
pragma solidity ^0.8.28;

contract SwapHTLC {
    enum State { Created, CompliancePending, Locked, Rejected, Released, Refunded }
    struct Swap { bytes32 secretHash; bytes32 policyHash; uint256 expiry; State state; address payable maker; address payable taker; }
    mapping(bytes32=>Swap) public swaps;
    mapping(bytes32=>bool) public compliance;
    event Created(bytes32 indexed id,bytes32 secretHash,bytes32 policyHash);
    event ComplianceSet(bytes32 indexed id,bool pass);
    event Claimed(bytes32 indexed id,address indexed who);
    event Refunded(bytes32 indexed id);

    function create(bytes32 id,bytes32 secretHash,bytes32 policyHash,uint256 expiry,address payable taker) external payable {
        require(swaps[id].maker==address(0) && expiry>block.timestamp);
        swaps[id]=Swap(secretHash,policyHash,expiry,State.CompliancePending,payable(msg.sender),taker); emit Created(id,secretHash,policyHash);
    }
    function setCompliance(bytes32 id,bool pass) external {
        require(swaps[id].maker!=address(0)); compliance[id]=pass; swaps[id].state=pass?State.Locked:State.Rejected; emit ComplianceSet(id,pass);
    }
    function claim(bytes32 id,bytes32 secret) external {
        Swap storage s=swaps[id]; require(s.state==State.Locked && block.timestamp<s.expiry && keccak256(abi.encode(secret))==s.secretHash,"INVALID_CLAIM");
        s.state=State.Released; s.taker.transfer(address(this).balance); emit Claimed(id,msg.sender);
    }
    function refund(bytes32 id) external {
        Swap storage s=swaps[id]; require(block.timestamp>=s.expiry || s.state==State.Rejected,"NOT_REFUNDABLE");
        s.state=State.Refunded; s.maker.transfer(address(this).balance); emit Refunded(id);
    }
}
