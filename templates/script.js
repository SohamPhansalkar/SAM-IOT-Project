console.log("JS connected");
var serverURL = "http://10.157.126.30:5000";

// Range slider
const rangeInput = document.getElementById("range4");
const rangeOutput = document.getElementById("rangeValue");
const toggleBtn = document.getElementById("toggleBtn");

rangeOutput.textContent = rangeInput.value;

// Slider changes threshold for auto mode
rangeInput.addEventListener("input", async function () {
  rangeOutput.textContent = this.value;
  await setThreshold(this.value);
  // Reset toggle button UI when using slider
  toggleBtn.textContent = "Turn: AUTO";
  toggleBtn.classList.remove("btn-outline-success", "btn-outline-warning");
  toggleBtn.classList.add("btn-outline-info");
});

// Toggle button function
let fanOn = true; // default state
async function toggleThreshold() {
  fanOn = !fanOn;
  const value = fanOn ? -1 : 100; // ON = -1, OFF = 100
  await setThreshold(value);

  if (fanOn) {
    toggleBtn.textContent = "Turn: ON";
    toggleBtn.classList.remove("btn-outline-warning", "btn-outline-info");
    toggleBtn.classList.add("btn-outline-success");
  } else {
    toggleBtn.textContent = "Turn: OFF";
    toggleBtn.classList.remove("btn-outline-success", "btn-outline-info");
    toggleBtn.classList.add("btn-outline-warning");
  }
}

// Send threshold to server
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

// Fetch sensor data
async function fetchData() {
  try {
    const response = await fetch(serverURL + "/get_data");
    const data = await response.json();

    document.getElementById("tempValue").textContent = data.temperature + "°C";
    document.getElementById("humidityValue").textContent = data.humidity + "%";
    document.getElementById("AQIValue").textContent = data.AQI;

    // Optional: update descriptions if you have desc function
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

setInterval(fetchData, 3000);
fetchData();

// Helper function for descriptions
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
