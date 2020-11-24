import "./App.css";
import { connect } from "react-redux";
import React, { Component } from "react";
import { Route, Router, Switch } from "react-router";
import history from "./helpers/history";
import LoginPage from "./components/auth/login.page";
import RegisterPage from "./components/auth/register.page";

class App extends Component {
  render() {
    return (
      <Router history={history}>
        <Switch>
          <Route path="/login" component={LoginPage} />
          <Route path="/register" component={RegisterPage} />
        </Switch>
      </Router>
    );
  }
}

function mapStateToProps(state) {
  const { user } = state.auth;
  return {
    user,
  };
}

export default connect(mapStateToProps)(App);
