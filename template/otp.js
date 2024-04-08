const confirmBtn = document.querySelector('.form-submit')

var validOtp = localStorage.getItem("otp");
var mainUser = localStorage.getItem("mainUser");
var inputId = localStorage.getItem("inputId");

confirmBtn.onclick = function(e) {
    e.preventDefault();
    let inputOtp = document.querySelector('#otp').value;
    if (inputOtp === validOtp) {
        const createTrans = 'http://127.0.0.1:8000/transactions/?otp=' + inputOtp;
        const updateBanlance = `http://127.0.0.1:8000/update_balance/?balance=${mainUser.balance - inputId.amount_due}&user_id=${mainUser.id}`
        fetch(createTrans)
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