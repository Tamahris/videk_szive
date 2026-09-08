let lastVersion = null;

async function checkVersion() {
    try {
        const response = await fetch("/dashboard/version/?t=" + Date.now(), {
            cache: "no-store"
        });

        const data = await response.json();

        console.log("Aktuális:", data.version);
        console.log("Előző:", lastVersion);

        
        if (lastVersion === null) {
            lastVersion = data.version;
            return;
        }

        if (data.version != lastVersion) {
            console.log("Verzió változott → oldal frissítése");
            window.location.reload();
            return;
        }

    } catch (error) {
        console.error("Verzió ellenőrzési hiba:", error);
    }
}

checkVersion();
setInterval(checkVersion, 2000);