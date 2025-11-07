document.addEventListener("DOMContentLoaded", () => {
  const activitiesList = document.getElementById("activities-list");
  const activitySelect = document.getElementById("activity");
  const signupForm = document.getElementById("signup-form");
  const messageDiv = document.getElementById("message");

  // Weather Dashboard Elements
  const locationInput = document.getElementById("location-input");
  const fetchWeatherBtn = document.getElementById("fetch-weather-btn");
  const refreshWeatherBtn = document.getElementById("refresh-weather-btn");
  const weatherDisplay = document.getElementById("weather-display");
  const weatherError = document.getElementById("weather-error");

  // Function to fetch weather data
  async function fetchWeather(location) {
    try {
      weatherError.classList.add("hidden");
      weatherDisplay.classList.add("hidden");

      const response = await fetch(
        `/weather?location=${encodeURIComponent(location)}`
      );

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || "Failed to fetch weather data");
      }

      const data = await response.json();

      // Update weather display
      document.getElementById("weather-location").textContent = data.location;
      document.getElementById("weather-temperature").textContent =
        data.temperature?.toFixed(1) || "N/A";
      document.getElementById("weather-conditions").textContent =
        data.conditions || "N/A";
      document.getElementById("weather-feels-like").textContent =
        data.feels_like ? `${data.feels_like.toFixed(1)}°F` : "N/A";
      document.getElementById("weather-humidity").textContent = data.humidity
        ? `${data.humidity}%`
        : "N/A";
      document.getElementById("weather-wind").textContent = data.wind_speed
        ? `${data.wind_speed.toFixed(1)} mph`
        : "N/A";
      
      const precip = data.precipitation || 0;
      const precipUnit = precip === 1 ? "inch" : "inches";
      document.getElementById("weather-precipitation").textContent = 
        `${precip} ${precipUnit}`;

      if (data.timestamp) {
        const timestamp = new Date(data.timestamp);
        document.getElementById("weather-timestamp").textContent =
          `Last updated: ${timestamp.toLocaleString()}`;
      }

      weatherDisplay.classList.remove("hidden");
      refreshWeatherBtn.classList.remove("hidden");
    } catch (error) {
      weatherError.textContent = error.message;
      weatherError.classList.remove("hidden");
      console.error("Error fetching weather:", error);
    }
  }

  // Event listeners for weather
  fetchWeatherBtn.addEventListener("click", () => {
    const location = locationInput.value.trim() || "New York";
    fetchWeather(location);
  });

  refreshWeatherBtn.addEventListener("click", () => {
    const location = locationInput.value.trim() || "New York";
    fetchWeather(location);
  });

  locationInput.addEventListener("keypress", (event) => {
    if (event.key === "Enter") {
      event.preventDefault();
      const location = locationInput.value.trim() || "New York";
      fetchWeather(location);
    }
  });

  // Load default weather on page load
  fetchWeather("New York");

  // Function to fetch activities from API
  async function fetchActivities() {
    try {
      const response = await fetch("/activities");
      const activities = await response.json();

      // Clear loading message
      activitiesList.innerHTML = "";

      // Populate activities list
      Object.entries(activities).forEach(([name, details]) => {
        const activityCard = document.createElement("div");
        activityCard.className = "activity-card";

        const spotsLeft = details.max_participants - details.participants.length;
        
        // Build participants list HTML
        let participantsHtml = '';
        if (details.participants.length > 0) {
          participantsHtml = `
            <div class="participants-section">
              <strong>Current Participants:</strong>
              <ul class="participants-list">
                ${details.participants.map(p => `<li>${p}</li>`).join('')}
              </ul>
            </div>
          `;
        } else {
          participantsHtml = '<p class="no-participants">No participants yet. Be the first to sign up!</p>';
        }

        activityCard.innerHTML = `
          <h4>${name}</h4>
          <p>${details.description}</p>
          <p><strong>Schedule:</strong> ${details.schedule}</p>
          <p><strong>Availability:</strong> ${spotsLeft} spots left</p>
          ${participantsHtml}
        `;

        activitiesList.appendChild(activityCard);

        // Add option to select dropdown
        const option = document.createElement("option");
        option.value = name;
        option.textContent = name;
        activitySelect.appendChild(option);
      });
    } catch (error) {
      activitiesList.innerHTML = "<p>Failed to load activities. Please try again later.</p>";
      console.error("Error fetching activities:", error);
    }
  }

  // Handle form submission
  signupForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const email = document.getElementById("email").value;
    const activity = document.getElementById("activity").value;

    try {
      const response = await fetch(
        `/activities/${encodeURIComponent(activity)}/signup?email=${encodeURIComponent(email)}`,
        {
          method: "POST",
        }
      );

      const result = await response.json();

      if (response.ok) {
        messageDiv.textContent = result.message;
        messageDiv.className = "success";
        signupForm.reset();
      } else {
        messageDiv.textContent = result.detail || "An error occurred";
        messageDiv.className = "error";
      }

      messageDiv.classList.remove("hidden");

      // Hide message after 5 seconds
      setTimeout(() => {
        messageDiv.classList.add("hidden");
      }, 5000);
    } catch (error) {
      messageDiv.textContent = "Failed to sign up. Please try again.";
      messageDiv.className = "error";
      messageDiv.classList.remove("hidden");
      console.error("Error signing up:", error);
    }
  });

  // Initialize app
  fetchActivities();
});
