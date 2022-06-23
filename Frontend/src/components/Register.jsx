import React, { useState,useContext } from "react";

import { UserContext } from "../context/UserContext";
import ErrorMessage from "./ErrorMessage";

const Register = () => {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [confirmationPassword, setConfirmationPassword] = useState("");
    const [errorMessage, setErrorMessage] = useState("");
    const [, setToken] = useContext(UserContext);


    const submitRegistration = async () => {
        const requestOptions = {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email: email, hashed_password: password }),

        };

        const response = await fetch("/api/users", requestOptions);
        const data = await response.json();
        
        if (!response.ok) {
            setErrorMessage(data.detail);
        }
        else {
            setToken(data.acces_token)
        }
    };
    const handleSubmit = (e) => {
        e.preventDefault();
        if (password === confirmationPassword && password.length > 8) {
            submitRegistration();
            console.log("Tinside the function")
        }
        else {

            setErrorMessage("The password and the confirmation Password doesnt match");

        }
    };

    return (
        <div className="column">
            <form className="box" onSubmit={handleSubmit}>
                <h1 className="title has-text-centered">Register</h1>
                <div className="field">
                    <label className="lab">Email Address</label>
                    <div className="control">
                        <input type="email"
                            placeholder="Enter Email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            className="input"
                            required />
                    </div>
                </div>
                <div className="field">
                    <label className="lab">Password</label>
                    <div className="control">
                        <input type="password"
                            placeholder="Enter Password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            className="input"
                            required />
                    </div>
                </div>

                <div className="field">
                    <label className="lab">Confirmation Password</label>
                    <div className="control">
                        <input type="password"
                            placeholder="Enter Password"
                            value={confirmationPassword}
                            onChange={(e) => setConfirmationPassword(e.target.value)}
                            className="input"
                            required />
                    </div>
                </div>
                <ErrorMessage message={errorMessage} />
                <br />
                <button className="button is-primary" type="submit">
                    Register
                </button>
            </form>
        </div>
    );
};

export default Register;