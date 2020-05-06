import React from 'react'

import AddOrderDialog from './AddOrderDialog'
import clsx from 'clsx'
import DeleteIcon from '@material-ui/icons/Delete'
import GlobalFilter from './GlobalFilter'
import IconButton from '@material-ui/core/IconButton'
import { lighten, makeStyles } from '@material-ui/core/styles'
import PropTypes from 'prop-types'
import PublishIcon from '@material-ui/icons/Publish';
import SaveIcon from '@material-ui/icons/Save';
import Toolbar from '@material-ui/core/Toolbar'
import Typography from '@material-ui/core/Typography'
import Tooltip from '@material-ui/core/Tooltip'

const useToolbarStyles = makeStyles(theme => ({
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
    iconBundle: {
        display: 'contents',
    },
    selectedIconBundle: {
        width: '25%',
        textAlign: 'right',
    },
    input: {
        display: 'none',
    },
}))

const TableToolbar = props => {
    const classes = useToolbarStyles()
    const {
    numSelected,
    addOrderHandler,
    deleteOrderHandler,
    importHandler,
    exportHandler,
    exportSelectedHandler,
    preGlobalFilteredRows,
    setGlobalFilter,
    globalFilter,
    } = props
    
    return (
        <Toolbar
            className={clsx(classes.root, {
                [classes.highlight]: numSelected > 0,
            })}
        >
            <AddOrderDialog addOrderHandler={addOrderHandler} />
            {numSelected > 0 ? (
                <Typography
                    className={classes.title}
                    color="inherit"
                    variant="subtitle1"
                >
                    {numSelected} selected
                </Typography>
            ) : (
                <Typography className={classes.title} variant="h6" id="tableTitle">
                    Orders
                </Typography>
            )}

            {numSelected > 0 ? (
                <div className={classes.selectedIconBundle}>
                    <Tooltip title="Export CSV">
                        <IconButton aria-label="export csv" onClick={exportSelectedHandler}>
                            <SaveIcon />
                        </IconButton>
                    </Tooltip>
                    <Tooltip title="Delete">
                        <IconButton aria-label="delete" onClick={deleteOrderHandler}>
                            <DeleteIcon />
                        </IconButton>
                    </Tooltip>
                </div>
            ) : (
                <div className={classes.iconBundle}>
                    <input className={classes.input} id="icon-import-csv" type="file" onChange={importHandler} />
                    <label htmlFor="icon-import-csv">
                        <Tooltip title="Import CSV">
                            <IconButton color="primary" aria-label="import csv" component="span">
                                <PublishIcon />
                            </IconButton>
                        </Tooltip>
                    </label>
                    <Tooltip title="Export CSV">
                        <IconButton color="secondary" aria-label="export csv" onClick={exportHandler}>
                            <SaveIcon />
                        </IconButton>
                    </Tooltip>
                    <GlobalFilter
                        preGlobalFilteredRows={preGlobalFilteredRows}
                        globalFilter={globalFilter}
                        setGlobalFilter={setGlobalFilter}
                    />
                </div>
            )}
        </Toolbar>
    )
}

TableToolbar.propTypes = {
  numSelected: PropTypes.number.isRequired,
  addOrderHandler: PropTypes.func.isRequired,
  deleteOrderHandler: PropTypes.func.isRequired,
  importHandler: PropTypes.func.isRequired,
  exportHandler: PropTypes.func.isRequired,
  exportSelectedHandler: PropTypes.func.isRequired,
  setGlobalFilter: PropTypes.func.isRequired,
  preGlobalFilteredRows: PropTypes.array.isRequired,
  globalFilter: PropTypes.string.isRequired,
}

export default TableToolbar
