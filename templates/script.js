console.log("JS connected");

var serverURL = "http://192.168.29.119:5000";

// Range slider
const rangeInput = document.getElementById("range4");
const rangeOutput = document.getElementById("rangeValue");

rangeOutput.textContent = rangeInput.value;

async function setThreshold(num) {
  try {
    const response = await fetch(serverURL + "/set_threshold", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ threshold: num }),
    });
    const result = await response.json();
    console.log("Threshold updated:", result);
  } catch (error) {
    console.error("Error sending threshold:", error);
  }
}

rangeInput.addEventListener("input", function () {
  rangeOutput.textContent = this.value;
  setThreshold(this.value);
});

// Manual toggle button
async function manualToggle() {
  try {
    const response = await fetch(serverURL + "/manual_toggle", {
      method: "POST",
    });
    const result = await response.json();
    console.log("Manual Toggle Response:", result);

    const toggleBtn = document.getElementById("toggleBtn");
    if (result.manual_toggle === 1) {
      toggleBtn.textContent = "Manual Toggle : ON";
      toggleBtn.classList.remove("btn-outline-success");
      toggleBtn.classList.add("btn-outline-warning");
    } else {
      toggleBtn.textContent = "Manual Toggle : OFF";
      toggleBtn.classList.remove("btn-outline-warning");
      toggleBtn.classList.add("btn-outline-success");
    }
  } catch (error) {
    console.error("Error toggling manually:", error);
  }
}

// Helper for descriptions
function desc(val, type) {
  if (type === "temp") {
    if (val < 0) return "Freezing";
    if (val < 10) return "Very Cold";
    if (val < 20) return "Cold";
    if (val < 30) return "Warm";
    if (val < 40) return "Hot";
    return "Scorching";
  } else if (type === "humidity") {
    if (val < 20) return "Very Dry";
    if (val < 40) return "Dry";
    if (val < 60) return "Comfortable";
    if (val < 80) return "Humid";
    return "Very Humid";
  } else if (type === "AQI") {
    if (val <= 50) return "Good";
    if (val <= 100) return "Moderate";
    if (val <= 150) return "Unhealthy for Sensitive Groups";
    if (val <= 200) return "Unhealthy";
    if (val <= 300) return "Very Unhealthy";
    return "Hazardous";
  }
}

// Fetch sensor data
async function fetchData() {
  try {
    const response = await fetch(serverURL + "/get_data");
    const data = await response.json();

    document.getElementById("tempValue").textContent = data.temperature + "°C";
    document.getElementById("humidityValue").textContent = data.humidity + "%";
    document.getElementById("AQIValue").textContent = data.AQI;

    document.getElementById("tempDesc").textContent = desc(
      data.temperature,
      "temp"
    );
    document.getElementById("humidityDesc").textContent = desc(
      data.humidity,
      "humidity"
    );
    document.getElementById("AQIDesc").textContent = desc(data.AQI, "AQI");
  } catch (error) {
    console.error("Error fetching data:", error);
  }
}

// Refresh every 3 seconds
setInterval(fetchData, 3000);
fetchData(); // Initial fetch
