import React, { Component } from "react";
import TextField from "@material-ui/core/TextField";
import { connect } from "react-redux";
import { Trans, withNamespaces } from "react-i18next";
import { withStyles } from "@material-ui/core/styles";
import PropTypes from "prop-types";
import Button from "@material-ui/core/Button";
import InputLabel from "@material-ui/core/InputLabel";
import Select from "@material-ui/core/Select";
import MenuItem from "@material-ui/core/MenuItem";
import FormControl from "@material-ui/core/FormControl";
import { addSensor } from "../../actions/sensor";
import history from "../../helpers/history";

const validate = require("uuid-validate");

const useStyles = (theme) => ({
  root: {
    "& .MuiTextField-root": {
      margin: theme.spacing(1),
      width: "50%",
    },
  },
});

class AddSensorPage extends Component {
  constructor(props) {
    super(props);
    this.state = {
      uuid: "",
      sensor_type: 1,
      errorUUID: false,
    };
  }

  handleInputChange = (event) => {
    const target = event.target;

    this.setState({
      [target.name]: target.value,
    });
  };

  handleUUIDChange = (event) => {
    const isValid = validate(event.target.value, 4);
    this.setState({
      errorUUID: !isValid,
    });
    this.handleInputChange(event);
  };

  handleSubmit = (event) => {
    event.preventDefault();
    const { dispatch } = this.props;
    dispatch(addSensor(this.state.uuid, this.state.sensor_type))
      .then(() => {
        history.push("/sensors");
      })
      .catch(() => this.setState({ errorUUID: true }));
  };

  formatMessage = (message) => {
    let result = "";
    for (let key in message) {
      result += `${key}: ${message[key].join(".")}\n`;
    }
    return result;
  };

  render() {
    const { classes, message, t } = this.props;

    return (
      <form className={classes.root} onSubmit={this.handleSubmit}>
        <div>
          <TextField
            id="sensor-uuid"
            name="uuid"
            variant="outlined"
            margin="normal"
            required
            error={this.state.errorUUID}
            value={this.state.uuid}
            onChange={this.handleUUIDChange}
            label="UUID"
            autoComplete={t("UUID")}
            autoFocus
            helperText={message && this.formatMessage(message)}
          />
        </div>
        <FormControl className={classes.formControl}>
          <InputLabel id="sensor-type-select-label">
            <Trans>Sensor type</Trans>
          </InputLabel>
          <Select
            labelId="sensor-type-select-label"
            id="sensor_type"
            name="sensor_type"
            value={this.state.sensor_type}
            onChange={this.handleInputChange}
            style={{ margin: "20px" }}
          >
            <MenuItem value={1}>
              <Trans>Movement</Trans>
            </MenuItem>
            <MenuItem value={2}>
              <Trans>Camera</Trans>
            </MenuItem>
          </Select>
        </FormControl>
        <div style={{ width: "50%" }}>
          <Button
            type="submit"
            fullWidth
            variant="contained"
            color="primary"
            className={classes.submit}
            disabled={this.state.errorUUID}
          >
            <Trans>Add</Trans> <Trans>sensor</Trans>
          </Button>
        </div>
      </form>
    );
  }
}

AddSensorPage.propTypes = {
  classes: PropTypes.object.isRequired,
};

const mapStateToProps = (state) => {
  const { message } = state.message;
  const { isLoading } = state.sensors;
  return {
    message,
    isLoading,
  };
};

export default connect(mapStateToProps)(
  withStyles(useStyles)(withNamespaces()(AddSensorPage))
);
