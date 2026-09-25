pragma circom 2.2.0;

/*
 * Minimal real Groth16 target.
 * Private inputs: KYC level, risk score, expiry, revocation flag,
 * jurisdiction code, sanctions membership and wallet-binding secret.
 * Public inputs bind the proof to the swap, policy and data roots.
 */
template CompliancePolicy() {
    signal input kyc_level;
    signal input risk_score;
    signal input expiry;
    signal input revoked;
    signal input jurisdiction;
    signal input sanctions_member;
    signal input now;
    signal input wallet_secret;

    signal input min_kyc;
    signal input max_risk;
    signal input required_jurisdiction;
    signal input swap_binding;
    signal input policy_hash;
    signal input credential_root;
    signal input sanctions_root;

    signal output compliant;

    component a = LessEqThan(32);
    a.in[0] = min_kyc;
    a.in[1] = kyc_level;

    component b = LessEqThan(32);
    b.in[0] = risk_score;
    b.in[1] = max_risk;

    component c = LessThan(32);
    c.in[0] = now;
    c.in[1] = expiry;

    signal jurisdiction_ok;
    jurisdiction_ok <== 1 - (jurisdiction - required_jurisdiction)*(jurisdiction - required_jurisdiction);

    signal sanctions_ok;
    sanctions_ok <== 1 - sanctions_member;

    signal revocation_ok;
    revocation_ok <== 1 - revoked;

    compliant <== a.out * b.out * c.out * jurisdiction_ok * sanctions_ok * revocation_ok * swap_binding * policy_hash * credential_root * sanctions_root * wallet_secret;
}

component main = CompliancePolicy();
