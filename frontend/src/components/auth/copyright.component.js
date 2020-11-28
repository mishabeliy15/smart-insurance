import Typography from "@material-ui/core/Typography";
import Link from "@material-ui/core/Link";
import React from "react";

function CopyrightComponent() {
  return (
    <Typography variant="body2" color="textSecondary" align="center">
      {"Copyright © "}
      <Link color="inherit" href="#">
        Smart Insurance by Mykhailo Bilyi
      </Link>{" "}
      {new Date().getFullYear()}
      {"."}
    </Typography>
  );
}

export default CopyrightComponent;
