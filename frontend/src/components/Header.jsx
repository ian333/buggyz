import React from "react";
import { useContext } from "react";
import { UserContext } from "../context/UserContext";
import {ReactComponent as Logo} from "../Lady_bug.svg"



const Header =({title}) => {
    const [token,setToken] = useContext(UserContext);

    const handleLogout=() =>{
        setToken(null)
    };
    return(

        <div className="has-text-centered is-size-1 m-6">
            <h1 className="title">{title}
            <Logo style={{ height: 36, width: 60 }}/>
            </h1>
            {token &&(<button className="button" onClick={handleLogout}>Logout </button>)}
        </div>
    );
};

export default Header;