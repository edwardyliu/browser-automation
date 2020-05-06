import React, { useState } from 'react'

import AddIcon from '@material-ui/icons/Add'
import Button from '@material-ui/core/Button'
import Dialog from '@material-ui/core/Dialog'
import DialogActions from '@material-ui/core/DialogActions'
import DialogContent from '@material-ui/core/DialogContent'
import DialogContentText from '@material-ui/core/DialogContentText'
import DialogTitle from '@material-ui/core/DialogTitle'
import IconButton from '@material-ui/core/IconButton'
import PropTypes from 'prop-types'
import Switch from '@material-ui/core/Switch'
import TextField from '@material-ui/core/TextField'
import Tooltip from '@material-ui/core/Tooltip'

const initialOrder = {
    userId: "",
    orderId: "",
    env: "",
    dict: "",
    subRows: undefined,
}

const AddOrderDialog = props => {
    const [order, setOrder] = useState(initialOrder)
    const { addOrderHandler } = props
    const [open, setOpen] = React.useState(false)

    const [switchState, setSwitchState] = React.useState({
        addMultiple: false,
    })

    const handleSwitchChange = name => event => {
        setSwitchState({ ...switchState, [name]: event.target.checked })
    }

    const resetSwitch = () => {
        setSwitchState({ addMultiple: false })
    }

    const handleClickOpen = () => {
        setOpen(true)
    }

    const handleClose = () => {
        setOpen(false)
        resetSwitch()
    }

    const handleAdd = event => {
        addOrderHandler(order)
        setOrder(initialOrder)
        switchState.addMultiple ? setOpen(true) : setOpen(false)
    }

    const handleChange = name => ({ target: { value } }) => {
        setOrder({ ...order, [name]: value })
    }

    return (
        <div>
            <Tooltip title="Add">
                <IconButton aria-label="add" onClick={handleClickOpen}>
                    <AddIcon />
                </IconButton>
            </Tooltip>
            <Dialog
                open={open}
                onClose={handleClose}
                aria-labelledby="form-dialog-title"
            >
                <DialogTitle id="form-dialog-title">Add Order</DialogTitle>
                <DialogContent>
                    <DialogContentText>Add a new order</DialogContentText>
                    <TextField
                        autoFocus
                        margin="dense"
                        label="User ID"
                        type="text"
                        fullWidth
                        value={order.userId}
                        onChange={handleChange('userId')}
                    />
                    <TextField
                        margin="dense"
                        label="Order ID"
                        type="text"
                        fullWidth
                        value={order.orderId}
                        onChange={handleChange('orderId')}
                    />
                    <TextField
                        margin="dense"
                        label="Environment"
                        type="text"
                        fullWidth
                        value={order.env}
                        onChange={handleChange('env')}
                    />
                    <TextField
                        margin="dense"
                        label="Dictionary"
                        type="text"
                        fullWidth
                        value={order.dict}
                        onChange={handleChange('dict')}
                    />
                </DialogContent>
                <DialogActions>
                    <Tooltip title="Add multiple">
                        <Switch
                            checked={switchState.addMultiple}
                            onChange={handleSwitchChange('addMultiple')}
                            value="addMultiple"
                            inputProps={{ 'aria-label': 'secondary checkbox' }}
                            />
                    </Tooltip>
                    <Button onClick={handleClose} color="primary">
                        Cancel
                    </Button>
                    <Button onClick={handleAdd} color="primary">
                        Add
                    </Button>
                </DialogActions>
            </Dialog>
        </div>
    )
}

AddOrderDialog.propTypes = {
    addOrderHandler: PropTypes.func.isRequired,
}

export default AddOrderDialog
