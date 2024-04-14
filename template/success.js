const backBtn = document.querySelector('.form-submit')

const bill = localStorage.getItem("bill");

function start() {
    const payment = document.querySelector('#payment')
    const payment_id = document.querySelector('#payment_id')

    payment.innerText = bill.amount;
    payment_id.innerText = bill.fee_id;
}

backBtn.onclick = function(e) {
    e.preventDefault();
    window.location.href = './payment.html';
}