import React from 'react'

import axios from 'axios'
import CssBaseline from '@material-ui/core/CssBaseline'
import NautoNotification from './components/NautoNotification'
import NautoTable from './components/NautoTable'

const App = () => {

    const server = "http://127.0.0.1:5000/api"
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
                Header: "Dictionary",
                accessor: "lut",
            },
            {
                Header: "Environment",
                accessor: "env",
            },
            {
                Header: "Order Name",
                accessor: "name",
            },
        ],
        []
    )
    
    // == States ==
    // For Request: Table
    const [data, setData] = React.useState(React.useMemo(() => [], []))
    const [marketplace, setMarketplace] = React.useState([])
    const [receipt, setReceipt] = React.useState("")

    // For Response: Notification
    const [uid, setUID] = React.useState("")
    const [notification, setNotification] = React.useState(false)
    
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

    // == Effects ==
    React.useEffect(() => {
        axios.get(server.concat('/tasks'))
            .then(response => {
                setMarketplace(response.data)
            }, error => {
                console.log(error)
            })
    }, [])

    // == Events ==
    const handleRequestScan = () => {
        setUID("")
        axios.post(server.concat('/scan'), {
                'receipt': receipt,
                'package': data,
            })
            .then(response => {
                setUID(response.data.scanId)
                setNotification(true)
            }, error => {
                console.log(error)
            })
        setNotification(true)
    }

    const handleRequestSend = () => {
        setUID("")
        axios.post(server.concat('/job'), {
                'receipt': receipt,
                'package': data,
            })
            .then(response => {
                setUID(response.data.jobId)
                setNotification(true)
            }, error => {
                console.log(error)
            })
        setNotification(true)
    }

    return (
        <div>
            <CssBaseline />
            <NautoTable
                columns={columns}
                data={data}
                handleRequestScan={handleRequestScan}
                handleRequestSend={handleRequestSend}
                marketplace={marketplace}
                receipt={receipt}
                setData={setData}
                setReceipt={setReceipt}
                skipPageReset={skipPageReset}
                updateData={updateData}
            />
            <NautoNotification 
                uid={uid}
                notification={notification}
                setNotification={setNotification}
            />
        </div>
    )
}

export default App
