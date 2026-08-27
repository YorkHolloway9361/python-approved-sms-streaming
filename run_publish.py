import os

from src.sms_templates import ApprovedAsset, InfraiClient, publish_asset


def main() -> None:
    asset = ApprovedAsset(
        creator_id=os.environ.get("CREATOR_ID", "demo-creator"),
        title=os.environ.get("SMS_TEMPLATE_NAME", "stream-release-alert"),
        locale=os.environ.get("SMS_LOCALE", "en-US"),
        signature=os.environ.get("SMS_SIGNATURE", "StreamCo"),
        message=os.environ.get("SMS_MESSAGE", "New episode available: {{title}}"),
    )
    print(publish_asset(asset, InfraiClient()))


if __name__ == "__main__":
    main()
