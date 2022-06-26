import React, { useContext, useState } from "react";
import { UserContext } from "../context/UserContext";
import ErrorMessage from "./ErrorMessage";



const Login = () => {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [, setToken] = useContext(UserContext);
    const [errorMessage, setErrorMessage] = useState("");

    const submitLogin = async () => {
        const requestOptions = {
            method: "POST",
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            body: JSON.stringify(
                `grant_type=&username=${email}&password=${password}&scope=&client_id=&client_secret=`
            ),
        };

        const response = await fetch("/api/token", requestOptions);
        const data = await response.json();

        if (!response.ok) {
            setErrorMessage(data.detail);
        }
        else {
            setToken(data.access_token);
        }
    };

    const handleSubmit = (e) => {

        e.preventDefault();
        submitLogin();
    };
    return (
        <div className="column">
            <form className="box" onSubmit={handleSubmit}>
                <h1 className="title has-text-centered">Login</h1>
                <div className="field">
                    <label className="label">Email Address</label>
                    <div className="control">
                        <input
                            type="email"
                            autoComplete="email"
                            placeholder="Enter email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            className="input"
                            required
                        />
                    </div>
                </div>
                <div className="field">
                    <label className="label">Password</label>
                    <div className="control">
                        <input
                            type="password"
                            placeholder="Enter password"
                            autoComplete="new-password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            className="input"
                            required
                        />
                    </div>
                </div>
                <ErrorMessage message={errorMessage} />
                <br />
                <button className="button is-primary" type="submit">
                    Login
                </button>
            </form>
        </div>
    );


};

export default Login;