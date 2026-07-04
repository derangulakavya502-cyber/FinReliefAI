// ------------------------------
// Sample Financial Data
// ------------------------------

const financialData = {
    income: 50000,
    expenses: 20000,
    emi: 9680,
    surplus: 20320,
    ratio: 19,
    status: "Healthy ✅"
};

// ------------------------------
// Update Dashboard Cards
// ------------------------------

document.getElementById("income").textContent =
    "₹" + financialData.income.toLocaleString();

document.getElementById("expenses").textContent =
    "₹" + financialData.expenses.toLocaleString();

document.getElementById("emi").textContent =
    "₹" + financialData.emi.toLocaleString();

document.getElementById("surplus").textContent =
    "₹" + financialData.surplus.toLocaleString();

document.getElementById("ratio").textContent =
    financialData.ratio + "%";

document.getElementById("status").textContent =
    financialData.status;


// ------------------------------
// Bar Chart
// ------------------------------

new Chart(document.getElementById("barChart"), {

    type: "bar",

    data: {

        labels: ["Income", "Expenses", "EMI"],

        datasets: [{

            label: "Amount (₹)",

            data: [

                financialData.income,

                financialData.expenses,

                financialData.emi

            ]

        }]

    },

    options: {

        responsive: true,

        plugins: {

            legend: {

                display: false

            }

        }

    }

});


// ------------------------------
// Pie Chart
// ------------------------------

new Chart(document.getElementById("pieChart"), {

    type: "pie",

    data: {

        labels: [

            "Expenses",

            "EMI",

            "Remaining Surplus"

        ],

        datasets: [{

            data: [

                financialData.expenses,

                financialData.emi,

                financialData.surplus

            ]

        }]

    },

    options: {

        responsive: true

    }

});