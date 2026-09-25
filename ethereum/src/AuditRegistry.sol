// SPDX-License-Identifier: MIT
pragma solidity ^0.8.28;
contract AuditRegistry {
    struct Record { bytes32 policyHash; bytes32 proofHash; bytes32 attestationRoot; bytes32 arbitrationId; uint64 timestamp; }
    mapping(bytes32=>Record) public records;
    event AuditCommitted(bytes32 indexed auditId,bytes32 policyHash,bytes32 proofHash,bytes32 attestationRoot,bytes32 arbitrationId);
    function commit(bytes32 auditId,bytes32 policyHash,bytes32 proofHash,bytes32 attestationRoot,bytes32 arbitrationId) external {
        require(records[auditId].timestamp==0,"EXISTS");
        records[auditId]=Record(policyHash,proofHash,attestationRoot,arbitrationId,uint64(block.timestamp));
        emit AuditCommitted(auditId,policyHash,proofHash,attestationRoot,arbitrationId);
    }
}
