document.addEventListener("DOMContentLoaded", function() {
    console.log("DOM fully loaded and parsed");

    const checkboxes = document.querySelectorAll(".card-checkbox");

    if (checkboxes.length === 0) {
        console.log("No checkboxes found!");
        return;
    }

    console.log("Found checkboxes:", checkboxes);

    checkboxes.forEach(checkbox => {
        checkbox.addEventListener("change", handleCheckboxChange);
        console.log("Event listener attached to checkbox:", checkbox);
    });

    function handleCheckboxChange() {
        console.log("Checkbox state changed");

        const checkedCards = document.querySelectorAll(".card-checkbox:checked");
        const primaryKeys = Array.from(checkedCards).map(cb => cb.closest(".card").dataset.pk);

        console.log("Primary keys of checked cards:", primaryKeys);

        if (primaryKeys.length === 0) {
            console.log("No primary keys found!");
            return;
        }

        const payload = JSON.stringify({ primary_keys: primaryKeys });
        console.log("Payload to send:", payload);

        console.log("Sending fetch request to:", calculateTotalUrl);
        fetch(calculateTotalUrl, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCookie('csrftoken')  // Include CSRF token in headers
            },
            body: payload
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log("Response data:", data);
            // Handle response data
            const totalAmountElement = document.getElementById("total-amount");
            if (totalAmountElement) {
                totalAmountElement.textContent = `Total Amount: $${data.total_amount}`;
            }
        })
        .catch(error => {
            console.error('Error fetching data:', error);
        });
    }

    // Function to get CSRF token from cookies
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
