import { initializeApp } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-app.js";
import { getAnalytics } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-analytics.js";
import { getAuth ,GoogleAuthProvider,signInWithPopup} from "https://www.gstatic.com/firebasejs/10.8.0/firebase-auth.js";
    
const firebaseConfig = {
    apiKey: "AIzaSyAtGqd3drPh4ZfE3DIw09PHL8gC_oqzpVw",
    authDomain: "news-magazine-894e1.firebaseapp.com",
    projectId: "news-magazine-894e1",
    storageBucket: "news-magazine-894e1.appspot.com",
    messagingSenderId: "717349651714",
    appId: "1:717349651714:web:133957fec9243c20a52e1b",
    measurementId: "G-H0SEB6FJPQ"
  };

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);
const provider = new GoogleAuthProvider();
const auth = getAuth(app);
auth.languageCode = 'en'
const googleLogin = document.getElementById("google-login-btn");
googleLogin.addEventListener("click", function() {
    signInWithPopup(auth, provider)
        .then((result) => {
            const credential = GoogleAuthProvider.credentialFromResult(result);
            const token = credential.accessToken;
            const user = result.user;
            
            if (user.email === "su-23019@sitare.org") {
                window.location.href = "../templates/signup.html";
            } else{         
            window.location.href = "../templates/index.html";
            }
        })
        .catch((error) => {
            const errorCode = error.code;
            const errorMessage = error.message;
            const email = error.customData.email;
            const credential = GoogleAuthProvider.credentialFromError(error);
        });
});
