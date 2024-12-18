/* User Requests */
async function fetchAllUsers() {
    try {
        const response = await fetch(`/users/all`);  // Use /users/all to match the route
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await response.json();
        document.getElementById('result1').innerText = JSON.stringify(data); // Display user data
    } catch (error) {
        console.error('There was a problem with the fetch operation:', error);
    }
}

async function fetchUser_byid() {
    try {
        const response = await fetch(`/users`);  // This will use the logged-in user ID
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await response.json();
        document.getElementById('result2').innerText = JSON.stringify(data); // Display user data
    } catch (error) {
        console.error('There was a problem with the fetch operation:', error);
    }
}

async function fetchUser_byname() {
    try {
        const user_name = document.getElementById('user_name').value;  // Get user name from input field
        const response = await fetch(`/users/${user_name}`);  // This will send the correct user name
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await response.json();
        document.getElementById('result3').innerText = JSON.stringify(data); // Display user data
    } catch (error) {
        console.error('There was a problem with the fetch operation:', error);
    }
}

async function createUser() {
    const userData = {
        firstName: document.getElementById('user_firstName').value,
        lastName: document.getElementById('user_lastName').value,
        tagNum: document.getElementById('user_tagNum').value,
        email: document.getElementById('user_email').value,
        password: document.getElementById('user_password').value  // Ensure you have a password field
    };

    try {
        const response = await fetch(`/users`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(userData)
        });

        if (response.ok) {
            const result = await response.json();
            console.log('User created successfully:', result);
        } else {
            const error = await response.json();
            console.error('Error creating user:', error);
        }
    } catch (error) {
        console.error('Network error:', error);
    }
}

async function editUser() {
    const userData = {
        firstName: document.getElementById('user_edit_firstName').value,
        lastName: document.getElementById('user_edit_lastName').value,
        email: document.getElementById('user_edit_email').value
    };

    const user_id = document.getElementById('user_edit_id').value; // Make sure to add a field to get the user ID

    try {
        const response = await fetch(`/users/${user_id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(userData)
        });

        if (response.ok) {
            const result = await response.json();
            console.log('User updated successfully:', result);
        } else {
            const error = await response.json();
            console.error('Error updating user:', error);
        }
    } catch (error) {
        console.error('Network error:', error);
    }
}

async function deleteUser() {
    try {
        const user_id = document.getElementById('user_delete_id').value;
        const response = await fetch(`/users/${user_id}`, {
            method: 'DELETE'
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await response.json();
        document.getElementById('result3').innerText = JSON.stringify(data);
    } catch (error) {
        console.error('There was a problem with the fetch operation:', error);
    }
}

/* Permission Requests */
async function fetchPermissions() {
    try {
        const response = await fetch(`/permissions`);
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await response.json();
        document.getElementById('result8').innerText = JSON.stringify(data); // Display permission data
    } catch (error) {
        console.error('There was a problem with the fetch operation:', error);
    }
}

/* Onlinetime Requests */
async function fetchALLOnlineTime() {
    try {
        const response = await fetch(`/onlinetime/all`);
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await response.json();
        document.getElementById('result6').innerText = JSON.stringify(data); // Display online time data
    } catch (error) {
        console.error('There was a problem with the fetch operation:', error);
    }
}

async function fetchOnlineTime() {
    try {
        const response = await fetch(`/onlinetime`);
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await response.json();
        document.getElementById('result7').innerText = JSON.stringify(data); // Display online time data
    } catch (error) {
        console.error('There was a problem with the fetch operation:', error);
    }
}

async function startSession() {
    try {
        const csrfToken = document.querySelector('[name=csrf_token]').value;  // Get CSRF token from the form

        const response = await fetch(`/onlinetime/start`, {
            method: 'POST', // Specify the request method
            headers: {
                'Content-Type': 'application/json',  // Indicate that we're sending JSON
                'X-CSRFToken': csrfToken  // Include CSRF token in the header
            }
        });

        if (response.ok) {
            const result = await response.json(); // Parse the JSON response
            console.log('Session started successfully:', result);
        } else {
            const error = await response.json(); // Parse the error response
            console.error('Error starting session:', error);
        }
    } catch (error) {
        console.error('Network error:', error); // Handle network errors
    }
}


async function stopSession() {
    try {
        const csrfToken = document.querySelector('[name=csrf_token]').value;  // Get CSRF token from the form

        const response = await fetch(`/onlinetime/stop`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',  // Indicate that we're sending JSON
                'X-CSRFToken': csrfToken  // Include CSRF token in the header
            }
        });

        if (response.ok) {
            const result = await response.json();
            console.log('Session stopped successfully:', result);
        } else {
            const error = await response.json();
            console.error('Error stopping session:', error);
        }
    } catch (error) {
        console.error('Network error:', error);
    }
}

async function editOnlineTime() {
    // Get and trim the input values
    const user_id = document.getElementById('user_id').value.trim();
    const session_time_identifier = document.getElementById('session_time_identifier').value.trim();
    const dateTimeStart = document.getElementById('dateTimeStart').value.trim();
    const dateTimeStop = document.getElementById('dateTimeStop').value.trim();

    const data = {
        dateTimeStart: dateTimeStart,
        dateTimeStop: dateTimeStop
    };

    const csrfToken = document.querySelector('[name=csrf_token]').value;

    try {
        const response = await fetch(`/onlinetime/edit/${user_id}/${session_time_identifier}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify(data)
        });

        if (response.ok) {
            const result = await response.json();
            document.getElementById('result8').innerText = JSON.stringify(result);
            console.log('Online time updated successfully:', result);
        } else {
            const error = await response.json();
            document.getElementById('result8').innerText = JSON.stringify(error);
            console.error('Error updating online time:', error);
        }
    } catch (error) {
        console.error('Network error:', error);
        document.getElementById('result8').innerText = 'Network error occurred.';
    }
}



async function deleteOnlineTime() {
    const user_id = document.getElementById('user_delete_id').value.trim();
    const session_time_identifier = document.getElementById('session_time_identifier1').value.trim();

    // Scope to the parent container of the "Delete OnlineTime" section
    const deleteSection = document.getElementById('delete-onlinetime-section'); // Add an ID to the delete section
    const csrfToken = deleteSection.querySelector('[name=csrf_token]').value; // Select the CSRF token within this section

    console.log(`CSRF Token: ${csrfToken}`); // Debugging

    try {
        const response = await fetch(`/onlinetime/${user_id}/${session_time_identifier}`, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': csrfToken
            }
        });

        if (response.ok) {
            const data = await response.json();
            document.getElementById('result4').innerText = JSON.stringify(data); // Display success message
            console.log('Online time deleted successfully:', data);
        } else {
            const error = await response.json();
            document.getElementById('result4').innerText = JSON.stringify(error); // Display error message
            console.error('Error deleting online time:', error);
        }
    } catch (error) {
        console.error('Network error:', error);
        document.getElementById('result4').innerText = 'Network error occurred.';
    }
}




/* Totaltime Requests */
async function fetchTotalTime() {
    try {
        const response = await fetch(`/totaltime`);
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await response.json();
        document.getElementById('result6').innerText = JSON.stringify(data); // Display total time data
    } catch (error) {
        console.error('There was a problem with the fetch operation:', error);
    }
}

async function fetchAllTotalTime() {
    try {
        const response = await fetch(`/totaltime/all`);
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await response.json();
        document.getElementById('result7').innerText = JSON.stringify(data); // Display all total time data
    } catch (error) {
        console.error('There was a problem with the fetch operation:', error);
    }
}