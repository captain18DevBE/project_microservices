
const submit = document.querySelector('.form-submit');
submit.onclick = function(e) {
    e.preventDefault();
    fetch(usersApi)
        .then(function(responses) {
            return responses.json();
        })
        .then(function(users) {
            const mssv = document.querySelector('#mssv').value;
            const password = document.querySelector('#password').value;
            var flag = true;
            for (var i=0; i<users.length; i++) {
                if (users[i].MSSV === mssv && users[i].password === password)
                {
                    console.log('Dang nhap thanh cong')
                    flag = false;
                    break;
                    window.location.href = './payment.html';
                }
            }
            if (flag)
            {
                console.log('Dang nhap that bai');
                e.preventDefault();
            }
        })
}

// function checkLogin(users) {
//     const mssv = document.querySelector('#mssv').value;
//     const password = document.querySelector('#password').value;
//     var flag = true;
//     for (var i=0; i<users.length; i++) {
//         if (users[i].MSSV === mssv && users[i].password === password)
//         {

//             flag = false;
//             break;
//         }
//     }
//     if (flag)
//     {
//         console.log('Dang nhap that bai');
//     }
// }