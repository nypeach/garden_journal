// Modal functionality for plant journal
document.addEventListener('DOMContentLoaded', function () {
  var modal = document.getElementById('journal-modal');
  var iframe = document.getElementById('journal-iframe');
  if (!modal || !iframe) return;

  function closeModal() {
    modal.classList.add('modal-hidden');
    document.body.style.overflow = '';
  }

  function openModal(plantId) {
    // Set iframe src to the journal route for this plant
    iframe.src = '/journal/' + plantId;
    modal.classList.remove('modal-hidden');
    document.body.style.overflow = 'hidden';
  }

  // Open modal when any journal link is clicked
  document.querySelectorAll('[data-open-modal]').forEach(function (link) {
    link.addEventListener('click', function (e) {
      e.preventDefault();
      var plantId = this.getAttribute('data-plant-id');
      if (plantId) {
        openModal(plantId);
      }
    });
  });

  // Close modal when clicking backdrop
  modal.addEventListener('click', function (e) {
    if (e.target === modal) {
      closeModal();
    }
  });

  // Close modal on ESC key
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && !modal.classList.contains('modal-hidden')) {
      closeModal();
    }
  });
});