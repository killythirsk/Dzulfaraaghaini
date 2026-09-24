/*
 * Small, dependency-free enhancements. Three independent pieces:
 *
 * 1. Lightbox — click any image wrapped in <a class="lightbox-link"> to view
 *    it full-size in a fading overlay. If the link has a data-group
 *    attribute, every other lightbox-link sharing that group on the current
 *    page becomes Next/Prev-able from inside the overlay (buttons, arrow
 *    keys, or swipe on touch). Progressive enhancement: if this script fails
 *    to load, the links still work, they just open the image directly.
 *
 * 2. Scene slider — the horizontal Scenes strip on the book page, stepped by
 *    its own on-page buttons.
 *
 * 3. Scroll reveal — catalog entries fade/rise gently into view as the page
 *    scrolls. Skipped entirely for prefers-reduced-motion.
 */
(function () {
  "use strict";

  var reduceMotion =
    window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------------- Lightbox ---------------- */
  var overlay = null;
  var lastFocused = null;
  var group = [];
  var groupIndex = 0;

  function buildOverlay() {
    overlay = document.createElement("div");
    overlay.className = "lightbox-overlay";
    overlay.setAttribute("role", "dialog");
    overlay.setAttribute("aria-modal", "true");
    overlay.setAttribute("aria-label", "Full-size image");

    var prevBtn = document.createElement("button");
    prevBtn.type = "button";
    prevBtn.className = "lightbox-nav lightbox-nav--prev";
    prevBtn.setAttribute("aria-label", "Previous image");
    prevBtn.innerHTML = "&lsaquo;";
    prevBtn.addEventListener("click", function () { showAt(groupIndex - 1); });
    overlay.appendChild(prevBtn);

    var img = document.createElement("img");
    img.className = "lightbox-image";
    overlay.appendChild(img);

    var nextBtn = document.createElement("button");
    nextBtn.type = "button";
    nextBtn.className = "lightbox-nav lightbox-nav--next";
    nextBtn.setAttribute("aria-label", "Next image");
    nextBtn.innerHTML = "&rsaquo;";
    nextBtn.addEventListener("click", function () { showAt(groupIndex + 1); });
    overlay.appendChild(nextBtn);

    var caption = document.createElement("p");
    caption.className = "lightbox-caption";
    caption.setAttribute("aria-live", "polite");
    overlay.appendChild(caption);

    var closeBtn = document.createElement("button");
    closeBtn.type = "button";
    closeBtn.className = "lightbox-close";
    closeBtn.setAttribute("aria-label", "Close");
    closeBtn.innerHTML = "&times;";
    closeBtn.addEventListener("click", closeLightbox);
    overlay.appendChild(closeBtn);

    overlay.addEventListener("click", function (e) {
      if (e.target === overlay) closeLightbox();
    });

    var touchStartX = null;
    overlay.addEventListener(
      "touchstart",
      function (e) { touchStartX = e.touches[0].clientX; },
      { passive: true }
    );
    overlay.addEventListener("touchend", function (e) {
      if (touchStartX === null) return;
      var dx = e.changedTouches[0].clientX - touchStartX;
      touchStartX = null;
      if (Math.abs(dx) < 40) return;
      showAt(dx < 0 ? groupIndex + 1 : groupIndex - 1);
    });

    document.body.appendChild(overlay);
  }

  function showAt(index) {
    if (!group.length) return;
    groupIndex = (index + group.length) % group.length;
    var item = group[groupIndex];
    var imgEl = overlay.querySelector(".lightbox-image");
    var captionEl = overlay.querySelector(".lightbox-caption");
    imgEl.style.opacity = "0";
    window.setTimeout(
      function () {
        imgEl.src = item.src;
        imgEl.alt = item.alt;
        var text = item.alt || "";
        if (group.length > 1) {
          text = (groupIndex + 1) + " of " + group.length + (text ? " \u2014 " + text : "");
        }
        captionEl.textContent = text;
        imgEl.style.opacity = "1";
      },
      reduceMotion ? 0 : 120
    );
  }

  function openLightbox(link) {
    if (!overlay) buildOverlay();

    var groupName = link.getAttribute("data-group");
    var links = groupName
      ? document.querySelectorAll('.lightbox-link[data-group="' + groupName + '"]')
      : [link];
    group = Array.prototype.map.call(links, function (el) {
      var img = el.querySelector("img");
      return { src: el.getAttribute("data-full") || el.getAttribute("href"), alt: img ? img.alt : "" };
    });
    groupIndex = Array.prototype.indexOf.call(links, link);
    if (groupIndex < 0) groupIndex = 0;

    overlay.classList.toggle("has-nav", group.length > 1);
    showAt(groupIndex);
    overlay.classList.add("is-open");
    document.body.classList.add("lightbox-open");
    lastFocused = link;
    overlay.querySelector(".lightbox-close").focus();
  }

  function closeLightbox() {
    if (!overlay || !overlay.classList.contains("is-open")) return;
    overlay.classList.remove("is-open");
    document.body.classList.remove("lightbox-open");
    if (lastFocused) lastFocused.focus();
  }

  document.addEventListener("click", function (e) {
    var link = e.target.closest ? e.target.closest(".lightbox-link") : null;
    if (!link) return;
    e.preventDefault();
    openLightbox(link);
  });

  document.addEventListener("keydown", function (e) {
    if (!overlay || !overlay.classList.contains("is-open")) return;
    if (e.key === "Escape") closeLightbox();
    if (e.key === "ArrowLeft") showAt(groupIndex - 1);
    if (e.key === "ArrowRight") showAt(groupIndex + 1);
  });

  /* ---------------- Image protection (a deterrent, not a lock) ----------------
     Blocks the right-click / long-press menu and dragging on images and
     image links. Anyone determined can still get an image another way. */
  document.addEventListener("contextmenu", function (e) {
    if (e.target.closest && e.target.closest("img, .lightbox-link, .lightbox-overlay")) e.preventDefault();
  });
  document.addEventListener("dragstart", function (e) {
    if (e.target.tagName === "IMG") e.preventDefault();
  });

  /* ---------------- Scene slider (horizontal scroll + step buttons) ---------------- */
  (function initSceneSlider() {
    var gallery = document.querySelector(".scene-gallery");
    var prevBtn = document.querySelector(".scene-btn--prev");
    var nextBtn = document.querySelector(".scene-btn--next");
    if (!gallery || !prevBtn || !nextBtn) return;

    function stepSize() {
      var item = gallery.querySelector("li");
      if (!item) return gallery.clientWidth;
      var gap = parseFloat(getComputedStyle(gallery).columnGap || 0) || 0;
      return item.getBoundingClientRect().width + gap;
    }

    function updateButtons() {
      var maxScroll = gallery.scrollWidth - gallery.clientWidth - 1;
      prevBtn.disabled = gallery.scrollLeft <= 0;
      nextBtn.disabled = gallery.scrollLeft >= maxScroll;
    }

    prevBtn.addEventListener("click", function () {
      gallery.scrollBy({ left: -stepSize(), behavior: reduceMotion ? "auto" : "smooth" });
    });
    nextBtn.addEventListener("click", function () {
      gallery.scrollBy({ left: stepSize(), behavior: reduceMotion ? "auto" : "smooth" });
    });
    gallery.addEventListener("scroll", updateButtons);
    window.addEventListener("resize", updateButtons);
    updateButtons();
  })();

  /* ---------------- Scroll reveal ---------------- */
  if (!reduceMotion && "IntersectionObserver" in window) {
    var targets = document.querySelectorAll(".catalog-list .entry");
    if (targets.length) {
      targets.forEach(function (el) { el.classList.add("reveal"); });
      var io = new IntersectionObserver(
        function (entries) {
          entries.forEach(function (entry) {
            if (entry.isIntersecting) {
              entry.target.classList.add("revealed");
              io.unobserve(entry.target);
            }
          });
        },
        { threshold: 0.15 }
      );
      targets.forEach(function (el) { io.observe(el); });
    }
  }
})();
