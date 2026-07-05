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
// Sample values (replace these with API values)
let emiRatio = 19;
let score = 82;

// Financial Health Score
document.querySelector("progress").value = score;

// Risk Indicator
const risk = document.getElementById("riskIndicator");

if (emiRatio < 30) {
    risk.innerHTML = "🟢 Low Risk";
    risk.className = "low";
}
else if (emiRatio < 50) {
    risk.innerHTML = "🟡 Medium Risk";
    risk.className = "medium";
}
else {
    risk.innerHTML = "🔴 High Risk";
    risk.className = "high";
}

// Settlement Recommendation
let recommendation = "";

if (emiRatio < 30) {
    recommendation = "Your financial condition is healthy. Continue making regular EMI payments.";
}
else if (emiRatio < 50) {
    recommendation = "Consider discussing repayment options with your lender.";
}
else {
    recommendation = "High repayment burden detected. Consider loan restructuring or settlement discussions.";
}

document.getElementById("recommendation").innerHTML = recommendation;