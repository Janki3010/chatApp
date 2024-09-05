function onLogout(){
    var url = "http://127.0.0.1:3050";
    var authToken = localStorage.getItem('auth_token');
    localStorage.removeItem('auth_token');
    localStorage.removeItem('u_name');
    localStorage.removeItem('u_id');
    localStorage.removeItem('userData');
    $(document).ready(function() {
        $('#logout-link').click(function(event) {
            event.preventDefault();
            $.ajax({
                url: url+'/logout',
                type: 'POST',
                headers: {
                    'Authorization': `Bearer ${authToken}`,
                    'Content-Type': 'application/json'
                },
                success: function(response) {
    //                console.log("Logged out successfully:", response);
                    alert("Logged out successfully!");
                    window.location.replace("http://127.0.0.1:3008/login");
                },
                error: function(xhr, status, error) {
                    console.error("Logout error:", error);
                }
            });
        });
    });

}

