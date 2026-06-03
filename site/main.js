// Fabric landing page — contact form handling.
// By default this validates client-side and posts to FORM_ENDPOINT if set.
// Configure FORM_ENDPOINT with a form backend (e.g. Formspree) to receive
// submissions; otherwise the form falls back to a mailto: handoff.

const FORM_ENDPOINT = ""; // e.g. "https://formspree.io/f/xxxxxxx"
const FALLBACK_EMAIL = "thefractionalpm@gmail.com";

document.getElementById("year").textContent = new Date().getFullYear();

const form = document.getElementById("contactForm");
const statusEl = document.getElementById("formStatus");

function setStatus(msg, kind) {
  statusEl.textContent = msg;
  statusEl.className = "form-status" + (kind ? " " + kind : "");
}

function validate() {
  let ok = true;
  for (const el of form.querySelectorAll("input, textarea")) {
    const invalid = el.required && !el.value.trim();
    const badEmail = el.type === "email" && el.value && !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(el.value);
    el.classList.toggle("invalid", invalid || badEmail);
    if (invalid || badEmail) ok = false;
  }
  return ok;
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  if (!validate()) {
    setStatus("Please complete the required fields with a valid email.", "err");
    return;
  }
  const data = Object.fromEntries(new FormData(form).entries());

  if (FORM_ENDPOINT) {
    setStatus("Sending…");
    try {
      const res = await fetch(FORM_ENDPOINT, {
        method: "POST",
        headers: { "Accept": "application/json", "Content-Type": "application/json" },
        body: JSON.stringify(data),
      });
      if (!res.ok) throw new Error(res.statusText);
      form.reset();
      setStatus("Thanks — we'll be in touch shortly.", "ok");
    } catch (err) {
      setStatus("Something went wrong. Please email " + FALLBACK_EMAIL + ".", "err");
    }
    return;
  }

  // No backend configured: hand off to the user's mail client.
  const subject = encodeURIComponent(`Fabric enquiry from ${data.name || "a visitor"}`);
  const body = encodeURIComponent(
    `Name: ${data.name || ""}\nEmail: ${data.email || ""}\nCompany: ${data.company || ""}\n\n${data.message || ""}`
  );
  window.location.href = `mailto:${FALLBACK_EMAIL}?subject=${subject}&body=${body}`;
  setStatus("Opening your email client…", "ok");
});
