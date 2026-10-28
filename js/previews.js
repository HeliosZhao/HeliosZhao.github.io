// Keep native controls available when autoplay, JavaScript, or observers are unavailable.
(() => {
  if (!('IntersectionObserver' in window)) return;

  const videos = document.querySelectorAll('video[data-preview]');
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  const visible = new Set();

  const update = (video) => {
    if (!visible.has(video) || reducedMotion.matches || document.hidden) {
      video.pause();
      return;
    }

    video.play().catch(() => {
      // The visitor can still start playback with the native controls.
    });
  };

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(({ target, isIntersecting }) => {
      if (isIntersecting) visible.add(target);
      else visible.delete(target);
      update(target);
    });
  });

  videos.forEach((video) => {
    video.muted = true;
    observer.observe(video);
  });

  reducedMotion.addEventListener('change', () => videos.forEach(update));
  document.addEventListener('visibilitychange', () => videos.forEach(update));
})();
