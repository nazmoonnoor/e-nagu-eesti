#!/usr/bin/env python3
"""Build the Settle in Estonia activity list as CSV + a wiki page.
Single source of truth: DATA below. Run from anywhere."""
import csv, os, sys

# (activity, meaning, example, chapter)
DATA = {
"Igapäevane rutiin — daily routine": [
 ("ärgata","to wake up","Ma ärkan kell seitse.",12),
 ("üles tõusta","to get up","Ma tõusen üles kell pool kaheksa.",12),
 ("duši all käia","to have a shower","Hommikul ma käin duši all.",12),
 ("hambaid pesta","to brush your teeth","Ma pesen hambaid vannitoas.",4),
 ("riidesse panna","to get dressed","Ma panen magamistoas riidesse.",4),
 ("riidest lahti võtta","to get undressed","Ma võtan riidest lahti magamistoas.",4),
 ("juukseid kammida","to comb your hair","Ma kammin juukseid vannitoas.",12),
 ("meiki teha","to do your make-up","Ma teen hommikul meiki.",12),
 ("magada","to sleep","Nädalavahetusel ma magan kaua.",12),
 ("päeval magada","to sleep during the day","Kes magas eile päeval?",20),
],
"Kodu ja kodused tööd — home & chores": [
 ("tuba koristada","to tidy the room","Mulle ei meeldi tuba koristada.",1),
 ("koristada","to clean, to tidy up","Ma koristan laupäeval.",4),
 ("kööki koristada","to clean the kitchen","Kes sinu peres koristab kööki?",14),
 ("maja koristada","to clean the house","Kevadel koristame maja.",30),
 ("kappe koristada","to tidy the cupboards","Mina koristan kappe.",30),
 ("garaaži koristada","to clean the garage","Minu mees koristab garaaži.",30),
 ("nõusid pesta","to wash the dishes","Kas sa pesed nõusid vannitoas?",4),
 ("aknaid pesta","to wash the windows","Ma pesen kevadel aknaid.",14),
 ("pesu pesta","to do the laundry","Laupäeval ma pesen pesu.",12),
 ("pesu triikida","to iron","Ma ei taha pesu triikida.",14),
 ("prügi välja viia","to take out the rubbish","Mul on vaja prügi välja viia.",14),
 ("prügi sorteerida","to sort the rubbish","Meie peres sorteerib prügi isa.",14),
 ("autot parandada","to repair a car","Kas sa oskad autot parandada?",14),
 ("remonti teha","to do repairs, to renovate","Minu vend oskab remonti teha.",1),
 ("koera pesta","to wash the dog","Mul on vaja koera pesta.",13),
 ("koeraga jalutada","to walk the dog","Ma jalutan koeraga iga päev.",12),
 ("kardinaid õmmelda","to sew curtains","Mõnikord õmblen uued kardinad.",30),
 ("majas elada","to live in a house","Ma elan suures majas.",3),
 ("koos elada","to live together","Me elame koos.",7),
],
"Söök ja jook — food & drink": [
 ("süüa teha","to cook","Õhtul ma teen süüa.",1),
 ("kohvi juua","to drink coffee","Hommikul ma joon kohvi.",1),
 ("veini juua","to drink wine","Õhtul meeldib mulle veini juua.",1),
 ("õlut juua","to drink beer","Kas sulle meeldib hommikul õlut juua?",1),
 ("jäätist süüa","to eat ice cream","Suvel meeldib mulle jäätist süüa.",1),
 ("pitsat süüa","to eat pizza","Kas sulle meeldib öösel pitsat süüa?",1),
 ("valget šokolaadi süüa","to eat white chocolate","Mulle meeldib valget šokolaadi süüa.",1),
 ("võileiba süüa","to eat a sandwich","Ma söön köögis võileiba.",4),
 ("tainast segada","to mix the dough","Sega tainast! · Ära sega tainast!",25),
 ("jahu võtta","to take flour","Võta jahu!",25),
 ("suppi maitsta","to taste the soup","Maitse suppi!",25),
 ("soola lisada","to add salt","Lisa soola ja pipart!",25),
 ("piima valada","to pour milk","Vala piima!",25),
 ("võid määrida","to spread butter","Määri võid!",25),
 ("kartulit koorida","to peel a potato","Koori kartulid!",25),
 ("tomatit lõigata","to cut a tomato","Lõika tomatit!",25),
 ("vett keeta","to boil water","Keeda vett!",25),
 ("kartuleid keeta","to boil potatoes","Keeda kartulid koos koorega!",25),
 ("tükkideks lõigata","to cut into pieces","Lõika sink, õun ja kurgid tükkideks!",25),
 ("kaussi panna","to put in a bowl","Pane kõik kaussi!",25),
 ("moosi keeta","to make jam","Ostan maasikaid ja keedan moosi.",30),
 ("grillida","to have a barbecue","Grillime sõpradega ja joome õlut.",30),
 ("kokaraamatut lugeda","to read a cookbook","Mitu kokaraamatut sul on?",25),
 ("kõht tühi olla","to be hungry","Triinul on kõht tühi.",25),
 ("head isu soovida","to wish bon appétit","Head isu!",25),
 ("kellelegi kohvi teha","to make someone a coffee","Õpetaja teeb sulle kohvi.",26),
 ("õunaveini teha","to make apple wine","Sügisel ma teen õunaveini.",3),
 ("süüa tahta","to want to eat","Ma tahaks praegu jäätist süüa.",29),
 ("juua tahta","to want to drink","Mida sa praegu juua tahaks?",29),
],
"Vaba aeg ja meelelahutus — free time": [
 ("kohvikus istuda","to sit in a café","Kas sulle meeldib kohvikus istuda?",1),
 ("saunas käia","to go to the sauna","Mulle meeldib laupäeval saunas käia.",1),
 ("diskol käia","to go to the disco","Kas sulle meeldib diskol käia?",1),
 ("ööklubis käia","to go to a nightclub","Ma ei käi ööklubis.",1),
 ("raamatukogus käia","to go to the library","Kas sulle meeldib raamatukogus käia?",1),
 ("televiisorit vaadata","to watch television","Õhtul ma vaatan televiisorit.",1),
 ("multifilme vaadata","to watch cartoons","Lastele meeldib multifilme vaadata.",1),
 ("märulifilme vaadata","to watch action films","Kas sulle meeldib märulifilme vaadata?",1),
 ("filmi vaadata","to watch a film","Ma vaatan Netflixist filmi.",12),
 ("klassikalist muusikat kuulata","to listen to classical music","Mulle meeldib klassikalist muusikat kuulata.",1),
 ("muusikat kuulata","to listen to music","Ma kuulan rõdul muusikat.",4),
 ("Facebookis istuda","to sit on Facebook","Mulle ei meeldi Facebookis istuda.",1),
 ("arvutis istuda","to sit at the computer","Ma istun terve päeva arvutis.",12),
 ("arvutimänge mängida","to play computer games","Õhtul ma mängin arvutimänge.",12),
 ("raamatut lugeda","to read a book","Ma loen elutoas raamatut.",4),
 ("uudiseid lugeda","to read the news","Hommikul ma loen uudiseid.",12),
 ("lauamänge mängida","to play board games","Tule külla, me mängime lauamänge.",13),
 ("laulda","to sing","Ma ei oska laulda.",1),
 ("tangot tantsida","to dance the tango","Kas sa oskad tangot tantsida?",1),
 ("klaverit mängida","to play the piano","Minu õde oskab klaverit mängida.",1),
 ("kitarri mängida","to play the guitar","Ma oskan natuke kitarri mängida.",1),
 ("käsitööd teha","to do handicrafts","Sügisel ma teen käsitööd.",30),
 ("puhata","to rest, to be on holiday","Suvel ma alati puhkan.",30),
],
"Sport ja liikumine — sport & outdoors": [
 ("sporti teha","to do sport","Kas sulle meeldib sporti teha?",1),
 ("trenni teha","to train, to work out","Ma teen kolm korda nädalas trenni.",12),
 ("ujuda","to swim","Kas sa oskad ujuda? — Oskan küll.",1),
 ("meres ujuda","to swim in the sea","Suvel ujutakse meres.",30),
 ("jalgpalli mängida","to play football","Kas sa oskad jalgpalli mängida?",1),
 ("tennist mängida","to play tennis","Ta oskab hästi tennist mängida.",1),
 ("hokit mängida","to play ice hockey","Talvel mängitakse hokit.",30),
 ("jalgrattaga sõita","to ride a bicycle","Suvel meeldib mulle jalgrattaga sõita.",1),
 ("öösel jalutada","to walk at night","Kas sulle meeldib öösel jalutada?",1),
 ("kelgutada","to go sledging","Lapsed kelgutavad.",30),
 ("lumememme teha","to build a snowman","Lapsed teevad lumememme.",30),
 ("päevitada","to sunbathe","Mu naine käib rannas ja päevitab.",30),
 ("kalal käia","to go fishing","Ma käin tihti kalal.",30),
 ("metsas käia","to go to the forest","Sügisel käime metsas.",30),
 ("seeni korjata","to pick mushrooms","Käime metsas, korjame seeni ja marju.",30),
 ("marju korjata","to pick berries","Sügisel korjatakse marju.",30),
 ("aias töötada","to work in the garden","Suvel meeldib mulle aias töötada.",1),
 ("tomateid kasvatada","to grow tomatoes","Kasvatame tomateid ja kurke.",30),
 ("lilli kasvatada","to grow flowers","Minu naine kasvatab lilli.",30),
 ("värsket õhku hingata","to breathe fresh air","Kevadel hingame värsket õhku.",30),
],
"Töö ja õppimine — work & study": [
 ("töötada","to work","Kes töötas eile?",20),
 ("haiglas töötada","to work in a hospital","Ma töötan haiglas, olen arst.",7),
 ("restoranis töötada","to work in a restaurant","Ta töötab restoranis.",23),
 ("kokana töötada","to work as a cook","Ma töötan restoranis kokana.",23),
 ("kellenagi töötada","to work as (a profession)","Ta võiks töötada poliitikuna.",6),
 ("eesti keelt õppida","to study Estonian","Mulle meeldib eesti keelt õppida.",1),
 ("e-kirju kirjutada","to write emails","Ma kirjutan töötoas e-kirju.",4),
 ("eksamit teha","to take an exam","Homme on eesti keele eksam.",26),
 ("CV-d kirjutada","to write a CV","Ma kirjutan oma CV eesti keeles.",24),
 ("kedagi tunda","to know someone","Kas sa tunned kedagi, kes on arhitekt?",23),
],
"Suhtlemine — communication": [
 ("aru saada","to understand","Vabandust, ma ei saa aru.",2),
 ("korrata","to repeat","Korda palun! · Korrake palun!",2),
 ("uuesti öelda","to say again","Ütle uuesti! · Öelge uuesti!",2),
 ("oodata","to wait","Oota! Ma ei saa aru.",2),
 ("tähendada","to mean","Mida tähendab „kullake”?",2),
 ("eesti keeles öelda","to say in Estonian","Kuidas on eesti keeles „smile”?",2),
 ("vene keelt rääkida","to speak Russian","Kas sa räägid vene keelt? — Räägin küll.",1),
 ("jaapani keelt osata","to know Japanese","Kas sa oskad jaapani keelt? — Ei, ei oska.",1),
 ("sõpradega rääkida","to talk with friends","Mulle meeldib Skype'is sõpradega rääkida.",1),
 ("emale helistada","to call your mother","Sünnipäeva hommikul me helistame emale.",4),
 ("sõbrale helistada","to call a friend","Kes helistas eile sõbrale?",20),
 ("komplimenti teha","to pay a compliment","Sul on väga ilusad pikad juuksed!",9),
 ("nõu anda","to give advice","Anna nõu, mida ma pean tegema!",27),
 ("reageerida","to react, to respond","Kuidas sa reageerid?",26),
 ("abielus olla","to be married","Kas sa oled abielus? — Jah, olen küll.",7),
],
"Külaskäik ja tähtpäevad — visiting & celebrations": [
 ("kellelegi külla minna","to go and visit someone","Pühapäeval lähen sõbrale külla.",8),
 ("külla tulla","to come and visit","Tule mulle õhtul külla!",13),
 ("külla kutsuda","to invite someone over","Ma kutsun sõbra külla.",13),
 ("külalisi kutsuda","to invite guests","Käime tihti külas ja kutsume külalisi.",30),
 ("sauna kutsuda","to invite to the sauna","Kolleegid kutsuvad sind sauna.",26),
 ("kaasa võtta","to bring along","Mis ma kaasa võtan? — Midagi pole vaja.",13),
 ("lilli kinkida","to give flowers","Sünnipäeval kingime emale lilled.",8),
 ("sünnipäevalaulu laulda","to sing the birthday song","Me laulame emale sünnipäevalaulu.",8),
 ("sünnipäevakaarti kirjutada","to write a birthday card","Kirjutame kolleegile sünnipäevakaardi.",8),
 ("jõulukaarti saata","to send a Christmas card","Saadame vanaemale jõulukaardi.",8),
 ("häid pühi soovida","to wish happy holidays","Soovime emale ja isale „Häid pühi!”.",8),
],
"Reisimine ja liikumine — getting around": [
 ("tööl käia / tööle minna","to go to work (regularly / now)","Ma käin tööl. · Ma lähen tööle kell kaheksa.",12),
 ("turul käia / turule minna","to go to the market","Laupäeviti käin turul.",12),
 ("koosolekul käia / koosolekule minna","to attend a meeting","Ma lähen koosolekule kell kaks.",12),
 ("lõunal käia / lõunale minna","to go to lunch","Ma käin lõunal kell üks.",12),
 ("teatris käia / teatrisse minna","to go to the theatre","Ma käin teatris kord kuus.",12),
 ("kohvikus käia / kohvikusse minna","to go to a café","Lähme kohvikusse!",12),
 ("poes käia / poodi minna","to go to the shop","Ma käin iga päev poes. · Ma lähen poodi.",1),
 ("kinos käia / kinno minna","to go to the cinema","Reedel läheme kinno.",1),
 ("restoranis käia / restorani minna","to go to a restaurant","Me läheme restorani.",12),
 ("trennis käia / trenni minna","to go to training","Esmaspäeviti käin trennis.",12),
 ("ülikoolis käia / ülikooli minna","to go to university","Ta käib ülikoolis.",12),
 ("sõbral külas käia / sõbrale külla minna","to visit a friend","Pühapäeval lähen sõbrale külla.",12),
 ("bussiga sõita","to travel by bus","Ma sõidan bussiga tööle.",19),
 ("rongiga sõita","to travel by train","Sõidan rongiga Tallinnast Tartusse.",19),
 ("lennukiga sõita","to travel by plane","Sõidan lennukiga Nigeeriast Hispaaniasse.",19),
 ("trammiga tulla","to come by tram","Tule trammiga number kaks!",13),
 ("jalgsi tulla","to come on foot","Tavaliselt tulen jalgsi, mõnikord bussiga.",19),
 ("ringi sõita","to drive around","Suvel sõidame ringi, avastame Eestit.",30),
 ("Eestit avastada","to explore Estonia","Suvel avastame Eestit.",30),
 ("reisida","to travel","Kevadel mõnikord ka reisin.",30),
 ("koju minna","to go home","Mine koju!",27),
 ("autorehve vahetada","to change the tyres","Sügisel vahetan autorehvid ära.",30),
],
"Ostlemine ja asjaajamine — shopping & errands": [
 ("toidupoes käia","to go to the grocery shop","Kes käis eile toidupoes?",20),
 ("autot osta","to buy a car","Kes ostis eile auto?",20),
 ("maasikaid osta","to buy strawberries","Ma käin turul ja ostan maasikaid.",30),
 ("korterit osta","to buy a flat","Ma ostsin korteri aastal 2019.",24),
 ("proovida","to try on","Kas ma võin proovida? — Muidugi!",16),
 ("aidata","to help, to serve","Kas ma saan teid aidata?",16),
 ("näidata","to show","Tulge, ma näitan!",16),
 ("kassasse minna","to go to the till","Tore! Lähme kassasse!",16),
 ("maksta","to cost, to pay","See kleit maksab 25 eurot.",16),
 ("kilekotti osta","to buy a plastic bag","Kas soovite kilekotti ka osta?",16),
 ("piletit osta","to buy a ticket","Üks pilet palun!",22),
 ("kaardiga maksta","to pay by card","Kas maksate sulas või kaardiga? — Kaardiga.",22),
 ("sularahas maksta","to pay cash","Ma maksan sularahas.",22),
 ("PIN-koodi panna","to enter your PIN","Pange kaart sisse ja pange PIN-kood!",22),
 ("viibata","to tap (contactless)","Kas klient viipab või paneb PIN-koodi?",22),
 ("dokumenti näidata","to show your ID","Teie dokument palun!",22),
 ("riideid kanda","to wear clothes","Ma kannan kodus sinist T-särki.",15),
 ("kokku sobida","to match, to go together","Roosa seelik sobib siniste sokkidega.",15),
 ("müügil olla","to be on sale","Spordipoes on müügil jalgpall.",10),
 ("avatud olla","to be open","Raamatupood on avatud E–R kümnest kuueni.",10),
],
"Üritused — events (käia + -l / -s)": [
 ("kontserdil käia","to go to a concert","Sügisel ma käin teatris ja kontserdil.",30),
 ("rokikontserdil käia","to go to a rock concert","Kas sa oled kunagi rokikontserdil käinud?",22),
 ("muuseumis käia","to go to a museum","Millal sa viimati muuseumis käisid?",22),
 ("laadal käia","to go to a fair","Kas sa oled kunagi jõululaadal käinud?",22),
 ("matkal käia","to go on a hike/trip","Kas sa oled kunagi kanuumatkal käinud?",22),
 ("koolitusel käia","to take a course","Kas sa oled kunagi keelekoolitusel käinud?",22),
 ("etendusel käia","to go to a performance","Kas sa oled kunagi teatrietendusel käinud?",22),
 ("töötoas käia","to attend a workshop","Kas sa oled kunagi keraamika töötoas käinud?",22),
 ("võistlusel käia","to go to a competition","Kas sa oled kunagi jalgpallivõistlusel käinud?",22),
 ("konverentsil käia","to attend a conference","Kas sa oled kunagi konverentsil käinud?",22),
 ("festivalil käia","to go to a festival","Kas sa oled kunagi muusikafestivalil käinud?",22),
 ("laulupeol käia","to go to the song festival","Kas sa oled kunagi laulupeol käinud?",22),
],
"Tervis ja enesetunne — health & how you feel": [
 ("haigeks jääda","to fall ill","Millal te haigeks jäite? — Kaks päeva tagasi.",28),
 ("terveks saada","to get well","Ma sain terveks. · Saa ruttu terveks!",28),
 ("kaevata","to complain of (a symptom)","Mille üle te kaebate?",28),
 ("suu lahti teha","to open your mouth","Tehke suu lahti!",28),
 ("analüüse teha","to do tests","Teeme analüüsid.",28),
 ("ravimit kirjutada","to prescribe medicine","Ma kirjutan teile ravimi.",28),
 ("arsti juures käia","to go to the doctor","Ma käisin eile arsti juures.",28),
 ("kiirabisse helistada","to call an ambulance","Helista kiirabisse!",27),
 ("perearstile helistada","to call your GP","Helista perearstile!",27),
 ("apteeki minna","to go to the pharmacy","Mine apteeki!",27),
 ("mul valutab pea","my head hurts","Mu pea valutab. · Mu kurk valutab.",27),
 ("haige olla","to be ill","Ma olen haige.",27),
 ("väsinud olla","to be tired","Ma olen väsinud.",27),
 ("palavik olla","to have a fever","Mul on palavik, 38,2 kraadi.",27),
 ("köha olla","to have a cough","Mul on köha ja nohu.",27),
 ("süda paha olla","to feel sick, nauseous","Mul on süda paha.",27),
 ("pea ringi käia","to feel dizzy","Mul käib pea ringi.",27),
],
"Ilm — weather": [
 ("tuul puhub","the wind blows","Kas täna puhub tuul? — Jah, puhub küll.",11),
 ("päike paistab","the sun shines","Kas täna paistab päike?",11),
 ("vihma sajab","it rains","Kas täna sajab vihma? — Ei, ei saja.",11),
 ("lund sajab","it snows","Talvel sajab lund.",11),
 ("taevas on pilves","the sky is cloudy","Kas taevas on pilves?",11),
 ("ilmateadet teha","to give a weather forecast","Homme on selge ilm, puhub läänetuul.",11),
],
"Elusündmused — life events": [
 ("sündida","to be born","Ma sündisin aastal 1988.",24),
 ("kooli minna","to start school","Ma läksin kooli aastal 1995.",24),
 ("kooli lõpetada","to finish school","Ma lõpetasin kooli aastal 2006.",24),
 ("tööle minna","to start work (begin a job)","Ma läksin tööle aastal 2010.",24),
 ("abielluda","to get married","Ma abiellusin aastal 2014.",24),
 ("laps sünnib","to have a child","Mul sündis tütar aastal 2016.",24),
 ("Eestisse tulla","to come to Estonia","Ma tulin Eestisse aastal 2021.",24),
 ("õppima hakata","to start learning","Ma hakkasin eesti keelt õppima aastal 2023.",24),
],
"Tegevusnimed (-mine) — activity nouns": [
 ("jooksmine","running","Mulle meeldib jooksmine.",17),
 ("ujumine","swimming","Mulle meeldib ujumine.",17),
 ("tantsimine","dancing","Kadrile meeldib tantsimine.",17),
 ("lugemine","reading","Suvel meeldib mulle rannas lugemine.",17),
 ("joonistamine","drawing","Talvel meeldib mulle joonistamine.",17),
 ("jalutamine","walking","Mulle meeldib sügisel pargis jalutamine.",17),
 ("päevitamine","sunbathing","Suvel meeldib mulle rannas päevitamine.",17),
 ("suusatamine","skiing","Talvel meeldib mulle suusatamine.",17),
 ("uisutamine","skating","Talvel meeldib mulle uisutamine.",17),
 ("reisimine","travelling","Reisimine mulle ei meeldi.",17),
 ("suitsetamine","smoking","Mulle üldse ei meeldi suitsetamine.",17),
 ("joomine","drinking","Mulle ei meeldi joomine.",17),
 ("söömine","eating","Ennule meeldib söömine.",17),
 ("filmi vaatamine","watching films","Ennule meeldib filmi vaatamine.",17),
 ("rattaga sõitmine","cycling","Rattaga sõitmine mulle väga ei meeldi.",17),
 ("šoppamine","shopping","Mulle meeldib šoppamine.",17),
],
"Käia …-mas — go and do": [
 ("jooksmas käia","to go running","Ma käin kolmapäeval metsas jooksmas.",17),
 ("ujumas käia","to go swimming","Kes käib talvel ujumas?",17),
 ("laulmas käia","to go singing","Kes käib karaokebaaris laulmas?",17),
 ("söömas käia","to go out to eat","Me käime reedel söömas.",17),
 ("tantsimas käia","to go dancing","Ma käin laupäeval tantsimas.",17),
 ("piljardit mängimas käia","to go and play billiards","Ma käin piljardit mängimas.",17),
 ("pubis õlut joomas käia","to go for a beer at the pub","Kes käib pubis õlut joomas?",17),
],
}

def main():
    out_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    wiki_dir = sys.argv[2] if len(sys.argv) > 2 else None

    rows, seen = [], set()
    for cat, items in DATA.items():
        for act, mean, ex, ch in items:
            if act in seen:
                print("DUPLICATE SKIPPED:", act); continue
            seen.add(act)
            rows.append((act, mean, ex, cat.split(" — ")[0], ch))

    csv_path = os.path.join(out_dir, "settle-tegevused.csv")
    with open(csv_path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["activity", "meaning", "example sentence", "category", "chapter"])
        w.writerows(rows)
    print("wrote", csv_path, "-", len(rows), "rows")

    if not wiki_dir:
        return
    def slug(s):
        import re
        s = s.strip().lower()
        s = re.sub(r"[^\w\s-]", "", s, flags=re.UNICODE)
        return re.sub(r"\s", "-", s)

    heads = [f"{i}. {c}" for i, c in enumerate(DATA, 1)]
    nav = " · ".join(f"[{h.split('. ',1)[1].split(' — ')[0]}](#{slug(h)})" for h in heads)
    L = ["# Tegevused — Settle in Estonia", "",
         "> **Activity phrases from the whole coursebook**, grouped by theme. Each entry is the verb *together with the object or complement it takes*, because the case on the object is part of what you have to learn: `sporti teha`, `tennist mängida`, `raamatut lugeda` are three different object cases.", "",
         f"**On this page:** {nav}", "",
         "> 🔹 **How to read these.** The headword is the **-da infinitive**, the form that slots into `Ma tahan …`, `Ma võin …`, `Mul on vaja …`, `Kas sulle meeldib …?`. The *Lk* column gives the chapter it first appears in. Two groups behave differently and are kept apart: **Tegevusnimed (-mine)** are nouns (`Mulle meeldib jooksmine`), and **Käia …-mas** is the third infinitive (`Ma käin jooksmas`).", "",
         "See also the [Overview — Settle in Estonia](Overview-Settle-in-Estonia.md) chapter map.", "", "---", ""]
    for i, (cat, items) in enumerate(DATA.items(), 1):
        L += [f"## {i}. {cat}", "", "| Tegevus | Tähendus | Näidislause | Ptk |",
              "|---|---|---|---|"]
        for act, mean, ex, ch in items:
            L.append(f"| **{act}** | {mean} | {ex} | {ch} |")
        L += ["", "---", ""]
    L += [f"*{len(rows)} phrases across {len(DATA)} categories, from all 30 chapters of Settle in Estonia.*", "",
          "← [Home](Home) · [Overview — Settle in Estonia](Overview-Settle-in-Estonia.md) →", ""]
    md_path = os.path.join(wiki_dir, "Tegevused-Settle-in-Estonia.md")
    open(md_path, "w", encoding="utf-8").write("\n".join(L))
    print("wrote", md_path)

main()
