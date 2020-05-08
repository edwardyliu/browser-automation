import React from 'react'

import FindInPageIcon from '@material-ui/icons/FindInPage'
import InputBase from '@material-ui/core/InputBase'
import { makeStyles, fade } from '@material-ui/core'
import PropTypes from 'prop-types'
import Tooltip from '@material-ui/core/Tooltip'

const useStyles = makeStyles(theme => ({
    search: {
        position: 'relative',
        borderRadius: theme.shape.borderRadius,
        backgroundColor: fade(theme.palette.common.white, 0.15),
        '&:hover': {
            backgroundColor: fade(theme.palette.common.white, 0.25),
        },
        marginRight: theme.spacing(2),
        marginLeft: 0,
        width: '100%',
        [theme.breakpoints.up('sm')]: {
            marginLeft: theme.spacing(3),
            width: 'auto',
        },
    },
    searchIcon: {
        width: theme.spacing(7),
        height: '100%',
        position: 'absolute',
        pointerEvents: 'none',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
    },
    inputRoot: {
        color: 'inherit',
    },
    inputInput: {
        padding: theme.spacing(1, 1, 1, 7),
        transition: theme.transitions.create('width'),
        width: '100%',
        [theme.breakpoints.up('md')]: {
            width: 200,
        },
    },
}))

const NautoGlobalFilter = ({
    globalFilter,
    preGlobalFilteredRows,
    setGlobalFilter,
}) => {

    const classes = useStyles()
    const count = preGlobalFilteredRows.length

    // Global filter only works with pagination from the first page.
    // This may not be a problem for server side pagination when
    // only the current page is downloaded.
    return (
        <div className={classes.search}>
            <div className={classes.searchIcon}>
                <FindInPageIcon />
            </div>
            <Tooltip title="Search">
                <InputBase 
                    value={globalFilter || ''}
                    onChange={e => {
                        setGlobalFilter(e.target.value || undefined) // Set undefined to remove the filter entirely
                    }}
                    placeholder={`${count} records...`}
                    classes={{
                        root: classes.inputRoot,
                        input: classes.inputInput,
                    }}
                    inputProps={{ 'aria-label': 'search' }}
                />
            </Tooltip>
        </div>
    )
}

NautoGlobalFilter.propTypes = {
    globalFilter: PropTypes.string,
    preGlobalFilteredRows: PropTypes.array.isRequired,
    setGlobalFilter: PropTypes.func.isRequired,
}

export default NautoGlobalFilter
