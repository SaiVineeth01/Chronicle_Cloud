// Load the sound file once at the top
const notificationSound = new Audio('/app/static/sounds/notification.mp3');

// Connect to WebSocket (Make sure to use the correct port)
const socket = io.connect('http://' + document.domain + ':5001');

socket.on('new_notification', function(data) {
    console.log('New notification received:', data);

    // Play the sound
    notificationSound.play().catch((error) => {
        console.warn('Sound playback failed:', error);
    });

    // Format the timestamp into a readable format
    const timestamp = new Date(data.created_at).toLocaleString();

    // Add the notification to your UI
    const notificationsList = document.getElementById('notificationsList');
    const notificationItem = document.createElement('div');
    notificationItem.classList.add('notification-item', 'new'); // 'new' for flash effect

    notificationItem.innerHTML = `
        <p>${data.message}</p>
        <small>${timestamp}</small> <!-- Display formatted timestamp -->
        <button onclick="markAsRead(${data.id})">Mark as Read</button>
    `;

    // Add to the top of the list
    notificationsList.prepend(notificationItem);

    // Optional: remove highlight after 2 seconds
    setTimeout(() => {
        notificationItem.classList.remove('new');
    }, 2000);
});
