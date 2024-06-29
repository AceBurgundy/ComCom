import makeToastNotification from "../../../static/helper.js";
import { eyeToggle } from "/static/helper.js";

const element = (className) => document.querySelector(className);

element("#to-login").addEventListener("click", () => window.location = "/login");

const pattern = /(where)|(select)|(update)|(delete)|(.schema)|(from)|(drop)|[0-9]|[!@#$%^&*()_+}{":?></*+[;'./,]|-/gi;
const userNameCircle = element("#first-name-circle");
const formRegister = element("#form-register");
const emailCircle = element("#email-circle");
const regPassword = element("#regpassword");
const email = element("#register-email");
const userName = element("#username");

eyeToggle(
    element("#regpassword-icon-container"),
    regPassword,
    element("#regeye"),
    element("#reg-eye-off")
);

let stillHasErrors = true;

function validateForm(event = null) {

    function validateUsername() {
        if (userName.value.trim() !== "") {
            const usernameValidations = [
                userName.value.length > 2,
                userName.value.length < 30,
                !userName.value.match(pattern),
                userName.value.trim() !== ""
            ];
    
            if (!usernameValidations[0]) {
                userNameCircle.style.fill = "red";
                makeToastNotification("Username should have at least 3 characters.");
            } else if (!usernameValidations[1]) {
                userNameCircle.style.fill = "red";
                makeToastNotification("Username should have at most 30 characters.");
            } else if (!usernameValidations[2]) {
                userNameCircle.style.fill = "red";
                makeToastNotification("Username should not contain special characters or numbers.");
            } else if (!usernameValidations[3]) {
                userNameCircle.style.fill = "red";
                makeToastNotification("Username should not be empty.");
            } else {
                userNameCircle.style.fill = "green";
            }
    
            stillHasErrors = usernameValidations.includes(false) ? true : false
        }
    }

    function validateRegister() {
        if (email.value.trim() !== "") {
            const emailValidations = [
                email.value.match(/[@]/),
                email.value.match(".com"),
                email.value.trim() !== ""
            ];
            
            if (emailValidations[0] === null) {
                emailCircle.style.fill = "red";
                makeToastNotification("Missing @");
            } else if (emailValidations[1] === null) {
                emailCircle.style.fill = "red";
                makeToastNotification("Missing .com");
            } else if (!emailValidations[2]) {
                emailCircle.style.fill = "red";
                makeToastNotification("Email cannot be empty.");
            } else {
                emailCircle.style.fill = "green";
            }
    
            stillHasErrors = emailValidations.some(element => element === null || element === false);
        }
    }
    
    function validatePassword() {
        if (regPassword.value.trim() !== "") {
            const passwordValidations = [
                !regPassword.value.match(/(where)|(select)|(update)|(delete)|(.schema)|(from)|(drop)|-/gi),
                regPassword.value.match(/[0-9]/),
                regPassword.value.match(/[!@#$%^&*()_+}{":?></*+[;'./,]/),
            ];
    
            if (!passwordValidations[0]) {
                regPassword.style.color = "red";
                makeToastNotification("Password should not contain forbidden keywords.");
            } else if (passwordValidations[1] === null || passwordValidations[2] === null) {
                regPassword.style.color = "red";
                makeToastNotification("Password should contain at least one number and one special character.");
            } else {
                regPassword.style.color = "green";
            }
    
            stillHasErrors = passwordValidations.some(element => element === null || element === false);
        }
    }

    // calls the appropriate function for their designated inputs
    if (event) {
        const target = event.target;

        if (target.id === "regpassword") {
            validatePassword()
        }
    
        if (target.id === "register-email") {
            validateRegister()
        }
    
        if (target.id === "username") {
            validateUsername()
        }
    }

    if (!event) {
        validatePassword()
        validateRegister()
        validateUsername()
    }
}

[...formRegister.querySelectorAll("input")].forEach(element => 
    element.addEventListener("click", event => {
        validateForm(event)
    }
))

let intervalId = setInterval(() => {
    const filledElements = document.querySelectorAll("input:-webkit-autofill");

    if (filledElements.length > 0) {
      clearInterval(intervalId); // Stop the interval
      validateForm()
    }
  }, 100);
  
formRegister.addEventListener("keyup", event => validateForm(event, true));
formRegister.addEventListener("input", event => validateForm(event, true));
element("#register-button").addEventListener("click", (event) => {
    
    validateForm()
    
    if (stillHasErrors) return

    event.preventDefault();

    const formData = new FormData(element("#form-register"));

    fetch(element("#form-register").getAttribute("data-route"), {
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
