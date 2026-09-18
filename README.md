🏨 Szállodairányítási Rendszer

📖 A projektről

Ez a projekt egy modern, Django alapú szállodairányítási rendszer, amely a szálloda mindennapi operatív folyamatainak digitalizálását és egyszerűsítését célozza.

A rendszer külön felületet biztosít a vendégek, a recepciósok, a takarító személyzet és a karbantartók számára. A modulok közötti együttműködésnek és a dinamikus állapotfrissítéseknek köszönhetően a szálloda működése átláthatóbbá, gyorsabbá és hatékonyabbá válik.

A projekt egy fiktív szálloda működését modellezi, és a szoftverfejlesztő- és tesztelő vizsgaremek részeként készült.

🎯 A projekt célja

A rendszer célja, hogy egyetlen központi platformon kezelje a szálloda legfontosabb folyamatait:

vendégek és foglalások kezelése,

online foglalási igények feldolgozása,

szobák foglaltsági és takarítási állapotának követése,

vendégkérések kezelése,

műszaki hibák bejelentése és nyomon követése,

takarítási feladatok kezelése,

recepciós adminisztráció támogatása,

korábbi takarítási és karbantartási események visszakeresése.

✨ Főbb funkciók

🔐 Bejelentkezés és jogosultságkezelés

A rendszer központi bejelentkezési felületet használ, amely a felhasználó szerepköre alapján a megfelelő kezelőfelületre irányítja a felhasználót.

Támogatott szerepkörök:

👤 Vendég

🛎️ Recepciós

🧹 Takarító

🔧 Karbantartó

A vendégek kizárólag a saját szobájukhoz kapcsolódó információkat érhetik el.

🛏️ Vendégoldali felület

A vendégek saját szobájukból kezelhetik a különböző kéréseiket, például:

takarítás kérése,

extra ágynemű,

extra törölköző,

fürdőszobai bekészítés,

szemét kiürítése,

ébresztési kérés,

műszaki hibabejelentés.

Az egyedi igények szöveges mezőben is megadhatók.

🔄 Dinamikus állapotkövetés

A vendég által elküldött hibák és kérések állapota nyomon követhető.

A személyzet visszajelzései megjelennek a vendég számára, a lezárt feladatok pedig automatikusan kikerülnek az aktív feladatok közül.

🔧 Karbantartói kezelőfelület

A karbantartók külön felületen látják a bejelentett műszaki hibákat.

A feladatkártyák tartalmazzák többek között:

szobaszámot,

bejelentés időpontját,

probléma leírását,

aktuális státuszt,

karbantartói megjegyzést.

A hiba elhárítása után a feladat lezárható.

🛎️ Recepciós vezérlőpult

A recepciós dashboard egy központi helyen jeleníti meg a szálloda legfontosabb aktuális adatait.

Többek között kezelhető:

check-in,

check-out,

tartózkodás hosszabbítása,

érkező vendégek,

távozó vendégek,

aktív karbantartási feladatok,

ébresztési kérések,

szobák aktuális állapota,

online foglalási igények.

🧹 Szobák állapotának követése

A szobák állapotát színkódolt rendszer segíti:

Szín

Állapot

🔴 Piros

Takarítást nem kér

🟡 Sárga

Takarítás szükséges

🔵 Kék

Takarítás alatt

🟢 Zöld

Takarítva

Ez lehetővé teszi, hogy a recepció és a takarító személyzet gyorsan átlássa a szálloda aktuális állapotát.

📊 Előzmények és analitika

A rendszer lehetőséget biztosít a korábbi események visszakeresésére.

Szűrhető például:

szobaszám alapján,

időintervallum alapján.

Nyomon követhetők a korábbi:

takarítási feladatok,

karbantartási hibák,

feladatstátuszok,

kezdési és befejezési időpontok,

karbantartói megjegyzések.

🌐 Online foglalás

A nyilvános weboldalon keresztül a vendégek foglalási igényt küldhetnek be.

A foglalási űrlapon megadható többek között:

érkezés és távozás dátuma,

szobatípus,

teljes név,

e-mail cím,

telefonszám,

felnőttek száma,

gyermekek száma.

A recepciós ezeket az igényeket egy külön felületen tudja feldolgozni, majd szabad szobát rendelhet hozzá és elfogadhatja vagy elutasíthatja a foglalást.

🧹 Takarítói dashboard

A takarító személyzet napi munkáját összesítő dashboard támogatja.

Megjelennek például:

takarítást igénylő szobák,

extra ágynemű kérések,

extra törölköző kérések,

fürdőszobai bekészítések,

szemétürítési kérések.

A takarítás folyamata:

Takarítás szükséges → Takarítás alatt → Takarítva

A rendszer a munkakezdés és a befejezés időpontját is naplózza.

🗄️ Adatbázis

A rendszer központi adatmodellje öt fontos entitás köré épül:

Guest – vendégek adatai

Room – szobák adatai és aktuális állapotai

Reservation – foglalások

RoomIssue – műszaki hibák

CleaningTask – takarítási feladatok

Egyszerűsített kapcsolati modell:

Guest
  │
  └──── Reservation ──── Room
                           │
                           ├──── RoomIssue
                           │
                           └──── CleaningTask

🛠️ Technológiák

A projekt fejlesztéséhez az alábbi technológiákat és eszközöket használtuk:

Python

Django

Django ORM

Django Authentication

HTML / CSS

JavaScript

Visual Studio Code

A Django biztosítja a backend működését, az adatkezelést, az autentikációt és az adminisztrációs felületet.

🧪 Tesztelés és validáció

A fejlesztés során külön figyelmet kapott az online foglalási rendszer validációja.

A tesztelés során problémát jelentett, hogy korábban múltbeli, illetve túl távoli dátumokra is lehetett foglalási igényt létrehozni.

A megoldás két szinten került kialakításra:

Frontend validáció

A JavaScript alapú naptár:

letiltja a múltbeli dátumokat,

letiltja az egy évnél távolabbi dátumokat,

megakadályozza az érvénytelen hónapokra történő lapozást,

vizuális visszajelzést ad az érvénytelen dátumokról.

Backend validáció

A Django backend oldalon is megtörténik a dátumok ellenőrzése, így egy manipulált HTTP-kérés sem tud érvénytelen időintervallumra foglalást létrehozni.

⚙️ Telepítés

1. Repository klónozása

git clone <repository-url>
cd <repository-folder>

2. Virtuális környezet létrehozása

Windows:

python -m venv venv
venv\Scripts\activate

Linux / macOS:

python3 -m venv venv
source venv/bin/activate

3. Függőségek telepítése

Ha a repository tartalmaz requirements.txt fájlt:

pip install -r requirements.txt

4. Adatbázis migrációk

python manage.py migrate

5. Admin felhasználó létrehozása

python manage.py createsuperuser

6. Fejlesztői szerver indítása

python manage.py runserver

Ezután a projekt a Django által megadott helyi fejlesztői címen érhető el.

Megjegyzés: A pontos környezeti változók, adatbázis-beállítások és további telepítési lépések a projekt aktuális repository-struktúrájától függenek.

👥 Felhasználói szerepkörök

Szerepkör

Fő feladat

👤 Vendég

Saját szoba, kérések, hibabejelentés és egyéb szolgáltatások kezelése

🛎️ Recepciós

Foglalások, vendégek, szobák és napi adminisztráció kezelése

🧹 Takarító

Takarítási feladatok és extra kérések kezelése

🔧 Karbantartó

Műszaki hibák kezelése és lezárása

⚙️ Adminisztrátor

Felhasználók, jogosultságok és adatbázis kezelése

🖥️ Django Admin

A rendszer a Django beépített adminisztrációs felületét is használja.

Az adminisztrációs felületen kezelhetők többek között:

felhasználók és jogosultsági csoportok,

vendégek,

szobák,

foglalások,

takarítási feladatok,

műszaki hibák.

🚀 Továbbfejlesztési lehetőségek

A projekt további fejlesztési irányai között szerepelnek:

teljes körű tartózkodás-hosszabbítás,

szobaszerviz és éttermi rendelés,

éttermi kezelőfelület,

éttermi asztalfoglalás,

wellness időpontfoglalás,

wellness kezelőfelület,

publikus éttermi és wellness foglalás,

részletes szobabemutató oldalak,

képgalériák,

interaktív felszereltségi listák.

📈 A rendszer előnyei

A rendszer célja, hogy csökkentse a szálloda belső kommunikációs terheit, valamint egyszerűbbé tegye az egyes részlegek közötti együttműködést.

A központi rendszer segítségével:

📌 átláthatóbbá válnak a napi feladatok,

📌 gyorsabban továbbíthatók a vendégkérések,

📌 könnyebben követhetők a műszaki hibák,

📌 egyszerűbbé válik a takarítás szervezése,

📌 naprakész információ áll rendelkezésre a szobákról,

📌 visszakereshetők a korábbi események,

📌 egyszerűbbé válik az online foglalások kezelése.

👨‍💻 Készítők

Róka Tamara
Komoróczy László Balázs

Szoftverfejlesztő- és tesztelő vizsgaremek — 2026

📄 Projekt dokumentáció

A projekt részletes dokumentációja tartalmazza a rendszer bemutatását, fejlesztői környezetét, funkcióit, adatbázis-modelljét, tesztelését és továbbfejlesztési lehetőségeit.
