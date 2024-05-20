async function sha256(message) {
  // encode as UTF-8
  const msgBuffer = new TextEncoder().encode(message);

  // hash the message
  const hashBuffer = await crypto.subtle.digest("SHA-256", msgBuffer);

  // convert ArrayBuffer to Array
  const hashArray = Array.from(new Uint8Array(hashBuffer));

  // convert bytes to hex string
  const hashHex = hashArray
    .map((b) => b.toString(16).padStart(2, "0"))
    .join("");
  return hashHex;
}

function redirectToLogin() {
  window.location.href = "/login";
}
function verifyToken() {
  let auth = localStorage.getItem("auth");
  if (auth == null) {
    return;
  } else {
    fetch("/verifyToken", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        token: auth,
      }),
    }).then((res) => {
      if (res.status == 200) {
        window.location.href = "/home";
      } else {
        localStorage.removeItem("auth");
      }
    });
  }
}
window.onload = function () {
  verifyToken();
  document
    .getElementById("registerForm")
    .addEventListener("submit", async function (event) {
      event.preventDefault();

      var name = document.getElementById("name").value;
      var password = document.getElementById("password").value;
      var passwordconf = document.getElementById("passwordconf").value;
      if (name === "" || password === "" || passwordconf === "") {
        alert("Please fill in all fields");
        return;
      }
      console.log(name, password, passwordconf);
      if (password !== passwordconf) {
        alert("Passwords do not match");
        return;
      }
      if(password.length < 8){
        alert("Password must be at least 8 characters long");
        return;
      }
      password = await sha256(password);
      var data = {
        name: name,
        password: password,
      };
      fetch("/createUser", {
        method: "POST", // Change method to POST
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      }).then((response) => {
        if (response.status === 200) {
          window.location.href = "/login";
        } else {
          alert("Something went wrong. Please try again.");
        }
      });
    });
};
