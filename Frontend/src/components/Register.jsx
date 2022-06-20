import React, { useState } from "react";
import { useContext } from "react";
import { UserContext } from "../context/UserContext";

const Register =() =>{
    const [email,setEmail]=useState("");
    const [password,setPassword]=useState("");
    const [confirmationPassword,setConfirmationPassword]=useState("");
    const [errorMessage,setErrorMessage]=useState("");
    const [,setToken]=useContext(UserContext);
    
    return(
        <div className="column">
            <form className="box">
                <h1 className="title has-text-centered">Register</h1>
                <div className="field">
                    <label className="lab">Email Address</label>
                    <div className="control">
                        <input type="email" placeholder="Enter Email" value={email} onChange={(e)=> setEmail(e)}/>
                    </div>
                </div>
            </form>
        </div>
    )
};