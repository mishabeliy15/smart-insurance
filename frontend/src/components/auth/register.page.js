import React, { Component } from "react";
import Avatar from "@material-ui/core/Avatar";
import Button from "@material-ui/core/Button";
import CssBaseline from "@material-ui/core/CssBaseline";
import TextField from "@material-ui/core/TextField";
import Grid from "@material-ui/core/Grid";
import LockOutlinedIcon from "@material-ui/icons/LockOutlined";
import Typography from "@material-ui/core/Typography";
import PropTypes from "prop-types";
import { withStyles } from "@material-ui/core/styles";
import { connect } from "react-redux";
import Paper from "@material-ui/core/Paper";
import useStyles from "./style";
import { Link } from "react-router-dom";
import CopyrightComponent from "./copyright.component";
import Box from "@material-ui/core/Box";
import { Trans, withNamespaces } from "react-i18next";
import Select from "@material-ui/core/Select";
import MenuItem from "@material-ui/core/MenuItem";
import Alert from "react-bootstrap/Alert";
import { login, register } from "../../actions/auth";
import ChangeLanguageComponent from "../common/change.lang.component";
import InputLabel from "@material-ui/core/InputLabel";
import FormControl from "@material-ui/core/FormControl";
import { CLEAR_MESSAGE } from "../../actions/types";

class RegisterPage extends Component {
  constructor(props) {
    super(props);
    this.state = {
      username: "",
      password: "",
      first_name: "",
      last_name: "",
      user_type: 1,
    };
    this.handleInputChange = this.handleInputChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
    const { dispatch } = this.props;
    dispatch({ type: CLEAR_MESSAGE });
  }

  handleInputChange(event) {
    console.log(event);
    const target = event.target;

    this.setState({
      [target.name]: target.value,
    });
  }

  handleSubmit(event) {
    event.preventDefault();
    console.log(this.state);
    const { dispatch, history } = this.props;
    dispatch(register(this.state)).then((temp) => {
      console.log(temp);
      dispatch(login(this.state.username, this.state.password)).then(() =>
        history.push("/")
      );
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
                <Trans>Sign up</Trans>
              </Typography>
              <form className={classes.form} onSubmit={this.handleSubmit}>
                <Grid container spacing={2}>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      onChange={this.handleInputChange}
                      autoComplete="fname"
                      name="first_name"
                      variant="outlined"
                      required
                      fullWidth
                      id="firstName"
                      label={t("First Name")}
                      autoFocus
                    />
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      onChange={this.handleInputChange}
                      variant="outlined"
                      required
                      fullWidth
                      id="lastName"
                      label={t("Last Name")}
                      name="last_name"
                      autoComplete="lname"
                    />
                  </Grid>
                  <Grid item xs={12}>
                    <TextField
                      onChange={this.handleInputChange}
                      variant="outlined"
                      required
                      fullWidth
                      id="username"
                      label={t("Username")}
                      name="username"
                      autoComplete="username"
                    />
                  </Grid>
                  <Grid item xs={12}>
                    <TextField
                      onChange={this.handleInputChange}
                      variant="outlined"
                      required
                      fullWidth
                      name="password"
                      label={t("Password")}
                      type="password"
                      id="password"
                      autoComplete="current-password"
                    />
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <FormControl className={classes.formControl}>
                      <InputLabel id="user-type-select-label">
                        <Trans>User type</Trans>
                      </InputLabel>
                      <Select
                        labelId="user-type-select-label"
                        id="user_type"
                        name="user_type"
                        value={this.state.user_type}
                        onChange={this.handleInputChange}
                      >
                        <MenuItem value={1}>
                          <Trans>Driver</Trans>
                        </MenuItem>
                        <MenuItem value={2}>
                          <Trans>Business</Trans>
                        </MenuItem>
                      </Select>
                    </FormControl>
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <ChangeLanguageComponent />
                  </Grid>
                </Grid>
                {message && (
                  <Alert key="error" variant="danger">
                    {t(message.trim())}
                  </Alert>
                )}
                <Button
                  type="submit"
                  fullWidth
                  variant="contained"
                  color="primary"
                  className={classes.submit}
                >
                  <Trans>Sign up</Trans>
                </Button>
                <Grid container justify="flex-end">
                  <Grid item>
                    <Link to="/login" variant="body2">
                      <Trans>Already have an account?</Trans>
                      <Trans>Sign in</Trans>
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

RegisterPage.propTypes = {
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

const styledComponent = withNamespaces()(withStyles(useStyles)(RegisterPage));

export default connect(mapStateToProps)(styledComponent);
