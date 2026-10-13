import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

new_titans = [
    # 1. JSW Group
    "sajjan.jindal@jsw.in",
    "sangita.jindal@jsw.in",
    "parth.jindal@jsw.in",
    "jayant.acharya@jsw.in",
    "sharad.mahendra@jsw.in",
    "seshagiri.rao@jsw.in",
    "gajraj.rathore@jsw.in",
    "swayam.saurabh@jsw.in",
    "jswsteel.investor@jsw.in",
    "investor.relations@jsw.in",

    # 2. Mahindra Group
    "mahindra.anand@mahindra.com",
    "shah.anish@mahindra.com",
    "jejurikar.rajesh@mahindra.com",
    "barua.amarjyoti@mahindra.com",
    "gurnani.cp@mahindra.com",
    "joshi.mohit@techmahindra.com",
    "bhat.manoj@mahindra.com",
    "rebello.raul@mahindra.com",
    "investor.relations@mahindra.com",

    # 3. Aditya Birla Group
    "kumar.birla@adityabirla.com",
    "ananya.birla@adityabirla.com",
    "aryaman.birla@adityabirla.com",
    "rajashree.birla@adityabirla.com",
    "himanshu.kapania@adityabirla.com",
    "satish.pai@adityabirla.com",
    "kc.jhanwar@adityabirla.com",
    "sandeep.kataria@adityabirla.com",
    "vishak.kumar@adityabirla.com",
    "abg.feedback@adityabirla.com",

    # 4. Reliance Industries Limited (RIL) & Jio
    "mukesh.ambani@ril.com",
    "nita.ambani@ril.com",
    "akash.ambani@jio.com",
    "isha.ambani@ril.com",
    "anant.ambani@ril.com",
    "nikhil.meswani@ril.com",
    "hital.meswani@ril.com",
    "srikanth.venkatachari@ril.com",
    "pms.prasad@ril.com",
    "pankaj.pawar@jio.com",
    "v.subramaniam@ril.com",
    "kv.kamath@ril.com",
    "investor.relations@ril.com",

    # 5. Torrent Group
    "samirmehta@torrentpharma.com",
    "sudhirmehta@torrentpharma.com",
    "amanmehta@torrentpharma.com",
    "jinal.mehta@torrentpower.com",
    "varun.mehta@torrentpower.com",
    "sanjaydalal@torrentpharma.com",
    "saurabh.mashruwala@torrentpower.com",
    "rahul.shah@torrentpower.com",
    "investors@torrentpharma.com",
    "investors@torrentpower.com"
]

queue_file = "data/all_unsent_emails.json"

with open(queue_file, "r", encoding="utf-8") as f:
    queue = json.load(f)

print(f"Current unsent queue count: {len(queue)}")
existing_set = set(e.lower().strip() for e in queue if isinstance(e, str))

to_add = []
seen_in_batch = set()

for em in new_titans:
    em_clean = em.lower().strip()
    if em_clean in seen_in_batch:
        continue
    seen_in_batch.add(em_clean)
    
    if em_clean in existing_set:
        print(f"Moving to front: {em_clean}")
        queue = [x for x in queue if x.lower().strip() != em_clean]
    else:
        print(f"Adding new: {em_clean}")
    to_add.append(em_clean)

queue = to_add + queue

with open(queue_file, "w", encoding="utf-8") as f:
    json.dump(queue, f, indent=2)

print(f"\nUpdated queue! Added {len(to_add)} emails to the front.")
print(f"New queue count: {len(queue)}")
print("Front 10 of queue:")
for i, e in enumerate(queue[:10]):
    print(f"  {i+1}. {e}")
