import { createContext, useState, useEffect } from "react";
import web3 from "../ethereum/web3";
import Cookies from "js-cookie";
import jwt_decode from "jwt-decode";
import { useNavigate } from "react-router-dom";

const AuthContext = createContext();

export default AuthContext;

export const AuthProvider = ({ children }) => {
  let [address, setAddress] = useState("");
  let [user, setUser] = useState(() =>
    localStorage.getItem("access_token")
      ? jwt_decode(localStorage.getItem("access_token"))
      : null
  );
  let [authToken, setAuthToken] = useState(() =>
    localStorage.getItem("access_token")
      ? localStorage.getItem("access_token")
      : null
  );

  let navigate = useNavigate();

  useEffect(() => {
    getUserAccountAddress();
  });

  let getUserAccountAddress = async () => {
    if (web3) {
      const accounts = await web3.eth.getAccounts();
      setAddress(accounts[0]);

      window.ethereum.on("accountsChanged", function (accounts) {
        setAddress(accounts[0]);
      });

      window.ethereum.on("disconnect", function (error) {
        window.alert("Your Metamask account must be connected to login!");
      });
    }
  };

  let loginUser = async (event) => {
    event.preventDefault();
    if (!web3) {
      window.alert("Metamask must be installed to login!");
      return;
    }

    await fetch(`http://127.0.0.1:8000/api/users/?public_address=${address}`) // MOVE URL TO ENV VARS
      .then((response) => {
        if (response.ok) return response.json();
      })
      .then((user) => (user ? user : handleCreateUser()))
      .then(handleSignMetamaskMessage)
      .then(handleAuthenticate)
      .catch((error) => console.log(error));
  };

  let handleCreateUser = async () => {
    let response = await fetch("http://127.0.0.1:8000/api/users/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFTOKEN": Cookies.get("csrftoken"),
      },
      body: JSON.stringify({ public_address: address }),
    });
    return await response.json();
  };

  let handleSignMetamaskMessage = async (user) => {
    let signature = await web3.eth.personal.sign(
      `I am signing my one-time nonce: ${user["nonce"]}`, // MOVE MESSAGE TO ENV VARS
      address,
      ""
    );

    return signature;
  };

  let handleAuthenticate = async (signature) => {
    let response = await fetch("http://127.0.0.1:8000/api/auth/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFTOKEN": Cookies.get("csrftoken"),
      },
      body: JSON.stringify({ public_address: address, signature: signature }),
    });

    if (response.ok) {
      let data = await response.json();
      user = jwt_decode(data.access_token);

      setAuthToken(data.access_token);
      setUser(user);
      localStorage.setItem("access_token", data.access_token);

      navigate("/");
    } else {
      window.alert("Authentication failed!");
    }
  };

  let logoutUser = () => {
    setAuthToken(null);
    setUser(null);
    localStorage.removeItem("access_token");

    navigate("/auth");
  };

  let contextData = {
    address: address,
    user: user,
    loginUser: loginUser,
    logoutUser: logoutUser,
  };

  return (
    <AuthContext.Provider value={contextData}>{children}</AuthContext.Provider>
  );
};
