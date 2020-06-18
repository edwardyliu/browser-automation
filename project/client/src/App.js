import React from 'react'

import axios from 'axios'
import CssBaseline from '@material-ui/core/CssBaseline'
import NautoFormPanel from './components/NautoFormPanel'
import NautoNotification from './components/NautoNotification'
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

    // For Secret Information: Form Panel
    const [formPanel, setFormPanel] = React.useState("")

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
        axios.get('/api/keys')
            .then(response => {
                setMarketplace(response.data)
            }, error => {
                console.log(error)
            })
    }, [])

    // == Events ==
    const handleButtonScan = () => { setFormPanel("Scan") }
    const handleButtonSend = () => { setFormPanel("Send") }

    // == Requests ==
    const handleRequestScan = (form) => {
        setUID("")
        axios.post('/api/scan', {
                'receipt': receipt,
                'form': form,
                'data': data,
            })
            .then(response => {
                setUID(response.data.data.job_id)
                setNotification(true)
            }, error => {
                console.log(error)
            })
        setNotification(true)
    }

    const handleRequestSend = (form) => {
        setUID("")
        axios.post('/api/job', {
                'receipt': receipt,
                'form': form,
                'data': data,
            })
            .then(response => {
                setUID(response.data.data.job_id)
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
                handleButtonScan={handleButtonScan}
                handleButtonSend={handleButtonSend}
                marketplace={marketplace}
                receipt={receipt}
                setData={setData}
                setReceipt={setReceipt}
                skipPageReset={skipPageReset}
                updateData={updateData}
            />
            <NautoFormPanel
                formPanel={formPanel}
                setFormPanel={setFormPanel}
                handleRequestScan={handleRequestScan}
                handleRequestSend={handleRequestSend}
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