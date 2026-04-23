// Navbar scroll
const nav = document.getElementById('navbar');
const backTop = document.getElementById('backTop');

window.addEventListener('scroll', () => {
  if (window.scrollY > 50) {
    nav.classList.add('scrolled');
    backTop.classList.add('show');
  } else {
    nav.classList.remove('scrolled');
    backTop.classList.remove('show');
  }
});

// Reveal on scroll
const reveals = document.querySelectorAll('.reveal');
const observer = new IntersectionObserver((entries) => {
  entries.forEach(e => {
    if (e.isIntersecting) {
      e.target.classList.add('visible');
      observer.unobserve(e.target);
    }
  });
}, { threshold: 0.1, rootMargin: '0px 0px -60px 0px' });

reveals.forEach(el => observer.observe(el));

// ============= SMOOTH SCROLL & ACTIVE MENU =============
document.addEventListener('DOMContentLoaded', function () {
  const navLinks = document.querySelectorAll('.nav-link');
  if (navLinks.length === 0) return; // اگر منو نبود، خارج شو

  // Smooth scroll
  navLinks.forEach(link => {
    link.addEventListener('click', function (e) {
      e.preventDefault();
      const targetId = this.getAttribute('href');
      if (targetId && targetId !== '#') {
        const targetElement = document.querySelector(targetId);
        if (targetElement) {
          targetElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
          history.pushState(null, null, targetId);
        }
      }
    });
  });

  // Highlight active menu on scroll
  const sections = document.querySelectorAll('section[id]');
  if (sections.length) {
    const observerOptions = { threshold: 0.3 };
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const activeId = entry.target.getAttribute('id');
          navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('data-target') === activeId) {
              link.classList.add('active');
            }
          });
        }
      });
    }, observerOptions);
    sections.forEach(section => observer.observe(section));
  }
});

// ============= HAMBURGER MENU TOGGLE =============
document.addEventListener('DOMContentLoaded', function () {
  const hamburger = document.getElementById('hamburger');
  const navMenu = document.getElementById('navMenu');
  const body = document.body;

  if (hamburger && navMenu) {
    // باز و بسته کردن منو با کلیک روی همبرگر
    hamburger.addEventListener('click', function () {
      hamburger.classList.toggle('open');
      navMenu.classList.toggle('open');
      body.classList.toggle('menu-open');
    });

    // بستن منو بعد از کلیک روی هر لینک
    const navLinks = navMenu.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
      link.addEventListener('click', function () {
        hamburger.classList.remove('open');
        navMenu.classList.remove('open');
        body.classList.remove('menu-open');
      });
    });
  }
});