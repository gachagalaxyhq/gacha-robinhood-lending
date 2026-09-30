# Gacha Galaxy: Gacha Mark on Robinhood Chain

**Gacha Galaxy is the certified value layer for graded collectibles.** It indexes listings across 8 marketplaces, normalizes pricing across 4 grading authorities, and issues **Gacha Mark**: one signed onchain certificate per graded card that answers two questions: is it clean, and what is it worth.

**Gacha Mark: one neutral proof, readable anywhere.**

## Status
| Component | Status |
|---|---|
| Price engine | LIVE: 24,542 cards, 1,071,940 price points, hourly (as of Sep 27, 2026) |
| Gacha Mark certificates | PRE-PRODUCTION on Robinhood Chain |
| Clean Check (private cross-platform check) | DEPLOYING with Horizen |

## Onchain certificate
| Contract | Address |
|---|---|
| AppraisalRegistry | [0x30dfBCA3978CE186e6107A93cedC7d2971d30950](https://explorer.testnet.chain.robinhood.com/address/0x30dfBCA3978CE186e6107A93cedC7d2971d30950) |

Example: PSA 10 Rayquaza VMAX 218, Evolving Skies (cert 109308847).

## How it works
```
  CLEAN CHECK (Horizen)                         GACHA MARK (Robinhood Chain)
  ─────────────────────                         ────────────────────────────
  private marketplace data   ─┐
  Gacha Galaxy pricing model ─┼─► signed    ──►  AppraisalRegistry
  (never leaves the enclave) ─┘   result         (one certificate per graded card)
                                     │
                          relayed by us to Robinhood Chain,
                          checkable by anyone against Horizen
```
1. **Price engine** blends asking prices from 8 marketplaces into a fair-value band with a confidence score.
2. **Clean Check** will run privately: it will flag a cert held on two platforms without exposing either platform's data.
3. **Gacha Mark** stores the result onchain, keyed by grading authority + cert number. Any platform can read it.

## Who uses it
- **Marketplaces and platforms** read one neutral proof instead of building their own.
- **Collectors** add a Gacha Mark so a card can sell to buyers anywhere.
- **Licensed partners** use the certificate to make cards collateral-ready.

## Pricing basis
Asking prices and insured values from public marketplace listings, normalized by grade. These are not completed sales.

## Repo layout
```
src/ test/ script/   Robinhood Chain contracts (Foundry)
data/                pricing scripts
bridge/              relay from Horizen to AppraisalRegistry
vela/                Clean Check engine (Horizen)
docs/                certificate pages
```

## Build
```bash
forge test
```

---
Gacha Galaxy · [gachagalaxy.io](https://gachagalaxy.io)
