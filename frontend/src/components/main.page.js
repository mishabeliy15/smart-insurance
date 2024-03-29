import { Trans, withNamespaces } from "react-i18next";
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
// import DashboardIcon from "@material-ui/icons/Dashboard";
import withTheme from "@material-ui/core/styles/withTheme";
import { Redirect, Router, Switch } from "react-router";
import { Link, Route } from "react-router-dom";
import { default as HrefLink } from "@material-ui/core/Link";
import history from "../helpers/history";
import useStyles from "./main.page.style";
import BuildIcon from "@material-ui/icons/Build";
import SensorPage from "./sensor/sensors.page";
import AddSensorPage from "./sensor/add-sensor-page";
import CreateCompanyPage from "./companies/create-company.page";
import AddIcon from "@material-ui/icons/Add";
import AccountBalanceIcon from "@material-ui/icons/AccountBalance";
import MyCompaniesPage from "./companies/my-companies.page";
import EditCompanyPage from "./companies/edit-company.page";
import BestCompanyPricePage from "./companies/best-company-price.page";
import EmojiTransportationIcon from "@material-ui/icons/EmojiTransportation";
import MyContractsPage from "./contracts/my-contracts.page";
import DescriptionIcon from "@material-ui/icons/Description";

const userTypeNavigationListItem = {
  1: [
    // { name: "Dashboard", icon: <DashboardIcon />, url: "/" },
    { name: "Sensors", icon: <BuildIcon />, url: "/sensors" },
    {
      name: "Find best company",
      icon: <EmojiTransportationIcon />,
      url: "/best-price",
    },
    {
      name: "My contracts",
      icon: <DescriptionIcon />,
      url: "/contracts",
    },
  ],
  2: [
    {
      name: "My companies",
      icon: <AccountBalanceIcon />,
      url: "/companies",
    },
    {
      name: "Add company",
      icon: <AddIcon />,
      url: "/companies/add",
    },
  ],
};

const userTypeSwitchRoutes = {
  1: (
    <Switch>
      <Route exact path="/">
        <Redirect to="/best-price" />
      </Route>
      <Route exact path="/sensors">
        <SensorPage />
      </Route>
      <Route exact path="/sensors/add">
        <AddSensorPage />
      </Route>
      <Route exact path="/best-price">
        <BestCompanyPricePage />
      </Route>
      <Route exact path="/contracts">
        <MyContractsPage />
      </Route>
    </Switch>
  ),
  2: (
    <Switch>
      <Route exact path="/">
        <Redirect to="/companies" />
      </Route>
      <Route exact path="/companies">
        <MyCompaniesPage />
      </Route>
      <Route exact path="/companies/add">
        <CreateCompanyPage />
      </Route>
      <Route path="/companies/:id" component={EditCompanyPage} />
    </Switch>
  ),
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
    const pathname = history.location.pathname;

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
            <HrefLink href="/admin/" color="inherit" className="MuiLink-button">
              <Trans>Admin panel</Trans>
            </HrefLink>
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
              <ListItem
                selected={item.url === pathname}
                button
                key={item.name}
                component={Link}
                to={item.url}
              >
                <ListItemIcon>{item.icon}</ListItemIcon>
                <ListItemText primary={t(item.name)} />
              </ListItem>
            ))}
          </List>
        </Drawer>
        <main className={classes.content}>
          <div className={classes.toolbar} />
          <Router history={history}>{userTypeSwitchRoutes[userType]}</Router>
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
