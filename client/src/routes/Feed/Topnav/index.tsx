import React from "react";
import AppBar from "@mui/material/AppBar";
import Toolbar from "@mui/material/Toolbar";
import Typography from "@mui/material/Typography";
import IconButton from "@mui/material/IconButton";
import MenuIcon from "@mui/icons-material/Menu";
import Avatar, { genConfig } from "react-nice-avatar";
import { Box, Divider, Menu, MenuItem } from "@mui/material";
import { useUser } from "../../../hooks/useUser";
import { ExitToApp } from "@mui/icons-material";

const Topnav: React.FC = () => {
  const { user, logoff } = useUser();
  const [userOptionsAnchor, setUserOptionsAnchor] =
    React.useState<null | HTMLElement>(null);

  const [menuAnchor, setMenuAnchor] = React.useState<null | HTMLElement>(null);

  return (
    <AppBar position="fixed">
      <Toolbar>
        <IconButton
          edge="start"
          color="inherit"
          aria-label="menu"
          sx={{ mr: 2 }}
          onClick={(event) => setMenuAnchor(event.currentTarget)}
        >
          <MenuIcon />
        </IconButton>
        <Menu
          anchorEl={menuAnchor}
          open={Boolean(menuAnchor)}
          onClose={() => setMenuAnchor(null)}
        >
          <MenuItem>
            <Box sx={{ display: "flex", alignItems: "center", gap: 2 }}>
              <Typography>YOOO</Typography>
              <ExitToApp />
            </Box>
          </MenuItem>
        </Menu>
        <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
          Hermes
        </Typography>
        <Box>
          <IconButton
            size="large"
            edge="end"
            color="inherit"
            aria-label="account"
            onClick={(event) => setUserOptionsAnchor(event.currentTarget)}
          >
            <Avatar
              style={{ height: "3rem", width: "3rem" }}
              {...genConfig(user?.user_id || "default")}
            />
          </IconButton>
          <Menu
            anchorEl={userOptionsAnchor}
            open={Boolean(userOptionsAnchor)}
            onClose={() => setUserOptionsAnchor(null)}
          >
            <MenuItem>
              <Typography>
                <strong>{user?.user_id}</strong>
              </Typography>
            </MenuItem>
            <Divider />
            <MenuItem onClick={logoff}>
              <Box sx={{ display: "flex", alignItems: "center", gap: 2 }}>
                <Typography>Logout</Typography>
                <ExitToApp />
              </Box>
            </MenuItem>
          </Menu>
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default Topnav;
