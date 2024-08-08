let currentCode = null;

function createTestResultContainer(container, testResult) {
    const urlParams = new URLSearchParams(window.location.search);
    const id = urlParams.get('id');

    const testResultContainer = document.createElement('div');
    testResultContainer.className = 'testResultContainer';
    container.appendChild(testResultContainer);

    const testResultImage = document.createElement('img');
    testResultImage.src = 'data:image/png;base64,' + testResult.image;
    testResultImage.style.width = '100%';
    testResultContainer.appendChild(testResultImage);

    const bottomContainer = document.createElement('div');
    bottomContainer.className = 'bottomContainer';
    
    const reasonElement = document.createElement('pre');
    reasonElement.className = 'reason';
    reasonElement.innerHTML = testResult.reason;
    bottomContainer.appendChild(reasonElement);

    const buttonContainer = document.createElement('div');
    buttonContainer.className = 'buttonContainer';

    let buttonSelenium = document.createElement('button');
    buttonSelenium.innerHTML = 'Generate Selenium test';
    buttonSelenium.className = 'buttonGen';
    buttonSelenium.addEventListener('click', () => {
        const previousCode = testResultContainer.getElementsByClassName('codeContainer');
        
        if (previousCode.length > 0 && currentCode === 'selenium') {
            buttonSelenium.classList.remove('buttonGenSelected');

            for (const code of previousCode) {
                code.remove();
            }
            return;
        }

        fetch(window.location.origin + '/api/generateTest?id=' + id + '&nodeId=' + testResult.id + '&language=selenium', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            currentCode = 'selenium';

            for (const buttonC of buttonContainer.children) {
                buttonC.classList.remove('buttonGenSelected');
            }
            buttonSelenium.classList.add('buttonGenSelected');

            const previousCode = testResultContainer.getElementsByClassName('codeContainer');
            for (const code of previousCode) {
                code.remove();
            }

            const codeContainer = document.createElement('div');
            codeContainer.className = 'codeContainer';

            const seleniumCodeElement = document.createElement('pre');
            seleniumCodeElement.innerHTML = data.code;
            seleniumCodeElement.classList.add('code');
            codeContainer.appendChild(seleniumCodeElement);

            bottomContainer.appendChild(codeContainer);
        });
    });
    buttonContainer.appendChild(buttonSelenium);

    let buttonPlayPy = document.createElement('button');
    buttonPlayPy.innerHTML = 'Generate Playwright Python test';
    buttonPlayPy.className = 'buttonGen';
    buttonPlayPy.addEventListener('click', () => {
        const previousCode = testResultContainer.getElementsByClassName('codeContainer');
        
        if (previousCode.length > 0 && currentCode === 'playwrightPython') {
            buttonPlayPy.classList.remove('buttonGenSelected');

            for (const code of previousCode) {
                code.remove();
            }
            return;
        }

        fetch(window.location.origin + '/api/generateTest?id=' + id + '&nodeId=' + testResult.id + '&language=playwrightPython', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            currentCode = 'playwrightPython';

            for (const buttonC of buttonContainer.children) {
                buttonC.classList.remove('buttonGenSelected');
            }
            buttonPlayPy.classList.add('buttonGenSelected');

            const previousCode = testResultContainer.getElementsByClassName('codeContainer');
            for (const code of previousCode) {
                code.remove();
            }

            const codeContainer = document.createElement('div');
            codeContainer.className = 'codeContainer';

            const playwrightCodeElement = document.createElement('pre');
            playwrightCodeElement.innerHTML = data.code;
            playwrightCodeElement.classList.add('code');
            codeContainer.appendChild(playwrightCodeElement);

            bottomContainer.appendChild(codeContainer);
        });
    });
    buttonContainer.appendChild(buttonPlayPy);

    let buttonPlayJS = document.createElement('button');
    buttonPlayJS.innerHTML = 'Generate Playwright JavaScript test';
    buttonPlayJS.className = 'buttonGen';
    buttonPlayJS.addEventListener('click', () => {
        const previousCode = testResultContainer.getElementsByClassName('codeContainer');
        
        if (previousCode.length > 0 && currentCode === 'playwrightJavaScript') {
            buttonPlayJS.classList.remove('buttonGenSelected');

            for (const code of previousCode) {
                code.remove();
            }
            return;
        }

        fetch(window.location.origin + '/api/generateTest?id=' + id + '&nodeId=' + testResult.id + '&language=playwrightJavaScript', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            currentCode = 'playwrightJavaScript';

            for (const buttonC of buttonContainer.children) {
                buttonC.classList.remove('buttonGenSelected');
            }
            buttonPlayJS.classList.add('buttonGenSelected');

            const previousCode = testResultContainer.getElementsByClassName('codeContainer');
            for (const code of previousCode) {
                code.remove();
            }

            const codeContainer = document.createElement('div');
            codeContainer.className = 'codeContainer';

            const playwrightCodeElement = document.createElement('pre');
            playwrightCodeElement.innerHTML = data.code;
            playwrightCodeElement.classList.add('code');
            codeContainer.appendChild(playwrightCodeElement);

            bottomContainer.appendChild(codeContainer);
        });
    });
    buttonContainer.appendChild(buttonPlayJS);

    let buttonPlayJava = document.createElement('button');
    buttonPlayJava.innerHTML = 'Generate Playwright Java test';
    buttonPlayJava.className = 'buttonGen';
    buttonPlayJava.addEventListener('click', () => {
        const previousCode = testResultContainer.getElementsByClassName('codeContainer');
        
        if (previousCode.length > 0 && currentCode === 'playwrightJava') {
            buttonPlayJava.classList.remove('buttonGenSelected');

            for (const code of previousCode) {
                code.remove();
            }
            return;
        }

        fetch(window.location.origin + '/api/generateTest?id=' + id + '&nodeId=' + testResult.id + '&language=playwrightJava', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            currentCode = 'playwrightJava';

            for (const buttonC of buttonContainer.children) {
                buttonC.classList.remove('buttonGenSelected');
            }
            buttonPlayJava.classList.add('buttonGenSelected');

            const previousCode = testResultContainer.getElementsByClassName('codeContainer');
            for (const code of previousCode) {
                code.remove();
            }

            const codeContainer = document.createElement('div');
            codeContainer.className = 'codeContainer';

            const playwrightCodeElement = document.createElement('pre');
            playwrightCodeElement.innerHTML = data.code;
            playwrightCodeElement.classList.add('code');
            codeContainer.appendChild(playwrightCodeElement);

            bottomContainer.appendChild(codeContainer);
        });
    });
    buttonContainer.appendChild(buttonPlayJava);

    let buttonRobot = document.createElement('button');
    buttonRobot.innerHTML = 'Generate Robot Python test';
    buttonRobot.className = 'buttonGen';
    buttonRobot.addEventListener('click', () => {
        const previousCode = testResultContainer.getElementsByClassName('codeContainer');
        
        if (previousCode.length > 0 && currentCode === 'robot') {
            buttonRobot.classList.remove('buttonGenSelected');

            for (const code of previousCode) {
                code.remove();
            }
            return;
        }

        fetch(window.location.origin + '/api/generateTest?id=' + id + '&nodeId=' + testResult.id + '&language=robot', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            currentCode = 'robot';

            for (const buttonC of buttonContainer.children) {
                buttonC.classList.remove('buttonGenSelected');
            }
            buttonRobot.classList.add('buttonGenSelected');

            const previousCode = testResultContainer.getElementsByClassName('codeContainer');
            for (const code of previousCode) {
                code.remove();
            }

            const codeContainer = document.createElement('div');
            codeContainer.className = 'codeContainer';

            const titleCodeElement = document.createElement('h3');
            titleCodeElement.innerHTML = 'variables.py';
            codeContainer.appendChild(titleCodeElement);

            const robotVariableCodeElement = document.createElement('pre');
            robotVariableCodeElement.innerHTML = data.code.variables;
            robotVariableCodeElement.classList.add('code');
            codeContainer.appendChild(robotVariableCodeElement);

            const titleCodeElement2 = document.createElement('h3');
            titleCodeElement2.innerHTML = 'robot.robot';
            codeContainer.appendChild(titleCodeElement2);

            const robotCodeElement = document.createElement('pre');
            robotCodeElement.innerHTML = data.code.robot;
            robotCodeElement.classList.add('code');
            codeContainer.appendChild(robotCodeElement);

            bottomContainer.appendChild(codeContainer);
        });
    });
    buttonContainer.appendChild(buttonRobot);

    bottomContainer.appendChild(buttonContainer);

    testResultContainer.appendChild(bottomContainer);
}

document.addEventListener('DOMContentLoaded', () => {
    // get the id in the url
    const urlParams = new URLSearchParams(window.location.search);
    const id = urlParams.get('id');
    console.log(id);

    // map the website
    let webmap = document.getElementById('webmap');
    webmap.innerHTML = '';

    fetch(window.location.origin + '/api/result?id=' + id, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);

        const h1Element = document.getElementById('websiteURL');
        h1Element.innerHTML = data.websiteURL;

        const imgElement = document.createElement('img');
        imgElement.src = 'data:image/png;base64,' + data.websiteMap;
        imgElement.style.width = '100%';
        webmap.appendChild(imgElement);

        const errorsContainer = document.getElementById('errors');

        const errorsElement = document.createElement('h2');
        errorsElement.innerHTML = 'Errors : ' + data.errorNodeList.length + ' errors found';
        errorsContainer.appendChild(errorsElement);

        for (const error of data.errorNodeList) {
            createTestResultContainer(errorsContainer, error);
        }

        const goalContainer = document.getElementById('goals');

        const goalElement = document.createElement('h2');
        goalElement.innerHTML = 'Goals : ' + data.goalNodeList.length + ' goal reached';
        goalContainer.appendChild(goalElement);

        for (const goal of data.goalNodeList) {
            createTestResultContainer(goalContainer, goal);
        }
    });
});