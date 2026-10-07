import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

new_emails = [
    # 1. Equirus
    "rituraj.chaudhari@equirusasset.com",

    # 2. Adani Strategic, Tech, Media & Infrastructure Desks
    "cto.office@adani.com",
    "procurement@adani.com",
    "mukund.seetharaman@adani.com",
    "sudhir.mattoo@adani.com",
    "anurag.varma@adani.com",
    "anup.dutta@adani.com",
    "parinita.duggal@adani.com",
    "investor.relations@ndtv.com",
    "malay.mahadevia@adani.com",
    "sudhir.d@adani.com",
    "shashi.shanker@adani.com",
    "vneet.jaain@adani.com",
    "samir.prakash@adani.com",
    "anant.sethi@adani.com",
    "himanshu.bhardwaj@adani.com",
    "samir.mishra@adani.com",

    # 3. Adani Family & Core Leadership
    "gautam.adani@adani.com",
    "priti.adani@adani.com",
    "rajesh.adani@adani.com",
    "vinod.adani@adani.com",
    "mahasukh.adani@adani.com",
    "karan.adani@adani.com",
    "jeet.adani@adani.com",
    "pranav.adani@adani.com",
    "sagar.adani@adani.com",
    "amankumar.singh@adani.com",
    "arun.bansal@adani.com",
    "ashish.rajvanshi@adani.com",
    "shersingh.khyalia@adani.com",
    "ashish.khanna@adani.com",
    "jatin.jalundhwala@adani.com",
    "samir.vora@adani.com",
    "sanjay.behl@adani.com",

    # 4. Adani CFOs, KMPs, Sector Heads & Desks
    "sreedhar.menon@adani.com",
    "saurabh.shah@adani.com",
    "rajesh.poddar@adani.com",
    "kamlesh.bhagia@adani.com",
    "pragnesh.darji@adani.com",
    "jeyakumar.janakaraj@adani.com",
    "thibault.lesueur@adani.com",
    "jayant.parimal@adani.com",
    "amit.grover@adani.com",
    "suchit.bansal@adani.com",
    "manojkumar.sharma@adani.com",
    "investor.ael@adani.com",
    "investor.apsezl@adani.com",
    "investor.agel@adani.com",
    "investor.apl@adani.com",
    "investor.atgl@adani.com",
    "investor.aesl@adani.com",

    # 5. Micro Labs Board of Directors
    "dilipsurana@microlabs.in",
    "dilip.surana@microlabsltd.com",
    "anandsurana@microlabs.in",
    "anand.surana@microlabsltd.com",
    "rajeshkshirsagar@microlabs.in",
    "rajesh.kshirsagar@microlabsltd.com",
    "ashokjain@microlabs.in",
    "ashok.jain@microlabsltd.com",
    "gramabalaji@microlabs.in",
    "balaji.gs@microlabsltd.com",
    "vijayshah@microlabs.in",
    "vijay.shah@microlabsltd.com",
    "pinkyjain@microlabs.in",
    "pinky.jain@microlabsltd.com",
    "ganeshanc@microlabs.in",
    "c.ganeshan@microlabsltd.com",

    # 6. Aditya Birla Group / Svatantra
    "a.birla@svatantra.adityabirla.com",
    "ananya.birla@adityabirla.com",
    "ananya.birla@hindalco.com"
]

queue_file = "data/all_unsent_emails.json"

with open(queue_file, "r", encoding="utf-8") as f:
    queue = json.load(f)

print(f"Current unsent queue count: {len(queue)}")
existing_set = set(e.lower().strip() for e in queue if isinstance(e, str))

to_add = []
seen_in_batch = set()

for em in new_emails:
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
