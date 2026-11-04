import { useState } from 'react'
function RegisterPage(){
    const [username,setUsername] = useState("")
    const[email,setEmail] = useState("")
    const[password,setPassword]=useState("")
    return(
        <div>
        <h1>Register Page</h1>
        <form classname = "register-form">
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
        </div>
        
    )
}

export default RegisterPage