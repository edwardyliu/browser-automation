import React from 'react'

import clsx from 'clsx'
import DeleteIcon from '@material-ui/icons/Delete'
import DeleteSweepIcon from '@material-ui/icons/DeleteSweep'
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
    titleLogoText: {
        fontSize: '2.0em',
        fontWeight: 'bold',
    },
    nColor: {
        color: '#010100',
    },
    aColor: {
        color: '#FD7F20',
    },
    uColor: {
        color: '#4d4d4d',
    },
    tColor: {
        color: '#FC2E20',
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

const NautoToolbar = ({
    globalFilter,
    handleAddOrder,
    handleClear,
    handleDeleteOrder,
    handleExportOrder,
    handleExportSelection,
    handleImportOrder,
    marketplace,
    numSelected,
    preGlobalFilteredRows,
    setGlobalFilter,
}) => {

    const classes = useStyles()
    
    return (
        <Toolbar
            className={clsx(classes.root, {
                [classes.highlight]: numSelected > 0,
            })}
        >
            <NautoAddDialog 
                handleAddOrder={handleAddOrder}
                marketplace={marketplace}
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
                    <span className={classes.titleLogoText}>
                        <span className={classes.nColor}>N</span>
                        <span className={classes.aColor}>a</span>
                        <span className={classes.uColor}>u</span>
                        <span className={classes.tColor}>to</span>
                    </span> Ordering Service
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
                            color="primary"
                            onClick={handleExportOrder}
                        >
                            <SaveIcon />
                        </IconButton>
                    </Tooltip>
                    <Tooltip title="Clear">
                        <IconButton
                            aria-label='clear'
                            color="secondary"
                            onClick={handleClear}
                        >
                            <DeleteSweepIcon />
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
    handleClear: PropTypes.func.isRequired,
    handleDeleteOrder: PropTypes.func.isRequired,
    handleExportOrder: PropTypes.func.isRequired,
    handleExportSelection: PropTypes.func.isRequired,
    handleImportOrder: PropTypes.func.isRequired,
    marketplace: PropTypes.array.isRequired,
    numSelected: PropTypes.number.isRequired,
    preGlobalFilteredRows: PropTypes.array,
    setGlobalFilter: PropTypes.func.isRequired,
}

export default NautoToolbar
