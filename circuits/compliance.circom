pragma circom 2.2.0;
include "circomlib/circuits/comparators.circom";

template CompliancePolicy() {
    signal input kyc_level;
    signal input risk_score;
    signal input expiry;
    signal input revoked;
    signal input jurisdiction;
    signal input sanctions_member;
    signal input now;
    signal input min_kyc;
    signal input max_risk;
    signal input required_jurisdiction;
    signal input swap_binding;
    signal input policy_hash;
    signal input credential_root;
    signal input sanctions_root;

    signal output compliant;

    component a = LessEqThan(32);
    a.in[0] <== min_kyc; a.in[1] <== kyc_level;
    component b = LessEqThan(32);
    b.in[0] <== risk_score; b.in[1] <== max_risk;
    component c = LessThan(32);
    c.in[0] <== now; c.in[1] <== expiry;
    component j = IsEqual();
    j.in[0] <== jurisdiction; j.in[1] <== required_jurisdiction;

    signal sanctions_ok; sanctions_ok <== 1 - sanctions_member;
    signal revocation_ok; revocation_ok <== 1 - revoked;

    // swap_binding is a binary public binding witness. The roots/hashes are
    // public signals in the generated Groth16 input vector; they bind the
    // proof transcript to a concrete policy/data snapshot.
    compliant <== a.out * b.out * c.out * j.out * sanctions_ok * revocation_ok * swap_binding;
}
component main {public [min_kyc,max_risk,required_jurisdiction,swap_binding,policy_hash,credential_root,sanctions_root]} = CompliancePolicy();
