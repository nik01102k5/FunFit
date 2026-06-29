let waterIntake = 0;
let waterGoal = 3;

// 🔹 Load data from backend
window.onload = function () {
    fetch('/api/water')
        .then(res => res.json())
        .then(data => {
            waterIntake = data.intake;
            waterGoal = data.goal;
            updateWaterUI();
            if (data.points !== undefined) {
                updatePoints(data.points);
            }
        });
};

function addWater(amount) {
    waterIntake += amount;

    if (waterIntake > waterGoal) {
        waterIntake = waterGoal;
    }

    // 🔹 Send to backend
    fetch("/api/water", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            intake: waterIntake
        })
    })
        .then(res => res.json())
        .then(data => {
            updateWaterUI();

            // 🎉 Celebration + points
            if (data.reward) {
                celebrate();
                updatePoints(data.points);
            }
        });
}

function updateWaterUI() {
    let percent = (waterIntake / waterGoal) * 100;

    document.getElementById("water-text").innerText =
        waterIntake.toFixed(1) + "L / " + waterGoal + "L";

    document.getElementById("water-bar").style.width = percent + "%";
}

// 🎉 Celebration
function celebrate() {

    for (let i = 0; i < 20; i++) {
        let confetti = document.createElement("div");
        confetti.className = "confetti";
        confetti.style.left = Math.random() * 100 + "vw";
        document.body.appendChild(confetti);

        setTimeout(() => confetti.remove(), 2000);
    }
}

// 💰 Update points UI
function updatePoints(points) {
    let el = document.querySelector(".points-text");
    if (el) el.innerText = points;
}