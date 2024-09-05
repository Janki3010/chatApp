var url = "http://127.0.0.1:3050";
var authToken = localStorage.getItem('auth_token');


function renderTable(userData) {
    let tableHtml = '<div class="container mt-3"><table border="1" class="table">';
    tableHtml += '<thead><tr><th>ID</th><th>Username</th><th>Email</th><th>Chat</th></tr></thead>';
    tableHtml += '<tbody>';

    for (let i = 0; i < userData.length; i++) {
        tableHtml += `<tr>
                <td>${i + 1}</td>
                <td>${userData[i].username}</td>
                <td>${userData[i].email}</td>
                <td>
                    <button type="button" class="btn btn-primary request-btn"
                            onclick="redirectToChat('${userData[i].id}')">
                        Chat
                    </button>
                </td>
              </tr>`;
    }
    tableHtml += '</tbody></table></div>';

    return tableHtml;
}


document.addEventListener('DOMContentLoaded', function() {
    $.ajax({
            url: "http://127.0.0.1:3050/my-friends",
            type: "POST",
            contentType: "application/json",
            headers: {
                'Authorization': `Bearer ${authToken}`,
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            success: function(response) {
                 if (response) {
                        //alert(response.msg);
                        document.getElementById('data').innerHTML = renderTable(response.data);
                        console.log(response.data);
                    }
            },

            error: function(xhr, status, error) {
                alert("error")
                console.log("errorrrrrrr")
            }
    });



});


function redirectToChat(userId) {

    window.location.href = `/chat/${userId}`;
}