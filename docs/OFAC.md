# Sanctions snapshot

The specification requires a frozen official sanctions snapshot. OFAC's Sanctions List Service is the current distribution mechanism for sanctions list data and publishes content hashes for assurance.

Workflow:

1. Download the exact SDN/consolidated data file from OFAC.
2. Record the publication/snapshot date.
3. Record its SHA-256.
4. Extract digital-currency addresses.
5. Build a deterministic Merkle tree and record the root.
6. Commit the metadata, not a mutable live query.

Use:

`python scripts/freeze_ofac.py <downloaded-file> --date YYYY-MM-DD`

The repository intentionally does not silently bundle a live sanctions list: the experiment must use a dated, hashed snapshot so results remain reproducible.
