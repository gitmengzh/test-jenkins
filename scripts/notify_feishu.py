import json
import os
import urllib.request
import xml.etree.ElementTree as ET


def read_junit(path: str):
    if not os.path.exists(path):
        return {"total": 0, "failures": 0, "errors": 0, "skipped": 0, "passed": 0}

    root = ET.parse(path).getroot()
    node = root
    if root.tag == "testsuites":
        suites = list(root.findall("testsuite"))
        if suites:
            node = suites[0]

    total = int(node.attrib.get("tests", 0))
    failures = int(node.attrib.get("failures", 0))
    errors = int(node.attrib.get("errors", 0))
    skipped = int(node.attrib.get("skipped", 0))
    passed = total - failures - errors - skipped
    return {
        "total": total,
        "failures": failures,
        "errors": errors,
        "skipped": skipped,
        "passed": passed,
    }


def send_feishu(webhook: str, text: str):
    body = {"msg_type": "text", "content": {"text": text}}
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(
        webhook, data=data, headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        return resp.read().decode("utf-8")


if __name__ == "__main__":
    webhook = os.getenv("FEISHU_WEBHOOK", "")
    report = read_junit("reports/junit.xml")
    status = "SUCCESS" if (report["failures"] + report["errors"]) == 0 else "FAILED"
    msg = (
        f"[Jenkins Pytest] {status}\n"
        f"total={report['total']}, passed={report['passed']}, "
        f"failures={report['failures']}, errors={report['errors']}, "
        f"skipped={report['skipped']}"
    )

    if webhook:
        result = send_feishu(webhook, msg)
        print("feishu:", result)
    else:
        print("FEISHU_WEBHOOK not set, skip send.")
        print(msg)
