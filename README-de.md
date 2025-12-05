<p align="center">
  <a href="https://trueconf.com" target="_blank" rel="noopener noreferrer">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="assets/logo-dark.svg">
      <img width="150" src="assets/logo.svg">
    </picture>
  </a>
</p>

<h1 align="center">Telegram-Bot zur Verwaltung des TrueConf Servers</h1>

<p align="center">Zugang zum Admin-Dashboard von überall auf der Welt durch die Telegram-Integration mit TrueConf</p>

<p align="center">
    <a href="https://t.me/trueconf_chat" target="_blank">
        <img src="https://img.shields.io/badge/Telegram-2CA5E0?logo=telegram&logoColor=white" />
    </a>
    <a href="https://discord.gg/2gJ4VUqATZ">
        <img src="https://img.shields.io/badge/Discord-%235865F2.svg?&logo=discord&logoColor=white" />
    </a>
    <a href="#">
        <img src="https://img.shields.io/github/stars/trueconf/trueconf-sdk-for-react-native?style=social" />
    </a>
</p>

<p align="center">
  <a href="./README.md">English</a> /
  <a href="./README-ru.md">Русский</a> /
  <a href="./README-de.md">Deutsch</a> /
  <a href="./README-es.md">Español</a>
</p>

<p align="center">
  <img src="assets/head_en.png" alt="Telegram Control Bot for TrueConf Server" width="800" height="auto">
</p>

Der Administrator von [TrueConf
Server](https://trueconf.ru/products/tcsf/besplatniy-server-videoconferenciy.html)
kann über beliebte Messenger wie Telegram schnellen Zugriff auf wichtige
Serverinformationen erhalten. Dazu kann ein Bot erstellt werden, der mithilfe
der [TrueConf Server API](https://developers.trueconf.ru/api/server/) die
benötigten Daten abruft. Der Bot kann sowohl lokal auf dem eigenen Server als
auch auf einem beliebigen dedizierten Server platziert werden.

In diesem Beispiel zeigen wir, wie man einen Telegram-Bot erstellt und ihn auf
dem Online-Dienst Replit startet. Dabei stellen wir ein fertiges Beispiel für
die Implementierung der Aufgabe in Python bereit. Der vorgeschlagene Bot verfügt
über folgende Funktionen:

1. Überprüfung des Serverstatus (läuft/gestoppt).
2. Abrufen der Liste der laufenden Konferenzen.
3. Überprüfung der Anzahl der Online-Nutzer.
4. Suche nach längere Zeit versehentlich aktiven Konferenzen und Beendigung jeder
einzelnen.

Im weiteren Text werden fälschlicherweise gestartete Konferenzen der Einfachheit
halber als "vergessene" bezeichnet, das heißt, sie wurden vom Besitzer und den
Moderatoren nicht beendet. Ein Beispiel wäre ein Webinar, bei dem die Teilnehmer
es verlassen haben, während der Moderator die Client-Anwendung minimiert hat,
ohne das Ereignis zu stoppen. Es läuft weiter und, falls die Aufnahme aktiviert
war, nimmt es unnötig Platz auf der SSD oder HDD mit einer sich vergrößernden
Aufnahmedatei ein.

Zum Beispiel betrachten wir eine "vergessene" Konferenz als:

- sie dauert länger als eine Stunde;
- darin blieb nur der Besitzer oder der Moderator übrig;
- sie hat Teilnehmer, aber keiner von ihnen ist ein Moderator.

<div align="center"><img src="assets/example1.png" width="350"/></div>

## Erforderliche Voraussetzungen für den Start

Für den erfolgreichen Start des Bots müssen zwei Bedingungen erfüllt sein:

- jeder überwachte Server muss über seine IP-Adresse oder seinen DNS-Namen auf
dem PC erreichbar sein, auf dem der Bot ausgeführt wird;
- Der PC mit dem Bot muss über eine Internetverbindung verfügen.

> [!NOTE]
> Der bereitgestellte Code ist ein Beispiel, auf dessen Grundlage Sie Ihren eigenen Bot entwickeln können. Beachten Sie, dass die Sicherheit des Bots durch das OAuth 2.0-Protokoll und HTTPS sowie auf der Netzwerkseite(Zugriffsregeln, Firewall usw.) gewährleistet wird. Der Bot arbeitet im **long_polling** Modus und fragt eigenständig den Telegram-Server nach neuen Updates ab. Im Gegensatz zum **webhook** ist diese Verbindungsmethode in einer Unternehmensumgebung völlig sicher.

## Registrierung und Konfiguration Ihres Bots

Um den Telegram-Bot zu nutzen, benötigen Sie den offiziellen Bot
[BotFather](http://t.me/BotFather).

BotFather ist der einzige Bot, der Bots in Telegram verwaltet. Weitere
Informationen finden Sie in der [offiziellen
Dokumentation](https://core.telegram.org/bots).

Um einen Bot zu erstellen:

1. Öffnen Sie [BotFather](http://t.me/BotFather) und klicken Sie auf **Starten**
oder **Start**.
1. Es öffnet sich eine Liste mit den Funktionen des Bots. Sie benötigen den
Befehl `/newbot`. Klicken Sie darauf in der Liste oder senden Sie dem Bot
eine neue Nachricht mit `/newbot`.

> [!TIP] 
> In Zukunft kann die Liste der verfügbaren Befehle über die Tasten `Menü` (mobile Version), `/` (Desktop-Version) oder einfach durch Eingabe von `/` im Nachrichtenfeld im Chat mit BotFather geöffnet werden.

Als nächstes wird BotFather vorschlagen, den neuen Bot zu benennen. Überlegen Sie
sich einen Namen, zum Beispiel `TCS [name_org]`, wobei `[name_org]` der Name
Ihrer Organisation ist.

Erstellen Sie nun einen Benutzernamen (username) für Ihren Bot. Der Name muss
**unbedingt** das Wort `bot` enthalten, da dies eine Anforderung von Telegram
ist, zum Beispiel `tcs_[name_org]_bot`.

> [!NOTE]
> Beachten Sie, dass der Name des Bots und sein Benutzername öffentliche Namen sind, unter denen er über die globale Suche gefunden werden kann.

Als Antwort erhalten Sie eine Nachricht mit Informationen über den erstellten Bot
und einem Zugriffstoken dafür über das HTTP-API in der Form:

```text
5032177032:AAGahjzZ6zbWSEsVFj13Ki-YMPhPEPzQjxE
```

Klicken Sie auf das Token im Nachrichtentext, um es in die Zwischenablage zu
kopieren. Speichern Sie es anschließend an einem sicheren Ort, da Sie es später
für die Nutzung des Bots benötigen.

Um zu den Einstellungen Ihres Bots zu gelangen, führen Sie den Befehl `/mybots`
aus und wählen Sie den entsprechenden Benutzernamen aus. Es öffnet sich ein
Menü, in dem Sie Folgendes tun können:

- den aktuellen Token widerrufen, wobei ein neuer Token automatisch erstellt wird;
- Name, Begrüßungsnachricht, Beschreibung, Bild bearbeiten;
- Befehle hinzufügen.

Jetzt, da der Bot eingerichtet ist, können Sie mit seiner Ausführung fortfahren.

## Vorbereitung der Konfigurationsdatei

Zunächst müssen Sie eine Einstellungsdatei mit den Zugangsdaten zu Ihrem Bot und
den Serverparametern vorbereiten.

Kopieren Sie die Datei `settings.example.toml` in eine neue Datei `settings.toml`:

```sh
cp settings.example.toml settings.toml
```

Jetzt müssen Sie diese Datenstruktur korrekt ausfüllen.

**tg-api-token** — HTTP API Telegram-Zugriffstoken.

**tg-users-id** — Ihre numerische Telegram-ID. Telegram sorgt für die Sicherheit
des Zugriffs auf den Bot durch einzigartige Benutzer-IDs. Daher müssen Sie Ihre
Telegram-ID kennen, um eine Antwort vom Bot zu erhalten. Um diese zu erhalten,
senden Sie dem Bot [@userinfobot](http://t.me/userinfobot) eine beliebige
Nachricht.

> [!TIP]
> Wenn Sie möchten, dass mehrere Personen Zugriff auf den Bot erhalten, können Sie deren IDs durch ein Komma getrennt eingeben.

**locale** — der Sprachcode, in dem der Bot antworten wird. Sie können Phrasen korrigieren oder Ihre eigene Übersetzung im Ordner `app/locales` hinzufügen.

Ersetzen Sie in `[servers.<server_name>]` `<server_name>` durch den bevorzugten
Servernamen. Dieser wird im Titel der Schaltflächen angezeigt:

<div align="center"><img src="assets/example2.png" width="350"/></div>

**ip** — FQDN oder IP-Adresse des Servers.

**client_id**, **client_secret** werden Ihnen nach der Erstellung einer
OAuth2-Anwendung zur Verfügung stehen. Wie Sie diese erstellen können, erfahren
Sie in [unserer
Dokumentation](https://docs.trueconf.com/server/admin/web-config/#oauth2).

Für unser Beispiel müssen Sie im OAuth-Anwendung folgende Berechtigungen
festlegen:

- *conferences*;
- *users:read*;
- *logs.calls:read*;
- *logs.calls.participants:read*.

**server_status.state** — Aktivierung oder Deaktivierung der automatischen
Überprüfung der Serververfügbarkeit. Werte: `true` oder `false`.

**server_status.timeout** — die Zeit in Sekunden, nach der der Bot die
Verfügbarkeit des Servers überprüft (Aktiv, Inaktiv). Standardmäßig ist 15
Sekunden eingestellt, aber Sie können einen eigenen Wert eingeben.

**ssl_certificate** — Einstellung zur Überprüfung des TLS-Zertifikats. Wenn
`true`, wird jede Serveranfrage überprüft. Wenn Ihr Server ein selbstsigniertes
Zertifikat verwendet, geben Sie in diesem Parameter den Pfad dazu an (verwenden
Sie den Schrägstrich `/`). Wenn der Bot in einer vertrauenswürdigen Zone
verwendet wird (zum Beispiel, wenn sich der Server in Ihrem Firmennetzwerk
befindet und nur Sie darauf Zugriff haben), geben Sie `false` an – dies
deaktiviert die Zertifikatsüberprüfung. Wenn nichts angegeben ist `""`, ist das
gleichbedeutend mit `false`.

Nach dem Ausfüllen der Datei sollten Sie eine Struktur wie im folgenden Beispiel
erhalten:

```toml
tg-api-token = "12345:example_key"  
tg-users-id = [12345, 123456]  
locale = "de"

[servers]

[servers."video.example.com"]  
ip = "video.example.com"  
client_id = "86add683ebc98123968a549f8976db0024abe288"  
client_secret = "b7f3f5cb51b02634b1bb546eb7f1f905c93960ba"  
access_token = "a5bace995fd9d65315f36518fd7b3b4f68a69557"  
ssl_certificate = ""

[servers."video.example.com".server_status]  
state = true  
timeout = 15

[servers."video.example.net"]  
ip = "video.example.net"  
client_id = "1ebb5498ddd6668d7885c1597f9a1330fc0caddd"  
client_secret = "067171487c59f063287a44c40671d6247d647e42"  
access_token = ""  
ssl_certificate = true

[servers."video.example.net".server_status]  
state = 0  
timeout = 15
```

## Starten des Bots

1. Installieren Sie Python.
1. Laden Sie das Projekt herunter. Klicken Sie auf der Hauptseite des Repositorys
auf die Schaltfläche **Code → ZIP herunterladen**, und entpacken Sie das
heruntergeladene Archiv.
1. Installieren Sie `pipenv`:

```sh
pip install pipenv
```

4. Führen Sie die Installation der Abhängigkeiten durch. Geben Sie dazu im
Projektverzeichnis im Terminal den folgenden Befehl ein:

```sh
pipenv install --python 3.x
```

wo `--python 3.x` Ihre Python-Version ist. Wir empfehlen die Verwendung von 3.7
oder höher.

5. Starten Sie den Bot:

```sh
pipenv run python3 main.py
```

Bei erfolgreichem Start des Bots wird im Terminal die Meldung **Bot is running...** angezeigt.

## Starten eines Bots auf Cloud-Diensten

Sie können Ihren Bot nicht nur auf Ihrem lokalen Rechner, sondern auch in der Cloud ausführen, was für den kontinuierlichen Betrieb und die Erreichbarkeit von überall aus praktisch ist. Dafür können Sie verschiedene Cloud-Plattformen
nutzen, die praktische Werkzeuge für die Entwicklung, das Testen und den Betrieb von Anwendungen bieten. Nachfolgend listen wir einige beliebte Dienste auf, auf
denen Sie Ihren Bot ausführen können:

- **Replit** ist ein Dienst zum Ausführen und Entwickeln von Anwendungen direkt
im Browser.
- **Heroku** — eine Plattform zum Bereitstellen und Hosten von Anwendungen mit
einfacher Integration in GitHub.
- **Google Cloud Platform (GCP)** — eine leistungsstarke Plattform mit
umfangreichen Möglichkeiten für das Hosting und die Verwaltung von Anwendungen.
- **AWS (Amazon Web Services)** — eine Cloud-Plattform von Amazon für skalierbare
Anwendungen mit zahlreichen Tools und Diensten.
- **Microsoft Azure** ist eine Plattform zur Entwicklung und Verwaltung von
Anwendungen in der Cloud mit Integration in das Microsoft-Ökosystem.
- **Glitch** — ein Service für schnelles Hosting und die Entwicklung von
Anwendungen mit einfacher Benutzeroberfläche und Integration in GitHub.

Diese Dienste ermöglichen es nicht nur, einen Bot zu starten, sondern auch, ihn
leicht zu skalieren und seine Verfügbarkeit für Benutzer weltweit
sicherzustellen.
