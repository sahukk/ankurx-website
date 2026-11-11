"""AnkurX publisher.

Usage:
  python3 publish.py check                 # validate all data, rebuild index.json, no push
  python3 publish.py bulletin DRAFT.json   # add/replace a bulletin, rebuild index, commit + push
  python3 publish.py opps                  # validate opportunities.json, commit + push
  python3 publish.py push "message"        # commit + push whatever changed

Bulletin JSON: {"id":"YYYY-MM-DD-am|pm","date":"YYYY-MM-DD","slot":"am|pm",
  "items":[{"cat":"job|gen|new|talent","head":..,"body":..,"source":..,"url":..,"district":..}],
  "corrections":[optional strings]}
Opportunity: {"title","org","lastDate":"YYYY-MM-DD","url","eligibility","district"}
"""
import json, os, re, sys, shutil, subprocess, datetime

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # repo root
BDIR = os.path.join(SITE, "data", "bulletins")
CATS = {"job", "gen", "new", "talent"}
IST = datetime.timezone(datetime.timedelta(hours=5, minutes=30))


def fail(msg):
    sys.exit("ERROR: " + msg)


def check_bulletin(b, name):
    for k in ("id", "date", "slot", "items"):
        if k not in b:
            fail(f"{name}: missing '{k}'")
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}-(am|pm)", b["id"]):
        fail(f"{name}: bad id {b['id']}")
    if b["id"] != f"{b['date']}-{b['slot']}":
        fail(f"{name}: id must equal date-slot")
    if not b["items"]:
        fail(f"{name}: no items")
    for i, it in enumerate(b["items"]):
        for k in ("cat", "head", "body"):
            if not it.get(k):
                fail(f"{name} item {i}: missing '{k}'")
        if it["cat"] not in CATS:
            fail(f"{name} item {i}: cat must be one of {sorted(CATS)}")
        if it.get("url") and not it["url"].startswith("https://"):
            fail(f"{name} item {i}: url must start with https://")


def rebuild_index():
    entries = []
    for f in sorted(os.listdir(BDIR)):
        if not f.endswith(".json"):
            continue
        b = json.load(open(os.path.join(BDIR, f), encoding="utf8"))
        check_bulletin(b, f)
        if f != b["id"] + ".json":
            fail(f"{f}: file name must be {b['id']}.json")
        entries.append({"id": b["id"], "date": b["date"], "slot": b["slot"],
                        "count": len(b["items"]), "lead": b["items"][0]["head"]})
    entries.sort(key=lambda e: e["id"], reverse=True)
    idx = {"updated": datetime.datetime.now(IST).isoformat(timespec="seconds"), "bulletins": entries}
    json.dump(idx, open(os.path.join(SITE, "data", "index.json"), "w", encoding="utf8"), ensure_ascii=False, indent=1)
    print(f"index: {len(entries)} bulletins, latest {entries[0]['id'] if entries else '-'}")


def check_opps():
    o = json.load(open(os.path.join(SITE, "data", "opportunities.json"), encoding="utf8"))
    for i, it in enumerate(o.get("items", [])):
        if not it.get("title") or not it.get("url", "").startswith("https://"):
            fail(f"opportunity {i}: needs title and https url")
        if it.get("lastDate") and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", it["lastDate"]):
            fail(f"opportunity {i}: lastDate must be YYYY-MM-DD")
    print(f"opportunities: {len(o.get('items', []))}")


def push(msg):
    git = lambda *a: subprocess.run(["git", "-C", SITE, *a], check=True)
    git("add", "-A")
    if subprocess.run(["git", "-C", SITE, "diff", "--cached", "--quiet"]).returncode == 0:
        print("nothing to publish")
        return
    git("commit", "-q", "-m", msg)
    git("push", "-q")
    print("pushed; live at https://ankurx.in in about a minute")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "check"
    if cmd == "bulletin":
        src = sys.argv[2]
        b = json.load(open(src, encoding="utf8"))
        check_bulletin(b, src)
        shutil.copyfile(src, os.path.join(BDIR, b["id"] + ".json"))
        rebuild_index(); check_opps()
        push(f"Bulletin {b['id']}")
    elif cmd == "opps":
        check_opps(); push("Update opportunities")
    elif cmd == "push":
        rebuild_index(); check_opps(); push(sys.argv[2] if len(sys.argv) > 2 else "Update site")
    else:
        rebuild_index(); check_opps()
