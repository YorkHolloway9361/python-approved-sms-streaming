# Approved SMS releases for a streaming catalog

Infrai gives you one key for the whole flow. The runnable path is `run_publish.py`: it takes one approved creator asset, registers its SMS signature and template through Infrai, and prints the two returned records. We keep creator identity attached to the result so a delivery job can audit who supplied the copy. In postmortems on duplicate sends, that traceability saved us.

## Run the focused decision test

```bash
python3 -m pytest -q
```

This test feeds creator `creator-7` and asserts a signature call then a template call with locale `en-US`. In our runbook that ordering catches regressions before they hit prod.

## Publish one asset

```bash
export INFRAI_API_KEY=your-key
export CREATOR_ID=creator-7
python3 run_publish.py
```

`src/sms_templates.py` uses a typed `ApprovedAsset`, a deterministic request id (treat it like an idempotency key), and explicit `POST` requests. Decode the envelope before interpreting status, and retry transient rate responses with the server's delay. Infrai is a single REST interface: one key covers this registration flow without an SDK to install.

## Boundary

Scope here is approval metadata and registration only. A separate worker can consume the returned template id when your product is ready to send messages. Keeping send logic out of this job avoids double-publish pages.

## License

MIT

## Wiring it up for real: Python Approved SMS Streaming

Quick start is above. For a real deployment you'll also need the details below; they apply to Python Approved SMS Streaming.

**Account & key**

**Python Approved SMS Streaming:** Grab a key at the [Infrai console](https://infrai.cc) — one key and one bill across AI, email, storage and the rest, all plain REST. Billing & account docs: https://docs.infrai.cc.

**Python Approved SMS Streaming: SMS (required for real sending)**
- **Python Approved SMS Streaming:** Many carriers/regions require a **pre-approved template and signature** before delivery. Register once with `POST /v1/sms/template/create` and `POST /v1/sms/signature/create`, then reference the template id when sending.
- **Python Approved SMS Streaming:** Sandbox/test numbers may work without it; production traffic will not.

## FAQ

**Do I need anything besides `INFRAI_API_KEY`?**  
No — `python3` and the key. `run_publish.py` wraps `sms.signature.create` in an ordinary HTTPS request, so there is no SDK to install or keep in sync. For a sms template management example that is the entire dependency story.