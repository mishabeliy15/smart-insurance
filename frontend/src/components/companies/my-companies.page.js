import React, { Component } from "react";
import { connect } from "react-redux";
import { Trans, withNamespaces } from "react-i18next";
import { withStyles } from "@material-ui/core/styles";
import { createCompany, getMyCompany } from "../../actions/company";
import history from "../../helpers/history";
import Card from "@material-ui/core/Card";
import CardActionArea from "@material-ui/core/CardActionArea";
import CardMedia from "@material-ui/core/CardMedia";
import CardContent from "@material-ui/core/CardContent";
import Typography from "@material-ui/core/Typography";
import CardActions from "@material-ui/core/CardActions";
import Button from "@material-ui/core/Button";
import Grid from "@material-ui/core/Grid";

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

class MyCompaniesPage extends Component {
  componentDidMount() {
    const { dispatch } = this.props;
    dispatch(getMyCompany());
  }

  render() {
    const { classes } = this.props;
    return (
      <div className={classes.root}>
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
                      <Trans>Base price</Trans>: {item.base_price}
                    </Typography>
                    <Typography
                      variant="body2"
                      color="textSecondary"
                      component="p"
                    >
                      <Trans>Max price</Trans>: {item.max_price}
                    </Typography>
                    <Typography
                      variant="body2"
                      color="textSecondary"
                      component="p"
                    >
                      <Trans>Updated</Trans>:{" "}
                      {new Date(item.updated).toLocaleString()}
                    </Typography>
                    <Typography
                      variant="body2"
                      color="textSecondary"
                      component="p"
                    >
                      <Trans>Created</Trans>:{" "}
                      {new Date(item.created).toLocaleString()}
                    </Typography>
                  </CardContent>
                </CardActionArea>
                <CardActions>
                  <Button size="small" color="primary">
                    Share
                  </Button>
                  <Button size="small" color="primary">
                    Learn More
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
  withStyles(useStyles)(withNamespaces()(MyCompaniesPage))
);
