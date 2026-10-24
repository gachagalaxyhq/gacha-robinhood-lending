# Gacha Galaxy: public vault recovery reference

This is a read-only status page, not a new vault and not a key-recovery tool.
No deployment, transaction, signing, approval, funding, or borrowing is included.
Transaction controls remain deliberately unavailable. Only verified, read-only debt display has been added.

## Save and reopen

Keep `index.html`, `config.json`, and this guide in durable storage (preferably two independent backups). The HTML embeds the exact public JSON configuration and needs no build, CDN, chat session, temporary server, or adjacent files. Open it directly to view the public reference; click **Refresh public status** for live reads. Live reads need internet, RPC availability, and browser CORS permission. Local-file wallet injection and browser RPC requests are environment-dependent and have not been verified in Trust Wallet. A read failure clears every live value; it does not mean balances are zero. No live balances or wallet permissions are persisted.

Owner and guardian (public): **0xD77C34899858088DE6888F36fA46e2d6468F4Ca5**

## Trust Wallet recovery and connection

1. Retain your existing Trust Wallet recovery material using your established offline process. Never type a seed phrase or private key into this page, a chat, source control, or any website. Restoring wallet keys is outside this page's scope; no operator/private material is included or read.
2. Confirm that the wallet address matches the owner above. The saved public address alone cannot restore control.
3. Manually select/configure Robinhood Chain mainnet: chain ID **4663** / **0x1237**, native symbol **ETH**, RPC `https://rpc.mainnet.chain.robinhood.com`, explorer `https://robinhoodchain.blockscout.com`. This page never requests a chain addition or switch.
4. In a trusted HTTPS copy opened through Trust Wallet's browser or injected extension, click **Connect Trust Wallet**. Only this click requests accounts. It checks `eth_chainId` and `eth_accounts`; it never asks for a signature or transaction. Other accounts and networks are rejected. No WalletConnect QR/relay fallback is included.
5. Account changes, network changes, disconnects, failed reads, and restored browser-history pages clear live values. Reconnect and refresh. **Forget connection** clears local session state, but does not revoke wallet-side site permissions.

## Public configuration and explorer fallback

| Item | Address / setting |
| --- | --- |
| Owner / guardian | 0xD77C34899858088DE6888F36fA46e2d6468F4Ca5 |
| Registry | 0x2A585396dd0248A060045b3f557076fB1B4Cb0eb |
| Cards | 0x487F04b4BCE3f1509e11c189A44b3aFfe21C6653 |
| Vault | 0xa4a98F8A373E98Ce555a7F6e1FF2094C858D8F23 |
| USDG | 0x5fc5360D0400a0Fd4f2af552ADD042D716F1d168 |
| USDG decimals / card ID | 6 / 1 |

Explorer: `https://robinhoodchain.blockscout.com` (append `/address/` and the public address). The HTML includes clickable links for every saved address.

Official USDG address reference: https://docs.paxos.com/guides/stablecoin/usdg/mainnet

## What is checked, and what is not

Each refresh checks the RPC chain before and after a block-pinned snapshot; nonempty code at vault/registry/cards/USDG; vault owner, guardian, loanAsset, cards and registry references; paused flag; USDG decimals; saved-owner ETH/USDG; vault USDG balance; card #1 owner; and token #1 position owner/debt using the verified schema. The vault runtime SHA-256 must match the verified deployment before position decoding. Browsers without Web Crypto fail closed. Connected-wallet network/account are checked before and after reads. Any failure discards the entire snapshot. Code presence is not a bytecode audit, proxy/implementation verification, or proof of safety. A chain ID returned by an RPC is not independent proof the RPC is honest. Public reads disclose queried public addresses to the RPC provider.

The exact scalar read selectors in the HTML were recomputed from their named signatures and confirmed against public mainnet RPC on 2026-10-24. Standard balance/owner reads are strictly length-validated. Local contract sources are outdated and were not used as deployed ABI authority.

### Verified debt schema

Authority: [Sourcify exact-match source, ABI and bytecode](https://sourcify.dev/server/v2/contract/4663/0xa4a98F8A373E98Ce555a7F6e1FF2094C858D8F23?fields=all), chain 4663, match ID `56301548`, verified `2026-10-17T12:56:54Z`. Blockscout did not provide a verified ABI. Sourcify's creation and runtime bytes were compared with RPC deployment input and runtime; its recompiled runtime plus documented immutable substitutions also matched exactly. No independent local Solidity recompilation was performed.

`positions(uint256) view returns (address owner, uint256 debt)`, selector `0x99fbab88`. Verified source declares `struct Position { address owner; uint256 debt; }`. Debt is a uint256 in the loan asset's base units; the configured USDG contract returns 6 decimals. The layout is not inferred from response length or zeros.

Expected deployed runtime SHA-256: `e9e012a1bc5dc65bb360584964158da67940510544233b004ae7c0836854c103`. Each refresh hashes the block-pinned vault runtime before decoding. The return must contain exactly two ABI words with valid address padding. Wrong runtime, malformed returns or read failures clear all live fields, including debt. There is no cached debt fallback.

At investigation block `96632730` (`0x5c27f9a`), token #1 had zero position owner and zero debt; card ownership was the saved owner. This is historical evidence, not a cached live value or proof of current debt. No `stats()` tuple or `poolCap()` / `perCardCap()` is used. Before any future transaction UI, separately review permissions, limits and transaction semantics. A passing snapshot is not an all-clear for funding or a contract safety audit.

## Hosting and independent copies

GitHub Pages serves `main` / `docs` at https://gachagalaxyhq.github.io/gacha-robinhood-lending/pilot/. Keep independent recovery copies: static hosting does not make a service permanent or restore lost keys. Earlier recovery ZIPs do not automatically receive this update.

## Verification and tests

The debt-display candidate passed 36 Node mock-harness tests covering the real inline JavaScript: nonzero debt, malformed ABI returns, wrong runtime hash, chain/account mismatch, read failures, stale-value clearing and wallet events. Test/evidence files are intentionally not published in this docs-only update. The original lending pages and tests are untouched.

Mock tests and a page screenshot do not prove Trust Wallet compatibility. No real wallet connection, signing, approvals, transactions, funding or contract deployment is part of this update. Live reads require internet, RPC availability, browser CORS permission and Web Crypto.
