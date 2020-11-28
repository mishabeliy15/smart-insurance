import React, { Component } from "react";
import Button from "@material-ui/core/Button";
import { Trans } from "react-i18next";
import { logout } from "../../actions/auth";
import { connect } from "react-redux";

class LogOutComponent extends Component {
  onClickHandler = (event) => {
    const { dispatch, history } = this.props;
    dispatch(logout());
    history.push("/login");
  };

  render() {
    return (
      <Button onClick={this.onClickHandler}>
        <Trans>Log out</Trans>
      </Button>
    );
  }
}

export default connect()(LogOutComponent);
