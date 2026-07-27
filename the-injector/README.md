```
=================================================
  THE INJECTOR
  Chester's Imports · CRATE POST
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

Opens `http://127.0.0.1:42961/`

Terminal mail must be up (sdk-import-station) so inject URL works — default  
`http://127.0.0.1:8765/api/mail/inject` (change if your ROM port differs).

### Seal

Default crate seal (token): `wire-whisper`  
Env override on terminal side: `SDK_MAIL_INJECT_TOKEN`

### What it does

POSTs the same inject the CLI uses:

```json
{ "token", "to", "from", "subject", "body" }
```

Station MAIL marks it **(outside)**. Station-to-station compose is still the terminal’s job; this product is only the **wrong door**.

### Deck Host

```powershell
py -3.12 run-in-deck-host.py
```

(from `prod/`)

---

*Chester’s Imports · “we deliver what was never sent”*
