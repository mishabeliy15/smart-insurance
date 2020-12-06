import React, { Component } from "react";
import { connect } from "react-redux";
import { Trans, withNamespaces } from "react-i18next";
import Grid from "@material-ui/core/Grid";
import { withStyles } from "@material-ui/core/styles";
import ImageUploader from "react-images-upload";
import TextField from "@material-ui/core/TextField";
import Button from "@material-ui/core/Button";
import Alert from "react-bootstrap/Alert";
import { createCompany, editCompany, getCompany } from "../../actions/company";
import SaveIcon from "@material-ui/icons/Save";

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

class EditCompanyPage extends Component {
  constructor(props) {
    super(props);
    this.state = {};
  }

  componentDidMount() {
    const id = this.props.match.params.id;
    const { dispatch } = this.props;
    dispatch(getCompany(id)).then((data) => {
      delete data.logo;
      this.setState(data);
    });
  }

  onDrop = (pictureFiles, pictureDataURLs) => {
    this.setState({
      logo: pictureFiles[0],
    });
  };

  handleInputChange = (event) => {
    const target = event.target;

    this.setState({
      [target.name]: target.value,
    });
  };

  handleOnSubmit = (event) => {
    event.preventDefault();
    const { dispatch } = this.props;
    dispatch(editCompany(this.state.id, this.state)).then((data) =>
      this.setState(data)
    );
  };

  render() {
    const { classes, t } = this.props;
    return (
      <div className={classes.root}>
        <form onSubmit={this.handleOnSubmit}>
          <Grid container spacing={3}>
            <Grid item xs={4}>
              <ImageUploader
                withIcon={true}
                required={true}
                withPreview={true}
                singleImage={true}
                name="logo"
                buttonText={t("Choose logo")}
                onChange={this.onDrop}
                imgExtension={[".jpg", ".png"]}
                maxFileSize={5242880}
              />
            </Grid>
            <Grid item xs={8}>
              <TextField
                required
                id="company-name"
                label={t("Name")}
                value={this.state.name}
                onChange={this.handleInputChange}
                name="name"
                fullWidth={true}
                autoComplete={t("Company name")}
                helperText={this.props.message && this.props.message.name}
                error={this.props.message && this.props.message.name}
              />
            </Grid>
            <Grid item xs={4}>
              <TextField
                required
                id="company-min_price"
                fullWidth={true}
                label={t("Min price")}
                onChange={this.handleInputChange}
                value={this.state.min_price}
                name="min_price"
                type="number"
                autoComplete={t("Min price")}
                helperText={this.props.message && this.props.message.min_price}
                error={this.props.message && this.props.message.min_price}
              />
            </Grid>
            <Grid item xs={4}>
              <TextField
                required
                fullWidth={true}
                id="company-base_price"
                label={t("Base price")}
                value={this.state.base_price}
                onChange={this.handleInputChange}
                name="base_price"
                type="number"
                autoComplete={t("Base price")}
                helperText={this.props.message && this.props.message.base_price}
                error={this.props.message && this.props.message.base_price}
              />
            </Grid>
            <Grid item xs={4}>
              <TextField
                required
                fullWidth={true}
                id="company-max_price"
                label={t("Max price")}
                onChange={this.handleInputChange}
                value={this.state.max_price}
                name="max_price"
                type="number"
                autoComplete={t("Max price")}
                helperText={this.props.message && this.props.message.max_price}
                error={this.props.message && this.props.message.max_price}
              />
            </Grid>
            <Grid item xs={3}>
              <TextField
                required
                fullWidth={true}
                id="percent_over_speeding"
                label={t("Percent over speeding")}
                onChange={this.handleInputChange}
                value={this.state.percent_over_speeding}
                name="percent_over_speeding"
                type="number"
                autoComplete={t("Percent over speeding")}
                placeholder={t("Percent over speeding")}
                helperText={
                  this.props.message && this.props.message.percent_over_speeding
                }
                error={
                  this.props.message && this.props.message.percent_over_speeding
                }
              />
            </Grid>
            <Grid item xs={3}>
              <TextField
                fullWidth={true}
                required
                id="min_speed_commit_rotate_head"
                label={t("Min speed to commit rotate head")}
                onChange={this.handleInputChange}
                value={this.state.min_speed_commit_rotate_head}
                name="min_speed_commit_rotate_head"
                type="number"
                autoComplete={t("Min speed to commit rotate head")}
                placeholder={t("Min speed to commit rotate head")}
                helperText={
                  this.props.message &&
                  this.props.message.min_speed_commit_rotate_head
                }
                error={
                  this.props.message &&
                  this.props.message.min_speed_commit_rotate_head
                }
              />
            </Grid>
            <Grid item xs={3}>
              <TextField
                fullWidth={true}
                required
                id="min_angle_commit_rotate_head"
                label={t("Min angle to commit rotate head")}
                onChange={this.handleInputChange}
                value={this.state.min_angle_commit_rotate_head}
                name="min_angle_commit_rotate_head"
                type="number"
                autoComplete={t("Min angle to commit rotate head")}
                placeholder={t("Min angle to commit rotate head")}
                helperText={
                  this.props.message &&
                  this.props.message.min_angle_commit_rotate_head
                }
                error={
                  this.props.message &&
                  this.props.message.min_angle_commit_rotate_head
                }
              />
            </Grid>
            <Grid item xs={3}>
              <TextField
                required
                fullWidth={true}
                id="percent_head_rotate_for_hour"
                label={t("Percent head rotate for hour")}
                onChange={this.handleInputChange}
                value={this.state.percent_head_rotate_for_hour}
                name="percent_head_rotate_for_hour"
                type="number"
                autoComplete={t("Percent head rotate for hour")}
                placeholder={t("Percent head rotate for hour")}
                helperText={
                  this.props.message &&
                  this.props.message.percent_head_rotate_for_hour
                }
                error={
                  this.props.message &&
                  this.props.message.percent_head_rotate_for_hour
                }
              />
            </Grid>
            <Grid item xs={6}>
              <TextField
                required
                fullWidth={true}
                id="max_speed_discount"
                label={t("Max speed discount")}
                onChange={this.handleInputChange}
                value={this.state.max_speed_discount}
                name="max_speed_discount"
                type="number"
                autoComplete={t("Max speed discount")}
                placeholder={t("Max speed discount")}
                helperText={
                  this.props.message && this.props.message.max_speed_discount
                }
                error={
                  this.props.message && this.props.message.max_speed_discount
                }
              />
            </Grid>
            <Grid item xs={6}>
              <TextField
                required
                fullWidth={true}
                id="max_speed_penalty"
                label={t("Max speed penalty")}
                onChange={this.handleInputChange}
                value={this.state.max_speed_penalty}
                name="max_speed_penalty"
                type="number"
                autoComplete={t("Max speed penalty")}
                placeholder={t("Max speed penalty")}
                helperText={
                  this.props.message && this.props.message.max_speed_penalty
                }
                error={
                  this.props.message && this.props.message.max_speed_penalty
                }
              />
            </Grid>
            <Grid item xs={6}>
              <TextField
                required
                fullWidth={true}
                id="max_rotate_head_discount"
                label={t("Max rotate discount")}
                onChange={this.handleInputChange}
                value={this.state.max_rotate_head_discount}
                name="max_rotate_head_discount"
                type="number"
                autoComplete={t("Max rotate discount")}
                placeholder={t("Max rotate discount")}
                helperText={
                  this.props.message &&
                  this.props.message.max_rotate_head_discount
                }
                error={
                  this.props.message &&
                  this.props.message.max_rotate_head_discount
                }
              />
            </Grid>
            <Grid item xs={6}>
              <TextField
                required
                fullWidth={true}
                id="max_rotate_head_penalty"
                label={t("Max rotate head penalty")}
                onChange={this.handleInputChange}
                value={this.state.max_rotate_head_penalty}
                name="max_rotate_head_penalty"
                type="number"
                autoComplete={t("Max rotate head penalty")}
                placeholder={t("Max rotate head penalty")}
                helperText={
                  this.props.message &&
                  this.props.message.max_rotate_head_penalty
                }
                error={
                  this.props.message &&
                  this.props.message.max_rotate_head_penalty
                }
              />
            </Grid>
            {this.props.message && this.props.message.non_field_errors && (
              <Grid item xs={12}>
                <Alert key="error" variant="danger">
                  {this.props.message.non_field_errors.join("\n")}
                </Alert>
              </Grid>
            )}
            <Grid item xs={4}>
              <Button
                type="submit"
                fullWidth
                variant="contained"
                startIcon={<SaveIcon />}
                color="primary"
                className={classes.submit}
              >
                <Trans>Save</Trans>
              </Button>
            </Grid>
          </Grid>
        </form>
      </div>
    );
  }
}

const mapStateToProps = (state) => {
  const { message } = state.message;
  return {
    message,
  };
};

export default connect(mapStateToProps)(
  withStyles(useStyles)(withNamespaces()(EditCompanyPage))
);
