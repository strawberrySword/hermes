import React from "react";
import AppBar from "@mui/material/AppBar";
import Toolbar from "@mui/material/Toolbar";
import Typography from "@mui/material/Typography";
import IconButton from "@mui/material/IconButton";
import MenuIcon from "@mui/icons-material/Menu";
import Avatar from "@mui/material/Avatar";
import { Box, Divider, Menu, MenuItem } from "@mui/material";
import { Apps, ExitToApp, History } from "@mui/icons-material";
import { Link } from "react-router";
import { routes } from "../../routes";
import { useAuth0 } from "@auth0/auth0-react";

const Topnav: React.FC = () => {
  const { user, logout } = useAuth0();
  const [userOptionsAnchor, setUserOptionsAnchor] =
    React.useState<null | HTMLElement>(null);

  const [menuAnchor, setMenuAnchor] = React.useState<null | HTMLElement>(null);

  return (
    <>
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
            <MenuItem
              component={Link}
              to={routes.HISTORY}
              onClick={() => setMenuAnchor(null)}
            >
              <Box
                sx={{
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "space-between",
                  width: "100%",
                  gap: 2,
                }}
              >
                <Typography>History</Typography>
                <History />
              </Box>
            </MenuItem>
            <MenuItem
              component={Link}
              to={routes.FEED}
              onClick={() => setMenuAnchor(null)}
            >
              <Box
                sx={{
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "space-between",
                  width: "100%",
                  gap: 2,
                }}
              >
                <Typography>Feed</Typography>
                <Apps />
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
                alt={user?.preferred_username}
                src={user?.picture}
              />
            </IconButton>
            <Menu
              anchorEl={userOptionsAnchor}
              open={Boolean(userOptionsAnchor)}
              onClose={() => setUserOptionsAnchor(null)}
            >
              <MenuItem>
                <Typography>
                  <strong>{user?.email}</strong>
                </Typography>
              </MenuItem>
              <Divider />
              <MenuItem
                onClick={() =>
                  logout({ logoutParams: { returnTo: window.location.origin } })
                }
              >
                <Box sx={{ display: "flex", alignItems: "center", gap: 2 }}>
                  <Typography>Logout</Typography>
                  <ExitToApp />
                </Box>
              </MenuItem>
            </Menu>
          </Box>
        </Toolbar>
      </AppBar>
      <Toolbar />
    </>
  );
};

export default Topnav;
