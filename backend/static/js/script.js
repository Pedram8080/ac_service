// Counter animation function
function animateCounter(element, target, duration = 2000) {
    let start = 0;
    const increment = target / (duration / 16); // 60fps
    const timer = setInterval(() => {
        start += increment;
        if (start >= target) {
            element.textContent = target;
            clearInterval(timer);
        } else {
            element.textContent = Math.floor(start);
        }
    }, 16);
}

// Initialize counters when the page loads
document.addEventListener('DOMContentLoaded', function() {
    // Customer satisfaction counter
    const satisfactionCounter = document.getElementById('satisfaction-counter');
    if (satisfactionCounter) {
        animateCounter(satisfactionCounter, 98);
    }

    // Years of experience counter
    const experienceCounter = document.getElementById('experience-counter');
    if (experienceCounter) {
        animateCounter(experienceCounter, 15);
    }

    // Completed projects counter
    const projectsCounter = document.getElementById('projects-counter');
    if (projectsCounter) {
        animateCounter(projectsCounter, 1000);
    }
});

// Loader functionality
setTimeout(function() {
    document.getElementById('loader-wrapper').style.display = 'none';
}, 2000);

// Form validation and Persian to English number conversion
document.addEventListener('DOMContentLoaded', function() {
    // Convert Persian numbers to English
    function fa2en(str) {
        return str.replace(/[۰-۹]/g, function(d) {
            return '۰۱۲۳۴۵۶۷۸۹'.indexOf(d);
        });
    }

    // Form validation for request form
    var form = document.getElementById('request-form');
    if (form) {
        var phoneInput = form.querySelector('input[name="phone"]');
        var nameInput = form.querySelector('input[name="name"]');
        var serviceInputs = form.querySelectorAll('input[name="service_type"]');

        if (phoneInput) {
            phoneInput.addEventListener('input', function() {
                this.value = fa2en(this.value);
                this.setCustomValidity('');
            });
        }

        form.addEventListener('submit', function(e) {
            let valid = true;

            // Name validation
            if (nameInput && !nameInput.value.trim()) {
                nameInput.setCustomValidity('لطفا نام و نام خانوادگی را وارد کنید');
                nameInput.reportValidity();
                valid = false;
            } else if (nameInput) {
                nameInput.setCustomValidity('');
            }

            // Phone validation
            if (phoneInput && !phoneInput.value.trim()) {
                phoneInput.setCustomValidity('لطفا شماره تماس را وارد کنید');
                phoneInput.reportValidity();
                valid = false;
            } else if (phoneInput && !/^09[0-9]{9}$/.test(phoneInput.value)) {
                phoneInput.setCustomValidity('شماره تماس باید با 09 شروع شده و 11 رقم باشد');
                phoneInput.reportValidity();
                valid = false;
            } else if (phoneInput) {
                phoneInput.setCustomValidity('');
            }

            // Service validation
            if (serviceInputs.length > 0) {
                let serviceChecked = false;
                serviceInputs.forEach(function(input) {
                    if (input.checked) serviceChecked = true;
                });
                if (!serviceChecked) {
                    alert('لطفا نوع سرویس را انتخاب کنید');
                    valid = false;
                }
            }

            if (!valid) {
                e.preventDefault();
            }
        });
    }

    // Book animation functionality
    const books = document.querySelectorAll(".book");
    if (books.length > 0) {
        books.forEach(book => {
            book.addEventListener("click", e => {
                e.stopPropagation();

                if (book.classList.contains("open")) {
                    book.classList.remove("open");
                } else {
                    books.forEach(b => b.classList.remove("open"));
                    book.classList.add("open");
                }
            });
        });

        document.addEventListener("click", () => {
            books.forEach(book => book.classList.remove("open"));
        });
    }

    // Phone input validation for all phone inputs
    var phoneInputs = document.querySelectorAll('input[name="phone"]');
    phoneInputs.forEach(function(input) {
        input.addEventListener('input', function() {
            this.value = fa2en(this.value);
            this.setCustomValidity('');
        });
        input.oninvalid = function(e) {
            if (!this.value) {
                this.setCustomValidity('لطفا شماره تماس را وارد کنید');
            } else if (!/^09[0-9]{9}$/.test(this.value)) {
                this.setCustomValidity('لطفا شماره تماس را صحیح و با اعداد انگلیسی وارد کنید');
            } else {
                this.setCustomValidity('');
            }
        }
    });

    // Required field validation
    var requiredFields = document.querySelectorAll('input[required], textarea[required], select[required]');
    requiredFields.forEach(function(field) {
        field.oninvalid = function(e) {
            if (this.name === 'phone') return;
            this.setCustomValidity('لطفا این فیلد را پر کنید');
        }
        field.oninput = function(e) {
            this.setCustomValidity('');
        }
    });

    // SweetAlert messages
    if (typeof djangoMessages !== 'undefined') {
        djangoMessages.forEach(function(msg) {
            Swal.fire({
                icon: msg.icon,
                title: msg.text,
                confirmButtonText: 'باشه'
            });
        });
    }
});

// Lazy loading for video
document.addEventListener('DOMContentLoaded', function() {
    const video = document.querySelector('video');
    if (video) {
        video.setAttribute('loading', 'lazy');
    }
});

document.addEventListener("DOMContentLoaded", function () {
  const video = document.getElementById("lazy-banner-video");
  if (!video) return;
  const sources = video.querySelectorAll("source");

  function tryPlayVideo() {
    video.play().catch((err) => {
      console.warn("Autoplay failed:", err);
    });
  }

  function loadVideoSources() {
    sources.forEach(source => {
      source.src = source.dataset.src;
    });
    video.load();
    tryPlayVideo();

    // تلاش دوباره بعد از تعامل کاربر (در صورت نیاز)
    document.addEventListener("click", tryPlayVideo, { once: true });
    document.addEventListener("touchstart", tryPlayVideo, { once: true });
    document.addEventListener("scroll", tryPlayVideo, { once: true });
  }

  if ("IntersectionObserver" in window) {
    const observer = new IntersectionObserver((entries, observer) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          loadVideoSources();
          observer.unobserve(video);
        }
      });
    });
    observer.observe(video);
  } else {
    // مرورگرهای قدیمی
    loadVideoSources();
  }
});
