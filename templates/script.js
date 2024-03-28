// Function to perform validation when the form is submitted
function validateForm() {
    var selectedSong = document.getElementById('song').value;
    if (!selectedSong) {
        alert('Please select a song.');
        return false; // Prevent form submission if no song is selected
    }
    return true; // Allow form submission if a song is selected
}

// Add an event listener to the form submission event for the form with id 'song-form'
document.getElementById('song-form').addEventListener('submit', function(event) {
    if (!validateForm()) {
        event.preventDefault(); // Prevent form submission if validation fails
        return; // Exit the function early if validation fails
    }

    // Prevent default form submission behavior
    event.preventDefault();

    // Get form data
    var formData = new FormData(this);

    // Create new XMLHttpRequest object
    var request = new XMLHttpRequest();

    // Specify HTTP method and URL
    request.open('POST', '/recom', true);

    // Define function to handle response
    request.onload = function() {
        if (request.status >= 200 && request.status < 400) {
            var response = request.responseText; // Get response from server
            document.getElementById('recommendations').innerHTML = response; // Update recommendations section with new content
        } else {
            console.error('Error receiving response from server.'); // Log error message
        }
    };

    // Define function to handle error
    request.onerror = function() {
        console.error('Error sending request to server.'); // Log error message
    };

    // Send form data to server
    request.send(formData);
});
