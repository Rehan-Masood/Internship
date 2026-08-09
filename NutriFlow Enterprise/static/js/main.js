let cart = [];

function addToCart(id, name, price) {
    const existing = cart.find(item => item.id === id);
    if (existing) {
        existing.qty += 1;
    } else {
        cart.push({ 
            id: id, 
            name: name, 
            price: parseFloat(price), 
            qty: 1 
        });
    }
    renderCart();
}

function updateQty(id, delta) {
    const item = cart.find(i => i.id === id);
    if (item) {
        item.qty += delta;
        if (item.qty <= 0) {
            cart = cart.filter(i => i.id !== id);
        }
    }
    renderCart();
}

function removeFromCart(id) {
    cart = cart.filter(item => item.id !== id);
    renderCart();
}

function renderCart() {
    const container = document.getElementById('cartItems');
    const totalElem = document.getElementById('cartTotal');
    const inputElem = document.getElementById('cartDataInput');
    
    if (!container) return;
    
    container.innerHTML = '';
    let total = 0;

    cart.forEach(item => {
        const itemTotal = item.price * item.qty;
        total += itemTotal;

        const row = document.createElement('div');
        row.className = 'cart-item';
        row.innerHTML = `
            <div>
                <b style="color: #f8fafc;">${item.name}</b><br>
                <small style="color: var(--text-muted);">$${item.price.toFixed(2)} each</small>
            </div>
            <div class="qty-controls">
                <button class="qty-btn" type="button" onclick="updateQty(${item.id}, -1)">-</button>
                <span style="font-size: 0.9rem; font-weight: 700; padding: 0 0.2rem;">${item.qty}</span>
                <button class="qty-btn" type="button" onclick="updateQty(${item.id}, 1)">+</button>
                <button type="button" onclick="removeFromCart(${item.id})" style="background:none; border:none; color: #ef4444; margin-left: 0.4rem; cursor:pointer;">✕</button>
            </div>
        `;
        container.appendChild(row);
    });

    if (totalElem) {
        totalElem.innerText = `$${total.toFixed(2)}`;
    }
    
    if (inputElem) {
        inputElem.value = JSON.stringify(cart);
    }
}