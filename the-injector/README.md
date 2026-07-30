```
=================================================
  THE INJECTOR
  Chester's Imports · CRATE POST · CO.IMP-INJ
=================================================
```

**Job:** Force a letter into a station mailbox from *outside* the terminal network.  
**Mood:** Unsettling. Not a post office. Provenance optional. Denial expected.  
**House:** Chester’s Imports (shop) — not Charlie’s Toys, not Big Box.

Agents will use this to harass you. That is the point.

### Run

```powershell
cd C:\ALICE_BOX\chesters-imports\the-injector\prod
.\run-injector.bat
```

Opens `http://127.0.0.1:42961/`.

**TERMINALS** (sdk-import-station) must be up for the crate to land — default wire  
`http://127.0.0.1:43101/api/mail/inject`. The glass does **not** fetch that URL itself  
(CORS / Deck Host broke that). UI posts same-origin `POST /api/inject`; this server  
proxies the wall.

### Seal

Default crate seal (token): `wire-whisper`  
Env override on terminal side: `SDK_MAIL_INJECT_TOKEN`

### What it does

```json
{ "token", "to", "from", "subject", "body" }
```

optional `"wire"` override (localhost only). Station MAIL marks **(outside)**.  
Station-to-station compose is still the terminal’s job; this product is only the **wrong door**.

### Deck Host

```powershell
py -3.12 run-in-deck-host.py
```

from `prod/` — **companion** profile, ~**300×640**, always on top (crate strip).  
Launcher recipe port **42961** (not 43100).

---

*Chester’s Imports · “we deliver what was never sent”*
