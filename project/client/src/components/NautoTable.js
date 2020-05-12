import React from 'react'

import Button from '@material-ui/core/Button'
import CenterFocusWeakIcon from '@material-ui/icons/CenterFocusWeak'
import FileSaver from "file-saver"
import Papa from "papaparse"
import PropTypes from 'prop-types'
import { makeStyles } from '@material-ui/core/styles'
import MaUTable from '@material-ui/core/Table'
import SendIcon from '@material-ui/icons/Send'
import TableBody from '@material-ui/core/TableBody'
import TableCell from '@material-ui/core/TableCell'
import TableContainer from '@material-ui/core/TableContainer'
import TableFooter from '@material-ui/core/TableFooter'
import TableHead from '@material-ui/core/TableHead'
import TablePagination from '@material-ui/core/TablePagination'
import TableRow from '@material-ui/core/TableRow'
import TableSortLabel from '@material-ui/core/TableSortLabel'
import TextField from '@material-ui/core/TextField'
import {
    useGlobalFilter,
    usePagination,
    useRowSelect,
    useSortBy,
    useTable,
  } from 'react-table'

import NautoCell from './NautoCell'
import NautoCheckbox from './NautoCheckbox'
import NautoToolbar from './NautoToolbar'
import NautoPaginationActions from './NautoPaginationActions'

const defaultColumn = {
    Cell: NautoCell,
}

const useStyles = makeStyles((theme) => ({
    button: {
        margin: theme.spacing(1),
        float: 'right',
    },
    eMail: {
        display: 'flex',
        float: 'right',
    },
}))

const NautoTable = ({
    columns,
    data,
    handleRequestScan,
    handleRequestSend,
    marketplace,
    receipt,
    setData,
    setReceipt,
    skipPageReset,
    updateData,
}) => {
    
    const classes = useStyles()
    const {
        getTableProps,
        gotoPage,
        headerGroups,
        page,
        preGlobalFilteredRows,
        prepareRow,
        setGlobalFilter,
        setPageSize,
        state: { pageIndex, pageSize, selectedRowIds, globalFilter },
    } = useTable(
        {
            autoResetPage: !skipPageReset,
            columns,
            data,
            defaultColumn,
            // updateData isn't part of the API, but
            // anything we put into these options will
            // automatically be available on the instance.
            // That way we can call this function from our
            // cell renderer!
            updateData,
        },
        useGlobalFilter,
        useSortBy,
        usePagination,
        useRowSelect,
        hooks => {
            hooks.allColumns.push(columns => [
                // Let's make a column for selection
                {
                    id: 'selection',
                    // The header can use the table's getToggleAllRowsSelectedProps method
                    // to render a checkbox.  Pagination is a problem since this will select all
                    // rows even though not all rows are on the current page.  The solution should
                    // be server side pagination.  For one, the clients should not download all
                    // rows in most cases.  The client should only download data for the current page.
                    // In that case, getToggleAllRowsSelectedProps works fine.
                    Header: ({ getToggleAllRowsSelectedProps }) => (
                        <div>
                            <NautoCheckbox {...getToggleAllRowsSelectedProps()} />
                        </div>
                    ),
                    // The cell can use the individual row's getToggleRowSelectedProps method
                    // to the render a checkbox
                    Cell: ({ row }) => (
                        <div>
                            <NautoCheckbox {...row.getToggleRowSelectedProps()} />
                        </div>
                    ),
                },
                ...columns
            ])
        }
    )
    
    // == Utils ==
    const selectByIndexs = (array, indexs) => 
        array.filter((_, i) => indexs.includes(i))

    const removeByIndexs = (array, indexs) =>
        array.filter((_, i) => !indexs.includes(i))

    // == Events ==
    const handleChangePage = (event, newPage) => {
        gotoPage(newPage)
    }

    const handleChangeRowsPerPage = event => {
        setPageSize(Number(event.target.value))
    }

    const handleChangeReceipt = event => {
        setReceipt(event.target.value)
    }

    const handleAddOrder = cart => {
        const orders = cart['items'].map(item => ({
            "usrId": cart['usrId'],
            "orderId": cart['orderId'],
            "lut": cart['lut'],
            "env": item['env'],
            "name": item['name'],
        }))        
        const newData = data.concat(orders)
        setData(newData)
    }

    const handleDeleteOrder = () => {
        const newData = removeByIndexs(
            data,
            Object.keys(selectedRowIds).map(x => parseInt(x, 10))
        )
        setData(newData)
    }

    const handleClear = () => {
        setData([])
    }

    const handleImportOrder = event => {
        const file = event.target.files[0]
        const reader = new FileReader()
        reader.onload = event => {
            const csvData = event.target.result
            const newData = Papa.parse(csvData, { header: true }).data
            setData(newData)
        }
        reader.readAsText(file)
    }

    const handleExportOrder = () => {
        const newData = data
        const csvRaw = Papa.unparse(newData)
        const csvData = new Blob([csvRaw], { type: "text/csv;charset=utf-8;" })
        FileSaver.saveAs(csvData, "nauto.csv")
    }

    const handleExportSelection = () => {
        const newData = selectByIndexs(
            data,
            Object.keys(selectedRowIds).map(x => parseInt(x, 10))
        )
        const csvRaw = Papa.unparse(newData)
        const csvData = new Blob([csvRaw], { type: "text/csv;charset=utf-8;" })
        FileSaver.saveAs(csvData, "nauto-selection.csv")
    }

    return (
        <TableContainer>
            <NautoToolbar
                globalFilter={globalFilter}
                handleAddOrder={handleAddOrder}
                handleClear={handleClear}
                handleDeleteOrder={handleDeleteOrder}
                handleExportOrder={handleExportOrder}
                handleExportSelection={handleExportSelection}
                handleImportOrder={handleImportOrder}
                marketplace={marketplace}
                numSelected={Object.keys(selectedRowIds).length}
                preGlobalFilteredRows={preGlobalFilteredRows}
                setGlobalFilter={setGlobalFilter}
            />
            <MaUTable {...getTableProps()}>
                <TableHead>
                    {headerGroups.map(headerGroup => (
                        <TableRow {...headerGroup.getHeaderGroupProps()}>
                            {headerGroup.headers.map(column => (
                                <TableCell
                                    {...(column.id === 'selection'
                                    ? column.getHeaderProps()
                                    : column.getHeaderProps(column.getSortByToggleProps()))}
                                >
                                    {column.render('Header')}
                                    {column.id !== 'selection' ? (
                                        <TableSortLabel
                                            active={column.isSorted}
                                            // react-table has a unsorted state which is not treated here
                                            direction={column.isSortedDesc ? 'desc' : 'asc'}
                                        />
                                    ) : null}
                                </TableCell>
                            ))}
                        </TableRow>
                    ))}
                </TableHead>
                <TableBody>
                    {page.map((row, i) => {
                        prepareRow(row)
                        return (
                            <TableRow {...row.getRowProps()}>
                                {row.cells.map(cell => {
                                    return (
                                        <TableCell {...cell.getCellProps()}>
                                            {cell.render('Cell')}
                                        </TableCell>
                                    )
                                })}
                            </TableRow>
                        )
                    })}
                </TableBody>
                <TableFooter>
                    <TableRow>
                        <TablePagination
                            ActionsComponent={NautoPaginationActions}
                            colSpan={3}
                            count={data.length}
                            onChangePage={handleChangePage}
                            onChangeRowsPerPage={handleChangeRowsPerPage}
                            page={pageIndex}
                            rowsPerPage={pageSize}
                            rowsPerPageOptions={[
                                5,
                                10,
                                25,
                                50,
                                { label: 'All', value: data.length },
                            ]}
                            SelectProps={{
                                inputProps: { 'aria-label': 'rows per page' },
                                native: true,
                            }}
                        />
                        <TableCell />
                        <TableCell />
                        <TableCell className={classes.eMail}>
                            <TextField
                                label='E-mail Receipt'
                                onChange={handleChangeReceipt}
                                style={{ width: '275px' }}
                                type='text'
                                value={receipt}
                            />
                            <div>
                                <Button
                                    className={classes.button}
                                    color="secondary"
                                    endIcon={<SendIcon />}
                                    onClick={handleRequestSend}
                                    variant="contained"
                                >
                                    Send
                                </Button>
                                <Button
                                    className={classes.button}
                                    color="primary"
                                    endIcon={<CenterFocusWeakIcon />}
                                    onClick={handleRequestScan}
                                    variant="contained"
                                >
                                    Scan
                                </Button>
                            </div>
                        </TableCell>
                    </TableRow>
                </TableFooter>
            </MaUTable>
        </TableContainer>
    )
}

NautoTable.propTypes = {
    columns: PropTypes.array.isRequired,
    data: PropTypes.array.isRequired,
    handleRequestScan: PropTypes.func.isRequired,
    handleRequestSend: PropTypes.func.isRequired,
    marketplace: PropTypes.array.isRequired,
    receipt: PropTypes.string.isRequired,
    setData: PropTypes.func.isRequired,
    setReceipt: PropTypes.func.isRequired,
    skipPageReset: PropTypes.bool.isRequired,
    updateData: PropTypes.func.isRequired,
}

export default NautoTable
