require('dotenv').config()

const express = require('express')
const app = express()
const bodyParser = require('body-parser');
app.set("view engine", "ejs")
app.use(express.static('public'))
app.use(express.json())
app.use(bodyParser.urlencoded({extended: true}))
app.use(bodyParser.json())

const paypal = require('@paypal/checkout-server-sdk')
const Environment = process.env.NODE_ENV === 'production' ? paypal.core.LiveEnvironment : paypal.core.SandboxEnvironment
const paypalClient = new paypal.core.PayPalHttpClient(new Environment(process.env.PAYPAL_CLIENT_ID, process.env.PAYPAL_CLIENT_SECRET))

app.get('/payment/', (req, res) => {
    res.render('index', { paypalClientId: process.env.PAYPAL_CLIENT_ID,})
})

app.post('/payment/create-order', async (req, res) => {

    const totalAmount = req.body.items.reduce((total, item) => {
        const itemAmount = parseFloat(item.price) * parseInt(item.quantity, 10);
        return total + itemAmount
    }, 0);

    const request = new paypal.orders.OrdersCreateRequest()
    request.prefer("return=representation")
    request.requestBody( {
        intent: 'CAPTURE',
        purchase_units: [
            {
                amount: {
                    currency_code: 'EUR',
                    value: totalAmount.toFixed(2),
                },
                description: 'Payment description',
                items: req.body.items,
            },
        ],
    });

    try{
        const order = await paypalClient.execute(request)
        res.json({ id: order.result.id})
    } catch(e) {
        res.status(500).json({ error: e.message })
    }
})

app.listen(4000)