// SPDX-License-Identifier: MIT
pragma solidity ^0.8.28;

interface IZKVerifier { function verifyProof(bytes calldata proof, uint256[] calldata inputs) external view returns (bool); }

contract ComplianceVerifier {
    IZKVerifier public immutable verifier;
    mapping(bytes32 => bool) public verified;

    event ComplianceVerified(bytes32 indexed proofId, bytes32 indexed swapId, bytes32 policyHash);

    constructor(address _verifier) { verifier = IZKVerifier(_verifier); }

    function verify(bytes32 proofId, bytes32 swapId, bytes calldata proof, uint256[] calldata inputs) external returns (bool) {
        require(verifier.verifyProof(proof, inputs), "INVALID_ZK");
        verified[proofId] = true;
        emit ComplianceVerified(proofId, swapId, bytes32(inputs[0]));
        return true;
    }
}
