var url = "http://127.0.0.1:3050";
function login_btn(){
    var email = document.getElementById("email").value;
    var password = document.getElementById("password").value;
    console.log(email,password);
    $.ajax({
        url: url+"/verify",
        type: "POST",
        data: {"email": email,
               "password": password},
        success: function(response) {
            if (response.msg === "loggedin") {
                const authToken = response.data.access_token;
                const uid = response.data.id;
                const user_name = response.data.name;
                localStorage.setItem('auth_token', authToken);
                localStorage.setItem('u_id', uid);
                localStorage.setItem('u_name', user_name);
                $.ajax({
                    url: url+"/home",
                    type: "POST",
                    contentType: "application/json",
                    headers: {
                        'Authorization': `Bearer ${authToken}`,
                        'Content-Type': 'application/json',
                        'Access-Control-Allow-Origin': '*'
                    },
                    success: function(response) {
                        if (response.msg === "success") {
                             const authToken = response.data.access_token;
                            // Store response.data in localStorage
                            localStorage.setItem('userData', JSON.stringify(response.data));
                            console.log(localStorage.getItem('userData'))
                            // Redirect to home page
                            window.location.replace("http://127.0.0.1:3008/home");
                        } else {
                            alert("Unexpected response from server");
                        }
                    },

                    error: function(xhr, status, error) {
                        console.log("errorrrrrrr")
                    }
                });

            } else {
                alert("Unexpected response from server");
            }

        },
        error: function(xhr, status, error) {
            var msg = "Error occurred during Login";
            if (xhr.responseJSON && xhr.responseJSON.msg) {
                msg = xhr.responseJSON.msg;
            } else if (xhr.responseText) {
                try {
                    var response = JSON.parse(xhr.responseText);
                    if (response && response.msg) {
                        msg = response.msg;
                    }
                } catch (e) {
                    console.error("Error parsing JSON response:", e);
                }
            }
            alert(msg);
        }
    });
}