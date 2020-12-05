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

class BestCompanyPricePage extends Component {
  constructor(props) {
    super(props);
    this.state = { dialogIsOpen: false, companyID: undefined, months: 3 };
  }

  componentDidMount() {
    const { dispatch } = this.props;
    dispatch(getPersonalCompanyPrices());
  }

  handleOpenSignContractDialog = (id) => {
    this.setState({
      dialogIsOpen: true,
      companyID: id,
    });
  };

  handleClose = () => {
    this.setState({ dialogIsOpen: false });
  };

  signContract = () => {
    ContractServices.createContract(
      this.state.companyID,
      this.state.months
    ).then(() => this.handleClose());
  };

  handleChangeMonths = (event) => {
    const target = event.target;
    if (target.value < 3 || target.value > 12) return;
    this.setState({
      [target.name]: target.value,
    });
  };

  render() {
    const { classes } = this.props;
    return (
      <div className={classes.root}>
        {this.state.dialogIsOpen && (
          <Dialog
            open={this.state.dialogIsOpen}
            onClose={this.handleClose}
            aria-labelledby="form-dialog-title"
          >
            <DialogTitle id="form-dialog-title">Subscribe</DialogTitle>
            <DialogContent>
              <DialogContentText>
                <Trans>To sign the contract, please enter month term</Trans>
              </DialogContentText>
              <TextField
                value={this.state.months}
                onChange={this.handleChangeMonths}
                autoFocus
                margin="dense"
                id="months"
                name="months"
                label="Duration (months)"
                type="number"
                fullWidth
              />
            </DialogContent>
            <DialogActions>
              <Button onClick={this.handleClose} color="primary">
                Cancel
              </Button>
              <Button onClick={this.signContract} color="primary">
                Sign a contract
              </Button>
            </DialogActions>
          </Dialog>
        )}
        <Grid container spacing={3}>
          {this.props.companies.map((item) => (
            <Grid item xs={12} sm={6} md={4}>
              <Card className={classes.root}>
                <CardActionArea>
                  <CardMedia
                    component="img"
                    alt="Contemplative Reptile"
                    height="140"
                    image={item.logo}
                    title="Contemplative Reptile"
                  />
                  <CardContent>
                    <Typography gutterBottom variant="h5" component="h2">
                      {item.name}
                    </Typography>
                    <Typography variant="body2" color="primary" component="p">
                      <Trans>Personal price</Trans>: {item.own_price}
                    </Typography>
                    <Typography
                      variant="body2"
                      color="textSecondary"
                      component="p"
                    >
                      <Trans>Speed discount</Trans>: {item.own_speed_discount}
                    </Typography>
                    <Typography
                      variant="body2"
                      color="textSecondary"
                      component="p"
                    >
                      <Trans>Head rotate discount</Trans>:{" "}
                      {item.own_head_rotate_discount}
                    </Typography>
                    <Typography
                      variant="body2"
                      color="textSecondary"
                      component="p"
                    >
                      <Trans>Base price</Trans>: {item.base_price}
                    </Typography>
                    <Typography
                      variant="body2"
                      color="textSecondary"
                      component="p"
                    >
                      <Trans>Min price</Trans>: {item.min_price}
                    </Typography>
                    <Typography
                      variant="body2"
                      color="textSecondary"
                      component="p"
                    >
                      <Trans>Max price</Trans>: {item.max_price}
                    </Typography>
                  </CardContent>
                </CardActionArea>
                <CardActions>
                  <Button
                    size="small"
                    variant="contained"
                    color="primary"
                    onClick={() => this.handleOpenSignContractDialog(item.id)}
                    startIcon={<ReceiptIcon />}
                  >
                    <Trans>Sign a contract</Trans>
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
  const { company } = state;
  return company;
};

export default connect(mapStateToProps)(
  withStyles(useStyles)(withNamespaces()(BestCompanyPricePage))
);
