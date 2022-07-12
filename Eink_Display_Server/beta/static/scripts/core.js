async function sha256(message) {
    // Băm chuỗi theo thuật toán sha256

    const msgBuffer = new TextEncoder().encode(message);
    const hashBuffer = await crypto.subtle.digest('SHA-256', msgBuffer);
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    const hashHex = hashArray.map(b => ('00' + b.toString(16)).slice(-2)).join('');

    return hashHex;
}

function parseDate(dateString) {
    const birth = new Date(dateString);  
    var day = birth.getDate().toString().padStart(2, '0');
    var month = birth.getMonth().toString().padStart( + 1).padStart(2, '0'); //January is 0!
    var year = birth.getFullYear().toString();
    var hour = birth.getHours().toString();
    var minute = birth.getMinutes().toString();
    var second = birth.getSeconds();
 
    const result = day + '/' + month + '/' + year + ' ' + hour + ':' + minute + ':' + second;
    // console.log('Token = ' + new Date(Date.UTC(year, month, day, hour, minute, second)))
    return new Date(Date.UTC(year, month, day, hour, minute, second));
}

function parseDateTime(value) {
    const birth = new Date(value);  
    var dd = String(birth.getDate()).padStart(2, '0');
    var mm = String(birth.getMonth() + 1).padStart(2, '0'); //January is 0!
    var yyyy = birth.getFullYear();
    var H = birth.getHours();
    var m = birth.getMinutes();
    var s = birth.getSeconds();

    const result = dd + '/' + mm + '/' + yyyy + ' ' + H + ':' + m + ':' + s;
    // console.log('Now = '+ new Date(result))
    return new Date(result);
}