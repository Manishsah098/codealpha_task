const API_BASE = 'http://127.0.0.1:8000/api';
let menuItems = [];
let cart = [];
let tables = [
    { id: 1, number: 1 }, { id: 2, number: 2 }, { id: 3, number: 3 }, { id: 4, number: 4 }, { id: 5, number: 5 }
];
let selectedTable = null;
let searchQuery = '';

// Navigation
document.querySelectorAll('.nav-item').forEach(item => {
    item.addEventListener('click', (e) => {
        e.preventDefault();
        document.querySelectorAll('.nav-item').forEach(nav => nav.classList.remove('active'));
        item.classList.add('active');
        
        const target = item.dataset.target;
        document.querySelectorAll('.page-section').forEach(sec => sec.classList.remove('active'));
        document.getElementById(target).classList.add('active');

        if (target === 'admin-orders') {
            fetchOrders();
        }
    });
});

// Stats and alerts have been removed per user request

// Fetch Menu
async function fetchMenu() {
    try {
        const res = await fetch(`${API_BASE}/menu/`);
        menuItems = await res.json();
        renderMenu();
    } catch (err) {
        console.error("Menu fetching failed", err);
    }
}
// Search Logic
document.getElementById('menu-search').addEventListener('input', (e) => {
    searchQuery = e.target.value.toLowerCase();
    renderMenu();
});

function renderMenu() {
    const grid = document.getElementById('menu-grid');
    const filtered = menuItems.filter(item => 
        item.name.toLowerCase().includes(searchQuery) || 
        (item.cuisine && item.cuisine.toLowerCase().includes(searchQuery))
    );

    if (filtered.length === 0) {
        grid.innerHTML = '<div class="loading-state">No matching dishes found.</div>';
        return;
    }

    grid.innerHTML = filtered.map(item => `
        <div class="menu-card" data-id="${item.id}">
            <div class="diet-symbol ${item.is_veg ? 'veg' : 'non-veg'}" title="${item.is_veg ? 'Vegetarian' : 'Non-Vegetarian'}"><div class="circle"></div></div>
            <img src="${item.image_url || 'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=500&q=80'}" class="menu-item-img" alt="${item.name}">
            <h3>${item.name}</h3>
            <div class="cuisine-tag" style="font-size: 0.8rem; color: #8b5cf6; font-weight: 600; margin-bottom: 5px; text-transform: uppercase; letter-spacing: 0.5px;">
                <i class="fa-solid fa-utensils" style="font-size: 0.7rem;"></i> ${item.cuisine || 'General'}
            </div>
            <p>${item.description || 'Delicious freshly made recipe.'}</p>
            <div class="menu-details" style="font-size: 0.85rem; color: #a0aec0; margin: 10px 0;">
                <div><i class="fa-solid fa-star text-orange"></i> ${item.rating || '4.5'}</div>
                <div><i class="fa-solid fa-store"></i> ${item.restaurant_name || 'RMS Local'}</div>
                <div><i class="fa-solid fa-map-pin"></i> ${item.restaurant_address || '123 Developer Lane'}</div>
            </div>
            <div class="price">₹${parseFloat(item.price).toFixed(2)}</div>
            <button class="btn-add" ${!selectedTable ? 'disabled' : ''} onclick="window.addToCart(${item.id})">
                <i class="fa-solid fa-plus"></i> ${selectedTable ? 'Add to Order' : 'Select Table First'}
            </button>
        </div>
    `).join('');
}

// Cart Logic
window.addToCart = function(id) {
    const item = menuItems.find(m => m.id === id);
    if (!item) return;

    const existing = cart.find(c => c.menu_item === id);
    if (existing) {
        existing.quantity++;
    } else {
        cart.push({ menu_item: id, menu_item_name: item.name, price: item.price, quantity: 1 });
    }
    renderCart();
    showToast(`Added ${item.name} to order`);
}

window.updateQty = function(id, delta) {
    const existing = cart.find(c => c.menu_item === id);
    if(existing) {
        existing.quantity += delta;
        if(existing.quantity <= 0) {
            cart = cart.filter(c => c.menu_item !== id);
        }
    }
    renderCart();
}

window.removeItem = function(id) {
    cart = cart.filter(c => c.menu_item !== id);
    renderCart();
    showToast('Item removed');
}

function renderCart() {
    const container = document.getElementById('cart-items');
    const subtotalEl = document.getElementById('cart-subtotal');
    const taxEl = document.getElementById('cart-tax');
    const totalEl = document.getElementById('cart-total');
    const orderBtn = document.getElementById('place-order-btn');
    const tableSelect = document.getElementById('table-select');

    if (cart.length === 0) {
        container.innerHTML = '<p class="empty-cart-msg text-muted">Your order is empty.</p>';
        subtotalEl.textContent = '₹0.00';
        taxEl.textContent = '₹0.00';
        totalEl.textContent = '₹0.00';
        orderBtn.disabled = true;
        return;
    }

    let subtotal = 0;
    container.innerHTML = cart.map(item => {
        subtotal += item.price * item.quantity;
        return `
        <div class="cart-item">
            <div class="cart-item-details">
                <h4>${item.menu_item_name}</h4>
                <span class="text-blue font-bold">₹${(item.price * item.quantity).toFixed(2)}</span>
            </div>
            <div style="display: flex; align-items: center; gap: 12px;">
                <div class="cart-qty-controls">
                    <button onclick="window.updateQty(${item.menu_item}, -1)"><i class="fa-solid fa-minus"></i></button>
                    <span>${item.quantity}</span>
                    <button onclick="window.updateQty(${item.menu_item}, 1)"><i class="fa-solid fa-plus"></i></button>
                </div>
                <button onclick="window.removeItem(${item.menu_item})" style="background: none; border: none; color: #f87171; cursor: pointer; font-size: 1.1rem; padding: 5px;" title="Remove Item">
                    <i class="fa-solid fa-trash-can"></i>
                </button>
            </div>
        </div>
    `}).join('');

    const tax = subtotal * 0.05;
    const grandTotal = subtotal + tax;

    subtotalEl.textContent = `₹${subtotal.toFixed(2)}`;
    taxEl.textContent = `₹${tax.toFixed(2)}`;
    totalEl.textContent = `₹${grandTotal.toFixed(2)}`;
    orderBtn.disabled = !tableSelect.value;
}

// Populate Tables for demo
const tableSelect = document.getElementById('table-select');
tables.forEach(t => {
    const opt = document.createElement('option');
    opt.value = t.id;
    opt.textContent = `New Option: Table ${t.number}`;
    tableSelect.appendChild(opt);
});

document.getElementById('table-select').addEventListener('change', (e) => {
    selectedTable = e.target.value;
    Array.from(tableSelect.options).forEach(opt => {
        if (opt.value) {
            const tnum = tables.find(t => t.id == opt.value).number;
            opt.textContent = (opt.value === e.target.value) ? `Selected Table ${tnum}` : `Table ${tnum}`;
        }
    });
    renderMenu(); // Re-render to enable/disable buttons
    renderCart();
});

// Place Order
document.getElementById('place-order-btn').addEventListener('click', async () => {
    const table = document.getElementById('table-select').value;
    if(!table || cart.length === 0) return;

    const payload = {
        table: parseInt(table),
        items: cart.map(c => ({ menu_item: c.menu_item, quantity: c.quantity }))
    };

    try {
        const btn = document.getElementById('place-order-btn');
        btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Processing...';
        btn.disabled = true;

        const res = await fetch(`${API_BASE}/orders/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload) // Make sure payload format matches backend expects
        });

        const data = await res.json();

        if (res.ok) {
            showToast('Order Placed Successfully!');
            cart = [];
            renderCart();
            // Removed fetchStats and fetchAlerts here
            document.getElementById('table-select').value = "";
        } else {
            showToast(data.error || 'Failed to place order', true);
        }
    } catch (err) {
        showToast('Connection Error. Make sure backend is running.', true);
        console.error(err);
    } finally {
        const btn = document.getElementById('place-order-btn');
        btn.innerHTML = 'Place Order <i class="fa-solid fa-arrow-right"></i>';
        renderCart();
    }
});

function showToast(msg, isError = false) {
    const toast = document.getElementById('toast');
    toast.textContent = msg;
    if(isError) toast.classList.add('error');
    else toast.classList.remove('error');
    
    toast.classList.add('show');
    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

// Clear Cart
document.getElementById('clear-cart-btn').addEventListener('click', () => {
    if (cart.length === 0) return;
    if (confirm('Clear all items from your current order?')) {
        cart = [];
        renderCart();
        showToast('Order cleared');
    }
});

// Admin Orders Logic
async function fetchOrders() {
    const container = document.getElementById('orders-container');
    container.innerHTML = '<div class="loading-state"><i class="fa-solid fa-spinner fa-spin"></i> Loading orders...</div>';

    try {
        const res = await fetch(`${API_BASE}/orders/all/`);
        const orders = await res.json();
        renderOrders(orders);
    } catch (err) {
        container.innerHTML = '<div class="loading-state error text-red">Failed to load orders.</div>';
        console.error(err);
    }
}

function renderOrders(orders) {
    const container = document.getElementById('orders-container');
    if (orders.length === 0) {
        container.innerHTML = '<div class="loading-state">No orders found.</div>';
        return;
    }

    container.innerHTML = orders.map(order => {
        const date = new Date(order.created_at).toLocaleString();
        const itemsHtml = order.items.map(item => `
            <div class="order-item-row">
                <span>${item.quantity}x ${item.menu_item_name}</span>
                <span>₹${(item.price * item.quantity).toFixed(2)}</span>
            </div>
        `).join('');

        let actionBtn = '';
        if (order.status === 'pending') {
            actionBtn = `<button class="btn-status-update btn-verify" onclick="updateOrderStatus(${order.id}, 'preparing')">Verify & Send to Waiter</button>`;
        } else if (order.status === 'preparing') {
            actionBtn = `<button class="btn-status-update btn-complete" onclick="updateOrderStatus(${order.id}, 'completed')">Mark Completed</button>`;
        }

        return `
            <div class="order-card anim-fade-in">
                <div class="order-card-header">
                    <div>
                        <div class="order-id">Order #${order.id}</div>
                        <div class="order-time">${date}</div>
                        <div style="font-size: 0.8rem; color: #60a5fa; margin-top: 4px;">Table ${order.table || 'N/A'}</div>
                    </div>
                    <span class="status-badge status-${order.status}">${order.status}</span>
                </div>
                <div class="order-items-list">
                    ${itemsHtml}
                </div>
                <div class="order-card-footer">
                    <div class="order-total">₹${parseFloat(order.total_amount).toFixed(2)}</div>
                    ${actionBtn}
                </div>
            </div>
        `;
    }).join('');
}

async function updateOrderStatus(orderId, newStatus) {
    try {
        const res = await fetch(`${API_BASE}/orders/${orderId}/status/`, {
            method: 'PATCH',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ status: newStatus })
        });

        if (res.ok) {
            showToast(`Order #${orderId} set to ${newStatus}`);
            fetchOrders();
        } else {
            showToast('Failed to update order status', true);
        }
    } catch (err) {
        showToast('Connection error', true);
        console.error(err);
    }
}

// Global exposure for onclick handlers
window.updateOrderStatus = updateOrderStatus;

document.getElementById('refresh-orders-btn').addEventListener('click', fetchOrders);

// Profile Dropdown Toggle
const profileBtn = document.getElementById('profile-btn');
const profileDropdown = document.getElementById('profile-dropdown');

if (profileBtn && profileDropdown) {
    profileBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        profileDropdown.style.display = profileDropdown.style.display === 'none' ? 'flex' : 'none';
        
        if (profileDropdown.style.display === 'flex') {
            profileDropdown.style.animation = 'fadeIn 0.2s ease';
        }
    });

    document.addEventListener('click', (e) => {
        if (!profileDropdown.contains(e.target)) {
            profileDropdown.style.display = 'none';
        }
    });
}

// Logout Logic
document.querySelector('#profile-dropdown a[style*="#ef4444"]').addEventListener('click', (e) => {
    e.preventDefault();
    if (confirm('Are you sure you want to logout?')) {
        cart = [];
        selectedTable = null;
        document.getElementById('table-select').value = '';
        renderMenu();
        renderCart();
        // Go to dashboard
        document.querySelector('.nav-item[data-target="dashboard"]').click();
        showToast('Logged out successfully');
        profileDropdown.style.display = 'none';
    }
});

// Initial Load
fetchMenu();
