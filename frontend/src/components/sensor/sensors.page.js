import React, { Component } from "react";

import { DataGrid } from "@material-ui/data-grid";
import { connect } from "react-redux";
import { getMySensors } from "../../actions/sensor";
import { Trans, withNamespaces } from "react-i18next";
import Button from "@material-ui/core/Button";
import history from "../../helpers/history";

class SensorComponent extends Component {
  componentDidMount() {
    const { dispatch } = this.props;
    dispatch(getMySensors());
  }

  getColumns() {
    const { t } = this.props;
    const transType = { 1: "Movement", 2: "Camera" };
    return [
      {
        field: "id",
        headerName: t("UUID"),
        width: 350,
      },
      {
        field: "sensor_type",
        headerName: t("Sensor type"),
        valueFormatter: ({ value }) => t(transType[value]),
        width: 150,
      },
      {
        field: "created",
        headerName: t("Created"),
        width: 200,
        valueFormatter: ({ value }) => new Date(value).toLocaleString(),
      },
    ];
  }

  getRows() {
    return this.props.sensors.map((item) => ({
      id: item.uuid,
      ...item,
    }));
  }

  render() {
    const rows = this.getRows();
    return (
      <div>
        <Button
          variant="contained"
          color="primary"
          onClick={() => history.push("/sensors/add")}
        >
          <Trans>Add</Trans> <Trans>sensor</Trans>
        </Button>
        <div style={{ height: 400, width: "100%" }}>
          <DataGrid
            rows={rows}
            columns={this.getColumns()}
            pageSize={Math.min(5, rows.length)}
            // checkboxSelection
            loading={this.props.isLoading}
          />
        </div>
      </div>
    );
  }
}

const mapStateToProps = (state) => state.sensors;

export default connect(mapStateToProps)(withNamespaces()(SensorComponent));
