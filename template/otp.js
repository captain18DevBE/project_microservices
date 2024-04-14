const confirmBtn = document.querySelector('.form-submit')

var validOtp = localStorage.getItem("otp");
var mainUser_id = localStorage.getItem("mainUser1_id");
var mainUser_balance = localStorage.getItem("mainUser1_balance");
var inputId = localStorage.getItem("inputId");

confirmBtn.onclick = function(e) {
    e.preventDefault();
    let inputOtp = document.querySelector('#otp').value;

    const createTrans = 'http://127.0.0.1:8000/transactions/?otp=' + inputOtp;
    if (inputOtp === validOtp) {
        const updateBanlance = `http://127.0.0.1:8000/update_balance/?balance=${mainUser_balance - inputId.amount_due}&user_id=${mainUser.id}`
        const data = {
            amount: localStorage.getItem("fee"),
            owner_id: mainUser_id,
            fee_id: localStorage.getItem("fee_id")
        }
        fetch(createTrans, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
            .then(function(response) {
                return response.json();
            })
            .then(function(bill) {
                localStorage.setItem('bill', bill);
                fetch(updateBanlance)
                    .then(function(response) {
                        return response.json();
                    })
                    .then(function(string) {
                        window.location.href = './success.html'
                    })
            })
    }
    else {
        const getError = document.querySelector('.form-message')
        getError.classList.add("error")
        getError.innerText = 'Mã OTP không hợp lệ'
    }
}