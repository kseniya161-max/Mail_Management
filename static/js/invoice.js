function parseNumber(value) {
    return parseFloat(String(value).replace(",", ".")) || 0;
}

function calculateItemTotal(itemForm) {
    const quantityInput = itemForm.querySelector('input[name$="-quantity"]');
    const priceInput = itemForm.querySelector('input[name$="-unit_price"]');
    const totalInput = itemForm.querySelector(".item-total");

    if (!quantityInput || !priceInput || !totalInput) {
        return 0;
    }

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

    const vat = subtotal * 0.22;
    const grandTotal = subtotal + vat;

    document.getElementById("subtotal").textContent = subtotal.toFixed(2);
    document.getElementById("vat").textContent = vat.toFixed(2);
    document.getElementById("grand-total").textContent = grandTotal.toFixed(2);
}

function fillPriceByProductName(input) {
    const productName = input.value;
    const options = document.querySelectorAll("#products-list option");

    options.forEach(function (option) {
        if (option.value === productName) {
            const price = option.dataset.price;
            const itemForm = input.closest(".item-form");
            const priceInput = itemForm.querySelector('input[name$="-unit_price"]');

            if (priceInput && price) {
                priceInput.value = price;
                calculateInvoiceTotals();
            }
        }
    });
}

function getTotalFormsInput() {
    return document.querySelector('input[name$="-TOTAL_FORMS"]');
}

function updateFormIndexes(form, newIndex) {
    form.innerHTML = form.innerHTML.replace(/-\d+-/g, `-${newIndex}-`);
    form.innerHTML = form.innerHTML.replace(/_\d+_/g, `_${newIndex}_`);
}

function clearNewForm(form) {
    form.querySelectorAll("input").forEach(function (input) {
        if (input.classList.contains("item-total")) {
            input.value = "0.00";
        } else if (input.type === "hidden") {
            input.value = "";
        } else {
            input.value = "";
        }
    });

    form.querySelectorAll("select").forEach(function (select) {
        select.selectedIndex = 0;
    });
}

function addNewItemForm() {
    const formsetDiv = document.getElementById("items");
    const totalForms = getTotalFormsInput();

    if (!formsetDiv || !totalForms) {
        console.error("Не найден formset или TOTAL_FORMS");
        return;
    }

    const currentFormCount = parseInt(totalForms.value, 10);
    const lastForm = formsetDiv.querySelector(".item-form:last-child");

    if (!lastForm) {
        console.error("Не найдена строка товара для копирования");
        return;
    }

    const newForm = lastForm.cloneNode(true);

    updateFormIndexes(newForm, currentFormCount);
    clearNewForm(newForm);

    formsetDiv.appendChild(newForm);
    totalForms.value = currentFormCount + 1;

    calculateInvoiceTotals();
}

document.addEventListener("DOMContentLoaded", function () {
    calculateInvoiceTotals();

    const addButton = document.getElementById("add-item");

    if (addButton) {
        addButton.addEventListener("click", function () {
            addNewItemForm();
        });
    }
});

document.addEventListener("input", function (event) {
    if (
        event.target.matches('input[name$="-quantity"]') ||
        event.target.matches('input[name$="-unit_price"]')
    ) {
        calculateInvoiceTotals();
    }
});

document.addEventListener("change", function (event) {
    if (event.target.matches('input[name$="-product_name_input"]')) {
        fillPriceByProductName(event.target);
    }
});

document.addEventListener("click", function (event) {
    if (event.target.classList.contains("remove-item")) {
        const itemForm = event.target.closest(".item-form");

        if (!itemForm) return;

        const totalForms = document.querySelector('input[name$="-TOTAL_FORMS"]');
        const forms = document.querySelectorAll(".item-form");

        // не даём удалить последнюю строку
        if (forms.length === 1) {
            itemForm.querySelectorAll("input").forEach(input => input.value = "");
            itemForm.querySelector(".item-total").value = "0.00";
            calculateInvoiceTotals();
            return;
        }

        itemForm.remove();

        totalForms.value = forms.length - 1;

        calculateInvoiceTotals();
    }
});