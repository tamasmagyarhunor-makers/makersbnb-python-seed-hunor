const calendarContainer = document.querySelector(".calendar-container");
const calendar = document.querySelector(".calendar");
const currentMonthYear = document.getElementById("currentMonthYear");
const prevMonthBtn = document.getElementById("prevMonthBtn");
const nextMonthBtn = document.getElementById("nextMonthBtn");

let today = new Date(
  Date.UTC(
    new Date().getUTCFullYear(),
    new Date().getUTCMonth(),
    new Date().getUTCDate()
  )
);
let currentMonth = today.getUTCMonth();
let currentYear = today.getUTCFullYear();

let selectingStart = true;
let startDate = null;
let endDate = null;

// Helper Functions
function normalizeDate(date) {
  return date.toISOString().split("T")[0]; // Get YYYY-MM-DD format
}

function clearSelection() {
  document.querySelectorAll(".day").forEach((day) => {
    day.classList.remove("selected");
  });
}

function updateHiddenInputs() {
  const startDateInput = document.getElementById("startDateInput");
  const endDateInput = document.getElementById("endDateInput");
  if (startDateInput) startDateInput.value = startDate ? normalizeDate(startDate) : "";
  if (endDateInput) endDateInput.value = endDate ? normalizeDate(endDate) : "";
}

// Main Calculations
function updateCalendar() {
  calendar.innerHTML = "";

  const firstDay = new Date(Date.UTC(currentYear, currentMonth, 1));
  const lastDay = new Date(Date.UTC(currentYear, currentMonth + 1, 0));
  const daysInMonth = lastDay.getUTCDate();

  currentMonthYear.textContent = `${firstDay.toLocaleString("default", {
    month: "long",
  })} ${currentYear}`;

  prevMonthBtn.disabled =
    currentYear == today.getUTCFullYear() &&
    currentMonth == today.getUTCMonth();

  for (let i = 1; i <= daysInMonth; i++) {
    const dayDiv = document.createElement("div");
    dayDiv.className = "day";

    const span = document.createElement("span");
    span.textContent = i;

    const dateStr = `${currentYear}-${String(currentMonth + 1).padStart(2, "0")}-${String(i).padStart(2, "0")}`;
    dayDiv.dataset.date = dateStr;

    dayDiv.appendChild(span);

    const dayDate = new Date(`${dateStr}T00:00:00Z`);
    if (dayDate < today) {
      dayDiv.classList.add("disabled");
      dayDiv.classList.add("occupied"); // Mark as occupied
    }
    if (startDate && !endDate && dayDate < startDate) {
      dayDiv.classList.add("disabled");
    }

    dayDiv.addEventListener("click", () => handleDateSelection(dayDiv));
    calendar.appendChild(dayDiv);
  }

  persistUserSelection(startDate, endDate, currentMonth, currentYear, lastDay);
}

function handleDateSelection(dayDiv) {
  const selectedDate = new Date(`${dayDiv.dataset.date}T00:00:00Z`);

  if (selectingStart) {
    if (selectedDate < today) {
      alert("Cannot select a date before today.");
      return;
    }
    startDate = selectedDate;
    endDate = null; // Reset end date
    clearSelection();
    updateCalendar();
    selectingStart = false;
  } else {
    if (selectedDate <= startDate) {
      alert("End date must be after the start date.");
      return;
    }
    endDate = selectedDate;
    selectingStart = true;
  }
  updateCalendar();
  updateHiddenInputs(); // Update hidden fields for form submission
}

function persistUserSelection(
  startDate,
  endDate,
  currentMonth,
  currentYear,
  lastDay
) {
  if (startDate && endDate) {
    highlightRange(startDate, endDate);
  } else if (
    startDate &&
    !endDate &&
    startDate.getUTCMonth() == currentMonth &&
    startDate.getUTCFullYear() == currentYear
  ) {
    highlightRange(startDate, null); // Only highlight the start date
  }
}

function highlightRange(startDate, endDate) {
  if (!startDate) return;

  const allDays = document.querySelectorAll(".day");
  allDays.forEach((day) => {
    const dayDate = new Date(`${day.dataset.date}T00:00:00Z`);

    if (normalizeDate(startDate) === normalizeDate(dayDate) && !endDate) {
      day.classList.add("selected");
      return;
    }
    if (
      endDate &&
      normalizeDate(dayDate) >= normalizeDate(startDate) &&
      normalizeDate(dayDate) <= normalizeDate(endDate)
    ) {
      day.classList.add("selected");
    }
  });
}

// EventListeners
prevMonthBtn.addEventListener("click", () => {
  currentMonth--;
  if (currentMonth < 0) {
    currentMonth = 11;
    currentYear--;
  }
  updateCalendar();
});

nextMonthBtn.addEventListener("click", () => {
  currentMonth++;
  if (currentMonth > 11) {
    currentMonth = 0;
    currentYear++;
  }
  updateCalendar();
});

updateCalendar();

// Deselect selected dates if you click on the calendar container but NOT on a day
calendarContainer.addEventListener("click", function (e) {
  // Only clear if you click directly on the container (not a day or any child)
  if (e.target === calendarContainer) {
    startDate = null;
    endDate = null;
    selectingStart = true;
    clearSelection();
    updateCalendar();
    updateHiddenInputs();
  }
});

// Toggle calendar when "Search by Date" button is clicked
document.addEventListener("DOMContentLoaded", function() {
  const calendarSection = document.getElementById("calendarSection");
  const selectDatesBtn = document.getElementById("selectDatesBtn");
  if (calendarSection && selectDatesBtn) {
    selectDatesBtn.addEventListener("click", function() {
      if (calendarSection.style.display === "block") {
        calendarSection.style.display = "none";
      } else {
        calendarSection.style.display = "block";
        calendarSection.scrollIntoView({ behavior: "smooth" });
      }
    });
  }
});