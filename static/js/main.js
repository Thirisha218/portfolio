const menuToggle = document.getElementById("menuToggle");
const nav = document.getElementById("nav");
menuToggle?.addEventListener("click", () => nav.classList.toggle("open"));
nav?.querySelectorAll("a").forEach(link => link.addEventListener("click", () => nav.classList.remove("open")));

document.getElementById("year").textContent = new Date().getFullYear();

// Reveal sections as they enter the viewport.
const revealObserver = new IntersectionObserver((entries, observer) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add("visible");
      observer.unobserve(entry.target);
    }
  });
}, { threshold: 0.12 });
document.querySelectorAll(".reveal").forEach(el => revealObserver.observe(el));

// Subtle cursor spotlight on desktop.
const glow = document.getElementById("cursorGlow");
window.addEventListener("pointermove", event => {
  if (glow && window.innerWidth > 900) {
    glow.style.left = `${event.clientX}px`;
    glow.style.top = `${event.clientY}px`;
  }
});

// Contact form -> Flask API -> SQLite database.
const contactForm = document.getElementById("contactForm");
const formStatus = document.getElementById("formStatus");
contactForm?.addEventListener("submit", async event => {
  event.preventDefault();
  const submitButton = contactForm.querySelector("button[type='submit']");
  const originalText = submitButton.innerHTML;
  submitButton.disabled = true;
  submitButton.innerHTML = 'Sending <i class="fa-solid fa-spinner fa-spin"></i>';
  formStatus.textContent = "";
  formStatus.classList.remove("error");

  const payload = Object.fromEntries(new FormData(contactForm).entries());
  try {
    const response = await fetch("/api/contact", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
    const result = await response.json();
    if (!response.ok) throw new Error(result.message || "Unable to send your message.");
    formStatus.textContent = result.message;
    contactForm.reset();
  } catch (error) {
    formStatus.textContent = error.message || "Something went wrong. Please try again.";
    formStatus.classList.add("error");
  } finally {
    submitButton.disabled = false;
    submitButton.innerHTML = originalText;
  }
});

// Confirm backend availability in the browser console.
fetch("/api/health").then(r => r.json()).then(data => {
  document.documentElement.dataset.api = data.status;
}).catch(() => {
  document.documentElement.dataset.api = "offline";
});
