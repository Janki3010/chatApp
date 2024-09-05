var url = "http://127.0.0.1:3050";
var authToken = localStorage.getItem('auth_token');


function renderTable(userData) {
    let tableHtml = '<div class="container mt-3"><table border="1" class="table">';
    tableHtml += '<thead><tr><th>ID</th><th>Username</th><th>Email</th><th>Action</th></tr></thead>';
    tableHtml += '<tbody>';

    for (let i = 0; i < userData.length; i++) {
        tableHtml += `<tr><td>${i + 1}</td><td>${userData[i][1]}</td><td>${userData[i][2]}</td><td><button type="button" class="btn btn-primary accept-btn" id="user_id" data-user-id="${userData[i][0]}">Accept</button></td></tr>`;
    }
    tableHtml += '</tbody></table></div>';

    return tableHtml;
}


document.addEventListener('DOMContentLoaded', function() {
    $.ajax({
            url: url+"/view_request",
            type: "POST",
            headers: {
                'Authorization': `Bearer ${authToken}`,
                'Content-Type': 'application/json'
            },
            success: function(response) {
                 if (response.msg == "success") {
                        console.log(response.data);
                        document.getElementById('data').innerHTML = renderTable(response.data);
                    }
            },

            error: function(xhr, status, error) {
                alert("error");
                console.log("errorrrrrrr");
            }
    });

});

document.addEventListener('click', function(event) {
    if (event.target.classList.contains('accept-btn')) {

        var acceptUserId = "";
        var payload = {};
        acceptUserId = event.target.getAttribute('data-user-id');
        payload = {"request_id": acceptUserId};
        var authToken = localStorage.getItem('auth_token');
        $.ajax({
                url: url+"/accept_request",
                type: "POST",
                data: JSON.stringify(payload),
                headers: {
                    'Authorization': `Bearer ${authToken}`,
                    'Content-Type': 'application/json'
                },
                success: function(response) {
                     if (response.msg == "success") {
                            alert(response.msg);
                            console.log(response);
                            // Remove the userData entry where id matches requestedUserId
//                            userData = userData.filter(user => user.id !== requestedUserId);
//                            localStorage.setItem('userData', JSON.stringify(userData));
//                            document.getElementById('data').innerHTML = renderTable(userData);
                            document.getElementById('user_id').disabled = true;
                            document.getElementById('user_id').innerHTML = 'Accepted';
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