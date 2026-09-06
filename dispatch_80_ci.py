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
FOLLOWUP_TRACKER = os.path.join(DATA_DIR, "followup_tracker.json")

os.makedirs(LOGS_DIR, exist_ok=True)

MAX_PER_SMTP = 80

RAW_PRIORITY = [
    "info@alokozay.com",
    "contact@cevital.com",
    "geral@refriango.com",
    "info@brandy.am",
    "info@azersun.com",
    "info@bmmi.com.bh",
    "cr@prangroup.com",
    "marketing@santabremor.com",
    "info@dhi.bt",
    "info@lidl.bg",
    "info@cambrew.com.kh",
    "contact.sabc@castel-afrique.com",
    "podravka@podravka.hr",
    "info@charalambideschristis.com.cy",
    "info.bralima@heineken.com",
    "banks@banksdih.com",
    "wisyncoir@wisynco.com",
    "info.bralirwa@heineken.com",
    "info@dahabshiil.com",
    "kellanovashareholders@kellanova.com",
    "ir@henkel.com",
    "investorrelations@adm.com",
    "investor.relations@beiersdorf.com",
    "investor.relations@churchdwight.com",
    "investorrelations@clorox.com",
    "investorrelations@estee.com",
    "ir@tyson.com",
    "investorrelations@hain.com",
    "ir.dept@jmsmucker.com",
    "ir@grupobimbo.com",
    "input.ir@pernod-ricard.com",
    "investor.relations@diageo.com",
    "ri@natura.net",
    "investorrelations@herbalife.com",
    "ir@conagra.com",
    "ir@jbs.com.br",
    "investor@carlsberg.com",
    "investorrelations@cbrands.com",
    "investor.relations@molsoncoors.com",
    "investor.relations@grupolala.com",
    "shareholder.services@unilever.com",
    "ir@nestle.com",
    "shareholderservices@coca-cola.com",
    "pepsicoinvestorrelations@pepsico.com",
    "ir@kraftheinz.com",
    "ir@mdlz.com",
    "investor_relations@colpal.com",
    "kc.investorrelations@kcc.com",
    "ir@reckitt.com",
    "investor.relations@danone.com",
    "consumercenter@cpf.co.th",
    "ir@masterkong.com.cn",
    "membership@landolakes.com",
    "investorrelations@treehousefoods.com",
    "corporate.communications@univarsolutions.com",
    "investorrelations@sealedair.com",
    "ri@marfrig.com.br",
    "irprib@pilgrims.com",
    "ir@wilmar.com.sg",
    "ir@thaiunion.com",
    "investor.relations@mosaicco.com",
    "ir@yara.com",
    "corporate.communications@nufarm.com",
    "fmcir@fmc.com",
    "investor.relations@tateandlyle.com",
    "ir@symrise.com",
    "investor.relations@lonza.com",
    "corporate.communications@syngentagroup.com",
    "csc@pidilite.com",
    "ranjana@bhaat.in",
    "renu@q49.in",
    "info@q49.in",
    "sunil.dsouza@tataconsumer.com", "investor.relations@tataconsumer.com",
    "sudarshan.maiya@maiyas.in", "info@maiyas.in",
    "sanjay.sharma@mtrfoods.com", "feedback@mtrfoods.com",
    "deepak.agarwal@bikaji.com", "investor.relations@bikaji.com",
    "ss.aggarwal@bikanervala.com", "info@bikanervala.com",
    "jayenmehta@amul.coop", "gcmmf@amul.coop",
    "oliver.mirza@oetker.in", "service@oetker.in",
    "ahsan.chowdhury@prangroup.com", "crd@prangroup.com",
    "saugata.gupta@marico.com", "investor@marico.com",
    "anand.khurana@genmills.com", "genmills.india@genmills.com",
    "suresh.narayanan@nestle.com", "consumer.services@nestle.com",
    "bimal@adf-foods.com", "info@adf-foods.com",
    "milan.patel@isconbalajifoods.com", "info@isconbalajifoods.com",
    "sagar@wowmomo.com", "info@wowmomo.co.in",
    "musthafa@idfreshfood.com", "info@idfreshfood.com", "evelyn@idfreshfood.com",
    "sameer.khetarpal@jublfood.com", "investor@jublfood.com",
    "bharat@yufoodlabs.com", "contact@yufoodlabs.com",
    "kartik@thetastecompany.com", "info@thetastecompany.com",
    "meghana@slurrpfarm.com", "wholesome@slurrpfarm.com",
    "nakul@mommymadeit.in", "care@mommymadeit.in",
    "viraj@veeba.in", "hello@veeba.in", "info@veeba.in",
    "abhay@licious.in", "talktous@licious.in",
    "gaurav.sharma@tastybite.com", "info@tastybite.com",
    "prasannakumar.b@venkys.com", "info@venkys.com",
    "jaydeep.barman@rebelfoods.com", "crm@rebelfoods.com",
    "lisa@prasuma.com", "contact@prasuma.com",
    "sahil.gilani@gitsfood.com", "gits@gitsfood.com",
    "sairaj@wakaofoods.com", "franchise@wakaoworld.com",
    "arun@nutriquofoods.com", "info@nutriquofoods.com",
    "ravi@currygram.in", "contact@currygram.in",
    "vibhuti@pisharodyfoods.com", "info@pisharodyfoods.com",
    "vasanth@expressfeast.com", "care@expressfeast.com",
    "ajay.gupta@capitalfoods.co.in", "customercare@capitalfoods.co.in",
    "manish.bandlish@motherdairy.com", "consumer.care@motherdairy.com",
    "dipak.sanghavi@nilons.com", "info@nilons.com",
    "sanjay.desai@mothersrecipe.com", "customercare@mothersrecipe.com",
    "parag.desai@waghbakritea.com", "feedback@waghbakritea.com",
    "anurag@bhaat.in", "connect@bhaat.in",
    "iqbal.fazlani@fazlanifoods.com", "info@fazlanifoods.com",
    "mithun.appaiah@sumeru.net", "info@sumeru.net",
    "rajesh@handibazar.com", "info@handibazar.com",
    "mohit.malhotra@dabur.com", "corpcomm@dabur.com",
    "balkrishna@patanjaliayurved.org", "feedback@patanjaliayurved.org",
    "kedar@chitalebandhu.in", "info@chitalebandhu.in",
    "ck.ranganathan@cavinkare.com", "corporate@cavinkare.com",
    "chandu.virani@balajiwafers.com", "info@balajiwafers.com",
    "nitin.patel@sakarfoods.com", "info@sakarfoods.com",
    "anjan.chowdhury@squaregroup.com", "sfbl@squaregroup.com",
    "shamim.uddin@akij.net", "info.afbl@akij.net",
    "syed.alamgir@aci-bd.com", "info@aci-bd.com",
    "mubarak.ali@olympicbd.com", "info@olympicbd.com",
    "padmasingh.isaac@aachifoods.com", "care@aachifoods.com",
    "radhakrishnan@trigunifood.com", "info@ezeeats.com",
    "kiran.cherukuri@priyafoods.com", "info@priyafoods.com",
    "shirisha.myadam@bambinoagro.com", "corporate@bambinoagro.com",
    "nitin.arora@veerfoods.com", "info@veerfoods.com",
    "piyush.pattnaik@mccain.com", "mccain.india@mccain.com",
    "alliances@shimlared.com", "info@shimlared.com",
    "india.sales@kerry.com", "info@kerry.com",
    "sourcing.india@newlywedsfoods.com", "info@newlywedsfoods.com",
    "india.info@bunge.com",
    "ankit.agarwal@veeba.in", "somesh.chaudhary@veeba.in", "rahul.chadha@veeba.in",
    "sunit.jha@nilons.net",
    "sanjana.desai@mothersrecipe.com",
    "s.nemani@vimalagro.com", "info@vimalagro.com",
    "rajashekar.seelam@srestaorganic.com", "investorrelations@srestaorganic.com", "renuka@24mantra.com",
    "alliances@cygnetfoods.com", "info@cygnetfoods.com",
    "shyamm.mariwala@marsonbiocare.com", "corporate@marsonbiocare.com",
    "bipin.hadhwani@gopalfoods.com", "info@gopalenterprise.com",
    "vishal.chordia@suhana.co.in", "customercare@suhana.co.in",
    "procurement@vlcspices.com", "info@vlcspices.com",
    "balaji.rao@venkys.org", "response@venkys.com", "corp.sec@venkys.com",
    "satnam.arora@kohinoorfoods.in", "info@kohinoorfoods.in",
    "angshu.mallick@adaniwilmar.in", "customercare@adaniwilmar.in",
    "varunberry@britannia.co.in", "procurement.ho@britannia.co.in",
    "tarun.arora@zyduswellness.com", "customercare@zyduswellness.com",
    "asheesh.sharma@atfoods.com", "atflltd@atfoods.com",
    "neeraj@paperboatfoods.com", "hello@paperboatfoods.com",
    "parag.bhattacharyya@rebelfoods.com",
    "naveen.srivastava@jublfood.com",
    "orklaindia.ipo@citi.com",
    "vijay.chauhan@parle.biz", "customercare@parle.biz",
    "kamal.agrawal@haldirams.com", "info@haldiram.com",
    "sourcing@jasperfoods.com", "info@jasperfoods.com",
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
BLACKLIST_DOMAINS = [
    "godrej", "godrejinds", "godrejagrotech", "godrejagrovet", "godrejagro",
    "itc.in", "itcportal",
    "barilla", "barilla.com",
    "3one4capital", "3one4caoital"
]

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

# Load Followup Tracker
followup_tracker = {}
if os.path.exists(FOLLOWUP_TRACKER):
    try:
        with open(FOLLOWUP_TRACKER, "r", encoding="utf-8") as f:
            followup_tracker = json.load(f)
    except Exception as ex:
        print(f"Followup tracker read error: {ex}", flush=True)

# Identify due follow-ups (Initial pitch sent >= 4 days ago, sequence < 2)
due_followups = []
now_dt = datetime.now()
for email_addr, f_info in list(followup_tracker.items()):
    if is_blacklisted(email_addr):
        continue
    try:
        last_dt = datetime.fromisoformat(f_info.get("last_sent", "2000-01-01T00:00:00"))
        seq = f_info.get("seq", 1)
        days_passed = (now_dt - last_dt).total_seconds() / 86400.0
        if seq == 1 and days_passed >= 4.0:
            due_followups.append((email_addr, 2))
        elif seq == 2 and days_passed >= 7.0:
            due_followups.append((email_addr, 3))
    except Exception:
        pass

print(f"Due follow-ups ready: {len(due_followups)}", flush=True)

total_target_cap = MAX_PER_SMTP * len(smtp_pool)

# Reserve up to 20% of daily capacity for due follow-ups, fill the rest with fresh leads
max_followups_today = min(len(due_followups), int(total_target_cap * 0.20))
today_followup_batch = due_followups[:max_followups_today]

fresh_target_cap = total_target_cap - len(today_followup_batch)
today_fresh_batch = all_pending[:fresh_target_cap]
remaining_queue = all_pending[fresh_target_cap:]

today_batch = [("fresh", e, 1) for e in today_fresh_batch] + [("followup", e, s) for (e, s) in today_followup_batch]
random.shuffle(today_batch)

print(f"Active SMTPs: {len(smtp_pool)} | Target: {len(today_batch)} (Fresh: {len(today_fresh_batch)}, Follow-ups: {len(today_followup_batch)}) | Remaining Queue: {len(remaining_queue)}")

with open(QUEUE_FILE, "w", encoding="utf-8") as f:
    json.dump(remaining_queue, f, indent=2)

from send_heatbolt_emails import build_html_body, build_plain_body, SUBJECT

REPLY_TO = "founder.heatbolt@gmail.com"
CC       = "team.heatbolt@gmail.com"

def build_followup_body(name_clean, seq):
    if seq == 2:
        subj = f"Re: {SUBJECT}"
        plain = (
            f"Dear {name_clean},\n\n"
            f"I wanted to follow up briefly on my previous note regarding Heatbolt's patented zero-electricity thermal activation technology.\n\n"
            f"Since my last email, our defense-validated thermal infrastructure has continued expanding into civilian, logistics, and industrial sectors where electricity-free, instant heating is mission critical.\n\n"
            f"Given your leadership in strategic investments and institutional growth, I wanted to ensure our executive overview didn't get buried in your inbox.\n\n"
            f"Would you be open to a brief 10-minute introductory conversation next week?\n\n"
            f"Best regards,\n"
            f"Dr. Kumarpal Porwal\n"
            f"Founder & MD, Heatbolt\n"
            f"PhD in Green Hydrogen (IISc Bangalore)\n"
        )
        html = (
            f"<div style=\"font-family:'Segoe UI',Arial,sans-serif;line-height:1.7;color:#222;max-width:680px;\">"
            f"<p>Dear <b>{name_clean}</b>,</p>"
            f"<p>I wanted to follow up briefly on my previous note regarding <b>Heatbolt's</b> patented zero-electricity thermal activation technology.</p>"
            f"<p>Since my last email, our defense-validated thermal infrastructure (rigorously tested at Siachen Glacier under -60°C conditions) has continued expanding into commercial and industrial sectors where electricity-free, instant heating is mission critical.</p>"
            f"<p>Given your leadership in strategic investments and institutional asset allocation, I wanted to make sure our brief introduction didn't get lost in the shuffle.</p>"
            f"<p>Would you be open to a brief 10-minute introductory conversation next week to see how Heatbolt fits your strategic vision?</p>"
            f"<p style=\"margin-top:25px;\">Warm regards,<br>"
            f"<b>Dr. Kumarpal Porwal</b><br>"
            f"<span style=\"color:#555;\">Founder & MD, Heatbolt</span><br>"
            f"<span style=\"color:#777;font-size:12px;\">PhD in Green Hydrogen, IISc Bangalore | Recipient of Indian Defence Validations</span></p>"
            f"</div>"
        )
    else:
        subj = f"Checking in / Heatbolt Strategic Infrastructure Update"
        plain = (
            f"Dear {name_clean},\n\n"
            f"I'm following up one last time to share a brief update. We are currently finalizing our institutional technical roadmap and expanding pilot deployments.\n\n"
            f"If off-grid, electricity-free thermal resilience aligns with your current investment thesis, I would be delighted to share our updated technical data room.\n\n"
            f"Best regards,\n"
            f"Dr. Kumarpal Porwal\n"
            f"Founder & MD, Heatbolt\n"
        )
        html = (
            f"<div style=\"font-family:'Segoe UI',Arial,sans-serif;line-height:1.7;color:#222;max-width:680px;\">"
            f"<p>Dear <b>{name_clean}</b>,</p>"
            f"<p>I'm following up one last time to share a brief update. We are currently finalizing our institutional technical roadmap and expanding commercial pilot deployments.</p>"
            f"<p>If off-grid, electricity-free thermal resilience aligns with your current investment thesis or strategic initiatives, I would be delighted to share our updated technical data room and field validation data.</p>"
            f"<p style=\"margin-top:25px;\">Best regards,<br>"
            f"<b>Dr. Kumarpal Porwal</b><br>"
            f"<span style=\"color:#555;\">Founder & MD, Heatbolt</span></p>"
            f"</div>"
        )
    return subj, plain, html

def send_one(smtp_user, smtp_pass, to_addr, item_type="fresh", seq=1):
    msg = MIMEMultipart("alternative")
    msg["From"]       = smtp_user
    msg["To"]         = to_addr
    msg["CC"]         = CC
    msg["Reply-To"]   = REPLY_TO
    msg["X-Priority"] = "1"
    msg["Importance"] = "High"
    
    name_clean = to_addr.split("@")[0].replace(".", " ").replace("_", " ").replace("-", " ").title()

    if item_type == "followup":
        sub, plain, html = build_followup_body(name_clean, seq)
    else:
        sub = SUBJECT
        plain = build_plain_body(name_clean, name_clean, "Your Organization", "Executive Leadership", "global_pe")
        html  = build_html_body(name_clean, name_clean, "Your Organization", "Executive Leadership", "global_pe")

    msg["Subject"] = sub
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

for idx, (item_type, target_email, seq) in enumerate(today_batch, 1):
    tries = 0
    while smtp_usage[current_smtp_idx] >= MAX_PER_SMTP and tries < len(smtp_pool):
        current_smtp_idx = (current_smtp_idx + 1) % len(smtp_pool)
        tries += 1
    
    if tries >= len(smtp_pool):
        print("All SMTP accounts reached daily cap!")
        leftover_fresh = [e for (t, e, s) in today_batch[idx-1:] if t == "fresh"]
        leftovers = leftover_fresh + remaining_queue
        with open(QUEUE_FILE, "w", encoding="utf-8") as f:
            json.dump(leftovers, f, indent=2)
        break
    
    acc = smtp_pool[current_smtp_idx]
    user = acc["user"]
    pwd  = acc["pass"]
    
    try:
        send_one(user, pwd, target_email, item_type=item_type, seq=seq)
        smtp_usage[current_smtp_idx] += 1
        rec = {
            "to": target_email,
            "from": user,
            "type": item_type,
            "seq": seq,
            "timestamp": datetime.now().isoformat(),
            "status": "SENT"
        }
        sent_records.append(rec)
        print(f"[{idx:4d}/{len(today_batch)}] SENT ({item_type.upper()} seq:{seq}) -> {target_email:<40} (via {user.split('@')[0]} | {smtp_usage[current_smtp_idx]}/{MAX_PER_SMTP})", flush=True)
        
        with open(LOG_FILE, "w", encoding="utf-8") as f:
            json.dump(sent_records, f, indent=2)
        
        # Update followup tracker
        followup_tracker[target_email] = {
            "last_sent": datetime.now().isoformat(),
            "seq": seq,
            "status": "sent"
        }
        with open(FOLLOWUP_TRACKER, "w", encoding="utf-8") as f:
            json.dump(followup_tracker, f, indent=2)

        # Update cumulative master sent history (only for fresh sends)
        if item_type == "fresh":
            master_list = []
            if os.path.exists(MASTER_SENT):
                try:
                    with open(MASTER_SENT, "r", encoding="utf-8") as f:
                        master_list = json.load(f)
                except:
                    master_list = []
            master_list.append({"to": target_email, "sent_at": datetime.now().isoformat(), "sender": user})
            with open(MASTER_SENT, "w", encoding="utf-8") as f:
                json.dump(master_list, f)
            
    except Exception as ex:
        print(f"[{idx:4d}/{len(today_batch)}] FAIL ({item_type}) -> {target_email} | Error: {ex}", flush=True)
        failed_records.append({"to": target_email, "from": user, "error": str(ex), "timestamp": datetime.now().isoformat()})
        with open(FAIL_FILE, "w", encoding="utf-8") as f:
            json.dump(failed_records, f, indent=2)
    
    current_smtp_idx = (current_smtp_idx + 1) % len(smtp_pool)
    delay = random.uniform(8, 12)
    time.sleep(delay)

print(f"Job finished. Successfully sent: {len(sent_records)}, Failed: {len(failed_records)}")
