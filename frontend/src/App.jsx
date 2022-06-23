import React, { useState, useEffect } from "react";
import Register from "./components/Register";
const App = () => {
  const [message, setMessage] = useState("");

  const getWelcomeMessage = async () => {
    const requestOptions = {
      method: "GET",
      headers: {
        "Content-Type": "application/json",

      },
    };
    const response = await fetch("/api", requestOptions);
    const data = await response.json()
    
    if (!response.ok){
      console.log("Something messed up");
    }
    else{
      setMessage(data.message);
    }
  };

  useEffect(() => {
    getWelcomeMessage();
  }, []);

  return (
    <div>
      <h1>{message}
      <Register/>
      </h1>
    </div>
  );
};


export default App;
