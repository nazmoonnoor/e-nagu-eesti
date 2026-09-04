#!/usr/bin/env python3
"""Build the A2 question bank as a wiki page + a CSV.

Source: the "Küsi ja vasta" tables in Settle in Estonia and the "NB!"
sections in E nagu Eesti, regrouped by exam topic instead of by chapter.
Model answers are written to be adapted — swap in your own details.

Usage:  python3 build_kysimused.py [WIKI_DIR] [CSV_DIR]
Defaults to the script's own directory for both.
"""
import csv, os, re, sys

# topic -> [(question, english, model answer, source)]
# source: S<n> = Settle chapter n, E<n> = E nagu Eesti chapter n
DATA = {
"Mina ja keeleõpe — me & learning Estonian": [
 ("Mis sinu nimi on?","What is your name?","Minu nimi on Nazmoon.","S1 · E1"),
 ("Mis sinu perekonnanimi on?","What is your surname?","Minu perekonnanimi on … .","S1"),
 ("Kust sa pärit oled?","Where are you from?","Ma olen pärit Bangladeshist.","S1 · E2"),
 ("Kus sa oled sündinud?","Where were you born?","Ma olen sündinud Dhakas.","E2"),
 ("Mis keelt sa räägid?","What language do you speak?","Ma räägin bengali ja inglise keelt, natuke ka eesti keelt.","S1"),
 ("Kas sa oskad eesti keelt?","Do you speak Estonian?","Natuke oskan. Ma õpin iga päev.","E2"),
 ("Mis keelt sa veel oskad?","What other languages do you know?","Ma oskan ka inglise keelt.","E2"),
 ("Kus sa praegu eesti keelt õpid?","Where are you studying Estonian now?","Ma õpin eesti keelt kursusel.","E2"),
 ("Kus sa oled eesti keelt õppinud?","Where have you studied Estonian?","Ma olen õppinud keeltekoolis ja kodus.","E2"),
 ("Kes on sinu eesti keele õpetaja?","Who is your Estonian teacher?","Minu õpetaja nimi on … .","E2 · S1"),
 ("Kas eesti keel on raske?","Is Estonian difficult?","Jah, päris raske, aga väga huvitav.","E2"),
 ("Mis päeval on eesti keele tund?","What day is your Estonian class?","Eesti keele tund on esmaspäeval ja neljapäeval.","S1"),
 ("Mis kell algab eesti keele tund?","What time does the class start?","Tund algab kell kuus.","S1"),
 ("Millal on järgmine eesti keele tund?","When is the next Estonian class?","Järgmine tund on neljapäeval.","E5"),
 ("Mis aastal sa eesti keelt õppima hakkasid?","What year did you start learning Estonian?","Ma hakkasin eesti keelt õppima aastal 2024.","S24"),
],
"Pere ja sugulased — family": [
 ("Kas sa oled abielus?","Are you married?","Jah, olen küll. / Ei, ma olen vallaline.","S7 · E7"),
 ("Kas sul on suur pere?","Do you have a big family?","Jah, mul on üsna suur pere.","E7"),
 ("Mitu õde-venda sul on?","How many siblings do you have?","Mul on kaks venda ja üks õde.","S7 · E4"),
 ("Kas sul on lapsi?","Do you have children?","Jah, mul on üks tütar. / Ei, mul ei ole lapsi.","S7"),
 ("Kus su ema ja isa elavad?","Where do your parents live?","Nad elavad Bangladeshis.","S7"),
 ("Kui vanad nad on?","How old are they?","Minu ema on kuuskümmend ja isa kuuskümmend viis aastat vana.","E7"),
 ("Kas sul on lemmikloom?","Do you have a pet?","Jah, mul on kass. / Ei, mul ei ole.","E7"),
 ("Kellel on sinu peres loom?","Who in your family has a pet?","Minu õel on koer.","E4"),
],
"Kodu ja elukoht — home": [
 ("Kus sa elad?","Where do you live?","Ma elan Tallinnas Mustamäel.","S3 · E1 · E3"),
 ("Mis on sinu aadress?","What is your address?","Minu aadress on Sõpruse puiestee 15–34.","S3 · E3"),
 ("Kas sa elad majas või korteris?","Do you live in a house or a flat?","Ma elan korteris.","S4 · E14"),
 ("Kas sa elad maal või linnas?","Do you live in the country or in town?","Ma elan linnas.","E3"),
 ("Mitu tuba sinu kodus on?","How many rooms does your home have?","Minu kodus on kolm tuba.","S4 · E14"),
 ("Mitmendal korrusel sa elad?","What floor do you live on?","Ma elan neljandal korrusel.","S3 · E14"),
 ("Kas sinu majas on lift?","Is there a lift in your building?","Jah, on küll. / Ei, ei ole.","S4"),
 ("Kui suur on sinu köök?","How big is your kitchen?","Minu köök on kaksteist ruutmeetrit.","S4"),
 ("Kas sul on rõdu, aed või kelder?","Do you have a balcony, garden or cellar?","Mul on rõdu ja kelder.","S4"),
 ("Missugune sinu tuba on?","What is your room like?","Minu tuba on väike, aga valge ja mõnus.","E14"),
 ("Milline mööbel sul korteris on?","What furniture do you have?","Mul on voodi, laud, kaks tugitooli ja suur riiul.","E14"),
 ("Kui suur on üür?","How much is the rent?","Üür on nelisada eurot kuus.","S4"),
 ("Kas sulle meeldib sinu kodu?","Do you like your home?","Jah, meeldib küll.","S4"),
 ("Kuidas sa oma naabritega läbi saad?","How do you get on with your neighbours?","Ma saan naabritega hästi läbi.","E13"),
 ("Milline on transpordiühendus?","What are the transport links like?","Ühendus on hea — buss sõidab iga kümne minuti tagant.","E14"),
],
"Igapäev ja nädal — daily routine": [
 ("Mis kell sa tavaliselt üles tõused?","What time do you usually get up?","Ma tõusen üles kell seitse.","E5"),
 ("Mida sa hommikul kodus teed?","What do you do at home in the morning?","Ma käin duši all, joon kohvi ja loen uudiseid.","E9"),
 ("Mida sa hommikul tavaliselt sööd?","What do you usually eat in the morning?","Tavaliselt söön võileiba ja joon kohvi.","E9"),
 ("Mis kell sa tööle lähed?","What time do you go to work?","Ma lähen tööle kell kaheksa.","E5"),
 ("Kuidas sa tavaliselt tööle lähed?","How do you usually get to work?","Ma lähen bussiga, mõnikord jalgsi.","E5"),
 ("Mis kell su töö algab ja lõpeb?","When does your work start and finish?","Töö algab kell üheksa ja lõpeb kell viis.","E10"),
 ("Mis kell sa koju tuled?","What time do you come home?","Ma tulen koju umbes kell kuus.","E5"),
 ("Mis kell sa magama lähed?","What time do you go to bed?","Ma lähen magama kell üksteist.","E7 · E14"),
 ("Mida sa teed täna õhtul?","What are you doing this evening?","Täna õhtul ma vaatan filmi ja loen raamatut.","S12 · E8"),
 ("Mida sa teed nädalavahetusel?","What do you do at the weekend?","Nädalavahetusel ma puhkan ja käin sõpradega väljas.","S12"),
 ("Mida sa teed järgmisel nädalal?","What are you doing next week?","Järgmisel nädalal ma lähen Tartusse.","S12"),
 ("Milliseid kodutöid sulle teha meeldib?","Which chores do you like doing?","Mulle meeldib süüa teha, aga ei meeldi koristada.","E14"),
 ("Kuidas sa prügi sorteerid?","How do you sort your rubbish?","Ma sorteerin paberi, plasti ja biojäätmed.","E14"),
 ("Mida sa pead täna veel tegema?","What else do you have to do today?","Ma pean veel nõusid pesema ja poes käima.","E7"),
],
"Töö ja haridus — work & education": [
 ("Kellena sa töötad?","What do you work as?","Ma töötan tarkvaraarendajana.","E10 · S23"),
 ("Kus sa töötad?","Where do you work?","Ma töötan ühes IT-firmas Tallinnas.","E10 · S23"),
 ("Kuidas see töö sulle meeldib?","How do you like the job?","Töö meeldib mulle väga, see on huvitav.","E10"),
 ("Kui kaua sa oled seal töötanud?","How long have you worked there?","Ma olen seal töötanud kolm aastat.","E10"),
 ("Mis haridus sul on?","What education do you have?","Mul on kõrgharidus.","E10"),
 ("Mis aastal sa kooli lõpetasid?","What year did you finish school?","Ma lõpetasin kooli aastal 2010.","S24"),
 ("Kas sa oled oma tööga rahul?","Are you happy with your job?","Jah, olen küll rahul.","E21"),
],
"Vaba aeg ja hobid — free time": [
 ("Mis on sinu hobid?","What are your hobbies?","Minu hobid on lugemine ja jooksmine.","E8"),
 ("Mis sporti sa teed?","What sport do you do?","Ma teen trenni ja käin ujumas.","E8"),
 ("Mitu korda nädalas sa trennis käid?","How often do you train?","Ma käin trennis kolm korda nädalas.","E8"),
 ("Milline muusika sulle meeldib?","What music do you like?","Mulle meeldib klassikaline muusika.","E8"),
 ("Kas sulle meeldib suusatada ja uisutada?","Do you like skiing and skating?","Suusatada meeldib, aga uisutada ma ei oska.","E8"),
 ("Mida uut sa tahad õppida?","What new thing do you want to learn?","Ma tahan õppida kitarri mängima.","E8"),
 ("Kas sa tahad täna kinno minna?","Do you want to go to the cinema today?","Jah, hea meelega!","E8"),
 ("Kus ja millal me kohtume?","Where and when shall we meet?","Kohtume kell seitse kino ees.","E8"),
 ("Millal sa viimati kinos käisid?","When did you last go to the cinema?","Viimati käisin kinos detsembris.","S22"),
 ("Kas sa oled kunagi laulupeol käinud?","Have you ever been to the song festival?","Jah, olen käinud. / Ei, ei ole veel.","S22"),
],
"Söök ja jook — food & drink": [
 ("Mida sa täna hommikul sõid?","What did you eat this morning?","Täna hommikul sõin putru.","S25"),
 ("Mida sa eile õhtul jõid?","What did you drink last night?","Eile õhtul jõin teed.","S25"),
 ("Kas sa oskad süüa teha?","Can you cook?","Jah, oskan küll. / Ei, ei oska.","S25 · S14"),
 ("Mis sööki sa väga hästi teed?","What dish do you make really well?","Ma teen väga hästi kanasuppi.","S25"),
 ("Kas sa soovid teed või kohvi?","Would you like tea or coffee?","Ma soovin kohvi, palun.","E9"),
 ("Millised söögid sulle ei maitse?","Which foods don't you like?","Mulle ei maitse verivorst.","E15"),
 ("Kas soovid valget või punast veini?","Would you like white or red wine?","Ma soovin punast veini.","E15"),
],
"Ostmine ja teenindus — shopping & services": [
 ("Kas ma võin proovida?","May I try it on?","Jah, muidugi. Proovikabiinid on seal.","S16"),
 ("Kui palju see maksab?","How much does it cost?","See maksab kakskümmend viis eurot.","S16"),
 ("Kas te maksate sularahas või kaardiga?","Are you paying cash or by card?","Ma maksan kaardiga.","S22"),
 ("Millal on pood avatud?","When is the shop open?","Pood on avatud iga päev kümnest kümneni.","S10"),
 ("Mitmendal korrusel asub raamatupood?","What floor is the bookshop on?","Raamatupood asub kolmandal korrusel.","S10"),
 ("Kui palju maksab sooduspilet?","How much is the concession ticket?","Sooduspilet maksab viis eurot.","S22"),
],
"Reisimine ja transport — travel": [
 ("Millal sa Tartusse lähed?","When are you going to Tartu?","Ma lähen Tartusse laupäeval.","E5"),
 ("Kui kaua sa Tartus oled?","How long will you be in Tartu?","Ma olen seal kaks päeva.","E5"),
 ("Millal läheb järgmine buss Pärnusse?","When does the next bus to Pärnu leave?","Järgmine buss läheb kell kaks.","E5"),
 ("Kui kaua buss sinna sõidab?","How long does the bus take?","Buss sõidab umbes kaks tundi.","E5"),
 ("Kui palju pilet maksab?","How much is the ticket?","Pilet maksab kümme eurot.","E5"),
 ("Mitu kilomeetrit on siit Tartusse?","How many kilometres is it to Tartu?","Siit on Tartusse umbes sada kaheksakümmend viis kilomeetrit.","E5"),
 ("Kellega sa sõidad?","Who are you travelling with?","Ma sõidan sõbraga.","E6"),
 ("Kuhu sa puhkusele sõidad?","Where are you going on holiday?","Ma sõidan Saaremaale.","E6"),
 ("Millal sul puhkus on?","When is your holiday?","Mul on puhkus juulis.","E6"),
 ("Mis aastal sa Eestisse tulid?","What year did you come to Estonia?","Ma tulin Eestisse aastal 2022.","S24"),
],
"Tervis — health": [
 ("Mis sul viga on?","What's wrong with you?","Mul on köha ja nohu.","S27"),
 ("Kas su pea valutab?","Does your head hurt?","Jah, natuke valutab. / Ei, ei valuta.","S26"),
 ("Kas sul on palavik?","Do you have a fever?","Jah, on küll — kolmkümmend kaheksa kraadi.","S26"),
 ("Millal sa haigeks jäid?","When did you fall ill?","Ma jäin haigeks kaks päeva tagasi.","S28"),
 ("Mille üle te kaebate?","What are you complaining of?","Mul valutab kõht ja mul on palavik.","S28"),
 ("Kas sa oled väsinud?","Are you tired?","Jah, olen natuke väsinud.","S26"),
 ("Mis on Eesti hädaabi number?","What is the Estonian emergency number?","Hädaabi number on sada kaksteist.","S27"),
],
"Ilm ja aastaajad — weather & seasons": [
 ("Mis ilm täna on?","What's the weather like today?","Täna on ilus ilm, päike paistab.","E6"),
 ("Kas täna sajab vihma?","Is it raining today?","Ei, ei saja. / Jah, sajab küll.","S11"),
 ("Mitu kraadi täna on?","What's the temperature today?","Täna on viisteist kraadi sooja.","S11"),
 ("Mis on sinu lemmikaastaaeg?","What's your favourite season?","Minu lemmikaastaaeg on suvi.","E6"),
 ("Miks sulle meeldib kevad?","Why do you like spring?","Kevad meeldib mulle, sest linnud laulavad ja päevad on pikad.","E6"),
 ("Millal algab sügis?","When does autumn begin?","Sügis algab septembris.","E6"),
 ("Mida tehakse talvel?","What do people do in winter?","Talvel suusatatakse ja uisutatakse.","S30"),
],
"Külalised ja tähtpäevad — visiting & celebrations": [
 ("Millal on sinu sünnipäev?","When is your birthday?","Minu sünnipäev on kolmandal mail.","S6 · E6"),
 ("Kellele sa lähed külla pühapäeval?","Who are you visiting on Sunday?","Pühapäeval lähen sõbrale külla.","S13"),
 ("Millal te meile külla tulete?","When will you come and visit us?","Me tuleme laupäeva õhtul.","E15"),
 ("Mis kell külalised tulevad?","What time are the guests coming?","Külalised tulevad kell seitse.","E15"),
 ("Mitu inimest sa peole kutsusid?","How many people did you invite?","Ma kutsusin kümme inimest.","E15"),
 ("Mida sa kingiks tood?","What will you bring as a present?","Ma toon lilled ja veini.","E15"),
 ("Kus me sünnipäeva peame?","Where shall we hold the birthday party?","Peame sünnipäeva kodus.","E15"),
],
"Minu elulugu — life story (CV)": [
 ("Mis aastal sa sündisid?","What year were you born?","Ma sündisin aastal 1990.","S24"),
 ("Mis aastal sa kooli läksid?","What year did you start school?","Ma läksin kooli aastal 1997.","S24"),
 ("Mis aastal sa abiellusid?","What year did you get married?","Ma abiellusin aastal 2015.","S24"),
 ("Mis aastal sul laps sündis?","What year was your child born?","Mul sündis tütar aastal 2018.","S24"),
 ("Mis aastal sa korteri ostsid?","What year did you buy your flat?","Ma ostsin korteri aastal 2021.","S24"),
],
"Vestlus ja viisakus — small talk & politeness": [
 ("Kuidas sul läheb?","How are you?","Hästi, aitäh! Aga sinul?","E1"),
 ("Kuidas sul eilne päev läks?","How was your day yesterday?","Läks hästi, aitäh.","E9"),
 ("Mis plaanid sul täna on?","What are your plans today?","Täna ma lähen tööle ja õhtul trenni.","E9"),
 ("Kas sa oled lõuna ajal vaba?","Are you free at lunchtime?","Jah, olen küll.","E9"),
 ("Kas sa oled minuga nõus?","Do you agree with me?","Jah, olen täiesti nõus. / Ei, mina nii ei arva.","E15"),
 ("Kuidas palun?","Pardon?","Vabandust, ma ei saa aru. Korrake palun!","S2"),
 ("Mida see sõna tähendab?","What does this word mean?","See tähendab … . Kuidas on see eesti keeles?","S2"),
],
}


def slug(s):
    s = s.strip().lower()
    s = re.sub(r"[^\w\s-]", "", s, flags=re.UNICODE)
    return re.sub(r"\s", "-", s)


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    wiki_dir = sys.argv[1] if len(sys.argv) > 1 else here
    csv_dir = sys.argv[2] if len(sys.argv) > 2 else here

    rows, seen = [], set()
    for topic, items in DATA.items():
        for q, en, ans, src in items:
            if q in seen:
                print("DUPLICATE SKIPPED:", q)
                continue
            seen.add(q)
            rows.append((q, en, ans, topic.split(" — ")[0], src))

    path = os.path.join(csv_dir, "settle-kysimused.csv")
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["question", "english", "model answer", "topic", "source"])
        w.writerows(rows)
    print("wrote", path, "-", len(rows), "questions")

    heads = [f"{i}. {t}" for i, t in enumerate(DATA, 1)]
    nav = " · ".join(
        f"[{h.split('. ', 1)[1].split(' — ')[0]}](#{slug(h)})" for h in heads)
    L = ["# Küsimused ja vastused — A2 eksamiks", "",
         "> **The speaking-test question bank.** Every question here is taken from the coursebooks — the `Küsi ja vasta!` tables in *Settle in Estonia* and the `NB!` sections in *E nagu Eesti* — regrouped by exam topic instead of by chapter.", "",
         f"**On this page:** {nav}", "",
         "> 🔹 **How to use this.** Cover the two right-hand columns, read the question aloud, answer from memory, then check. The model answers are **written to be adapted** — swap in your own name, address, job and dates. Learn to *ask* each question as well as answer it; the examiner expects you to hold a two-way conversation.", "",
         "> ⚠️ **Prepare your own facts first.** Your name, address, date of birth, job, family and the year you came to Estonia come up in nearly every exam. Fix one Estonian sentence for each and reuse it — improvising numbers under pressure is where marks get lost.", "",
         "Related: [Tegevused — Settle in Estonia](Tegevused-Settle-in-Estonia.md) · [Overview — Settle in Estonia](Overview-Settle-in-Estonia.md) · [Overview — E nagu Eesti](Overview-E-nagu-Eesti.md)", "",
         "---", ""]
    for i, (topic, items) in enumerate(DATA.items(), 1):
        L += [f"## {i}. {topic}", "",
              "| Küsimus | English | Näidisvastus | Allikas |", "|---|---|---|---|"]
        for q, en, ans, src in items:
            L.append(f"| **{q}** | {en} | {ans} | {src} |")
        L += ["", "---", ""]
    L += [f"*{len(rows)} questions across {len(DATA)} topics. "
          "Source codes: **S** = Settle in Estonia chapter, **E** = E nagu Eesti chapter.*", "",
          "← [Home](Home) · [Tegevused](Tegevused-Settle-in-Estonia.md) →", ""]
    path = os.path.join(wiki_dir, "Kysimused-A2-eksamiks.md")
    open(path, "w", encoding="utf-8").write("\n".join(L))
    print("wrote", path)


main()
