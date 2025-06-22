// // import {
// //   Button,
// //   Card,
// //   CardContent,
// //   CardHeader,
// //   Divider,
// //   Input,
// //   Stack,
// //   Tooltip,
// //   Typography,
// //   Chip,
// // } from "@mui/material";
// // import Grid from "@mui/material/Grid";
// // import { Google, Refresh } from "@mui/icons-material";
// // import { useState } from "react";
// // import { useUser } from "../../hooks/useUser";
// // import { useNavigate } from "react-router";
// // import { routes } from "../routes";

// // export const Login = () => {
// //   const loginCardStyle = {
// //     padding: 20,
// //     width: "60vh",
// //     margin: "auto auto",
// //   };

// //   const [username, setUsername] = useState("");
// //   const [randomUsername, setRandomUsername] = useState("");
// //   const navigate = useNavigate();
// //   const { login } = useUser();

// //   const handleLogin = async (username: string) => {
// //     const user = await login(username);

// //     if (user) {
// //       navigate(routes.MF);
// //     } else {
// //       console.error("Login failed");
// //     }
// //   };

// //   const getRandomUsername = async () => {
// //     const res = await fetch("/api/user/random");
// //     if (res.ok) {
// //       const data = await res.json();
// //       const randomUser = data as { user_id: string };
// //       setRandomUsername(randomUser.user_id);
// //     } else {
// //       console.error("Failed to fetch random username");
// //     }
// //   };

// //   return (
// //     <Grid
// //       justifyContent="center"
// //       alignItems="center"
// //       alignContent="center"
// //       height="80vh"
// //     >
// //       <Card elevation={10} style={loginCardStyle}>
// //         <CardHeader
// //           title="Login"
// //           sx={{ borderBottom: "1px solid lightgray" }}
// //         />
// //         <CardContent>
// //           <Stack gap="1rem">
// //             <Grid container spacing={2}>
// //               <Grid size="grow">
// //                 <Input
// //                   fullWidth
// //                   placeholder="Log in with MIND account"
// //                   value={username}
// //                   onChange={(event) => {
// //                     setUsername(event.target.value);
// //                   }}
// //                 />
// //               </Grid>
// //               <Grid size={2} alignSelf="end">
// //                 <Button
// //                   variant="contained"
// //                   color="primary"
// //                   onClick={() => {
// //                     handleLogin(username);
// //                   }}
// //                 >
// //                   login
// //                 </Button>
// //               </Grid>
// //             </Grid>
// //             <Grid container spacing={2}>
// //               <Grid size="grow">
// //                 <Typography>Log in with random MIND account</Typography>
// //               </Grid>
// //               <Grid>
// //                 <Chip label={randomUsername} />
// //               </Grid>
// //               <Grid>
// //                 <Button
// //                   variant="contained"
// //                   color="primary"
// //                   onClick={getRandomUsername}
// //                 >
// //                   <Typography>Resample</Typography>
// //                   <Refresh />
// //                 </Button>
// //               </Grid>
// //               <Grid>
// //                 <Button
// //                   variant="contained"
// //                   color="primary"
// //                   onClick={() => {
// //                     handleLogin(randomUsername);
// //                   }}
// //                 >
// //                   login
// //                 </Button>
// //               </Grid>
// //             </Grid>
// //             <Divider />
// //             <Tooltip title="Currently not supported">
// //               <Button variant="contained" color="primary">
// //                 <Grid container width="80%" justifyContent="space-between">
// //                   <Google />
// //                   <Typography>Login with Google</Typography>
// //                   <div></div>
// //                 </Grid>
// //               </Button>
// //             </Tooltip>
// //           </Stack>
// //         </CardContent>
// //       </Card>
// //     </Grid>
// //   );
// // };

// import React, { useEffect, useState } from "react";
// import { useAuth0 } from "@auth0/auth0-react";
// import axios from "axios";

// export default function Login() {
//   const {
//     loginWithRedirect,
//     logout,
//     user,
//     isAuthenticated,
//     getAccessTokenSilently,
//   } = useAuth0();

//   const [profile, setProfile] = useState<{
//     picture: string;
//     name: string;
//     email: string;
//   } | null>(null);

//   useEffect(() => {
//     const fetchProfile = async () => {
//       try {
//         const token = await getAccessTokenSilently();
//         const res = await axios.get("/api/profile", {
//           headers: { Authorization: `Bearer ${token}` },
//         });
//         setProfile(res.data);
//       } catch (err) {
//         console.error("Failed to fetch profile:", err);
//         setProfile(null);
//       }
//     };

//     if (isAuthenticated) {
//       fetchProfile();
//     } else {
//       setProfile(null);
//     }
//   }, [isAuthenticated, getAccessTokenSilently]);

//   return (
//     <div>
//       {isAuthenticated && profile ? (
//         <>
//           <img
//             src={profile.picture}
//             width="50"
//             alt={`${profile.name}'s avatar`}
//           />
//           <p>
//             {profile.name} ({profile.email})
//           </p>
//           <button
//             onClick={() =>
//               logout({ logoutParams: { returnTo: window.location.origin } })
//             }
//           >
//             Logout
//           </button>
//         </>
//       ) : (
//         <button onClick={() => loginWithRedirect()}>Login / Signup</button>
//       )}
//     </div>
//   );
// }

import React from "react";
import { useAuth0 } from "@auth0/auth0-react";

const LoginButton = () => {
  const { loginWithRedirect } = useAuth0();

  return <button onClick={() => loginWithRedirect()}>Log In</button>;
};

export default LoginButton;
