var url = "http://127.0.0.1:3050";
var userData = JSON.parse(localStorage.getItem('userData'));
function renderTable(userData) {
    let tableHtml = '<div class="container mt-3"><table border="1" class="table">';
    tableHtml += '<thead><tr><th>ID</th><th>Username</th><th>Email</th><th>Action</th></tr></thead>';
    tableHtml += '<tbody>';

    for (let i = 0; i < userData.length; i++) {
        tableHtml += `<tr>
                <td>${i + 1}</td>
                <td>${userData[i][1]}</td>
                <td>${userData[i][2]}</td>
                <td>`;

            if (userData[i][4] == null) {
                tableHtml += `<button type="button" class="btn btn-primary request-btn" id="user_id" data-user-id="${userData[i][0]}">Request</button>`;
            } else {
                tableHtml += `<button type="button" class="btn btn-primary pending-btn" id="user_id" data-user-id="${userData[i][0]}" disabled>Pending</button>`;
            }

            tableHtml += `</td>
</tr>`;

    }
    tableHtml += '</tbody></table></div>';

    return tableHtml;
}

document.addEventListener('DOMContentLoaded', function() {
    // Retrieve userData from localStorage
    if (userData) {
        document.getElementById('data').innerHTML = renderTable(userData);
        console.log(userData);
        // Now you can access userData and use it as needed on the home page
    } else {
        // Handle case where userData is not available
        console.error('userData not found in localStorage');
    }
});



// Function to handle button click event
document.addEventListener('click', function(event) {
    if (event.target.classList.contains('request-btn')) {

        var requestedUserId = "";
        var payload = {};
        requestedUserId = event.target.getAttribute('data-user-id');
        payload = {"friend_id": requestedUserId};
        var authToken = localStorage.getItem('auth_token');
        $.ajax({
                url: url+"/friend_request",
                type: "POST",
                data: JSON.stringify(payload),
                headers: {
                    'Authorization': `Bearer ${authToken}`,
                    'Content-Type': 'application/json'
                },
                success: function(response) {
                     if (response.msg == "Friend Request is Sent Successfully") {
                            alert(response.msg);

//                            document.getElementById('user_id').disabled = true;
//                            document.getElementById('user_id').innerHTML = 'Pending';
                            document.getElementById('data').innerHTML = renderTable(response.data);

                        }
                },

                error: function(xhr, status, error) {
                    alert("Friend user not found");
                    console.log("errorrrrrrr");
                }
        });

    }
});


