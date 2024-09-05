function register_btn(){
    var username = document.getElementById("username").value;
    var email = document.getElementById("email").value;
    var password = document.getElementById("psw").value;
    var cpassword = document.getElementById("cpsw").value;
    console.log(username,password,cpassword)
    if( password == cpassword ){
           $.ajax({
                url: "http://127.0.0.1:3050/reg",
                type: "POST",
                data: {"username": username,
                        "email": email,
                         "password": password},
                success: function(response) {
                    if (response.msg === "registered") {
                        alert("Registered successfully");
                        window.location.replace("http://127.0.0.1:3008/login");
                    } else {
                        // Handle unexpected response
                        alert("Unexpected response from server");
                    }
                },
                error: function(xhr, status, error) {
                    var msg = "Error occurred during registration";
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
    else{
        alert("password and cpassword doesn't match");
    }

}