const getUsersDetail = 'http://127.0.0.1:8000/users/?skip=0&limit=100';
const mainId = '3';

function start() {
    fetch(getUsersDetail)
        .then(function(responses) {
            return responses.json();
        })
        .then(function(usersDetail) {
            renderUser(usersDetail);
        })
}

function renderUser(usersDetail) {
    const mainUser = document.querySelector('#fullname')
    const mainPhone = document.querySelector('#phonenumber')
    const mainEmail = document.querySelector('#email')
    const mainCredit = document.querySelector('#credit')

    for (var i=0;i<usersDetail.length;i++)
    {
        if (usersDetail[i].id === mainId) {
            mainUser.setAttribute("placeholder", usersDetail[i].full_name)
            mainPhone.setAttribute("placeholder", usersDetail[i].phone_number)
            mainEmail.setAttribute("placeholder", usersDetail[i].email)
            mainCredit.innerText = usersDetail[i].balance + ' VNĐ'
            break;
        }
    }
}

let condition = document.querySelector('#checkbox');
const button = document.querySelector('button');

function getTransaction() {
    const id = document.querySelector('#mssv').value;
    const userPaymentName = document.querySelector('#studentname');
    const payment1 = document.querySelector('#payment1');
    const payment2 = document.querySelector('#payment2');
    condition.checked = false;
    button.classList.add('button-disable');

    const id_fees = 'http://127.0.0.1:8000/fees/' + id;
    fetch(id_fees)
        .then(function(response) {
            return response.json();
        })
        .then(function(userDetail) {
            const getUserById = 'http://127.0.0.1:8000/user/' + id;
            if (!Array.isArray(userDetail))
            {
                fetch(getUserById)
                    .then(function(response) {
                        return response.json();
                    })
                    .then(function(user) {
                        userPaymentName.setAttribute("placeholder", user.full_name);
                        payment1.innerText = '0 VNĐ';
                        payment2.innerText = '0 VNĐ';
                    })
            }
            else {
                fetch(getUserById)
                    .then(function(response) {
                        return response.json();
                    })
                    .then(function(user) {
                        userPaymentName.setAttribute("placeholder", user.full_name);
                        payment1.innerText = userDetail[0].amount_due + ' VNĐ';
                        payment2.innerText = userDetail[0].amount_due + ' VNĐ';
                    })
            }
        })
}

start();

condition.onclick = function(e) {
    const balance = parseFloat(document.querySelector('#credit').textContent);
    const payment = parseFloat(document.querySelector('#payment2').textContent);

    if (condition.checked == true && balance >= payment) {
        button.classList.remove('button-disable');
        button.disabled = false;
    }
    else {
        button.classList.add('button-disable');
        button.disabled = true;
    }
}

button.onclick = function(e) {
    e.preventDefault();
    input_id = document.querySelector('#mssv').value;
    fetch(getUsersDetail)
        .then(function(response) {
            return response.json();
        })
        .then(function(allUsers) {
            for (var i=0;i<allUsers.length;i++)
            {
                if (allUsers[i].id === mainId)
                {
                    localStorage.setItem("mainUser1_id", allUsers[i].id)
                    localStorage.setItem("mainUser1_balance", allUsers[i].balance)
                }
                if (allUsers[i].id == input_id)
                {
                    localStorage.setItem("inputId", allUsers[i])
                }
            }
            if (condition.checked == true) {
                const getFeeInputId = 'http://127.0.0.1:8000/fees/' + input_id; // Nguoi can dong hoc phi
        
                fetch(getFeeInputId)
                    .then(function(response) {
                        return response.json()
                    })
                    .then(function(fee) {
                        localStorage.setItem("fee_id", fee[0].id);
                        localStorage.setItem("fee", fee[0].amount_due);
                    })
                const send_otp = `http://127.0.0.1:8000/send_otp/?fee_id=${localStorage.getItem("fee_id").toString()}&user_id=${localStorage.getItem("mainUser1_id")}`
                fetch(send_otp , {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(null)
                })
                    .then(function(response) {
                        return response.json();
                    })
                    .then(function(otp_sent) {
                        window.location.href = './otp.html'
                    })
            }
        })
}
