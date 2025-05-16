//# finds the first 'calendar container' item within the styles file and returns ii
const calendarContainer = document.querySelector(".calendar-container");

//#region Booking & Calendar Logic

//#sets up variables - 'querySelector' items come from styles.css doc, 'getElementById' come from HTML using id tag
const calendar = document.querySelector(".calendar");
const currentMonthYear = document.getElementById("currentMonthYear");
const prevMonthBtn = document.getElementById("prevMonthBtn");
const nextMonthBtn = document.getElementById("nextMonthBtn");

//# creates a date object representing today's date
let today = new Date(
  Date.UTC(
    new Date().getUTCFullYear(),
    new Date().getUTCMonth(),
    new Date().getUTCDate()
  )
);
//# Stores elements of today
let currentMonth = today.getUTCMonth();
let currentYear = today.getUTCFullYear();

//# selectingStart to stores whether the user is selecting the start date (true) or the end date (false) - toggles depending which stage of the selection process they are in
//# two variables store start and end date of the booking
let selectingStart = true;
let startDate = null;
let endDate = null;
//#endregion

//# Converts a JS Date object into a string - so that it works with HTML
function normalizeDate(date) {
  return date.toISOString().split("T")[0]; // Get YYYY-MM-DD format
}

function isDateInRange(date, rangeStart, rangeEnd) {
  return normalizeDate(date) >= rangeStart && normalizeDate(date) <= rangeEnd;
}

//# removes all selection and status classes from every calendar day tile
function clearSelection() {
  document.querySelectorAll(".day").forEach((day) => {
    day.classList.remove("selected", "afternoon", "morning", "full");
  });
}

//#region Main Calculations
//#redraws the calendar for the current month and year
function updateCalendar() {
  calendar.innerHTML = "";

  //# calculates month boundaries
  const firstDay = new Date(Date.UTC(currentYear, currentMonth, 1));
  const lastDay = new Date(Date.UTC(currentYear, currentMonth + 1, 0));
  const daysInMonth = lastDay.getUTCDate();

  //# displays current month and year at top of calendar
  currentMonthYear.textContent = `${firstDay.toLocaleString("default", {
    month: "long",
  })} ${currentYear}`;

  //#disables previous month bytton if calendar on current month
  prevMonthBtn.disabled =
    currentYear == today.getUTCFullYear() &&
    currentMonth == today.getUTCMonth();

    //# loop creating day tiles
  for (let i = 1; i <= daysInMonth; i++) {
    const dayDiv = document.createElement("div");
    dayDiv.className = "day";

    const span = document.createElement("span");
    span.textContent = i;

    const dateStr = `${currentYear}-${String(currentMonth + 1).padStart(2, "0")}-${String(i).padStart(2, "0")}`;
    dayDiv.dataset.date = dateStr;

    dayDiv.appendChild(span);

    const dayDate = new Date(`${dateStr}T00:00:00Z`);

    // Disable if before today
    if (dayDate < today) {
      dayDiv.classList.add("disabled", "occupied");
    }
    // Disable if outside selectable range
    else if (!isDateInRange(dayDate, selectableRange.start, selectableRange.end)) {
      dayDiv.classList.add("disabled", "occupied");
    }
    // Disable if in occupiedDates
    else if (occupiedDates.some(occ =>
      normalizeDate(dayDate) >= occ.startDate && normalizeDate(dayDate) <= occ.endDate
    )) {
      dayDiv.classList.add("disabled", "occupied");
    }
    // Disable if before selected start date (when picking end date)
    else if (startDate && !endDate && dayDate < startDate) {
      dayDiv.classList.add("disabled");
    }

    //# listens for user clicking on a day, then applies the handle date selection function below
    dayDiv.addEventListener("click", () => handleDateSelection(dayDiv));
    calendar.appendChild(dayDiv);
  }

  //# when the calendar is redrawn (e.g. after changing months) it checks for existing user date selections
  //# if they exist, it plots them, to ensure they are not lost
  persistUserSelection(startDate, endDate, currentMonth, currentYear, lastDay);
}
//#endregion

//# Handles what happens if a user clicks a date
// #if selecting start date, checks if it's available, sets startdate var, and redraws
//# if selecting end date, checks for overlaps, sets enddate var and redraws
function handleDateSelection(dayDiv) {
  const selectedDate = new Date(`${dayDiv.dataset.date}T00:00:00Z`);

  if (selectingStart) {
    if (
      occupiedDates.find((x) => x.startDate == normalizeDate(selectedDate)) ||
      !isDateInRange(selectedDate, selectableRange.start, selectableRange.end)
    ) {
      alert("Arrival date is not available.");
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

//# Below function is a helper function used for occupied dates, and for the dates the user is currently selecting
//# When called with an object from OccupiedDates - it highlights booked / unavailable days
//# When called with the users current selection - it highlights the user's current range

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

//# Highlights the occupied dates
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

//#region EventListeners - scroll through months when user clicks the arrows
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
    // Format and display the selected dates in the dialog
    const options = { weekday: 'short', month: 'short', day: 'numeric', year: 'numeric' };
    const startStr = startDate.toLocaleDateString(undefined, options);
    const endStr = endDate.toLocaleDateString(undefined, options);

    // Update selected dates
    const selectedDatesDiv = document.getElementById("selectedDates");
    if (selectedDatesDiv) {
      selectedDatesDiv.textContent = `${startStr} - ${endStr}`;
    }

    // Calculate nights and price
    const msPerDay = 24 * 60 * 60 * 1000;
    const nights = Math.round((endDate - startDate) / msPerDay);
    const total = nights * pricePerNight;

    // Update price per night in dialog
    const priceDiv = document.getElementById("price");
    if (priceDiv) {
      priceDiv.textContent = `£${pricePerNight} per night`;
    }

    // Update nights and total in summary
    const nightsCountSpan = document.getElementById("nightsCount");
    if (nightsCountSpan) {
      nightsCountSpan.textContent = nights;
    }
    const totalPriceSpan = document.getElementById("totalPrice");
    if (totalPriceSpan) {
      totalPriceSpan.textContent = `£${total.toFixed(2)}`;
    }

    //# This section finds the hidden input fields for start and end date in the booking form (HTML)
    //# It sets their values to the selected start and end date formatted as 'YYYY-MM-DD'
    //# Then it opens the booking form so the user can review it and submit
    //# important that this info is passed into the form correctly so it will move through the HTML, into Python code and into database
    const startDateInput = document.getElementById("startDateInput");
    const endDateInput = document.getElementById("endDateInput");
    if (startDateInput) startDateInput.value = startDate ? startDate.toISOString().split("T")[0] : "";
    if (endDateInput) endDateInput.value = endDate ? endDate.toISOString().split("T")[0] : "";

    bookingDialog.showModal();
  });
}

//# These functions allow you to click off the booking form and it will disappear

if (closeDialogBtn && bookingDialog) {
  closeDialogBtn.addEventListener("click", () => {
    bookingDialog.close();
  });
}

if (bookingDialog) {
  bookingDialog.addEventListener("click", function (e) {
    if (e.target === bookingDialog) {
      bookingDialog.close();
    }
  });
}
//#endregion

//#endregion