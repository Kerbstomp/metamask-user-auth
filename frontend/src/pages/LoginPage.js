import React, { useContext } from "react";
import AuthContext from "../context/AuthContext";

const LoginPage = () => {
  let { loginUser } = useContext(AuthContext);

  return (
    <div>
      <button onClick={loginUser}>Login with metamask</button>
    </div>
  );
};

export default LoginPage;
