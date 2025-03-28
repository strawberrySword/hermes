import { Avatar, Button, Card, CardContent, CardHeader, Checkbox, FormControlLabel, Grid, Link, Paper, TextField, Typography } from '@mui/material'
import { Google, LockOutlined } from '@mui/icons-material'
import React from 'react'

export const Login = () => {

    const loginCardStyle = { padding: 20, height: '20vh', width: '60vh', margin: 'auto auto' }

    return (
        <Grid justifyContent='center' alignItems='center' alignContent='center' height='80vh'>
            <Card elevation={10} style={loginCardStyle}>
                <CardHeader
                    title='Login!'
                    // have a bottom border for the card header
                    sx={{ borderBottom: '1px solid lightgray' }}
                />

                <CardContent>
                    <Button
                        variant='contained'
                        fullWidth
                        color='primary'
                    >
                        <Grid
                            container
                            // have grid full width
                            width='80%'
                            justifyContent='space-between'
                                                         
                        >
                            <Google />
                            <Typography>
                                Login with Google
                            </Typography>
                            <div></div>
                        </Grid>
                    </Button>
                </CardContent>
            </Card>
        </Grid>
    )
}