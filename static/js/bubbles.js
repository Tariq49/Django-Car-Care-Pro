document.addEventListener("DOMContentLoaded", function() {
    const bubbleContainer = document.createElement('div');
    bubbleContainer.id = 'bubble-container';
    document.body.appendChild(bubbleContainer);

    function createBubble() {
        const bubble = document.createElement('div');
        bubble.className = 'bubble';
        const size = Math.random() * 60 + 20 + 'px';
        bubble.style.width = size;
        bubble.style.height = size;
        bubble.style.top = Math.random() * 100 + '%';
        bubble.style.left = Math.random() * 100 + '%';
        bubbleContainer.appendChild(bubble);

        moveBubble(bubble);
    }

    function moveBubble(bubble) {
        const speed = Math.random() * 2 + 1; // Slow speed
        const direction = Math.random() * 360; // Random initial direction
        let x = parseFloat(bubble.style.left);
        let y = parseFloat(bubble.style.top);
        let dx = Math.cos(direction) * speed;
        let dy = Math.sin(direction) * speed;

        function animate() {
            x += dx;
            y += dy;

            if (x <= 0 || x >= window.innerWidth - bubble.offsetWidth) {
                dx *= -1;
            }
            if (y <= 0 || y >= window.innerHeight - bubble.offsetHeight) {
                dy *= -1;
            }

            bubble.style.left = `${x}px`;
            bubble.style.top = `${y}px`;

            requestAnimationFrame(animate);
        }

        animate();
    }

    
    for (let i = 0; i < 15; i++) {
        createBubble();
    }
});