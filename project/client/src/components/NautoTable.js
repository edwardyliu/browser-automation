import React from 'react'

import Button from '@material-ui/core/Button';
import CenterFocusWeakIcon from '@material-ui/icons/CenterFocusWeak';
import FileSaver from "file-saver"
import Papa from "papaparse"
import PropTypes from 'prop-types'
import { makeStyles } from '@material-ui/core/styles';
import MaUTable from '@material-ui/core/Table'
import SendIcon from '@material-ui/icons/Send';
import TableBody from '@material-ui/core/TableBody'
import TableCell from '@material-ui/core/TableCell'
import TableContainer from '@material-ui/core/TableContainer'
import TableFooter from '@material-ui/core/TableFooter'
import TableHead from '@material-ui/core/TableHead'
import TablePagination from '@material-ui/core/TablePagination'
import TableRow from '@material-ui/core/TableRow'
import TableSortLabel from '@material-ui/core/TableSortLabel'
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
    },
    rightwards: {
        float: 'right',
    },
}))

const NautoTable = ({
    columns,
    data,
    setData,
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
    
    const possibleItems = [
        { name: 'The Shawshank Redemption', env: "DEV" },
        { name: 'The Godfather', env: "DEV" },
        { name: 'The Godfather: Part II', env: "DEV" },
        { name: 'The Dark Knight', env: "DEV" },
        { name: '12 Angry Men', env: "DEV" },
        { name: "Schindler's List", env: "DEV" },
        { name: 'Pulp Fiction', env: "DEV" },
        { name: 'The Lord of the Rings: The Return of the King', env: "DEV" },
        { name: 'The Good, the Bad and the Ugly', env: "DEV" },
        { name: 'Fight Club', env: "DEV" },
        { name: 'The Lord of the Rings: The Fellowship of the Ring', env: "DEV" },
        { name: 'Star Wars: Episode V - The Empire Strikes Back', env: "DEV" },
        { name: 'Forrest Gump', env: "DEV" },
        { name: 'Inception', env: "DEV" },
        { name: 'The Lord of the Rings: The Two Towers', env: "DEV" },
        { name: "One Flew Over the Cuckoo's Nest", env: "DEV" },
        { name: 'Goodfellas', env: "DEV" },
        { name: 'The Matrix', env: "DEV" },
        { name: 'Seven Samurai', env: "DEV" },
        { name: 'Star Wars: Episode IV - A New Hope', env: "DEV" },
        { name: 'City of God', env: "UAT" },
        { name: 'Se7en', env: "UAT" },
        { name: 'The Silence of the Lambs', env: "UAT" },
        { name: "It's a Wonderful Life", env: "UAT" },
        { name: 'Life Is Beautiful', env: "UAT" },
        { name: 'The Usual Suspects', env: "UAT" },
        { name: 'Léon: The Professional', env: "UAT" },
        { name: 'Spirited Away', env: "UAT" },
        { name: 'Saving Private Ryan', env: "UAT" },
        { name: 'Once Upon a Time in the West', env: "UAT" },
        { name: 'American History X', env: "UAT" },
        { name: 'Interstellar', env: "UAT" },
        { name: 'Casablanca', env: "UAT" },
        { name: 'City Lights', env: "UAT" },
        { name: 'Psycho', env: "UAT" },
        { name: 'The Green Mile', env: "UAT" },
        { name: 'The Intouchables', env: "UAT" },
        { name: 'Modern Times', env: "UAT" },
        { name: 'Raiders of the Lost Ark', env: "UAT" },
        { name: 'Rear Window', env: "UAT" },
        { name: 'The Pianist', env: "UAT" },
        { name: 'The Departed', env: "UAT" },
        { name: 'Terminator 2: Judgment Day', env: "UAT" },
        { name: 'Back to the Future', env: "UAT" },
        { name: 'Whiplash', env: "PROD" },
        { name: 'Gladiator', env: "PROD" },
        { name: 'Memento', env: "PROD" },
        { name: 'The Prestige', env: "PROD" },
        { name: 'The Lion King', env: "PROD" },
        { name: 'Apocalypse Now', env: "PROD" },
        { name: 'Alien', env: "PROD" },
        { name: 'Sunset Boulevard', env: "PROD" },
        { name: 'Dr. Strangelove or: How I Learned to Stop Worrying and Love the Bomb', env: "PROD" },
        { name: 'The Great Dictator', env: "PROD" },
        { name: 'Cinema Paradiso', env: "PROD" },
        { name: 'The Lives of Others', env: "PROD" },
        { name: 'Grave of the Fireflies', env: "PROD" },
        { name: 'Paths of Glory', env: "PROD" },
        { name: 'Django Unchained', env: "PROD" },
        { name: 'The Shining', env: "PROD" },
        { name: 'WALL·E', env: "PROD" },
        { name: 'American Beauty', env: "PROD" },
    ]

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

    const handleAddOrder = cart => {
        const orders = cart['items'].map(item => ({
            "usrId": cart['usrId'],
            "lut": cart['lut'],
            "name": item['name'],
            "env": item['env'],
        }))
        console.log(orders)
        
        const newData = data.concat(orders)
        setData(newData)
    }

    const handleDeleteOrder = event => {
        const newData = removeByIndexs(
            data,
            Object.keys(selectedRowIds).map(x => parseInt(x, 10))
        )
        setData(newData)
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

    const handleExportOrder = event => {
        const newData = data
        const csvRaw = Papa.unparse(newData)
        const csvData = new Blob([csvRaw], { type: "text/csv;charset=utf-8;" })
        FileSaver.saveAs(csvData, "nauto.csv")
    }

    const handleExportSelection = event => {
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
                handleDeleteOrder={handleDeleteOrder}
                handleExportOrder={handleExportOrder}
                handleExportSelection={handleExportSelection}
                handleImportOrder={handleImportOrder}
                numSelected={Object.keys(selectedRowIds).length}
                possibleItems={possibleItems}
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
                        <TableCell></TableCell>
                        <TableCell className={classes.rightwards}>
                            <Button
                                variant="contained"
                                color="secondary"
                                className={classes.button}
                                endIcon={<SendIcon />}
                            >
                                Send
                            </Button>
                            <Button
                                variant="contained"
                                color="primary"
                                className={classes.button}
                                endIcon={<CenterFocusWeakIcon />}
                            >
                                Scan
                            </Button>
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
    setData: PropTypes.func.isRequired,
    skipPageReset: PropTypes.bool.isRequired,
    updateData: PropTypes.func.isRequired,
}

export default NautoTable
