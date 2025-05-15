document.addEventListener("DOMContentLoaded", function () {
  const showCalendarBtn = document.getElementById("showCalendarBtn");
  const calendarContainer = document.querySelector(".calendar-container");
  if (showCalendarBtn && calendarContainer) {
    showCalendarBtn.addEventListener("click", () => {
      calendarContainer.classList.toggle("active");
      showCalendarBtn.textContent = calendarContainer.classList.contains("active")
        ? "Hide Calendar"
        : "Show Calendar";
    });
  }
});

//#region finds the first 'calendar container' item within the styles file and returns it
const calendarContainer = document.querySelector(".calendar-container");
//#endregion

//#region Booking & Calendar Logic

//#region Starting Variables
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
//#endregion

//#region Predefined Dates -> Integrate DB Here
const occupiedDates = [
  { startDate: "2024-12-10", endDate: "2024-12-15" },
  { startDate: "2024-12-03", endDate: "2024-12-04" },
  { startDate: "2024-12-08", endDate: "2024-12-10" },
  { startDate: "2024-12-29", endDate: "2025-01-03" },
  { startDate: "2025-03-01", endDate: "2025-05-02" },
];
occupiedDates.sort((a, b) => {
  return (
    new Date(`${a.startDate}T00:00:00Z`) - new Date(`${b.startDate}T00:00:00Z`)
  );
});
//#endregion

//#region Helper Functions
function normalizeDate(date) {
  return date.toISOString().split("T")[0]; // Get YYYY-MM-DD format
}

function clearSelection() {
  document.querySelectorAll(".day").forEach((day) => {
    day.classList.remove("afternoon", "morning", "full", "disabled");
  });
}

function disableFullyOccupiedTiles() {
  document.querySelectorAll(".day").forEach((day) => {
    if (
      day.classList.contains("full") ||
      (day.classList.contains("morning") && day.classList.contains("afternoon"))
    ) {
      day.classList.add("disabled");
    }
  });
}
//#endregion

//#region Main Calculations
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

    const dateStr = `${currentYear}-${String(currentMonth + 1).padStart(
      2,
      "0"
    )}-${String(i).padStart(2, "0")}`;
    dayDiv.dataset.date = dateStr;

    dayDiv.appendChild(span);

    //If the date have already passed then disable those tiles
    const dayDate = new Date(`${dateStr}T00:00:00Z`);
    if (dayDate < today) {
      dayDiv.classList.add("disabled");
    }
    if (startDate && !endDate && dayDate < startDate) {
      dayDiv.classList.add("disabled");
    }

    dayDiv.addEventListener("click", () => handleDateSelection(dayDiv));
    calendar.appendChild(dayDiv);
  }

  highlightOccupiedDates(occupiedDates, currentMonth, currentYear, lastDay);
  disableFullyOccupiedTiles();
  persistUserSelection(startDate, endDate, currentMonth, currentYear, lastDay);
}
//#endregion

//#region Hidden Input Updater
const startDateInput = document.getElementById("start_date");
const endDateInput = document.getElementById("end_date");

function updateHiddenInputs() {
  if (startDateInput) startDateInput.value = startDate ? normalizeDate(startDate) : "";
  if (endDateInput) endDateInput.value = endDate ? normalizeDate(endDate) : "";
}
//#endregion

function handleDateSelection(dayDiv) {
  const selectedDate = new Date(`${dayDiv.dataset.date}T00:00:00Z`);

  if (selectingStart) {
    if (occupiedDates.find((x) => x.startDate == normalizeDate(selectedDate))) {
      alert("Arrival date is already booked");
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
    // check if selection is overlapping

    const noOverlaps = occupiedDates.every((occupiedDate) => {
      const isOverlapping =
        (normalizeDate(startDate) > occupiedDate.startDate &&
          normalizeDate(startDate) < occupiedDate.endDate) ||
        (occupiedDate.startDate > normalizeDate(startDate) &&
          occupiedDate.startDate < normalizeDate(selectedDate));
      return !isOverlapping;
    });
    if (!noOverlaps) {
      alert("You are trying to book already booked dates.");
      return;
    }
    endDate = selectedDate;
    selectingStart = true;
  }
  updateCalendar();
  updateHiddenInputs();
}

function calculateHighlightRange(
  occupation,
  currentMonth,
  currentYear,
  lastDay
) {
  const startingDate = new Date(`${occupation.startDate}T00:00:00Z`);
  const endingDate = new Date(`${occupation.endDate}T00:00:00Z`);

  if (
    startingDate.getUTCMonth() !== currentMonth ||
    startingDate.getUTCFullYear() !== currentYear
  ) {
    let d = new Date(startingDate);
    let monthStartDate = null;
    while (!monthStartDate && d <= endingDate) {
      if (
        d.getUTCMonth() === currentMonth &&
        d.getUTCFullYear() === currentYear
      ) {
        monthStartDate = new Date(d);
      }
      d.setUTCDate(d.getUTCDate() + 1);
    }

    if (
      endingDate.getUTCMonth() > currentMonth ||
      endingDate.getUTCFullYear() > currentYear
    ) {
      return { start: monthStartDate, end: lastDay };
    } else {
      return { start: monthStartDate, end: endingDate };
    }
  } else {
    return { start: startingDate, end: endingDate };
  }
}

function highlightOccupiedDates(
  occupiedDates,
  currentMonth,
  currentYear,
  lastDay
) {
  occupiedDates.forEach((occupation) => {
    const { start, end } = calculateHighlightRange(
      occupation,
      currentMonth,
      currentYear,
      lastDay
    );
    if (!start || !end) return;

    const displayFullStart = normalizeDate(start) > occupation.startDate;
    const displayFullEnd = normalizeDate(end) < occupation.endDate;

    if (displayFullStart && displayFullEnd) {
      highlightRange(start, end, false, false);
    } else if (displayFullStart) {
      highlightRange(start, end, false, true);
    } else if (displayFullEnd) {
      highlightRange(start, end, true, false);
    } else {
      highlightRange(start, end);
    }
  });
}

function persistUserSelection(
  startDate,
  endDate,
  currentMonth,
  currentYear,
  lastDay
) {
  if (startDate && endDate) {
    const { start, end } = calculateHighlightRange(
      {
        startDate: normalizeDate(startDate),
        endDate: normalizeDate(endDate),
      },
      currentMonth,
      currentYear,
      lastDay
    );

    if (!start || !end) return;

    const displayFullStart = normalizeDate(start) > normalizeDate(startDate);
    const displayFullEnd = normalizeDate(end) < normalizeDate(endDate);

    if (displayFullStart && displayFullEnd) {
      highlightRange(start, end, false, false);
    } else if (displayFullStart) {
      highlightRange(start, end, false, true);
    } else if (displayFullEnd) {
      highlightRange(start, end, true, false);
    } else {
      highlightRange(start, end);
    }
  } else if (
    startDate &&
    !endDate &&
    startDate.getUTCMonth() == currentMonth &&
    startDate.getUTCFullYear() == currentYear
  ) {
    highlightRange(startDate, null); // Only highlight the start date
  }
}

function highlightRange(
  startDate,
  endDate,
  startTriangle = true,
  endTriangle = true
) {
  if (!startDate) return;

  const allDays = document.querySelectorAll(".day");
  allDays.forEach((day) => {
    const dayDate = new Date(`${day.dataset.date}T00:00:00Z`);

    if (normalizeDate(startDate) === normalizeDate(dayDate) && !endDate) {
      day.classList.add("afternoon");
      return;
    }
    if (
      endDate &&
      normalizeDate(dayDate) >= normalizeDate(startDate) &&
      normalizeDate(dayDate) <= normalizeDate(endDate)
    ) {
      if (
        normalizeDate(dayDate) === normalizeDate(startDate) &&
        startTriangle
      ) {
        day.classList.add("afternoon");
      } else if (
        normalizeDate(dayDate) === normalizeDate(endDate) &&
        endTriangle
      ) {
        day.classList.add("morning");
      } else {
        day.classList.add("full");
      }
    }
  });
}
//#endregion

//#region EventListeners
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
//#endregion

//#endregion

// --- Optional: Output selected dates to a visible div ---
// If you want to show the selected dates to the user, uncomment below:

// const openModalBtn = document.querySelector(".open-modal-btn");
// const selectedDatesDiv = document.getElementById("selected-dates");

// openModalBtn.addEventListener("click", (e) => {
//   if (!startDate || !endDate) {
//     e.preventDefault();
//     alert("Please select the arrival and departure dates.");
//     return;
//   }
//   selectedDatesDiv.textContent = `Selected dates: ${normalizeDate(startDate)} to ${normalizeDate(endDate)}`;
// });