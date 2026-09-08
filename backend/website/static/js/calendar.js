let currentDate = new Date();
currentDate.setDate(1);

// Dátumhatárok beállítása (Mai nap és 1 évvel későbbi nap)
const today = new Date();
today.setHours(0, 0, 0, 0);

const maxDate = new Date();
maxDate.setFullYear(today.getFullYear() + 1);
maxDate.setHours(0, 0, 0, 0);

let startDate = null;
let endDate = null;

function renderCalendars() {
    renderSingleCalendar(currentDate, 'monthTitle1', 'calendarGrid1');
    
    const nextMonthDate = new Date(currentDate.getFullYear(), currentDate.getMonth() + 1, 1);
    renderSingleCalendar(nextMonthDate, 'monthTitle2', 'calendarGrid2');
}

function renderSingleCalendar(dateObj, titleId, gridId) {
    const grid = document.getElementById(gridId);
    grid.innerHTML = '';

    const year = dateObj.getFullYear();
    const month = dateObj.getMonth();

    const monthName = dateObj.toLocaleString('hu-HU', { month: 'long', year: 'numeric' });
    document.getElementById(titleId).innerText = monthName;

    const days = ['H', 'K', 'Sze', 'Cs', 'P', 'Szo', 'V'];
    days.forEach(d => grid.innerHTML += `<div class="day-name">${d}</div>`);

    let firstDayIndex = new Date(year, month, 1).getDay() - 1;
    if (firstDayIndex === -1) firstDayIndex = 6;

    const totalDays = new Date(year, month + 1, 0).getDate();

    // Üres mezők a hónap kezdése előtt
    for (let i = 0; i < firstDayIndex; i++) {
        grid.innerHTML += `<div class="day disabled"></div>`;
    }

    // Napok kirajzolása és validálása
    for (let day = 1; day <= totalDays; day++) {
        const thisDate = new Date(year, month, day);
        thisDate.setHours(0, 0, 0, 0);

        const cell = document.createElement('div');
        cell.className = 'day';
        cell.innerText = day;

        // Érvényesség ellenőrzése: Múltbeli vagy 1 évnél távolabbi?
        const isDisabled = thisDate < today || thisDate > maxDate;

        if (isDisabled) {
            cell.classList.add('disabled');
            cell.style.pointerEvents = 'none';
            cell.style.opacity = '0.3';
        } else {
            applyStyles(cell, thisDate);
            cell.onclick = () => selectDate(thisDate);
        }

        grid.appendChild(cell);
    }
}

function applyStyles(cell, date) {
    const time = date.getTime();

    if (startDate && endDate) {
        if (time === startDate.getTime()) cell.classList.add('selected-start');
        else if (time === endDate.getTime()) cell.classList.add('selected-end');
        else if (time > startDate.getTime() && time < endDate.getTime()) cell.classList.add('selected-full');
    } else if (startDate && time === startDate.getTime()) {
        cell.classList.add('selected-start');
    }
}

function selectDate(date) {
    if (!startDate || (startDate && endDate)) {
        startDate = date;
        endDate = null;
    } else if (date > startDate) {
        endDate = date;
    } else {
        startDate = date;
        endDate = null;
    }

    if (startDate) {
        const formattedStart = formatDate(startDate);
        document.getElementById('check_in').value = formattedStart;
        document.getElementById('check_in_display').value = formattedStart;
    } else {
        document.getElementById('check_in').value = '';
        document.getElementById('check_in_display').value = '';
    }

    if (endDate) {
        const formattedEnd = formatDate(endDate);
        document.getElementById('check_out').value = formattedEnd;
        document.getElementById('check_out_display').value = formattedEnd;
    } else {
        document.getElementById('check_out').value = '';
        document.getElementById('check_out_display').value = '';
    }

    renderCalendars();
}

function formatDate(d) {
    const year = d.getFullYear();
    const month = String(d.getMonth() + 1).padStart(2, '0');
    const day = String(d.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
}

function changeMonth(direction) {
    const newDate = new Date(currentDate.getFullYear(), currentDate.getMonth() + direction, 1);
    
    // A legkorábbi megjeleníthető hónap (a jelenlegi hónap)
    const minMonthDate = new Date(today.getFullYear(), today.getMonth(), 1);
    
    // A legkésőbbi megjeleníthető hónap (1 év múlva)
    const maxMonthDate = new Date(maxDate.getFullYear(), maxDate.getMonth(), 1);

    // Csak akkor engedjük a lapozást, ha a megengedett tartományban maradunk
    if (newDate >= minMonthDate && newDate <= maxMonthDate) {
        currentDate = newDate;
        renderCalendars();
    }
}

document.addEventListener('DOMContentLoaded', renderCalendars);