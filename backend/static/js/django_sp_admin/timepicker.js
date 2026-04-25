/**
 * Time Picker Widget
 *
 * Handles time selection via spinner controls with inc/dec buttons.
 * Supports multiple pickers on the same page through container-scoped state.
 */

document.addEventListener('DOMContentLoaded', () => {
  // Event delegation for all time picker interactions
  document.addEventListener('click', tp_handleSpinnerButtonClick);
  document.addEventListener('click', tp_handleOpenButton);
  document.addEventListener('click', tp_handleSubmitButton);
  document.addEventListener('click', tp_handleResetButton);
  document.addEventListener('click', tp_handleNowButton);

  document.addEventListener('mousedown', tp_handleSpinnerButtonMouseDown);
  document.addEventListener('mouseup', tp_handleSpinnerButtonMouseUp);

  document.addEventListener('change', tp_handleSpinnerInputChange);
});

/**
 * Get the closest time picker container from an element
 */
function tp_getContainer(element) {
  return element.closest('[data-tp-container]');
}

/**
 * Parse integer value from input, returning 0 if invalid
 */
function tp_getSpinnerValue(input) {
  const value = Number.parseInt(input.value, 10);
  return Number.isNaN(value) ? 0 : value;
}

/**
 * Set spinner value with clamping and zero-padding
 */
function tp_setSpinnerValue(input, value, max) {
  const clamped = Math.max(0, Math.min(value, max));
  input.value = String(clamped).padStart(2, '0');
}

/**
 * Parse time string in HH:MM format
 */
function tp_parseTimeFormat(timeStr) {
  const parts = timeStr.trim().split(':');
  return {
    hours: Number.parseInt(parts[0], 10) || 0,
    minutes: Number.parseInt(parts[1], 10) || 0
  };
}

/**
 * Format hours and minutes as HH:MM string
 */
function tp_formatTime(hours, minutes) {
  return `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}`;
}

/**
 * Update the display element with current spinner values
 */
function tp_updateDisplay(container) {
  const hoursInput = container.querySelector('[data-tp-hours]');
  const minutesInput = container.querySelector('[data-tp-minutes]');
  const displayElement = container.querySelector('[data-tp-display]');

  const hours = tp_getSpinnerValue(hoursInput);
  const minutes = tp_getSpinnerValue(minutesInput);

  if (displayElement) {
    displayElement.textContent = tp_formatTime(hours, minutes);
  }
}

/**
 * Handle open button - read initial time from output and populate spinners
 */
function tp_handleOpenButton(e) {
  const btn = e.target.closest('[data-tp-open]');
  if (!btn) return;

  const container = tp_getContainer(btn);
  if (!container) return;

  // Parse initial time from data-tp-output
  const outputInput = container.querySelector('[data-tp-output]');
  const timeValue = outputInput.value || '00:00';
  const { hours, minutes } = tp_parseTimeFormat(timeValue);

  // Initialize container state
  if (!container._tpState) {
    container._tpState = {};
  }
  container._tpState.initialTime = { hours, minutes };

  // Populate spinner inputs with parsed values
  const hoursInput = container.querySelector('[data-tp-hours]');
  const minutesInput = container.querySelector('[data-tp-minutes]');

  tp_setSpinnerValue(hoursInput, hours, 23);
  tp_setSpinnerValue(minutesInput, minutes, 59);

  // Update display to reflect loaded time
  tp_updateDisplay(container);
}

/**
 * Handle direct input on hours/minutes fields
 */
function tp_handleSpinnerInputChange(e) {
  const input = e.target.closest('[data-tp-hours], [data-tp-minutes]');
  if (!input) return;

  const container = tp_getContainer(input);
  if (!container) return;

  // Determine max value based on input type
  const max = input.dataset.tpHours ? 23 : 59;
  const value = tp_getSpinnerValue(input);

  // Clamp and format
  tp_setSpinnerValue(input, value, max);

  // Sync display
  tp_updateDisplay(container);
}

/**
 * Handle single click on spinner up/down buttons
 */
function tp_handleSpinnerButtonClick(e) {
  const btn = e.target.closest('[data-tp-spinner-btn]');
  if (!btn) return;

  const container = tp_getContainer(btn);
  if (!container) return;

  const direction = btn.dataset.tpSpinnerBtn; // 'up' or 'down'
  const spinner = btn.closest('[data-tp-spinner]');

  if (!spinner) return;

  const input = spinner.querySelector('[data-tp-hours], [data-tp-minutes]');
  if (!input) return;

  const isHours = !!input.dataset.tpHours;
  const max = isHours ? 23 : 59;
  const currentValue = tp_getSpinnerValue(input);

  let newValue;
  if (direction === 'up') {
    // Wrap around: 23->0 for hours, 59->0 for minutes
    newValue = (currentValue + 1) % (max + 1);
  } else {
    // Wrap around: 0->23 for hours, 0->59 for minutes
    newValue = (currentValue - 1 + (max + 1)) % (max + 1);
  }

  tp_setSpinnerValue(input, newValue, max);
  tp_updateDisplay(container);
}

/**
 * Handle mouse down on spinner buttons - start hold-to-repeat
 */
function tp_handleSpinnerButtonMouseDown(e) {
  const btn = e.target.closest('[data-tp-spinner-btn]');
  if (!btn) return;

  const container = tp_getContainer(btn);
  if (!container) return;

  if (!container._tpState) {
    container._tpState = {};
  }

  // Clear any existing intervals/timeouts
  if (container._tpState.repeatInterval) {
    clearInterval(container._tpState.repeatInterval);
  }
  if (container._tpState.repeatTimeout) {
    clearTimeout(container._tpState.repeatTimeout);
  }

  // Wait 300ms before starting repeat
  container._tpState.repeatTimeout = setTimeout(() => {
    // Then repeat every 50ms
    container._tpState.repeatInterval = setInterval(() => {
      // Trigger the click handler logic
      tp_handleSpinnerButtonClick(e);
    }, 50);
  }, 300);
}

/**
 * Handle mouse up - stop hold-to-repeat
 */
function tp_handleSpinnerButtonMouseUp(e) {
  const btn = e.target.closest('[data-tp-spinner-btn]');
  if (!btn) return;

  const container = tp_getContainer(btn);
  if (!container) return;

  if (!container._tpState) {
    container._tpState = {};
  }

  // Clear all pending timers
  if (container._tpState.repeatTimeout) {
    clearTimeout(container._tpState.repeatTimeout);
    container._tpState.repeatTimeout = null;
  }
  if (container._tpState.repeatInterval) {
    clearInterval(container._tpState.repeatInterval);
    container._tpState.repeatInterval = null;
  }
}

/**
 * Handle submit button - write time to output and close dropdown
 */
function tp_handleSubmitButton(e) {
  const btn = e.target.closest('[data-tp-submit]');
  if (!btn) return;

  const container = tp_getContainer(btn);
  if (!container) return;

  // Read current spinner values
  const hoursInput = container.querySelector('[data-tp-hours]');
  const minutesInput = container.querySelector('[data-tp-minutes]');

  const hours = tp_getSpinnerValue(hoursInput);
  const minutes = tp_getSpinnerValue(minutesInput);

  // Write to output field
  const outputInput = container.querySelector('[data-tp-output]');
  outputInput.value = tp_formatTime(hours, minutes);

  // Close dropdown menu
  const menu = container.querySelector('[data-tp-menu]');
  if (menu) {
    menu.classList.remove('open');
  }

  // Clear any pending hold timers
  if (!container._tpState) {
    container._tpState = {};
  }
  if (container._tpState.repeatTimeout) {
    clearTimeout(container._tpState.repeatTimeout);
    container._tpState.repeatTimeout = null;
  }
  if (container._tpState.repeatInterval) {
    clearInterval(container._tpState.repeatInterval);
    container._tpState.repeatInterval = null;
  }
}

/**
 * Handle reset button - restore to initial time when picker opened
 */
function tp_handleResetButton(e) {
  const btn = e.target.closest('[data-tp-reset]');
  if (!btn) return;

  const container = tp_getContainer(btn);
  if (!container) return;

  if (!container._tpState) {
    container._tpState = {};
  }

  // Get the initial time stored when picker opened
  const initialTime = container._tpState.initialTime || { hours: 0, minutes: 0 };

  // Restore spinners to initial values
  const hoursInput = container.querySelector('[data-tp-hours]');
  const minutesInput = container.querySelector('[data-tp-minutes]');

  tp_setSpinnerValue(hoursInput, initialTime.hours, 23);
  tp_setSpinnerValue(minutesInput, initialTime.minutes, 59);

  // Update display
  tp_updateDisplay(container);
}

/**
 * Handle now button - set spinners to current time
 */
function tp_handleNowButton(e) {
  const btn = e.target.closest('[data-tp-now]');
  if (!btn) return;

  const container = tp_getContainer(btn);
  if (!container) return;

  // Get current time
  const now = new Date();
  const hours = now.getHours();
  const minutes = now.getMinutes();

  console.log(`Setting time to now: ${tp_formatTime(hours, minutes)}`);

  // Set spinner inputs to current time
  const hoursInput = container.querySelector('[data-tp-hours]');
  const minutesInput = container.querySelector('[data-tp-minutes]');

  tp_setSpinnerValue(hoursInput, hours, 23);
  tp_setSpinnerValue(minutesInput, minutes, 59);

  // Update display
  tp_updateDisplay(container);
}
