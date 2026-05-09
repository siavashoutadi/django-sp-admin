const relatedWindows = [];

// Clone table row for tabular inline formsets
window.cloneTableRow = (button, prefix) => {
  const formsetGroup = button.closest('.js-inline-admin-formset');
  if (!formsetGroup) {
    return;
  }

  const tbody = formsetGroup.querySelector('tbody');
  if (!tbody) {
    return;
  }

  const emptyRow = tbody.querySelector('tr.empty-form');
  if (!emptyRow) {
    return;
  }

  const totalFormsInput = formsetGroup.querySelector(`[name$="-TOTAL_FORMS"]`);
  if (!totalFormsInput) {
    return;
  }

  const formNum = parseInt(totalFormsInput.value);

  // Clone the empty row
  const newRow = emptyRow.cloneNode(true);
  newRow.classList.remove('empty-form');
  newRow.style.display = '';
  newRow.id = `${prefix}-${formNum}`;

  // Update all __prefix__ references
  newRow.querySelectorAll('[name]').forEach((field) => {
    if (field.name.includes('__prefix__')) {
      field.name = field.name.replace('__prefix__', formNum);
    }
  });

  newRow.querySelectorAll('[id]').forEach((field) => {
    if (field.id.includes('__prefix__')) {
      field.id = field.id.replace('__prefix__', formNum);
    }
  });

  newRow.querySelectorAll('label[for]').forEach((label) => {
    if (label.htmlFor.includes('__prefix__')) {
      label.htmlFor = label.htmlFor.replace('__prefix__', formNum);
    }
  });

  // Reset input values
  newRow.querySelectorAll('input[type="text"], input[type="email"], input[type="password"], input[type="number"], textarea, select').forEach((field) => {
    if (field.type !== 'hidden' && !field.name.includes('-id')) {
      field.value = '';
      if (field.type === 'checkbox') {
        field.checked = false;
      }
    }
  });

  // Insert before empty row
  emptyRow.parentNode.insertBefore(newRow, emptyRow);

  // Update TOTAL_FORMS
  totalFormsInput.value = formNum + 1;
};

// Remove table row for tabular inline formsets
window.removeTableRow = (button) => {
  const row = button.closest('tr');
  if (!row) {
    return;
  }

  const formsetGroup = row.closest('.js-inline-admin-formset');
  if (!formsetGroup) {
    return;
  }

  // Check if existing or newly added
  const pkField = row.querySelector('[name*="-id"]');
  const deleteCheckbox = row.querySelector('[name*="-DELETE"]');

  if (pkField && pkField.value && deleteCheckbox) {
    // Mark existing for deletion
    deleteCheckbox.checked = true;
    row.style.opacity = '0.5';
    row.style.pointerEvents = 'none';
  } else {
    // Remove newly added row
    const totalFormsInput = formsetGroup.querySelector('[name$="-TOTAL_FORMS"]');
    if (totalFormsInput) {
      totalFormsInput.value = parseInt(totalFormsInput.value) - 1;
    }
    row.remove();
  }
};

// Global functions for popup dismissal (called by Django's popup_response.js)
window.dismissChangeRelatedObjectPopup = (win) => {
  // Close the popup window
  if (win) {
    win.close();
  }
  const index = relatedWindows.indexOf(win);
  if (index > -1) {
    relatedWindows.splice(index, 1);
  }
};

window.dismissAddRelatedObjectPopup = (win) => {
  // Close the popup window
  if (win) {
    win.close();
  }
  const index = relatedWindows.indexOf(win);
  if (index > -1) {
    relatedWindows.splice(index, 1);
  }
};

window.dismissDeleteRelatedObjectPopup = (win) => {
  // Close the popup window
  if (win) {
    win.close();
  }
  const index = relatedWindows.indexOf(win);
  if (index > -1) {
    relatedWindows.splice(index, 1);
  }
};

// Handle related widget wrapper links
document.addEventListener('click', (e) => {
  const link = e.target.closest('a.related-widget-wrapper-link');
  if (!link) return;

  // Check if this is a change, add, delete, or view related link
  if (!link.classList.contains('change-related') &&
      !link.classList.contains('add-related') &&
      !link.classList.contains('delete-related') &&
      !link.classList.contains('view-related')) {
    return;
  }

  e.preventDefault();

  let href = link.getAttribute('href') || link.getAttribute('data-href-template');
  if (!href) return;

  // Replace __fk__ placeholder if present
  if (href.includes('__fk__')) {
    const linkId = link.getAttribute('id');
    if (linkId) {
      const fieldId = linkId.replace(/^(change|add|delete|view)_/, '');
      const selectField = document.getElementById(fieldId);

      if (selectField?.value) {
        href = href.replace('__fk__', selectField.value);
      } else {
        alert('Please select an item first.');
        return;
      }
    }
  }

  // View links should navigate directly, not as popups
  if (link.classList.contains('view-related')) {
    window.location = href;
    return;
  }

  // For change, add, delete links: open as popups with _popup=1
  const url = new URL(href, window.location.origin);
  url.searchParams.set('_popup', '1');

  const windowName = link.getAttribute('id') || `related_window_${Date.now()}`;
  const windowFeatures = 'height=500,width=800,resizable=yes,scrollbars=yes';

  const win = window.open(url.toString(), windowName, windowFeatures);
  if (win) {
    relatedWindows.push(win);
    win.focus();
  }
}, true); // Use capture phase to handle the event before other handlers

// Hide empty formset forms (templates cloned by Django's formset.js)
document.addEventListener('DOMContentLoaded', () => {
  const hideEmptyForms = () => {
    for (const form of document.querySelectorAll('.empty-form')) {
      form.style.display = 'none';
    }
  };

  hideEmptyForms();

  // Watch for dynamically added forms and hide new empty forms
  const observer = new MutationObserver(hideEmptyForms);
  for (const formContainer of document.querySelectorAll('.inline-forms')) {
    observer.observe(formContainer, { childList: true, subtree: true });
  }

  // Handle Add button clicks - custom cloning logic
  document.addEventListener('click', (e) => {
    const addBtn = e.target.closest('[data-inline-add-btn]');
    if (!addBtn) return;

    e.preventDefault();
    e.stopPropagation();

    // Get the formset prefix from the button ID
    const prefix = addBtn.id.replace('add_', '');

    // Find the formset group container
    const formsetGroup = addBtn.closest('.js-inline-admin-formset');
    if (!formsetGroup) {
      return;
    }

    const formsContainer = formsetGroup.querySelector('.inline-forms');
    if (!formsContainer) {
      return;
    }

    const emptyForm = formsetGroup.querySelector('.empty-form');
    if (!emptyForm) {
      return;
    }

    const totalFormsInput = formsetGroup.querySelector(`[name$="-TOTAL_FORMS"]`);
    if (!totalFormsInput) {
      return;
    }

    const currentFormNumber = parseInt(totalFormsInput.value);

    // Clone the empty form
    const newForm = emptyForm.cloneNode(true);
    newForm.classList.remove('empty-form');
    newForm.style.display = '';
    newForm.id = `${prefix}-${currentFormNumber}`;

    // Update all field names and IDs - replace __prefix__ with actual form number
    let updateCount = 0;
    newForm.querySelectorAll('[name*="__prefix__"]').forEach((field) => {
      const oldName = field.name;
      field.name = field.name.replace('__prefix__', currentFormNumber);
      updateCount++;
    });

    newForm.querySelectorAll('[id*="__prefix__"]').forEach((field) => {
      const oldId = field.id;
      field.id = field.id.replace('__prefix__', currentFormNumber);
      updateCount++;
    });

    // Update label references
    newForm.querySelectorAll('label[for*="__prefix__"]').forEach((label) => {
      label.htmlFor = label.htmlFor.replace('__prefix__', currentFormNumber);
    });

    // Update aria-describedby references
    newForm.querySelectorAll('[aria-describedby*="__prefix__"]').forEach((field) => {
      const oldAttr = field.getAttribute('aria-describedby');
      field.setAttribute('aria-describedby', oldAttr.replace(/__prefix__/g, currentFormNumber));
    });

    // Insert the new form before the empty form
    emptyForm.parentNode.insertBefore(newForm, emptyForm);

    // Update TOTAL_FORMS
    totalFormsInput.value = currentFormNumber + 1;

    // Re-hide the empty form
    hideEmptyForms();
  }, false);

  // Handle remove button clicks - remove the form from DOM
  document.addEventListener('click', (e) => {
    const removeBtn = e.target.closest('[data-inline-remove-btn]');
    if (!removeBtn) return;

    e.preventDefault();
    e.stopPropagation();

    const formDiv = removeBtn.closest('.inline-related');
    if (!formDiv) {
      return;
    }

    const formsetGroup = formDiv.closest('.js-inline-admin-formset');
    if (!formsetGroup) {
      return;
    }

    // Check if this is an existing form (has a PK field with value) or newly added
    const pkField = formDiv.querySelector('[name*="-id"]');
    const deletionCheckbox = formDiv.querySelector('[name*="-DELETE"]');

    if (pkField && pkField.value && deletionCheckbox) {
      // Existing form - mark for deletion instead of removing
      deletionCheckbox.checked = true;
      formDiv.style.opacity = '0.5';
      formDiv.style.pointerEvents = 'none';
    } else {
      // Newly added form - remove from DOM and update counts
      const totalFormsInput = formsetGroup.querySelector('[name$="-TOTAL_FORMS"]');
      if (totalFormsInput) {
        totalFormsInput.value = parseInt(totalFormsInput.value) - 1;
      }
      formDiv.remove();
    }
  }, false);

  // Update related object links visibility based on field value
  for (const select of document.querySelectorAll('select[data-model-ref]')) {
    select.addEventListener('change', () => {
      // Find sibling related links
      const siblings = select.parentElement.querySelectorAll('.view-related, .change-related, .delete-related, .add-related');
      const value = select.value;

      for (const link of siblings) {
        if (value) {
          // Enable the link and update href if there's a template
          const template = link.getAttribute('data-href-template');
          if (template?.includes('__fk__')) {
            link.setAttribute('href', template.replace('__fk__', value));
          } else if (!link.getAttribute('href')) {
            link.setAttribute('href', link.getAttribute('data-href-template') || '#');
          }
          link.removeAttribute('aria-disabled');
        } else {
          // Disable the link
          link.removeAttribute('href');
          link.setAttribute('aria-disabled', 'true');
        }
      }
    });

    // Trigger change event on page load to set initial state
    select.dispatchEvent(new Event('change', { bubbles: true }));
  }
});
