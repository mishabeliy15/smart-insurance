import React from "react";
import { Route, Redirect } from "react-router-dom";

const AnonymousRoute = ({ component: Component, authed, ...rest }) => (
  <Route
    {...rest}
    render={(props) =>
      authed ? <Redirect to="/" /> : <Component {...props} />
    }
  />
);

export default AnonymousRoute;
