let globalSelectedRoomPrice = 0;
let currentActiveStep = 1;

function goToStep(step) {
    if (step > 1) {
        const requiredInputs = document.querySelectorAll('#step-1 [required]');
        for (let input of requiredInputs) {
            if (!input.value) {
                alert("Kérjük, töltsön ki minden kötelező (*) mezőt a vendégadatoknál!");
                return;
            }
        }
    }
    
    if (step === 3) {
        const roomSelected = document.querySelector('input[name="selected_room"]:checked');
        if (!roomSelected) {
            alert("Kérjük, válasszon ki egy szabad szobát a folytatáshoz!");
            return;
        }
        compileSummary(); 
    }

    currentActiveStep = step;

    document.querySelectorAll('.form-step').forEach(el => el.style.display = 'none');
    document.getElementById('step-' + step).style.display = 'block';

    for (let i = 1; i <= 3; i++) {
        const badge = document.getElementById('step-badge-' + i);
        if (badge) {
            badge.classList.remove('active-badge', 'done-step-badge');

            if (i === step) {
                badge.classList.add('active-badge');
            } else if (i < step) {
                badge.classList.add('done-step-badge');
            }
        }
    }
}

function nextStep(step) {
    goToStep(step);
}

function prevStep(step) {
    goToStep(step);
}

function updateSummaryDetails(num, type, persons, price) {
    document.getElementById('sum-room-num').innerText = num + ". szoba";
    document.getElementById('sum-room-type').innerText = type;
    document.getElementById('sum-room-persons').innerText = persons + " fő";
    globalSelectedRoomPrice = parseInt(price) || 0;
}

function compileSummary() {
    const name = document.querySelector('input[name="guest_name"]').value;
    const personalId = document.querySelector('input[name="personal_id"]').value;
    const phone = document.querySelector('input[name="phone_number"]').value || '-';
    const arrive = document.getElementById('id_arrive_date').value;
    const leave = document.getElementById('id_leave_date').value;

    document.getElementById('sum-name').innerText = name || '-';
    document.getElementById('sum-id').innerText = personalId || '-';
    document.getElementById('sum-phone').innerText = phone;
    document.getElementById('sum-dates').innerText = (arrive && leave) ? (arrive + " - " + leave) : '-';

    const selectedRoomInput = document.querySelector('input[name="selected_room"]:checked');
    if (selectedRoomInput) {
        selectedRoomInput.dispatchEvent(new Event('change'));
    }

    if (arrive && leave) {
        const date1 = new Date(arrive);
        const date2 = new Date(leave);
        const diffTime = date2 - date1;
        const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
        
        if (diffDays > 0) {
            const totalPrice = diffDays * globalSelectedRoomPrice;
            document.getElementById('sum-total-price').innerText = totalPrice.toLocaleString('hu-HU');
        } else {
            document.getElementById('sum-total-price').innerText = '0';
        }
    }
}

document.addEventListener("DOMContentLoaded", function() {
    const selectedRoomInput = document.querySelector('input[name="selected_room"]:checked');
    if (selectedRoomInput) {
        selectedRoomInput.dispatchEvent(new Event('change'));
    }
});