import React from 'react'

import clsx from 'clsx'
import DeleteIcon from '@material-ui/icons/Delete'
import IconButton from '@material-ui/core/IconButton'
import { lighten, makeStyles } from '@material-ui/core/styles'
import PropTypes from 'prop-types'
import PublishIcon from '@material-ui/icons/Publish'
import SaveIcon from '@material-ui/icons/Save'
import Toolbar from '@material-ui/core/Toolbar'
import Tooltip from '@material-ui/core/Tooltip'
import Typography from '@material-ui/core/Typography'

import NautoGlobalFilter from './NautoGlobalFilter'
import NautoAddDialog from './NautoAddDialog'

const useStyles = makeStyles(theme => ({
    root: {
        paddingLeft: theme.spacing(2),
        paddingRight: theme.spacing(1),
    },
    highlight:
        theme.palette.type === 'light'
            ? {
                color: theme.palette.secondary.main,
                backgroundColor: lighten(theme.palette.secondary.light, 0.85),
            }
            : {
                color: theme.palette.text.primary,
                backgroundColor: theme.palette.secondary.dark,
            },
    title: {
        flex: '1 1 100%',
    },
    defaultIconBundle: {
        display: 'contents',
    },
    selectedIconBundle: {
        width: '25%',
        textAlign: 'right',
    },
    importInput: {
        display: 'none',
    },
}))

const NautoToolbar = props => {
    const classes = useStyles()
    const {
        globalFilter,
        handleAddOrder,
        handleDeleteOrder,
        handleExportOrder,
        handleExportSelection,
        handleImportOrder,
        numSelected,
        possibleItems,
        preGlobalFilteredRows,
        setGlobalFilter,
    } = props

    return (
        <Toolbar
            className={clsx(classes.root, {
                [classes.highlight]: numSelected > 0,
            })}
        >
            <NautoAddDialog 
                handleAddOrder={handleAddOrder}
                possibleItems={possibleItems}
            />
            {numSelected > 0 ? (
                <Typography
                    className={classes.title}
                    color='inherit'
                    variant='subtitle1'
                >
                    {numSelected} selected
                </Typography>
            ) : (
                <Typography
                    className={classes.title}
                    variant='h6'
                    id='tableTitle'
                >
                    Nauto Orders
                </Typography>
            )}

            {numSelected > 0 ? (
                <div className={classes.selectedIconBundle}>
                    <Tooltip title='Export as CSV'>
                        <IconButton
                            aria-label='export as csv'
                            onClick={handleExportSelection}
                        >
                            <SaveIcon />
                        </IconButton>
                    </Tooltip>
                    <Tooltip title='Delete'>
                        <IconButton
                            aria-label='delete'
                            onClick={handleDeleteOrder}
                        >
                            <DeleteIcon />
                        </IconButton>
                    </Tooltip>
                </div>
            ) : (
                <div className={classes.defaultIconBundle}>
                    <input 
                        className={classes.importInput}
                        id='import-input'
                        onChange={handleImportOrder}
                        type='file'
                    />
                    <label htmlFor='import-input'>
                        <Tooltip title='Import via CSV'>
                            <IconButton
                                aria-label='import via csv'
                                color='primary'
                                component='span'
                            >
                                <PublishIcon />
                            </IconButton>
                        </Tooltip>
                    </label>
                    <Tooltip title="Export as CSV">
                        <IconButton
                            aria-label='export as csv'
                            color="secondary"
                            onClick={handleExportOrder}
                        >
                            <SaveIcon />
                        </IconButton>
                    </Tooltip>
                    <NautoGlobalFilter 
                        globalFilter={globalFilter}
                        preGlobalFilteredRows={preGlobalFilteredRows}
                        setGlobalFilter={setGlobalFilter}
                    />
                </div>
            )}
        </Toolbar>
    )
}

NautoToolbar.propTypes = {
    globalFilter: PropTypes.string,
    handleAddOrder: PropTypes.func.isRequired,
    handleDeleteOrder: PropTypes.func.isRequired,
    handleExportOrder: PropTypes.func.isRequired,
    handleExportSelection: PropTypes.func.isRequired,
    handleImportOrder: PropTypes.func.isRequired,
    numSelected: PropTypes.number.isRequired,
    possibleItems: PropTypes.array.isRequired,
    preGlobalFilteredRows: PropTypes.array,
    setGlobalFilter: PropTypes.func.isRequired,
}

export default NautoToolbar
