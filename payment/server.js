require('dotenv').config()

const express = require('express')
const app = express()
app.set("view engine", "ejs")
app.use(express.static('public'))
app.use(express.json())

const paypal = require('@paypal/checkout-server-sdk')
const Environment = process.env.NODE_ENV === 'production' ? paypal.core.LiveEnvironment : paypal.core.SandboxEnvironment
const paypalClient = new paypal.core.PayPalHttpClient(new Environment(process.env.PAYPAL_CLIENT_ID, process.env.PAYPAL_CLIENT_SECRET))

// const storeItems = new Map([
    // [1, { price: 1, name: "yeet"}],
    // [2, { price: 2, name: "yeeeeeet"}],
// ])

app.get('/', (req, res) => {
    res.render('index', { paypalClientId: process.env.PAYPAL_CLIENT_ID,})
})

app.post('/create-order/:orderId', async (req, res) => {
    const request = new paypal.orders.OrdersCreateRequest()
    const storeItems = req.params.orderId
    const total = req.body.items.reduce((sum, item) => {
        return sum + storeItems.get(item.id).price
    }, 0)
    request.prefer("return=representation")
    request.requestBody({
        intent: 'CAPTURE',
        purchase_units: [
            {
                amount: {
                    currency_code: 'EUR',
                    value: total,
                    breakdown: {
                        item_total: {
                            currency_code: "EUR",
                            value: total
                        }
                    }
                },
                items: req.body.items.map(item => {
                    const storeItem = storeItems.get(item.id)
                    return{
                        name: storeItem.name,
                        unit_amount: {
                            currency_code: "EUR",
                            value: storeItem.price
                        },
                        quantity: item.quantity
                    }
                })
            }
        ]
    })

    try{
        const order = await paypalClient.execute(request)
        res.json({ id: order.result.id})
    } catch(e) {
        res.status(500).json({ error: e.message })
    }
})

app.listen(4000)