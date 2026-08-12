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

  // Confirm before deleting a post
  document.querySelectorAll(".delete-post-form").forEach(function (form) {
    form.addEventListener("submit", function (e) {
      if (!confirm("Delete this article permanently? This cannot be undone.")) {
        e.preventDefault();
      }
    });
  });
});
