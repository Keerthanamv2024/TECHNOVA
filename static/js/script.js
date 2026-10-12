/**
 * TechNova – IT Company Profile Website
 * Client-Side JavaScript (Vanilla JS)
 * Features: Mobile menu toggle, active section scrollspy, client-side validation, AJAX submission
 */

document.addEventListener("DOMContentLoaded", () => {
  initMobileNavigation();
  initContactFormValidation();
  initScrollSpy();
  initAlertDismissal();
});

/**
 * 1. Mobile Hamburger Navigation
 */
function initMobileNavigation() {
  const navToggle = document.getElementById("navToggle");
  const navMenu = document.getElementById("navMenu");

  if (!navToggle || !navMenu) return;

  navToggle.addEventListener("click", () => {
    const isOpen = navMenu.classList.toggle("open");
    navToggle.classList.toggle("active", isOpen);
    navToggle.setAttribute("aria-expanded", isOpen);
  });

  // Close mobile menu when clicking any nav link
  const navLinks = navMenu.querySelectorAll(".nav-link");
  navLinks.forEach((link) => {
    link.addEventListener("click", () => {
      if (navMenu.classList.contains("open")) {
        navMenu.classList.remove("open");
        navToggle.classList.remove("active");
        navToggle.setAttribute("aria-expanded", "false");
      }
    });
  });
}

/**
 * 2. Active Navigation Highlight (Scrollspy)
 */
function initScrollSpy() {
  const sections = document.querySelectorAll("section[id]");
  const navLinks = document.querySelectorAll(".nav-menu .nav-link");

  if (sections.length === 0 || navLinks.length === 0) return;

  window.addEventListener("scroll", () => {
    let currentId = "";
    const scrollPosition = window.pageYOffset + 120;

    sections.forEach((section) => {
      const sectionTop = section.offsetTop;
      const sectionHeight = section.offsetHeight;
      if (scrollPosition >= sectionTop && scrollPosition < sectionTop + sectionHeight) {
        currentId = section.getAttribute("id");
      }
    });

    navLinks.forEach((link) => {
      link.classList.remove("active");
      const href = link.getAttribute("href");
      if (href === `#${currentId}`) {
        link.classList.add("active");
      }
    });
  });
}

/**
 * 3. Contact Form Validation & Asynchronous Submission
 */
function initContactFormValidation() {
  const form = document.getElementById("contactForm");
  const responseBox = document.getElementById("formResponse");
  const submitBtn = document.getElementById("contactSubmitBtn");

  if (!form) return;

  const fields = {
    name: {
      input: document.getElementById("name"),
      group: document.getElementById("group-name"),
      error: document.getElementById("error-name"),
      validate: (val) => (val.trim().length >= 2 ? "" : "Full name must be at least 2 characters."),
    },
    email: {
      input: document.getElementById("email"),
      group: document.getElementById("group-email"),
      error: document.getElementById("error-email"),
      validate: (val) => {
        const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return regex.test(val.trim()) ? "" : "Please enter a valid email address.";
      },
    },
    subject: {
      input: document.getElementById("subject"),
      group: document.getElementById("group-subject"),
      error: document.getElementById("error-subject"),
      validate: (val) => (val.trim().length >= 3 ? "" : "Subject must be at least 3 characters."),
    },
    message: {
      input: document.getElementById("message"),
      group: document.getElementById("group-message"),
      error: document.getElementById("error-message"),
      validate: (val) => (val.trim().length >= 10 ? "" : "Message must be at least 10 characters."),
    },
  };

  // Real-time error clearing when user types
  Object.keys(fields).forEach((key) => {
    const item = fields[key];
    if (item.input) {
      item.input.addEventListener("input", () => {
        clearFieldError(item);
      });
    }
  });

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    let hasErrors = false;

    // Run client-side validation on each field
    Object.keys(fields).forEach((key) => {
      const item = fields[key];
      const errorMsg = item.validate(item.input.value);
      if (errorMsg) {
        showFieldError(item, errorMsg);
        hasErrors = true;
      } else {
        clearFieldError(item);
      }
    });

    if (hasErrors) {
      displayAlert("Please fix the errors highlighted above before submitting.", "danger");
      return;
    }

    // Prepare payload
    const payload = {
      name: fields.name.input.value.trim(),
      email: fields.email.input.value.trim(),
      subject: fields.subject.input.value.trim(),
      message: fields.message.input.value.trim(),
    };

    // Button loading state
    const originalBtnText = submitBtn.innerHTML;
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<span>Sending Message...</span>';

    try {
      const response = await fetch(form.action, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-Requested-With": "XMLHttpRequest",
        },
        body: JSON.stringify(payload),
      });

      const result = await response.json();

      if (response.ok && result.success) {
        displayAlert(result.message, "success");
        form.reset();
      } else {
        displayAlert(result.message || "Failed to submit enquiry. Please check your data.", "danger");
      }
    } catch (err) {
      displayAlert("Network error or server unavailable. Please try again later.", "danger");
    } finally {
      submitBtn.disabled = false;
      submitBtn.innerHTML = originalBtnText;
    }
  });

  function showFieldError(item, message) {
    if (item.group) item.group.classList.add("has-error");
    if (item.error) item.error.textContent = message;
  }

  function clearFieldError(item) {
    if (item.group) item.group.classList.remove("has-error");
    if (item.error) item.error.textContent = "";
  }

  function displayAlert(message, type) {
    if (!responseBox) return;
    responseBox.innerHTML = `
      <div class="alert-banner alert-${type}" role="alert">
        <span>${message}</span>
        <button type="button" class="alert-close" aria-label="Close" onclick="this.parentElement.remove();">&times;</button>
      </div>
    `;
    responseBox.scrollIntoView({ behavior: "smooth", block: "nearest" });
  }
}

/**
 * 4. Dismissible Alert Helper
 */
function initAlertDismissal() {
  document.querySelectorAll(".alert-close").forEach((button) => {
    button.addEventListener("click", function () {
      const alert = this.closest(".alert-banner");
      if (alert) alert.remove();
    });
  });
}
