var listSlave = [];

function logout() {
    localStorage.clear();
    sessionStorage.clear();
    window.location = '/auth/login';
}

function refreshToken(callback) { 
    if (localStorage.getItem('loginName') !== null) {
        let timeDiff = +(parseDateTime(new Date)) - +parseDate(sessionStorage.getItem('tokenExpired'));
 
        console.log(timeDiff);
        if (timeDiff >= -300000) { // 300000 = 5 phut
            loginCall(localStorage.getItem('loginName'), localStorage.getItem('pwdHash'), {
                complete: () => {},
                success: (response) => {
                    if (response.code === '0') {
                        sessionStorage.setItem('token', response.data.token);
                        sessionStorage.setItem('tokenExpired', response.data.expired);

                        callback();
                    } else {
                        alert('Failed refresh API token, loggin out...');
                        logout();
                    }
                },
                error: () => {
                    alert('Failed refresh API token, loggin out...');
                    logout();
                }
            });
        } else {
            callback();
        }
    } else {
        alert('Missing login data, logging out...');
        logout();
    }
}

function updateAccount() {
    let loginName = $('#js-login-name').val();
    let oldPwd = $('#js-old-pwd').val();
    let newPwd = $('#js-new-pwd').val();
    let reNewPwd = $('#js-re-new-pwd').val();

    if (newPwd !== reNewPwd) {
        $('#js-new-pwd').val('');
        $('#js-re-new-pwd').val('');

        alert('New password not match');
        return;
    }

    refreshToken(() => {
        updateAccountCall(loginName, oldPwd, newPwd, sessionStorage.getItem('token'), {
            complete: () => {},
            success: (response) => {
                if (response.code === '0') {
                    alert(response.msg);
                    localStorage.setItem('loginName', loginName);
                    localStorage.setItem('pwdHash', newPwd);
                    
                    window.location = '/auth/login';
                } else {
                    alert(response.msg);
                }
            },
            error: () => {
                alert('Update account failed, try again later...');
            }
        })
    });
}

function fetchConnectedSlaves() {
    this.listSlave = [];
    $('#js-reloader').addClass('disabled'); 
    refreshToken(() => {
        getAllSlaveCall(sessionStorage.getItem('token'), {
            complete: () => {
                $('#js-reloader').removeClass('disabled');
            },
            success: (jsonData) => {
                if (jsonData.code !== '0') {
                    alert('Could not get slave data, redirect to dashboard...');
                    window.location = '/';
                }
    
                $('#js-slave-table').empty();
                if (jsonData.data.length === 0) {
                    $('#js-slave-table').append('<tr><td colspan="5">No data found</td></tr>');
                }
                
                jsonData.data.forEach((slave, index) => {
                    this.listSlave.push(slave); 
                    let rowTemplate =
                        `<tr>` +
                        `<td>${index + 1}</td>` +
                        `<td>${slave.mac}</td>` +
                        `<td>${slave.device_name}</td>` +
                        `<td>${slave.product_name}</td>` +
                        `<td>${slave.product_price}</td>` +
                        `<td class="p-1 text-center">
                            ${(slave.run_time === 1) ? 
                                "<a class='btn' style='color: green'>Connected</a>" : 
                                `<a href='javascript:connectSlave("${slave.mac}")' class='btn btn-warning'>Connect</a>`}
                        </td>` +
                        `<td class="p-1 text-center">
                            <a href="${slave.mac.replace(/:/g, '%3A')}" class="btn btn-primary text-light">Details</a>
                        </td>` +
                        '</tr>'; 
    
                    $('#js-slave-table').append(rowTemplate);
                });
            },
            error: () => {
                alert('Could not get slave data, redirect to dashboard...');
                window.location = '/';
            }
        });
    });
}

function connectSlave(mac) {  
    refreshToken(() => {
        connectSlaveCall(mac, sessionStorage.getItem('token'), {
            complete: () => {
                
            },
            success: (jsonData) => {
                alert(jsonData.msg)
                if (jsonData.code === '0') {
                    this.fetchConnectedSlaves()
                }
            },
            error: () => {
                alert('Task failed');
            }
        });
    });
}

function slaveScan() {
    $('#js-reloader').addClass('disabled');
    refreshToken(() => {
        scanSlaveCall(sessionStorage.getItem('token'), {
            complete: () => {
                $('#js-reloader').removeClass('disabled');
            },
            success: (jsonData) => {
                if (jsonData.code !== '0') {
                    alert('Could not get slave data, redirect to dashboard...');
                    window.location = '/';
                }

                $('#js-slave-table').empty();
                if (jsonData.data.length === 0) {
                    $('#js-slave-table').append('<tr><td colspan="3">No data found</td></tr>');
                }
                jsonData.data.forEach(slave => {
                    let rowTemplate =
                        '<tr>' +
                        `<td>${slave.mac}</td>` +
                        `<td>${slave.network_name}</td>` +
                        `<td class="p-1 text-center"><a href="${slave.mac.replace(/:/g, '%3A')}/test" class="btn btn-primary text-light">Details</a></td>` +
                        '</tr>';


                    $('#js-slave-table').append(rowTemplate);
                });
            },
            error: () => {
                alert('Could not get slave data, redirect to dashboard...');
                window.location = '/';
            }
        });
    });
}

function addSlave() {
    $('#js-add').addClass('disabled');
    let mac = $('#js-mac').html();
    let deviceName = $('#js-device-name').val();
    let productName = $('#js-product-name').val();
    let productPrice = $('#js-product-price').val();

    if (!mac) {
        alert('Provide MAC first');
        $('#js-add').removeClass('disabled');
        return;
    }
    if (!deviceName) {
        alert('Provide device name first');
        $('#js-add').removeClass('disabled');
        return;
    }
    refreshToken(() => {
        addSlaveCall(mac, deviceName, productName, productPrice, sessionStorage.getItem('token'), {
            complete: () => {
                $('#js-add').removeClass('disabled');
            },
            success: (response) => {
                if (response.code !== '0') {
                    alert(response.msg);
                    return;
                }

                window.location = '/slave/scan';
            },
            error: () => {
                alert('Task failed');
            }
        });
    });
}

function displayProductName(type = 'test') {
    $('#js-dpn').addClass('disabled');
    let mac = $('#js-mac').html();
    let productName = $('#js-product-name').val();

    if (!mac) {
        $('#js-dpn').removeClass('disabled');
        alert('Provide MAC first');
        return;
    }

    refreshToken(() => {
        displayProductNameCall(mac, productName, sessionStorage.getItem('token'), type, {
            complete: () => {
                $('#js-dpn').removeClass('disabled');
            },
            success: (response) => {
                alert(response.msg);
            },
            error: () => {
                alert('Task failed');
            }
        });
    });
} 

function displayProduct(mac, name, price) {    
    displayProductCall(mac, name, price, sessionStorage.getItem('token'), {
        complete: () => {
            
        },
        success: (response) => {
            if (response.code !== '0') {
                alert(response.msg + ', ' + response.data); 
            }else {
                alert(response.msg);
            }
            
            if (response.code === '0') {
                this.fetchConnectedSlaves();
                this.hideBtn();
            }
        },
        error: () => {
            alert('Task failed');
        }
    }); 
}

function displayRefreshAll() {
    refreshToken(() => {
        displayRefreshAllCall(sessionStorage.getItem("token"), {
            complete: () => {
                
            },
            success: (response) => {
                if (response.code !== '0') {
                    alert(response.msg + ', ' + response.data); 
                }else {
                    alert(response.msg);
                }
            },
            error: () => {
                alert('Task failed');
            }
        });
    });
}

function displayProductPrice(type = 'test') {
    $('#js-dpp').addClass('disabled');
    let mac = $('#js-mac').html();
    let productPrice = $('#js-product-price').val();

    if (!mac) {
        $('#js-dpp').removeClass('disabled');
        alert('Provide MAC first');
        return;
    }

    refreshToken(() => {
        displayProductPriceCall(mac, productPrice, sessionStorage.getItem('token'), type, {
            complete: () => {
                $('#js-dpp').removeClass('disabled');
            },
            success: (response) => {
                alert(response.msg);
            },
            error: () => {
                alert('Task failed');
            }
        });
    });
}

function displayRefresh(type = 'test') {
    $('#js-drf').addClass('disabled');
    let mac = $('#js-mac').html();

    if (!mac) {
        $('#js-drf').removeClass('disabled');
        alert('Provide MAC first');
        return;
    }

    refreshToken(() => {
        displayRefreshCall(mac, sessionStorage.getItem("token"), type, {
            complete: () => {
                $('#js-drf').removeClass('disabled');
            },
            success: (response) => {
                alert(response.msg);
            },
            error: () => {
                alert('Task failed');
            }
        });
    });
}

function getCurrentSlave() {
    let currentMac = $('#js-mac').html();
    refreshToken(() => {
        getSlaveCall(currentMac, sessionStorage.getItem("token"), {
            success: (jsonData) => {
                if (jsonData.code !== '0') {
                    alert('Could not get slave data, redirect to dashboard...');
                    window.location = '/';
                }

                $("#js-device-name").val(jsonData.data.device_name);
                $("#js-product-name").val(jsonData.data.product_name);
                $("#js-product-price").val(jsonData.data.product_price);
            },
            error: () => {
                alert('Could not get slave data, redirect to dashboard...');
                window.location = '/';
            }
        });
    });
}

function updateSlave() {
    let currentMac = $('#js-mac').html();
    let updatedName = $('#js-device-name').val();
    refreshToken(() => {
        updateSlaveCall(currentMac, updatedName, sessionStorage.getItem("token"), {
            success: (jsonData) => {
                if (jsonData.code !== '0') {
                    alert(jsonData.msg);
                }

                if (jsonData.code === '0') {
                    alert(jsonData.msg);
                }

                window.location.reload();
            },
            error: () => {
                alert('Task failed successfully');
            }
        });
    });
}

function removeSlave() {
    if (!confirm('Are you sure to delete this slave?')) {
        return;
    }

    let currentMac = $('#js-mac').html();
    refreshToken(() => {
        removeSlaveCall(currentMac, sessionStorage.getItem("token"), {
            success: (jsonData) => {
                if (jsonData.code !== '0') {
                    alert(jsonData.msg);
                }

                window.location = '/slave';
            },
            error: () => {
                alert('Task failed successfully');
            }
        });
    });
}

function editDataSlave() 
{ 
    this.showBtn();

    if (this.listSlave.length > 0) {
        $('#js-slave-table').empty();
        this.listSlave.forEach((slave, index) => { 
            let rowTemplate =
                '<tr>' +
                `<td>${index + 1}</td>` +
                `<td>${slave.mac}</td>` +
                `<td>${slave.device_name}</td>` +
                `<td><input id="${slave.mac}name" value="${slave.product_name}"/></td>` +
                `<td><input id="${slave.mac}price" value="${slave.product_price}"/></td>` +
                `<td class="p-1 text-center">
                    ${(slave.run_time === 1) ? 
                        "<a class='btn' style='color: green'>Connected</a>" : 
                        `<a href='javascript:connectSlave("${slave.mac}")' class='btn btn-warning'>Connect</a>`}
                </td>` +
                `<td class="p-1 text-center"><a href="${slave.mac.replace(/:/g, '%3A')}" class="btn btn-primary text-light">Details</a></td>` +
                '</tr>'; 

            $('#js-slave-table').append(rowTemplate);
        });
    }
}

function cancelEditDataSlave() 
{ 
    this.hideBtn(); 
    this.fetchConnectedSlaves();
} 

function saveEditDataSlave() 
{  
    this.listSlave.forEach(element => {
        var name = document.getElementById(element.mac + 'name').value;
        var price = document.getElementById(element.mac + 'price').value; 

        displayProduct(element.mac, name, price);
    });
    this.hideBtn(); 
    this.fetchConnectedSlaves();
}

function refetchSlave() 
{  
    displayRefreshAll();
}

function showBtn() {
    $('#btnEdit').hide();
    $('#btnCancel').show();
    $('#btnSave').show();
    $('#btnFetch').show();
}

function hideBtn() {
    $('#btnCancel').hide();
    $('#btnSave').hide();
    $('#btnEdit').show();
    $('#btnFetch').hide();
}

function dropDownPwdModal() { 
    var loginName = localStorage.getItem('loginName');
    $('#js-login-name').val(loginName);
    var doc = document.getElementById("password-modal");
    if (doc.style.display === "none") {
        doc.style.display = "block";
    }else {
        doc.style.display = "none";
    }
}