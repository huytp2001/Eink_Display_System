function loginCall(loginName, loginPwd, { complete, success, error }) {
    let reqData = {
        name: loginName,
        pwd: loginPwd
    };

    $.ajax({
        url: `/api/auth/login`,
        method: 'POST',
        dataType: "json",
        contentType: "application/json; charset=utf-8",
        data: JSON.stringify(reqData),
        complete: complete,
        success: success,
        error: error
    });
}

function updateAccountCall(name, oldPwd, newPwd, token, { complete, success, error }) {
    let reqData = {
        name: name,
        old_pwd: oldPwd,
        new_pwd: newPwd
    };

    $.ajax({
        url: `/api/sys/update-account`,
        method: 'POST',
        dataType: "json",
        contentType: "application/json; charset=utf-8",
        beforeSend: (request) => {
            request.setRequestHeader("access-token", token);
        },
        data: JSON.stringify(reqData),
        complete: complete,
        success: success,
        error: error
    });
}

function getAllSlaveCall(token, { complete, success, error }) {
    $.ajax({
        url: "/api/slave/all",
        dataType: "json",
        method: 'GET',
        beforeSend: (request) => {
            request.setRequestHeader("access-token", token);
        },
        complete: complete,
        success: success,
        error: error
    });
}

function scanSlaveCall(token, { complete, success, error }) {
    $.ajax({
        url: "/api/slave/scan",
        dataType: "json",
        method: 'GET',
        beforeSend: (request) => {
            request.setRequestHeader("access-token", token);
        },
        complete: complete,
        success: success,
        error: error
    });
}

function addSlaveCall(mac, deviceName, productName, productPrice, token, { complete, success, error }) {
    let postData = {
        mac: mac,
        device_name: deviceName,
        product_name: productName,
        product_price: productPrice
    };

    $.ajax({
        url: `/api/slave/add`,
        method: 'POST',
        dataType: "json",
        contentType: "application/json; charset=utf-8",
        data: JSON.stringify(postData),
        beforeSend: (request) => {
            request.setRequestHeader("access-token", token);
        },
        complete: complete,
        success: success,
        error: error
    });
}

function displayProductCall(mac, productName, productPrice, token, { complete, success, error }) {
    let postData = {
        mac: mac,
        product_name: productName,
        product_price: productPrice
    };

    $.ajax({
        url: `/api/slave/disp-product`,
        method: 'POST',
        dataType: "json",
        contentType: "application/json; charset=utf-8",
        data: JSON.stringify(postData),
        beforeSend: (request) => {
            request.setRequestHeader("access-token", token);
        },
        complete: complete,
        success: success,
        error: error
    });
}

function displayProductNameCall(mac, productName, token, type, { complete, success, error }) {
    let postData = {
        mac: mac,
        product_name: productName,
        type: type
    };

    $.ajax({
        url: `/api/slave/disp-product-name`,
        method: 'POST',
        dataType: "json",
        contentType: "application/json; charset=utf-8",
        data: JSON.stringify(postData),
        beforeSend: (request) => {
            request.setRequestHeader("access-token", token);
        },
        complete: complete,
        success: success,
        error: error
    });
}

function displayProductPriceCall(mac, productPrice, token, type, { complete, success, error }) {
    let postData = {
        mac: mac,
        product_price: productPrice,
        type: type
    };

    $.ajax({
        url: `/api/slave/disp-product-price`,
        method: 'POST',
        dataType: "json",
        contentType: "application/json; charset=utf-8",
        data: JSON.stringify(postData),
        beforeSend: (request) => {
            request.setRequestHeader("access-token", token);
        },
        complete: complete,
        success: success,
        error: error
    });
}

function displayRefreshCall(mac, token, type, { complete, success, error }) {
    let postData = {
        mac: mac,
        type: type
    }

    $.ajax({
        url: `/api/slave/disp-refresh`,
        method: 'POST',
        dataType: "json",
        contentType: "application/json; charset=utf-8",
        data: JSON.stringify(postData),
        beforeSend: (request) => {
            request.setRequestHeader("access-token", token);
        },
        complete: complete,
        success: success,
        error: error
    });
}


function displayRefreshAllCall(token, { complete, success, error }) {
    $.ajax({
        url: `/api/slave/disp-refresh-all`,
        method: 'POST',
        dataType: "json",
        contentType: "application/json; charset=utf-8",
        data: null,
        beforeSend: (request) => {
            request.setRequestHeader("access-token", token);
        },
        complete: complete,
        success: success,
        error: error
    });
}

function getSlaveCall(mac, token, { complete, success, error }) {
    $.ajax({
        url: `/api/slave/get?mac=${mac}`,
        dataType: "json",
        method: 'GET',
        beforeSend: (request) => {
            request.setRequestHeader("access-token", token);
        },
        complete: complete,
        success: success,
        error: error
    });
}

function removeSlaveCall(mac, token, { complete, success, error }) {
    $.ajax({
        url: `/api/slave/remove?mac=${mac}`,
        dataType: "json",
        method: 'POST',
        beforeSend: (request) => {
            request.setRequestHeader("access-token", token);
        },
        complete: complete,
        success: success,
        error: error
    });
}

function updateSlaveCall(mac, name, token, { complete, success, error }) {
    $.ajax({
        url: `/api/slave/update?mac=${mac}&name=${name}`,
        dataType: "json",
        method: 'POST',
        beforeSend: (request) => {
            request.setRequestHeader("access-token", token);
        },
        complete: complete,
        success: success,
        error: error
    });
}

function connectSlaveCall(mac, token, { complete, success, error }) {
    $.ajax({
        url: `/api/slave/connect?mac=${mac}`,
        dataType: "json",
        method: 'POST',
        beforeSend: (request) => {
            request.setRequestHeader("access-token", token);
        },
        complete: complete,
        success: success,
        error: error
    });
}
