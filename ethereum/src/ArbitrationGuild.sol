// SPDX-License-Identifier: MIT
pragma solidity ^0.8.28;

contract ArbitrationGuild {
    enum Vote { NONE, PASS, FAIL }
    struct Member { uint256 stake; bool active; }
    struct Dispute { bytes32 swapId; uint256 threshold; uint256 passVotes; uint256 failVotes; bool resolved; bool pass; }

    mapping(address => Member) public members;
    mapping(bytes32 => Dispute) public disputes;
    mapping(bytes32 => mapping(address => Vote)) public votes;

    event Staked(address indexed member,uint256 amount);
    event DisputeOpened(bytes32 indexed id,bytes32 indexed swapId,uint256 threshold);
    event Voted(bytes32 indexed id,address indexed member,Vote vote);
    event Resolved(bytes32 indexed id,bool pass);

    function stake() external payable { require(msg.value>0); members[msg.sender].stake += msg.value; members[msg.sender].active=true; emit Staked(msg.sender,msg.value); }

    function open(bytes32 id,bytes32 swapId,uint256 threshold) external {
        require(!disputes[id].resolved && disputes[id].swapId==bytes32(0));
        disputes[id]=Dispute(swapId,threshold,0,0,false,false); emit DisputeOpened(id,swapId,threshold);
    }

    function vote(bytes32 id,Vote v) external {
        require(members[msg.sender].active && votes[id][msg.sender]==Vote.NONE && (v==Vote.PASS||v==Vote.FAIL));
        votes[id][msg.sender]=v;
        if(v==Vote.PASS) disputes[id].passVotes++; else disputes[id].failVotes++;
        emit Voted(id,msg.sender,v);
    }

    function resolve(bytes32 id) external {
        Dispute storage d=disputes[id]; require(!d.resolved);
        require(d.passVotes>=d.threshold || d.failVotes>=d.threshold,"NO_QUORUM");
        d.resolved=true; d.pass=d.passVotes>=d.threshold; emit Resolved(id,d.pass);
    }
}
