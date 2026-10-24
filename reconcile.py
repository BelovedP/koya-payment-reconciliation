import json

def parse_amount(value):
    if isinstance(value, str):
        value = value.replace(",", "")
    return float(value)

latest = {}
with open("payments.jsonl") as f:
    for line in f:
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if not isinstance(event, dict) or not event.get("txn_id"):
            continue
        txn_id = event["txn_id"]
        if txn_id not in latest or event["ts"] > latest[txn_id]["ts"]:
            latest[txn_id] = event

total = 0.0
count = 0
for event in latest.values():
    if event["status"] == "success":
        total += parse_amount(event["amount"])
        count += 1

with open("expected.txt") as f:
    expected = int(f.read().strip())

if count != expected:
    print(f"Check failed: counted {count} successful payments, expected {expected}.")
else:
    print(f"Check passed: {count} successful payments.")
    print(f"Your code: KOYA-{round(total)}")
