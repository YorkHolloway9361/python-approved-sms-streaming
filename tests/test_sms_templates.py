from src.sms_templates import ApprovedAsset, publish_asset


class FakeClient:
    def __init__(self):
        self.calls = []

    def create_signature(self, payload):
        self.calls.append(("signature", payload))
        return {"id": "sig-1"}

    def create_template(self, payload):
        self.calls.append(("template", payload))
        return {"id": "tpl-1"}


def test_publish_asset_keeps_creator_trace_and_two_approved_records():
    client = FakeClient()
    result = publish_asset(ApprovedAsset("creator-7", "release-alert", "en-US", "StreamCo", "New episode: {{title}}"), client)
    assert result["creator_id"] == "creator-7"
    assert [kind for kind, _ in client.calls] == ["signature", "template"]
    assert client.calls[1][1]["locale"] == "en-US"
