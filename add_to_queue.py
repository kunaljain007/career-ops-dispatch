import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

new_emails = [
    "ananya.birla@hindalco.com",
    "peyushbansal@gmail.com",
    "peyushb@lenskart.com",
    "amiteshjha@gmail.com",
    "amiteshjha@rediffmail.com",
    "amitesh.jha@swiggy.in",
    "nandanreddy17@gmail.com",
    "dilipsurana@microlabs.in",
    "ranjeet.goswami@tcs.com",
    "major_ranjeet@yahoo.co.in",
    "mitin@indiasmeinvestments.com",
    "anandsurana@microlabs.in",
    "surana.anand@gmail.com",
    "suranaanand@gmail.com",
    "anandsurana@icegen.net",
    "pranav.jyoti@chicagoboothexec.org",
    "prjyoti@gmail.com",
    "pranavjyoti@hotmail.com",
    "prkharjain@gmail.com",
    "sanjana.simha@ap.gov.in",
    "akshat.jain@nic.in",
    "acs.arom@maharashtra.gov.in",
    "ssaunik@gmail.com",
    "tukaram.mundhe@maharashtra.gov.in",
    "ias.tukaram@gmail.com",
    "shrikarpardeshi@gmail.com",
    "dcm@maharashtra.gov.in",
    "psec.cm@maharashtra.gov.in",
    "p.ias@maharashtra.gov.in",
    "sravankps4uall@gmail.com",
    "ncnara486@gmail.com",
    "l.nara@ap.gov.in",
    "lokesh.nara@gmail.com",
    "rmdf@rmdgroup.net",
    "rmdhariwal@manikchandgroup.com",
    "a_dhariwal@manikchandgroup.com",
    "nilavikhe@gmail.com",
    "nila_patil@hotmail.com",
    "nila.patil@se.pwc.com"
]

queue_file = "data/all_unsent_emails.json"
sent_log_file = "data/logs/master_all_sent.json"

blacklist = ["godrej", "itc.in", "3one4capital"]

# Load sent log
sent_emails = set()
if os.path.exists(sent_log_file):
    try:
        with open(sent_log_file, "r", encoding="utf-8") as f:
            sent_data = json.load(f)
            if isinstance(sent_data, list):
                for item in sent_data:
                    if isinstance(item, str):
                        sent_emails.add(item.lower().strip())
                    elif isinstance(item, dict) and "email" in item:
                        sent_emails.add(item["email"].lower().strip())
            elif isinstance(sent_data, dict):
                for k in sent_data.keys():
                    sent_emails.add(k.lower().strip())
        print(f"Loaded {len(sent_emails)} sent emails for deduplication.")
    except Exception as e:
        print(f"Warning reading sent log: {e}")

# Load unsent queue
with open(queue_file, "r", encoding="utf-8") as f:
    queue = json.load(f)

print(f"Current unsent queue count: {len(queue)}")
existing_queue_set = set(e.lower().strip() for e in queue if isinstance(e, str))

to_add = []
for em in new_emails:
    em_clean = em.lower().strip()
    # Check blacklist
    if any(b in em_clean for b in blacklist):
        print(f"SKIPPED (blacklisted): {em_clean}")
        continue
    # Check sent
    if em_clean in sent_emails:
        print(f"SKIPPED (already sent): {em_clean}")
        continue
    # Check queue
    if em_clean in existing_queue_set:
        print(f"ALREADY IN QUEUE: {em_clean}")
        # If in queue, move to front
        queue = [x for x in queue if x.lower().strip() != em_clean]
        to_add.append(em_clean)
    else:
        to_add.append(em_clean)

# Prepend to front of queue
queue = to_add + queue

with open(queue_file, "w", encoding="utf-8") as f:
    json.dump(queue, f, indent=2)

print(f"Updated unsent queue! Added {len(to_add)} emails to the front.")
print(f"New queue count: {len(queue)}")
print("Front of queue:")
for i, e in enumerate(queue[:6]):
    print(f"  {i+1}. {e}")
