document.getElementById("predictButton").addEventListener("click", function() {
    let coin = document.getElementById("coinInput").value.toLowerCase().trim();
    let days = document.getElementById("daysInput").value;

    if (!coin) {
        document.getElementById("result").innerHTML = "<span style='color:red;'>Please enter a cryptocurrency symbol (e.g., btc, eth).</span>";
        return;
    }

    if (!days || days <= 0) {
        document.getElementById("result").innerHTML = "<span style='color:red;'>Please enter a valid number of days.</span>";
        return;
    }

    fetch('/predict', {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ coin: coin, days: days })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            document.getElementById("result").innerHTML = `<span style="color: red;">${data.error}</span>`;
        } else {
            document.getElementById("result").innerHTML = `<strong>Predicted Prices:</strong> ${data.prices.join(', ')}`;
        }
    })
    .catch(error => {
        document.getElementById("result").innerHTML = "<span style='color:red;'>Error fetching data. Try again.</span>";
        console.error("Error:", error);
    });
});
