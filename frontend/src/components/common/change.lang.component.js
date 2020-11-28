import React, { Component } from "react";
import PropTypes from "prop-types";
import { withStyles } from "@material-ui/core/styles";
import FormControl from "@material-ui/core/FormControl";
import InputLabel from "@material-ui/core/InputLabel";
import Select from "@material-ui/core/Select";
import { connect } from "react-redux";
import MenuItem from "@material-ui/core/MenuItem";
import { changeLanguage } from "../../actions/common";
import { Trans } from "react-i18next";

const useStyles = (theme) => ({
  formControl: {
    margin: theme.spacing(1),
    minWidth: 120,
  },
  selectEmpty: {
    marginTop: theme.spacing(2),
  },
});

class ChangeLanguageComponent extends Component {
  constructor(props) {
    super(props);
    this.state = {
      lang: this.props.lang,
    };
    this.handleChange.bind(this);
  }

  handleChange = (event) => {
    const newLang = event.target.value;
    const { dispatch } = this.props;
    dispatch(changeLanguage(newLang));
    this.setState({
      lang: newLang,
    });
  };

  render() {
    const { classes } = this.props;
    console.log(this.props);
    return (
      <FormControl className={classes.formControl}>
        <InputLabel id="lang-select-label">
          <Trans>Language</Trans>
        </InputLabel>
        <Select
          labelId="lang-select-label"
          id="lang-select"
          value={this.state.lang}
          onChange={this.handleChange}
        >
          <MenuItem value="en-US">
            <Trans>English</Trans>
          </MenuItem>
          <MenuItem value="ru-RU">
            <Trans>Russian</Trans>
          </MenuItem>
          <MenuItem value="uk-UA">
            <Trans>Ukrainian</Trans>
          </MenuItem>
        </Select>
      </FormControl>
    );
  }
}

ChangeLanguageComponent.propTypes = {
  classes: PropTypes.object.isRequired,
};

function mapStateToProps(state) {
  const { lang } = state.common;
  return {
    lang,
  };
}

const styledComponent = withStyles(useStyles)(ChangeLanguageComponent);

export default connect(mapStateToProps)(styledComponent);
