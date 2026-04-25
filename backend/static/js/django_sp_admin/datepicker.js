/**
 * Date Picker Widget
 *
 * Handles date selection via calendar grid with month/year navigation.
 * Supports multiple pickers on the same page through container-scoped state.
 */

document.addEventListener('DOMContentLoaded', () => {
  // Event delegation for all date picker interactions
  document.addEventListener('click', dp_handleOpenButton);
  document.addEventListener('click', dp_handleDateCellClick);
  document.addEventListener('click', dp_handleYesterdayButton);
  document.addEventListener('click', dp_handleTodayButton);
  document.addEventListener('click', dp_handleTomorrowButton);

  document.addEventListener('change', dp_handleMonthSelectChange);
  document.addEventListener('change', dp_handleYearInputChange);

  document.addEventListener('mousedown', dp_handleNavButtonMouseDown);
  document.addEventListener('mouseup', dp_handleNavButtonMouseUp);

  document.addEventListener('click', dp_handleOutsideClick);
});

/**
 * Get the closest date picker container from an element
 */
function dp_getContainer(element) {
  return element.closest('[data-dp-container]');
}

/**
 * Parse date string in YYYY-MM-DD format
 */
function dp_parseDate(dateStr) {
  if (!dateStr) {
    return null;
  }
  const parts = dateStr.trim().split('-');
  if (parts.length !== 3) {
    return null;
  }
  const year = Number.parseInt(parts[0], 10);
  const month = Number.parseInt(parts[1], 10) - 1; // JS months are 0-11
  const day = Number.parseInt(parts[2], 10);

  if (Number.isNaN(year) || Number.isNaN(month) || Number.isNaN(day)) {
    return null;
  }

  return { year, month, day };
}

/**
 * Format year, month, day as YYYY-MM-DD string
 */
function dp_formatDate(year, month, day) {
  return `${year}-${String(month + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
}

/**
 * Get number of days in a given month
 */
function dp_getDaysInMonth(year, month) {
  return new Date(year, month + 1, 0).getDate();
}

/**
 * Get first day of week (0-6) for a given month
 * 0 = Sunday, 1 = Monday, etc.
 */
function dp_getFirstDayOfMonth(year, month) {
  return new Date(year, month, 1).getDay();
}

/**
 * Get today's date as {year, month, day}
 */
function dp_getTodayDate() {
  const now = new Date();
  return {
    year: now.getFullYear(),
    month: now.getMonth(),
    day: now.getDate()
  };
}

/**
 * Add or subtract days from a date
 */
function dp_addDays(date, daysToAdd) {
  const d = new Date(date.year, date.month, date.day);
  d.setDate(d.getDate() + daysToAdd);
  return {
    year: d.getFullYear(),
    month: d.getMonth(),
    day: d.getDate()
  };
}

/**
 * Check if two dates are the same
 */
function dp_isSameDate(date1, date2) {
  if (!date1 || !date2) return false;
  return date1.year === date2.year &&
         date1.month === date2.month &&
         date1.day === date2.day;
}

/**
 * Generate calendar cells for a given month
 * Returns array of cells with state information
 */
function dp_generateCalendarCells(year, month, selectedDate, todayDate) {
  const cells = [];
  const daysInMonth = dp_getDaysInMonth(year, month);
  const firstDay = dp_getFirstDayOfMonth(year, month);

  // Days from previous month
  if (firstDay > 0) {
    const prevMonthDays = dp_getDaysInMonth(year, month - 1);
    for (let i = firstDay - 1; i >= 0; i--) {
      const day = prevMonthDays - i;
      cells.push({
        day,
        date: dp_formatDate(year, month - 1, day),
        isCurrentMonth: false,
        isToday: false,
        isSelected: false
      });
    }
  }

  // Days of current month
  for (let day = 1; day <= daysInMonth; day++) {
    const date = dp_formatDate(year, month, day);
    const dateObj = { year, month, day };
    cells.push({
      day,
      date,
      isCurrentMonth: true,
      isToday: dp_isSameDate(dateObj, todayDate),
      isSelected: dp_isSameDate(dateObj, selectedDate)
    });
  }

  // Days from next month
  const cellsNeeded = 42; // 7 days × 6 weeks
  const remainingCells = cellsNeeded - cells.length;
  for (let day = 1; day <= remainingCells; day++) {
    cells.push({
      day,
      date: dp_formatDate(year, month + 1, day),
      isCurrentMonth: false,
      isToday: false,
      isSelected: false
    });
  }

  return cells;
}

/**
 * Render calendar grid HTML
 */
function dp_renderCalendarGrid(container, cells) {
  const calendarDiv = container.querySelector('[data-dp-calendar]');
  if (!calendarDiv) return;

  calendarDiv.innerHTML = '';

  // Add weekday headers
  const weekdays = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
  for (const day of weekdays) {
    const header = document.createElement('div');
    header.setAttribute('data-dp-weekday', '');
    header.textContent = day;
    calendarDiv.appendChild(header);
  }

  // Add date cells
  for (const cell of cells) {
    const button = document.createElement('button');
    button.type = 'button';
    button.setAttribute('data-dp-date-cell', '');
    button.setAttribute('data-cell-date', cell.date);

    if (cell.isSelected) {
      button.setAttribute('data-dp-selected', 'true');
    }
    if (cell.isToday && !cell.isSelected) {
      button.setAttribute('data-dp-today', 'true');
    }
    if (!cell.isCurrentMonth) {
      button.setAttribute('data-dp-disabled', 'true');
    }

    button.textContent = cell.day;
    button.disabled = !cell.isCurrentMonth;

    calendarDiv.appendChild(button);
  }
}

/**
 * Update calendar display with new month/year
 */
function dp_updateCalendarDisplay(container) {
  if (!container._dpState) {
    container._dpState = {};
  }

  const year = container._dpState.currentYear;
  const month = container._dpState.currentMonth;
  const selectedDate = container._dpState.selectedDate
    ? dp_parseDate(container._dpState.selectedDate)
    : null;

  const todayDate = dp_getTodayDate();

  // Update month/year display
  const monthYearDiv = container.querySelector('[data-dp-month-year]');
  if (monthYearDiv) {
    const monthNames = ['January', 'February', 'March', 'April', 'May', 'June',
                        'July', 'August', 'September', 'October', 'November', 'December'];
    monthYearDiv.textContent = `${monthNames[month]} ${year}`;
  }

  // Update month select
  const monthSelect = container.querySelector('[data-dp-month-select]');
  if (monthSelect) {
    monthSelect.value = month;
  }

  // Update year input
  const yearInput = container.querySelector('[data-dp-year-select]');
  if (yearInput) {
    yearInput.value = year;
  }

  // Generate and render calendar cells
  const cells = dp_generateCalendarCells(year, month, selectedDate, todayDate);
  dp_renderCalendarGrid(container, cells);
}

/**
 * Close the dropdown menu
 */
function dp_closeDropdown(container) {
  const menu = container.querySelector('[data-dp-menu]');
  if (menu) {
    menu.classList.remove('open');
  }
}

/**
 * Handle open button - read initial date from output and populate calendar
 */
function dp_handleOpenButton(e) {
  const btn = e.target.closest('[data-dp-open]');
  if (!btn) return;

  const container = dp_getContainer(btn);
  if (!container) return;

  // Parse initial date from data-dp-output
  const outputInput = container.querySelector('[data-dp-output]');
  const dateValue = outputInput.value;

  if (!container._dpState) {
    container._dpState = {};
  }

  // Initialize state
  let selectedDate = null;
  let displayYear;
  let displayMonth;

  if (dateValue) {
    selectedDate = dp_parseDate(dateValue);
    if (selectedDate) {
      displayYear = selectedDate.year;
      displayMonth = selectedDate.month;
      container._dpState.selectedDate = dateValue;
      container._dpState.initialDate = dateValue;
    }
  }

  // If no date selected, default to today
  if (!displayYear) {
    const today = dp_getTodayDate();
    displayYear = today.year;
    displayMonth = today.month;
    container._dpState.selectedDate = null;
    container._dpState.initialDate = null;
  }

  container._dpState.currentYear = displayYear;
  container._dpState.currentMonth = displayMonth;

  // Render calendar
  dp_updateCalendarDisplay(container);
}

/**
 * Handle month select change
 */
function dp_handleMonthSelectChange(e) {
  const select = e.target.closest('[data-dp-month-select]');
  if (!select) return;

  const container = dp_getContainer(select);
  if (!container) return;

  if (!container._dpState) {
    container._dpState = {};
  }

  container._dpState.currentMonth = Number.parseInt(select.value, 10);
  dp_updateCalendarDisplay(container);
}

/**
 * Handle year input change
 */
function dp_handleYearInputChange(e) {
  const input = e.target.closest('[data-dp-year-select]');
  if (!input) return;

  const container = dp_getContainer(input);
  if (!container) return;

  if (!container._dpState) {
    container._dpState = {};
  }

  const year = Number.parseInt(input.value, 10);
  if (!Number.isNaN(year)) {
    container._dpState.currentYear = year;
    dp_updateCalendarDisplay(container);
  }
}

/**
 * Handle month navigation buttons with hold-to-repeat acceleration
 */
function dp_handleNavButtonMouseDown(e) {
  const btn = e.target.closest('[data-dp-nav]');
  if (!btn) return;

  const container = dp_getContainer(btn);
  if (!container) return;

  if (!container._dpState) {
    container._dpState = {};
  }

  const direction = btn.getAttribute('data-dp-nav'); // 'prev' or 'next'

  // Perform initial click
  performNavigation(container, direction);

  // Set up hold-to-repeat: initial 500ms delay, then 100ms repeats
  container._dpState.repeatTimeout = setTimeout(() => {
    container._dpState.repeatInterval = setInterval(() => {
      performNavigation(container, direction);
    }, 100);
  }, 500);
}

/**
 * Handle navigation button mouse up - stop hold-to-repeat
 */
function dp_handleNavButtonMouseUp(e) {
  const btn = e.target.closest('[data-dp-nav]');
  if (!btn) return;

  const container = dp_getContainer(btn);
  if (!container) return;

  if (!container._dpState) {
    container._dpState = {};
  }

  // Clear all pending timers
  if (container._dpState.repeatTimeout) {
    clearTimeout(container._dpState.repeatTimeout);
    container._dpState.repeatTimeout = null;
  }
  if (container._dpState.repeatInterval) {
    clearInterval(container._dpState.repeatInterval);
    container._dpState.repeatInterval = null;
  }
}

/**
 * Perform the actual navigation
 */
function performNavigation(container, direction) {
  if (!container._dpState) {
    container._dpState = {};
  }

  if (direction === 'prev') {
    container._dpState.currentMonth--;
    if (container._dpState.currentMonth < 0) {
      container._dpState.currentMonth = 11;
      container._dpState.currentYear--;
    }
  } else if (direction === 'next') {
    container._dpState.currentMonth++;
    if (container._dpState.currentMonth > 11) {
      container._dpState.currentMonth = 0;
      container._dpState.currentYear++;
    }
  }

  dp_updateCalendarDisplay(container);
}

/**
 * Handle date cell clicks
 */
function dp_handleDateCellClick(e) {
  const cell = e.target.closest('[data-dp-date-cell]');
  if (!cell) return;

  // Ignore clicks on disabled cells (other month)
  if (cell.disabled) return;

  const container = dp_getContainer(cell);
  if (!container) return;

  if (!container._dpState) {
    container._dpState = {};
  }

  const dateStr = cell.getAttribute('data-cell-date');
  container._dpState.selectedDate = dateStr;

  // Update output field
  const outputInput = container.querySelector('[data-dp-output]');
  outputInput.value = dateStr;

  dp_updateCalendarDisplay(container);

  // Close dropdown
  dp_closeDropdown(container);
}

/**
 * Handle yesterday button
 */
function dp_handleYesterdayButton(e) {
  const btn = e.target.closest('[data-dp-yesterday]');
  if (!btn) return;

  const container = dp_getContainer(btn);
  if (!container) return;

  if (!container._dpState) {
    container._dpState = {};
  }

  const today = dp_getTodayDate();
  const yesterday = dp_addDays(today, -1);

  const dateStr = dp_formatDate(yesterday.year, yesterday.month, yesterday.day);
  container._dpState.selectedDate = dateStr;

  // Navigate to yesterday's month if different
  container._dpState.currentYear = yesterday.year;
  container._dpState.currentMonth = yesterday.month;

  // Update output field
  const outputInput = container.querySelector('[data-dp-output]');
  outputInput.value = dateStr;

  dp_updateCalendarDisplay(container);

  // Close dropdown
  dp_closeDropdown(container);
}

/**
 * Handle today button
 */
function dp_handleTodayButton(e) {
  const btn = e.target.closest('[data-dp-today]');
  if (!btn) return;

  const container = dp_getContainer(btn);
  if (!container) return;

  if (!container._dpState) {
    container._dpState = {};
  }

  const today = dp_getTodayDate();
  const dateStr = dp_formatDate(today.year, today.month, today.day);

  container._dpState.selectedDate = dateStr;
  container._dpState.currentYear = today.year;
  container._dpState.currentMonth = today.month;

  // Update output field
  const outputInput = container.querySelector('[data-dp-output]');
  outputInput.value = dateStr;

  dp_updateCalendarDisplay(container);

  // Close dropdown
  dp_closeDropdown(container);
}

/**
 * Handle tomorrow button
 */
function dp_handleTomorrowButton(e) {
  const btn = e.target.closest('[data-dp-tomorrow]');
  if (!btn) return;

  const container = dp_getContainer(btn);
  if (!container) return;

  if (!container._dpState) {
    container._dpState = {};
  }

  const today = dp_getTodayDate();
  const tomorrow = dp_addDays(today, 1);

  const dateStr = dp_formatDate(tomorrow.year, tomorrow.month, tomorrow.day);
  container._dpState.selectedDate = dateStr;

  // Navigate to tomorrow's month if different
  container._dpState.currentYear = tomorrow.year;
  container._dpState.currentMonth = tomorrow.month;

  // Update output field
  const outputInput = container.querySelector('[data-dp-output]');
  outputInput.value = dateStr;

  dp_updateCalendarDisplay(container);

  // Close dropdown
  dp_closeDropdown(container);
}

/**
 * Close dropdown when clicking outside
 */
function dp_handleOutsideClick(e) {
  // Check if click is outside any date picker container
  const clickInContainer = e.target.closest('[data-dp-container]');
  if (clickInContainer) {
    return; // Click is inside a date picker, don't close
  }

  // Close all open dropdowns
  for (const menu of document.querySelectorAll('[data-dp-menu].open')) {
    menu.classList.remove('open');
  }
}
