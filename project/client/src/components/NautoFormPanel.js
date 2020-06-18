import React from 'react'

import Button from '@material-ui/core/Button'
import Dialog from '@material-ui/core/Dialog'
import DialogActions from '@material-ui/core/DialogActions'
import DialogContent from '@material-ui/core/DialogContent'
import DialogContentText from '@material-ui/core/DialogContentText'
import DialogTitle from '@material-ui/core/DialogTitle'
import Draggable from 'react-draggable'
import Paper from '@material-ui/core/Paper'
import PropTypes from 'prop-types'
import TextField from '@material-ui/core/TextField'

const PaperComponent = props => {
    return (
        <Draggable handle="#nauto-form-panel" cancel={'[class*="MuiDialogContent-root"]'}>
            <Paper {...props} />
        </Draggable>
    )
}

const newForm = {
    usrId: "",
    secret: "",
}

const NautoFormPanel = ({
    formPanel,
    setFormPanel,
    handleRequestScan,
    handleRequestSend,
}) => {

    const open = (selection) => {
        if (selection === "") {
            return false
        } else {
            return true
        }
    }
    const [form, setForm] = React.useState(newForm)

    // == Events ==
    const handleClose = () => {
        setForm(newForm)
        setFormPanel("")
    }
    const handleSubmit = () => {
        if (formPanel === "Scan") {
            handleRequestScan(form)
        } else if (formPanel === "Send") {
            handleRequestSend(form)
        }
        setForm(newForm)
        setFormPanel("")
    }
    const handleChangeTextField = name => ({ target: { value } }) => {
        setForm({ ...form, [name]: value })
    }

    return (
        <div>
            <Dialog
            open={open(formPanel)}
            onClose={handleClose}
            PaperComponent={PaperComponent}
            aria-labelledby="nauto-form-panel"
            >
                <DialogTitle style={{ cursor: 'move' }} id="nauto-form-panel">
                    Request Confirmation Panel
                </DialogTitle>
                <DialogContent>
                    <DialogContentText>
                        Please Confirm the Following:<br/>
                        1. Identity of the Requestor (i.e. You)<br/>
                        2. The Correctness of the Order(s)
                    </DialogContentText>
                    <TextField
                        autoFocus
                        fullWidth
                        label='User ID'
                        margin='dense'
                        onChange={handleChangeTextField('usrId')}
                        required
                        type='text'
                        value={form.usrId}
                        variant='filled'
                    />
                    <TextField
                        autoFocus
                        fullWidth
                        label='Secret'
                        margin='dense'
                        onChange={handleChangeTextField('secret')}
                        required
                        type='password'
                        value={form.secret}
                        variant='filled'
                    />
                </DialogContent>
                <DialogActions>
                    <Button
                        autoFocus
                        color="secondary"
                        onClick={handleClose}
                    >
                        Cancel
                    </Button>
                    <Button
                        color="primary"
                        disabled={!(form.usrId && form.secret)}
                        onClick={handleSubmit}
                    >
                        Submit
                    </Button>
                </DialogActions>
            </Dialog>
        </div>
    )
}

NautoFormPanel.propTypes = {
    formPanel: PropTypes.string.isRequired,
    setFormPanel: PropTypes.func.isRequired,
    handleRequestScan: PropTypes.func.isRequired,
    handleRequestSend: PropTypes.func.isRequired,
}

export default NautoFormPanel