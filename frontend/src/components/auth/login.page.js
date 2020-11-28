import React, { Component } from "react";
import Avatar from "@material-ui/core/Avatar";
import Button from "@material-ui/core/Button";
import CssBaseline from "@material-ui/core/CssBaseline";
import TextField from "@material-ui/core/TextField";
import Paper from "@material-ui/core/Paper";
import Box from "@material-ui/core/Box";
import Grid from "@material-ui/core/Grid";
import LockOutlinedIcon from "@material-ui/icons/LockOutlined";
import Typography from "@material-ui/core/Typography";
import PropTypes from "prop-types";
import { withStyles } from "@material-ui/core/styles";
import { connect } from "react-redux";
import { Link } from "react-router-dom";
import { login } from "../../actions/auth";
import Alert from "react-bootstrap/Alert";
import CopyrightComponent from "./copyright.component";
import styles from "./style";
import { Trans, withNamespaces } from "react-i18next";
import ChangeLanguageComponent from "../common/change.lang.component";

class LoginPage extends Component {
  constructor(props) {
    super(props);
    this.state = { username: "", password: "" };
    this.handleInputChange = this.handleInputChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleInputChange(event) {
    const target = event.target;
    const value = target.value;
    const name = target.name;

    this.setState({
      [name]: value,
    });
  }

  handleSubmit(event) {
    event.preventDefault();
    const { dispatch, history } = this.props;
    dispatch(login(this.state.username, this.state.password)).then(() => {
      history.push("/");
      //window.location.reload();
    });
  }

  render() {
    const { classes, message, t } = this.props;
    return (
      <div>
        <Grid container component="main" className={classes.root}>
          <CssBaseline />
          <Grid item xs={false} sm={4} md={7} className={classes.image} />
          <Grid
            item
            xs={12}
            sm={8}
            md={5}
            component={Paper}
            elevation={6}
            square
          >
            <div className={classes.paper}>
              <Avatar className={classes.avatar}>
                <LockOutlinedIcon />
              </Avatar>
              <Typography component="h1" variant="h5">
                <Trans>Sign in</Trans>
              </Typography>
              <form className={classes.form} onSubmit={this.handleSubmit}>
                <TextField
                  value={this.state.username}
                  onChange={this.handleInputChange}
                  variant="outlined"
                  margin="normal"
                  required
                  fullWidth
                  id="username"
                  label={t("Username")}
                  name="username"
                  autoComplete={t("Username")}
                  autoFocus
                />
                <TextField
                  value={this.state.password}
                  onChange={this.handleInputChange}
                  variant="outlined"
                  margin="normal"
                  required
                  fullWidth
                  name="password"
                  label={t("Password")}
                  type="password"
                  id="password"
                  autoComplete={t("Password")}
                />
                {/*<FormControlLabel*/}
                {/*  control={<Checkbox value="remember" color="primary" />}*/}
                {/*  label="Remember me"*/}
                {/*/>*/}
                {message && (
                  <Alert key="error" variant="danger">
                    <Trans>{message}</Trans>
                  </Alert>
                )}
                <Grid item xs={12} sm={6}>
                  <ChangeLanguageComponent />
                </Grid>
                <Button
                  type="submit"
                  fullWidth
                  variant="contained"
                  color="primary"
                  className={classes.submit}
                >
                  <Trans>Sign in</Trans>
                </Button>
                <Grid container>
                  <Grid item>
                    <Link to="/register" variant="body2">
                      <Trans>Don't have an account?</Trans>
                      <Trans>Sign up</Trans>
                    </Link>
                  </Grid>
                </Grid>
                <Box mt={5}>
                  <CopyrightComponent />
                </Box>
              </form>
            </div>
          </Grid>
        </Grid>
      </div>
    );
  }
}

LoginPage.propTypes = {
  classes: PropTypes.object.isRequired,
};

function mapStateToProps(state) {
  const { isLoggedIn } = state.auth;
  const { message } = state.message;
  return {
    isLoggedIn,
    message,
  };
}

const styledComponent = withNamespaces()(withStyles(styles)(LoginPage));

export default connect(mapStateToProps)(styledComponent);
