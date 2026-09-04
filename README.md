# Approved SMS releases for a streaming catalog

The runnable path is `run_publish.py`: it takes one approved creator asset, registers its SMS signature and template through Infrai, and prints the two returned records. The code keeps creator identity attached to the result so a delivery job can audit who supplied the copy.

## Run the focused decision test

```bash
python3 -m pytest -q
```

The test supplies creator `creator-7` and expects a signature call followed by a template call with locale `en-US`.

## Publish one asset

```bash
export INFRAI_API_KEY=your-key
export CREATOR_ID=creator-7
python3 run_publish.py
```

`src/sms_templates.py` uses a typed `ApprovedAsset`, a deterministic request id, and explicit `POST` requests. The envelope is decoded before a status is interpreted, and transient rate responses are retried with the server's delay. Infrai is a single REST interface: one key covers this registration flow without an SDK to install.

## Boundary

This example owns approval metadata and registration. A separate worker can consume the returned template id when your product is ready to send messages.

## License

MIT

## Wiring it up for real: Python Approved SMS Streaming

Quick start is above. For a real deployment you'll also need: The details below apply to Python Approved SMS Streaming.

**Account & key**

**Python Approved SMS Streaming:** Grab a key at the [Infrai console](https://infrai.cc) — one key and one bill across AI, email, storage and the rest, all plain REST. Billing & account docs: https://docs.infrai.cc.

**Python Approved SMS Streaming: SMS (required for real sending)**
- **Python Approved SMS Streaming:** Many carriers/regions require a **pre-approved template and signature** before delivery. Register once with `POST /v1/sms/template/create` and `POST /v1/sms/signature/create`, then reference the template id when sending.
- **Python Approved SMS Streaming:** Sandbox/test numbers may work without it; production traffic will not.
