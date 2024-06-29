import makeToastNotification from "../../../static/helper.js";
import { eyeToggle } from "/static/helper.js";

const element = (className) => document.querySelector(className)

eyeToggle(
    element("#logpassword-icon-container"),
    element("#logpassword"),
    element("#logeye"),
    element("#log-eye-off")
);

const toRegister = element("#to-register");

toRegister.addEventListener("click", () => {
    window.location = "/register";
});

element("#login-button").addEventListener("click", (event) => {
    
    event.preventDefault();

    const formData = new FormData(element(".authentication-form"));

    fetch(element(".authentication-form").getAttribute("data-route"), {
        method: "POST",
        body: formData,
    })
    .then((response) => response.json())
    .then((response) => {

        if (response.status === "success") {
            if (response.url) {
                window.location.href = response.url;
            }
        } else {
            if (response.message) {
                response.message.forEach((message) => {
                    makeToastNotification(message);
                });
            }
        }

    })
    .catch((error) => {
        console.log(error);
    });
});
