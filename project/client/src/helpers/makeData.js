import namor from 'namor'

const range = len => {
    const arr = []
    for (let i = 0; i < len; i++) {
        arr.push(i)
    }
    return arr
}

const newOrder = () => {
    return {
        usrId: namor.generate({ words: 1, numbers: 0 }),
        orderId: "",
        env: namor.generate({ words: 1, numbers: 0 }),
        name: namor.generate({ words: 1, numbers: 0 }),
        lut: "",
    }
}

export default function makeData(...lens) {
    const makeDataLevel = (depth = 0) => {
        const len = lens[depth]
        return range(len).map(d => {
            return {
                ...newOrder(),
                subRows: lens[depth + 1] ? makeDataLevel(depth + 1) : undefined,
            }
        })
    }

    return makeDataLevel()
}
