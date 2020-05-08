import React from 'react'

import PropTypes from 'prop-types'

const cellStyle = {
    padding: 0,
    margin: 0,
    border: 0,
    background: 'transparent',
}

// Create an editable cell renderer
const NautoCell = ({
    value: initialValue,
    row: { index },
    column: { id },
    updateData, // This is a custom function that we supplied to our table instance
}) => {

    // We need to keep and update the state of the cell normally
    const [value, setValue] = React.useState(initialValue)

    const onChange = e => {
        setValue(e.target.value)
    }

    // We'll only update the external data when the input is blurred
    const onBlur = () => {
        updateData(index, id, value)
    }

    // If the initialValue is changed externally, sync it up with our state
    React.useEffect(() => {
        setValue(initialValue)
    }, [initialValue])

    return (
        <input
            style={cellStyle}
            value={value}
            onChange={onChange}
            onBlur={onBlur}
        />
    )
}

NautoCell.propTypes = {
    cell: PropTypes.shape({
        value: PropTypes.any.isRequired,
    }),
    row: PropTypes.shape({
        index: PropTypes.number.isRequired,
    }),
    column: PropTypes.shape({
        id: PropTypes.number.isRequired,
    }),
    updateData: PropTypes.func.isRequired,
}

export default NautoCell
