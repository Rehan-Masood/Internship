document.addEventListener("DOMContentLoaded", function () {
  // Mobile nav toggle
  const toggle = document.querySelector(".nav-toggle");
  const links = document.querySelector(".nav-links");
  if (toggle && links) {
    toggle.addEventListener("click", function () {
      links.classList.toggle("open");
    });
  }

  // Dismiss flash messages
  document.querySelectorAll(".flash-close").forEach(function (btn) {
    btn.addEventListener("click", function () {
      btn.closest(".flash").remove();
    });
  });

  // Auto-hide flash messages after 5 seconds
  document.querySelectorAll(".flash").forEach(function (flash) {
    setTimeout(function () {
      flash.style.transition = "opacity 0.4s ease";
      flash.style.opacity = "0";
      setTimeout(function () {
        flash.remove();
      }, 400);
    }, 5000);
  });

  function openDeleteModal(modal) {
    if (!modal) return;
    modal.hidden = false;
    modal.setAttribute("aria-hidden", "false");
    modal.classList.add("is-open");
    document.body.classList.add("modal-open");
  }

  function closeDeleteModal(modal) {
    if (!modal) return;
    modal.classList.remove("is-open");
    modal.setAttribute("aria-hidden", "true");
    modal.hidden = true;
    document.body.classList.remove("modal-open");
  }

  document.querySelectorAll(".delete-post-trigger").forEach(function (trigger) {
    trigger.addEventListener("click", function () {
      const modal = document.getElementById(trigger.dataset.modalTarget);
      openDeleteModal(modal);
    });
  });

  document.querySelectorAll("[data-modal-close='true']").forEach(function (control) {
    control.addEventListener("click", function () {
      const modal = control.closest(".inkwell-modal");
      closeDeleteModal(modal);
    });
  });

  document.querySelectorAll(".inkwell-modal").forEach(function (modal) {
    modal.addEventListener("click", function (event) {
      if (event.target === modal || event.target.classList.contains("inkwell-modal-backdrop")) {
        closeDeleteModal(modal);
      }
    });
  });

  document.addEventListener("keydown", function (event) {
    if (event.key === "Escape") {
      document.querySelectorAll(".inkwell-modal.is-open").forEach(function (modal) {
        closeDeleteModal(modal);
      });
    }
  });
});
