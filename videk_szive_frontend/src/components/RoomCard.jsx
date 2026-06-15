const RoomCard = ({ status, roomNumber, name, startDate, endDate }) => {
    const validStatus = ["occupied", "cleaning-needed", "cleaning", "done"]

    if (!validStatus.includes(status)) {
        console.error(`Nincs olyan status hogy ${status}!`)
    }

    return (
        <div className={`room ${status}`}>
            <h3>{roomNumber}</h3>
            <p>{name}</p>
            <p>{startDate} - {endDate}</p>
            {
                status !== "cleaning-needed" && status !== "cleaning" &&
                <>
                <button class="primary">Check-out</button>
                <button>Takarítás kérése</button>
                </>
            }

            { status == "cleaning" && <p>Takarítás alatt</p> }
            { status == "cleaning-needed" && <p>Takarítás szükséges</p> }

        </div>
    )
}

export default RoomCard