import React, { createContext } from "react";
import { useEffect } from "react";
import { useState } from "react";
export const UserContext = createContext();

export const UserProvider= (props) => {

    const[token,setToken] = useState(localStorage.getItem("awesomeLeadsToken"))

    useEffect(()=>{
        const fetchUser = async() => {
            requestOptions ={
                method:"GET",
                headers:{
                    "Content-type":"application/json",
                    Authorization:"Bearer"+token,
                     
                }
            };
        const response = await fetch("/api/users/me",requestOptions);
        if (!response.ok){
            setToken(null);
        }
        localStorage.setItem(awesomeLeadsToken,token);
        };
        fetchUser()
    },[token]);
    return <UserContext.Provider value={[token,setToken]}>
        {props.children}
    </UserContext.Provider>
}