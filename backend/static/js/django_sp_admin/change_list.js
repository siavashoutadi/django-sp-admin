document.addEventListener('DOMContentLoaded', () => {
  const actionToggle = document.getElementById('action-toggle');
  const selectedActions = document.querySelectorAll('input[name="_selected_action"]');

  if (actionToggle) {
    // Handle select all checkbox
    actionToggle.addEventListener('change', function() {
      for (const checkbox of selectedActions) {
        checkbox.checked = this.checked;
      }
    });

    // Update select all checkbox when individual checkboxes change
    for (const checkbox of selectedActions) {
      checkbox.addEventListener('change', () => {
        const allChecked = Array.from(selectedActions).every(cb => cb.checked);
        const someChecked = Array.from(selectedActions).some(cb => cb.checked);
        actionToggle.checked = allChecked;
        actionToggle.indeterminate = someChecked && !allChecked;
      });
    }
  }
});
