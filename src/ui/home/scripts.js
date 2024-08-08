// import la fonction notification qUI EST DANS LE FICHIER SCRIPTS.JS
import { notification } from '../scripts.js';

function createInputPattern(loginOptions) {
    const loginButtonHolder = document.createElement('div');
    loginButtonHolder.classList.add('login-holder');

    const InputLabel = document.createElement('div');
    InputLabel.textContent = 'Input';
    InputLabel.classList.add('label-login');
    loginButtonHolder.appendChild(InputLabel);

    const InputPath = document.createElement('input');
    InputPath.setAttribute('type', 'text');
    InputPath.setAttribute('placeholder', 'Enter XPath of the input field');
    loginButtonHolder.appendChild(InputPath);

    const InputText = document.createElement('input');
    InputText.setAttribute('type', 'text');
    InputText.setAttribute('placeholder', 'Enter text to input');
    InputText.style.marginLeft = '10px';
    loginButtonHolder.appendChild(InputText);

    const cross = document.createElement('button');
    cross.classList.add('cross');
    cross.textContent = 'X';
    cross.addEventListener('click', () => {
        loginOptions.removeChild(loginButtonHolder);
    });
    loginButtonHolder.appendChild(cross);

    loginOptions.appendChild(loginButtonHolder);
}

function createClickPattern(loginOptions) {
    const loginButtonHolder = document.createElement('div');
    loginButtonHolder.classList.add('login-holder');

    const InputLabel = document.createElement('div');
    InputLabel.textContent = 'Click';
    InputLabel.classList.add('label-login');
    loginButtonHolder.appendChild(InputLabel);

    const ClickPath = document.createElement('input');
    ClickPath.setAttribute('type', 'text');
    ClickPath.setAttribute('placeholder', 'Enter XPath of the button to click');
    loginButtonHolder.appendChild(ClickPath);

    const cross = document.createElement('button');
    cross.classList.add('cross');
    cross.textContent = 'X';
    cross.addEventListener('click', () => {
        loginOptions.removeChild(loginButtonHolder);
    });
    loginButtonHolder.appendChild(cross);

    loginOptions.appendChild(loginButtonHolder);
}

function createLoginButtons(loginOptions) {
    const loginButtonHolder = document.createElement('div');
    loginButtonHolder.classList.add('login-holder');

    const loginButtonInput = document.createElement('button');
    loginButtonInput.classList.add('login-button');
    loginButtonInput.textContent = 'Add Input pattern';
    loginButtonInput.addEventListener('click', () => {
        loginOptions.removeChild(loginButtonHolder);
        createInputPattern(loginOptions);
        createLoginButtons(loginOptions);
    });
    loginButtonHolder.appendChild(loginButtonInput);

    const loginButtonClick = document.createElement('button');
    loginButtonClick.classList.add('login-button');
    loginButtonClick.textContent = 'Add Click pattern';
    loginButtonClick.addEventListener('click', () => {
        loginOptions.removeChild(loginButtonHolder);
        createClickPattern(loginOptions);
        createLoginButtons(loginOptions);
    });
    loginButtonHolder.appendChild(loginButtonClick);

    loginOptions.appendChild(loginButtonHolder);
}

function createInputButtons(inputOptions) {
    const loginButtonHolder = document.createElement('div');
    loginButtonHolder.classList.add('login-holder');

    const loginButtonInput = document.createElement('button');
    loginButtonInput.classList.add('login-button');
    loginButtonInput.textContent = 'Add Input pattern';
    loginButtonInput.addEventListener('click', () => {
        inputOptions.removeChild(loginButtonHolder);
        createInputPattern(inputOptions);
        createInputButtons(inputOptions);
    });
    loginButtonHolder.appendChild(loginButtonInput);

    inputOptions.appendChild(loginButtonHolder);
}

function createCardQueue(element, website, pos) {
    const card = document.createElement('div');
    card.classList.add('test-card');

    const cardTitle = document.createElement('h2');
    cardTitle.textContent = website['websiteURL'];
    card.appendChild(cardTitle);

    const position = document.createElement('p');
    position.textContent = 'Position in queue: ' + pos;
    card.appendChild(position);

    const maxRepeat = document.createElement('p');
    maxRepeat.textContent = 'Number of repeats: ' + website.maxRepeat;
    card.appendChild(maxRepeat);

    const maxTime = document.createElement('p');
    maxTime.textContent = 'Time per repeat: ' + website.maxTime + ' minutes';
    card.appendChild(maxTime);

    const buttonCancel = document.createElement('button');
    buttonCancel.textContent = 'Cancel';
    buttonCancel.addEventListener('click', () => {
        fetch(window.location.origin + '/api/cancel', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                id: website.id
            })
        }).then(response => {
            if (response.ok) {
                console.log('Success');
                element.removeChild(card);
            } else {
                console.error('Error: ' + response.status);
                notification('red', 'Error', 'An error occurred while cancelling the test');
            }
        }).catch(error => {
            console.error(error);
        });
    });
    card.appendChild(buttonCancel);

    element.appendChild(card);
}


function createCardTest(element, website) {
    const card = document.createElement('div');
    card.classList.add('test-card');

    const cardTitle = document.createElement('h2');
    cardTitle.textContent = website['websiteURL'];
    card.appendChild(cardTitle);

    let progressBar = document.createElement('div');
    progressBar.classList.add('progress-bar');

    let progress = document.createElement('div');
    progress.classList.add('progress');
    progress.style.width = (website.repeat * 100 / website.maxRepeat) + '%';
    progressBar.appendChild(progress);

    let spanProgress = document.createElement('span');
    spanProgress.textContent = website.repeat + '/' + website.maxRepeat + ' repeats';
    progressBar.appendChild(spanProgress);

    card.appendChild(progressBar);

    progressBar = document.createElement('div');
    progressBar.classList.add('progress-bar');

    progress = document.createElement('div');
    progress.classList.add('progress');
    progress.style.width = (website.time * 100 / website.maxTime) + '%';
    progressBar.appendChild(progress);

    spanProgress = document.createElement('span');
    spanProgress.textContent = website.time + '/' + website.maxTime + ' minutes';
    progressBar.appendChild(spanProgress);

    card.appendChild(progressBar);

    const result = document.createElement('div');
    result.classList.add('result');

    const pGoal = document.createElement('p');
    pGoal.textContent = 'Goal reached: ' + website.nbGoal;
    result.appendChild(pGoal);

    const pError = document.createElement('p');
    pError.textContent = 'Error found: ' + website.nbError;
    result.appendChild(pError);

    const buttonResult = document.createElement('button');
    buttonResult.textContent = 'Show result';
    buttonResult.addEventListener('click', () => {
        window.location.href = window.location.origin + '/result?id=' + website.id;
    });

    // si dans website la clé "map" n'existe pas alors on affiche pas le bouton
    if (website.repeat === website.maxRepeat && website.time === website.maxTime)
        result.appendChild(buttonResult);

    card.appendChild(result);

    element.appendChild(card);
}

document.addEventListener('DOMContentLoaded', () => {

    // Sliders
    const repeatsSlider = document.getElementById('repeats');
    const timePerRepeatSlider = document.getElementById('time-per-repeat');
    const repeatsValue = document.getElementById('repeats-value');
    const timePerRepeatValue = document.getElementById('time-per-repeat-value');

    timePerRepeatSlider.value = 10;
    timePerRepeatValue.textContent = timePerRepeatSlider.value;

    repeatsSlider.value = 10;
    repeatsValue.textContent = repeatsSlider.value;

    repeatsSlider.addEventListener('input', () => {
        repeatsValue.textContent = repeatsSlider.value;
    });

    timePerRepeatSlider.addEventListener('input', () => {
        timePerRepeatValue.textContent = timePerRepeatSlider.value;
    });

    //Login form
    const loginOptions = document.getElementById('login-options');
    const loginButton = document.getElementById('login-button');
    const loginTitle = document.getElementById('login-option-title');

    loginButton.addEventListener('click', () => {
        loginOptions.removeChild(loginButton);

        loginTitle.textContent = 'Make the pattern to login on your website';

        const loginURL = document.createElement('input');
        loginURL.setAttribute('type', 'text');
        loginURL.setAttribute('placeholder', 'Enter your login page URL');
        loginURL.setAttribute('id', 'login-url');
        loginOptions.appendChild(loginURL);

        createLoginButtons(loginOptions);
    });

    //Input form
    const inputOptions = document.getElementById('input-options');
    const inputButton = document.getElementById('input-button');

    inputButton.addEventListener('click', () => {
        inputOptions.removeChild(inputButton);
        createInputPattern(inputOptions);
        createInputButtons(inputOptions);
    });

    //Run button
    const runButton = document.getElementById('run-button');

    runButton.addEventListener('click', () => {

        const websiteURL = document.getElementById('website-url').value;
        const targetURL = document.getElementById('target-url').value;
        const inputOptions = document.getElementById('input-options');
        const loginOptions = document.getElementById('login-options');
        const repeats = repeatsSlider.value;
        const timePerRepeat = timePerRepeatSlider.value;

        const inputPattern = [];
        console.log(inputOptions.getElementsByClassName('login-holder').length);

        //how many login-holder elements are in inputOptions, if > 0, then we have login patterns
        if (inputOptions.getElementsByClassName('login-holder').length > 0) {

            const inputHolder = inputOptions.getElementsByClassName('login-holder');

            for (let i = 0; i < inputHolder.length; i++) {
                const inputOption = inputHolder[i];

                if (inputOption.getElementsByTagName('input').length === 0) {
                    continue;
                }

                const inputPath = inputOption.getElementsByTagName('input')[0].value;
                const inputValue = inputOption.getElementsByTagName('input')[1].value;

                inputPattern.push({
                    type: 'input',
                    XPath: inputPath,
                    value: inputValue
                });
            }
        }

        let loginURL = '';
        const patterns = [];

        if (loginOptions.getElementsByClassName('login-holder').length > 0) {
            loginURL = document.getElementById('login-url').value;
            const loginHolder = loginOptions.getElementsByClassName('login-holder');

            for (let i = 0; i < loginHolder.length; i++) {
                const loginOption = loginHolder[i];

                if (loginOption.getElementsByTagName('input').length === 0) {
                    continue;
                }

                const loginType = loginOption.getElementsByClassName('label-login')[0].textContent;
                console.log(loginType);

                if (loginType === 'Input') {
                    const inputPath = loginOption.getElementsByTagName('input')[0].value;
                    const inputValue = loginOption.getElementsByTagName('input')[1].value;

                    patterns.push({
                        type: 'input',
                        XPath: inputPath,
                        value: inputValue
                    });
                } else if (loginType === 'Click') {
                    const clickPath = loginOption.getElementsByTagName('input')[0].value;

                    patterns.push({
                        type: 'click',
                        XPath: clickPath
                    });
                }
            }
        }

        console.log('Run button clicked');

        fetch(window.location.origin + '/api/run', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                websiteURL,
                targetURL,
                "maxRepeat": repeats,
                "maxTime": timePerRepeat,
                loginURL,
                "loginPatterns": patterns,
                "inputPatterns": inputPattern
            })
        }).then(response => {
            if (response.ok) {
                console.log('Success');
            } else {
                console.error('Error: ' + response.status);
                notification('red', 'Error', 'An error occurred while running the test\nThe website may not be reachable');
            }
        }).catch(error => {
            console.error(error);
        });
    });

    //Call API for know the state of all the tests
    const queueCard = document.getElementById('queue-card');
    const testCard = document.getElementById('test-card');
    const completeCard = document.getElementById('complete-card');
    let lastProgress = false;

    function fetchTests() {
        fetch(window.location.origin + '/api/gettests', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        }).then(response => {
            if (response.ok) {
                return response.json();
            } else {
                console.error('Error: ' + response.status);
            }
        }).then(data => {
            console.log(data);

            if (lastProgress && data.testInProgress === null) {
                lastProgress = false;
                notification('green', 'Success', 'The test has been completed');
            }

            queueCard.innerHTML = '';
            testCard.innerHTML = '';
            completeCard.innerHTML = '';

            if (data.testInQueue.length > 0)
                for (let i = 0; i < data.testInQueue.length; i++)
                    createCardQueue(queueCard, data.testInQueue[i], i + 1);

            if (data.testInProgress !== null) {
                lastProgress = true;
                createCardTest(testCard, data.testInProgress);
            }

            if (data.testCompleted.length > 0)
                data.testCompleted.forEach(test => {
                    createCardTest(completeCard, test);
                });

        }).catch(error => {
            console.error(error);
        });
    }

    fetchTests();
    setInterval(fetchTests, 3000);

});
