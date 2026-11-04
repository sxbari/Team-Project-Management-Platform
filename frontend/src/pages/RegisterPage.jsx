import { useState } from 'react'
function RegisterPage(){
    const [username,setUsername] = useState("")
    const[email,setEmail] = useState("")
    const[password,setPassword]=useState("")
    const[message,setMessage] = useState("")

    async function handleSubmit(e) {
        e.preventDefault();

        try{
            const csrfResponse = await fetch("/api/csrf/");
            if (!csrfResponse.ok){
                throw new Error("could not fetch csrf token");
            }
            const csrfData = await csrfResponse.json();

            const response = await fetch("/api/register/",{
                method : "POST",
                headers : {
                    "Content-Type" : "application/json",
                    "X-CSRFToken" : csrfData.csrfToken
                },
            credentials: "same-origin",
            body : JSON.stringify({
                username : username,
                email : email,
                password : password
            })
        });

        const data = await response.json();
        if (response.ok){
            setMessage("Registration successfull");
        } else{
            setMessage(data.error || "Registration failed");
        }

    }catch (error) {
            console.error("Error during registration:", error);
        }
    }
    return(
        <div>
        <h1>Register Page</h1>
        <form classname = "register-form" onSubmit={handleSubmit}>
            <input 
            type="text" 
            placeholder = "username"
            value = {username}
            onChange={(e) => setUsername(e.target.value)}
            />
            <br/>
            <input 
            type="email" 
            placeholder="email" 
            value = {email} 
            onChange={(e) => setEmail(e.target.value)}
            />
            <br/>
            <input 
            type="password" 
            placeholder="password" 
            value = {password} 
            onChange={(e) => setPassword(e.target.value)}
            />
            <br/>
            <button type="submit">Register</button>
        </form>
        <p>{message}</p>
        </div>

        
        
    )
}

export default RegisterPage