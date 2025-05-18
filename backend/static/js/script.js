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
