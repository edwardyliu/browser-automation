import React from 'react'

import LinearProgress from '@material-ui/core/LinearProgress'
import { makeStyles } from '@material-ui/core'
import MuiAlert from '@material-ui/lab/Alert'
import PropTypes from 'prop-types'
import Snackbar from '@material-ui/core/Snackbar'

const Alert = props => {
    return (
        <MuiAlert elevation={6} variant='filled' {...props} />
    )
}

const useStyles = makeStyles(theme => ({
    barBGColor: {
        background: '#ccf0ff',
    },
    progress: {
        display: 'block',
        paddingTop: '10px',
    },
    uid: {
        color: '#004f00',
        fontSize: '1.1em',
        fontWeight: 'bold',
    },
}))

const NautoNotification = ({
    uid,
    notification,
    setNotification,
}) => {

    const classes = useStyles()

    // == Events ==
    const handleClose = () => {
        setNotification(false)
    }

    return (
        <Snackbar
            autoHideDuration={6000}
            onClose={handleClose}
            open={notification}
        >
            {uid ? (
                <Alert onClose={handleClose} severity="success">
                    Request Successful!<br />
                    Task ID: <span className={classes.uid}>{uid}</span>
                </Alert>
            ) : (
                <Alert onClose={handleClose} severity="info">
                    Your request is being processed:<br />
                    <span className={classes.progress}><LinearProgress className={classes.barBGColor} /></span>
                </Alert>
            )}
        </Snackbar>
    )
}

NautoNotification.propTypes = {
    uid: PropTypes.string.isRequired,
    notification: PropTypes.bool.isRequired,
    setNotification: PropTypes.func.isRequired,
}

export default NautoNotification
