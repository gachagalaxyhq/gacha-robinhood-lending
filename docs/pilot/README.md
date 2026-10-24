# Gacha Galaxy: public vault recovery reference

This is a read-only status page, not a new vault and not a key-recovery tool.
No deployment, transaction, signing, approval, funding, or borrowing is included.
Transaction controls are deliberately unavailable pending deployed ABI verification.

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

Each refresh checks the RPC chain before and after a block-pinned snapshot; nonempty code at vault/registry/cards/USDG; vault owner, guardian, loanAsset, cards and registry references; paused flag; USDG decimals; saved-owner ETH/USDG; vault USDG balance; and card #1 owner. Connected-wallet network/account are checked before and after reads. Any failure discards the entire snapshot. Code presence is not a bytecode audit, proxy/implementation verification, or proof of safety. A chain ID returned by an RPC is not independent proof the RPC is honest. Public reads disclose queried public addresses to the RPC provider.

The exact scalar read selectors in the HTML were recomputed from their named signatures and confirmed against public mainnet RPC on 2026-10-24. Standard balance/owner reads are strictly length-validated. Local contract sources are outdated and were not used as deployed ABI authority. No full deployed ABI was obtained from the public explorer response. `positions(uint256)` output layout is not verified, so **debt remains explicitly unavailable** (the previously reported zero is not promoted to a live read). No `stats()` tuple layout or `poolCap()` / `perCardCap()` is assumed. Before any future transaction UI, independently verify the deployed ABI/implementation, debt schema, permissions, limits and transaction semantics. A passing snapshot is not an all-clear for funding.

## Hosting proposal — NOT published

The existing repository is `gachagalaxyhq/gacha-robinhood-lending`. If its GitHub Pages setup serves `docs/`, the proposed route is `https://gachagalaxyhq.github.io/gacha-robinhood-lending/pilot/`. This change does not commit, push, enable Pages, publish that URL, or verify its availability. A future explicit deployment authorization is required. The recovery ZIP remains usable without that hosting; keep your own copies. Static hosting does not make a service permanent or restore lost keys.

## Tests

From the repository root: `node --test test/lending-ui.test.cjs test/pilot-ui.test.cjs`.
The original lending tests and pages are untouched. Pilot tests execute the real inline JavaScript with mocked DOM, RPC and wallet providers; they do not prove actual Trust Wallet/browser compatibility or chain safety.

From the extracted ZIP: `node --test test/pilot-ui.test.cjs` (pilot files are under `docs/pilot/`).
