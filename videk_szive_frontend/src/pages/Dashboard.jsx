import RoomCard from "../components/RoomCard"
import Sidebar from "../components/Sidebar"

const Dashboard = () => {
  return (
    <div class="layout">
     <Sidebar />
     <main class="main">
        <h1>Recepció</h1>
        <div class="rooms-grid">
            <RoomCard status={"cleaning-needed"} name={"Horváth Lilla"} roomNumber={"106"} startDate={"2025.05.19"} endDate={"2025.05.23"} />
            <RoomCard status={"occupied"} name={"Kovács Anna"} roomNumber={"101"} startDate={"2025.05.20"} endDate={"2025.05.24"} />
            <RoomCard status={"cleaning-needed"} name={"Teszt Elek"} roomNumber={"101"} startDate={"2025.05.20"} endDate={"2025.05.24"} />
        </div>
     </main>
    </div>
  )
}

export default Dashboard