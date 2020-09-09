$(document).ready(function () {
    var form = $('form#stripe-payment-form');
    var strip_key = form.data('stripeKey');
    console.log(strip_key)
    var stripe = Stripe(strip_key);

    // Create an instance of Elements
    var elements = stripe.elements();

    // Custom styling can be passed to options when creating an Element.
    // (Note that this demo uses a wider set of styles than the guide below.)
    var style = {
        base: {
            color: '#32325d',
            lineHeight: '24px',
            fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
            fontSmoothing: 'antialiased',
            fontSize: '16px',
            '::placeholder': {
                color: '#aab7c4'
            }
        },
        invalid: {
            color: '#fa755a',
            iconColor: '#fa755a'
        }
    };

    // Create an instance of the card Element
    var card = elements.create('card', {hidePostalCode: true, style: style});

    // Add an instance of the card Element into the `card-element` <div>
    card.mount('#stripe-card-element');

    // Handle real-time validation errors from the card Element.
    card.addEventListener('change', function (event) {
        var displayError = document.getElementById('stripe-card-errors');
        if (event.error) {
            displayError.textContent = event.error.message;
        } else {
            displayError.textContent = '';
        }
    });

    var stripe_token = $('#id_stripe_token');

    // Handle form submission
    form.submit(function (e) {
        if (!stripe_token.val()) {
            e.preventDefault();

            stripe.createToken(card).then(function (result) {
                if (result.error) {
                    // Inform the user if there was an error
                    var errorElement = document.getElementById('stripe-card-errors');
                    errorElement.textContent = result.error.message;
                } else {
                    // Send the token to your server
                    stripe_token.val(result.token.id);
                    form.submit();
                }
            });
        }
    });
});
