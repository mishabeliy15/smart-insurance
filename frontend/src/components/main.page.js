import { withNamespaces } from "react-i18next";
import { withStyles } from "@material-ui/core/styles";
import { connect } from "react-redux";
import LogOutComponent from "./auth/logout.component";
import ChangeLanguageComponent from "./common/change.lang.component";
import React, { Component } from "react";
import clsx from "clsx";
import Drawer from "@material-ui/core/Drawer";
import AppBar from "@material-ui/core/AppBar";
import Toolbar from "@material-ui/core/Toolbar";
import List from "@material-ui/core/List";
import CssBaseline from "@material-ui/core/CssBaseline";
import Divider from "@material-ui/core/Divider";
import IconButton from "@material-ui/core/IconButton";
import MenuIcon from "@material-ui/icons/Menu";
import ChevronLeftIcon from "@material-ui/icons/ChevronLeft";
import ChevronRightIcon from "@material-ui/icons/ChevronRight";
import ListItem from "@material-ui/core/ListItem";
import ListItemIcon from "@material-ui/core/ListItemIcon";
import ListItemText from "@material-ui/core/ListItemText";
import DashboardIcon from "@material-ui/icons/Dashboard";
import withTheme from "@material-ui/core/styles/withTheme";
import { Router, Switch } from "react-router";
import { Link, Route } from "react-router-dom";
import history from "../helpers/history";
import useStyles from "./main.page.style";
import BuildIcon from "@material-ui/icons/Build";
import SensorComponent from "./sensor/sensors.page";

const userTypeNavigationListItem = {
  1: [
    { name: "Dashboard", icon: <DashboardIcon />, url: "/" },
    { name: "Sensors", icon: <BuildIcon />, url: "/sensors" },
  ],
};

class MainComponent extends Component {
  constructor(props) {
    super(props);
    this.state = { isOpen: false };
  }

  handleDrawerOpen = () => {
    this.setState({ isOpen: true });
  };

  handleDrawerClose = () => {
    this.setState({ isOpen: false });
  };

  render() {
    const { classes, theme, t } = this.props;
    const userType = this.props.user.user_type;
    const navigationItems = userTypeNavigationListItem[userType];

    return (
      <div className={classes.root}>
        <CssBaseline />
        <AppBar
          position="fixed"
          className={clsx(classes.appBar, {
            [classes.appBarShift]: this.state.isOpen,
          })}
        >
          <Toolbar>
            <IconButton
              color="inherit"
              aria-label="open drawer"
              onClick={this.handleDrawerOpen}
              edge="start"
              className={clsx(classes.menuButton, {
                [classes.hide]: this.state.isOpen,
              })}
            >
              <MenuIcon />
            </IconButton>
            <ChangeLanguageComponent />
            <LogOutComponent color="inherit" className={classes.panelButton} />
          </Toolbar>
        </AppBar>
        <Drawer
          variant="permanent"
          className={clsx(classes.drawer, {
            [classes.drawerOpen]: this.state.isOpen,
            [classes.drawerClose]: !this.state.isOpen,
          })}
          classes={{
            paper: clsx({
              [classes.drawerOpen]: this.state.isOpen,
              [classes.drawerClose]: !this.state.isOpen,
            }),
          }}
        >
          <div className={classes.toolbar}>
            <IconButton onClick={this.handleDrawerClose}>
              {theme.direction === "rtl" ? (
                <ChevronRightIcon />
              ) : (
                <ChevronLeftIcon />
              )}
            </IconButton>
          </div>
          <Divider />
          <List>
            {navigationItems.map((item) => (
              <ListItem button key={item.name} component={Link} to={item.url}>
                <ListItemIcon>{item.icon}</ListItemIcon>
                <ListItemText primary={t(item.name)} />
              </ListItem>
            ))}
          </List>
        </Drawer>
        <main className={classes.content}>
          <div className={classes.toolbar} />
          <Router history={history}>
            <Switch>
              <Route exact path="/">
                Dashboard
              </Route>
              <Route exact path="/sensors">
                <SensorComponent />
              </Route>
            </Switch>
          </Router>
        </main>
      </div>
    );
  }
}

const mapStateToProps = (state) => {
  const { user } = state.auth;
  return { user };
};

const styledComponent = withNamespaces()(
  withTheme(withStyles(useStyles)(MainComponent))
);

export default connect(mapStateToProps)(styledComponent);
