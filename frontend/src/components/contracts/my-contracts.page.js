import React, { Component } from "react";
import Button from "@material-ui/core/Button";
import history from "../../helpers/history";
import { Trans, withNamespaces } from "react-i18next";
import { getPersonalCompanyPrices } from "../../actions/company";
import { connect } from "react-redux";
import Grid from "@material-ui/core/Grid";
import Card from "@material-ui/core/Card";
import CardActionArea from "@material-ui/core/CardActionArea";
import CardMedia from "@material-ui/core/CardMedia";
import CardContent from "@material-ui/core/CardContent";
import Typography from "@material-ui/core/Typography";
import CardActions from "@material-ui/core/CardActions";
import ReceiptIcon from "@material-ui/icons/Receipt";
import { withStyles } from "@material-ui/core/styles";
import DialogTitle from "@material-ui/core/DialogTitle";
import DialogContent from "@material-ui/core/DialogContent";
import DialogContentText from "@material-ui/core/DialogContentText";
import TextField from "@material-ui/core/TextField";
import DialogActions from "@material-ui/core/DialogActions";
import Dialog from "@material-ui/core/Dialog";
import ContractServices from "./../../services/contract.services";
import DeleteIcon from "@material-ui/icons/Delete";
import {
  deleteContract,
  getContracts,
  getContractsWithCompanies,
} from "../../actions/contracts";

const useStyles = (theme) => ({
  root: {
    flexGrow: 1,
  },
  paper: {
    padding: theme.spacing(2),
    textAlign: "center",
    color: theme.palette.text.secondary,
  },
});

class MyContractsPage extends Component {
  constructor(props) {
    super(props);
    this.state = { dialogIsOpen: false, contractID: undefined };
  }

  componentDidMount() {
    const { dispatch } = this.props;
    dispatch(getContractsWithCompanies());
    console.log(this.props);
  }

  handleOpenDeleteContractDialog = (id) => {
    this.setState({
      dialogIsOpen: true,
      contractID: id,
    });
  };

  handleClose = () => {
    this.setState({ dialogIsOpen: false });
  };

  deleteContract = () => {
    const { dispatch } = this.props;
    dispatch(deleteContract(this.state.contractID)).then(() =>
      this.handleClose()
    );
  };

  handleChangeMonths = (event) => {
    const target = event.target;
    if (target.value < 3 || target.value > 12) return;
    this.setState({
      [target.name]: target.value,
    });
  };

  transformCompaniesToDict = () => {
    let companies = {};
    this.props.company.companies.forEach((item) => (companies[item.id] = item));
    return companies;
  };

  render() {
    const { classes, t } = this.props;
    const companies = this.transformCompaniesToDict();
    return (
      <div className={classes.root}>
        {this.state.dialogIsOpen && (
          <Dialog
            open={this.state.dialogIsOpen}
            onClose={this.handleClose}
            aria-labelledby="alert-dialog-title"
            aria-describedby="alert-dialog-description"
          >
            <DialogTitle id="alert-dialog-title">
              {t("Delete the contract?")}
            </DialogTitle>
            <DialogContent>
              <DialogContentText id="alert-dialog-description">
                <Trans>Are you sure you want to delete?</Trans>
              </DialogContentText>
            </DialogContent>
            <DialogActions>
              <Button onClick={this.handleClose} color="primary">
                <Trans>Cancel</Trans>
              </Button>
              <Button onClick={this.deleteContract} color="primary" autoFocus>
                <Trans>Delete</Trans>
              </Button>
            </DialogActions>
          </Dialog>
        )}
        <Grid container spacing={3}>
          {this.props.contract.contracts.map((contract) => (
            <Grid item xs={12} sm={6} md={4}>
              <Card className={classes.root}>
                <CardActionArea>
                  <CardMedia
                    component="img"
                    alt="Contemplative Reptile"
                    height="140"
                    image={companies[contract.company].logo}
                    title="Contemplative Reptile"
                  />
                  <CardContent>
                    <Typography gutterBottom variant="h4" component="h2">
                      {companies[contract.company].name}
                    </Typography>
                    <Typography variant="body2" color="primary" component="p">
                      <Trans>Personal coefficient</Trans>:{" "}
                      {contract.personal_coefficient}
                    </Typography>
                    <Typography variant="body2" color="primary" component="p">
                      <Trans>Term date</Trans>:{" "}
                      {new Date(contract.end_date).toLocaleString()}
                    </Typography>
                    <Typography variant="body2" color="primary" component="p">
                      <Trans>Start date</Trans>:{" "}
                      {new Date(contract.created).toLocaleString()}
                    </Typography>
                    <Typography variant="body2" color="primary" component="p">
                      <Trans>Personal price</Trans>:{" "}
                      {companies[contract.company].own_price}
                    </Typography>
                    <Typography
                      variant="body2"
                      color="textSecondary"
                      component="p"
                    >
                      <Trans>Speed discount</Trans>:{" "}
                      {companies[contract.company].own_speed_discount}
                    </Typography>
                    <Typography
                      variant="body2"
                      color="textSecondary"
                      component="p"
                    >
                      <Trans>Head rotate discount</Trans>:{" "}
                      {companies[contract.company].own_head_rotate_discount}
                    </Typography>
                    <Typography
                      variant="body2"
                      color="textSecondary"
                      component="p"
                    >
                      <Trans>Base price</Trans>:{" "}
                      {companies[contract.company].base_price}
                    </Typography>
                    <Typography
                      variant="body2"
                      color="textSecondary"
                      component="p"
                    >
                      <Trans>Min price</Trans>:{" "}
                      {companies[contract.company].min_price}
                    </Typography>
                    <Typography
                      variant="body2"
                      color="textSecondary"
                      component="p"
                    >
                      <Trans>Max price</Trans>:{" "}
                      {companies[contract.company].max_price}
                    </Typography>
                  </CardContent>
                </CardActionArea>
                <CardActions>
                  <Button
                    variant="contained"
                    color="secondary"
                    className={classes.button}
                    startIcon={<DeleteIcon />}
                    onClick={() =>
                      this.handleOpenDeleteContractDialog(contract.id)
                    }
                  >
                    <Trans>Delete</Trans>
                  </Button>
                </CardActions>
              </Card>
            </Grid>
          ))}
        </Grid>
      </div>
    );
  }
}

const mapStateToProps = (state) => {
  const { company, contract } = state;
  return { company, contract };
};

export default connect(mapStateToProps)(
  withStyles(useStyles)(withNamespaces()(MyContractsPage))
);
