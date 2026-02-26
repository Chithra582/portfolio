// Nav scroll effect
  window.addEventListener('scroll', () => {
    document.getElementById('nav').classList.toggle('scrolled', scrollY > 40);
  });

  // Skill bars — animate on scroll into view
  const skillObs = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        const fill = e.target.querySelector('.skill-fill');
        const val = e.target.dataset.fill || 0;
        if (fill) fill.style.width = val + '%';
        skillObs.unobserve(e.target);
      }
    });
  }, { threshold: 0.2 });
  document.querySelectorAll('.skill-chip').forEach(el => skillObs.observe(el));
