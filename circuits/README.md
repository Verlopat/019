# Groth16 circuit

Install Circom 2.x, Node.js and the npm packages `circomlib` and `snarkjs`.

Typical local flow:

```bash
npm install circomlib snarkjs
circom circuits/compliance.circom --r1cs --wasm --sym -o build
snarkjs groth16 setup build/compliance.r1cs powersOfTau28_hez_final_*.ptau build/compliance_0000.zkey
snarkjs zkey contribute build/compliance_0000.zkey build/compliance_final.zkey --name=local --entropy=research
snarkjs zkey export verificationkey build/compliance_final.zkey build/verification_key.json
snarkjs zkey export solidityverifier build/compliance_final.zkey ethereum/src/Groth16Verifier.sol
```

The trusted setup command above is for a local prototype. A production research deployment must document the ceremony and entropy source. The Python reference prover is deliberately not described as Groth16.
