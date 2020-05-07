import React from 'react'
import TextField from '@material-ui/core/TextField'
import Autocomplete from '@material-ui/lab/Autocomplete'
import parse from 'autosuggest-highlight/parse'
import match from 'autosuggest-highlight/match'

const top100Films = [
    { title: 'DEV: The Shawshank Redemption', year: 1994 },
    { title: 'DEV: The Godfather', year: 1972 },
    { title: 'DEV: The Godfather: Part II', year: 1974 },
    { title: 'DEV: The Dark Knight', year: 2008 },
    { title: 'DEV: 12 Angry Men', year: 1957 },
    { title: "DEV: Schindler's List", year: 1993 },
    { title: 'DEV: Pulp Fiction', year: 1994 },
    { title: 'DEV: The Lord of the Rings: The Return of the King', year: 2003 },
    { title: 'DEV: The Good, the Bad and the Ugly', year: 1966 },
    { title: 'DEV: Fight Club', year: 1999 },
    { title: 'DEV: The Lord of the Rings: The Fellowship of the Ring', year: 2001 },
    { title: 'UAT: Star Wars: Episode V - The Empire Strikes Back', year: 1980 },
    { title: 'UAT: Forrest Gump', year: 1994 },
    { title: 'UAT: Inception', year: 2010 },
    { title: 'UAT: The Lord of the Rings: The Two Towers', year: 2002 },
    { title: "UAT: One Flew Over the Cuckoo's Nest", year: 1975 },
    { title: 'UAT: Goodfellas', year: 1990 },
    { title: 'UAT: The Matrix', year: 1999 },
    { title: 'UAT: Seven Samurai', year: 1954 },
    { title: 'UAT: Star Wars: Episode IV - A New Hope', year: 1977 },
    { title: 'UAT: City of God', year: 2002 },
    { title: 'UAT: Se7en', year: 1995 },
    { title: 'UAT: The Silence of the Lambs', year: 1991 },
    { title: "UAT: It's a Wonderful Life", year: 1946 },
    { title: 'UAT: Life Is Beautiful', year: 1997 },
    { title: 'UAT: The Usual Suspects', year: 1995 },
    { title: 'UAT: Léon: The Professional', year: 1994 },
    { title: 'UAT: Spirited Away', year: 2001 },
    { title: 'SIT: Saving Private Ryan', year: 1998 },
    { title: 'SIT: Once Upon a Time in the West', year: 1968 },
    { title: 'SIT: American History X', year: 1998 },
    { title: 'SIT: Interstellar', year: 2014 },
    { title: 'SIT: Casablanca', year: 1942 },
    { title: 'SIT: City Lights', year: 1931 },
    { title: 'SIT: Psycho', year: 1960 },
    { title: 'SIT: The Green Mile', year: 1999 },
    { title: 'SIT: The Intouchables', year: 2011 },
    { title: 'SIT: Modern Times', year: 1936 },
    { title: 'SIT: Raiders of the Lost Ark', year: 1981 },
    { title: 'SIT: Rear Window', year: 1954 },
    { title: 'SIT: The Pianist', year: 2002 },
    { title: 'SIT: The Departed', year: 2006 },
    { title: 'SIT: Terminator 2: Judgment Day', year: 1991 },
    { title: 'SIT: Back to the Future', year: 1985 },
    { title: 'PROD: Whiplash', year: 2014 },
    { title: 'PROD: Gladiator', year: 2000 },
    { title: 'PROD: Memento', year: 2000 },
    { title: 'PROD: The Prestige', year: 2006 },
    { title: 'PROD: The Lion King', year: 1994 },
    { title: 'PROD: Apocalypse Now', year: 1979 },
    { title: 'PROD: Alien', year: 1979 },
    { title: 'PROD: Sunset Boulevard', year: 1950 },
    { title: 'PROD: Dr. Strangelove or: How I Learned to Stop Worrying and Love the Bomb', year: 1964 },
    { title: 'PROD: The Great Dictator', year: 1940 },
    { title: 'PROD: Cinema Paradiso', year: 1988 },
    { title: 'PROD: The Lives of Others', year: 2006 },
    { title: 'PROD: Grave of the Fireflies', year: 1988 },
    { title: 'PROD: Paths of Glory', year: 1957 },
    { title: 'PROD: Django Unchained', year: 2012 },
    { title: 'PROD: The Shining', year: 1980 },
    { title: 'PROD: WALL·E', year: 2008 },
    { title: 'PROD: American Beauty', year: 1999 },
]

const OrderSuggestion = ({
    value,
    valueHandler,
}) => {

    const options = top100Films.map((option) => {
        const delimiter = ": "
        const environment = option.title.split(delimiter)[0].toUpperCase()
        return {
            environment: environment,
            ...option,
        }
    })

    return (
        <Autocomplete
            id="order-suggestion"
            options={options.sort((a, b) => -b.environment.localeCompare(a.environment))}
            groupBy={(option) => option.environment}
            getOptionLabel={(option) => option.title}
            fullWidth
            renderInput={(params) => (
                <TextField 
                    {...params}
                    margin="normal"
                    label="Order ID"
                    variant="outlined"
                />
            )}
            renderOption={(option, { inputValue }) => {
                const matches = match(option.title, inputValue)
                const parts = parse(option.title, matches)

                return (
                    <div>
                        {parts.map((part, index) => (
                            <span key={index} style={{ fontWeight: part.highlight ? 700 : 400 }}>
                                {part.text}
                            </span>
                        ))}
                    </div>
                )
            }}
            value={value} 
            onChange={valueHandler}
        />
    )
}

export default OrderSuggestion
