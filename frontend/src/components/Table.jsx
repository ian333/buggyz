import React, { useEffect } from "react";
import moment from "moment";
import ErrorMessage from "./ErrorMessage";
import { UserContext } from "../context/UserContext";
import { useContext } from "react";
import { useState } from "react";

const Table = () => {
    const [token] = useContext(UserContext);
    const [leads, setLeads] = useState(null);
    const [errorMessage, setErrorMessage] = useState("");
    const [loaded, setLoaded] = useState(false);
    const [activeModal, setActiveModal] = useState(false)
    const [id, setId] = useState(null)

    const getLeads = async () => {
        const requestOptions = {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                Authorization: "Bearer " + token,
            }
        };
        const response = await fetch("/api/leads", requestOptions);
        const data = await response.json()

        if (!response.ok) {
            console.log("Something went wrong. Couldnt load Leads");
        }
        else {
            setLeads(data);
            setLoaded(true);
        }
    };
    useEffect(()=>{
        getLeads()
    },[])

    return (
        <>
        <button className="button is-fullwidht mb-5 is-primary">
            Create Lead
            </button>
            <ErrorMessage message={errorMessage}/>
            {
                loaded && leads ? 
                <table className="table is-fullwidht">
                    <thead>
                        <tr></tr>
                    </thead>

                </table>:<p>Loading</p>
            }
        </>
    )
};