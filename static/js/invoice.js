function parseNumber(value) {
    return parseFloat(String(value).replace(",", ".")) || 0;
}

function calculateItemTotal(itemForm) {
    const quantityInput = itemForm.querySelector('input[name$="-quantity"]');
    const priceInput = itemForm.querySelector('input[name$="-unit_price"]');
    const totalInput = itemForm.querySelector(".item-total");

    const quantity = parseNumber(quantityInput.value);
    const price = parseNumber(priceInput.value);

    const total = quantity * price;

    totalInput.value = total.toFixed(2);

    return total;
}

function calculateInvoiceTotals() {
    const itemForms = document.querySelectorAll(".item-form");

    let subtotal = 0;

    itemForms.forEach(function (itemForm) {
        subtotal += calculateItemTotal(itemForm);
    });

    const vatRate = 0.22;
    const vat = subtotal * vatRate;
    const grandTotal = subtotal + vat;

    document.getElementById("subtotal").textContent = subtotal.toFixed(2);
    document.getElementById("vat").textContent = vat.toFixed(2);
    document.getElementById("grand-total").textContent = grandTotal.toFixed(2);
}

document.addEventListener("input", function (event) {
    if (
        event.target.matches('input[name$="-quantity"]') ||
        event.target.matches('input[name$="-unit_price"]')
    ) {
        calculateInvoiceTotals();
    }
});

document.addEventListener("DOMContentLoaded", function () {
    calculateInvoiceTotals();
});