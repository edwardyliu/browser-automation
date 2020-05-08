import React from "react"

import AddIcon from '@material-ui/icons/Add'
import Autocomplete from '@material-ui/lab/Autocomplete'
import Button from '@material-ui/core/Button'
import Checkbox from '@material-ui/core/Checkbox';
import CheckBoxIcon from '@material-ui/icons/CheckBox';
import CheckBoxOutlineBlankIcon from '@material-ui/icons/CheckBoxOutlineBlank';
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

const newCart = {
    usrId: "",
    lut: "",
    items: [],
}

const NautoAddDialog = props => {
    const {
        handleAddOrder,
        possibleItems,
    } = props

    const [cart, setCart] = React.useState(newCart)
    const [open, setOpen] = React.useState(false)
    const [switchState, setSwitchState] = React.useState({
        addMultiple: false,
    })

    // == Events ==
    const handleOpen = () => {
        setOpen(true)
    }

    const handleChangeSwitchState = name => event => {
        setSwitchState({ ...switchState, [name]: event.target.checked })
    }

    const resetSwitchState = () => {
        setSwitchState({ addMultiple: false })
    }

    const handleChangeTextField = name => ({ target: { value } }) => {
        setCart({ ...cart, [name]: value })
    }

    const handleChangeAutocomplete = (event, value, name) => {
        setCart({ ...cart, [name]: value })
    }

    const handleAdd = event => {
        handleAddOrder(cart)
        setCart(newCart)
        switchState.addMultiple ? setOpen(true) : setOpen(false)
    }

    const handleClose = () => {
        setOpen(false)
        resetSwitchState()
    }

    return (
        <div>
            <Tooltip title="Add">
                <IconButton aria-label="add" onClick={handleOpen}>
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
                    <DialogContentText>Add new order</DialogContentText>
                    <TextField
                        autoFocus
                        fullWidth
                        label="User ID"
                        margin="normal"
                        onChange={handleChangeTextField('usrId')}
                        type="text"
                        value={cart.usrId}
                    />
                    <TextField
                        fullWidth
                        label="Look-Up Table"
                        margin="normal"
                        onChange={handleChangeTextField('lut')}
                        type="text"
                        value={cart.lut}
                    />
                     <Autocomplete
                        disableCloseOnSelect
                        fullWidth
                        id="autocomplete-cart-items"
                        margin="normal"
                        multiple
                        options={possibleItems}
                        getOptionLabel={(option) => (option.env + ": " + option.name)}
                        onChange={(event, value) => handleChangeAutocomplete(event, value, 'items')}
                        value={cart.items}
                        renderOption={(option, { selected }) => (
                            <React.Fragment>
                                <Checkbox
                                    icon={<CheckBoxOutlineBlankIcon fontSize="small" />}
                                    checkedIcon={<CheckBoxIcon fontSize="small" />}
                                    style={{ marginRight: 8 }}
                                    checked={selected}
                                />
                                {option.env + ": " + option.name}
                            </React.Fragment>
                        )}
                        renderInput={(params) => (
                            <TextField {...params} variant="outlined" label="Orders" placeholder="Orders" />
                        )}
                    />
                </DialogContent>
                <DialogActions>
                    <Tooltip title="Add multiple">
                        <Switch
                            checked={switchState.addMultiple}
                            inputProps={{ 'aria-label': 'secondary checkbox' }}
                            onChange={handleChangeSwitchState('addMultiple')}
                            value="addMultiple"
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

NautoAddDialog.propTypes = {
    handleAddOrder: PropTypes.func.isRequired,
    possibleItems: PropTypes.array.isRequired,
}

export default NautoAddDialog
