require('dotenv').config()

const express = require('express')
const app = express()
app.set("view engine", "ejs")
app.use(express.static('public'))
app.use(express.json())

const paypal = require('@paypal/checkout-server-sdk')
const Environment = process.env.NODE_ENV === 'production' ? paypal.core.LiveEnvironment : paypal.core.SandboxEnvironment
const paypalClient = new paypal.core.PayPalHttpClient(new Environment(process.env.PAYPAL_CLIENT_ID, process.env.PAYPAL_CLIENT_SECRET))

app.get('/payment/', (req, res) => {
    res.render('index', { paypalClientId: process.env.PAYPAL_CLIENT_ID,})
})

app.post('/payment/create-order', async (req, res) => {
    const { items } = req.body;

    const itemList = items.map((item) => ({
        name: item.name,
        sku: item.sku,
        price: item.price,
        currency: item.currency,
        quantity: item.quantity,
    }));

    const totalAmount = items.reduce((total, item) => {
        const itemAmount = parseFloat(item.price) * parseInt(item.quantity);
        return total + itemAmount
    }, 0);
    
    const createPaymentJson = {
        intent: 'sale',
        payer: {
            payment_method: 'paypal',   // ?? talvez obriga a meter pagamento com paypal
        },
        redirect_urls: {
            return_url: '/success',
            cancel_url: '/cancel',
        },
        transactions: [
            {
                item_list: {
                    items: itemList,
                },
                amonut: {
                    currency: 'EUR',
                    total: totalAmount.toFixed(2),
                },
                description: 'Payment description',
            },
        ],
    };

    paypal.payment.create(createPaymentJson, (error, payment) => {
        if (error) {
          throw error;
        } else {
          // Redirect user to PayPal for approval
          res.redirect(payment.links[1].href);
        }
      });
})
    
app.get('/success', (req, res) => {
    const payerId = req.query.PayerID;
    const paymentId = req.query.paymentId;
      
    const executePaymentJson = {
        payer_id: payerId,
    };
      
    paypal.payment.execute(paymentId, executePaymentJson, (error, payment) => {
        if (error) {
            throw error;
        } else {
            // Payment successful, handle the transaction
            res.send('Payment successful!');

        }
    });
});
      
app.get('/cancel', (req, res) => {
    // Handle cancellation
    res.send('Payment cancelled!');
});

app.listen(4000)