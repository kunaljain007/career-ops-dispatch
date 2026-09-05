# -*- coding: utf-8 -*-
import json, smtplib, time, os, sys, random, re
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

# Running directory relative paths (Works on GitHub Actions Linux VM AND Windows seamlessly)
BASE_DIR    = os.path.dirname(os.path.abspath(__file__))
DATA_DIR    = os.path.join(BASE_DIR, "data")
LOGS_DIR    = os.path.join(DATA_DIR, "logs")

SMTP_FILE   = os.path.join(DATA_DIR, "smtp_pool.json")
QUEUE_FILE  = os.path.join(DATA_DIR, "all_unsent_emails.json")
MASTER_SENT = os.path.join(LOGS_DIR, "master_all_sent.json")

_DATE_TAG   = datetime.now().strftime("%b%d").lower()
LOG_FILE    = os.path.join(LOGS_DIR, f"dispatch_{_DATE_TAG}_sent.json")
FAIL_FILE   = os.path.join(LOGS_DIR, f"dispatch_{_DATE_TAG}_failed.json")

os.makedirs(LOGS_DIR, exist_ok=True)

MAX_PER_SMTP = 80

RAW_PRIORITY = [
    "wgriffiths@lexingtonpartners.com", "dominique.senequier@ardian.com",
    "phealy@hf.com", "ddeb@franciscopartners.com", "brian.guthrie@trs.texas.gov",
    "atucker@sib.wa.gov", "thomas.lee@nystrs.org", "clichnock@calstrs.com",
    "doug.ostrover@blueowl.com", "hmarks@oaktreecapital.com",
    "christina.tan@hengxin.com.sg", "egon.durban@silverlake.com",
    "rsmith@vistaequitypartners.com", "lzhang@hillhousecap.com",
    "kurt.bjorklund@permira.com", "stuart.mcalpine@cinven.com",
    "rhastings@netflix.org", "eline@moveenergy.vc", "Aaron.Appelhanz@ADM.com",
    "rajeevranjan.kushwaha@gov.in", "Ginger.McKinney@ADM.com",
    "elevate-ktech@ka.gov.in", "hackathon.nihr@gov.in",
    "support@nato-diana.org", "makeit@hax.co", "info@greenhouseaccelerator.com",
    "build@temple.com", "d@zomato.com", "deepinder@zomato.com",
    "akshant.goyal@zomato.com", "vss@paytm.com", "vijay@paytm.com",
    "kunal.shah@cred.club", "abhirajbhal@urbancompany.com", "varun@honasa.in",
    "raj@houseofx.nyc", "raj@figuringout.co", "rajshamani29@gmail.com",
    "rema@ankurcapital.com", "krishnan@ankurcapital.com", "shiva@ankurcapital.com",
    "amaan@ankurcapital.com", "vishesh.rajaram@specialeinvest.com",
    "arjun.rao@specialeinvest.com", "anjali@avaanacapital.com",
    "vatsal@avaanacapital.com", "srishti@avaanacapital.com",
    "mark@omnivore.vc", "jinesh@omnivore.vc", "reihem@omnivore.vc",
    "kunal@infuseventures.in", "pranav@3one4capital.com",
    "shivank@aavishkaar.in", "sandip.herlekar@eversourcecapital.com",
    "manish@cie.co", "vikram@ivycapventures.com", "padmaja@indianangelnetwork.com",
    "vinod@khoslaventures.com", "keith@khoslaventures.com",
    "chris@lowercarboncapital.com", "chris@lowercarbon.com", "clea@lowercarbon.com",
    "maddison@climatecap.co", "sundeep@climatecap.co",
    "gabriel@preludeventures.com", "tim@preludeventures.com",
    "markus@carbondrawdown.co",
    "carmichael@breakthroughenergy.org", "rodi@breakthroughenergy.org",
    "david@breakthroughenergy.org", "eric@breakthroughenergy.org",
    "sean@sosv.com", "tom@atoneventures.com",
    "reddy@energyimpactpartners.com", "brendan@fifthwall.com",
    "veery@galvanizeclimate.com", "hbranz@galvanizeclimate.com",
    "rachel@dcvc.com", "matt@dcvc.com", "phil@xorainnovation.com",
    "ira@dblpartners.com", "nancy@dblpartners.com",
    "katie@engine.xyz", "pitches@engine.xyz",
    "danijel@worldfund.vc", "renesavelsberg@setventures.com",
    "stefan@aenu.vc", "mkovacs@solas-capital.com",
    "gdarrah@systemiqcapital.earth", "pe.franc@hy24partners.com",
    "tim@gforce.vc", "lucy@extantia.com", "yair@extantia.com",
    "peter@foundersfund.com", "trae@foundersfund.com",
    "roelof@sequoia.com", "douglas@sequoia.com", "alfred@sequoia.com",
    "pat@sequoia.com", "shaun@sequoia.com", "bryan@sequoia.com",
    "garry@ycombinator.com", "pg@ycombinator.com",
    "ben@a16z.com", "marc@a16z.com",
    "eric@benchmark.com", "sarah@benchmark.com", "miles@benchmark.com",
    "mamoon@kleinerperkins.com", "jdoerr@kleinerperkins.com",
    "ravi@lsvp.com", "steve@foundationcap.com", "luke@gigafund.com",
    "hemant@generalcatalyst.com", "lior@eclipse.vc",
    "brad@altimeter.com", "josh@thrivecap.com",
    "mmurphy@menloventures.com", "sacks@craftventures.com", "jeff@craftventures.com",
    "gavin@atreidesmgmt.com", "lee@addition.com",
    "chase@tigerglobal.com", "scott@tigerglobal.com",
    "naval@co-found.com", "naval@angellist.com",
    "obravo@thomabravo.com", "scott@highalpha.com",
    "gurley@benchmark.com", "nchaddha@mayfield.com", "rbatra@mayfield.com",
    "ping@redpoint.com", "sraney@redpoint.com",
    "blake@byerscapital.com", "aydin@felicis.com",
    "vas@accel.com", "ryan@accel.com", "neeraj@battery.com",
    "rajat@matrixpartners.in", "tarun@matrixpartners.in", "avnish@matrixpartners.in",
    "samir@venturehighway.vc", "ninad@100x.vc", "usomani@gmail.com",
    "devendra@dexterangels.com", "ashish@innovencapital.com",
    "vinod@alteriacapital.com", "siddharth@3one4capital.com",
    "nshah@nvp.com", "kanwal@firesideventures.com",
    "prashanth@accel.com", "subrata@accel.com", "anand@accel.com",
    "sandeep@lightbox.vc", "siddharth@lightbox.vc",
    "kartik@jumpstart.vc", "anirudh@artha.vc", "sanjay@mehtaventures.com",
    "martin@indexventures.com", "shardul@indexventures.com",
    "danny@indexventures.com", "jan@indexventures.com",
    "pawel@pointnine.com", "luciana@sequoia.com",
    "avi@entreecap.com", "saul@phoenixcourt.vc",
    "reshma@seedcamp.com", "carlos@seedcamp.com",
    "klaus.hommels@lakestar.com", "niklas.zennstrom@atomico.com",
    "hiro.tamura@atomico.com",
    "climatepledgefund@amazon.com", "khurst@amazon.com",
    "geert.vandewouw@shell.com", "didier.holleaux@engie.com",
    "julius.tan@genzero.co", "pitches@regeneration.vc",
    "info@closedlooppartners.com", "info@g2vp.com", "proposals@gv.com",
    "ventures@qualcomm.com", "info@sony-innovation-fund.com",
    "tdk.ventures@tdk.com", "intelcapital@intel.com",
    "contact@steadview.com", "investor@infoedge.in", "audit@zerodha.com",
    "proposals@iqt.org", "pitches@shieldcapital.com",
    "info@helsing.ai", "pitches@marqueventures.com",
    "tlc@temasekfoundation.org.sg", "info@theliveabilitychallenge.org",
    "kirsten.dunlop@climate-kic.org", "proposals@climate-kic.org",
    "grants@climatechange.ai", "paul@conservationxlabs.org",
    "amangla@cisco.com", "contact@mitigation-action-facility.org",
    "grants@climateworks.org", "climate@docsociety.org",
    "sgp.info@undp.org", "contact@c40.org",
    "decks@climentum.vc", "idex-ddp@gov.in", "sbir@darpa.mil",
    "proposals@natofund.vc", "info@sirius-hub.com",
    "info@earthshotprize.org", "info@xprize.org",
    "info@calseed.fund", "decks@vireo.vc",
    "secretariat@unfccc.int", "W.Huang@iaea.org", "H.Paillere@iaea.org",
    "gernot.laganda@wfp.org", "climateliteracytraining@gmail.com",
    "m.haigh@soas.ac.uk", "info@adia.ae", "info@qia.qa",
    "info@cppib.com", "tvg@otpp.com",
    "strategic.communications@temasek.com.sg", "info@temasek.com.sg",
    "info@gic.com.sg", "info@mubadala.ae", "info@pif.gov.sa",
    "mrbeast@night.co", "pewdiepie@opg.tv", "pokimane@night.co",
    "marques@mkbhd.com", "markiplierbusiness@gmail.com",
    "linus@linusmediagroup.com", "casey@neistat.com",
    "business@mrwhosetheboss.me", "loganpaul@night.co",
    "jake.paul@nakisatg.com", "daviddobrikbusiness@gmail.com",
    "info@kingstudio.co", "business@carryminati.com",
    "bhuvan.bam@bbkivines.in", "connect@ankurwarikoo.com",
    "sharan@financewithsharan.com", "business@technicalguruji.in",
    "contact.avneetk@gmail.com", "ashishchanchlanivines@gmail.com",
    "info@cornerstone.in", "rohit.sharma@riseaworld.com",
    "hardik.pandya@riseaworld.com", "contact@collectiveartists.com",
    "alia.bhatt@matrixindia.in", "info@sevenbucks.com",
    "info@maximumeffort.com", "info@springhillco.com",
    "info@wmeagency.com", "info@cr7unscripted.com",
    "info@leomessi.com", "arr@rahmanmusic.com",
    "patrick@stripe.com", "john@stripe.com", "vitalik@ethereum.org",
    "daniel@spotify.com", "brian.chesky@airbnb.com", "christian@ecosia.org",
    "k.krithivasan@tcs.com", "puneet.chhatwal@ihcltata.com",
    "tv.narendran@tatasteel.com", "aathreya@tejasnetworks.com",
    "p.venkatesalu@trent-tata.com", "sunil.dsouza@tataconsumer.com",
    "praveer.sinha@tatapower.com", "manoj.raghavan@tataelxsi.co.in",
    "pradeepbakshi@voltas.com", "girish.wagh@tatamotors.com",
    "ckvenkat@titan.co.in", "rmukundan@tatachemicals.com",
    "as.lakshminarayanan@tatacommunications.com",
    "warren.harris@tatatechnologies.com", "pjnath@nelco.in",
    "adalal@tata.com", "gyanendra.shukla@rallis.com",
    "pranjan@orientalhotels.co.in", "uksingh@trf.co.in", "pghosh@acglgoa.com",
    "debra.crew@diageo.com", "andrew.fell@diageo.com",
    "michel.doukeris@ab-inbev.com", "jan.craps@budweiserapac.com",
    "dolf.vandenbrink@heineken.com", "stacey.tank@heineken.com",
    "alexandre.ricard@pernod-ricard.com", "mariapia.decaro@pernod-ricard.com",
    "gavin.hattersley@molsoncoors.com", "bill.newlands@cbrands.com",
    "jacob.aarup-andersen@carlsberg.com", "a.katsuki@asahigroup-holdings.com",
    "lawson_whiting@b-f.com", "mmadhavan@bacardi.com",
    "jquincey@coca-cola.com", "bperez@coca-cola.com",
    "ramon.laguarta@pepsico.com", "jim.andrew@pepsico.com",
    "tim.cofer@kdrp.com", "takeshi_niinami@suntory.co.jp",
    "oliver.mintzlaff@redbull.com", "rsacks@monsterenergy.com",
    "tim@fever-tree.com", "laurent.freixe@nestle.com",
    "antonia.wanner@nestle.com", "hein.schumacher@unilever.com",
    "michael.stewart@unilever.com", "moeller.jr@pg.com",
    "helias.v@pg.com", "nicolas.hieronimus@loreal.com",
    "dirkvandeput@mdlz.com", "antoine.desaintaffrique@danone.com",
    "poul.weihrauch@effem.com", "jeffrey.harmening@genmills.com",
    "carlos.abrams-rivera@kraftheinz.com", "ffreda@estee.com",
    "noel_wallace@colgpal.com", "steve.cahillane@kellanova.com",
    "rohit.jawa@unilever.com", "sanjiv.puri@itc.in",
    "p.schaus@lvmh.com", "greg.hughes@suntory.com",
    "matteo.fantacchiotti@campari.com", "soren.hagh@wgrant.com",
    "eric.vallat@remy-cointreau.com", "ernest.gallo@ejgallo.com",
    "eguilisasti@conchaytoro.cl", "tim.ford@tweglobal.com",
    "michael.spillane@bostonbeer.com", "brian.niccol@starbucks.com",
    "luc.vandevelde@jdepeets.com", "mdeleo@oceanspray.com",
    "ncaporella@nationalbeverage.com", "simon.litherland@britvic.com",
    "d-honjo@itoen.co.jp", "michael.hsu@kcc.com",
    "tmongon@kenvue.com", "kris.licht@reckitt.com",
    "carsten.knobel@henkel.com", "y-hasebe@kao.co.jp",
    "k-fujiwara@shiseido.co.jp", "sean.connolly@conagra.com",
    "mark_clouse@campbellsoup.com", "mbuck@hersheys.com",
    "lapo.civiletti@ferrero.com", "clopez@chiquita.com",
    "david.murdock@dole.com", "doug.mcmillon@walmart.com",
    "rvachris@costco.com", "brian.cornell@target.com",
    "alexandre_bompard@carrefour.com", "ken.murphy@tesco.com",
    "alechner@lindt.com", "peter_feld@barry-callebaut.com",
    "george.weston@abf.co.uk", "claudio.colzani@barilla.com",
    "albert.christmann@oetker.com", "taro_fujie@ajinomoto.com",
    "miles.hurrell@fonterra.com", "peder.tuborgh@arlafoods.com",
    "janderck.vankarnebeek@frieslandcampina.com", "pat.sly@reckitt.com",
    "jacek.olczak@pmi.com", "tadeu_marroco@bat.com",
    "masamichi.terahat@jti.com", "stefan.bomhard@impbrands.com",
    "juan.luciano@adm.com", "greg.heckman@bunge.com",
    "brian_sikes@cargill.com", "michael.gelchie@ldc.com",
    "chairman@tata.com", "info@tata.com", "noel.tata@tata.com",
    "anant.ambani@reliance.com", "gburman@burmanfh.com",
    "agupta@burmanfh.com", "jsangwan@burmanfh.com", "anand.burman@dabur.com",
    "anna.ohlsson-baskerville@unilever.com",
    "deepak@catamaran.in", "deepak.padaki@sxc.com", "sheetal@catamaran.in",
    "sudipto@catamaran.in", "udit@catamaran.in", "chirag@catamaran.in",
    "rounak@catamaran.in", "karthik@catamaran.in",
    "akash.ambani@ril.com", "piramales@gmail.com",
    "lakshmi.mittal@arcelormittal.com", "yuvraj.singh@youwecan.org",
    "harish.manwani@tata.com", "anita.george@tata.com",
    "venu.srinivasan@tata.com", "vs@tvsmotor.com",
    "siddharth.sharma@tatatrusts.org", "ssharma@tatatrusts.org",
    "vijay.singh@tatatrusts.org", "vijay.singh@tata.com",
    "darius.khambata@tata.com", "mehli.mistry@tata.com",
    "jimmy.tata@tata.com", "kevinkwilinski@berryglobal.com",
    "investorrelations@berryglobal.com", "info@danoneventures.com",
    "edmond.scanlon@kerry.com", "jayenmehta@amul.coop",
    "gcmmf@amul.coop", "devendra.shah@parag.com",
    "investors@paragmilkfoods.com", "leah.tata@tata.com",
    "leah.tata@trent-tata.com", "maya.tata@tata.com", "maya.tata@tatadigital.com",
    "ajoyendra.mukherjee@tatatechnologies.com", "warren.harris@tatatechnologies.com",
    "ng.subramaniam@tatacommunications.com"
]

sent_history = set()
if os.path.exists(MASTER_SENT):
    try:
        with open(MASTER_SENT, "r", encoding="utf-8") as f:
            for item in json.load(f):
                if isinstance(item, str):
                    sent_history.add(item.strip().lower())
                elif isinstance(item, dict):
                    e = (item.get("to") or item.get("email") or "").strip().lower()
                    if e:
                        sent_history.add(e)
    except:
        pass

if os.path.exists(LOG_FILE):
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            for item in json.load(f):
                if isinstance(item, dict) and "to" in item:
                    sent_history.add(item["to"].strip().lower())
    except:
        pass

print(f"Master sent history: {len(sent_history)} already sent")

with open(SMTP_FILE, "r", encoding="utf-8") as f:
    smtp_pool = json.load(f)

queue_emails = []
if os.path.exists(QUEUE_FILE):
    try:
        with open(QUEUE_FILE, "r", encoding="utf-8") as f:
            for item in json.load(f):
                if isinstance(item, str) and "@" in item:
                    queue_emails.append(item.strip().lower())
    except:
        pass

all_pending = []
seen = set(sent_history)
BLACKLIST_DOMAINS = ["godrejagrotech", "godrejagrovet", "godrejagro", "3one4capital", "3one4caoital"]

def is_blacklisted(email):
    email_lower = email.lower()
    return any(b in email_lower for b in BLACKLIST_DOMAINS)

for e in RAW_PRIORITY:
    e_clean = e.strip().lower()
    if "@" in e_clean and e_clean not in seen and not is_blacklisted(e_clean):
        seen.add(e_clean)
        all_pending.append(e_clean)

for e in queue_emails:
    e_clean = e.strip().lower()
    if "@" in e_clean and e_clean not in seen and not is_blacklisted(e_clean):
        seen.add(e_clean)
        all_pending.append(e_clean)

total_target_cap = MAX_PER_SMTP * len(smtp_pool)
today_batch = all_pending[:total_target_cap]
remaining_queue = all_pending[total_target_cap:]

print(f"Active SMTPs: {len(smtp_pool)} | Target: {len(today_batch)} | Remaining: {len(remaining_queue)}")

with open(QUEUE_FILE, "w", encoding="utf-8") as f:
    json.dump(remaining_queue, f, indent=2)

from send_heatbolt_emails import build_html_body, build_plain_body, SUBJECT

REPLY_TO = "founder.heatbolt@gmail.com"
CC       = "team.heatbolt@gmail.com"

def send_one(smtp_user, smtp_pass, to_addr):
    msg = MIMEMultipart("alternative")
    msg["Subject"]    = SUBJECT
    msg["From"]       = smtp_user
    msg["To"]         = to_addr
    msg["CC"]         = CC
    msg["Reply-To"]   = REPLY_TO
    msg["X-Priority"] = "1"
    msg["Importance"] = "High"
    
    name_clean = to_addr.split("@")[0].replace(".", " ").replace("_", " ").replace("-", " ").title()
    plain = build_plain_body(name_clean, name_clean, "Your Organization", "Executive Leadership", "global_pe")
    html  = build_html_body(name_clean, name_clean, "Your Organization", "Executive Leadership", "global_pe")
    
    msg.attach(MIMEText(plain, "plain"))
    msg.attach(MIMEText(html, "html"))
    
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=25) as s:
        s.login(smtp_user, smtp_pass)
        s.sendmail(smtp_user, [to_addr, CC], msg.as_string())

sent_records = []
if os.path.exists(LOG_FILE):
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            sent_records = json.load(f)
    except:
        sent_records = []

failed_records = []
smtp_usage = [0] * len(smtp_pool)
current_smtp_idx = 0

for idx, target_email in enumerate(today_batch, 1):
    tries = 0
    while smtp_usage[current_smtp_idx] >= MAX_PER_SMTP and tries < len(smtp_pool):
        current_smtp_idx = (current_smtp_idx + 1) % len(smtp_pool)
        tries += 1
    
    if tries >= len(smtp_pool):
        print("All SMTP accounts reached daily cap!")
        leftovers = today_batch[idx-1:] + remaining_queue
        with open(QUEUE_FILE, "w", encoding="utf-8") as f:
            json.dump(leftovers, f, indent=2)
        break
    
    acc = smtp_pool[current_smtp_idx]
    user = acc["user"]
    pwd  = acc["pass"]
    
    try:
        send_one(user, pwd, target_email)
        smtp_usage[current_smtp_idx] += 1
        rec = {"to": target_email, "from": user, "timestamp": datetime.now().isoformat(), "status": "SENT"}
        sent_records.append(rec)
        print(f"[{idx:4d}/{len(today_batch)}] SENT -> {target_email:<40} (via {user.split('@')[0]} | {smtp_usage[current_smtp_idx]}/{MAX_PER_SMTP})", flush=True)
        
        with open(LOG_FILE, "w", encoding="utf-8") as f:
            json.dump(sent_records, f, indent=2)
        
        master_list = []
        if os.path.exists(MASTER_SENT):
            try:
                with open(MASTER_SENT, "r", encoding="utf-8") as f:
                    master_list = json.load(f)
            except:
                master_list = []
        master_list.append(target_email)
        with open(MASTER_SENT, "w", encoding="utf-8") as f:
            json.dump(master_list, f)
            
    except Exception as ex:
        print(f"[{idx:4d}/{len(today_batch)}] FAIL -> {target_email} | Error: {ex}", flush=True)
        failed_records.append({"to": target_email, "from": user, "error": str(ex), "timestamp": datetime.now().isoformat()})
        with open(FAIL_FILE, "w", encoding="utf-8") as f:
            json.dump(failed_records, f, indent=2)
    
    current_smtp_idx = (current_smtp_idx + 1) % len(smtp_pool)
    delay = random.uniform(8, 12)
    time.sleep(delay)

print(f"Job finished. Successfully sent: {len(sent_records)}, Failed: {len(failed_records)}")
