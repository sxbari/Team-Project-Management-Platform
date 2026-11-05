import { useState } from "react";
import { useNavigate } from "react-router-dom";
function LoginPage() {
    const navigate = useNavigate();
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [message, setMessage] = useState("");

    async function handleSubmit(e){
        e.preventDefault();
        try{
            const csrfResponse = await fetch('/api/csrf/');
            if (!csrfResponse.ok){
                throw new Error("could not fetch csrf token");
            }
            const csrfData = await csrfResponse.json();
            const response = await fetch("/api/login/",{
                method : "POST",
                headers : {
                    "Content-Type" : "application/json",
                    "X-CSRFToken" : csrfData.csrfToken
                },

                credentials : "same-origin",
                body :JSON.stringify({
                    username : username,
                    password : password
                })
            })
            const data = await response.json();
            if (response.ok){
                setMessage("Login successful");
                navigate("/homepage");
            } else{
                setMessage(data.error || "Login failed");
            }
        } 
        catch(error){
            console.error("Error during login:", error);
            setMessage("An error occurred during login.");
        }

    }

    return(
        <div>
            <h1>Login Page</h1>
            <form onSubmit={handleSubmit}>
                <div>
                    <input
                        type="text"
                        id="username"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                    />
                </div>
                <div>
                    <input
                        type="password"
                        id="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                    />
                </div>
                <button type="submit">Login</button>
            </form>
            <p>{message}</p>
            
        </div>
    );
}
export default LoginPage;