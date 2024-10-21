var apiUrl
async function fetchIpAddress() {
    try {
        const response = await fetch('/api/ip');
        const data = await response.json();
        console.log("API IP Address:", data.ip_address);
        // Set apiUrl to the full URL including protocol and port
        apiUrl = `${window.location.protocol}//${data.ip_address}:${window.location.port}`; 
    } catch (error) {
        console.error("Error fetching IP address:", error);
    }
}

async function fetchData() {
    if (!apiUrl) {
        console.error("API URL is not set. Please fetch the IP address first.");
        return; // Exit if apiUrl is not set
    }
    const response = await fetch(`${apiUrl}/api/data`);
    const data = await response.json();
    document.getElementById(`result`).innerText = JSON.stringify(data)
    console.log(data);
}
/* User Requests */
async function fetchUsers() {
    try {
        const response = await fetch(`${apiUrl}/users`);
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await response.json();
        document.getElementById('result1').innerText = JSON.stringify(data);
    } catch (error) {
        console.error('There was a problem with the fetch operation:', error);
    }
}
async function fetchUser_byid() {
    try {
        var user_id = document.getElementById('user_id').value;
        const response = await fetch(`${apiUrl}/users/` + user_id);
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await response.json();
        document.getElementById('result2').innerText = JSON.stringify(data);
    } catch (error) {
        console.error('There was a problem with the fetch operation:', error);
    }
}
async function fetchUser_byname() {
    try {
        var user_name = document.getElementById('user_name').value;
        const response = await fetch(`${apiUrl}/users/` + user_name);
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await response.json();
        document.getElementById('result3').innerText = JSON.stringify(data);
    } catch (error) {
        console.error('There was a problem with the fetch operation:', error);
    }
}
async function createUser() {
    // User data to be sent in the request
    const userData = {
        firstName: document.getElementById(`user_firstName`).value,
        lastName: document.getElementById(`user_lastName`).value,
        tagNum: document.getElementById(`user_tagNum`).value,
        email: document.getElementById(`user_email`).value,
        password: "your_password_here" // Make sure to handle passwords securely
    };

    try {
        const response = await fetch(`${apiUrl}/users`, {
            method: 'POST', // Specify the request method
            headers: {
                'Content-Type': 'application/json' // Indicate that we're sending JSON
            },
            body: JSON.stringify(userData) // Convert the user data to a JSON string
        });

        // Check if the response is OK (status in the range 200-299)
        if (response.ok) {
            const result = await response.json(); // Parse the JSON response
            console.log('User created successfully:', result);
        } else {
            const error = await response.json(); // Parse the error response
            console.error('Error creating user:', error);
        }
    } catch (error) {
        console.error('Network error:', error); // Handle network errors
    }
}

/* Permission Requests */



/* Onlinetime Requests */



/* Totaltime Requests */



fetchIpAddress();


