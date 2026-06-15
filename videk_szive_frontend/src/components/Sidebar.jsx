const Sidebar = () => {
    return (
        <aside className="sidebar">
            <div className="logo">
                <img src="images/header_logo_white.png" alt="" />
            </div>
            <div className="login-box">
                <h3>Bejelentkezés</h3>
                <input type="text" placeholder="Felhasználónév" />
                <input type="password" placeholder="Jelszó" />
                <button>Belépés</button>
            </div>
            <nav>
                <a href="#" className="active">Áttekintés</a>
                <a href="#">Szobák</a>
                <a href="#">Feladatok</a>
                <a href="#">Üzenetek</a>
                <a href="#">Statisztika</a>
                <a href="#">Beállítások</a>
            </nav>
            <div className="logout">
                <img src="images/logout.png" /><br />
                Kijelentkezés
            </div>
        </aside>
    )
}

export default Sidebar