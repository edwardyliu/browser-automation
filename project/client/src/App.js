import React from 'react'

import CssBaseline from '@material-ui/core/CssBaseline'
import NautoTable from './components/NautoTable'

const App = () => {

    const columns = React.useMemo(
        () => [
            {
                Header: "User ID",
                accessor: "usrId",
            },
            {
                Header: "Order ID",
                accessor: "orderId",
            },
            {
                Header: "Environment",
                accessor: "env",
            },
            {
                Header: "Order Name",
                accessor: "name",
            },
            {
                Header: "Dictionary",
                accessor: "lut",
            },
        ],
        []
    )
    const [data, setData] = React.useState(React.useMemo(() => [], []))
    
    // We need to keep the table from resetting the pageIndex when we
    // Update data. So we can keep track of that flag with a ref.
    const [skipPageReset, setSkipPageReset] = React.useState(false)

    // When our cell renderer calls updateData, we'll use
    // the rowIndex, columnId and new value to update the
    // original data
    const updateData = (rowIndex, columnId, value) => {
        // We also turn on the flag to not reset the page
        setSkipPageReset(true)
        setData(old =>
            old.map((row, index) => {
                if (index === rowIndex) {
                    return {
                        ...old[rowIndex],
                        [columnId]: value,
                    }
                }
                return row
            })
        )
    }

    return (
        <div>
            <CssBaseline />
            <NautoTable
                columns={columns}
                data={data}
                setData={setData}
                skipPageReset={skipPageReset}
                updateData={updateData}
            />
        </div>
    )
}

export default App
