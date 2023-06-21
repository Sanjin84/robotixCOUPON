function redeemCoupon() {
    const couponCode = document.getElementById('couponCode').value;
    console.log('Coupon:', couponCode);

    fetch('https://ru9y4i71s1.execute-api.ap-southeast-2.amazonaws.com/v5', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ coupon: couponCode }),
    })
        .then(response => response.json())
        .then(data => {
            console.log('Response:', data);  // print the full response
            if (data.message.startsWith("Your link: ")) {
                var link = document.getElementById('link');
                link.href = data.message.replace("Your link: ", "");
                link.textContent = "Arduino Zero to Hero FREE SIGNUP";
                link.style.display = "block";
            } else {
                document.getElementById('message').textContent = data.message;
            }
        })
        .catch((error) => {
            console.error('Error:', error);
        });
}
