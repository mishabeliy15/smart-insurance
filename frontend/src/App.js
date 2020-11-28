import "./App.css";
import { connect } from "react-redux";
import React, { Component } from "react";
import { Router, Switch } from "react-router";
import history from "./helpers/history";
import LoginPage from "./components/auth/login.page";
import RegisterPage from "./components/auth/register.page";
import AnonymousRoute from "./routers/anonymous.router";
import PrivateRoute from "./routers/private.router";
import MainComponent from "./components/main.page";

class App extends Component {
  render() {
    return (
      <Router history={history}>
        <Switch>
          <AnonymousRoute
            component={LoginPage}
            authed={this.props.isLoggedIn}
            exact
            path="/login"
          />
          <AnonymousRoute
            exact
            path="/register"
            component={RegisterPage}
            authed={this.props.isLoggedIn}
          />
          <PrivateRoute
            exact
            path="/"
            component={MainComponent}
            authed={this.props.isLoggedIn}
          />
        </Switch>
      </Router>
    );
  }
}

function mapStateToProps(state) {
  const { user, isLoggedIn } = state.auth;
  return {
    user,
    isLoggedIn,
  };
}

export default connect(mapStateToProps)(App);
