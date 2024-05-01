const btnRock = document.getElementById('rock')
const btnSiccor = document.getElementById('siccor')
const btnPaper = document.getElementById('paper')
const docStatus = document.getElementById('status')
const docResult = document.getElementById('result')

const origin = window.location.origin
const clientId = Math.random()

const actionMap = {
    0: "石头",
    1: "剪刀",
    2: "布&emsp;"
}
const resultMap = {
    0: "平局了",
    1: "你赢了",
    2: "你输了"
}

let roundNum = 0, winNum = 0, loseNum = 0, nieNum = 0

const check = (playerAction, agentAction) => {
    if (playerAction == agentAction) return 0;
    else if ((playerAction + 1) % 3 == agentAction) return 1;
    else return 2;
}

const render = (playerAction, agentAction, result) => {
    roundNum++
    if (result === 1) winNum++
    else if (result === 2) loseNum++
    else nieNum++

    docStatus.innerHTML = 
        `第 ${roundNum} 轮：你出了${actionMap[playerAction]}，` +
        `智能体出了${actionMap[agentAction]}。<br>` +
        `${resultMap[result]}。 胜/负： ${winNum} / ${loseNum}。<br>` +
        docStatus.innerHTML
}

const action = (playerAction, agentAction) => {
    const result = check(playerAction, agentAction)
    render(playerAction, agentAction, result)
    
    fetch(origin + '/agent' + `?id=${clientId}`, {
        method: 'POST',
        headers: {
            "Content-Type": "text/plain",
	    "x-content-type-options": "nosniff"
        },
        body: `${playerAction},${agentAction},${result}`
    }).catch()
}

const round = (playerAction) => {
    fetch(origin + '/agent' + `?id=${clientId}`, {
        method: 'GET',
        headers: {
            "Content-Type": "text/plain",
            "x-content-type-options": "nosniff"
        }
    })
    .then((response) => {
        if (response.ok) {
            response.text().then((text) => action(playerAction, Number(text)))
        } else {
            action(playerAction, Math.floor(Math.random() * 3))
        }
    })
    .catch(() => action(playerAction, Math.floor(Math.random() * 3)))
}

btnRock.addEventListener('click', () => round(0))
btnSiccor.addEventListener('click', () => round(1))
btnPaper.addEventListener('click', () => round(2))

window.addEventListener('keydown', (ev) => {
    if (ev.code == 'Digit1') round(0)
    if (ev.code == 'Digit2') round(1)
    if (ev.code == 'Digit3') round(2)
})

const alive = () => {
    fetch(origin + '/agent' + `?id=${clientId}`, {
        method: 'POST',
        headers: {
            "Content-Type": "text/plain",
            "x-content-type-options": "nosniff"
        },
        body: 'alive'
    })
    .catch()
}

setInterval(alive, 60000)
