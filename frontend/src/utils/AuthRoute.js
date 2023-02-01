import React, { useContext } from "react";
import { Navigate } from "react-router-dom";
import AuthContext from "../context/AuthContext";

const AuthRoute = ({ children, redirectTo }) => {
  let { user } = useContext(AuthContext);
  return user ? children : <Navigate to={redirectTo} />;
};

export default AuthRoute;
