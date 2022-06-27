import React, { useEffect } from "react";
import moment from "moment";
import ErrorMessage from "./ErrorMessage";
import { UserContext } from "../context/UserContext";
import { useContext } from "react";
import { useState } from "react";
import LeadModal from "./LeadModal";

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

    const handleModal = () =>{
        setActiveModal(!activeModal);
        getLeads()
        setId(null)
    };

    return (
        <>
        <LeadModal 
        active={activeModal}
        handleModal={handleModal}
        token={token}
        id={id}
        setErrorMessage={setErrorMessage}/>

        <button className="button is-fullwidth mb-5 is-primary" onClick={()=> setActiveModal(true)}>
            Create Lead
            </button>
            <ErrorMessage message={errorMessage}/>
            {
                loaded && leads ? (
                <table className="table is-fullwidth">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>First Name</th>
                            <th>Last Name</th>
                            <th>Company</th>
                            <th>Email</th>
                            <th>Note</th>
                            <th>Last Updated</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {leads.map((lead)=>(
                         <tr key={lead.id}>
                            <td>{lead.id}</td>
                            <td>{lead.first_name}</td>
                            <td>{lead.last_name}</td>
                            <td>{lead.company}</td>
                            <td>{lead.email}</td>
                            <td>{lead.note}</td>
                            <td>{moment(lead.date_last_updated).format("Do MMM YY")}</td>
                            <td>
                            <div className="columns">
                            <button className="button is-primary is-light m-2" onClick={()=> setActiveModal(true) & setId(lead.id)}>Edit</button>
                            <button className="button is-danger is-light m-2">Delete</button>
                            </div>
                            </td>

                         </tr>))
                        }
                    </tbody>
                </table>
                ):(
                <p>Loading</p>
                )
            }
        </>
    )
};

export default Table