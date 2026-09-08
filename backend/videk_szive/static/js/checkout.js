function processCheckoutSearch() {
    const select = document.getElementById('checkout_room_select');
    
    if (!select || !select.value) {
        alert("Kérjük, válasszon ki egy szobát a listából!");
        return;
    }

    const selectedOption = select.options[select.selectedIndex];

    const hiddenInput = document.getElementById('hidden_checkout_room_number');
    if (hiddenInput) {
        hiddenInput.value = select.value;
    }

    document.getElementById('out-sum-room').innerText = select.value + ". szoba";
    document.getElementById('out-sum-name').innerText = selectedOption.getAttribute('data-guest') || '-';
    document.getElementById('out-sum-type').innerText = selectedOption.getAttribute('data-type') || '-';
    
    const price = selectedOption.getAttribute('data-price');
    document.getElementById('out-sum-price').innerText = price ? parseInt(price).toLocaleString('hu-HU') : '0';
    
    document.getElementById('out-sum-issues').innerText = selectedOption.getAttribute('data-issues') || 'Nincs';
    document.getElementById('out-sum-wakeup').innerText = selectedOption.getAttribute('data-wakeup') || 'Nem';

    document.getElementById('checkout-step-1').style.display = 'none';
    document.getElementById('checkout-step-2').style.display = 'block';
}

function backToCheckoutSearch() {
    document.getElementById('checkout-step-2').style.display = 'none';
    document.getElementById('checkout-step-1').style.display = 'block';
}