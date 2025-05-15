const calendarContainer = document.querySelector(".calendar-container");

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
    day.classList.remove("selected", "afternoon", "morning", "full");
    // Do NOT remove "occupied" here, as those are set by the backend
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

    const dayDate = new Date(`${dateStr}T00:00:00Z`);
    if (dayDate < today) {
      dayDiv.classList.add("disabled");
    }
    if (startDate && !endDate && dayDate < startDate) {
      dayDiv.classList.add("disabled");
    }

    // --- Mark occupied days ---
    const isOccupied = occupiedDates.some(occ =>
      normalizeDate(dayDate) >= occ.startDate && normalizeDate(dayDate) <= occ.endDate
    );
    if (isOccupied) {
      dayDiv.classList.add("occupied");
      dayDiv.classList.add("disabled"); // Prevent clicking
    }

    dayDiv.addEventListener("click", () => handleDateSelection(dayDiv));
    calendar.appendChild(dayDiv);
  }

  highlightOccupiedDates(occupiedDates, currentMonth, currentYear, lastDay);
  persistUserSelection(startDate, endDate, currentMonth, currentYear, lastDay);
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
  // No need to highlight occupied days here, as they're handled in updateCalendar
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

    highlightRange(start, end);
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
  endDate
) {
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

// Deselect selected dates if you click on the calendar container but NOT on a day
calendarContainer.addEventListener("click", function (e) {
  // Only clear if you click directly on the container (not a day or any child)
  if (e.target === calendarContainer) {
    startDate = null;
    endDate = null;
    selectingStart = true;
    clearSelection();
    updateCalendar();
  }
});

// Modal open/close logic
const openModalBtn = document.getElementById("openModalBtn");
const bookingDialog = document.getElementById("bookingDialog");
const closeDialogBtn = document.getElementById("closeDialog");

if (openModalBtn && bookingDialog) {
  openModalBtn.addEventListener("click", () => {
    if (!startDate || !endDate) {
      alert("Please select the arrival and departure dates.");
      return;
    }
    bookingDialog.showModal();
  });
}

if (closeDialogBtn && bookingDialog) {
  closeDialogBtn.addEventListener("click", () => {
    bookingDialog.close();
  });
}
//#endregion

//#endregion